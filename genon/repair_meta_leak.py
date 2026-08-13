#!/usr/bin/env python3
"""repair_meta_leak.py — strike the SERVE CONTRACT out of teacher-facing text (2026-08-13).

THE DEFECT, in one line: the brief tells the model *"this unit must not assume another
unit"*, and the model writes the instruction down instead of obeying it silently.

    "This surfaces the full conceptual map of the chapter **without requiring any
     specific earlier activity to have occurred**."      — TWAU iv ch 2 U17, BAND text

That clause is addressed to us, not to the teacher. She has never heard of a canonical, a
variant or a slot fill; told that her lesson does not require a prior activity, the only
thing she can conclude is that some other version of her lesson exists and she has not got
it. It is the machinery becoming visible on the one surface where it must not be.

HOW IT WAS FOUND. Not by a scanner — by F1 (C8 across the batch), reading borrowed seams on
TWAU. One instance was already repaired the same morning in SS·IX ch 5 ("an integrative
question that surveys the chapter's full arc *without claiming the chapter is complete*"),
and mathematics·IX had produced one earlier. Three separate sightings in three subjects
made it worth a corpus sweep, which found **29 instances across FOUR subjects, 21 files and
16 chapters — 10 of them in BAND text**, i.e. in the script the teacher reads aloud from,
not merely in guidance she can skip.

    the_world_around_us 20 · social_sciences 6 · english 2 · mathematics 1

WHY A SEPARATE TOOL FROM repair_register.py. That file is keyed by (subject, grade) and its
sets are stale by design once applied; this is ONE pattern across every subject at once, and
it will recur — english, mathematics and science have not been batch-authored yet. It keeps
repair_register's discipline exactly: every edit is a STATED (old → new) pair, applied by
assertion, never a generated rewrite; if `old` is not found verbatim the run fails loudly.

ALMOST EVERY EDIT IS A PURE DELETION of a trailing clause, and no teaching instruction is
removed anywhere. Five edits also capitalise the following word because the deletion took a
sentence's opening clause; those are marked CAP in the note and are the only characters this
tool adds. What survives every edit is the teacher's actual instruction — the question to
ask, the task to set, the thing to watch for.

WHAT IS DELIBERATELY *NOT* FIXED HERE, because it is a different and worse defect:
`social_sciences/ix/ch_01_canonical_p09.json` U9 band 3 names other units outright in
teacher-facing text — "(from the opening unit's definition)", "(from the third unit's
drought argument)" — in the very sentences preceding a claim to be working "without naming
any other unit". Deleting the meta-clause there leaves two real unit references standing.
That is a register ban-2 breach and belongs to repair_register.py or a re-author, on the
founder's call. Recorded here so the survivor is not mistaken for an oversight.

THE REAL FIX IS UPSTREAM and this tool does not deliver it: a brief phrased as a prohibition
hands the model a sentence to repeat. State self-containment as a property of the output
("each unit opens on its own ground"), never as a rule to acknowledge. Until that lands,
`genon/register_scan.py` now carries the pattern so certification catches it.

    python3 genon/repair_meta_leak.py --list      # show every declared edit
    python3 genon/repair_meta_leak.py --apply     # back up, apply, record, purge, re-scan
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))

from repair_register import _get_set                                   # noqa: E402
from purge_derived import purge                                        # noqa: E402

SAVED = REPO / "data" / "content" / "saved_plans"
BACKUP = REPO / "backup" / "meta_leak_repair"

# ── the declared edits ───────────────────────────────────────────────────────────
# "subject/grade/file": [(unit, locator, old, new, note)]
# CAP in a note = the deletion took a sentence opener, so the next word is capitalised.
EDITS = {
    # ── english ──────────────────────────────────────────────────────────────────
    "english/iii/ch_11_canonical.json": [
        (11, "teacher_notes",
         " without requiring any prior activity to have been set", "",
         "trailing clause; the stanzas and what they reward are untouched"),
        (12, "teacher_notes",
         " — without requiring any specific earlier activity to have taken place. "
         "Children who encounter this as their first sitting can still participate fully "
         "in every band.",
         ".",
         "clause + a whole sentence that is nothing but the serve contract ('their first "
         "sitting'). The list of what the synthesis draws on stands"),
    ],
    # ── mathematics ──────────────────────────────────────────────────────────────
    "mathematics/iii/ch_05_canonical.json": [
        (14, "teacher_notes",
         "Because the unit does not require any specific earlier activity to have been "
         "conducted, the opening recall wall",
         "The opening recall wall",
         "CAP. The 'whatever route children took' half is real guidance and stands"),
    ],
    # ── social_sciences ──────────────────────────────────────────────────────────
    "social_sciences/ix/ch_01_canonical.json": [
        (11, "teacher_notes",
         " The closing cross-discipline question draws on the chapter's earlier "
         "presentation of all four disciplines without naming specific earlier units.", "",
         "whole sentence is serve narration; the equity/efficiency guidance stands"),
        (13, "teacher_notes",
         " The quick-write connects back to the four-discipline structure without naming "
         "specific earlier units.", "",
         "same. NB this unit's OTHER breach — 'Having covered all four disciplines' — is "
         "ARV-D-157, accepted by founder ruling and deliberately left"),
    ],
    "social_sciences/ix/ch_01_canonical_p09.json": [
        (9, "band:3",
         " This task asks students to synthesise across the chapter's own argument without "
         "naming any other unit — the content is the chain, not the chain's links.", "",
         "the sentence claims to name no other unit while sitting directly after two that "
         "do. Only the CLAIM is struck here; the two real references are a register breach "
         "and are left for a founder call — see the module docstring"),
    ],
    "social_sciences/ix/ch_05_canonical_p13.json": [
        (4, "teacher_notes",
         " without requiring any prior activity from another unit", "",
         "trailing clause; 'the role play makes the deliberative function concrete' stands"),
    ],
    "social_sciences/ix/ch_03_canonical_p10.json": [
        (10, "band:3",
         " — without claiming coverage is complete or final", "",
         "BAND text. Found only by the new scanner's disclaimer pattern; 'coverage' is our "
         "word for our problem. The closing arc it names is real content and stands"),
    ],
    "social_sciences/ix/ch_05_canonical_p17.json": [
        (17, "teacher_notes",
         "Having examined state, society, religion, knowledge, and economy across seventeen "
         "units, this unit asks",
         "Having examined state, society, religion, knowledge, and economy, this unit asks",
         "THE COUNT. Seventeen is this variant's length, not the teacher's — every other "
         "serve of this chapter makes the sentence false. Same shape as the clock ban in a "
         "different currency. The five domains are content and stay"),
        (17, "teacher_notes",
         " — no prior artefact is needed", "",
         "the self-sufficiency boast. 'The cause-effect map is constructed and completed "
         "entirely within the unit' already tells the teacher everything she needs"),
        (17, "band:3",
         " — without claiming the chapter's work is complete", "",
         "BAND text; the summary quotation and the closing question are untouched"),
    ],
    "social_sciences/ix/ch_07_canonical_p05.json": [
        (2, "teacher_notes",
         " — students produce it within this unit's time, so no prior material is needed",
         " — students produce it within this unit's time",
         "SECOND leak in a unit already declared for another, and it survived the first "
         "--apply because the hand list had this file at band:2 only. Caught on the "
         "post-apply re-scan, which is the argument for the scanner over the list"),
        (2, "band:2",
         ", without requiring a definitive answer in this unit", "",
         "self-referential rather than cross-unit, but 'unit' is engine vocabulary on a "
         "teacher surface. The hypotheses task is untouched"),
    ],
    "social_sciences/viii/ch_03_canonical_p10.json": [
        (1, "teacher_notes",
         " without requiring any specific prior unit", "",
         "trailing clause; the Sikh-gurus bridge stands"),
    ],
    # ── the_world_around_us ──────────────────────────────────────────────────────
    "the_world_around_us/iii/ch_03_canonical_p06.json": [
        (6, "band:0",
         " This draws together the threads of the chapter — Rishi's journey, the spring "
         "festivals, the regional foods — without claiming to finish any topic.",
         " This draws together the threads of the chapter — Rishi's journey, the spring "
         "festivals, the regional foods.",
         "only the disclaimer goes; the three named threads are content and stay"),
    ],
    "the_world_around_us/iii/ch_10_canonical.json": [
        (2, "teacher_notes",
         " without requiring any prior unit", "",
         "trailing clause on a home-connection prompt"),
        (4, "band:3",
         " This sets up the intergenerational Find-out conversation without requiring it to "
         "be homework from a prior unit.",
         " This sets up the intergenerational Find-out conversation.",
         "the set-up is the point; the homework disclaimer is ours"),
    ],
    "the_world_around_us/iii/ch_10_canonical_p06.json": [
        (5, "teacher_notes",
         " without requiring it to be formalised in this unit", "",
         "self-referential 'unit'; 'plants the seed of change-of-state thinking' stands"),
    ],
    "the_world_around_us/iii/ch_12_canonical.json": [
        (16, "teacher_notes",
         "Do not ask children to recall specific earlier activities — instead ask what the "
         "chapter taught them about waste as a whole.",
         "Ask what the chapter taught them about waste as a whole.",
         "CAP. The instruction survives in the positive; the prohibition it was justifying "
         "was the serve contract said out loud"),
    ],
    "the_world_around_us/iii/ch_12_canonical_p10.json": [
        (10, "teacher_notes",
         " This reinforces transfer without naming other units.",
         " This reinforces transfer.",
         "the acknowledgement script before it is untouched"),
    ],
    "the_world_around_us/iv/ch_02_canonical.json": [
        (5, "teacher_notes",
         " without requiring a prior homework task", "",
         "trailing clause on the money-order prompt"),
        (17, "band:0",
         " This surfaces the full conceptual map of the chapter without requiring any "
         "specific earlier activity to have occurred.",
         " This surfaces the full conceptual map of the chapter.",
         "BAND text, and the worst-read instance in the corpus — the teacher's own script "
         "telling her what the lesson does not require"),
    ],
    "the_world_around_us/iv/ch_06_canonical.json": [
        (19, "band:0",
         "Without naming any particular sitting or activity, the teacher asks",
         "The teacher asks",
         "CAP. BAND text, in the STANDARD's synthesis unit — the one unit every class meets "
         "through a different prefix, so the leak reaches the widest audience of any. Found "
         "by the new register_scan pattern, NOT by the hand list: the leak opened a sentence "
         "with a capital and the hand sweep's boundary rule walked past it"),
    ],
    "the_world_around_us/iv/ch_06_canonical_p11.json": [
        (10, "band:0",
         "Teacher recalls (without naming any unit): ", "Teacher recalls: ",
         "BAND text; a parenthetical addressed to the pipeline, mid-script"),
    ],
    "the_world_around_us/iv/ch_06_canonical_p15.json": [
        (10, "teacher_notes",
         ", without naming those units", "",
         "trailing clause; the play-and-sleep link is real guidance"),
    ],
    "the_world_around_us/iv/ch_08_canonical.json": [
        (10, "teacher_notes",
         " without requiring a formal homework task", "",
         "trailing clause on the family-elder prompt"),
    ],
    "the_world_around_us/iv/ch_09_canonical_p10.json": [
        (10, "band:3",
         " — without claiming any journey is complete", "",
         "BAND text; 'travelled through four very different Indian lands' is the close and "
         "stands"),
    ],
    "the_world_around_us/v/ch_06_canonical.json": [
        (2, "teacher_notes",
         " without naming any unit", "",
         "trailing clause on the island-forest prompt"),
        (10, "band:3",
         " Drawing the parallel without naming another unit's content.",
         " Drawing the parallel.",
         "BAND text; the Hargila question itself is untouched"),
        (14, "teacher_notes",
         " without requiring them to have read anything before this unit", "",
         "trailing clause; the personal entry point stands"),
    ],
    "the_world_around_us/v/ch_09_canonical.json": [
        (12, "band:1",
         " (since this is a classroom sitting)", "",
         "BAND text. 'In the absence of actual family conversations' is a real pedagogical "
         "accommodation and stays; only the parenthetical explaining our scheduling goes"),
    ],
    "the_world_around_us/v/ch_10_canonical.json": [
        (4, "band:3",
         " — linking forward to the chapter's broader theme without naming any unit", "",
         "BAND text, and it carries a forward reference as well as the meta-clause"),
        (16, "teacher_notes",
         "This synthesis works with what any class has actually encountered in this chapter "
         "— whether they covered all the stories or only some, the connecting idea holds. ",
         "",
         "whole sentence narrates variable coverage; the sentence after it — accept any "
         "combination of examples — gives the teacher the same latitude without it"),
    ],
    "the_world_around_us/v/ch_10_canonical_p13.json": [
        (6, "teacher_notes",
         " without requiring prior homework", "",
         "trailing clause on the spice prompt"),
        (10, "teacher_notes",
         " without requiring prior homework to have been completed", "",
         "trailing clause; the bridge into the classroom stands"),
    ],
}


def apply_file(rel, edits, dry, resume=False):
    path = SAVED / rel
    if not path.is_file():
        raise SystemExit(f"missing: {path}")
    plan = json.loads(path.read_text(encoding="utf-8"))
    units = {u["period_number"]: u for u in plan["result"]["lesson_plan"]["periods"]}
    done, skipped = [], []
    for unit_no, loc, old, new, note in edits:
        u = units.get(unit_no)
        if u is None:
            raise SystemExit(f"{rel}: no unit {unit_no}")
        cur = _get_set(u, loc)
        if old not in cur:
            # --resume EXISTS BECAUSE THE SET GREW AFTER A PARTIAL APPLY (2026-08-13): the
            # post-apply re-scan found a second leak in a unit already repaired for a first,
            # and the file's other edits would then fail the guard forever. It does NOT
            # weaken the guard — an already-applied edit must PROVE itself by carrying the
            # `new` text (and, for a pure deletion, by the `old` being genuinely absent).
            # Anything else is still a hard stop, which is the case the guard is for.
            if resume and (new in cur if new.strip() else True):
                skipped.append((unit_no, loc))
                continue
            raise SystemExit(
                f"{rel} U{unit_no} {loc}: declared text not found — the artefact has changed "
                f"since this repair was written. Re-read it, do not force.\n  wanted: {old!r}"
                + ("\n  (--resume did not clear it: the replacement text is not there either, "
                   "so this is drift, not a re-run)" if resume else ""))
        if not dry:
            _get_set(u, loc, cur.replace(old, new, 1))
        done.append({"unit": unit_no, "field": loc, "rule": "register/meta-leak",
                     "removed": old.strip(), "replaced_with": new.strip(), "note": note})
    if not dry and done:
        gc = plan.setdefault("genon_canonical", {})
        gc.setdefault("repairs", []).append({
            "at": datetime.now().isoformat(timespec="seconds"),
            "tool": "genon/repair_meta_leak.py v1.0",
            "reason": ("the serve contract narrated into teacher-facing text — found at F1 "
                       "(C8 across the TWAU batch), 2026-08-13; founder instruction to fix "
                       "all 29 corpus-wide"),
            "edits": done,
        })
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return done, skipped


def main():
    dry = "--apply" not in sys.argv
    resume = "--resume" in sys.argv
    if not dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    n = 0
    touched = set()
    for rel, edits in EDITS.items():
        if not dry:
            src = SAVED / rel
            shutil.copy2(src, BACKUP / f"{rel.replace('/', '_')[:-5]}_{ts}.json")
        done, skipped = apply_file(rel, edits, dry, resume)
        for unit_no, loc in skipped:
            print(f"\n=== {rel} — U{unit_no} {loc}: ALREADY APPLIED, skipped (--resume)")
        if not done:
            continue
        n += len(done)
        subject, grade, fname = rel.split("/")
        touched.add((subject, grade, int(fname.split("_")[1])))
        print(f"\n=== {rel} — {len(done)} edit(s)"
              f"{' (DRY RUN, nothing written)' if dry else ''}")
        for d in done:
            print(f"  U{d['unit']:<3} {d['field']:<12} [{d['note']}]")
            print(f"        - {d['removed'][:150]}")
            print(f"        + {d['replaced_with'][:150] or '(deleted)'}")
    print(f"\n{'='*78}\n{n} edit(s) across {len(EDITS)} file(s), "
          f"{len(touched)} chapter(s)")
    if dry:
        print("dry run — re-run with --apply to write.")
        return
    # ARV-D-034: canonical_version is the GENERATION timestamp, so a repair does not move
    # it and the cache would serve pre-repair bytes forever. Purge per chapter, and say so.
    for subject, grade, ch in sorted(touched):
        gone = purge(subject, grade, ch, reason="meta-leak repair 2026-08-13")
        if gone:
            print(f"  purged {subject}/{grade} ch {ch:02d}: {len(gone)} derived plan(s)")
    print("\nderived plans purged; re-certify every touched stage with --certify-only.")


if __name__ == "__main__":
    main()
