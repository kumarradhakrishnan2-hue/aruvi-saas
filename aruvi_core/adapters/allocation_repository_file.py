"""AllocationRepository over the document backend (file or Postgres — Track C, 2026-09-09).

Persists the Persistent Annual Allocation Register as one JSON document per subject·grade
at key allocations/{tenant_id}/{user_id}/{year_id}/{subject}/{grade}/allocation.json.

The register is per-user/tenant STATE (Bucket B), so it is keyed by tenant_id + user_id —
the same identity readiness uses — so two teachers never share or overwrite each other's
allocations. It is also YEAR-SCOPED (administrative_architecture.md Step 1, 2026-08-22):
an allocation belongs to one academic year, so `year_id` (e.g. "2026-27") is a path
segment after user. Cutover starts a fresh year folder; it never rewrites this one.
The API layer resolves which year is current — this adapter just addresses by it.

Each chapter's value is a full AllocationRecord — {chapter_title, weight,
periods_by_duration, total_periods, total_minutes} — not just an int. This keeps the
register "redraw-ready": the frontend's final-allocation table can be rebuilt straight
from what's on disk, with no re-derivation against the LRM/mappings needed.

Merge semantics: chapters in the new allocation overwrite existing allocations
for those chapters; chapters not in the new allocation retain their previous
allocations.
"""
from typing import Dict, Union

from aruvi_core.ports import AllocationRecord, AllocationRepository, AllocationSummary
from aruvi_core.grades import stage_for
from aruvi_core.adapters.document_backend import as_backend, slug as _slug


class AllocationRepositoryFileImpl(AllocationRepository):
    """Persistent Annual Allocation Register over a document backend, keyed per tenant + user."""

    def __init__(self, data_dir):
        """
        Args:
            data_dir: a DocumentBackend, or a directory (→ FileBackend, e.g. STATE_DIR).
        """
        self.backend = as_backend(data_dir)

    def _key(self, tenant_id: str, user_id: str, year_id: str,
             subject: str, grade: Union[str, int]) -> str:
        """The register document's key for one teacher-year-subject-grade."""
        return (f"allocations/{_slug(tenant_id)}/{_slug(user_id)}/{_slug(year_id)}"
                f"/{subject}/{grade}/allocation.json")

    def load_register(self, tenant_id: str, user_id: str, year_id: str,
                      subject: str, grade: Union[str, int]) -> Dict[str, AllocationRecord]:
        """Load this teacher's Annual Allocation Register for one academic year.

        Returns empty dict if no register exists yet.
        """
        data = self.backend.get_json(self._key(tenant_id, user_id, year_id, subject, grade))
        if not isinstance(data, dict):
            return {}

        # Normalize each entry to the AllocationRecord shape. Tolerates legacy registers
        # written before this schema (plain int = total periods only) by upgrading them
        # to a minimal record on read, rather than crashing.
        normalized: Dict[str, AllocationRecord] = {}
        for k, v in data.items():
            if isinstance(v, dict):
                normalized[str(k)] = v
            else:
                normalized[str(k)] = {
                    "chapter_title": "",
                    "weight": 0,
                    "periods_by_duration": {},
                    "total_periods": int(v),
                    "total_minutes": 0,
                }
        return normalized

    def save_allocation(self, tenant_id: str, user_id: str, year_id: str,
                        subject: str, grade: Union[str, int],
                        chapters_allocation: Dict[str, AllocationRecord]) -> None:
        """Save allocation data for this teacher's year, merging into the existing register.

        Chapters in chapters_allocation overwrite existing allocations for those chapters.
        Chapters not in chapters_allocation retain their previous allocations.
        """
        # Load existing register (this teacher's, this year's)
        existing = self.load_register(tenant_id, user_id, year_id, subject, grade)

        # Merge: update with new allocations, preserve untouched chapters
        merged = {**existing, **chapters_allocation}

        self.backend.put_json(self._key(tenant_id, user_id, year_id, subject, grade), merged)

    def get_summary(self, tenant_id: str, user_id: str, year_id: str,
                    subject: str, grade: Union[str, int]) -> AllocationSummary:
        """Return a summary of this teacher's current register state for one year."""
        register = self.load_register(tenant_id, user_id, year_id, subject, grade)

        # Count allocated chapters
        chapters_allocated = len(register)

        # Total periods allocated (now read from each record, not the bare value)
        total_periods = sum(int(rec.get("total_periods", 0)) for rec in register.values())

        # Get stage to determine total chapters for "remaining" count
        # grade can be int or string; convert to string for stage_for()
        stage = stage_for(str(grade))

        # For now, we don't have a centralized "total chapters per subject/stage" mapping.
        # Rough heuristic: assume 12 chapters for middle/secondary, fewer for preparatory.
        # This will be refined once we have the full subject specs.
        if stage == "preparatory":
            total_chapters_estimate = 8  # Typical for preparatory
        elif stage == "middle":
            total_chapters_estimate = 12  # Typical for middle
        else:  # secondary
            total_chapters_estimate = 12  # Typical for secondary

        chapters_remaining = max(0, total_chapters_estimate - chapters_allocated)

        # total_minutes now comes straight from each record (sum of periods_by_duration *
        # duration, computed by the caller when the record was built) instead of being
        # estimated from a flat 45-min assumption.
        total_time_minutes = sum(int(rec.get("total_minutes", 0)) for rec in register.values())

        return AllocationSummary(
            chapters_allocated=chapters_allocated,
            chapters_remaining=chapters_remaining,
            total_planned_periods=total_periods,
            total_planned_time_minutes=total_time_minutes,
        )

    def clear_register(self, tenant_id: str, user_id: str, year_id: str,
                       subject: str, grade: Union[str, int]) -> None:
        """Erase this teacher's register for a subject·grade in one year. No-op if it
        doesn't exist (the file backend leaves an empty document where unlink is
        forbidden, so "Reset allocations" never errors)."""
        self.backend.delete(self._key(tenant_id, user_id, year_id, subject, grade))
