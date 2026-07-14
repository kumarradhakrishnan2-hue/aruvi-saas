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
from typing import Any, Dict, List, Optional

from .unitize import unitize_lesson_plan_dict


class StimulusType(str, Enum):
    """The renderer keys visual handling off this type — never off subject."""
    NONE = "none"
    SVG = "svg"        # e.g. Mathematics geometry figures
    TABLE = "table"    # pipe-delimited / structured rows (Science, SS)
    NUMBER_LINE = "number_line"  # Maths: an ordered tick line (labels + blank ticks), NOT a grid
    PROSE = "prose"    # fallback descriptive text


class QuestionType(str, Enum):
    """The full question-type registry (docs/assessment-question-type-registry.md §3).

    The PRIMARY render axis: the 3b assessment renderer switches on this, never on
    subject/grade. NOTE the spec's prose says "11 types" but its own §3/§5 enumeration —
    and the real saved-plan corpus — carry exactly these TWELVE; the corpus is authoritative
    (all 12 appear in saved plans as of 2026-07-10)."""
    MCQ = "MCQ"
    TRUE_FALSE = "TRUE_FALSE"
    SCR = "SCR"
    ECR = "ECR"
    OPEN_TASK = "OPEN_TASK"
    PROJECT = "PROJECT"
    WRITING_TASK = "WRITING_TASK"
    FILL_IN = "FILL_IN"
    MATCH = "MATCH"
    ORAL_PROMPT = "ORAL_PROMPT"
    NUM = "NUM"
    EXTRACT_ANALYSIS = "EXTRACT_ANALYSIS"


