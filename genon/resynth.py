#!/usr/bin/env python3
"""resynth.py — re-author the TOP's synthesis unit against the whole library (spec §6 v1.3).

WHY. science·middle serves whole plans; at X = K+1 the top's synthesis unit is appended to
the K-count compact. The 2026-08-17 F1 read all 114 such serves: 101 double capstones
(the compact's own closer followed by a second whole-chapter closing, often the same
signature device — the Gandhian quote twice, the shell question re-answered twice) and 3
serves demanding a skill the served compact never taught (distance-time graphs, the
Section 13.6 response framework). Root cause: the synthesis was authored against the
top's own arc by a brief that never knew compacts existed.

THE FOUNDER'S CORRECTION (2026-08-17, replacing the same-day CODA design): do NOT add a
second serve asset or touch the serve law — that would give one stage of eleven its own
algorithm and a new artefact to maintain. Instead the top's synthesis unit itself is
RE-AUTHORED after wave 2, reading across the chapter's compacts. The serve law stays
byte-identical; whatever mild lightness the new unit has as the top's own finale is
confined to ONE serve (the top's identity) instead of 114.

WHAT THE NEW UNIT IS. Still the top's genuine closing synthesis — it keeps its
`synthesis: true` carrier, its period number, its stage — but it closes the chapter
THROUGH a fresh application (the pattern every CLEAN seam in the F1 read shared) rather
than through a ceremonial recap, and it is authored against:
  - the INTERSECTION of the compacts' coverage (it may demand only what every compact
    teaches — kills the skill-gap family by construction);
  - the compacts' final units in full (their vehicles and signature devices are spent —
    kills the material-redundancy family);
  - the top's own unit-title map (it must still land as that plan's closer).

The brief states these as properties of the output, never as prohibitions to acknowledge
(the meta-leak lesson, repair_meta_leak.py).

FIELDS. The model authors CONTENT: activity_title, activity_description, teacher_notes,
materials, time_bands, homework, pedagogical_approach. Install PRESERVES the unit's
identity fields from the old unit: period_number, period_duration_minutes,
progression_stage, stage_label, synthesis, roles. The old unit is archived whole inside
`genon_canonical.synthesis_reauthor.replaced`, with the compact fingerprints that were
read — provenance only, no staleness gate (founder: nothing new to maintain).

    python3 genon/resynth.py brief science vi 4       # print the two prompt blocks
    (generation itself rides batch_api.py --wave resynth)
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
for _p in (str(REPO), str(HERE)):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import generate_canonical as gc                                    # noqa: E402
import prompt_assembly as pa                                       # noqa: E402
from generate_canonical import (                                   # noqa: E402
    FOLDER_TO_SUBJECT, ROMAN, std_duration, master_plan_entry,
    parse_with_repair, log_token_log, log_ledger,
)
from purge_derived import purge                                    # noqa: E402

SAVED = REPO / "data" / "content" / "saved_plans"
BACKUP = REPO / "backup" / "resynth"

MAX_TOKENS_RESYNTH = 8_000

# authored by the model / preserved from the old unit — the install seam
AUTHORED = ("activity_title", "activity_description", "teacher_notes", "materials",
            "time_bands", "homework", "pedagogical_approach")
PRESERVED = ("period_number", "period_duration_minutes", "progression_stage",
             "stage_label", "synthesis", "roles")

# ── THE STAGE TABLE (2026-08-19, S7) ────────────────────────────────────────────
# science·middle is no longer the only stage that resynths, so the three stage-shaped
# facts — the contract, what the model authors, what the platform keeps — become a table
# row rather than module constants. The engine does not branch on subject; it looks the
# stage up, and a stage that is not in the table is refused rather than served science's
# fields (which is how a maths unit would silently acquire `progression_stage`).
#
# maths·middle authors `pedagogical_method` and `section_goal` where science authors
# `pedagogical_approach` and `activity_description`, and it authors its item pools too —
# as EMPTY arrays, which is the whole point of its brief and is why they are in AUTHORED
# rather than PRESERVED: the old unit's pools must be replaced, not carried over.
# `textbook_segments` is PRESERVED — the sections the closer revisits are the platform's
# registry business (serve.section_registry reads them), not the model's to re-decide.
STAGES = {
    ("science", "middle"): {
        "block": lambda d: resynth_system_block(d),
        "authored": AUTHORED,
        "preserved": PRESERVED,
        "spec": "science_middle_stage_serve.md §6 v1.3",
    },
    ("mathematics", "middle"): {
        "block": lambda d: resynth_system_block_maths_middle(d),
        "authored": ("activity_title", "pedagogical_method", "section_goal",
                     "teacher_notes", "visual_aids", "materials", "time_bands",
                     "textbook_items_in_class", "homework"),
        "preserved": ("period_number", "period_duration_minutes", "synthesis",
                      "textbook_segments"),
        "spec": "ARV-D-181 · F1 2026-08-19 (the double-closer collision)",
    },
}


def stage_row(subject_folder: str, grade_folder: str) -> dict:
    from aruvi_core.grades import stage_for
    key = (subject_folder, stage_for(grade_folder))
    if key not in STAGES:
        raise SystemExit(
            f"resynth is not defined for {key[0]} · {key[1]}. It re-authors a closing "
            "synthesis against the whole library, and what that unit must BE differs by "
            "stage — science closes through a fresh applied setting, mathematics through "
            "teacher-posed problems. Add a STAGES row with its own contract before running "
            "it here; serving another stage's brief would author the wrong unit and its "
            "fields with it.")
    return STAGES[key]


# ── library reading ─────────────────────────────────────────────────────────────

def _library(subject_folder: str, grade_folder: str, ch: int):
    """[(filename, plan_dict)], top first."""
    d = SAVED / subject_folder / grade_folder
    files = sorted(d.glob(f"ch_{ch:02d}_canonical*.json"))
    lib = [(f.name, json.loads(f.read_text(encoding="utf-8"))) for f in files]
    lib.sort(key=lambda t: -len(t[1]["result"]["lesson_plan"]["periods"]))
    return lib


def _final_unit(plan):
    return plan["result"]["lesson_plan"]["periods"][-1]


def _title_map(plan):
    ps = plan["result"]["lesson_plan"]["periods"]
    return [f"U{p['period_number']}: {p['activity_title']}" for p in ps]


def _canonical_version(plan):
    return (plan.get("genon_canonical") or {}).get("canonical_version") \
        or plan.get("saved_at") or ""


# ── the brief ───────────────────────────────────────────────────────────────────

def resynth_system_block(duration: int) -> str:
    """Stage-wide contract + schema; chapter-independent (cacheable per duration)."""
    return f"""ARUVI — CLOSING SYNTHESIS RE-AUTHORING · SCIENCE · MIDDLE STAGE

