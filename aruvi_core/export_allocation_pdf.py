"""
Period Allocation Report — HTML template + PDF export.

The layout is ported from the prototype's report (knowledge_commons/pdf_generator.py).
There are two renderers: render_report_html() (flexbox, for the on-screen / mobile
web preview) and render_pdf_html() + export_allocation_report_pdf() which use
xhtml2pdf — pure-Python (reportlab + html5lib) with NO system-library dependency,
so the PDF generates identically on a teacher's Mac/Windows and on a cloud server
with nothing to install at the OS level.

Per product direction: NO per-chapter effort-index line and NO "About the Effort
Index" section. Each chapter shows its allocation pill and a competency table
(# / Code / Competency / Justification). Competency-weight subjects also show a
weight indicator.
"""

from __future__ import annotations

import html as _html
from typing import List

from .report_competency import (
    CompetencyAllocationReport, ChapterReport,
    grade_roman, subject_display, date_long, executive_summary_paragraphs,
)


# ── HTML template ──────────────────────────────────────────────────────────

def render_report_html(report: CompetencyAllocationReport, *, for_pdf: bool = True) -> str:
    """Build the full report HTML. `for_pdf=True` includes @page/print rules and
    the fixed footer; the web preview passes for_pdf=False."""
    esc = lambda s: _html.escape(str(s or ""))

    g = grade_roman(report.grade)
    subj = subject_display(report.subject)
    today = date_long(report.generated_at)

    types = report.sorted_types
    total_periods = report.total_periods
    total_mins = report.total_minutes
    total_hrs, rem = divmod(total_mins, 60)
    time_str = f"{total_hrs}h {rem}min" if rem else f"{total_hrs}h"
    period_type_str = " · ".join(f"{t.count}×{t.minutes}min" for t in types) or "—"

    # ── stat strip ──
    summary_cells = [
        (len(report.chapters), "Chapters"),
        (total_periods, "Periods"),
        (time_str, "Total time"),
        (period_type_str, "Period types"),
    ]
    summary_html = "".join(
        f'<div class="sum-cell"><span class="sum-val">{esc(v)}</span>'
        f'<span class="sum-key">{esc(k)}</span></div>'
        for v, k in summary_cells
    )

    # ── executive summary ──
    intro = executive_summary_intro(report)
    exec_html = f"""
    <div class="exec">
      <div class="exec-title">Executive Summary</div>
      <p>This report presents the allocation of available instructional periods across the
         selected chapters for {esc(subj)}, Grade {esc(g)}.</p>
      <p>{esc(intro)}</p>
      <p>The allocation shown below distributes the available periods across the chapters using
         the approach described above. For each chapter, the competency section lists the
         competencies the chapter addresses, together with the rationale for including each one.</p>
      <p>This information is intended to support teacher planning, curriculum alignment, and
         instructional decision-making.</p>
    </div>"""

    # ── chapter blocks ──
    blocks = "".join(_chapter_block(ch, types, report.is_effort, esc) for ch in report.chapters)

    page_css = """
  @page {
    size: A4; margin: 18mm 14mm 16mm 14mm;
    @bottom-left { content: "Aruvi · Period Allocation Report"; font-size: 6pt; color: #bbb; }
    @bottom-right { content: "Page " counter(page) " of " counter(pages) " · Confidential"; font-size: 6pt; color: #bbb; }
  }
""" if for_pdf else ""

    footer_html = ""  # PDF footer comes from @page; web preview needs none

    return f"""<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8"><style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: 'Helvetica Neue', Arial, sans-serif; font-size: 8pt; color: #1a1917; background: #fff; line-height: 1.5; }}
  {page_css}

  .page-header {{ display: flex; justify-content: space-between; align-items: flex-end; padding-bottom: 6px; border-bottom: 2px solid #1a1917; }}
  .brand-name {{ font-size: 13pt; font-weight: 700; font-family: Georgia, serif; color: #1a1917; letter-spacing: .04em; }}
  .brand-sub {{ font-size: 6pt; color: #999; display: block; margin-top: 1px; letter-spacing:.04em; }}
  .report-right {{ text-align: right; }}
  .report-title {{ font-size: 9.5pt; font-weight: 700; }}
  .report-sub {{ font-size: 6.5pt; color: #777; margin-top: 2px; }}
  .header-rule2 {{ border: none; border-top: 0.5px solid #1a1917; margin: 3px 0 12px 0; }}

  .summary {{ display: flex; margin-bottom: 14px; border: 0.5px solid #ddd; }}
  .sum-cell {{ flex: 1; padding: 6px 8px; border-right: 0.5px solid #ddd; text-align: center; }}
  .sum-cell:last-child {{ border-right: none; }}
  .sum-val {{ font-size: 10pt; font-weight: 700; display: block; }}
  .sum-key {{ font-size: 5.5pt; color: #999; text-transform: uppercase; letter-spacing: .06em; margin-top: 2px; display: block; }}

  .exec {{ margin-bottom: 16px; }}
  .exec-title {{ font-size: 9pt; font-weight: 700; text-transform: uppercase; letter-spacing: .08em; color:#1a1917; padding-bottom: 4px; border-bottom: 1px solid #1a1917; margin-bottom: 6px; }}
  .exec p {{ font-size: 7.5pt; color: #333; margin-bottom: 5px; line-height: 1.55; }}

  .section-label {{ font-size: 9pt; font-weight: 700; text-transform: uppercase; letter-spacing:.08em; margin-bottom: 8px; }}

  .chapter-block {{ margin-bottom: 14px; page-break-inside: avoid; break-inside: avoid; }}
  .chapter-header {{ display: flex; align-items: baseline; gap: 6px; flex-wrap: wrap; padding-bottom: 3px; border-bottom: 1.5px solid #1a1917; }}
  .ch-num {{ font-size: 6.5pt; color: #aaa; font-weight: 500; white-space: nowrap; }}
  .ch-title {{ font-size: 8.5pt; font-weight: 700; font-family: Georgia, serif; flex: 1; min-width: 0; word-break: break-word; }}
  .ch-alloc {{ font-size: 6.5pt; font-weight: 600; color: #fff; background: #1a1917; padding: 2px 6px; border-radius: 3px; white-space: nowrap; }}
  .ch-weight {{ font-size: 6.5pt; color: #aaa; white-space: nowrap; padding-left: 6px; }}

  .comp-table {{ width: 100%; border-collapse: collapse; margin-top: 2px; }}
  .comp-table th {{ font-size: 6pt; font-weight: 600; letter-spacing:.05em; text-transform: uppercase; color: #bbb; padding: 4px 6px; text-align: left; border-bottom: 0.5px solid #e0ddd8; }}
  .th-seq {{ width: 16px; text-align: right; }}
  .th-code {{ width: 42px; }}
  .th-comp {{ width: 30%; }}
  .th-wt {{ width: 44px; text-align: center; }}
  .comp-table tr {{ break-inside: avoid; page-break-inside: avoid; }}
  .comp-table td {{ padding: 4px 6px; vertical-align: top; border-bottom: 0.5px solid #f0ede9; font-size: 7pt; line-height: 1.45; color: #2a2a2a; }}
  .comp-table tr:last-child td {{ border-bottom: none; }}
  .seq {{ color: #bbb; font-size: 6.5pt; text-align: right; }}
  .code {{ font-weight: 700; font-size: 7.5pt; white-space: nowrap; }}
  .wt {{ text-align: center; vertical-align: middle; }}
  .dots {{ display: flex; gap: 3px; justify-content: center; align-items: center; }}
  .dot {{ width: 5px; height: 5px; border-radius: 50%; display: inline-block; }}
  .dot.filled {{ background: #1a1917; }}
  .dot.empty {{ border: 1px solid #ccc; }}
  .nocomp {{ font-size: 7pt; color: #aaa; padding: 4px 0; }}

  .page-footer {{ display: flex; justify-content: space-between; font-size: 6pt; color: #bbb; border-top: 0.5px solid #eee; padding-top: 4px; }}
</style></head>
<body>
  <div class="page-header">
    <div>
      <span class="brand-name">ARUVI</span>
      <span class="brand-sub">NCF 2023 · Pedagogical Platform</span>
    </div>
    <div class="report-right">
      <div class="report-title">Period Allocation Report</div>
      <div class="report-sub">{esc(today)} · Grade {esc(g)} · {esc(subj)}</div>
    </div>
  </div>
  <hr class="header-rule2">

  <div class="summary">{summary_html}</div>

  {exec_html}

  <div class="section-label">Allocation &amp; Competency Detail</div>
  {blocks}
  {footer_html}
</body></html>"""


