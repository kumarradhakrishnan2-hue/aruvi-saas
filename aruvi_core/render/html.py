"""
The shared HTML renderer — ONE renderer for every subject.

It is structure-driven: it walks whatever Groups / Periods / AssessmentGroups the view model
declares and lays them out, reading group `type`/`label`/`meta` to title each section. It
never branches on subject. Stage differences (A/B/C vs implied-LO), subject differences
(progression-stage vs section->spine), all arrive as the same Group/Period shapes and render
through the same code. Visual stimuli render off their typed `StimulusType` — never dumped
as raw markup.
"""
from __future__ import annotations

import html as _html
from typing import List

from ..normalize import parse_table
from ..view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView,
    Period, StimulusType, ViewModel, VisualStimulus,
)


def _esc(s) -> str:
    return _html.escape(str(s if s is not None else ""))


def _meta_chips(meta: dict) -> str:
    """Render selected, human-useful meta as small chips (weight, implied LO, stage no…)."""
    keep = ("weight", "implied_lo", "stage_number", "description", "spine_code", "section_id")
    chips: List[str] = []
    for k in keep:
        v = meta.get(k)
        if v not in (None, "", [], {}):
            chips.append(f'<span class="chip"><b>{_esc(k)}</b> {_esc(v)}</span>')
    return f'<div class="chips">{"".join(chips)}</div>' if chips else ""


def _render_table(pipe_text: str) -> str:
    t = parse_table(pipe_text)  # single shared parser (normalize.py) — never re-split here
    if not t["header"] and not t["rows"]:
        return ""
    head = "".join(f"<th>{_esc(c)}</th>" for c in t["header"])
    body = "".join(
        "<tr>" + "".join(f"<td>{_esc(c)}</td>" for c in row) + "</tr>"
        for row in t["rows"]
    )
    return f'<table class="vs-table"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>'


def _render_stimulus(vs: VisualStimulus) -> str:
    if vs is None or vs.type == StimulusType.NONE or not vs.content:
        return ""
    if vs.type == StimulusType.SVG:
        return f'<div class="vs vs-svg">{vs.content}</div>'  # our own generated SVG
    if vs.type == StimulusType.TABLE:
        return f'<div class="vs">{_render_table(vs.content)}</div>'
    return f'<div class="vs vs-prose">{_esc(vs.content)}</div>'


def _render_period(p: Period) -> str:
    parts = [f'<div class="period"><div class="period-hd">'
             f'<span class="pnum">P{_esc(p.number)}</span> {_esc(p.title)}']
    dur = (p.meta or {}).get("duration_minutes")
    if dur:
        parts.append(f'<span class="dur">{_esc(dur)} min</span>')
    parts.append("</div>")
    if p.activities:
        parts.append("<ul class='acts'>" + "".join(f"<li>{_esc(a)}</li>" for a in p.activities) + "</ul>")
    if p.learning_outcomes:
        parts.append("<div class='lo'><b>LO:</b> " + "; ".join(_esc(x) for x in p.learning_outcomes) + "</div>")
    if p.teacher_notes:
        parts.append("<div class='tn'><b>Teacher notes:</b> " + " ".join(_esc(x) for x in p.teacher_notes) + "</div>")
    if p.homework:
        parts.append(f"<div class='hw'><b>Homework:</b> {_esc(p.homework)}</div>")
    parts.append("</div>")
    return "".join(parts)


def _render_group(g: Group) -> str:
    out = [f'<section class="grp grp-{_esc(g.type)}">',
           f'<div class="grp-hd"><span class="grp-type">{_esc(g.type)}</span>'
           f'<span class="grp-label">{_esc(g.label)}</span></div>',
           _meta_chips(g.meta or {})]
    for p in g.periods:
        out.append(_render_period(p))
    for child in g.children:          # nesting (English section -> spine)
        out.append(_render_group(child))
    out.append("</section>")
    return "".join(out)


def _render_item(it: AssessmentItem) -> str:
    out = [f'<div class="item"><div class="item-hd">'
           f'<span class="qtype">{_esc(it.item_type)}</span> {_esc(it.prompt)}</div>']
    out.append(_render_stimulus(it.visual_stimulus))
    if it.options:
        out.append("<ol class='opts' type='A'>" + "".join(f"<li>{_esc(o)}</li>" for o in it.options) + "</ol>")
    if it.answer:
        out.append(f"<div class='ans'><b>Answer:</b> {_esc(it.answer)}</div>")
    if it.implied_lo:
        out.append(f"<div class='lo'><b>Implied LO:</b> {_esc(it.implied_lo)}</div>")
    if it.teacher_guide:
        out.append("<div class='tg'><b>Teacher guide:</b><ul>"
                   + "".join(f"<li>{_esc(x)}</li>" for x in it.teacher_guide) + "</ul></div>")
    out.append("</div>")
    return "".join(out)