You are re-writing ONE unit: the closing whole-chapter synthesis of a chapter's fullest
lesson plan. This unit is served in two situations, and it must be excellent in both:

1. As the FINAL unit of the fullest plan — the class finishes the chapter with it.
2. As ONE EXTRA {duration}-minute period appended to a SHORTER complete plan of the same
   chapter, whose own final unit (given below) already consolidated the chapter
   yesterday.

THE UNIT YOU ARE WRITING closes the chapter through one fresh, concrete application: a
scenario, artefact, dataset, place or design problem the chapter itself never uses. The
class brings the chapter's concepts; the unit puts them to work in the new setting, and
what the task shows IS the synthesis — the chapter drawn together by using it whole, not
by summarising it.

PROPERTIES OF THE UNIT:
- It opens directly onto its fresh setting: the first band presents the new material and
  puts the first question to the class.
- Every concept or skill it calls on appears in EVERY unit-title map given below — the
  shorter plans differ in what they cover; write only to what all of them share.
- The SHORTEST plan's map is the binding one: applied topics and late enrichment are cut
  from it first, so each concrete demand in your task (a condition to cite, a feature to
  identify, a mechanism to explain) is checked against that map before it is used.
- Every mechanism, apparatus, circuit form or process your setting relies on is one the
  chapter itself teaches — the setting is new, its physics is entirely the chapter's.
- Its vehicle (the kind of task: scenario cards, argument construction, data table,
  concept map, design brief, error correction, narrative trace…) is different in kind
  from every FINAL UNIT given below, and it uses none of the specific stories, quotes,
  objects, questions or catchphrases those final units use.
- Its closing band consolidates what THE TASK ITSELF showed, naming the chapter's central
  ideas as the reason the task worked — earned closure, not ceremony.
- All materials are in its own `materials` list: things any classroom has or the unit
  itself makes.
- Band narration never states a quantity of minutes or any calendar time — the band's
  `minutes` field carries the clock.

OUTPUT — exactly this JSON object, nothing else:
{{
  "synthesis_unit": {{
    "activity_title": "…",
    "activity_description": "…",
    "pedagogical_approach": "a 2–5 word LABEL naming the method (e.g. 'Problem-based
      Collaborative Inquiry') — never a sentence; it prints beside the duration",
    "teacher_notes": "…",
    "materials": ["…"],
    "time_bands": [
      {{"minutes": "0-N", "activity": "…"}},
      …bands in sequence, integer boundaries, last band ends at {duration}…
    ],
    "homework": []
  }}
}}
No other keys — the platform carries the unit's number, stage and duration itself."""


