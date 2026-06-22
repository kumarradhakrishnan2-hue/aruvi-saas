"""
DEPRECATED — superseded by report_competency.py.

This was the first, simpler summary-table report model (per-duration columns,
single total). The live Period Allocation Report now matches the prototype's
richer per-chapter competency format and is built by `report_competency.py` +
`export_allocation_pdf.py` (WeasyPrint) / `export_allocation_docx.py`. Nothing
imports this module anymore; kept only to avoid breaking any external reference.
Safe to delete.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class PeriodType:
    """One period type the teacher defined (a duration + how many of them)."""
    name: str                 # teacher-given label, e.g. "Core"
    minutes: int              # duration in minutes, e.g. 45
    count: int = 0            # how many periods of this type are available


@dataclass
class AllocationRow:
    """A single chapter's allocation row.

    `periods_by_duration` maps a duration (in minutes, as int) to the number of
    periods of that duration allocated to this chapter — this is what powers the
    per-duration columns. `allocated_periods` is the row total (sum across
    durations), kept for backward compatibility and the summary column.
    """
    chapter_number: int
    chapter_name: str
    total_periods: int                              # periods allocated for this chapter
    allocated_periods: int                          # same as total_periods (back-compat)
    periods_by_duration: Dict[int, int] = field(default_factory=dict)
    total_minutes: int = 0                          # instructional minutes for this chapter
    effort_index: Optional[float] = None
    competency_weight: Optional[float] = None
    notes: str = ""


@dataclass
class AllocationReport:
    """Complete allocation report for a subject/grade combination."""
    subject: str
    grade: int
    stage: str
    period_profile_name: str           # legacy label (e.g. "Mixed"); kept for back-compat
    period_duration_minutes: int       # representative duration (largest), kept for back-compat
    total_periods: int                 # sum of all allocated periods
    generated_at: datetime
    rows: List[AllocationRow]
    allocation_basis: str              # "Effort Index" | "Competency Weights" | "Custom"
    period_types: List[PeriodType] = field(default_factory=list)
    total_minutes: int = 0             # total instructional minutes across all chapters
    notes: Optional[str] = None

    # ----- derived helpers -----------------------------------------------
    @property
    def durations(self) -> List[int]:
        """Distinct durations present, longest first (column order)."""
        ds = {pt.minutes for pt in self.period_types}
        for r in self.rows:
            ds.update(int(d) for d in r.periods_by_duration.keys())
        return sorted(ds, reverse=True)

    @property
    def total_hours(self) -> float:
        return round(self.total_minutes / 60, 1) if self.total_minutes else 0.0

    def name_for_duration(self, minutes: int) -> str:
        for pt in self.period_types:
            if int(pt.minutes) == int(minutes):
                return pt.name or f"{minutes} min"
        return f"{minutes} min"

    def to_dict(self) -> Dict:
        """Serialize to dict for JSON/template rendering."""
        return {
            "subject": self.subject,
            "grade": self.grade,
            "stage": self.stage,
            "period_profile_name": self.period_profile_name,
            "period_duration_minutes": self.period_duration_minutes,
            "total_periods": self.total_periods,
            "total_minutes": self.total_minutes,
            "generated_at": self.generated_at.isoformat(),
            "allocation_basis": self.allocation_basis,
            "notes": self.notes,
            "period_types": [
                {"name": pt.name, "minutes": pt.minutes, "count": pt.count}
                for pt in self.period_types
            ],
            "rows": [
                {
                    "chapter_number": row.chapter_number,
                    "chapter_name": row.chapter_name,
                    "total_periods": row.total_periods,
                    "allocated_periods": row.allocated_periods,
                    "periods_by_duration": {str(k): v for k, v in row.periods_by_duration.items()},
                    "total_minutes": row.total_minutes,
                    "effort_index": row.effort_index,
                    "competency_weight": row.competency_weight,
                    "notes": row.notes,
                }
                for row in self.rows
            ],
        }


def _coerce_period_types(raw: Optional[List[Dict]]) -> List[PeriodType]:
    out: List[PeriodType] = []
    for pt in raw or []:
        out.append(PeriodType(
            name=pt.get("name") or f"{pt.get('minutes', '')} min",
            minutes=int(pt.get("minutes", 0)),
            count=int(pt.get("count", 0)),
        ))
    return out


def create_report(
    subject: str,
    grade: int,
    stage: str,
    period_profile_name: str,
    period_duration_minutes: int,
    allocation_rows: List[Dict],
    allocation_basis: str,
    period_types: Optional[List[Dict]] = None,
    notes: Optional[str] = None,
) -> AllocationReport:
    """Factory to create an AllocationReport from raw allocation data.

    Each item in `allocation_rows` is a dict with keys:
        chapter_number (int), chapter_name (str), total_periods (int),
        allocated_periods (int), periods_by_duration (dict[int|str, int], optional),
        total_minutes (int, optional), effort_index (float, optional),
        competency_weight (float, optional), notes (str, optional).
    """
    rows: List[AllocationRow] = []
    for r in allocation_rows:
        pbd = {int(k): int(v) for k, v in (r.get("periods_by_duration") or {}).items()}
        total_minutes = r.get("total_minutes")
        if total_minutes is None:
            total_minutes = sum(int(m) * int(c) for m, c in pbd.items())
        rows.append(AllocationRow(
            chapter_number=r["chapter_number"],
            chapter_name=r["chapter_name"],
            total_periods=r["total_periods"],
            allocated_periods=r["allocated_periods"],
            periods_by_duration=pbd,
            total_minutes=int(total_minutes),
            effort_index=r.get("effort_index"),
            competency_weight=r.get("competency_weight"),
            notes=r.get("notes", ""),
        ))

    total_allocated = sum(r.allocated_periods for r in rows)
    total_minutes = sum(r.total_minutes for r in rows)

    return AllocationReport(
        subject=subject,
        grade=grade,
        stage=stage,
        period_profile_name=period_profile_name,
        period_duration_minutes=period_duration_minutes,
        total_periods=total_allocated,
        generated_at=datetime.now(),
        rows=rows,
        allocation_basis=allocation_basis,
        period_types=_coerce_period_types(period_types),
        total_minutes=total_minutes,
        notes=notes,
    )


# ── shared copy used by every renderer (web, PDF, DOCX) ────────────────────

def grade_roman(grade: int) -> str:
    romans = {3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}
    return romans.get(int(grade), str(grade))


def subject_display(subject: str) -> str:
    return subject.replace("_", " ").title()


def allocation_note(basis: str) -> str:
    if basis == "Effort Index":
        return ("Aruvi estimates the teaching effort required for each chapter and allocates "
                "periods proportionally to its effort index — chapters with a higher effort "
                "index receive more time to ensure mastery.")
    if basis == "Competency Weights":
        return ("Periods are allocated according to the relative weight of the competencies "
                "covered in each chapter — chapters carrying heavier competencies receive "
                "more time.")
    return ("Periods are allocated using the allocation strategy defined for this curriculum.")


EXEC_SUMMARY_WHY = (
    "This report explains how the available instructional time has been distributed across "
    "the selected chapters for the chosen time period. Aruvi estimates the teaching effort "
    "required for each chapter and allocates periods proportionally. The factors considered "
    "vary by subject and may include task complexity, practice requirements, projects, "
    "assessments and activity load."
)

EXEC_SUMMARY_CONTENTS = [
    "Period allocation across the selected chapters",
    "The basis on which allocation was made for each chapter (competency weightage / effort index)",
    "Total instructional time across the chosen period types",
]

EXEC_SUMMARY_POINTER = (
    'For a detailed explanation of how time has been distributed across specific chapters, '
    'open Ask Aruvi and select: "How time is allocated across chapters".'
)
