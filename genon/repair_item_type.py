#!/usr/bin/env python3
"""repair_item_type.py — declared correction of a mislabelled assessment `question_type` (v1.0, 2026-08-12).

    python3 genon/repair_item_type.py --list     # show the declared repairs, change nothing
    python3 genon/repair_item_type.py            # apply them

WHY THIS EXISTS. ARV-D-120: the assessment constitutions select a question type from a TABLE
whose left column is a different enumeration (TWAU's `dominant_mode`, science's mode, SS's
weight tier). A model that copies the left column emits a value that looks like data because
it IS data — from the wrong column. The item is otherwise a perfectly good item: only the
label is wrong. Regenerating a whole canonical to fix one string is not worth the money, and
hand-editing the artefact is what every other repair tool in this folder exists to avoid.

WHAT IT WILL NOT DO, and this is the point of a DECLARED repair:
  * it never guesses the correct type. Every repair is written out below by a human with its
    evidence, and the script refuses unless what is on disk matches the declared `frm`;
  * it CROSS-CHECKS the target against the item's own `guide` block. A TWAU item's guide is
    keyed by its own question_type (assessment constitution Rule 9), so a mislabelled item
    carries the right answer in the key: `guide.SCR` on an item claiming `HI` says SCR. If
    the guide key and the declared target disagree, the repair is refused;
  * it touches ONE field. No text, no options, no reordering.

QUARANTINE. `build_library.py` moves a failed canonical to `backup/quarantine/` — so the file
this repairs is usually NOT in the library. When the library copy is missing, the newest
quarantined copy for that chapter is repaired and INSTALLED back under its proper name.

AND IT PURGES (ARV-D-034, and the 2026-08-11 lesson that `repair_unit_order.py` was the one
repair tool that forgot): an in-place repair does not change `canonical_version`, so any plan
already served from the old bytes keeps the cache key it was built with. Derived plans for
this chapter are removed; the next request rebuilds in milliseconds.
"""
from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from aruvi_core.genon.carriers import raw_item_list                # noqa: E402
from purge_derived import purge                                    # noqa: E402

LIB = REPO / "data" / "content" / "saved_plans"
QUAR = REPO / "backup" / "quarantine"

# ── THE DECLARED REPAIRS ────────────────────────────────────────────────────────
# subject, grade, chapter, unit_ref, frm, to, evidence (why `to` is the right answer).
DECLARED = [
    # APPLIED 2026-08-12. Kept as the record and SKIPPED by main(): re-running it fails its
    # own guard (the item no longer carries 'HI', which is the guard working), and a refusal
    # here used to abort every later declaration in the list. Once applied, a declaration is
    # a record, not an instruction — the same convention repair_register.py follows.
    dict(subject="the_world_around_us", grade="iv", chapter=6, unit=13, applied=True,
         frm="HI", to="SCR",
         evidence="ARV-D-120 recurrence, wave 1 of S5's corpus (2026-08-12). 'HI' is the "
                  "period's dominant_mode (Hands-on Investigation), copied from the LEFT "
                  "column of assessment v1.5 Rule 3's table; the row reads "
                  "'HI / CG-6 inquiry steps ... | SCR'. The item is an SCR in every other "
                  "respect: guide key SCR with two expected_elements, options [], look_for "
                  "[], task/scaffold '', performance_task false, and a populated stem "
                  "(Nila's three nights of sleep data). Founder authorised the back-fill "
                  "rather than a regeneration."),

    # ── S4 · mathematics · IX · WAVE 2 (the compacts), 2026-08-18 ──────────────────────
    # THREE ITEMS REPORTED AS "no stem — there is nothing to ask". None of them is missing
    # anything: each is a complete OPEN_TASK wearing an SCR/ECR label. The prompt is in
    # `task`, with `scaffold`, `format_of_output` and expected_elements/look_for populated,
    # and stem, options and expected_answer all empty — which is the OPEN_TASK shape the
    # constitution specifies and the certifier's own pair of checks tests for. Mathematics
    # emits a static five-key `guide` reference block rather than one keyed by the item's
    # type, so `shape="open_task"` is declared and verified field by field instead.
    dict(subject="mathematics", grade="ix", chapter=7, variant="p06",
         unit=None, section_ref="7.4", frm="SCR", to="OPEN_TASK", shape="open_task",
         evidence="the task is a drawn TREE DIAGRAM for two draws with replacement from a "
                  "3-ball bag, plus a written sample space in set notation and a probability "
                  "calculation. format_of_output demands 'A drawn tree diagram with labelled "
                  "branches' — there is no stem because the work IS the answer, which is what "
                  "OPEN_TASK is for. An SCR asks a question and expects a short constructed "
                  "response; this asks for a construction."),
    dict(subject="mathematics", grade="ix", chapter=8, variant="p10",
         unit=None, section_ref="8.4.1", frm="ECR", to="OPEN_TASK", shape="open_task",
         evidence="the gym-membership AP task: write the sequence, give the explicit formula "
                  "and the recursive rule, then explain part (d). format_of_output asks for "
                  "'Full working for each part' and 'A sentence of explanation'. Multi-part "
                  "constructed work against look_for criteria, with no stem to ask — "
                  "OPEN_TASK, not ECR."),
    dict(subject="mathematics", grade="ix", chapter=8, variant="p10",
         unit=None, section_ref="8.6.1", frm="ECR", to="OPEN_TASK", shape="open_task",
         evidence="the Sierpinski-triangle task: tabulate stage/count/area for Stages 0-3, "
                  "give explicit and recursive rules for two GPs, explain (e). "
                  "format_of_output asks for a TABLE plus formulae plus a written "
                  "explanation — a produced artefact, not an answer to a question."),
    # The fourth of the family needs no type change: ch 8 p07's item is already OPEN_TASK
    # and correct in every respect except that its `question_text` is JSON null rather than
    # "", which renders as the string 'None' and reads to the certifier as a populated stem.
    # frm == to makes this a pure serialisation normalisation, and the guard still holds:
    # the item must be found, alone, carrying exactly that type.
    dict(subject="mathematics", grade="ix", chapter=8, variant="p07",
         unit=None, section_ref="8.6.2", frm="OPEN_TASK", to="OPEN_TASK", shape="open_task",
         evidence="type is already right; the repair is `question_text` null -> \"\". Nothing "
                  "a teacher or student sees changes — the stem was already blank on the page."),
]


