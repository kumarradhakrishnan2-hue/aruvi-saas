"""
Canonical view model — the single contract between subject plugins and the shared renderer.

Design rule (see architecture plan §"One renderer, many subjects"): this model is
structure-PRESERVING, not flattening. Each subject's organizing axis survives as a typed,
labeled, nestable Group carrying its own `meta`; the renderer is structure-driven and never
branches on subject. Visual style is unified; organizing structure is preserved.

Expressed here as stdlib dataclasses (zero deps, runs on 3.9+). The API layer may wrap these
in pydantic for request/response validation, but the engine and renderer speak this shape.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from typing import Any, Dict, List


class StimulusType(str, Enum):
    """The renderer keys visual handling off this type — never off subject."""
    NONE = "none"
    SVG = "svg"        # e.g. Mathematics geometry figures
    TABLE = "table"    # pipe-delimited / structured rows (Science, SS)
    PROSE = "prose"    # fallback descriptive text


@dataclass
class VisualStimulus:
    type: StimulusType = StimulusType.NONE
    content: str = ""  # svg markup, table source, or prose — interpreted by `type`


@dataclass
class Phase:
    """One timed step within a period — the SINGLE timed spine (layout decision 2026-07-09).

    Raw saved plans carry per-phase minutes as band strings ("0–5", "10-30"); normalization
    parses them ONCE into integers here (see normalize.parse_minutes_band). `label` keeps the
    raw band string for provenance/fallback. Display shows the DURATION ("5 min") in the
    marginal rail — derived as end_min - start_min, never re-parsed downstream. Phases should
    tile 0 → period duration (validated by normalize.phase_tiling_issues, best-effort carry)."""
    text: str = ""
    start_min: Any = None   # int | None (unparseable band)
    end_min: Any = None     # int | None
    label: str = ""         # the raw minutes string as generated, e.g. "0–5"


@dataclass
class Period:
    number: int
    title: str = ""
    approach: str = ""  # canonical "how do I run this period?" line (2026-07-09): Science
    #                     pedagogical_approach · Maths pedagogical_method · English joined
    #                     pedagogical_methods · TWAU dominant_mode spelled out · SS/Maths-prep
    #                     have no source field (empty). Display: "40 min · {approach}".
    activities: List[str] = field(default_factory=list)
    phases: List[Phase] = field(default_factory=list)   # the timed spine (2026-07-09; activities
    #                                                     keeps legacy flat lines until the new
    #                                                     period layout lands in the renderers)
    materials: List[str] = field(default_factory=list)  # first-class: fixed slot in the anatomy
    teacher_notes: List[str] = field(default_factory=list)
    learning_outcomes: List[str] = field(default_factory=list)
    homework: str = ""
    meta: Dict[str, Any] = field(default_factory=dict)  # subject extras, carried not interpreted


@dataclass
class Group:
    """A labeled, optionally-nested container of periods — the organizing axis.

    `type`  names the subject's organizing concept: "spine" | "competency" |
            "progression_stage" | "section" | ...
    `label` is the display heading ("Reading for Comprehension", "C-2.1 Analyses...").
    `meta`  carries axis-specific data (weight, c_code, implied_lo, stage_index, ...).
    `children` enables multi-axis structures (English: section -> spine).
    """
    type: str
    label: str
    periods: List[Period] = field(default_factory=list)
    children: List["Group"] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AssessmentItem:
    prompt: str
    item_type: str = ""  # MCQ | OPEN_TASK | FILL_IN | EXTRACT_ANALYSIS | ...
    options: List[str] = field(default_factory=list)
    answer: str = ""
    teacher_guide: List[str] = field(default_factory=list)
    implied_lo: str = ""
    visual_stimulus: VisualStimulus = field(default_factory=VisualStimulus)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AssessmentGroup:
    """Same idea as Group, for assessment: a labeled grouping of items.

    Maths-middle -> type "section", labels "Section A/B/C".
    Maths-secondary -> type "section" with meta["implied_lo"] per section.
    SS -> type "competency"; English -> type "spine".
    """
    type: str
    label: str
    items: List[AssessmentItem] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class LessonPlanView:
    subject: str
    grade: str
    chapter_number: int
    chapter_title: str
    total_periods: int = 0
    groups: List[Group] = field(default_factory=list)  # organizing structure preserved here
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AssessmentView:
    subject: str
    grade: str
    chapter_number: int
    chapter_title: str
    groups: List[AssessmentGroup] = field(default_factory=list)
    teacher_notes: List[str] = field(default_factory=list)
    meta: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ViewModel:
    """The whole render-ready artifact a subject plugin produces for one chapter run."""
    lesson_plan: LessonPlanView
    assessment: AssessmentView

    def to_dict(self) -> Dict[str, Any]:
        """JSON-serializable dict (StimulusType is a str-Enum, so json.dumps works).
        This is what gets output-cached and what the API serves."""
        return asdict(self)