def resynth_system_block_maths_middle(duration: int) -> str:
    """mathematics·middle's own contract (2026-08-19, S7 · F1).

    WHY IT IS NOT SCIENCE'S. Two differences, both measured.

    (a) THE COLLISION IS MEDIATED BY THE TEXTBOOK REFERENCE, and by nothing else. F1
    enumerated all 81 cross-canonical borrows on this stage: 18 of them repeat an exercise
    the previous sitting has just worked, and every single one is the SAME `book_ref` on
    both sides of the join — viii ch 11 re-issues all four of Figure it Out Q1–Q4 §4.2.7,
    vi ch 3 spends 20 of 40 minutes on Q1, Q8 and Q9 of §3.12. The cause is structural, not
    careless: a chapter has ONE end-of-chapter review set, both plans' closers reach for it,
    and neither author knew the other would be attached. A closing unit that names no
    textbook item cannot collide with any compact's closer, at any count, ever. So this
    brief does not ask for a better choice of exercises; it asks for a unit that has none.
    Rule 3's step 4 already declares that shape — a period whose item pools are empty takes
    an empty anchor, and "the assessment generator omits the exercise companion in this case
    but still generates a typed question grounded in the section's prose".

    (b) SIZE. Science's brief asks for "one fresh, concrete application — a scenario,
    artefact, dataset, place or design problem the chapter itself never uses", and a new
    setting has to be built before it can be used: science·middle's re-authored synthesis
    now runs 8,115 characters against a 2,520-character body unit (×3.2). Maths does not
    need a new world to be synthetic in — a proportional-reasoning problem IS the synthesis.
    This brief therefore asks for the same weight as any other sitting, and says so.

    THE TEMPLATE IS ONE OF OUR OWN. viii ch 7's synthesis was the cleanest seam in the F1
    read, and clean for exactly this reason: three teacher-posed problems, one per strand of
    the chapter, no textbook reference anywhere, 3,682 characters — our median. It is
    described below as properties of the output, never as a model to imitate or a rule to
    acknowledge (the meta-leak lesson, repair_meta_leak.py).
    """
    return f"""ARUVI — CLOSING SYNTHESIS RE-AUTHORING · MATHEMATICS · MIDDLE STAGE

You are re-writing ONE unit: the closing whole-chapter synthesis of a chapter's fullest
lesson plan. It is served in two situations and must be excellent in both:

1. As the FINAL unit of the fullest plan — the class finishes the chapter with it.
2. As ONE EXTRA {duration}-minute period appended to a SHORTER complete plan of the same
   chapter, whose own final unit (given below) already drew the chapter together
   yesterday.

THE UNIT YOU ARE WRITING closes the chapter by putting its methods to work on a small set
of problems the teacher poses. Solving them IS the synthesis: the chapter is drawn
together by being used, not by being recited.

PROPERTIES OF THE UNIT:
- It carries TWO TO FOUR problems, each reaching for a DIFFERENT major method of the
  chapter, and together spanning its main strands. Each problem is stated in full, with
  its numbers, inside the band that poses it — a teacher reads the band aloud and the
  class can start.
- The problems are the TEACHER'S OWN, written for this unit and posed on the board. The
  mathematics in each is the chapter's, and nothing is invented or imported.
- THE PROBLEMS AND THEIR SOLUTIONS LIVE IN ONE TABLE, in `visual_aids` — three columns,
  `No. | Problem | Solution`, one row per problem. The Problem cell states the problem in
  one or two plain sentences with its numbers. The Solution cell gives the answer and the
  few steps that reach it, in plain words and figures — brief enough for a teacher to read
  at a glance while the class works, and no longer than the problem it answers. This table
  is the teacher's whole worked reference.
- EACH PROBLEM IS WELL-POSED AND SELF-CONSISTENT. It states everything needed to solve it,
  its data agree with each other and with the solution beside it, and it has one answer.
  Where a count is named ("the four corner cells", "the six expressions you can form"),
  that count is the number the problem's own conditions produce. Where a figure carries
  measurements, they can all hold at once. Where a construction is described, the described
  construction is the one the solution works on.
- THE SOLUTION CELL IS THE SETTLED ANSWER. Work each problem out fully first; then write
  only the route that reaches the answer and the answer itself. Trials that failed,
  possibilities considered and rejected, re-checks and corrections belong to the working,
  not to the page a teacher reads at the board. Every step written is a step that holds:
  a justification names the fact it rests on, and never assumes what it is proving.
- `teacher_notes` is SHORT — a few sentences at most. It says how the sitting is run and
  what to watch for as students work; the mathematics is in the table, and is not repeated
  here. Name, for each problem, only the chapter method it needs — the method its own
  solution actually uses — and warn only about errors that problem can produce.
- THE NOTES OPEN BY SENDING THE TEACHER TO THE TABLE. Their first sentence is exactly:
  Refer to Prepared Table (see material: '<the table's title>') for the problems in full
  and their worked solutions.
  Everything above about the notes applies to what follows that sentence. Without it the
  notes describe a sitting whose mathematics has visibly gone somewhere and say nothing
  about where.
- Its `textbook_items_in_class` and `homework` are both `[]`, and its band text names no
  page, no exercise and no book item. The class works from the board.
- Its shape gives every student a full attempt before any answer is public: the problems
  are posed, worked individually with full working, compared in small groups where a
  disagreement is reconstructed step by step, and then presented — and each presentation
  is followed by the class NAMING the chapter method the solution rested on.
- The closing band states the chapter's one idea in a sentence, as the reason the problems
  yielded — earned closure, not ceremony.
- It is ONE sitting and weighs the same as any other: {duration} minutes, a handful of
  bands, materials any classroom has. Depth here is the demand of the problems, never the
  quantity of material.
- Every method it calls on appears in EVERY unit-title map given below — the shorter plans
  differ in what they reach, so write only to what all of them share, and treat the
  SHORTEST map as binding.
- Its vehicle differs in kind from every FINAL UNIT given below, and it reuses none of
  their specific contexts, objects, puzzles or framing questions.
- NO TEXT ANYWHERE IN THIS UNIT states a quantity of minutes or points beyond this sitting
  — not the bands, not the teacher notes, not the table. The band's `minutes` field carries
  the clock, and the platform rescales it to whatever length the sitting is served at, so a
  duration written into prose is wrong for most of the classes that meet it. Say "the first
  stretch", "before any discussion", "once every student has attempted all four" — the
  sequence, never the count. The one exception is a MEASUREMENT inside a problem or its
  solution: where minutes are the quantity the mathematics is about, they are data and stay.

OUTPUT — exactly this JSON object, nothing else:
{{
  "synthesis_unit": {{
    "activity_title": "…",
    "pedagogical_method": "one of: Discovery · Problem-solving · Play-way · Inductive ·
      Deductive — the method this unit runs on",
    "section_goal": "recall | reason | apply — the goal this unit works at",
    "teacher_notes": "a few sentences: how the sitting runs, what to watch for, and the
      chapter method each problem needs — NOT the solutions, which are in the table",
    "visual_aids": [
      {{"type": "table",
        "title": "Problems and solutions",
        "table": "No. | Problem | Solution\\n1 | … | …\\n2 | … | …"}}
    ],
    "materials": ["…"],
    "time_bands": [
      {{"minutes": "0-N", "activity": "…"}},
      …bands in sequence, integer boundaries, last band ends at {duration}…
    ],
    "textbook_items_in_class": [],
    "homework": []
  }}
}}
No other keys — the platform carries the unit's number, duration, section coverage and
synthesis marker itself."""


