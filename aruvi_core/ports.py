"""
Adapter ports — the seams that keep Aruvi free of vendor lock-in.

Core logic depends only on these abstract Protocols; each vendor (Anthropic, Supabase,
Upstash, Razorpay, ...) is a thin adapter implementing one of them, wired in at the edge.
Swapping a provider = write one adapter, never touch the engine or app. This is the same
pattern the prototype's `llm_client.py` already proved, applied across the board.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Protocol, Union, runtime_checkable


# ── LLM provider ──────────────────────────────────────────────────────────────
@dataclass
class Prompt:
    system: str
    messages: List[Dict[str, Any]]
    max_tokens: int = 32000
    cache_system: bool = True  # turn on Anthropic prompt-caching for the static constitution block


@dataclass
class LLMResponse:
    text: str
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0


@runtime_checkable
class LLMClient(Protocol):
    """Port over the model provider. Aruvi is certified Claude-only today; the Anthropic
    adapter is the one implementation. A version bump or provider swap is one adapter."""
    def generate(self, prompt: Prompt) -> LLMResponse: ...


# ── Output cache: the #1 economic lever ────────────────────────────────────────
@runtime_checkable
class OutputCache(Protocol):
    """Keyed by (subject, grade, chapter, normalized period_profile, constitution_version).
    A hit means the model is never called — the profitability hinge at seasonal volume.
    Applied by the service layer that wraps the engine, not by the engine itself."""
    def get(self, key: str) -> Optional[Dict[str, Any]]: ...
    def put(self, key: str, value: Dict[str, Any]) -> None: ...


# ── Object storage (generated PDFs / artifacts) ────────────────────────────────
@runtime_checkable
class Storage(Protocol):
    def put_bytes(self, path: str, data: bytes, content_type: str = "application/octet-stream") -> str: ...
    def get_bytes(self, path: str) -> bytes: ...
    def url_for(self, path: str) -> str: ...


# ── Tenant data (plans, feedback, cost ledger) ─────────────────────────────────
@runtime_checkable
class Repository(Protocol):
    """Our own DB is source of truth for users, entitlements, and the cost ledger —
    so auth/billing providers stay swappable."""
    def save_plan(self, tenant_id: str, user_id: str, plan: Dict[str, Any]) -> str: ...
    def list_plans(self, tenant_id: str, user_id: str) -> List[Dict[str, Any]]: ...
    def record_cost(self, tenant_id: str, entry: Dict[str, Any]) -> None: ...


# ── Async job queue (long-running generation) ──────────────────────────────────
@runtime_checkable
class JobQueue(Protocol):
    def enqueue(self, job_type: str, payload: Dict[str, Any]) -> str: ...


# ── Auth (managed identity provider behind an adapter) ─────────────────────────
@runtime_checkable
class AuthProvider(Protocol):
    def verify_token(self, token: str) -> Dict[str, Any]: ...  # -> {user_id, tenant_id, role}


# ── Billing (Razorpay etc.; provider is just the charging mechanism) ───────────
@runtime_checkable
class BillingProvider(Protocol):
    def create_subscription(self, tenant_id: str, plan_id: str) -> Dict[str, Any]: ...
    def verify_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]: ...


# ── Allocation persistence (Persistent Annual Allocation Register) ──────────────
@dataclass
class AllocationSummary:
    """Summary of the current state of a subject/grade allocation register."""
    chapters_allocated: int
    chapters_remaining: int
    total_planned_periods: int
    total_planned_time_minutes: int


# A single chapter's saved allocation record. `periods_by_duration` is keyed by the
# period-type minutes (as a string, e.g. "45"), matching the shape the LRM/allocate
# engine and the frontend both already use — so the register is "redraw-ready" with no
# re-derivation needed (chapter_title/weight/totals travel with it, not just an int).
AllocationRecord = Dict[str, Any]  # {chapter_title, weight, periods_by_duration, total_periods, total_minutes}


@runtime_checkable
class AllocationRepository(Protocol):
    """Persists the Persistent Annual Allocation Register, per tenant + user.

    The register is per-user/tenant STATE (Bucket B, CLOUD_DATA_MODEL.md §2.2), so every
    method is keyed by tenant_id + user_id — the same identity readiness uses — in addition
    to subject·grade. Today auth is stubbed so tenant_id == user_id (the X-Aruvi-User
    header); Phase 4 derives both from the Supabase auth token with no signature change.

    Merge semantics: save_allocation() merges new/overwritten chapters into the existing
    register, preserving chapters not included in the current save.

    File-based (JSON) implementation for now; Supabase adapter swaps in later without
    touching business logic.
    """
    def load_register(self, tenant_id: str, user_id: str,
                      subject: str, grade: Union[str, int]) -> Dict[str, "AllocationRecord"]:
        """Load this teacher's Annual Allocation Register for a subject·grade as
        {chapter_num: AllocationRecord}. Returns empty dict if none exists yet."""
        ...

    def save_allocation(self, tenant_id: str, user_id: str,
                        subject: str, grade: Union[str, int],
                        chapters_allocation: Dict[str, "AllocationRecord"]) -> None:
        """Save allocation data for this teacher, merging into the existing register.

        Chapters in chapters_allocation overwrite existing allocations for those chapters.
        Chapters not in chapters_allocation retain their previous allocations.
        """
        ...

    def get_summary(self, tenant_id: str, user_id: str,
                    subject: str, grade: Union[str, int]) -> AllocationSummary:
        """Return a summary of this teacher's current register state."""
        ...

    def clear_register(self, tenant_id: str, user_id: str,
                       subject: str, grade: Union[str, int]) -> None:
        """Erase this teacher's register for a subject·grade (the "Reset allocations"
        action). No-op if no register exists yet."""
        ...