def newest_quarantined(subject: str, grade: str, ch: int, variant: str | None = None) -> Path | None:
    d = QUAR / subject / grade
    if not d.is_dir():
        return None
    pat = (f"ch_{ch:02d}_canonical_{variant}_*.json" if variant
           else f"ch_{ch:02d}_canonical_2*.json")     # the standard: stamp, not a p-suffix
    hits = sorted(d.glob(pat))
    return hits[-1] if hits else None


def guide_key(item: dict) -> str | None:
    g = item.get("guide")
    if isinstance(g, dict) and len(g) == 1:
        return next(iter(g))
    return None


def _open_task_shape(item: dict, retyping: bool = True) -> tuple[list[str], list[str]]:
    """Why an item IS an OPEN_TASK, read off its own fields. Returns (failures, advisories).

    `retyping` is False when the declared repair leaves question_type alone (frm == to) and
    only normalises serialisation. Marking criteria are then NOT a precondition: they are
    evidence that a mislabelled item should be retyped, and demanding them where the type is
    not in question would refuse a correct repair for an unrelated reason. Their absence is
    still reported — no check gates on it, so this is the only place it gets said.
    """
    bad, advisory = [], []
    if not str(item.get("task") or "").strip():
        bad.append("`task` is empty — an OPEN_TASK's prompt lives there")
    if str(item.get("question_text") or "").strip():
        bad.append("`question_text` is populated — an OPEN_TASK carries an empty stem")
    if item.get("options"):
        bad.append("`options` is populated")
    if str(item.get("expected_answer") or "").strip():
        bad.append("`expected_answer` is populated")
    if not (item.get("expected_elements") or item.get("look_for")):
        (bad if retyping else advisory).append(
            "neither `expected_elements` nor `look_for` is populated — the item carries no "
            "marking criteria at all, which nothing in certification checks")
    return bad, advisory