# ── per-chapter exclusions, learned by READING (never guessed) ──────────────────
# When the F1-resynth read finds a floor gap the generated unit missed, the finding is
# fed forward here verbatim — deterministic evidence in the brief, not another blind
# roll. Keyed (subject, grade, chapter); appended to the user block when present.
EXCLUSIONS = {
    ("science", "vi", 12):
        "VERIFIED GAPS IN THE SHORTEST (8-unit) PLAN — none of these may appear as a "
        "clue, a demand, or a closing concept: crater formation / impacts on an airless "
        "surface; the Pleiades/Krittika cluster (also absent from the 10-unit plan); "
        "identifying Mars by its reddish colour. Available instead, taught even in the "
        "8-unit plan: Venus as the dawn/dusk object, Sirius, the Pole Star with the "
        "Saptarishi pointer method, the Milky Way, a comet's tail pointing away from "
        "the Sun, artificial satellites.",
}


def resynth_user_block(subject_folder: str, grade_folder: str, ch: int) -> tuple[str, dict]:
    """The chapter's material. Returns (text, compacts_fingerprint)."""
    subject = FOLDER_TO_SUBJECT[subject_folder]
    grade = f"Grade {ROMAN[grade_folder]}"
    paths = pa.resolve_paths(grade, subject, ch)
    summary = Path(paths["chapter_summary"]).read_text(encoding="utf-8")

    lib = _library(subject_folder, grade_folder, ch)
    if len(lib) < 2:
        raise SystemExit(f"ch {ch}: no compacts on disk — the resynth reads across them")
    top_name, top = lib[0]
    compacts = lib[1:]

    parts = [f"CHAPTER SUMMARY:\n\n{summary}\n"]
    parts.append("=" * 70)
    parts.append(
        f"\nTHE FULLEST PLAN ({len(top['result']['lesson_plan']['periods'])} units). "
        "The unit you write REPLACES its final unit, closing this arc:\n")
    parts.append("\n".join(_title_map(top)[:-1]) + "\nU<final>: ← the unit you are writing")
    fingerprint = {}
    parts.append(
        f"\nTHE SHORTER PLANS ({len(compacts)}). Your unit may also be served right "
        "after any of their final units, all given here in full — write to what every "
        "title map shares, in a vehicle none of these final units uses.\n")
    for name, plan in compacts:
        n = len(plan["result"]["lesson_plan"]["periods"])
        fingerprint[name] = _canonical_version(plan)
        parts.append(f"\n--- PLAN OF {n} UNITS — unit-title map ---")
        parts.append("\n".join(_title_map(plan)))
        parts.append("\n--- its FINAL unit, in full ---")
        parts.append(json.dumps(_final_unit(plan), ensure_ascii=False, indent=1))
    excl = EXCLUSIONS.get((subject_folder, grade_folder, ch))
    if excl:
        parts.append("\n" + "=" * 70)
        parts.append("\n" + excl)
    parts.append("\n" + "=" * 70)
    parts.append("\nWrite the synthesis unit now, as the single JSON object specified.")
    return "\n".join(parts), fingerprint


def prepare_resynth_job(subject_folder: str, grade_folder: str, ch: int,
                        quiet: bool = True) -> dict | None:
    mp_row = master_plan_entry(subject_folder, grade_folder, ch)
    if mp_row and mp_row.get("placeholder"):
        return None
    duration = std_duration(grade_folder)
    title = (mp_row and str(mp_row["title"]).split(": ", 1)[-1]) or ""
    user_text, fingerprint = resynth_user_block(subject_folder, grade_folder, ch)
    system_text = stage_row(subject_folder, grade_folder)["block"](duration)
    if not quiet:
        print(f"{subject_folder} · {grade_folder} · ch {ch} — resynth "
              f"(system {len(system_text):,} chars · user {len(user_text):,} chars)")
    return {
        "subject_folder": subject_folder, "grade_folder": grade_folder, "ch": ch,
        "title": title, "duration": duration, "resynth": True,
        "inputs": fingerprint,
        "system_blocks": [{"type": "text", "text": system_text}],
        "user_blocks": [{"type": "text", "text": user_text}],
        "max_tokens": MAX_TOKENS_RESYNTH,
        "sys_chars": len(system_text), "usr_chars": len(user_text),
    }


# ── validate + install ──────────────────────────────────────────────────────────