# ── Readiness teaching-profile persistence (the setup payload) ──────────────────
# The per-teacher "teaching profile" emitted by web/app/components/Readiness.jsx —
# which subjects/grades/sections/durations a teacher takes, plus the weekly grid and
# annual budget. This is the single most important Bucket-B item to persist (see
# CLOUD_DATA_MODEL.md §2.1): without it the readiness flow is lost on every refresh.
#
# The CANONICAL shape is the self-contained `subjects[]` array. Each element:
#   {name, durations[], grades[{grade, sections[{tag,sec}], durations[]}],
#    grids[grade][section][day]=durationIdx|-1, budget{gradeIdx:{method,value}}}
# The denormalized "active subject" projection the component also emits
# (subject/grades/grids/durations/budget at top level) is derived sugar for current
# consumers — it is NEVER persisted (CLOUD_DATA_MODEL.md §5 invariant). The adapter
# stores subjects[] only; the projection is regenerated on read by the frontend.
#
# Every record is keyed by tenant_id + user_id. With no auth yet both stub to "local";
# Phase 4 swaps the values straight from the Supabase auth token — no schema change.
ReadinessProfile = Dict[str, Any]  # {subjects: [...], updated_at: str}


@runtime_checkable
class ReadinessRepository(Protocol):
    """Persists a teacher's readiness teaching profile, keyed by tenant_id + user_id.

    File-based (JSON) implementation for now; a Supabase adapter swaps in later behind
    this same port without touching the engine, API routes, or the React component.
    """
    def load_profile(self, tenant_id: str, user_id: str) -> Optional["ReadinessProfile"]:
        """Load the saved readiness profile, or None if the teacher has none yet.
        A None result is what the frontend reads as "not ready" (setup incomplete)."""
        ...

    def save_profile(self, tenant_id: str, user_id: str,
                     profile: "ReadinessProfile") -> None:
        """Persist the readiness profile (full replace — readiness setup is re-run whole,
        not merged chapter-by-chapter the way allocations are)."""
        ...

    def clear_profile(self, tenant_id: str, user_id: str) -> None:
        """Erase the teacher's readiness profile (the "start setup over" action).
        No-op if none exists yet."""
        ...


