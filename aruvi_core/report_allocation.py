"""
Allocation report generator for all subjects.
Produces standardized allocation table with subject-agnostic data structure.
"""

from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime


@dataclass
class AllocationRow:
    """A single chapter's allocation row."""
    chapter_number: int
    chapter_name: str
    total_periods: int
    allocated_periods: int
    effort_index: Optional[float] = None
    competency_weight: Optional[float] = None
    notes: str = ""


@dataclass
class AllocationReport:
    """Complete allocation report for a subject/grade combination."""
    subject: str
    grade: int
    stage: str
    period_profile_name: str  # "Core", "Extended", etc.
    period_duration_minutes: int
    total_periods: int  # sum of all allocated periods
    generated_at: datetime
    rows: List[AllocationRow]
    allocation_basis: str  # "Effort Index" | "Competency Weights" | "Custom"
    notes: Optional[str] = None

    def to_dict(self) -> Dict:
        """Serialize to dict for JSON/template rendering."""
        return {
            "subject": self.subject,
            "grade": self.grade,
            "stage": self.stage,
            "period_profile_name": self.period_profile_name,
            "period_duration_minutes": self.period_duration_minutes,
            "total_periods": self.total_periods,
            "generated_at": self.generated_at.isoformat(),
            "allocation_basis": self.allocation_basis,
            "notes": self.notes,
            "rows": [
                {
                    "chapter_number": row.chapter_number,
                    "chapter_name": row.chapter_name,
                    "total_periods": row.total_periods,
                    "allocated_periods": row.allocated_periods,
                    "effort_index": row.effort_index,
                    "competency_weight": row.competency_weight,
                    "notes": row.notes,
                }
                for row in self.rows
            ],
        }


def create_report(
    subject: str,
    grade: int,
    stage: str,
    period_profile_name: str,
    period_duration_minutes: int,
    allocation_rows: List[Dict],
    allocation_basis: str,
    notes: Optional[str] = None,
) -> AllocationReport:
    """
    Factory to create an AllocationReport.

    Args:
        subject: "science", "social_sciences", "mathematics", "english", "the_world_around_us"
        grade: 3-10
        stage: "preparatory", "middle", "secondary"
        period_profile_name: User-defined (e.g., "Core", "Extended")
        period_duration_minutes: e.g., 40, 45, 60
        allocation_rows: List of dicts with keys:
            - chapter_number (int)
            - chapter_name (str)
            - total_periods (int) — chapters in original curriculum
            - allocated_periods (int) — periods assigned for this year
            - effort_index (float, optional)
            - competency_weight (float, optional)
            - notes (str, optional)
        allocation_basis: How allocation was calculated
        notes: Optional report-level note

    Returns:
        AllocationReport ready for rendering/export
    """
    rows = [
        AllocationRow(
            chapter_number=r["chapter_number"],
            chapter_name=r["chapter_name"],
            total_periods=r["total_periods"],
            allocated_periods=r["allocated_periods"],
            effort_index=r.get("effort_index"),
            competency_weight=r.get("competency_weight"),
            notes=r.get("notes", ""),
        )
        for r in allocation_rows
    ]

    total_allocated = sum(r.allocated_periods for r in rows)

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
        notes=notes,
    )


def format_report_title(report: AllocationReport) -> str:
    """Format a human-readable title for the report."""
    subject_display = report.subject.replace("_", " ").title()
    stage_abbr = "".join(w[0].upper() for w in report.stage.split("_"))
    return f"Period Allocation Report · Grade {report.grade} · {subject_display}"


def format_report_subtitle(report: AllocationReport) -> str:
    """Format subtitle with NCF and date."""
    return f"NCF 2023 · Pedagogical Platform · Grade {report.grade} · {report.subject.title()} · {report.generated_at.strftime('%Y-%m-%d')}"
