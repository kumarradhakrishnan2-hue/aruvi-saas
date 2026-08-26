"""File-based implementation of AcademicYearRepository.

Persists a teacher's academic years as JSON at
ARUVI_STATE_DIR/academic_years/{tenant_id}/{user_id}/years.json, shaped as

    {"years": [{year_id, starts_on, ends_on, is_current}, ...], "updated_at": iso}

This is administrative_architecture.md Step 1's reference adapter. The year list is
per-teacher because schools start at different times (CBSE Apr–Mar, several state
boards Jun–May) — Aruvi's d-date and the teacher's own cutover are different events
(§2.1). Exactly one year is current at a time; open_year/set_current maintain that
invariant. The API layer bootstraps a default year on first touch — this adapter never
invents one.

Step 2 (cutover) extends the port with close_year() against this same file; nothing
here anticipates it.
"""
import json
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import List, Optional

from aruvi_core.ports import AcademicYear, AcademicYearRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class AcademicYearRepositoryFileImpl(AcademicYearRepository):
    """File-based academic-year store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the academic_years/ folder lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.base_dir = self.data_dir / "academic_years"

    def _path(self, tenant_id: str, user_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / _slug(user_id) / "years.json"

    def _read(self, tenant_id: str, user_id: str) -> List[AcademicYear]:
        path = self._path(tenant_id, user_id)
        if not path.exists():
            return []
        try:
            with open(path, "r") as f:
                raw = json.load(f) or {}
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to load academic years from {path}: {e}")
        out: List[AcademicYear] = []
        for y in raw.get("years", []):
            out.append(AcademicYear(
                year_id=str(y.get("year_id", "")),
                starts_on=str(y.get("starts_on", "")),
                ends_on=str(y.get("ends_on", "")),
                is_current=bool(y.get("is_current", False)),
                cleanup_pending=bool(y.get("cleanup_pending", False)),
            ))
        return out

    def _write(self, tenant_id: str, user_id: str, years: List[AcademicYear]) -> None:
        path = self._path(tenant_id, user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        record = {
            "years": [asdict(y) for y in years],
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        try:
            with open(path, "w") as f:
                json.dump(record, f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save academic years to {path}: {e}")

    def current(self, tenant_id: str, user_id: str) -> Optional[AcademicYear]:
        """The teacher's current academic year, or None if none has been opened yet."""
        for y in self._read(tenant_id, user_id):
            if y.is_current:
                return y
        return None

    def list_years(self, tenant_id: str, user_id: str) -> List[AcademicYear]:
        """All years ever opened for this teacher, oldest first (by starts_on, then
        year_id, so a missing date cannot scramble the order). Empty list if none."""
        return sorted(self._read(tenant_id, user_id),
                      key=lambda y: (y.starts_on, y.year_id))

    def open_year(self, tenant_id: str, user_id: str, year: AcademicYear) -> None:
        """Add a year (idempotent on year_id — re-opening updates in place). If the year
        is marked current, every other year's is_current is cleared."""
        years = self._read(tenant_id, user_id)
        replaced = False
        for i, y in enumerate(years):
            if y.year_id == year.year_id:
                years[i] = year
                replaced = True
                break
        if not replaced:
            years.append(year)
        if year.is_current:
            for y in years:
                if y.year_id != year.year_id:
                    y.is_current = False
        self._write(tenant_id, user_id, years)

    def set_current(self, tenant_id: str, user_id: str, year_id: str) -> None:
        """Mark one existing year current (clearing the others). Raises ValueError if
        the year_id has never been opened — callers open before they point."""
        years = self._read(tenant_id, user_id)
        if not any(y.year_id == year_id for y in years):
            raise ValueError(f"Academic year {year_id!r} has never been opened for "
                             f"{_slug(tenant_id)}/{_slug(user_id)}")
        for y in years:
            y.is_current = (y.year_id == year_id)
        self._write(tenant_id, user_id, years)
