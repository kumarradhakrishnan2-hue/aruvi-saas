"""File-based implementation of the YearCutover port — administrative architecture Step 2.

Read the port's docstring first (ports.py, `YearCutover`): the reason this file is short
is that Step 1 already did the hard part. Every teaching store is year-scoped by PATH and
readiness deliberately is not, so cutover **moves nothing and deletes nothing**. It opens
the next year and points the teacher at it; the old year's folders stay exactly where they
are. That single fact gives, for free, every behaviour the spec asks for:

    last year readable · this year empty · attachments and pointers cleared ·
    class list carried · notes left with the plans they were written against

The counts in the result are gathered BEFORE the switch, purely so the confirmation
screen can state what happened instead of promising it.

Idempotency is the one thing that needs care — "a teacher WILL tap twice"
(administrative_architecture.md §Step 2). A second call finds she is already in the target
year and returns `already_done=True` without opening anything or touching the year she has
just started working in.
"""
from __future__ import annotations

from datetime import date
from typing import Any, Optional

from aruvi_core.ports import AcademicYear, CutoverResult


class YearCutoverFileImpl:
    """Moves one teacher into the next academic year, using the existing repositories."""

    def __init__(self, year_repo: Any, readiness_repo: Any, prepared_repo: Any,
                 section_state_repo: Any):
        """
        Args:
            year_repo: AcademicYearRepository — where the switch actually happens.
            readiness_repo: ReadinessRepository — read only, to count what carries.
            prepared_repo: PreparedPlansRepository — read only, to count what archives.
            section_state_repo: SectionStateRepository — read only; its year-scoped
                folder being empty in the NEW year is what clears her attachments.
        """
        self.years = year_repo
        self.readiness = readiness_repo
        self.prepared = prepared_repo
        self.sections = section_state_repo

    # ── year arithmetic ────────────────────────────────────────────────────────
    @staticmethod
    def next_year_id(year_id: str) -> str:
        """"2026-27" → "2027-28". Falls back to the label itself if it is not in that
        shape, so a hand-edited year can never crash a teacher's session."""
        try:
            start = int(str(year_id).split("-")[0])
        except (ValueError, IndexError):
            return year_id
        return f"{start + 1}-{str(start + 2)[-2:]}"

    @staticmethod
    def year_bounds(year_id: str) -> tuple:
        """(starts_on, ends_on) as ISO strings for an April-anchored Indian year."""
        try:
            start = int(str(year_id).split("-")[0])
        except (ValueError, IndexError):
            today = date.today()
            return today.isoformat(), today.isoformat()
        return date(start, 4, 1).isoformat(), date(start + 1, 3, 31).isoformat()

    @classmethod
    def cutover_date(cls, to_year_id: str, month_day: str = "06-01") -> Optional[date]:
        """The date on which the move INTO `to_year_id` is offered — by default 1 June of
        that year's opening calendar year ("2027-28" → 2027-06-01)."""
        try:
            start = int(str(to_year_id).split("-")[0])
            month, day = [int(x) for x in str(month_day).split("-")]
            return date(start, month, day)
        except (ValueError, IndexError):
            return None

    # ── the action ─────────────────────────────────────────────────────────────
    def cutover(self, tenant_id: str, user_id: str,
                from_year: str, to_year: str) -> CutoverResult:
        """Open `to_year` and make it current. Idempotent."""
        current = self.years.current(tenant_id, user_id)
        if current is not None and current.year_id == to_year:
            # She already cut over — say so and change nothing. Re-running the counts
            # here would report the NEW year's (empty) state as if it were the result.
            return CutoverResult(closed_year=from_year, opened_year=to_year,
                                 sections_carried=0, plans_archived=0, already_done=True)

        # Count what she is carrying and what she is leaving behind — BEFORE the switch,
        # while `from_year` is still the year the repos answer for.
        sections_carried = 0
        try:
            profile = self.readiness.load_profile(tenant_id, user_id) or {}
            for subject in profile.get("subjects", []) or []:
                for grade in subject.get("grades", []) or []:
                    sections_carried += len(grade.get("sections", []) or [])
        except Exception:                       # noqa: BLE001 — a count must never fail a cutover
            sections_carried = 0

        plans_archived = 0
        try:
            plans_archived = len(self.prepared.load_all(tenant_id, user_id, from_year) or {})
        except Exception:                       # noqa: BLE001
            plans_archived = 0

        starts_on, ends_on = self.year_bounds(to_year)
        self.years.open_year(tenant_id, user_id,
                             AcademicYear(year_id=to_year, starts_on=starts_on,
                                          ends_on=ends_on, is_current=True))
        self.years.set_current(tenant_id, user_id, to_year)

        return CutoverResult(closed_year=from_year, opened_year=to_year,
                             sections_carried=sections_carried,
                             plans_archived=plans_archived, already_done=False)
