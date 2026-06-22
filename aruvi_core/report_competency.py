"""
Period Allocation Report — full per-chapter competency report.

Ports the prototype's report (knowledge_commons/pdf_generator.py) into aruvi_core:
a branded header, an executive summary, a stat strip, per-chapter blocks each
with a competency table (Code / Competency / Justification) and an effort-index
breakdown line, and an "About the Effort Index" methodology section.

The HTML/CSS here is the single source of truth for BOTH the PDF (rendered with
WeasyPrint — pure-Python, no headless browser, cloud-safe) and the on-screen /
mobile preview, so a teacher gets the same layout whether she views or downloads.

Subject groups
--------------
- Effort-index subjects (science, mathematics, the_world_around_us): allocation
  is driven by `effort_index`; each chapter shows its effort-index breakdown.
- Competency-weight subjects (social_sciences, english): allocation is driven by
  competency weight; each chapter shows a weight indicator.

Effort-index schema varies by stage; `effort_breakdown()` and the methodology box
adapt accordingly.
"""

from __future__ import annotations

import html
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


EFFORT_SUBJECTS = {"science", "mathematics", "the_world_around_us"}


# ── helpers shared with the rest of the report layer ───────────────────────

_ROMAN = {3: "III", 4: "IV", 5: "V", 6: "VI", 7: "VII", 8: "VIII", 9: "IX", 10: "X"}
_ROMAN_STR = {"iii": "III", "iv": "IV", "v": "V", "vi": "VI", "vii": "VII",
              "viii": "VIII", "ix": "IX", "x": "X"}


def grade_roman(grade) -> str:
    s = str(grade).strip().lower().replace("grade", "").strip()
    if s in _ROMAN_STR:
        return _ROMAN_STR[s]
    try:
        return _ROMAN.get(int(s), s.upper())
    except (TypeError, ValueError):
        return s.upper()


def subject_display(subject: str) -> str:
    return subject.replace("_", " ").title()


def date_long(dt: datetime) -> str:
    """Top-left date format requested: 22-June-2026."""
    return f"{dt.day:02d}-{dt.strftime('%B')}-{dt.year}"


@dataclass
class Competency:
    c_code: str
    description: str
    justification: str
    weight: Optional[int] = None  # 1..3 for competency-weight subjects


@dataclass
class ChapterReport:
    chapter_number: int
    chapter_title: str
    periods_by_duration: Dict[int, int] = field(default_factory=dict)
    total_periods: int = 0
    total_minutes: int = 0
    competencies: List[Competency] = field(default_factory=list)
    effort_index: Optional[float] = None
    chapter_weight: Optional[float] = None
    signals: Dict[str, Any] = field(default_factory=dict)  # raw effort signals


@dataclass
class PeriodType:
    minutes: int
    count: int


@dataclass
class CompetencyAllocationReport:
    subject: str
    grade: str
    stage: str
    period_types: List[PeriodType]
    chapters: List[ChapterReport]
    generated_at: datetime = field(default_factory=datetime.now)
    notes: Optional[str] = None

    @property
    def is_effort(self) -> bool:
        return self.subject in EFFORT_SUBJECTS

    @property
    def sorted_types(self) -> List[PeriodType]:
        return sorted(self.period_types, key=lambda p: -p.minutes)

    @property
    def total_periods(self) -> int:
        return sum(p.count for p in self.period_types)

    @property
    def total_minutes(self) -> int:
        return sum(p.minutes * p.count for p in self.period_types)


def _coerce_pbd(raw, period_types) -> Dict[int, int]:
    """Normalize periods_by_duration to {minutes: count}, tolerating shape drift.

    Accepts: a dict {min: count} (keys str or int), a list aligned to the sorted
    period-type minutes (e.g. [2, 1] → {longest: 2, next: 1}), or None/empty.
    Never raises — a malformed value yields an empty/zero allocation rather than a 500.
    """
    if isinstance(raw, dict):
        out = {}
        for k, v in raw.items():
            try:
                out[int(k)] = int(v or 0)
            except (TypeError, ValueError):
                continue
        return out
    if isinstance(raw, (list, tuple)):
        mins = [pt.minutes for pt in sorted(period_types, key=lambda p: -p.minutes)]
        out = {}
        for i, v in enumerate(raw):
            if i < len(mins):
                try:
                    out[int(mins[i])] = int(v or 0)
                except (TypeError, ValueError):
                    continue
        return out
    return {}


def _num(v) -> str:
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else str(f)
    except (TypeError, ValueError):
        return str(v)


# ── assembler: build the report from mapping data + descriptions ───────────

