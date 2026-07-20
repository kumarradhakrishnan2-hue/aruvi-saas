"""
Lesson Plan Report — HTML template + PDF export.

Sibling of ``export_allocation_pdf.py`` and built on the SAME proven pattern:
a pure-Python xhtml2pdf (reportlab + html5lib) render with NO system-library
dependency, so the PDF generates identically on a teacher's Mac/Windows and on a
cloud server with nothing to ``brew install``.

Design (founder-directed, 2026-07-16): the BODY follows the prototype lesson-plan
report — a chapter metadata table, a targeted-competencies table, a progression-
stage table, then per-stage bands, and per-period blocks (Materials · Activity
Description · the timed phase spine). The TOP (masthead) follows the ALLOCATION
report's surface — the warm "Aruvi. LESSON STUDIO / NCF 2023 aligned" brand block
with the heavy rule — so the two exports read as siblings. Accents use Aruvi pine
(#164436) rather than the prototype's generic blue.

Founder rules kept from the on-screen renderer: LO is NEVER printed in a lesson
plan (it is reserved for assessment), and assessment items are NOT part of this
document (that is the separate Assessment PDF).

Scope for this first cut is WHOLE CHAPTER (every stage + period, in order).

Data sources (the renderer is subject-agnostic; the caller enriches, exactly as
``api.main._build_report`` does for the allocation report):
  • ``view``        — ViewModel.to_dict()'s ``lesson_plan`` (structure: groups →
                      periods with title/approach/phases/materials/homework).
  • ``competencies``— [{c_code, text}] for the chapter, from the mapping's
                      ``primary`` list + the competency-description glossary
                      (see ``targeted_competencies``).
  • ``activity_desc_by_period`` — {period_number: text}; the raw plan's
                      ``activity_description`` per period, which the view model
                      does not carry (see ``activity_descriptions_from_result``).
"""

from __future__ import annotations

import html as _html
import re
from datetime import datetime
from typing import Any, Dict, List, Optional

from .report_competency import grade_roman, subject_display
from .pdf_fonts import font_face_css


# ── enrichment helpers (pure; the endpoint/sample calls these) ──────────────

def targeted_competencies(mapping: Dict[str, Any],
                          descriptions: Dict[str, str]) -> List[Dict[str, str]]:
    """The chapter's targeted competencies as [{c_code, text, justification}]: text = the
    glossary description, justification = the mapping's chapter-level rationale for why this
    competency applies (rendered as a sub-line in the report; the on-screen view omits it).
    Reads the mapping's ``primary`` list (science/SS/… effort-index shape), then the
    competency-weight shape (``core_competencies`` / ``adjunct_competencies``). De-duplicated,
    order preserved. When there's no glossary description the justification stands in for the
    text and is NOT repeated as a sub-line."""
    out: List[Dict[str, str]] = []
    seen = set()
    for key in ("primary", "core_competencies", "adjunct_competencies"):
        block = mapping.get(key)
        if not isinstance(block, list):
            continue
        for c in block:
            if not isinstance(c, dict):
                continue
            code = c.get("c_code") or c.get("code")
            if not code or code in seen:
                continue
            seen.add(code)
            desc = descriptions.get(code)
            just = c.get("justification") or ""
            out.append({"c_code": code, "text": desc or just,
                        "justification": ("" if not desc else just)})
    return out


def activity_descriptions_from_result(result: Dict[str, Any]) -> Dict[int, str]:
    """{period_number: activity_description} from the raw saved-plan result. The
    view model normalizes titles/phases/materials but drops the free-text activity
    description, so it is read from the raw periods here by period number."""
    periods = (result.get("lesson_plan", {}) or {}).get("periods", []) or []
    out: Dict[int, str] = {}
    for p in periods:
        n = p.get("period_number")
        desc = p.get("activity_description")
        if n is not None and desc:
            out[int(n)] = desc
    return out


# ── unit flattening + axis (mirrors LessonView.flattenUnits) ────────────────

CTX_LABEL = {
    "spine": "Spine", "section": "Section", "competency": "Competency",
    "stage": "Stage", "progression_stage": "Stage", "unit": "Unit",
}