def _chapter_block(ch: ChapterReport, types, is_effort: bool, esc) -> str:
    period_cells = " · ".join(
        f'{ch.periods_by_duration.get(t.minutes, 0)}×{t.minutes}min' for t in types
    ) or "—"
    weight_chip = ""
    if not is_effort and ch.chapter_weight not in (None, ""):
        weight_chip = f'<span class="ch-weight">Weight {esc(ch.chapter_weight)}</span>'

    show_wt = (not is_effort) and any(c.weight is not None for c in ch.competencies)
    head = (
        '<tr><th class="th-seq">#</th><th class="th-code">Code</th>'
        '<th class="th-comp">Competency</th><th>Justification</th>'
        + ('<th class="th-wt">Weight</th>' if show_wt else '')
        + '</tr>'
    )
    rows = ""
    for i, c in enumerate(ch.competencies, 1):
        wt_cell = ""
        if show_wt:
            w = int(c.weight or 0)
            dots = "".join(
                f'<span class="dot {"filled" if d < w else "empty"}"></span>' for d in range(3)
            )
            wt_cell = f'<td class="wt"><div class="dots">{dots}</div></td>'
        rows += (
            f'<tr><td class="seq">{i}</td>'
            f'<td class="code">{esc(c.c_code)}</td>'
            f'<td>{esc(c.description)}</td>'
            f'<td>{esc(c.justification)}</td>'
            f'{wt_cell}</tr>'
        )
    table = (
        f'<table class="comp-table"><thead>{head}</thead><tbody>{rows}</tbody></table>'
        if rows else '<p class="nocomp">No competency entries for this chapter.</p>'
    )

    return (
        f'<div class="chapter-block">'
        f'<div class="chapter-header">'
        f'<span class="ch-num">Ch {str(ch.chapter_number).zfill(2)}</span>'
        f'<span class="ch-title">{esc(ch.chapter_title)}</span>'
        f'<span class="ch-alloc">{period_cells} · {ch.total_periods} periods · {ch.total_minutes}min</span>'
        f'{weight_chip}'
        f'</div>{table}</div>'
    )


