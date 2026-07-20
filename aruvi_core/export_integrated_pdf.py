"""
Integrated Lesson Plan + Assessment — HTML template + PDF export.

The third composition (after the standalone lesson-plan and assessment PDFs):
one document that runs the plan and its assessment together, so a teacher who
"tests on the go" gets the whole chapter — or a single unit — as one artifact.

Design rules (founder, 2026-07-16):
  • COLOUR carries the mode. The lesson-plan halves stay in the warm paper / pine
    world (kraft stage bands, grey period bands); the assessment halves switch to
    the GREEN world (green question header, green answer sub-section). The colour
    change is what tells the reader they've crossed from planning into assessment.
  • ONE intro up top, covering BOTH. The lesson-plan front matter (metadata,
    targeted competencies, progression stages + the axis blurb) is followed by the
    assessment intro paragraph ("This assessment is formative …").
  • The STAGE is printed ONCE (the lesson-plan kraft band). Assessment items do
    NOT repeat it — they simply appear under the unit they belong to.
  • PLACEMENT follows the linking golden rules exactly: an item is placed under the
    unit it ANCHORS to (its closing unit), so a many-units→one-item link surfaces
    once, at the end of the span it covers. This reuses the same anchor_period the
    on-screen renderer keys off.

Scope: whole chapter (``unit_number=None``) or a single unit. Answers are the same
layer as the standalone assessment, governed by ``include_answers``.

This module OWNS a consolidated stylesheet (union of the two exporters' classes) so
it can host both fragment renderers in one document. If the lesson-plan or
assessment styling changes, re-check the mirrored rules here.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from .report_competency import grade_roman, subject_display
from .pdf_fonts import font_face_css
from .export_lesson_pdf import (
    PINE, KRAFT, GREY_BAND, GREY_HEAD, INK, LINE,
    _metadata_table, _competency_table, _english_competency_table, _stage_table, _period_block,
    _group_word, targeted_competencies,
)
from .export_assessment_pdf import (
    G_ACCENT, G_HEAD, G_DARK, G_TINT,
    intro_paragraph, _question_block,
)


# ── placement (the linking golden rules) ────────────────────────────────────

def _anchor_of(it: Dict[str, Any]) -> Any:
    """The unit an item anchors to — meta.anchor_period first (what the on-screen
    renderer uses), then normalized.anchor_period."""
    ap = (it.get("meta", {}) or {}).get("anchor_period")
    if ap is None:
        ap = (it.get("normalized") or {}).get("anchor_period")
    return ap


def _items_by_anchor(av: Dict[str, Any]) -> Dict[Any, List[Dict[str, Any]]]:
    m: Dict[Any, List[Dict[str, Any]]] = {}
    for g in av.get("groups", []) or []:
        for it in g.get("items", []) or []:
            m.setdefault(_anchor_of(it), []).append(it)
    return m


def _iter_group_periods(g: Dict[str, Any]) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    out.extend(g.get("periods", []) or [])
    for c in g.get("children", []) or []:
        out.extend(_iter_group_periods(c))
    return out


# ── body: stage band once · unit · its anchored items ───────────────────────

def _stage_band(word: str, n: Any, label: str) -> str:
    return (
        '<table class="stage-band"><tr><td>'
        f'<span class="st-k">{_esc(word).upper()} {_esc(n)}</span><br/>'
        f'<span class="st">{label}</span>'
        '</td></tr></table>'
    )


def _integrated_body(view: Dict[str, Any], include_answers: bool,
                     unit_number: Optional[int]) -> str:
    lp = view.get("lesson_plan", {}) or {}
    av = view.get("assessment", {}) or {}
    groups = lp.get("groups", []) or []
    by_anchor = _items_by_anchor(av)
    word = _group_word(groups)
    # Mathematics renders its units as one flat run — no section/stage band (founder 2026-07-20).
    _show_band = lp.get("subject", "") != "mathematics"

    placed_ids = set()
    qn = 0
    first_period = True
    out = ""

    for gi, g in enumerate(groups, 1):
        periods = _iter_group_periods(g)
        if unit_number is not None and not any(p.get("number") == unit_number for p in periods):
            continue
        if _show_band:
            out += _stage_band(word, gi, _esc(g.get("label")))
        for p in periods:
            if unit_number is not None and p.get("number") != unit_number:
                continue
            out += _period_block(p, is_first=first_period)
            first_period = False
            items = by_anchor.get(p.get("number"), [])
            if items:
                out += '<div class="assess-head">Assessment</div>'
            for idx, it in enumerate(items):
                qn += 1
                out += _question_block(it, qn, include_answers)
                placed_ids.add(id(it))
                # one row of gap below the rule between consecutive questions
                if idx < len(items) - 1:
                    out += '<div class="q-space">&nbsp;</div>'

    # Whole-chapter only: catch any item whose anchor matched no unit (defensive).
    if unit_number is None:
        leftovers = [it for items in by_anchor.values() for it in items if id(it) not in placed_ids]
        if leftovers:
            out += '<div class="leftover">Further assessment</div>'
            for it in leftovers:
                qn += 1
                out += _question_block(it, qn, include_answers)

    return out


# ── html document ───────────────────────────────────────────────────────────

import html as _html


def _esc(s: Any) -> str:
    return _html.escape(str(s if s is not None else ""))


def _date_spaces(dt: datetime) -> str:
    return f"{dt.day} {dt.strftime('%B')} {dt.year}"


def _css() -> str:
    return f"""
  @page {{ size: a4 portrait; margin: 1.5cm 1.3cm 1.4cm 1.3cm;
    @frame footer {{ -pdf-frame-content: footerContent; bottom: 0.7cm; margin-left: 1.3cm; margin-right: 1.3cm; height: 0.6cm; }} }}
  body {{ font-family: Helvetica; font-size: 8pt; color: {INK}; }}

  .brand-aruvi {{ font-family: Georgia, "Times New Roman", serif; font-size: 16pt; font-weight: bold; color: {PINE}; }}
  .brand-dot {{ font-family: Georgia, serif; font-size: 16pt; font-style: italic; color: #b65a31; }}
  .brand-studio {{ font-size: 7pt; letter-spacing: 1.5px; color: #6b6a63; }}
  .brand-ncf {{ font-family: Georgia, serif; font-style: italic; font-size: 7.5pt; color: #6b6a63; }}
  .rep-title {{ font-family: Georgia, serif; font-size: 11pt; font-weight: bold; color: {PINE}; }}
  .rep-sub {{ font-size: 7pt; color: #555; }}
  .rule-tbl {{ width: 100%; margin-top: 10px; margin-bottom: 12px; }}
  .rule-tbl td {{ border-bottom: 2px solid {INK}; font-size: 1pt; line-height: 1pt; }}

  /* front-matter tables (lesson-plan / kraft) */
  table.grid {{ width: 100%; margin-bottom: 12px; }}
  table.grid td {{ border: 0.75px solid {LINE}; padding: 5px 8px; vertical-align: top; }}
  .gh {{ background-color: {GREY_HEAD}; font-size: 6.5pt; letter-spacing: 0.5px; color: #555;
        text-transform: uppercase; text-align: center; font-weight: bold; }}
  .gh-l {{ text-align: left; }}
  .gv {{ font-size: 8pt; color: #2a2a2a; text-align: center; }}
  .gv-l {{ text-align: left; }}
  .gv-title {{ font-family: Georgia, serif; font-weight: bold; color: {INK}; }}
  .ccode {{ color: {PINE}; font-weight: bold; text-align: center; }}
  .snum {{ color: {PINE}; font-weight: bold; text-align: center; }}
  .cjust {{ font-size: 7pt; font-style: italic; color: #6b6a63; margin-top: 3px; line-height: 1.4; }}
  .axis-note td {{ font-size: 7pt; font-style: italic; color: #555; text-align: left; }}

  .intro {{ font-size: 8pt; color: #2a2a2a; line-height: 1.5; margin: 4px 0 6px; }}

  /* lesson-plan stage band — kraft, no rules */
  .stage-band {{ width: 100%; margin-top: 14px; margin-bottom: 8px; }}
  .stage-band td {{ background-color: {KRAFT}; padding: 8px 12px; text-align: left; }}
  .stage-band .st-k {{ font-family: Helvetica; font-size: 6.5pt; font-weight: bold; letter-spacing: 1px;
                       text-transform: uppercase; color: {PINE}; }}
  .stage-band .st {{ font-family: Georgia, serif; font-size: 10.5pt; font-weight: bold; color: {INK}; }}

  /* lesson-plan unit block */
  .period-band {{ width: 100%; margin-top: 12px; }}
  .period-band td {{ background-color: {GREY_BAND}; border-top: 0.75px solid #e2ddd2; border-bottom: 0.75px solid #e2ddd2;
                     padding: 5px 8px; vertical-align: middle; }}
  .pb-n {{ font-weight: bold; color: {INK}; font-size: 8.5pt; }}
  .pb-dur {{ color: #555; font-size: 8pt; }}
  .pb-title {{ font-family: Georgia, serif; font-weight: bold; color: {INK}; font-size: 9pt; }}
  .pb-ped {{ font-size: 9pt; color: #555; font-style: italic; }}
  .pb-ped-k {{ font-weight: bold; font-style: normal; color: {INK}; }}
  .p-line {{ font-size: 7.5pt; color: #2a2a2a; margin-top: 6px; margin-bottom: 2px; line-height: 1.45; }}
  .p-lbl {{ font-weight: bold; color: {INK}; }}
  .phase-tbl {{ width: 100%; margin-top: 5px; }}
  .phase-tbl td {{ vertical-align: top; padding: 4px 0; border-bottom: 0.5px solid #f0ede9; }}
  .ph-band {{ width: 54px; font-size: 6.5pt; color: #8a8a86; padding-right: 12px; }}
  .ph-text {{ font-size: 7.5pt; color: #2a2a2a; line-height: 1.45; }}
  .u-hw {{ margin-top: 6px; padding: 5px 8px; background-color: {GREY_BAND}; }}
  .u-hw-k {{ font-weight: bold; color: {INK}; font-size: 7.5pt; }}
  .u-hw-t {{ font-size: 7.5pt; color: #2a2a2a; }}

  /* assessment item (green) */
  .qmeta {{ width: 100%; margin-top: 10px; margin-bottom: 6px; }}
  .qmeta td {{ background-color: {G_HEAD}; vertical-align: top; }}
  .qm-top {{ padding: 5px 10px 0 10px; }}
  .qm-bot {{ padding: 0 10px 5px 10px; }}
  .qm-l {{ text-align: left; }}
  .qm-r {{ text-align: right; white-space: nowrap; }}
  .qm-qn {{ font-family: Georgia, serif; font-size: 9pt; font-weight: bold; color: {G_DARK}; }}
  .qm-k {{ font-size: 6.5pt; font-weight: bold; letter-spacing: 0.5px; text-transform: uppercase; color: {G_ACCENT}; }}
  .qm-v {{ font-size: 7.5pt; color: #1f3a30; line-height: 1.35; }}
  .qm-cogv {{ font-size: 7.5pt; font-weight: normal; color: #1f3a30; text-transform: none; letter-spacing: 0; }}

  .assess-head {{ font-size: 10pt; font-weight: bold; text-align: center; color: {G_DARK}; margin: 12px 0 6px; }}
  .q-stem {{ font-size: 8pt; color: {INK}; line-height: 1.45; }}
  .q-n {{ font-weight: bold; color: {INK}; }}
  .opts {{ width: 100%; margin-top: 5px; }}
  .opt-lab {{ width: 22px; font-weight: bold; color: #444; font-size: 7.5pt; vertical-align: top; padding: 2px 0; }}
  .opt-txt {{ font-size: 7.5pt; color: #2a2a2a; padding: 2px 0; vertical-align: top; }}
  .opt-correct .opt-lab, .opt-correct .opt-txt {{ color: {G_ACCENT}; font-weight: bold; }}
  .stim-tbl {{ width: 100%; margin: 6px 0; table-layout: fixed; }}
  .st-th {{ background-color: {G_HEAD}; font-size: 7pt; font-weight: bold; color: {G_DARK};
            border: 0.5px solid #cde0d8; padding: 4px 6px; word-wrap: break-word; }}
  .st-td {{ font-size: 7pt; color: #2a2a2a; border: 0.5px solid #cde0d8; padding: 4px 6px; word-wrap: break-word; }}
  .stim-tbl-wide .st-th, .stim-tbl-wide .st-td {{ font-size: 6pt; padding: 3px 4px; }}
  .stim-prose {{ font-size: 7.5pt; color: #2a2a2a; font-style: italic; margin: 5px 0; }}
  .stim-note {{ font-size: 7pt; color: #8a8a86; font-style: italic; margin: 5px 0; }}
  .scaf {{ font-size: 7.5pt; color: #2a2a2a; margin: 4px 0 2px; }}
  .task-k {{ font-size: 6.5pt; font-weight: bold; letter-spacing: 0.5px; text-transform: uppercase; color: {G_ACCENT}; }}
  .task-ul {{ margin: 2px 0 0 14px; padding: 0; }}
  .task-ul li {{ font-size: 7.5pt; color: #2a2a2a; margin-bottom: 1px; }}
  .ans {{ margin-top: 8px; }}
  .ans-title {{ font-size: 8pt; font-weight: bold; text-align: center; color: {G_DARK};
                background-color: {G_TINT}; padding: 4px 0; margin-bottom: 5px; }}
  .ans-sub {{ margin-top: 4px; }}
  .ans-k {{ font-weight: bold; color: {G_DARK}; font-size: 7pt; }}
  .ans-t {{ font-size: 7.5pt; color: #1f3a30; }}
  .ans-ul {{ margin: 2px 0 0 14px; padding: 0; }}
  .ans-ul li {{ font-size: 7pt; color: #1f3a30; margin-bottom: 1px; }}
  .rev-row td {{ font-size: 7pt; color: #1f3a30; padding: 1px 0; vertical-align: top; }}
  .rev-lab {{ width: 20px; font-weight: bold; color: {G_ACCENT}; }}
  .q-rule {{ width: 100%; margin-top: 9px; }}
  .q-rule td {{ border-bottom: 0.75px solid #7fa091; font-size: 1pt; line-height: 1pt; }}
  .q-space {{ font-size: 11pt; line-height: 11pt; }}

  .leftover {{ font-size: 7pt; font-weight: bold; letter-spacing: 0.6px; text-transform: uppercase;
               color: {G_DARK}; margin-top: 12px; }}
  .footer {{ font-size: 6pt; color: #999; }}
"""


def render_integrated_pdf_html(
    view: Dict[str, Any],
    *,
    include_answers: bool = False,
    unit_number: Optional[int] = None,
    competencies: Optional[List[Dict[str, str]]] = None,
    competency_spines: Optional[List[Dict[str, Any]]] = None,
    plan_date: Optional[datetime] = None,
    generated_at: Optional[datetime] = None,
) -> str:
    lp = view.get("lesson_plan", {}) or {}
    av = view.get("assessment", {}) or {}
    groups = lp.get("groups", []) or []
    competencies = competencies or []

    subject_slug = lp.get("subject", "")
    subject = subject_display(subject_slug)
    grade = grade_roman(lp.get("grade", ""))
    ch_no = lp.get("chapter_number", "")
    ch_title = lp.get("chapter_title", "")
    masthead_dt = generated_at or plan_date or datetime.now()

    from .export_lesson_pdf import _duration_breakdown
    total_periods = lp.get("total_periods") or sum(len(g.get("periods", []) or []) for g in groups)
    duration_str = _duration_breakdown(lp)

    # Front matter: whole-chapter shows the full lesson-plan front matter; a unit
    # sheet keeps just the chapter id line. BOTH carry the assessment intro paragraph.
    front = _metadata_table(ch_no, ch_title, total_periods, duration_str)
    if unit_number is None:
        if competency_spines:
            front += _english_competency_table(competency_spines)  # spine table lists the spines →
        else:                                                       # skip the redundant stage table
            front += _competency_table(competencies)
            # Mathematics has no meaningful progression axis — suppress the stage table for
            # maths too (founder 2026-07-20). Secondary Science is section-anchored and FLAT
            # (no per-period progression_stage — see science subject.py), so its stage table
            # would only re-list the chapter sections; suppress it there too (founder
            # 2026-07-20). Detect by the data, not the grade string: secondary science emits
            # top-level groups typed "section", middle science "progression_stage"/"stage".
            # Other non-English subjects keep it. (Mirrors export_lesson_pdf._no_progression.)
            _science_sectioned = (
                subject_slug == "science"
                and bool(groups)
                and groups[0].get("type") == "section"
            )
            if subject_slug != "mathematics" and not _science_sectioned:
                front += _stage_table(groups)
    front += f'<p class="intro">{_esc(intro_paragraph(subject_slug, groups, lp.get("grade")))}</p>'

    body = _integrated_body(view, include_answers, unit_number)
    scope = f"Unit {unit_number}" if unit_number is not None else "Full chapter"
    ans_flag = " · With answers" if include_answers else ""

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{font_face_css()}{_css()}</style></head><body>

  <table class="hdr" width="100%"><tr>
    <td width="60%">
      <span class="brand-aruvi">Aruvi</span><span class="brand-dot">.</span>
      <span class="brand-studio">LESSON STUDIO</span><br/>
      <span class="brand-ncf">NCF 2023 aligned</span>
    </td>
    <td width="40%" align="right">
      <span class="rep-title">Lesson plan &amp; assessment</span><br/>
      <span class="rep-sub">Grade {_esc(grade)} · {_esc(subject)} · {_esc(_date_spaces(masthead_dt))}</span>
    </td>
  </tr></table>
  <table class="rule-tbl"><tr><td></td></tr></table>

  {front}
  {body}

  <div id="footerContent" class="footer">
    Aruvi · Lesson plan &amp; assessment · Grade {_esc(grade)} · {_esc(subject)} · Ch {_esc(ch_no)} · {scope}{ans_flag} · Confidential
  </div>
</body></html>"""


def export_integrated_pdf(
    view: Dict[str, Any],
    *,
    include_answers: bool = False,
    unit_number: Optional[int] = None,
    competencies: Optional[List[Dict[str, str]]] = None,
    competency_spines: Optional[List[Dict[str, Any]]] = None,
    plan_date: Optional[datetime] = None,
    generated_at: Optional[datetime] = None,
) -> bytes:
    """Render the integrated Lesson Plan + Assessment to PDF bytes (xhtml2pdf)."""
    from io import BytesIO
    from xhtml2pdf import pisa

    html_str = render_integrated_pdf_html(
        view, include_answers=include_answers, unit_number=unit_number,
        competencies=competencies, competency_spines=competency_spines,
        plan_date=plan_date, generated_at=generated_at,
    )
    buf = BytesIO()
    result = pisa.CreatePDF(html_str, dest=buf, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"xhtml2pdf failed with {result.err} error(s)")
    return buf.getvalue()
