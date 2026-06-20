"""
Renderer test — proves ONE renderer lays out two very different subjects correctly.

- Science: progression-stage groups render, and the litmus pipe-table renders as a real
  HTML <table> (NOT dumped as raw "A | B | C" text — the prototype's recurring bug).
- English: the two-axis structure renders as nested section -> spine groups.

Running as __main__ also writes viewable HTML to out/ for eyeballing in a browser.
"""
from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import aruvi_core.subjects.english  # noqa: E402  (register)
import aruvi_core.subjects.science  # noqa: E402  (register)
from aruvi_core.render import render_view, render_view_fragment  # noqa: E402
from aruvi_core.subjects.english import EnglishSubject  # noqa: E402
from aruvi_core.subjects.science import ScienceSubject  # noqa: E402
from aruvi_core.view_model import ViewModel  # noqa: E402

FX = os.path.join(os.path.dirname(__file__), "fixtures")


def _vm(subject, fixture_name):
    saved = json.load(open(os.path.join(FX, fixture_name)))
    r = saved["result"]
    ch = {"chapter_number": saved["chapter_number"], "chapter_title": saved["chapter_title"]}
    lp = subject.lesson_plan_to_view(r["lesson_plan"], grade=saved["grade"], chapter=ch)
    a = subject.assessment_to_view(r, grade=saved["grade"], chapter=ch)
    return ViewModel(lp, a)


def test_science_renders_table_and_stages():
    html = render_view_fragment(_vm(ScienceSubject(), "science_vii_ch02_saved.json"))
    assert 'grp-type">progression_stage' in html       # stage groups rendered
    assert '<table class="vs-table"' in html            # litmus table is a real table
    assert "Blue litmus" in html                        # its content is there
    assert "Substance | Blue litmus" not in html        # NOT dumped as raw pipe text
    assert "is_correct" not in html                      # options are clean text, not raw dicts
    assert "Answer:" in html                             # correct option surfaced


def test_english_renders_nested_section_and_spine():
    html = render_view_fragment(_vm(EnglishSubject(), "english_vii_ch01_saved.json"))
    assert 'grp-type">section' in html                  # outer axis
    assert 'grp-type">spine' in html                    # inner axis (nested)
    # a nested spine group must appear inside a section group
    assert html.index('grp-type">section') < html.index('grp-type">spine')
    assert "task_brief" not in html and "task_index" not in html  # tasks shown as text, not dicts


if __name__ == "__main__":
    test_science_renders_table_and_stages()
    test_english_renders_nested_section_and_spine()
    out = os.path.join(os.path.dirname(__file__), "..", "out")
    os.makedirs(out, exist_ok=True)
    sci = _vm(ScienceSubject(), "science_vii_ch02_saved.json")
    eng = _vm(EnglishSubject(), "english_vii_ch01_saved.json")
    open(os.path.join(out, "science.html"), "w").write(render_view(sci, "Aruvi — Science VII Ch02"))
    open(os.path.join(out, "english.html"), "w").write(render_view(eng, "Aruvi — English VII Ch01"))
    combined = ('<!doctype html><meta charset="utf-8"><body style="margin:24px;">'
                + render_view_fragment(sci) + "<hr style='margin:32px 0'>"
                + render_view_fragment(eng) + "</body>")
    open(os.path.join(out, "demo.html"), "w").write(combined)
    print("OK — renderer: Science table+stages and English nested section->spine both rendered.")
    print("Wrote out/science.html, out/english.html, out/demo.html")