def validate_resynth(parsed: dict, duration: int, *, row: dict = None) -> list[str]:
    """`row` defaults to science's for call-site stability; every stage-shaped check below
    reads it. The maths·middle additions are the two the brief turns on — the empty item
    pools and the absence of a page reference — checked here rather than trusted, because
    a closer that quietly kept one exercise would reintroduce the collision this whole
    re-author exists to remove, and nothing downstream looks."""
    row = row or STAGES[("science", "middle")]
    authored = row["authored"]
    problems = []
    u = parsed.get("synthesis_unit")
    if not isinstance(u, dict):
        return ["no synthesis_unit object"]
    method_key = "pedagogical_approach" if "pedagogical_approach" in authored else "pedagogical_method"
    for k in ("activity_title", "teacher_notes", method_key):
        if not u.get(k):
            problems.append(f"{k} missing")
    pa = u.get(method_key) or ""
    if len(pa.split()) > 6:
        problems.append(f"{method_key} {len(pa.split())} words — it is a "
                        "LABEL (2–5 words), it prints beside the duration")
    extra = set(u) - set(authored)
    if extra:
        problems.append(f"unexpected keys {sorted(extra)} — identity fields are the "
                        "platform's, not the model's")
    if "textbook_items_in_class" in authored:
        # DRAFTING SCRATCH IS REJECTED (2026-08-20, the first resynth wave's F1 read).
        # Seven of 38 closers shipped their working: "wait —", "Re-examine:", "✗", and in
        # one case ~600 words of abandoned trials before the answer. The brief now asks for
        # the settled answer only; this refuses the unsettled one, because a teacher reads
        # this table at the board and nothing downstream looks at it. Deliberately narrow —
        # these are drafting TELLS, not prose the model might legitimately want.
        import re as _re
        # THE CLOCK BAN, CHECKED AT INSTALL (2026-08-20). It has cost 22 declared repairs
        # on one wave and 28 on the next — more repair effort than every other defect on
        # this stage combined — because the brief stated it for BANDS and the model obeyed
        # it exactly there and nowhere else. The brief now binds the whole unit; this
        # refuses what slips through, so the sweep does not have to run a third time.
        # `visual_aids` is deliberately NOT scanned: minutes inside a problem are the
        # quantity being measured, which is why register_scan is scoped away from that
        # field too (maths vii ch 13, "Priya read for these many minutes each day").
        _clock = _re.findall(r"\bfor\b[^.;]{0,20}\bminutes\b",
                             json.dumps({k: u.get(k) for k in ("time_bands", "teacher_notes")},
                                        ensure_ascii=False), _re.I)
        if _clock:
            problems.append(
                f"a clock quantity in the lesson's own prose {sorted(set(_clock))} — the "
                "band's `minutes` carries the clock and the platform rescales it")
        _blob = json.dumps({k: u.get(k) for k in ("visual_aids", "time_bands")},
                           ensure_ascii=False)
        _tells = _re.findall(r"wait\s*[—\-–]|re-?examine[:,]|scratch that|"
                             r"let me (?:re)?check|actually,? (?:no|wait)|✗|"
                             r"on second thought|correction:|that'?s wrong", _blob, _re.I)
        if _tells:
            problems.append(
                f"the table carries drafting scratch {sorted(set(t.lower() for t in _tells))} "
                "— the Solution cell is the settled answer, not the working")
        # The problem/solution TABLE, and a teacher_notes that has not swallowed it.
        # Both are the 2026-08-19 correction: the first maths resynth put every worked
        # solution in teacher_notes, which ran to 3,268 characters against a 335-character
        # median for that chapter's body units. The mathematics belongs in the Material
        # tab as a table; the notes say how the sitting runs.
        aids = u.get("visual_aids")
        tabs = [a for a in (aids or []) if isinstance(a, dict) and a.get("type") == "table"]
        if not tabs:
            problems.append("visual_aids carries no table — the problems and their "
                            "solutions are the Material tab's, not teacher_notes'")
        else:
            head = str(tabs[0].get("table") or "").splitlines()[:1]
            if head and len(head[0].split("|")) != 3:
                problems.append(f"the table has {len(head[0].split('|'))} columns — it is "
                                "No. | Problem | Solution")
        tn = len(u.get("teacher_notes") or "")
        # 1200 -> 1600 (2026-08-20, second wave). The bound exists to stop the SOLUTIONS
        # living in the notes: the first resynth wrote 3,268 characters there against a
        # 335-character median for that chapter's body units. It was set at 1200 from that
        # one observation, and on the second wave it refused FIVE units whose solutions
        # were properly in the table — vi ch 3 (notes 1,225 · table 2,444), vi ch 4
        # (1,212 · 2,581), viii ch 4 (1,234 · 1,801), viii ch 5 (1,330 · 4,846), viii ch 8
        # (1,396 · 1,372) — every one with four table rows. The tightened brief also asks
        # the notes to name a method AND a watch-for per problem, which is four of each;
        # ~1,300 characters is that written plainly. 1600 clears the observed maximum with
        # headroom and still sits far below the failure it was written against. A bound
        # that refuses compliant work is a bound set from too little data.
        if tn > 1600:
            problems.append(f"teacher_notes {tn} chars — it is a few sentences on running "
                            "the sitting; the solutions live in the table")
        for k in ("textbook_items_in_class", "homework"):
            if u.get(k):
                problems.append(
                    f"{k} carries {len(u[k])} item(s) — this unit works from the board. "
                    "A textbook item here is what collides with the shorter plan's own "
                    "closer, which is the defect being repaired (ARV-D-181).")
        import re as _re
        hits = [b.get("minutes") for b in (u.get("time_bands") or [])
                if _re.search(r"\bp\.?\s?\d|\bpage\s\d|Figure it Out|Math Talk|Example \d"
                              r"|Let us|Try This", str(b.get("activity") or ""), _re.I)]
        if hits:
            problems.append(f"band(s) {hits} name a textbook item — same reason")
    bands = u.get("time_bands") or []
    if not bands:
        problems.append("no time_bands")
    else:
        end = 0
        for tb in bands:
            try:
                a, z = (int(x) for x in str(tb["minutes"]).replace("–", "-").split("-"))
            except Exception:
                problems.append(f"unparseable band minutes {tb.get('minutes')!r}")
                break
            if a != end:
                problems.append(f"band gap/overlap at {tb['minutes']}")
                break
            end = z
        else:
            if end != duration:
                problems.append(f"bands end at {end}, duration is {duration}")
    return problems


