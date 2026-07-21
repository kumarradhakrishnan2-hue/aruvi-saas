"""
Chapter Assessment Report — HTML template + PDF export.

Sibling of ``export_lesson_pdf.py`` / ``export_allocation_pdf.py``, same proven
pure-Python xhtml2pdf pattern (no system libs).

Two things distinguish it from the lesson-plan PDF, by founder direction:

  1. COLOUR — the assessment lives in a GREEN world, taken from the on-screen
     assessment surface (LessonView Screen 3b): bands ``#dceae3`` / ``#e7f0ec``,
     accents deep green ``#0f6e56``, titles ``#0c3a2e``, the LO box ``#eef6f1``
     with a green left rule. The masthead stays the allocation-report surface
     (pine "Aruvi. LESSON STUDIO"), so the export still reads as a sibling — only
     the body switches colour to signal "assessment, not lesson".

  2. ANSWERS are a LAYER, not a default. ``include_answers=False`` (the default)
     renders the class-facing question paper — stem, stimulus, plain options, and
     a green LO / cognitive-demand box, but NO answers — so the sheet can be handed
     out unedited. ``include_answers=True`` adds a distinct green ANSWER box per
     item mirroring the online Answer tab (correct option ✓, model answer / key,
     what each choice reveals, expected elements, look-fors, method, and the Maths
     textbook-exercise companion). Because the answers are a separate rendered
     block, an un-ticked copy can never carry them.

Unlike the lesson plan, the LO **is** shown here — assessment is its home.

Input is the ``view`` dict's ``assessment`` block (ViewModel.to_dict()); the
renderer reads only ``view["assessment"]``.
"""

from __future__ import annotations

import html as _html
from datetime import datetime
from typing import Any, Dict, List, Optional

from .report_competency import grade_roman, subject_display
from .pdf_fonts import font_face_css
from .grades import stage_for


# ── palette (green assessment world) ────────────────────────────────────────
PINE = "#164436"          # brand masthead
G_ACCENT = "#0f6e56"      # kickers, codes, ticks
G_DARK = "#0c3a2e"        # titles
G_BAND = "#c4ddd0"        # stage / spine band — the DARKEST green (like the LP kraft stage band)
G_HEAD = "#dceae3"        # table header + question (LO) header — a shade lighter than the band
G_TINT = "#eef6f1"        # answer section — the lightest green
G_ANS = "#e3efe9"         # (legacy)
G_EDGE = "#cde0d8"        # green hairlines
INK = "#1a1917"
GREY_LINE = "#dddddd"

CTX_WORD = {
    "progression_stage": "Stage", "stage": "Stage", "section": "Section",
    "competency": "Competency", "spine": "Spine", "unit": "Unit",
    "question_type": "Question type",
}

# Full, teacher-facing names for the internal question-type codes. Social Sciences and TWAU
# assessments group by question type (AssessmentGroup type="question_type", label=<raw code>);
# the report must never surface the raw acronym (founder 2026-07-20). Names verified against the
# subject assessment constitutions (e.g. "SCR — Short Constructed Response").
QUESTION_TYPE_NAMES = {
    "MCQ": "Multiple Choice Question",
    "SCR": "Short Constructed Response",
    "ECR": "Extended Constructed Response",
    "NUM": "Numerical Answer",
    "OPEN_TASK": "Open Task",
    "ORAL_PROMPT": "Oral Prompt",
    "FILL_IN": "Fill in the Blanks",
    "WRITING_TASK": "Writing Task",
    "MATCH": "Matching",
    "TRUE_FALSE": "True or False",
    "PROJECT": "Project",
    "SOURCE_INTERPRETATION": "Source Interpretation",
    "EXTRACT_ANALYSIS": "Extract Analysis",
    "ITEM": "Question",
}


def question_type_full(code: Any) -> str:
    """Full, teacher-facing name for an internal question-type code
    ("MCQ" → "Multiple Choice Question"). Unknown/future codes fall back to a
    title-cased, de-underscored form so a raw token never reaches the page."""
    key = str(code or "").strip()
    if not key:
        return "Question"
    return QUESTION_TYPE_NAMES.get(key.upper(), key.replace("_", " ").title())


# ── intro paragraph (common across subjects; one word adapts + two riders) ───

