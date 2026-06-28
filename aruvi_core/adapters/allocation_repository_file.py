"""File-based implementation of AllocationRepository.

Persists the Persistent Annual Allocation Register as JSON at
STATE_DIR/allocations/{tenant_id}/{user_id}/{subject}/{grade}/allocation.json.

The register is per-user/tenant STATE (Bucket B), so it is keyed by tenant_id + user_id —
the same identity readiness uses — so two teachers never share or overwrite each other's
allocations. Today auth is stubbed so tenant_id == user_id (the X-Aruvi-User header);
Phase 4 swaps the values from the Supabase auth token with no code change here.

Each chapter's value is a full AllocationRecord — {chapter_title, weight,
periods_by_duration, total_periods, total_minutes} — not just an int. This keeps the
register "redraw-ready": the frontend's final-allocation table can be rebuilt straight
from what's on disk, with no re-derivation against the LRM/mappings needed.

Merge semantics: chapters in the new allocation overwrite existing allocations
for those chapters; chapters not in the new allocation retain their previous
allocations.
"""
import json
from pathlib import Path
from typing import Dict, Union

from aruvi_core.ports import AllocationRecord, AllocationRepository, AllocationSummary
from aruvi_core.grades import stage_for


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class AllocationRepositoryFileImpl(AllocationRepository):
    """File-based Persistent Annual Allocation Register, keyed per tenant + user."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where allocations/ folder lives (e.g., STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.allocations_dir = self.data_dir / "allocations"

    def _register_path(self, tenant_id: str, user_id: str,
                       subject: str, grade: Union[str, int]) -> Path:
        """Return the path to this teacher's allocation register file."""
        return (self.allocations_dir / _slug(tenant_id) / _slug(user_id)
                / subject / str(grade) / "allocation.json")

    def load_register(self, tenant_id: str, user_id: str,
                      subject: str, grade: Union[str, int]) -> Dict[str, AllocationRecord]:
        """Load this teacher's Annual Allocation Register.

        Returns empty dict if no register exists yet.
        """
        path = self._register_path(tenant_id, user_id, subject, grade)
        if not path.exists():
            return {}

        try:
            with open(path, "r") as f:
                data = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to load allocation register from {path}: {e}")

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

    def save_allocation(self, tenant_id: str, user_id: str,
                        subject: str, grade: Union[str, int],
                        chapters_allocation: Dict[str, AllocationRecord]) -> None:
        """Save allocation data for this teacher, merging into the existing register.

        Chapters in chapters_allocation overwrite existing allocations for those chapters.
        Chapters not in chapters_allocation retain their previous allocations.
        """
        # Load existing register (this teacher's)
        existing = self.load_register(tenant_id, user_id, subject, grade)

        # Merge: update with new allocations, preserve untouched chapters
        merged = {**existing, **chapters_allocation}

        # Ensure path exists
        path = self._register_path(tenant_id, user_id, subject, grade)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write merged register
        try:
            with open(path, "w") as f:
                json.dump(merged, f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save allocation register to {path}: {e}")

    def get_summary(self, tenant_id: str, user_id: str,
                    subject: str, grade: Union[str, int]) -> AllocationSummary:
        """Return a summary of this teacher's current register state."""
        register = self.load_register(tenant_id, user_id, subject, grade)

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

    def clear_register(self, tenant_id: str, user_id: str,
                       subject: str, grade: Union[str, int]) -> None:
        """Erase this teacher's register for a subject·grade. No-op if it doesn't exist.

        Prefers removing the file; on filesystems where unlink is not permitted (some
        read-restricted mounts allow overwrite but not delete) falls back to writing an
        empty register, so "Reset allocations" never errors.
        """
        path = self._register_path(tenant_id, user_id, subject, grade)
        if not path.exists():
            return
        try:
            path.unlink()
        except OSError:
            with open(path, "w") as f:
                json.dump({}, f)