def install_resynth(parsed: dict, job: dict, ts: str, model: str) -> Path:
    """Replace the top's final unit's AUTHORED fields in place; archive the old unit and
    the compact fingerprints under genon_canonical.synthesis_reauthor; back up; purge."""
    sf, gf, ch = job["subject_folder"], job["grade_folder"], job["ch"]
    path = SAVED / sf / gf / f"ch_{ch:02d}_canonical.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    periods = doc["result"]["lesson_plan"]["periods"]
    old = periods[-1]
    if old.get("synthesis") is not True:
        raise SystemExit(f"{path.name}: final unit is not the synthesis — refusing")

    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, BACKUP / f"{sf}_{gf}_ch{ch:02d}_{ts}.json")

    row = stage_row(sf, gf)
    new_unit = {k: old[k] for k in row["preserved"] if k in old}
    authored = parsed["synthesis_unit"]
    for k in row["authored"]:
        # `in authored` is not enough on maths·middle: its item pools are authored as
        # EMPTY arrays, and the point of the brief is that they replace the old unit's
        # full ones. A key the brief names is written whether or not it is truthy.
        if k in authored:
            new_unit[k] = authored[k]
    periods[-1] = new_unit

    doc.setdefault("genon_canonical", {})["synthesis_reauthor"] = {
        "spec": row["spec"],
        "at": datetime.now().isoformat(timespec="seconds"),
        "ledger_ts": ts, "model": model,
        # provenance only — no staleness gate (founder 2026-08-17: nothing to maintain)
        "compacts_read": job["inputs"],
        # the replaced unit is NOT embedded (founder 2026-08-18: stale defective content
        # must not ride in Bucket A) — the pre-replacement file is the backup below
        "replaced_in": f"backup/resynth/{sf}_{gf}_ch{ch:02d}_{ts}.json",
    }
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    # ARV-D-034: repairs/replacements never move canonical_version, so derived plans
    # would serve pre-resynth bytes forever. Purge, loudly.
    purge(sf, gf, ch, reason="synthesis re-authored (spec §6 v1.3)")
    return path


def finish_resynth(job: dict, full: str, it: int, ot: int, *, model: str, ts: str,
                   cost_inr: float) -> tuple[str, list[str]]:
    sf, gf, ch = job["subject_folder"], job["grade_folder"], job["ch"]
    out_dir = gc.OUT_DIR / sf / gf
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"ch_{ch:02d}_{ts}_resynth_raw.txt"
    raw_path.write_text(full, encoding="utf-8")

    parsed, problems, repairs = parse_with_repair(full)
    if parsed is not None:
        problems = validate_resynth(
            parsed, job["duration"],
            row=stage_row(job["subject_folder"], job["grade_folder"]))
    elif not problems:
        problems = ["output is not valid JSON"]
    status = "ok" if not problems else "problems"
    if parsed is not None and status == "ok":
        dest = install_resynth(parsed, job, ts, model)
        print(f"  replaced synthesis in: {dest}")
    for p in problems:
        print(f"  ⚠ {p}")

    log_token_log("resynth_generation", sf, gf, ch, job["title"], it, ot, cost_inr)
    log_ledger({
        "ts": ts, "mode": "batch", "tag": "resynth", "model": model, "variant": "resynth",
        "subject": sf, "grade": gf, "chapter": ch,
        "schedule": f"1x{job['duration']}", "lp_only": False,
        "constitution": "resynth §6 v1.3",
        "input_tokens": it, "output_tokens": ot,
        "cost_inr": round(cost_inr, 2), "seconds": 0.0,
        "status": status,
        "problems": "; ".join(
            ([f"{len(repairs)} serialization repair(s)"] if repairs else []) + problems
        )[:400],
        "raw_file": raw_path.name,
    })
    return status, problems


# ═══════════════════════════════════════════════════════════════════════════════
# THE POLISH PASS (founder, 2026-08-18) — density + typed visuals for the same unit
# ═══════════════════════════════════════════════════════════════════════════════
# The re-authored synthesis notes ran mean 259 / max 450 words against the
# constitution's own Rule 10 ("2–3 sentences") and a corpus norm of 79 — the model
# packed card text, table designs and accept-lists into teacher_notes because the
# brief gave that content nowhere else to live. The polish pass gives it somewhere:
# prepared content moves to TYPED visual_aids (table entries as pipe-tables split by
# aruvi_core/normalize.parse_table — the same typing item stimuli use; prose entries
# for card text and accept-lists), materials point at them, and teacher_notes shrink
# to the constitution's shape with an explicit "(see material)" pointer. STRICT
# REORGANIZATION: the model receives only its own unit and may invent nothing.

MAX_TOKENS_POLISH = 6_000

POLISH_AUTHORED = ("teacher_notes", "materials", "visual_aids")


