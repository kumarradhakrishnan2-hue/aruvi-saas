"""
Assessment item normalization → the uniform NormalizedItem contract.

The registry spec (docs/assessment-question-type-registry.md §1) identifies THREE
incompatible source field-shapes for the same question_type string, by subject family:

  • Constitution family — Science, Social Sciences, TWAU: `question_text`/`task`,
    `expected_elements[]`, `look_for[]`, `scaffold`, `format_of_output[]`, and a
    `guide{TYPE: {what_each_option_reveals, inclusivity, …}}` dict keyed by question type.
  • Maths family — `prompt`, `teacher_guide{expected_answer, method_one_line,
    what_each_option_reveals, inclusivity}`, `exercise{book_ref, description}`.
    SECONDARY maths is a verified hybrid (saved-file inspection 2026-07-10): it carries
    `question_text` + constitution-style `guide{TYPE}` + TOP-LEVEL expected_answer/
    method_one_line/look_for/expected_elements/scaffold — both shapes are read here.
  • English family — `item_stem`, `teacher_guide{suggested_answer, expected_elements[],
    what_each_option_reveals, note}`, `transcript_ref`.

One builder per family (spec §4 master mapping); each subject plugin's normalizer calls
its family builder ONCE per item, after link_resolver.stamp() has filled the meta, and
attaches the result as AssessmentItem.normalized. The 3b renderer reads ONLY that.

Locked rules honoured here:
  • cognitive_demand: absent key OR "" → None (same state; spec Open-items).
  • audio_ref: English transcript_ref ONLY when source_spine is the listening spine —
    its own field, NEVER merged with Maths exercise_ref.
  • EXTRACT_ANALYSIS: the extract routes to `passage`, never a generic stimulus.
  • Legacy English MCQ prose `note` → option_reveals under the "note" key (fallback the
    renderer shows as prose; constitutions were rewritten 2026-07-10, saved plans migrated,
    but un-migrated fallback items must still normalize).
  • English TRUE_FALSE `note` (verdict + justification) → model_answer, not reveals.
  • Tables are pre-split via normalize.parse_table — no renderer re-splits pipe strings.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from .normalize import as_list, classify_stimulus, parse_table
from .view_model import NormalizedItem, RENDER_TEMPLATE, StimulusType

_OT_GUIDE_KEYS = ("format_type", "format_rationale", "what_this_demonstrates",
                  "reading_the_scaffold", "strong_vs_weak_markers",
                  "observation_rubric")  # TWAU performance_task=true variant (Rule 9)


# ── small shared pieces ──────────────────────────────────────────────────────────
def _clean(v: Any) -> Optional[str]:
    """'' / None / whitespace → None; else the stripped string. The empty-string-and-
    absent-are-the-same-state rule (cognitive_demand et al.)."""
    s = str(v).strip() if v is not None else ""
    return s or None


def typed_block(raw: Any) -> Optional[Dict[str, Any]]:
    """Type a raw stimulus string exactly like LP visuals (classify_stimulus), with
    pipe-tables pre-split via parse_table so the wire shape is renderer-ready."""
    vs = classify_stimulus(raw if isinstance(raw, str) else "")
    if vs.type == StimulusType.NONE:
        return None
    d: Dict[str, Any] = {"type": vs.type.value, "content": vs.content}
    if vs.type == StimulusType.TABLE:
        d["table"] = parse_table(vs.content)
    return d


def structured_options(raw: Any) -> List[Dict[str, Any]]:
    """Options preserved STRUCTURED ({label, text, is_correct}) — unlike the legacy
    normalize_options flattening, the 3b renderer marks the correct one itself."""
    out: List[Dict[str, Any]] = []
    for o in raw or []:
        if isinstance(o, dict):
            out.append({"label": str(o.get("label") or ""),
                        "text": str(o.get("text") or o.get("option") or ""),
                        "is_correct": bool(o.get("is_correct"))})
        elif str(o).strip():
            out.append({"label": "", "text": str(o), "is_correct": False})
    return out


def _competency(v: Any) -> Optional[Dict[str, str]]:
    if not isinstance(v, dict):
        return None
    code = _clean(v.get("c_code") or v.get("code"))
    text = _clean(v.get("competency_text") or v.get("text"))
    if not code and not text:
        return None
    return {"code": code or "", "text": text or ""}


def _reveals(v: Any) -> Dict[str, str]:
    if not isinstance(v, dict):
        return {}
    return {str(k): str(t) for k, t in v.items() if _clean(t)}


def _ot_guide(guide_for_type: Any) -> Optional[Dict[str, str]]:
    if not isinstance(guide_for_type, dict):
        return None
    d = {k: str(guide_for_type[k]) for k in _OT_GUIDE_KEYS if _clean(guide_for_type.get(k))}
    return d or None


def _finish(n: NormalizedItem) -> NormalizedItem:
    """Shared tail: template lookup + EXTRACT_ANALYSIS passage routing."""
    n.template = RENDER_TEMPLATE.get(n.question_type, "")
    if n.question_type == "EXTRACT_ANALYSIS" and n.visual_stimulus:
        n.passage, n.visual_stimulus = n.visual_stimulus, None
    return n


def _link(n: NormalizedItem, meta: Dict[str, Any]) -> NormalizedItem:
    """Copy the stamped link contract in — call AFTER link_resolver.stamp(meta, …)."""
    n.linked_periods = list(meta.get("linked_periods") or [])
    n.anchor_period = meta.get("anchor_period")
    n.linked_lo = meta.get("linked_lo") or None
    return n


# ── family builders (spec §4 master mapping) ─────────────────────────────────────
_FLAT_GUIDE_KEYS = ("what_each_option_reveals", "inclusivity") + _OT_GUIDE_KEYS


def from_constitution(it: Dict[str, Any], meta: Dict[str, Any]) -> NormalizedItem:
    """Science (both stages), Social Sciences, TWAU.

    Canonical guide shape: nested under the item's own type key
    (`guide.MCQ.what_each_option_reveals`) — since 2026-07-10 all three constitutions
    specify it (SS v1.7 / TWAU v1.3 amended from their earlier FLAT shape, mirroring the
    English MCQ-reveals fix) and the saved corpus was migrated in place (pure relocation).
    The FLAT read below is kept as a legacy fallback only — corpus-unused, exercised by
    nothing current, tolerated for any stray pre-migration file. SS/TWAU duplicate SCR/ECR
    rubrics into the guide, but the top-level fields carry them too, so the top-level read
    below stays the single source for those."""
    qt = str(it.get("question_type") or "")
    guide = it.get("guide") if isinstance(it.get("guide"), dict) else {}
    gd = guide.get(qt) if isinstance(guide.get(qt), dict) else None
    if gd is None and any(k in guide for k in _FLAT_GUIDE_KEYS):
        gd = guide                      # the SS/TWAU flat shape
    gd = gd or {}
    reveals = _reveals(gd.get("what_each_option_reveals"))
    if not reveals and qt == "MCQ":
        # True last resort for shapes carrying neither guide form: the SS/TWAU `annotation`
        # prose (a per-item marking note) lands under the same "note" fallback key as
        # legacy English MCQs and renders as prose.
        note = _clean(it.get("annotation"))
        if note:
            reveals = {"note": note}
    n = NormalizedItem(
        question_type=qt,
        id=_clean(it.get("id")),
        stem=str(it.get("question_text") or it.get("task") or ""),
        visual_stimulus=typed_block(it.get("visual_stimulus")),
        options=structured_options(it.get("options")),
        expected_elements=as_list(it.get("expected_elements")),
        option_reveals=reveals,
        look_fors=as_list(it.get("look_for")),
        scaffold=_clean(it.get("scaffold")),
        format_of_output=as_list(it.get("format_of_output")),
        open_task_guide=_ot_guide(gd) if qt == "OPEN_TASK" else None,
        inclusivity=_clean(gd.get("inclusivity")),
        cognitive_demand=_clean(it.get("cognitive_demand")),
        competency=_competency(it.get("competency")),
    )
    return _finish(_link(n, meta))


def from_maths(it: Dict[str, Any], meta: Dict[str, Any]) -> NormalizedItem:
    """Mathematics, all stages. Middle/prep carry the teacher_guide dict; SECONDARY is the
    hybrid (top-level expected_answer/method_one_line + constitution-style guide{TYPE} +
    look_for/expected_elements/scaffold) — both shapes read tolerantly, spec §4 column 2."""
    qt = str(it.get("question_type") or "")
    tg = it.get("teacher_guide") if isinstance(it.get("teacher_guide"), dict) else {}
    gd = (it.get("guide") or {}).get(qt) or {}
    ex = it.get("exercise") if isinstance(it.get("exercise"), dict) else {}
    ref = _clean(ex.get("book_ref"))
    desc = _clean(ex.get("description"))
    n = NormalizedItem(
        question_type=qt,
        id=_clean(it.get("id")),
        stem=str(it.get("prompt") or it.get("question_text") or it.get("task") or ""),
        visual_stimulus=typed_block(it.get("visual_stimulus")),
        options=structured_options(it.get("options")),
        model_answer=_clean(tg.get("expected_answer")) or _clean(it.get("expected_answer")),
        expected_elements=as_list(it.get("expected_elements")),
        option_reveals=_reveals(tg.get("what_each_option_reveals")) or _reveals(gd.get("what_each_option_reveals")),
        look_fors=as_list(it.get("look_for")),
        scaffold=_clean(it.get("scaffold")),
        method_one_line=_clean(tg.get("method_one_line")) or _clean(it.get("method_one_line")),
        format_of_output=as_list(it.get("format_of_output")),
        open_task_guide=_ot_guide(gd) if qt == "OPEN_TASK" else None,
        exercise_ref=(f"{ref} — {desc}" if ref and desc else ref or desc),
        inclusivity=_clean(tg.get("inclusivity")) or _clean(gd.get("inclusivity")),
        cognitive_demand=_clean(it.get("cognitive_demand")),   # present secondary only; ""/absent → None
        competency=_competency(it.get("competency")),
    )
    return _finish(_link(n, meta))


def from_english(it: Dict[str, Any], meta: Dict[str, Any]) -> NormalizedItem:
    """English, all stages."""
    qt = str(it.get("question_type") or "")
    tg = it.get("teacher_guide") if isinstance(it.get("teacher_guide"), dict) else {}
    note = _clean(tg.get("note"))
    reveals = _reveals(tg.get("what_each_option_reveals"))
    if not reveals and qt == "MCQ" and note:
        reveals = {"note": note}          # legacy prose fallback, rendered as prose
    model = _clean(tg.get("suggested_answer"))
    if not model and qt == "TRUE_FALSE" and note:
        model = note                      # TRUE_FALSE verdict+justification → model_answer
    spine = str(it.get("source_spine") or "").lower()
    n = NormalizedItem(
        question_type=qt,
        id=_clean(it.get("id")),
        stem=str(it.get("item_stem") or it.get("question_text") or ""),
        visual_stimulus=typed_block(it.get("visual_stimulus")),
        options=structured_options(it.get("options")),
        audio_ref=_clean(it.get("transcript_ref")) if "listening" in spine else None,
        model_answer=model,
        expected_elements=as_list(tg.get("expected_elements")),
        option_reveals=reveals,
        cognitive_demand=_clean(it.get("cognitive_demand")),   # ""/absent → None (all English)
    )
    return _finish(_link(n, meta))