# The registry's type → render-template collapse (spec §3: 6 card templates; T6 is one
# template with three single-type variant bodies, keyed separately here so the renderer's
# switch stays flat). Adding a future type = map it here + declare its populated fields.
RENDER_TEMPLATE: Dict[str, str] = {
    QuestionType.MCQ: "selected_response",            # T1
    QuestionType.TRUE_FALSE: "true_false",            # T1b — own template (statements+verdicts,
    #                                                   collapsed once in assessment_norm to kill
    #                                                   the stem/options + ticks/prose duplication;
    #                                                   degrades to selected_response with no options)
    QuestionType.SCR: "scr",                          # T2
    QuestionType.ECR: "ecr",                          # T3
    QuestionType.OPEN_TASK: "open_task",              # T4
    QuestionType.PROJECT: "open_task",                # T4
    QuestionType.WRITING_TASK: "open_task",           # T4
    QuestionType.FILL_IN: "cloze_match",              # T5
    QuestionType.MATCH: "match",                      # T5b — own template: pairs render as
    #                                                   left→right rows from a structured
    #                                                   answer_key (kills the answer-as-prose
    #                                                   blob); degrades to prose with no key
    QuestionType.ORAL_PROMPT: "oral",                 # T6a
    QuestionType.NUM: "numeric",                      # T6b
    QuestionType.EXTRACT_ANALYSIS: "passage",         # T6c
}


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
class NormalizedItem:
    """The UNIFORM renderer-facing item contract (registry spec §2). Every subject's
    normalizer flattens its own source shape (three incompatible field families — see
    spec §1) into THIS one shape; the 3b renderer reads ONLY this, never a raw source key.

    Typed blocks (`visual_stimulus`, `passage`) are plain dicts:
        {"type": "svg"|"table"|"prose", "content": str, "table": {"header","rows"}?}
    — the SAME typing as LP visuals, with pipe-tables pre-split via normalize.parse_table
    so no renderer ever re-splits the raw string (the recurring drift-bug class).

    Serialization rule (spec §2): fields absent for a type/subject are OMITTED, not
    blanked — `to_dict()` prunes None/empty; the identity/link fields always survive.
    The Maths-middle/prep no-LO case therefore ships with NO `linked_lo` key at all
    (renderer: line absent, never a blank label)."""
    # ── identity & discriminator ──
    question_type: str = ""            # a QuestionType value (unknown carried as-is)
    template: str = ""                 # RENDER_TEMPLATE[question_type]; "" = unknown → legacy card
    id: Optional[str] = None
    # ── the question ──
    stem: str = ""
    # Structured stem when the prose packs a numbered/lettered list into one string
    # (parsed ONCE in assessment_norm.split_parts, never at render time). `stem_lead` is
    # the intro before the first marker; `stem_parts` is [{marker, text}]. Empty when the
    # stem is plain prose — the renderer then shows `stem` as-is.
    stem_lead: str = ""
    stem_parts: List[Dict[str, str]] = field(default_factory=list)
    visual_stimulus: Optional[Dict[str, Any]] = None
    passage: Optional[Dict[str, Any]] = None      # EXTRACT_ANALYSIS extract (routed, never a generic stimulus)
    options: List[Dict[str, Any]] = field(default_factory=list)  # [{label,text,is_correct}] — selected-response only
    # TRUE_FALSE ONLY: the per-statement key, collapsed ONCE in assessment_norm.tf_statements
    # from the doubly-stored source (statements live in BOTH item_stem and options; verdicts in
    # BOTH each option's is_correct AND the suggested-answer prose). Each row is
    # {marker, text, verdict: bool, reason}. When populated the renderer reads THIS and shows
    # the statements/verdicts exactly once — `options` is then carried-but-not-rendered.
    tf_statements: List[Dict[str, Any]] = field(default_factory=list)
    # MATCH ONLY: the structured pairing key from teacher_guide.answer_key. Each row is
    # {left, right} — the app renders these as left→right rows instead of the free-form
    # suggested_answer prose (which varies too much to structure reliably). Empty when the
    # item carries no answer_key → renderer falls back to the model_answer prose.
    match_pairs: List[Dict[str, Any]] = field(default_factory=list)
    audio_ref: Optional[str] = None    # English listening-spine transcript_ref ("p.NN"); NEVER merged with exercise_ref
    # ── the answer / marking surface ──
    model_answer: Optional[str] = None
    # Structured answer key — same parse as the stem, for multi-part keys packed into one
    # string ("(a) … (b) …" / "1. … 2. …"). Empty → renderer shows `model_answer` as prose.
    answer_lead: str = ""
    answer_parts: List[Dict[str, str]] = field(default_factory=list)
    expected_elements: List[str] = field(default_factory=list)
    option_reveals: Dict[str, str] = field(default_factory=dict)  # label → misconception ("note" key = legacy prose fallback)
    look_fors: List[str] = field(default_factory=list)
    scaffold: Optional[str] = None
    # A fill-in scaffold split into display ROWS so a numbered/step template never runs
    # together in one paragraph (parsed ONCE in assessment_norm.split_scaffold_lines,
    # never at render time). Authored newlines are row breaks; an inline "Step N"/"(N)"/
    # "N." run on a single line is split too; a blank authored line is kept as "" (spacer).
    # Empty → the renderer shows `scaffold` as plain prose.
    scaffold_lines: List[str] = field(default_factory=list)
    method_one_line: Optional[str] = None
    format_of_output: List[str] = field(default_factory=list)
    open_task_guide: Optional[Dict[str, str]] = None   # OPEN_TASK only: format_type/format_rationale/
    #                                                    what_this_demonstrates/reading_the_scaffold/strong_vs_weak_markers
    exercise_ref: Optional[str] = None  # Maths exercise.book_ref — the BOOK ITEM (rendered bold)
    exercise_desc: Optional[str] = None  # Maths exercise.description — the task text after the ref
    inclusivity: Optional[str] = None
    # ── context (quiet meta, never structural labels) ──
    cognitive_demand: Optional[str] = None   # absent key OR "" in source → None (same state)
    competency: Optional[Dict[str, str]] = None   # {code, text}
    # ── the LP link (mirrors link_resolver.stamp; renderer treats as opaque) ──
    linked_lo: Optional[str] = None
    linked_periods: List[int] = field(default_factory=list)
    anchor_period: Optional[int] = None

    # keys that survive pruning even when empty (identity + the always-meaningful link set)
    _KEEP = ("question_type", "template", "stem", "linked_periods", "anchor_period")

    def to_dict(self) -> Dict[str, Any]:
        """Spec §2 'omitted, not blanked': drop None / "" / empty-list / empty-dict fields."""
        d = asdict(self)
        return {k: v for k, v in d.items()
                if k in self._KEEP or v not in (None, "", [], {})}


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
    normalized: Optional[NormalizedItem] = None  # the §2 uniform contract — the ONLY thing 3b reads


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
        This is what gets output-cached and what the API serves.

        Assessment items' `normalized` blocks are re-pruned here (asdict recursion emits
        every field incl. Nones; the wire shape honours the spec-§2 'omitted, not blanked'
        rule via NormalizedItem.to_dict). An item with no normalized contract omits the
        key entirely."""
        d = asdict(self)
        keep = NormalizedItem._KEEP
        for g in d.get("assessment", {}).get("groups", []):
            for it in g.get("items", []):
                n = it.get("normalized")
                if n:
                    it["normalized"] = {k: v for k, v in n.items()
                                        if k in keep or v not in (None, "", [], {})}
                else:
                    it.pop("normalized", None)
        # Lever B (2026-07-13): display-time 'period' -> 'unit' in teacher-facing narrative.
        # Rescues historic saved plans (born saying 'period') without backfilling storage —
        # the engine's view model stays literal; only the served/rendered text is cleaned.
        unitize_lesson_plan_dict(d.get("lesson_plan"))
        return d
