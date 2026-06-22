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


@runtime_checkable
class AllocationRepository(Protocol):
    """Persists the Persistent Annual Allocation Register.

    Merge semantics: save_allocation() merges new/overwritten chapters into the existing
    register, preserving chapters not included in the current save.

    File-based (JSON) implementation for now; Supabase adapter swaps in later without
    touching business logic.
    """
    def load_register(self, subject: str, grade: Union[str, int]) -> Dict[str, int]:
        """Load the Annual Allocation Register as {chapter_num: periods_allocated}.
        Returns empty dict if no register exists yet."""
        ...

    def save_allocation(self, subject: str, grade: Union[str, int], chapters_allocation: Dict[str, int]) -> None:
        """Save allocation data, merging into the existing register.

        Chapters in chapters_allocation overwrite existing allocations for those chapters.
        Chapters not in chapters_allocation retain their previous allocations.
        """
        ...

    def get_summary(self, subject: str, grade: Union[str, int]) -> AllocationSummary:
        """Return a summary of the current register state."""
        ...