def _axis_word(groups: List[Dict[str, Any]]) -> str:
    gt = groups[0].get("type") if groups else ""
    return CTX_WORD.get(gt, "stage")


_RIDER = {
    # Maths carries no learning outcomes at any stage, and its textbook-exercise
    # companion is disclosed only in the answer section (present only when answers
    # are included) — so the companion clause is worded to say so.
    "mathematics": " For each item, a companion in the answer section points to a parallel textbook exercise; the textbook's own key remains the canonical solution.",
    "english": " Each item is written from the section's own text, not from the textbook exercises.",
}


def intro_paragraph(subject_slug: str, groups: List[Dict[str, Any]],
                    grade: Any = None) -> str:
    axis = _axis_word(groups).lower()
    plural = {"stage": "stages", "section": "sections", "competency": "competencies",
              "spine": "spines", "unit": "units"}.get(axis, axis + "s")
    # Mathematics has NO learning outcomes at prep/middle, and those stages carry no
    # cognitive demand either — so the LO+cognitive-demand copy is stripped there. Only
    # SECONDARY maths (which carries LO + cognitive demand on its items) keeps the original
    # copy, the same as every other subject. Stage is authoritative when the grade is
    # known; the item-level cognitive-demand presence is a fallback for callers that don't
    # thread a grade through.
    maths_no_meta = False
    if subject_slug == "mathematics":
        stage = ""
        if grade not in (None, ""):
            try:
                stage = stage_for(grade)
            except Exception:
                stage = ""
        if stage:
            maths_no_meta = stage != "secondary"
        else:
            has_cog = any(
                (it.get("normalized") or {}).get("cognitive_demand")
                for g in groups for it in (g.get("items") or [])
            )
            maths_no_meta = not has_cog
    if maths_no_meta:
        base = (
            "This assessment is formative. Every question traces to a specific NCF "
            "competency this chapter develops. Rather than testing recall or asking "
            "whether a student “understood” a topic, each item asks for an observable "
            "demonstration — a response, a classification, a justification, or a "
            "product — of the thinking the lessons built. The questions are grouped by "
            f"{plural}, so you can see how the assessment maps onto what the chapter "
            "develops."
        )
    else:
        base = (
            "This assessment is formative. Every question traces to a specific learning "
            "outcome, and each outcome is derived from an NCF competency this chapter "
            "develops. Rather than testing recall or asking whether a student "
            "“understood” a topic, each item asks for an observable demonstration "
            "— a response, a classification, a justification, or a product — of the "
            f"thinking the lessons built. The questions are grouped by {plural}, and each "
            "shows the learning outcome it assesses and its cognitive demand, so you can see "
            "exactly what each question checks and why."
        )
    return base + _RIDER.get(subject_slug, "")


# ── formatting helpers ──────────────────────────────────────────────────────

def _esc(s: Any) -> str:
    return _html.escape(str(s if s is not None else ""))


def _date_spaces(dt: datetime) -> str:
    return f"{dt.day} {dt.strftime('%B')} {dt.year}"


def _count_items(groups: List[Dict[str, Any]]) -> int:
    return sum(len(g.get("items", []) or []) for g in groups)


# ── typed stimulus / passage (svg / table / number_line / prose) ────────────

def _stimulus_html(block: Optional[Dict[str, Any]]) -> str:
    """Render a typed stimulus/passage block. Table + prose render fully; SVG and
    number-line (which xhtml2pdf can't rasterize) fall back to their instruction/
    content text so nothing is silently dropped."""
    if not block:
        return ""
    btype = block.get("type")
    if btype == "table" and block.get("table"):
        t = block["table"]
        header = t.get("header", []) or []
        rows = t.get("rows", []) or []
        # Explicit, even column widths + fixed layout: without them xhtml2pdf sizes columns
        # by content and starves the trailing columns — a 7-column science data table was
        # collapsing its last three columns into unreadable single-letter stacks off the
        # right margin. Even widths guarantee every column is visible and wraps.
        ncols = max([len(header)] + [len(r) for r in rows]) if (header or rows) else 0
        colw = f"{100.0 / ncols:.4f}%" if ncols else ""
        wide = ncols >= 5  # shrink type/padding on many-column tables so cells still wrap cleanly
        tcls = "stim-tbl stim-tbl-wide" if wide else "stim-tbl"

        def _row(cells: List[Any], cls: str) -> str:
            return "<tr>" + "".join(
                f'<td class="{cls}" width="{colw}">{_esc(c)}</td>' for c in cells
            ) + "</tr>"

        head = _row(header, "st-th") if header else ""
        body = "".join(_row(r, "st-td") for r in rows)
        return f'<table class="{tcls}">{head}{body}</table>'
    if btype == "number_line" and block.get("number_line"):
        nl = block["number_line"]
        labels = " · ".join(str(t.get("label", "")) for t in nl.get("ticks", []) if t.get("label"))
        instr = nl.get("instruction", "")
        return f'<div class="stim-prose">{_esc(instr)}{(" (" + _esc(labels) + ")") if labels else ""}</div>'
    content = block.get("content")
    if content and btype != "svg":
        return f'<div class="stim-prose">{_esc(content)}</div>'
    if btype == "svg":
        return '<div class="stim-note">[figure — see the on-screen version]</div>'
    return ""