def _render_agroup(g: AssessmentGroup) -> str:
    chips = _meta_chips(g.meta or {})
    items = "".join(_render_item(it) for it in g.items)
    return (f'<section class="grp grp-{_esc(g.type)}">'
            f'<div class="grp-hd"><span class="grp-type">{_esc(g.type)}</span>'
            f'<span class="grp-label">{_esc(g.label)}</span></div>{chips}{items}</section>')


def render_lesson_plan(lp: LessonPlanView) -> str:
    body = "".join(_render_group(g) for g in lp.groups)
    return (f'<div class="block"><h2>Lesson Plan — {_esc(lp.chapter_title)} '
            f'<small>({_esc(lp.subject)}, grade {_esc(lp.grade)}, {_esc(lp.total_periods)} periods)</small></h2>'
            f'{body}</div>')


def render_assessment(a: AssessmentView) -> str:
    body = "".join(_render_agroup(g) for g in a.groups)
    return f'<div class="block"><h2>Assessment — {_esc(a.chapter_title)}</h2>{body}</div>'


_STYLE = """
<style>
.aruvi { font-family: -apple-system, Segoe UI, Roboto, sans-serif; color:#1a2230; line-height:1.5; max-width:860px; }
.aruvi h2 { font-size:18px; margin:18px 0 6px; border-bottom:2px solid #2d6cdf; padding-bottom:4px; }
.aruvi h2 small { color:#7a8699; font-weight:400; font-size:12px; }
.aruvi .grp { margin:10px 0; padding:8px 12px; border-left:4px solid #2d6cdf; background:#f5f8ff; border-radius:4px; }
.aruvi .grp .grp { background:#eef3ff; }      /* nested (spine inside section) */
.aruvi .grp-hd { display:flex; gap:8px; align-items:baseline; }
.aruvi .grp-type { font-size:10px; text-transform:uppercase; letter-spacing:.5px; color:#fff; background:#2d6cdf; padding:1px 6px; border-radius:8px; }
.aruvi .grp-label { font-weight:600; }
.aruvi .chips { margin:4px 0; }
.aruvi .chip { display:inline-block; font-size:11px; background:#dde7fb; color:#28427a; padding:1px 6px; border-radius:6px; margin:2px 4px 0 0; }
.aruvi .period, .aruvi .item { background:#fff; border:1px solid #e2e8f2; border-radius:6px; padding:8px 10px; margin:6px 0; }
.aruvi .period-hd, .aruvi .item-hd { font-weight:600; }
.aruvi .pnum, .aruvi .qtype { background:#1a2230; color:#fff; font-size:11px; padding:1px 6px; border-radius:6px; margin-right:6px; }
.aruvi .dur { float:right; color:#7a8699; font-size:12px; font-weight:400; }
.aruvi ul.acts, .aruvi ol.opts, .aruvi .tg ul { margin:4px 0 4px 18px; }
.aruvi .lo, .aruvi .tn, .aruvi .hw, .aruvi .tg { font-size:13px; color:#3a4658; margin-top:4px; }
.aruvi .ans { font-size:13px; color:#1c7a4a; margin-top:4px; font-weight:600; }
.aruvi .vs { margin:6px 0; }
.aruvi table.vs-table { border-collapse:collapse; font-size:13px; }
.aruvi table.vs-table th, .aruvi table.vs-table td { border:1px solid #c7d2e6; padding:3px 8px; text-align:left; }
.aruvi table.vs-table th { background:#e8eefb; }
.aruvi .vs-prose { font-style:italic; color:#55617a; }
.aruvi .vs-svg svg { max-width:100%; height:auto; }
</style>
"""


def render_view_fragment(vm: ViewModel) -> str:
    """Style + body, no <html>/<head> wrapper — for embedding."""
    return f'{_STYLE}<div class="aruvi">{render_lesson_plan(vm.lesson_plan)}{render_assessment(vm.assessment)}</div>'


def render_view(vm: ViewModel, title: str = "Aruvi") -> str:
    """A full standalone HTML document."""
    return (f'<!doctype html><html lang="en"><head><meta charset="utf-8">'
            f'<meta name="viewport" content="width=device-width, initial-scale=1">'
            f'<title>{_esc(title)}</title></head><body style="margin:24px;">'
            f'{render_view_fragment(vm)}</body></html>')