# ── PDF rendering (xhtml2pdf) ──────────────────────────────────────────────
# xhtml2pdf is pure-Python (reportlab + html5lib) and needs NO system libraries —
# so the PDF generates identically on a teacher's Mac, on Windows, and on a cloud
# server, with nothing to `brew install`. Its CSS subset is narrower than a
# browser's (no flexbox, limited @page), so the PDF uses a dedicated table-based
# template below rather than the flexbox web template in render_report_html().

def render_pdf_html(report: CompetencyAllocationReport) -> str:
    """xhtml2pdf-friendly report (table layout, no flexbox). Three sections:
    Executive Summary · Allocation Details (periods table) · Competency Report."""
    esc = lambda s: _html.escape(str(s or ""))
    g = grade_roman(report.grade)
    subj = subject_display(report.subject)
    today = date_long(report.generated_at)

    types = report.sorted_types
    total_mins = report.total_minutes
    hrs, rem = divmod(total_mins, 60)
    time_str = f"{hrs}h {rem}min" if rem else f"{hrs}h"
    ptype = " · ".join(f"{t.count}×{t.minutes}min" for t in types) or "—"

    # ── (point 1) summary strip — mimic prototype: Chapters / Periods / Total time / Period types
    stats = [(len(report.chapters), "Chapters"), (report.total_periods, "Periods"),
             (time_str, "Total time"), (ptype, "Period types")]
    stat_cells = "".join(
        f'<td class="sum-cell" width="25%"><span class="sum-val">{esc(v)}</span><br/>'
        f'<span class="sum-key">{esc(k)}</span></td>' for v, k in stats
    )

    # ── (point 7) executive summary paragraphs
    exec_paras = "".join(f'<p class="exec">{esc(p)}</p>' for p in executive_summary_paragraphs(report))

    # ── (point 9) Allocation Details table + (point 10) Competency Report blocks
    alloc_table = _pdf_allocation_table(report, types, esc)
    comp_blocks = "".join(_pdf_chapter_block(ch, types, report.is_effort, esc) for ch in report.chapters)

    return f"""<!DOCTYPE html><html><head><meta charset="UTF-8"><style>
  @page {{
    size: a4 portrait; margin: 1.6cm 1.3cm 1.4cm 1.3cm;
    @frame footer {{ -pdf-frame-content: footerContent; bottom: 0.7cm; margin-left: 1.3cm; margin-right: 1.3cm; height: 0.6cm; }}
  }}
  body {{ font-family: Helvetica; font-size: 8pt; color: #1a1917; }}

  /* ── header / brand (point 5: match the site's "Aruvi.lesson studio") ── */
  .hdr {{ width: 100%; }}
  .brand-aruvi {{ font-family: Georgia, "Times New Roman", serif; font-size: 16pt; font-weight: bold; color: #164436; }}
  .brand-dot {{ font-family: Georgia, serif; font-size: 16pt; font-style: italic; color: #b65a31; }}
  .brand-studio {{ font-size: 7pt; letter-spacing: 1.5px; color: #6b6a63; }}
  .brand-ncf {{ font-family: Georgia, serif; font-style: italic; font-size: 7.5pt; color: #6b6a63; }}
  .rep-title {{ font-family: Georgia, serif; font-size: 11pt; font-weight: bold; color: #164436; }}
  .rep-sub {{ font-size: 7pt; color: #555; }}
  /* (point 1) gap below the logo, then the prototype's heavy full-width rule (2px solid).
     Rendered as a 1-cell table because xhtml2pdf draws table borders reliably. */
  .rule-tbl {{ width: 100%; margin-top: 10px; margin-bottom: 12px; }}
  .rule-tbl td {{ border-bottom: 2px solid #1a1917; font-size: 1pt; line-height: 1pt; }}

  /* (point 1) summary strip */
  .summary {{ width: 100%; border: 0.75px solid #ddd; margin-bottom: 14px; }}
  .sum-cell {{ text-align: center; padding: 6px 4px; border-right: 0.75px solid #ddd; }}
  .sum-val {{ font-size: 11pt; font-weight: bold; color: #1a1917; }}
  .sum-key {{ font-size: 5.5pt; letter-spacing: 0.5px; color: #777; }}

  /* (point 6) section heads — chapter-title font, two notches larger than chapter title (8.5pt -> 10.5pt) */
  .section-head {{ font-family: Georgia, serif; font-size: 10.5pt; font-weight: bold; color: #1a1917;
                   border-bottom: 1.25px solid #1a1917; padding-bottom: 3px; margin-top: 14px; margin-bottom: 7px; }}
  .exec p {{ font-size: 8pt; color: #333; margin-top: 5px; }}

  /* (point 9) Allocation Details table — clean, no dark bands (mirrors uploaded sample).
     Hairlines + alt shading live on the CELLS (not the table element) so they span the
     full width including the last column, which is where the previous version clipped. */
  .alloc-table {{ width: 100%; }}
  .alloc-table th {{ font-size: 6.5pt; color: #1a1917; font-weight: normal; text-align: center;
                     padding: 5px 6px; border-top: 0.75px solid #cccccc; border-bottom: 0.75px solid #dddddd; }}
  .alloc-table td {{ font-size: 8pt; color: #2a2a2a; padding: 5px 6px; text-align: center;
                     border-bottom: 0.5px solid #efefef; }}
  .alloc-table .alloc-name {{ text-align: left; padding-left: 8px; }}
  .alloc-seq {{ color: #888; font-size: 7pt; }}
  .alloc-strong {{ font-weight: bold; }}
  .alloc-table th:last-child, .alloc-table td:last-child {{ padding-right: 14px; }}
  .alloc-table th:first-child, .alloc-table td:first-child {{ padding-left: 10px; }}
  .alloc-table tr.alt td {{ background-color: #faf9f7; }}
  .alloc-table tr.alloc-total td {{ font-weight: bold; border-top: 0.75px solid #cccccc;
                                    border-bottom: 0.75px solid #cccccc; background-color: #f4f2ee; }}

  /* (point 10) Competency Report — prototype look, minus dark bands (point 3) */
  .ch-head {{ width: 100%; border-bottom: 0.75px solid #1a1917; margin-top: 12px; }}
  .ch-num {{ font-size: 8pt; font-weight: bold; color: #1a1917; }}   /* (point 8) same color as title */
  .ch-title {{ font-size: 8.5pt; font-weight: bold; font-family: Georgia, serif; color: #1a1917; }}
  .ch-alloc {{ font-size: 6.5pt; color: #333; }}                     /* (point 3) plain text, no dark band */
  .ch-weight {{ font-size: 6.5pt; color: #777; }}
  .comp-table {{ width: 100%; margin-top: 3px; }}
  /* (point 3) competency header: light row with dark text + underline, NOT a dark band */
  .comp-table th {{ font-size: 6pt; color: #1a1917; font-weight: normal; letter-spacing: 0.4px;
                    background-color: #ffffff; padding: 4px 6px; text-align: left;
                    border-bottom: 0.75px solid #d8d8d8; }}
  .comp-table td {{ font-size: 7pt; color: #2a2a2a; padding: 4px 6px; border-bottom: 0.5px solid #eee; vertical-align: top; }}
  .seq {{ color: #888; font-size: 6.5pt; text-align: center; }}
  .code {{ font-weight: bold; }}
  .wt {{ text-align: center; }}
  .nocomp {{ font-size: 7pt; color: #888; }}
  .footer {{ font-size: 6pt; color: #999; }}
</style></head><body>

  <table class="hdr"><tr>
    <td width="60%">
      <span class="brand-aruvi">Aruvi</span><span class="brand-dot">.</span>
      <span class="brand-studio">LESSON STUDIO</span><br/>
      <span class="brand-ncf">NCF 2023 aligned</span>
    </td>
    <td width="40%" align="right">
      <span class="rep-title">Allocation &amp; Competency report</span><br/>
      <span class="rep-sub">Grade {esc(g)} · {esc(subj)} · {esc(today)}</span>
    </td>
  </tr></table>
  <table class="rule-tbl"><tr><td></td></tr></table>

  <table class="summary"><tr>{stat_cells}</tr></table>

  <div class="section-head">Executive summary</div>
  {exec_paras}

  <div class="section-head">Allocation details</div>
  {alloc_table}

  <div class="section-head">Competency report</div>
  {comp_blocks}

  <div id="footerContent" class="footer">
    Aruvi · Allocation &amp; Competency report · Grade {esc(g)} · {esc(subj)} · Confidential
  </div>
</body></html>"""