# ── Section teaching-state persistence (the lesson execution pointer) ───────────
# Per-section execution state: which chapter a section is tracking (`chapter`), how far
# along it is (`unit_index`, the current Learning Unit, 0-based), and whether the chapter
# is fully taught (`done`). This is the ONLY true execution state (CLAUDE.md §11: "status
# is execution, and lives in My Plans") and today lives ONLY in browser localStorage
# (current_chapter_* / lu_pointer_* / lu_done_*), so it does NOT follow a teacher across
# devices — the bug this store fixes. It is the Bucket-B "teaching pointer" of
# CLOUD_DATA_MODEL.md §2.4, whose target table `lesson_pointer(tenant_id, user_id,
# section_key, unit_index, updated_at)` is extended here with `chapter` + `done` (the same
# per-section execution state). localStorage stays as an optimistic cache; the stored row
# is authoritative for cross-device (exactly §2.4's prescription).
#
# Keyed by tenant_id + user_id (auth stubbed → tenant_id == user_id today). `section_key`
# is the frontend's `${subjectSlug}_${gradeSlug}_${sectionTag}`.
SectionState = Dict[str, Any]  # {chapter: str, unit_index: Optional[int], done: bool, updated_at: str}


@runtime_checkable
class SectionStateRepository(Protocol):
    """Persists per-section teaching execution state, keyed by tenant_id + user_id.

    File-based (JSON) implementation for now; a Supabase adapter (the `lesson_pointer`
    table, extended with `chapter` + `done`) swaps in behind this same port at Phase 4
    without touching the API routes, engine, or the React components.
    """
    def load_all(self, tenant_id: str, user_id: str) -> Dict[str, "SectionState"]:
        """All tracked sections for this teacher: {section_key: SectionState}.
        Returns an empty dict if the teacher has tracked nothing yet."""
        ...

    def save_one(self, tenant_id: str, user_id: str, section_key: str,
                 chapter: str, unit_index: Optional[int], done: bool) -> None:
        """Upsert one section's execution state as a full snapshot for that section
        (the client always sends the complete current state, so no field-merge needed)."""
        ...

    def delete_one(self, tenant_id: str, user_id: str, section_key: str) -> None:
        """Remove one section's state — the "untrack" reversal. No-op if absent."""
        ...


# ── Plan archive ───────────────────────────────────────────────────────────────────
# A teacher can ARCHIVE a lesson plan from My Lessons to declutter without ever losing it
# (there is deliberately NO hard delete — plans carry real generation cost, and the teacher-
# specific state around them — the LU pointer, notes, section attachments — is irreplaceable;
# the design decision, 2026-07-04). Archive is a per-tenant FLAG, not a physical move: the
# plan asset itself is shared read-only CONTENT under DATA_DIR (Bucket A), so archiving cannot
# relocate it. Instead we record the plan's key `{subject}/{grade}/{filename}` in this Bucket-B
# store; My Lessons lists un-archived plans, an Archived view lists the rest, and Restore just
# drops the key. Frozen identity + all back-references = restore is lossless. A plan being
# actively taught (any section attached) is blocked from archiving in the UI, so archived plans
# are only ever detached ones.
#
# Keyed by tenant_id + user_id (auth stubbed → tenant_id == user_id today). A Supabase adapter
# (an `archived_at` column on the plan row, or a small `plan_archive` table) swaps in behind
# this same port at Phase 4 with no change to the API routes or the React components.
@runtime_checkable
class PlanArchiveRepository(Protocol):
    """Persists which saved plans a teacher has archived, keyed by tenant_id + user_id.

    The plan key is the frontend's `${subjectSlug}/${gradeSlug}/${filename}` — the same
    identity used to load the plan — so archive state binds to the plan without duplicating
    any of its content.
    """
    def load_all(self, tenant_id: str, user_id: str) -> Dict[str, str]:
        """All archived plan keys for this teacher: {plan_key: archived_at_iso}.
        Returns an empty dict if nothing is archived."""
        ...

    def archive(self, tenant_id: str, user_id: str, plan_key: str) -> None:
        """Mark one plan archived (records archived_at). Idempotent — re-archiving a plan
        that is already archived leaves the original timestamp untouched."""
        ...

    def restore(self, tenant_id: str, user_id: str, plan_key: str) -> None:
        """Un-archive one plan — the reversal. No-op if the plan was not archived."""
        ...