def apply_one(rep: dict, dry: bool) -> bool:
    subject, grade, ch = rep["subject"], rep["grade"], rep["chapter"]
    # v1.1, 2026-08-18 (S4 · maths·IX wave 2): a defect can land in a COMPACT, not only in
    # the standard. `variant` names the file suffix ("p10"); absent, the standard is meant.
    variant = rep.get("variant")
    stem = f"ch_{ch:02d}_canonical" + (f"_{variant}" if variant else "")
    target = LIB / subject / grade / f"{stem}.json"
    source, from_quarantine = target, False
    if not target.is_file():
        q = newest_quarantined(subject, grade, ch, variant)
        if q is None:
            print(f"  REFUSED {subject}/{grade} ch {ch}: no library copy and none quarantined")
            return False
        source, from_quarantine = q, True
        print(f"  (library copy absent — repairing the quarantined file {q.name})")

    doc = json.loads(source.read_text(encoding="utf-8"))
    res = doc.get("result", doc)
    where = f"unit {rep['unit']}" if rep.get("unit") is not None else f"section {rep.get('section_ref')}"
    if rep.get("unit") is not None:
        hits = [it for it in raw_item_list(res)
                if rep["unit"] in [int(x) for x in (it.get("period_ref") or [])
                                   if str(x).isdigit()]
                or str(it.get("period_ref")) == str(rep["unit"])]
    else:
        # DERIVED-ANCHOR STAGES have no period_ref by constitution (mathematics·IX assessment
        # v1.1 bans it outright), so the item is addressed by the section it tests.
        hits = [it for it in raw_item_list(res)
                if str(it.get("section_ref")) == str(rep["section_ref"])]
    hits = [it for it in hits if str(it.get("question_type")) == rep["frm"]]
    if len(hits) != 1:
        print(f"  REFUSED {subject}/{grade} ch {ch} {where}: expected exactly one "
              f"item carrying question_type {rep['frm']!r}, found {len(hits)}")
        return False
    item = hits[0]
    gk = guide_key(item)
    if gk is None and rep.get("shape") == "open_task":
        # The guide cross-check assumes a guide block keyed by the item's OWN type (TWAU
        # assessment Rule 9). Mathematics·IX emits a STATIC five-key reference block instead,
        # so the key carries no signal and cannot arbitrate. Where it cannot, the item's own
        # SHAPE must be declared and is then verified field by field — never assumed.
        bad, advisory = _open_task_shape(item, retyping=rep["frm"] != rep["to"])
        if bad:
            print(f"  REFUSED {subject}/{grade} ch {ch} {where}: declared shape open_task "
                  f"but " + "; ".join(bad))
            return False
        what = ("question_type %r -> %r" % (rep["frm"], rep["to"])
                if rep["frm"] != rep["to"] else "serialisation only (type unchanged)")
        print(f"  {subject}/{grade} ch {ch} {where}: {what}  (guide block is a static "
              f"reference; OPEN_TASK shape verified: task populated, stem/options/"
              f"expected_answer empty)")
        for a in advisory:
            print(f"      ADVISORY: {a}")
    elif gk != rep["to"]:
        print(f"  REFUSED {subject}/{grade} ch {ch} {where}: guide key {gk!r} does "
              f"not agree with the declared target {rep['to']!r}")
        return False
    else:
        print(f"  {subject}/{grade} ch {ch} {where}: question_type "
              f"{rep['frm']!r} -> {rep['to']!r}  (guide key {gk!r} agrees)")
    if dry:
        return True

    item["question_type"] = rep["to"]
    stem_fixed = False
    if rep["to"] == "OPEN_TASK" and item.get("question_text") is None:
        # An OPEN_TASK's stem must be "" — JSON null renders as the string 'None' downstream
        # and the certifier reads it as a populated stem. Normalising it is part of making
        # the label true, not a separate edit.
        item["question_text"] = ""
        stem_fixed = True
    doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
        "tool": "repair_item_type.py v1.1", "at": datetime.now().isoformat(timespec="seconds"),
        "unit": rep.get("unit"), "section_ref": rep.get("section_ref"),
        "variant": variant, "field": "question_type",
        "from": rep["frm"], "to": rep["to"], "evidence": rep["evidence"],
        **({"also": "question_text null -> \"\""} if stem_fixed else {}),
    })
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(doc, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"  written: {target.relative_to(REPO)}"
          + ("  (restored from quarantine)" if from_quarantine else ""))
    gone = purge(subject, grade, ch, reason="repair_item_type")
    print(f"  derived plans purged: {len(gone)}" + (f" — {gone}" if gone else ""))
    return True


def main() -> int:
    dry = "--list" in sys.argv
    live = [r for r in DECLARED if not r.get("applied")]
    print(f"repair_item_type.py — {len(live)} live declaration(s), "
          f"{len(DECLARED) - len(live)} already applied (kept as the record)"
          + ("  [--list: nothing will be written]" if dry else ""))
    # Evaluate every declaration before reporting: `all()` short-circuits, so one refusal
    # used to hide the rest.
    ok = all([apply_one(r, dry) for r in live])
    if not dry and ok:
        print("\nNext: re-certify the chapter(s), e.g.\n"
              "  python3 genon/build_library.py the_world_around_us iv 6 --certify-only")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