def _pdf_allocation_table(report: CompetencyAllocationReport, types, esc) -> str:
    """(point 9) The Allocation Details table: one row per chapter with the per-duration
    period columns + total + the basis metric (Effort Index or Competency Weight)."""
    is_effort = report.is_effort
    metric_head = "Effort Index" if is_effort else "Competency Weight"

    # Column widths are set as per-cell width="%" on the header <th> cells.
    # xhtml2pdf 0.2.17 does NOT honor <colgroup>/<col> widths (it silently falls back
    # to equal-width columns), but it DOES honor width="" on the header cells. It also
    # systematically shrinks the LAST column below its requested width — which is what
    # previously collapsed the metric column to a ~12pt sliver, so its header and value
    # overflowed past the page's right edge. A small empty trailing "spacer" column
    # absorbs that shrink: with the spacer last, the metric column keeps its full width
    # and the alternating-/total-row shading reaches the table's true right border.
    n_dur = len(types)
    seq_w, total_w, metric_w, spacer_w, dur_w = 4, 12, 15, 3, 11
    chapter_w = 100 - (seq_w + total_w + metric_w + spacer_w + dur_w * n_dur)
    if chapter_w < 18:
        dur_w = max(7, (100 - seq_w - total_w - metric_w - spacer_w - 18) // max(n_dur, 1))
        chapter_w = 100 - (seq_w + total_w + metric_w + spacer_w + dur_w * n_dur)

    header = (
        f'<tr><th width="{seq_w}%">#</th>'
        f'<th class="alloc-name" width="{chapter_w}%">Chapter</th>'
        + "".join(f'<th width="{dur_w}%">{t.minutes}-min Periods</th>' for t in types)
        + f'<th width="{total_w}%">Total Periods</th>'
        + f'<th width="{metric_w}%">{metric_head}</th>'
        + f'<th width="{spacer_w}%"></th></tr>'
    )

    rows = ""
    tot_by_dur = {t.minutes: 0 for t in types}
    tot_periods = 0
    for i, ch in enumerate(report.chapters, 1):
        alt = " alt" if i % 2 == 0 else ""
        dur_cells = ""
        for t in types:
            v = ch.periods_by_duration.get(t.minutes, 0)
            tot_by_dur[t.minutes] += v
            dur_cells += f'<td>{v}</td>'
        tot_periods += ch.total_periods
        if is_effort:
            metric = "" if ch.effort_index in (None, "") else _g(ch.effort_index)
        else:
            metric = "" if ch.chapter_weight in (None, "") else _g(ch.chapter_weight)
        rows += (
            f'<tr class="row{alt}">'
            f'<td class="alloc-seq">{i}</td>'
            f'<td class="alloc-name">{esc(ch.chapter_title)}</td>'
            f'{dur_cells}'
            f'<td class="alloc-strong">{ch.total_periods}</td>'
            f'<td class="alloc-strong">{esc(metric)}</td>'
            f'<td></td></tr>'
        )

    foot_dur = "".join(f'<td>{tot_by_dur[t.minutes]}</td>' for t in types)
    footer = (
        f'<tr class="alloc-total"><td></td><td class="alloc-name">Total</td>{foot_dur}'
        f'<td>{tot_periods}</td><td></td><td></td></tr>'
    )
    return f'<table class="alloc-table" width="100%"><thead>{header}</thead><tbody>{rows}{footer}</tbody></table>'


def _g(v) -> str:
    """Trim trailing .0 (13.0 -> 13, 13.5 -> 13.5)."""
    try:
        f = float(v)
        return str(int(f)) if f == int(f) else str(f)
    except (TypeError, ValueError):
        return str(v)


def _pdf_chapter_block(ch: ChapterReport, types, is_effort: bool, esc) -> str:
    period_cells = " · ".join(
        f'{ch.periods_by_duration.get(t.minutes, 0)}×{t.minutes}min' for t in types
    ) or "—"
    weight_chip = ""
    if not is_effort and ch.chapter_weight not in (None, ""):
        weight_chip = f' &nbsp; <span class="ch-weight">Weight {esc(ch.chapter_weight)}</span>'

    show_wt = (not is_effort) and any(c.weight is not None for c in ch.competencies)
    if show_wt:
        head = ('<tr><th width="6%">#</th><th width="11%">Code</th>'
                '<th width="30%">Competency</th><th width="42%">Justification</th>'
                '<th width="11%">Weight</th></tr>')
    else:
        head = ('<tr><th width="6%">#</th><th width="12%">Code</th>'
                '<th width="33%">Competency</th><th width="49%">Justification</th></tr>')
    rows = ""
    for i, c in enumerate(ch.competencies, 1):
        wt_cell = ""
        if show_wt:
            w = int(c.weight or 0)
            wt_cell = f'<td class="wt">{"●" * w}{"○" * (3 - w)}</td>'
        rows += (
            f'<tr><td class="seq">{i}</td>'
            f'<td class="code">{esc(c.c_code)}</td>'
            f'<td>{esc(c.description)}</td>'
            f'<td>{esc(c.justification)}</td>'
            f'{wt_cell}</tr>'
        )
    table = (
        f'<table class="comp-table"><thead>{head}</thead><tbody>{rows}</tbody></table>'
        if rows else '<p class="nocomp">No competency entries for this chapter.</p>'
    )

    # chapter header: Ch NN (point 8: dark, same as title) + title; allocation as plain text (point 3)
    return (
        f'<table class="ch-head"><tr>'
        f'<td><span class="ch-num">Ch {str(ch.chapter_number).zfill(2)}</span> '
        f'<span class="ch-title">{esc(ch.chapter_title)}</span>{weight_chip}</td>'
        f'<td align="right"><span class="ch-alloc">{period_cells} · {ch.total_periods} periods · {ch.total_minutes}min</span></td>'
        f'</tr></table>{table}'
    )


def export_allocation_report_pdf(report: CompetencyAllocationReport) -> bytes:
    """Render the report to PDF bytes via xhtml2pdf (pure-Python, no system libs)."""
    from io import BytesIO
    from xhtml2pdf import pisa
    html_str = render_pdf_html(report)
    buf = BytesIO()
    result = pisa.CreatePDF(html_str, dest=buf, encoding="utf-8")
    if result.err:
        raise RuntimeError(f"xhtml2pdf failed with {result.err} error(s)")
    return buf.getvalue()