def build_report(
    subject: str,
    grade: str,
    stage: str,
    period_types: List[Dict[str, int]],
    chapters_alloc: List[Dict[str, Any]],
    mappings_by_chapter: Dict[int, Dict[str, Any]],
    descriptions: Dict[str, str],
    generated_at: Optional[datetime] = None,
    notes: Optional[str] = None,
) -> CompetencyAllocationReport:
    """Assemble the full report.

    chapters_alloc: [{chapter_number, chapter_title, periods_by_duration {min:count},
                      total_periods, total_minutes, weight}], i.e. the allocate output.
    mappings_by_chapter: {chapter_number: mapping_json} for competencies + effort signals.
    descriptions: {c_code: description}.
    """
    pts = [PeriodType(minutes=int(p["minutes"]), count=int(p["count"]))
           for p in period_types if int(p.get("count", 0)) > 0]

    chapters: List[ChapterReport] = []
    for a in chapters_alloc:
        cn = int(a["chapter_number"])
        m = mappings_by_chapter.get(cn, {})
        comps: List[Competency] = []
        # core first, then adjunct (matches prototype ordering)
        for src in (m.get("core_competencies"), m.get("adjunct_competencies"),
                    m.get("primary"), m.get("competencies")):
            for c in (src or []):
                code = c.get("c_code", "") or c.get("code", "")
                comps.append(Competency(
                    c_code=code,
                    description=c.get("description") or descriptions.get(code, ""),
                    justification=c.get("justification", ""),
                    weight=c.get("weight"),
                ))
        pbd = _coerce_pbd(a.get("periods_by_duration"), pts)
        total_periods = a.get("total_periods")
        total_periods = int(total_periods) if total_periods is not None else sum(pbd.values())
        total_minutes = a.get("total_minutes")
        total_minutes = int(total_minutes) if total_minutes is not None else sum(k * v for k, v in pbd.items())
        chapters.append(ChapterReport(
            chapter_number=cn,
            chapter_title=a.get("chapter_title") or m.get("chapter_title", ""),
            periods_by_duration=pbd,
            total_periods=total_periods,
            total_minutes=total_minutes,
            competencies=comps,
            effort_index=m.get("effort_index"),
            chapter_weight=a.get("weight"),
            signals={k: m.get(k) for k in (
                "conceptual_demand", "task_load", "exploration_load", "procedural_load",
                "activity_count", "activity_load", "demo_count", "reasoning_load", "exec_load",
            ) if k in m},
        ))

    return CompetencyAllocationReport(
        subject=subject, grade=grade, stage=stage, period_types=pts,
        chapters=chapters, generated_at=generated_at or datetime.now(), notes=notes,
    )


# ── executive summary copy (per the spec) ──────────────────────────────────

def _allocation_factors(report: "CompetencyAllocationReport") -> str:
    if report.is_effort:
        if report.stage == "preparatory":
            factors = ("how abstract each chapter's ideas are, how many tasks it sets, "
                       "how much hands-on exploration it involves, and how much routine "
                       "practice it requires")
        elif report.stage == "secondary":
            factors = ("how abstract each chapter's ideas are, how much sustained reasoning "
                       "it demands, and the in-class workload of its exercises")
        else:
            factors = ("how abstract each chapter's ideas are, how many student activities "
                       "and teacher demonstrations it involves, and the in-class workload of "
                       "its exercises")
        return (
            f"Aruvi looks at the teaching effort each chapter is likely to need — {factors} — "
            f"and turns that into a single effort index for the chapter. Chapters with a higher "
            f"effort index are given a larger share of the available periods, so that harder "
            f"chapters get more classroom time, and periods are then distributed across all the "
            f"selected chapters in proportion to their effort index."
        )
    return (
        "Aruvi looks at the competencies each chapter develops and how strongly the chapter "
        "addresses each one. Chapters that carry heavier or more central competencies are given "
        "a larger share of the available periods, so that the most important learning gets more "
        "classroom time, and periods are then distributed across all the selected chapters in "
        "proportion to this competency load."
    )


def executive_summary_intro(report: "CompetencyAllocationReport") -> str:
    """Back-compat single-paragraph accessor (first paragraph of the summary)."""
    return executive_summary_paragraphs(report)[0]


def executive_summary_paragraphs(report: "CompetencyAllocationReport") -> List[str]:
    """The executive-summary body as ordered paragraphs (per the spec, point 7):

    1. report intro + the allocation-factors explanation + the "allocation report below…" line
       (the old paragraphs 1 and 2 merged).
    2. the competency-section description.
    3. the intended-use / audit-trail closing line.
    """
    subj = subject_display(report.subject)
    g = grade_roman(report.grade)
    return [
        (f"This report presents the allocation of available instructional periods across the "
         f"selected chapters for {subj}, Grade {g}. {_allocation_factors(report)} "
         f"The allocation report below shows the distribution of the available periods across "
         f"the chapters using the approach described here."),
        ("For each chapter, the competency section lists the competencies the chapter addresses, "
         "together with the rationale for including each one."),
        ("This information is intended to help the teacher in planning the class time, aligning "
         "with curriculum guidelines, and to provide an audit trail for the same."),
    ]