def polish_system_block() -> str:
    """Chapter-independent (one cacheable block for the whole stage)."""
    return """ARUVI — SYNTHESIS UNIT POLISH · SCIENCE · MIDDLE STAGE

You are reorganising ONE teaching unit you are given in full. Its content is final and
correct; the problem is WHERE things live. Its teacher_notes currently carry preparation
detail — card text, table designs, accept-lists, profiles — that belongs in structured
materials, leaving the notes far beyond their mandated 2–3 sentences.

REORGANISE. Drop nothing the teacher needs; every fact in your output must already be
in the unit you were given — with ONE licensed exception (founder ruling, 2026-08-18):
where the unit tells the teacher to PREPARE content it never specifies (cards, data
rows, reference answers), you may write that content out, provided every fact in it is
standard chapter-level science consistent with the unit's own bands. Specified content
is moved, never rewritten; only unspecified blanks may be filled.

Return exactly this JSON object, nothing else:
{
  "teacher_notes": "2–3 sentences of flowing prose. What the unit is doing and the one
    or two facilitation moves that matter most. Where preparation detail now lives in a
    visual aid, say so with '(see material)'. Never a list, never card text.",
  "materials": ["short physical items; where an item is prepared content, name its
    visual aid — e.g. \\"Twelve decision cards (see visual aid: 'Ramnagar decision
    cards')\\""],
  "visual_aids": [
    {"type": "table", "title": "…", "table": "pipe-delimited rows, first row the
      header, one row per line — e.g. Leg | Distance (km) | Time (min)\\n1 | 3 | 15"},
    {"type": "prose", "title": "…", "text": "card text / profile / accept-list moved
      here verbatim or lightly tightened"}
  ]
}

Rules: teacher_notes ≤ 3 sentences and ≤ 90 words · no quantity of minutes or calendar
time anywhere · every table's rows all have the same number of cells · visual_aids only
for content that genuinely helps the teacher prepare or project (do not manufacture a
table out of running prose) · time_bands are not yours to touch and their narration may
keep describing the same content."""


# Per-chapter polish notes, read-derived (same doctrine as the resynth EXCLUSIONS:
# when the fidelity read finds a shape the generic brief missed, the finding is fed
# forward verbatim rather than re-rolled blind).
POLISH_NOTES = {
    ("science", "vi", 10):
        "FOUNDER DIRECTION FOR THIS UNIT (2026-08-18): exactly TWO aids. Aid 1 — the "
        "student worksheet, ONE merged table: Object | Observation notes | Movement | "
        "Growth | Nutrition | Respiration | Excretion | Sensitivity | Reproduction | "
        "Verdict, where Observation notes carries exactly two authored sentences per "
        "object written so students must reason (no verdict words, no characteristic "
        "named as an answer) and all other cells are blank for the student. These "
        "fourteen sentences are the licensed teacher-prepared blank — author them. "
        "There is NO separate printed data card; the description lives beside the grid "
        "it feeds. Aid 2 — the teacher key, a second table only the teacher sees: "
        "Object | Intended verdict | Decisive characteristic | one-line steer. This "
        "replaces the current prose essay entirely (its design intent survives as "
        "columns; its repetition of the teacher notes does not). Materials should note "
        "the worksheet prints best landscape.",
}


def prepare_polish_job(subject_folder: str, grade_folder: str, ch: int) -> dict | None:
    mp_row = master_plan_entry(subject_folder, grade_folder, ch)
    if mp_row and mp_row.get("placeholder"):
        return None
    p = SAVED / subject_folder / grade_folder / f"ch_{ch:02d}_canonical.json"
    doc = json.loads(p.read_text(encoding="utf-8"))
    unit = doc["result"]["lesson_plan"]["periods"][-1]
    if unit.get("synthesis") is not True:
        return None
    title = (mp_row and str(mp_row["title"]).split(": ", 1)[-1]) or ""
    note = POLISH_NOTES.get((subject_folder, grade_folder, ch))
    user_text = ("THE UNIT, in full:\n\n" + json.dumps(unit, ensure_ascii=False, indent=1)
                 + (("\n\n" + "=" * 70 + "\n" + note) if note else "")
                 + "\n\nReorganise it now, as the single JSON object specified.")
    system_text = polish_system_block()
    return {
        "subject_folder": subject_folder, "grade_folder": grade_folder, "ch": ch,
        "title": title, "duration": std_duration(grade_folder), "polish": True,
        "inputs": {},
        "system_blocks": [{"type": "text", "text": system_text}],
        "user_blocks": [{"type": "text", "text": user_text}],
        "max_tokens": MAX_TOKENS_POLISH,
        "sys_chars": len(system_text), "usr_chars": len(user_text),
    }


def validate_polish(parsed: dict) -> list[str]:
    problems = []
    tn = parsed.get("teacher_notes")
    if not isinstance(tn, str) or not tn.strip():
        return ["teacher_notes missing"]
    # The constitutional gate is SENTENCES (Rule 10: "2–3 sentences of flowing prose"),
    # not words — the first word-count gate (~90) refused a compliant 3-sentence/119-word
    # result on the densest unit in the corpus (vi ch 11, 2026-08-18). 130 words stays as
    # a sanity ceiling only.
    import re as _re
    sents = [s for s in _re.split(r"(?<=[.!?])\s+", tn.strip()) if s]
    if len(sents) > 3:
        problems.append(f"teacher_notes {len(sents)} sentences — Rule 10 caps it at 3")
    words = len(tn.split())
    if words > 130:
        problems.append(f"teacher_notes {words} words — beyond any 3-sentence reading")
    if not isinstance(parsed.get("materials"), list) or not parsed["materials"]:
        problems.append("materials missing/empty")
    vas = parsed.get("visual_aids")
    if not isinstance(vas, list):
        problems.append("visual_aids must be a list (may be empty)")
    else:
        sys.path.insert(0, str(REPO))
        from aruvi_core.normalize import parse_table
        for i, va in enumerate(vas):
            t = va.get("type")
            if t == "table":
                if not va.get("table"):
                    problems.append(f"visual_aids[{i}]: table entry without table text")
                else:
                    parsed_t = parse_table(va["table"])
                    if not parsed_t["rows"]:
                        problems.append(f"visual_aids[{i}]: table has no body rows")
            elif t == "prose":
                if not va.get("text"):
                    problems.append(f"visual_aids[{i}]: prose entry without text")
            else:
                problems.append(f"visual_aids[{i}]: unknown type {t!r}")
            if not va.get("title"):
                problems.append(f"visual_aids[{i}]: title missing")
    return problems