def _top_groups(lp: Dict[str, Any]) -> List[Dict[str, Any]]:
    """The organizing spine at the top level (progression stages / spines / sections)."""
    return lp.get("groups", []) or []


def _group_word(groups: List[Dict[str, Any]]) -> str:
    """The word for the organizing axis: 'Stage' (science), 'Spine' (English), etc."""
    gt = groups[0].get("type") if groups else ""
    return CTX_LABEL.get(gt, "Stage")


# ── small formatting helpers ────────────────────────────────────────────────

def _esc(s: Any) -> str:
    return _html.escape(str(s if s is not None else ""))


_BOLD_RE = re.compile(r"\*\*(.+?)\*\*")


def _bold_marks(s: Any) -> str:
    return _BOLD_RE.sub(r"<b>\1</b>", _esc(s))


def _date_spaces(dt: datetime) -> str:
    return f"{dt.day} {dt.strftime('%B')} {dt.year}"


def _phase_duration(ph: Dict[str, Any]) -> str:
    """The phase length in minutes ('7 min'), from end − start; falls back to the
    raw band label when the minutes can't be parsed."""
    a, b = ph.get("start_min"), ph.get("end_min")
    if isinstance(a, (int, float)) and isinstance(b, (int, float)):
        return f"{int(b) - int(a)} min"
    return str(ph.get("label") or "")


def _iter_periods(lp: Dict[str, Any]):
    """Every period, top-level and nested (English section → spine)."""
    def walk(groups):
        for g in groups:
            for p in g.get("periods", []) or []:
                yield p
            yield from walk(g.get("children", []) or [])
    yield from walk(_top_groups(lp))


def _duration_breakdown(lp: Dict[str, Any]) -> str:
    """The period-length distribution, e.g. '40 mins × 7 · 60 mins × 3'
    (ascending by minutes)."""
    counts: Dict[int, int] = {}
    for p in _iter_periods(lp):
        d = (p.get("meta", {}) or {}).get("duration_minutes")
        if isinstance(d, (int, float)):
            counts[int(d)] = counts.get(int(d), 0) + 1
    if not counts:
        return "—"
    return " · ".join(f"{m} mins × {counts[m]}" for m in sorted(counts))


def _total_minutes(lp: Dict[str, Any]) -> int:
    total = 0
    for g in _top_groups(lp):
        for p in g.get("periods", []) or []:
            total += int((p.get("meta", {}) or {}).get("duration_minutes") or 0)
            for child in g.get("children", []) or []:
                pass
    # children periods too (English section → spine)
    def add_children(groups):
        nonlocal total
        for g in groups:
            for c in g.get("children", []) or []:
                for p in c.get("periods", []) or []:
                    total += int((p.get("meta", {}) or {}).get("duration_minutes") or 0)
                add_children([c])
    add_children(_top_groups(lp))
    return total


# ── PDF rendering (xhtml2pdf) ───────────────────────────────────────────────

GREY_HEAD = "#f1ece2"     # warm paper-sunk — table header rows
GREY_BAND = "#f4f2ee"     # period bands (the lighter of the two)
KRAFT = "#ebe3d3"         # stage bands — a stronger warm fill, no rules
PINE = "#164436"          # brand masthead + body accent (codes + stage numbers)
INK = "#1a1917"
LINE = "#dddddd"

# The organizing-axis blurb shown under the progression-stage table — verbatim from
# the on-screen Chapter Organization page (LessonView.jsx AXIS_INFO), keyed by the
# top-level group type. First letter capitalized for the document.
AXIS_INFO = {
    "stage": "The learning progression each group moves through, from first contact to confident practice — the staged, inquiry-led sequence the NCF asks of Science.",
    "progression_stage": "The learning progression each group moves through, from first contact to confident practice — the staged, inquiry-led sequence the NCF asks of Science.",
    "section": "The parts of the chapter, taught in the graded, build-from-the-familiar sequence the NCF encourages.",
    "competency": "The skill each group of units builds — the competency-based design at the heart of the NCF.",
    "spine": "The language skills the units develop together, in the integrated way the NCF asks languages to be taught.",
}