def _ticks(label: str, items: List[str]) -> str:
    if not items:
        return ""
    lis = "".join(f"<li>{_esc(x)}</li>" for x in items)
    return f'<div class="ans-sub"><span class="ans-k">{_esc(label)}</span><ul class="ans-ul">{lis}</ul></div>'


def _block(label: str, text: Any) -> str:
    if not text:
        return ""
    return f'<div class="ans-sub"><span class="ans-k">{_esc(label)}</span> <span class="ans-t">{_esc(text)}</span></div>'


# ── PDF rendering ───────────────────────────────────────────────────────────

def render_assessment_pdf_html(
    view: Dict[str, Any],
    *,
    include_answers: bool = False,
    assessment_type: str = "Formative",
    plan_date: Optional[datetime] = None,
    generated_at: Optional[datetime] = None,
) -> str:
    av = view.get("assessment", {}) or {}
    groups = av.get("groups", []) or []
    subject_slug = av.get("subject", "")
    subject = subject_display(subject_slug)
    grade = grade_roman(av.get("grade", ""))
    ch_no = av.get("chapter_number", "")
    ch_title = av.get("chapter_title", "")
    masthead_dt = generated_at or plan_date or datetime.now()

    total_q = _count_items(groups)
    meta_table = (
        '<table class="grid"><tr>'
        '<td class="gh" width="13%">Chapter</td>'
        '<td class="gh" width="52%">Title</td>'
        '<td class="gh" width="18%">Total questions</td>'
        '<td class="gh" width="17%">Type</td></tr>'
        f'<tr><td class="gv">Ch {_esc(ch_no)}</td>'
        f'<td class="gv gv-title">{_esc(ch_title)}</td>'
        f'<td class="gv">{total_q}</td>'
        f'<td class="gv">{_esc(assessment_type)}</td></tr></table>'
    )

    intro = f'<p class="intro">{_esc(intro_paragraph(subject_slug, groups, av.get("grade")))}</p>'
    body = _groups_body(groups, include_answers)
    ans_flag = ' · With answers' if include_answers else ''

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
  .rep-title {{ font-family: Georgia, serif; font-size: 11pt; font-weight: bold; color: {G_ACCENT}; }}
  .rep-sub {{ font-size: 7pt; color: #555; }}
  .rule-tbl {{ width: 100%; margin-top: 10px; margin-bottom: 12px; }}
  .rule-tbl td {{ border-bottom: 2px solid {INK}; font-size: 1pt; line-height: 1pt; }}

  table.grid {{ width: 100%; margin-bottom: 12px; }}
  table.grid td {{ border: 0.75px solid {GREY_LINE}; padding: 5px 8px; vertical-align: top; }}
  .gh {{ background-color: {G_HEAD}; font-size: 6.5pt; letter-spacing: 0.5px; color: {G_DARK};
        text-transform: uppercase; text-align: center; font-weight: bold; }}
  .gv {{ font-size: 8pt; color: #2a2a2a; text-align: center; }}
  .gv-title {{ font-family: Georgia, serif; font-weight: bold; color: {INK}; }}

  .intro {{ font-size: 8pt; color: #2a2a2a; line-height: 1.5; margin-bottom: 6px; }}

  .stage-band {{ width: 100%; margin-top: 14px; margin-bottom: 8px; }}
  .stage-band td {{ background-color: {G_BAND}; padding: 8px 12px; text-align: left; }}
  .stage-band .st-k {{ font-family: Helvetica; font-size: 6.5pt; font-weight: bold; letter-spacing: 1px;
                       text-transform: uppercase; color: {G_ACCENT}; }}
  .stage-band .st {{ font-family: Helvetica; font-size: 9.5pt; font-weight: bold; color: {G_DARK}; }}

  .q {{ margin-top: 10px; }}
  .q-stem {{ font-size: 8pt; color: {INK}; line-height: 1.45; }}
  .q-n {{ font-weight: bold; color: {INK}; }}
  .opts {{ width: 100%; margin-top: 5px; }}
  .opt-lab {{ width: 22px; font-weight: bold; color: #444; font-size: 7.5pt; vertical-align: top; padding: 2px 0; }}
  .opt-txt {{ font-size: 7.5pt; color: #2a2a2a; padding: 2px 0; vertical-align: top; }}
  .opt-correct .opt-lab, .opt-correct .opt-txt {{ color: {G_ACCENT}; font-weight: bold; }}

  .stim-tbl {{ width: 100%; margin: 6px 0; table-layout: fixed; }}
  .st-th {{ background-color: {G_HEAD}; font-size: 7pt; font-weight: bold; color: {G_DARK};
            border: 0.5px solid {G_EDGE}; padding: 4px 6px; word-wrap: break-word; }}
  .st-td {{ font-size: 7pt; color: #2a2a2a; border: 0.5px solid {G_EDGE}; padding: 4px 6px; word-wrap: break-word; }}
  .stim-tbl-wide .st-th, .stim-tbl-wide .st-td {{ font-size: 6pt; padding: 3px 4px; }}
  .stim-prose {{ font-size: 7.5pt; color: #2a2a2a; font-style: italic; margin: 5px 0; }}
  .stim-note {{ font-size: 7pt; color: #8a8a86; font-style: italic; margin: 5px 0; }}
  .scaf {{ font-size: 7.5pt; color: #2a2a2a; margin: 4px 0 2px; }}
  .task-k {{ font-size: 6.5pt; font-weight: bold; letter-spacing: 0.5px; text-transform: uppercase; color: {G_ACCENT}; }}
  .task-ul {{ margin: 2px 0 0 14px; padding: 0; }}
  .task-ul li {{ font-size: 7.5pt; color: #2a2a2a; margin-bottom: 1px; }}

  .qmeta {{ width: 100%; margin-top: 13px; margin-bottom: 6px; }}
  .qmeta td {{ background-color: {G_HEAD}; vertical-align: top; }}
  .qm-top {{ padding: 5px 10px 1px 10px; }}
  .qm-bot {{ padding: 1px 10px 5px 10px; }}
  .qm-l {{ text-align: left; }}
  .qm-rk {{ text-align: right; white-space: nowrap; border-left: 0.75px solid {G_EDGE}; }}
  .qm-rv {{ text-align: right; white-space: nowrap; border-left: 0.75px solid {G_EDGE};
            font-size: 7.5pt; color: #1f3a30; }}
  .qm-qn {{ font-family: Georgia, serif; font-size: 9pt; font-weight: bold; color: {G_DARK}; }}
  .qm-k {{ font-size: 6.5pt; font-weight: bold; letter-spacing: 0.5px; text-transform: uppercase; color: {G_ACCENT}; }}
  .qm-v {{ font-size: 7.5pt; color: #1f3a30; line-height: 1.35; }}

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

  .footer {{ font-size: 6pt; color: #999; }}
</style></head><body>

  <table class="hdr" width="100%"><tr>
    <td width="60%">
      <span class="brand-aruvi">Aruvi</span><span class="brand-dot">.</span>
      <span class="brand-studio">LESSON STUDIO</span><br/>
      <span class="brand-ncf">NCF 2023 aligned</span>
    </td>
    <td width="40%" align="right">
      <span class="rep-title">Chapter Assessment</span><br/>
      <span class="rep-sub">Grade {_esc(grade)} · {_esc(subject)} · {_esc(_date_spaces(masthead_dt))}</span>
    </td>
  </tr></table>
  <table class="rule-tbl"><tr><td></td></tr></table>

  {meta_table}
  {intro}
  {body}

  <div id="footerContent" class="footer">
    Aruvi · Assessment · Grade {_esc(grade)} · {_esc(subject)} · Ch {_esc(ch_no)}{ans_flag} · Confidential
  </div>
</body></html>"""


def _groups_body(groups: List[Dict[str, Any]], include_answers: bool) -> str:
    out = ""
    qn = 0
    for i, g in enumerate(groups, 1):
        gtype = g.get("type", "")
        if gtype == "question_type":
            # SS / TWAU group by question type — the band carries a "QUESTION TYPE" kicker (no
            # number: question types aren't a numbered progression) over the FULL type name, not
            # the raw "STAGE n / MCQ" the generic path produced (founder 2026-07-20).
            kicker = "Question type"
            title = question_type_full(g.get("label"))
        else:
            word = CTX_WORD.get(gtype, "Stage")
            snum = (g.get("meta", {}) or {}).get("stage_number", i)
            kicker = f"{word} {snum}"
            title = g.get("label")
        out += (
            f'<table class="stage-band"><tr><td>'
            f'<span class="st-k">{_esc(kicker.upper())}</span><br/>'
            f'<span class="st">{_esc(title)}</span>'
            f'</td></tr></table>'
        )
        for it in g.get("items", []) or []:
            qn += 1
            out += _question_block(it, qn, include_answers, is_first=(qn == 1))
    return out


def _question_block(it: Dict[str, Any], qn: int, include_answers: bool, is_first: bool = False) -> str:
    n = it.get("normalized") or {}
    stem = n.get("stem") or it.get("prompt") or ""
    template = n.get("template") or ""

    parts = []

    # Question header — a green-filled block that IS the question's own header: the
    # number is stamped into it ("Q1 · Learning Outcome · Cognitive Demand") so the LO
    # unmistakably belongs to THIS question rather than heading a group. The stem below
    # then drops the redundant number. Items with no LO/demand (e.g. Maths) keep the
    # number on the stem instead.
    lo = n.get("linked_lo") or it.get("implied_lo") or ""
    cog = n.get("cognitive_demand")
    template = n.get("template") or ""
    tf = n.get("tf_statements") or []
    is_tf = template == "true_false" and bool(tf)
    stem_parts = n.get("stem_parts") or []
    stem_lead = n.get("stem_lead") or ""

    # Question header — green box: "Q1 · Learning Outcome" with Cognitive Demand on the top-right,
    # and the LO text spanning the FULL width below (not a narrow column).
    if cog:
        # Two-column meta as a 2×2 grid: the LABELS sit on the top row
        # ("Q1 · Learning Outcome" | "Cognitive Demand") and their VALUES align on the
        # row directly below (LO text | demand). LO keeps ~3/4 of the width; the demand
        # column is set off at the far right by a hairline so it reads as its own field.
        head = (
            '<table class="qmeta">'
            '<tr>'
            f'<td class="qm-l qm-k qm-top" width="76%"><span class="qm-qn">Q{qn}</span>'
            f'{" · Learning Outcome" if lo else ""}</td>'
            f'<td class="qm-rk qm-k qm-top" width="24%">Cognitive Demand</td>'
            '</tr><tr>'
            f'<td class="qm-l qm-v qm-bot" width="76%">{_esc(lo)}</td>'
            f'<td class="qm-rv qm-bot" width="24%">{_esc(cog)}</td>'
            '</tr></table>'
        )
        parts.append(head)
        q_prefix = ""
    elif lo:
        head = (
            '<table class="qmeta">'
            f'<tr><td class="qm-l qm-k qm-top"><span class="qm-qn">Q{qn}</span>'
            ' · Learning Outcome</td></tr>'
            f'<tr><td class="qm-l qm-v qm-bot">{_esc(lo)}</td></tr>'
            '</table>'
        )
        parts.append(head)
        q_prefix = ""
    else:
        q_prefix = f'<span class="q-n">Q{qn}.</span> '

    # EXTRACT_ANALYSIS: the extract is set off BEFORE the multi-part stem.
    if template == "passage":
        parts.append(_stimulus_html(n.get("passage")))

    # Question body — match the on-screen precedence so redundant statements/parts never repeat:
    #   TRUE_FALSE → instruction (stem_lead) + statements ONCE (from tf_statements), NEVER options.
    #   a stem with a parsed numbered/lettered list → intro + parts once.
    #   otherwise → the plain stem.
    if is_tf:
        parts.append(f'<div class="q-stem">{q_prefix}{_esc(stem_lead or stem)}</div>')
        parts.append(_parts_rows([{"marker": s.get("marker"), "text": s.get("text")} for s in tf]))
    elif stem_parts:
        if stem_lead:
            parts.append(f'<div class="q-stem">{q_prefix}{_esc(stem_lead)}</div>')
        elif q_prefix:
            parts.append(f'<div class="q-stem">{q_prefix}</div>')
        parts.append(_parts_rows(stem_parts))
    else:
        parts.append(f'<div class="q-stem">{q_prefix}{_esc(stem)}</div>')

    # visual stimulus (the passage template already showed its extract above)
    if template != "passage":
        parts.append(_stimulus_html(n.get("visual_stimulus")))
    if it.get("visual_stimulus") and not (n.get("visual_stimulus") or n.get("passage")):
        vs = it["visual_stimulus"]
        if isinstance(vs, dict):
            parts.append(_stimulus_html(vs))

    # options (plain; correct marked ✓ in answer mode). TRUE_FALSE never shows options — the
    # statements above ARE the options; showing both would repeat every line.
    opts = n.get("options") or []
    if opts and not is_tf:
        rows = ""
        for o in opts:
            correct = include_answers and o.get("is_correct")
            tick = " ✓" if correct else ""
            cls = " opt-correct" if correct else ""
            rows += (
                f'<tr class="{cls.strip()}"><td class="opt-lab">{_esc(o.get("label"))}.</td>'
                f'<td class="opt-txt">{_esc(o.get("text"))}{tick}</td></tr>'
            )
        parts.append(f'<table class="opts">{rows}</table>')

    # student-facing task framing (belongs on the question paper, mirrors the on-screen
    # question tab order): WHAT TO PRODUCE (format_of_output) → SCAFFOLD. The open-task
    # "Reading this task" guide is teacher framing and lives in the answer layer instead.
    wtp = n.get("format_of_output") or []
    if wtp:
        lis = "".join(f"<li>{_esc(x)}</li>" for x in wtp if x)
        parts.append(
            '<div class="scaf"><span class="task-k">What to produce</span>'
            f'<ul class="task-ul">{lis}</ul></div>'
        )
    scaf_lines = n.get("scaffold_lines") or []
    if scaf_lines:
        body = "<br/>".join(_esc(x) for x in scaf_lines if x)
        parts.append(f'<div class="scaf"><span class="task-k">Scaffold</span><br/>{body}</div>')
    elif n.get("scaffold"):
        parts.append(
            '<div class="scaf"><span class="task-k">Scaffold</span><br/>'
            f'{_esc(n.get("scaffold"))}</div>'
        )

    # ANSWER layer
    if include_answers:
        parts.append(_answer_block(n, opts))

    parts.append('<table class="q-rule"><tr><td></td></tr></table>')
    return '<div class="q">' + "".join(p for p in parts if p) + '</div>'


def _parts_rows(rows: List[Dict[str, Any]]) -> str:
    """A marker + text list (numbered/lettered parts, or TRUE_FALSE statements) — same layout
    as the option rows so the two read consistently."""
    r = "".join(
        f'<tr><td class="opt-lab">{_esc(p.get("marker"))}</td>'
        f'<td class="opt-txt">{_esc(p.get("text"))}</td></tr>' for p in rows
    )
    return f'<table class="opts">{r}</table>' if r else ""


def _reading_this_task(n: Dict[str, Any]) -> str:
    """OPEN_TASK teacher framing — mirrors the on-screen 'Reading this task' panel
    (Format · What this demonstrates · Reading the scaffold, plus the TWAU performance-task
    riders when present). Teacher-facing, so it rides in the answer layer, not the handout."""
    g = n.get("open_task_guide") or {}
    if not g:
        return ""
    fmt = " — ".join(str(x) for x in (g.get("format_type"), g.get("format_rationale")) if x)
    rows = ""
    rows += _block("Format:", fmt)
    rows += _block("What this demonstrates:", g.get("what_this_demonstrates"))
    rows += _block("Reading the scaffold:", g.get("reading_the_scaffold"))
    rows += _block("Strong vs weak markers:", g.get("strong_vs_weak_markers"))
    rows += _block("Observation rubric:", g.get("observation_rubric"))
    if not rows:
        return ""
    return f'<div class="ans-sub"><span class="ans-k">Reading this task</span></div>{rows}'


def _answer_block(n: Dict[str, Any], opts: List[Dict[str, Any]]) -> str:
    inner = ""
    # TRUE_FALSE: one verdict (+ reason) per statement — this REPLACES the "Correct answer"
    # list and the options entirely (mirrors the on-screen Answer tab).
    tf = n.get("tf_statements") or []
    if (n.get("template") == "true_false") and tf:
        has_reasons = any(s.get("reason") for s in tf)
        if not has_reasons and n.get("model_answer"):
            inner += _block("Suggested answer:", n.get("model_answer"))
        else:
            rows = ""
            for s in tf:
                verdict = "True" if s.get("verdict") else "False"
                reason = f" — {_esc(s.get('reason'))}" if s.get("reason") else ""
                rows += (f'<tr class="rev-row"><td class="rev-lab">{_esc(s.get("marker"))}</td>'
                         f'<td><b>{verdict}</b>{reason}</td></tr>')
            inner += f'<div class="ans-sub"><span class="ans-k">Answer key</span><table>{rows}</table></div>'
        return f'<div class="ans"><div class="ans-title">Answer section</div>{inner}</div>' if inner else ""
    # correct option letter(s)
    correct = [o.get("label") for o in opts if o.get("is_correct")]
    if correct:
        inner += _block("Correct answer:", ", ".join(str(c) for c in correct))
    # model answer / key
    if n.get("answer_parts"):
        rows = "".join(
            f'<tr class="rev-row"><td class="rev-lab">{_esc(p.get("marker"))}</td>'
            f'<td>{_esc(p.get("text"))}</td></tr>' for p in n["answer_parts"]
        )
        lead = f'<span class="ans-t">{_esc(n.get("answer_lead"))}</span>' if n.get("answer_lead") else ""
        inner += f'<div class="ans-sub"><span class="ans-k">Answer key:</span> {lead}<table>{rows}</table></div>'
    elif n.get("model_answer"):
        inner += _block("Model answer:", n.get("model_answer"))
    # what each choice reveals
    reveals = n.get("option_reveals") or {}
    if reveals:
        rows = ""
        for lab, txt in reveals.items():
            if lab == "note":
                rows += f'<tr class="rev-row"><td colspan="2">{_esc(txt)}</td></tr>'
            else:
                rows += (f'<tr class="rev-row"><td class="rev-lab">{_esc(lab)}</td>'
                         f'<td>{_esc(txt)}</td></tr>')
        inner += f'<div class="ans-sub"><span class="ans-k">What each choice reveals</span><table>{rows}</table></div>'
    inner += _ticks("Expected elements", n.get("expected_elements") or [])
    inner += _ticks("Look for", n.get("look_fors") or [])
    inner += _block("Method:", n.get("method_one_line"))
    # OPEN_TASK "Reading this task" teacher framing (answer-layer only)
    inner += _reading_this_task(n)
    # Maths textbook-exercise companion
    if n.get("exercise_ref") or n.get("exercise_desc"):
        ref = n.get("exercise_ref") or ""
        desc = n.get("exercise_desc") or ""
        inner += _block("Textbook exercise:", f"{ref} — {desc}".strip(" —"))
    if not inner:
        return ""
    return f'<div class="ans"><div class="ans-title">Answer section</div>{inner}</div>'


def export_assessment_pdf(
    view: Dict[str, Any],
    *,
    include_answers: bool = False,
    assessment_type: str = "Formative",
    plan_date: Optional[datetime] = None,
    generated_at: Optional[datetime] = None,
) -> bytes:
    """Render the chapter assessment to PDF bytes via xhtml2pdf (pure-Python)."""
    from io import BytesIO
    from xhtml2pdf import pisa

    html_str = render_assessment_pdf_html(
        view, include_answers=include_answers, assessment_type=assessment_type,
        plan_date=plan_date, generated_at=generated_at,
    )
    buf = BytesIO()
    result = pisa.CreatePDF(html_str, dest=buf, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"xhtml2pdf failed with {result.err} error(s)")
    return buf.getvalue()