def install_polish(parsed: dict, job: dict, ts: str, model: str) -> Path:
    sf, gf, ch = job["subject_folder"], job["grade_folder"], job["ch"]
    path = SAVED / sf / gf / f"ch_{ch:02d}_canonical.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    unit = doc["result"]["lesson_plan"]["periods"][-1]
    if unit.get("synthesis") is not True:
        raise SystemExit(f"{path.name}: final unit is not the synthesis — refusing")
    BACKUP.mkdir(parents=True, exist_ok=True)
    shutil.copy2(path, BACKUP / f"{sf}_{gf}_ch{ch:02d}_polish_{ts}.json")
    for k in POLISH_AUTHORED:
        if k in parsed:
            unit[k] = parsed[k]
    doc.setdefault("genon_canonical", {})["synthesis_polish"] = {
        "spec": "density + typed visual_aids (founder, 2026-08-18)",
        "at": datetime.now().isoformat(timespec="seconds"),
        "ledger_ts": ts, "model": model,
        # payload not embedded (founder 2026-08-18) — the pre-polish file is the backup
        "replaced_in": f"backup/resynth/{sf}_{gf}_ch{ch:02d}_polish_{ts}.json",
    }
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    purge(sf, gf, ch, reason="synthesis polished (notes density + typed visual aids)")
    return path


def finish_polish(job: dict, full: str, it: int, ot: int, *, model: str, ts: str,
                  cost_inr: float) -> tuple[str, list[str]]:
    sf, gf, ch = job["subject_folder"], job["grade_folder"], job["ch"]
    out_dir = gc.OUT_DIR / sf / gf
    out_dir.mkdir(parents=True, exist_ok=True)
    raw_path = out_dir / f"ch_{ch:02d}_{ts}_polish_raw.txt"
    raw_path.write_text(full, encoding="utf-8")
    parsed, problems, repairs = parse_with_repair(full)
    if parsed is not None:
        problems = validate_polish(parsed)
    elif not problems:
        problems = ["output is not valid JSON"]
    status = "ok" if not problems else "problems"
    if parsed is not None and status == "ok":
        dest = install_polish(parsed, job, ts, model)
        print(f"  polished: {dest}")
    for p in problems:
        print(f"  ⚠ {p}")
    log_token_log("polish_generation", sf, gf, ch, job["title"], it, ot, cost_inr)
    log_ledger({
        "ts": ts, "mode": "batch", "tag": "polish", "model": model, "variant": "polish",
        "subject": sf, "grade": gf, "chapter": ch,
        "schedule": f"1x{job['duration']}", "lp_only": False,
        "constitution": "polish 2026-08-18",
        "input_tokens": it, "output_tokens": ot,
        "cost_inr": round(cost_inr, 2), "seconds": 0.0,
        "status": status,
        "problems": "; ".join(
            ([f"{len(repairs)} serialization repair(s)"] if repairs else []) + problems
        )[:400],
        "raw_file": raw_path.name,
    })
    return status, problems


def polish_ts(subject_folder: str, grade_folder: str, ch: int) -> str:
    p = SAVED / subject_folder / grade_folder / f"ch_{ch:02d}_canonical.json"
    if not p.is_file():
        return ""
    doc = json.loads(p.read_text(encoding="utf-8"))
    return ((doc.get("genon_canonical") or {}).get("synthesis_polish") or {}).get(
        "ledger_ts", "")


def is_reauthored(subject_folder: str, grade_folder: str, ch: int) -> bool:
    p = SAVED / subject_folder / grade_folder / f"ch_{ch:02d}_canonical.json"
    if not p.is_file():
        return False
    doc = json.loads(p.read_text(encoding="utf-8"))
    return bool((doc.get("genon_canonical") or {}).get("synthesis_reauthor"))


def reauthor_ts(subject_folder: str, grade_folder: str, ch: int) -> str:
    """The ledger_ts of the installed re-author, '' when none. Collect's skip guard
    compares THIS, not is_reauthored: after wave 3 every chapter is re-authored, so an
    is_reauthored skip silently discards every --redo re-run at collect (bitten
    2026-08-18, vi ch 4/12 — paid results skipped, rescued only because batches keep
    29 days). Batch-aware: skip only what THIS manifest already installed."""
    p = SAVED / subject_folder / grade_folder / f"ch_{ch:02d}_canonical.json"
    if not p.is_file():
        return ""
    doc = json.loads(p.read_text(encoding="utf-8"))
    return ((doc.get("genon_canonical") or {}).get("synthesis_reauthor") or {}).get(
        "ledger_ts", "")


if __name__ == "__main__":
    if len(sys.argv) == 5 and sys.argv[1] == "brief":
        _, _cmd, sf, gf, ch = sys.argv
        job = prepare_resynth_job(sf, gf, int(ch), quiet=False)
        if job:
            print("\n===== SYSTEM =====\n" + job["system_blocks"][0]["text"])
            print("\n===== USER =====\n" + job["user_blocks"][0]["text"][:4000] + " …")
    else:
        print(__doc__)