def render_lesson_pdf_html(
    view: Dict[str, Any],
    *,
    competencies: Optional[List[Dict[str, str]]] = None,
    competency_spines: Optional[List[Dict[str, Any]]] = None,
    activity_desc_by_period: Optional[Dict[int, str]] = None,
    plan_date: Optional[datetime] = None,
    generated_at: Optional[datetime] = None,
) -> str:
    lp = view.get("lesson_plan", {}) or {}
    competencies = competencies or []
    activity_desc_by_period = activity_desc_by_period or {}
    groups = _top_groups(lp)

    subject = subject_display(lp.get("subject", ""))
    grade = grade_roman(lp.get("grade", ""))
    ch_no = lp.get("chapter_number", "")
    ch_title = lp.get("chapter_title", "")
    masthead_dt = generated_at or plan_date or datetime.now()

    total_periods = lp.get("total_periods") or sum(len(g.get("periods", []) or []) for g in groups)
    duration_str = _duration_breakdown(lp)

    meta_table = _metadata_table(ch_no, ch_title, total_periods, duration_str)
    comp_table = _english_competency_table(competency_spines) if competency_spines else _competency_table(competencies)
    # English's spine competency table already lists the spines, so the progression-spine table is
    # redundant there — suppress it. Mathematics has no meaningful progression axis either (prep
    # collapses to a single "Lesson" group; middle/secondary sections carry no cross-chapter
    # progression), so suppress it for maths as well (founder 2026-07-20). Secondary Science is
    # section-anchored and FLAT (no progression_stage per period — see science subject.py), so its
    # only "progression" table would just re-list the chapter sections; suppress it there too
    # (founder 2026-07-20). Detect by the data, not the grade string: secondary science emits
    # top-level groups typed "section" where middle science emits "progression_stage"/"stage".
    # Other subjects keep it.
    _science_sectioned = (
        lp.get("subject", "") == "science"
        and bool(groups)
        and groups[0].get("type") == "section"
    )
    _no_progression = (
        bool(competency_spines)
        or lp.get("subject", "") == "mathematics"
        or _science_sectioned
    )
    stage_table = "" if _no_progression else _stage_table(groups)
    body = _stages_body(groups, lp.get("subject", ""))

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>{font_face_css()}
  @page {{
    size: a4 portrait; margin: 1.5cm 1.3cm 1.4cm 1.3cm;
    @frame footer {{ -pdf-frame-content: footerContent; bottom: 0.7cm; margin-left: 1.3cm; margin-right: 1.3cm; height: 0.6cm; }}
  }}
  body {{ font-family: Helvetica; font-size: 8pt; color: {INK}; }}

  .brand-aruvi {{ font-family: Georgia, "Times New Roman", serif; font-size: 16pt; font-weight: bold; color: {PINE}; }}
  .brand-dot {{ font-family: Georgia, serif; font-size: 16pt; font-style: italic; color: #b65a31; }}
  .brand-studio {{ font-size: 7pt; letter-spacing: 1.5px; color: #6b6a63; }}
  .brand-ncf {{ font-family: Georgia, serif; font-style: italic; font-size: 7.5pt; color: #6b6a63; }}
  .rep-title {{ font-family: Georgia, serif; font-size: 11pt; font-weight: bold; color: {PINE}; }}
  .rep-sub {{ font-size: 7pt; color: #555; }}
  .rule-tbl {{ width: 100%; margin-top: 10px; margin-bottom: 14px; }}
  .rule-tbl td {{ border-bottom: 2px solid {INK}; font-size: 1pt; line-height: 1pt; }}

  table.grid {{ width: 100%; margin-bottom: 12px; }}
  table.grid td, table.grid th {{ border: 0.75px solid {LINE}; padding: 5px 8px; vertical-align: top; }}
  .gh {{ background-color: {GREY_HEAD}; font-size: 6.5pt; letter-spacing: 0.5px; color: #555;
        text-transform: uppercase; text-align: center; font-weight: bold; }}
  .gh-l {{ text-align: left; }}
  .gv {{ font-size: 8pt; color: #2a2a2a; text-align: center; }}
  .gv-l {{ text-align: left; }}
  .gv-title {{ font-family: Georgia, serif; font-weight: bold; color: {INK}; }}
  .ccode {{ color: {PINE}; font-weight: bold; text-align: center; }}
  .snum {{ color: {PINE}; font-weight: bold; text-align: center; }}
  .ecg-sp {{ font-weight: bold; vertical-align: middle; text-align: center; }}
  .ecg-sec {{ vertical-align: middle; }}
  .cjust {{ font-size: 7pt; font-style: italic; color: #6b6a63; margin-top: 3px; line-height: 1.4; }}
  .axis-note td {{ font-size: 7pt; font-style: italic; color: #555; text-align: left; }}

  .stage-band {{ width: 100%; margin-top: 14px; margin-bottom: 8px; }}
  .stage-band td {{ background-color: {KRAFT}; padding: 8px 12px; text-align: left; }}
  .stage-band .st-k {{ font-family: Helvetica; font-size: 6.5pt; font-weight: bold; letter-spacing: 1px;
                       text-transform: uppercase; color: {PINE}; }}
  .stage-band .st {{ font-family: Georgia, serif; font-size: 10.5pt; font-weight: bold; color: {INK}; }}

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
  .ph-band {{ width: 60px; font-size: 6.5pt; color: #8a8a86; padding-right: 12px; }}
  .ph-text {{ font-size: 7.5pt; color: #2a2a2a; line-height: 1.45; }}

  .u-hw {{ margin-top: 6px; padding: 5px 8px; background-color: {GREY_BAND}; }}
  .u-hw-k {{ font-weight: bold; color: {INK}; font-size: 7.5pt; }}
  .u-hw-t {{ font-size: 7.5pt; color: #2a2a2a; }}

  .footer {{ font-size: 6pt; color: #999; }}
</style></head><body>

  <table class="hdr" width="100%"><tr>
    <td width="60%">
      <span class="brand-aruvi">Aruvi</span><span class="brand-dot">.</span>
      <span class="brand-studio">LESSON STUDIO</span><br/>
      <span class="brand-ncf">NCF 2023 aligned</span>
    </td>
    <td width="40%" align="right">
      <span class="rep-title">Lesson plan</span><br/>
      <span class="rep-sub">Grade {_esc(grade)} · {_esc(subject)} · {_esc(_date_spaces(masthead_dt))}</span>
    </td>
  </tr></table>
  <table class="rule-tbl"><tr><td></td></tr></table>

  {meta_table}
  {comp_table}
  {stage_table}
  {body}

  <div id="footerContent" class="footer">
    Aruvi · Lesson plan · Grade {_esc(grade)} · {_esc(subject)} · Ch {_esc(ch_no)} · Confidential
  </div>
</body></html>"""


def _metadata_table(ch_no, ch_title, total_periods, duration_str) -> str:
    return (
        '<table class="grid"><tr>'
        '<td class="gh" width="12%">Chapter</td>'
        '<td class="gh" width="45%">Title</td>'
        '<td class="gh" width="15%">Total periods</td>'
        '<td class="gh" width="28%">Duration</td></tr>'
        f'<tr><td class="gv">Ch {_esc(ch_no)}</td>'
        f'<td class="gv gv-title">{_esc(ch_title)}</td>'
        f'<td class="gv">{_esc(total_periods)}</td>'
        f'<td class="gv">{_esc(duration_str)}</td></tr></table>'
    )


def _competency_table(comps: List[Dict[str, str]]) -> str:
    if not comps:
        return ""
    # When the mapping carries a chapter-level rationale, show it in a THIRD column, in the same
    # font/size as the competency text (report-only depth; the on-screen view omits it).
    if any(c.get("justification") for c in comps):
        rows = "".join(
            f'<tr><td class="ccode" width="10%">{_esc(c["c_code"])}</td>'
            f'<td class="gv gv-l" width="42%">{_esc(c["text"])}</td>'
            f'<td class="gv gv-l">{_esc(c.get("justification"))}</td></tr>'
            for c in comps
        )
        return (
            '<table class="grid"><tr>'
            '<td class="gh" width="10%">C No.</td>'
            '<td class="gh gh-l" width="42%">Targeted NCF competencies</td>'
            '<td class="gh gh-l">Justification</td></tr>'
            f'{rows}</table>'
        )
    rows = "".join(
        f'<tr><td class="ccode" width="12%">{_esc(c["c_code"])}</td>'
        f'<td class="gv gv-l">{_esc(c["text"])}</td></tr>'
        for c in comps
    )
    return (
        '<table class="grid"><tr>'
        '<td class="gh" width="12%">C No.</td>'
        '<td class="gh gh-l">Targeted NCF competencies</td></tr>'
        f'{rows}</table>'
    )


def english_competency_spines(spine_to_cg: Dict[str, Any],
                              descriptions: Dict[str, str]) -> List[Dict[str, Any]]:
    """English's STANDARDIZED spine competency map as [{spine, section, rows:[{c_code,text}]}].
    English carries the SAME competencies in every chapter, so instead of a per-chapter targeted
    list it presents the fixed spine → section → competency table from
    framework/english/{stage}/spine_to_cg.json (order preserved: Oracy, Reading, Writing, …)."""
    out: List[Dict[str, Any]] = []
    for sp in (spine_to_cg or {}).get("spines", {}).values():
        rows = [{"c_code": c, "text": descriptions.get(c, "")} for c in sp.get("competency_codes", []) or []]
        if not rows:
            continue
        out.append({
            "spine": sp.get("label", ""),
            "section": ", ".join(sp.get("textbook_section_names", []) or []),
            "rows": rows,
        })
    return out


def _english_competency_table(spines: List[Dict[str, Any]]) -> str:
    """English's 4-column competency table: Spine · Section Name · Code · Competency, with the
    Spine and Section cells spanning their competency rows."""
    if not spines:
        return ""
    body = ""
    for sp in spines:
        rws = sp.get("rows", [])
        n = len(rws)
        first, rest = rws[0], rws[1:]
        body += (
            '<tr>'
            f'<td class="gv gv-l ecg-sp" rowspan="{n}">{_esc(sp.get("spine"))}</td>'
            f'<td class="gv gv-l ecg-sec" rowspan="{n}">{_esc(sp.get("section"))}</td>'
            f'<td class="ccode" width="9%">{_esc(first.get("c_code"))}</td>'
            f'<td class="gv gv-l">{_esc(first.get("text"))}</td></tr>'
        )
        for r in rest:
            body += (
                f'<tr><td class="ccode">{_esc(r.get("c_code"))}</td>'
                f'<td class="gv gv-l">{_esc(r.get("text"))}</td></tr>'
            )
    return (
        '<table class="grid"><tr>'
        '<td class="gh" width="14%">Spine</td>'
        '<td class="gh" width="24%">Section Name</td>'
        '<td class="gh" width="9%">Code</td>'
        '<td class="gh gh-l">Competency</td></tr>'
        f'{body}</table>'
    )


def _stage_table(groups: List[Dict[str, Any]]) -> str:
    if not groups:
        return ""
    word = _group_word(groups)
    rows = ""
    for i, g in enumerate(groups, 1):
        rows += (
            f'<tr><td class="snum" width="12%">{i}</td>'
            f'<td class="gv gv-l">{_esc(g.get("label"))}</td></tr>'
        )
    # A full-width blurb naming what this axis is — verbatim from the Chapter
    # Organization page (AXIS_INFO), keyed by the top-level group type.
    blurb = AXIS_INFO.get(groups[0].get("type", ""))
    note_row = (
        f'<tr class="axis-note"><td colspan="2">{_esc(blurb)}</td></tr>' if blurb else ""
    )
    return (
        '<table class="grid"><tr>'
        f'<td class="gh" width="12%">{_esc(word)} No.</td>'
        f'<td class="gh gh-l">Progression {_esc(word)}</td></tr>'
        f'{rows}{note_row}</table>'
    )


def _stages_body(groups: List[Dict[str, Any]], subject: str = "") -> str:
    word = _group_word(groups)
    # Mathematics shows no section/stage band above its periods — the units render as one flat
    # run (founder 2026-07-20); every other subject keeps its organizing band.
    show_band = subject != "mathematics"
    out = ""
    seen = 0  # running period count across the whole chapter — first one carries the "Pedagogy:" label
    for i, g in enumerate(groups, 1):
        if show_band:
            out += (
                f'<table class="stage-band"><tr><td>'
                f'<span class="st-k">{_esc(word)} {i}</span><br/>'
                f'<span class="st">{_esc(g.get("label"))}</span>'
                f'</td></tr></table>'
            )
        for p in g.get("periods", []) or []:
            seen += 1
            out += _period_block(p, is_first=(seen == 1))
        # nested children (English section → spine): render child periods under the section
        for c in g.get("children", []) or []:
            for p in c.get("periods", []) or []:
                seen += 1
                out += _period_block(p, is_first=(seen == 1))
    return out


def _period_block(p: Dict[str, Any], *, is_first: bool = False) -> str:
    num = p.get("number")
    dur = (p.get("meta", {}) or {}).get("duration_minutes")
    dur_str = f"{dur} min" if dur else ""

    # Pedagogy rides at the right end of the period band. The first period spells the
    # label ("Pedagogy: …"); every later period shows just the value, since the field
    # is then understood.
    ped = p.get("approach") or ""
    if ped:
        inner = (f'<span class="pb-ped-k">Pedagogy:</span> {_esc(ped)}' if is_first else _esc(ped))
        ped_cell = f'<td width="26%" align="right"><span class="pb-ped">{inner}</span></td>'
    else:
        ped_cell = '<td width="26%"></td>'

    band = (
        '<table class="period-band"><tr>'
        f'<td width="15%"><span class="pb-n">Period {_esc(num)}</span></td>'
        f'<td width="10%"><span class="pb-dur">{_esc(dur_str)}</span></td>'
        f'<td><span class="pb-title">{_esc(p.get("title"))}</span></td>'
        f'{ped_cell}'
        '</tr></table>'
    )

    mats = p.get("materials") or []
    mat_line = (
        f'<div class="p-line"><span class="p-lbl">Materials:</span> {_esc(", ".join(mats))}</div>'
        if mats else ""
    )

    # Teacher notes — the colleague's margin note (view-model first-class field),
    # replacing the raw activity description.
    notes = p.get("teacher_notes") or []
    notes_line = (
        f'<div class="p-line"><span class="p-lbl">Teacher notes:</span> {_esc(" ".join(notes))}</div>'
        if notes else ""
    )

    phases = [ph for ph in (p.get("phases") or []) if ph.get("text") or ph.get("label")]
    if phases:
        prows = "".join(
            f'<tr><td class="ph-band">{_esc(_phase_duration(ph))}</td>'
            f'<td class="ph-text">{_esc(ph.get("text"))}</td></tr>'
            for ph in phases
        )
        phase_tbl = f'<table class="phase-tbl">{prows}</table>'
    elif p.get("activities"):
        prows = "".join(f'<tr><td class="ph-text">{_esc(a)}</td></tr>' for a in p["activities"])
        phase_tbl = f'<table class="phase-tbl">{prows}</table>'
    else:
        phase_tbl = ""

    hw = p.get("homework")
    homework = (
        f'<div class="u-hw"><span class="u-hw-k">Homework:</span> '
        f'<span class="u-hw-t">{_bold_marks(hw)}</span></div>'
        if hw else ""
    )

    return band + mat_line + notes_line + phase_tbl + homework


def export_lesson_plan_pdf(
    view: Dict[str, Any],
    *,
    competencies: Optional[List[Dict[str, str]]] = None,
    competency_spines: Optional[List[Dict[str, Any]]] = None,
    activity_desc_by_period: Optional[Dict[int, str]] = None,
    plan_date: Optional[datetime] = None,
    generated_at: Optional[datetime] = None,
) -> bytes:
    """Render the whole-chapter lesson plan to PDF bytes via xhtml2pdf (pure-Python,
    no system libs)."""
    from io import BytesIO
    from xhtml2pdf import pisa

    html_str = render_lesson_pdf_html(
        view, competencies=competencies, competency_spines=competency_spines,
        activity_desc_by_period=activity_desc_by_period,
        plan_date=plan_date, generated_at=generated_at,
    )
    buf = BytesIO()
    result = pisa.CreatePDF(html_str, dest=buf, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"xhtml2pdf failed with {result.err} error(s)")
    return buf.getvalue()
