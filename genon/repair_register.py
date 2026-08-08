#!/usr/bin/env python3
"""repair_register.py — backfill register breaches in an authored library (v1.0, 2026-08-02).

FOUNDER RULING, 2026-08-02: regenerating is a lottery. The SS·IX ch 3 top canonical breached
THE SELF-CONTAINED REGISTER nine times while authored under v1.10, which bans it in terms;
another run samples the same distribution at Rs 39 with no guarantee. So breaches are repaired
in place — and the doctrine that "fixes happen upstream, never by hand-editing artifacts" is
honoured by making the repair a PIPELINE STAGE rather than a text editor session: the edits are
declared here in code, applied by assertion, recorded in the artefact, and re-scanned.

WHAT MAKES THIS SAFE, and the line it must not cross:
  * every edit is a STATED (old -> new) pair, not a generated rewrite. No model authors text
    here. If `old` is not found verbatim the file is left untouched and the run fails loudly —
    so a repair can never silently drift against a regenerated artefact.
  * almost every edit is a DELETION of a trailing clause (the breaches are appositives:
    "— a thread to pick up in the climate-change unit"). Nothing is invented.
  * the artefact records what was done, in genon_canonical.repairs[], so corpus statistics can
    still tell generation quality from repair quality. Without that record we would lose the
    evidence that says whether to change the MECHANISM instead of repairing forever.
  * STRUCTURAL and PEDAGOGICAL defects are OUT OF SCOPE and must stay out: a cross-unit
    materials dependency, approach-diversity repeats, an anchor that names the wrong section.
    Repairing those here would launder content changes as text hygiene. They go to the human
    gate or a regeneration decision.

    python3 genon/repair_register.py --list                        # show the declared edits
    python3 genon/repair_register.py --apply                       # back up, apply, record, re-scan
    python3 genon/repair_register.py --grade ix --list             # an older stage's set

v1.3, 2026-08-04: the library path is no longer hard-coded to social_sciences/ix — the tool
takes --subject/--grade and selects the matching declaration set, because S2 needed it. Each
set is keyed by (subject, grade) and is stale by design once applied: re-running an applied set
FAILS its own "declared text not found" assertion, which is the guard, not a bug.

v1.4, 2026-08-08 (S4): the mathematics·IX ch 4 set — six forward references, no clock
quantities, five of the six in the standard canonical. First library whose breaches are ALL of
one ban, and the first where every hit is a pedagogical signpost rather than the boilerplate the
ban's own examples name. See the set's header comment: one hit is the model paraphrasing the
brief's own description of the synthesis unit, which is an argument about the BRIEF, not the
model. Repair remains the founder's route (2026-08-02: regenerating is a lottery).
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

from register_scan import scan_plan, report                      # noqa: E402
from purge_derived import purge                                  # noqa: E402

SAVED = REPO / "data" / "content" / "saved_plans"
BACKUP = REPO / "backup" / "register_repair"

# ── the declared edits ───────────────────────────────────────────────────────────
# file -> [(unit_number, field_locator, old, new, rule_broken, note)]
# field_locator: "teacher_notes" | "band:<index>" | "homework:<index>"
#
# DECLARATIONS REWRITTEN 2026-08-03 (v1.1). The previous set was written against the
# 2026-08-01 library (12/9/7) and went stale the moment that library was regenerated under
# LP v1.10 / assessment v1.6 on 2026-08-03 (12/10/7) — `--list` failed its own assertion on
# the very first edit, which is the guard working exactly as designed. The p09 variant no
# longer exists; p07 now scans clean. What follows is declared against the CURRENT artefacts
# (ch_03_canonical.json 14:19, ch_03_canonical_p10.json 14:34, ch_03_canonical_p07.json 14:34)
# and covers the four surviving breaches in the 2026-08-03 certification report.
#
# Three of the four are the SAME family: a clock quantity written into band prose when the
# band already carries its own `minutes`. Those are pure deletions of the quantity — the
# activity, the grouping and the output all stand. The fourth is a forward reference.
# ── v1.2 ADDITIONS, 2026-08-03 (ARV-D-026) ──────────────────────────────────────
# Four breaches found at C3 that the 18:07 pass never saw, because register_scan had no
# pattern for their phrasing: a RANGED clock quantity ("for two to three minutes" — the
# scanner matches "for two minutes") and three forward references in prose the pattern list
# did not cover. The patterns are added to register_scan.py in the same change, so the next
# library is gated on them rather than found by hand. The p10 U1 "the three functions the
# whole chapter unpacks" borderline is deliberately NOT repaired (founder ruling, same day):
# read as orienting prose about the chapter as an object, not a pointer to a later unit.
#
# ── v1.3, 2026-08-04 · S2 · social_sciences VIII ch 3 "The Rise of the Marathas" ──
# Seven breaches in the 16:37 certification report — 3 forward references, 4 clock quantities,
# across the standard canonical (6) and p10 (1); p13 scanned clean.
#
# WHY THIS LIBRARY BREACHED, and why repair is the founder's call rather than the obvious one:
# the artefact records `constitution: LP v2.7 / assessment v2.3`. It was authored at 16:10-16:37,
# BEFORE the stage's P1-P4 amendments landed at 17:39 — so it was generated against a
# constitution that did not contain THE SELF-CONTAINED REGISTER at all. The model was never told
# the three bans. That makes this NOT the 2026-08-02 lottery case (SS·IX breached a register its
# constitution stated in terms); a run under v2.8 would have been the first roll with the rule
# present. FOUNDER RULING 2026-08-04: repair now, do not regenerate — ~Rs 150 and the ordering
# breach is recorded as a waiver instead. Consequence carried forward: the v2.8 register block
# enters the campaign never having been GENERATED against, and is owed a live check at the
# corpus pre-warm (MEMORY.md "AMENDMENTS TO BE TESTED").
#
# All seven are pure deletions. Nothing is rewritten and no clause is replaced with new text:
# three trailing forward-reference appositives go whole, and four clock quantities are struck
# from sentences that read correctly without them ("for four minutes" -> ""), which is exactly
# what the register asks for — the band already carries its own `minutes`, and the platform
# rescales them.
REPAIRS = {
    ("social_sciences", "viii"): {
        "ch_03_canonical.json": [
            (2, "band:3",
             " as a preview of the next unit's content", "",
             "register/forward",
             "the timeline mark itself is the teaching act and stands alone; naming what the "
             "NEXT unit holds is false for any teacher whose X ends here or borrows a "
             "different unit at this slot"),
            (6, "band:3",
             " — setting up the military and conflict discussion in later units", "",
             "register/forward",
             "trailing appositive on the Amatya/Sachiv answer. The revenue question closes on "
             "its own ground; 'later units' is unknowable at authoring"),
            (7, "band:0",
             "; navy addressed in the next unit", "",
             "register/forward",
             "the cavalry correction (bargirs/shiledars) is complete without it. The navy has "
             "its own registry section and will be reached, or not, by the served count"),
            (7, "band:0",
             " for four minutes", "",
             "register/clock",
             "same band as the edit above. The read-then-fill instruction is unchanged; the "
             "band's own 0-8 minutes carry the time and are rescaled per sitting"),
            (9, "band:0",
             " for five minutes", "",
             "register/clock",
             "'begin reading the two sections from the chapter summary' is the instruction; "
             "the quantity is falsified silently whenever the sitting is not 45 min"),
            (16, "band:0",
             "Teacher circulates for three minutes, then students share",
             "Teacher circulates, then students share",
             "register/clock",
             "synthesis unit. The circulate-then-share sequence is the teaching move and "
             "survives the quantity's removal intact"),
        ],
        "ch_03_canonical_p10.json": [
            (4, "band:0",
             "Students discuss in pairs for two minutes, then share",
             "Students discuss in pairs, then share",
             "register/clock",
             "the only hit in the compact. Pair-discuss-then-share is unchanged"),
        ],
    },
    # ── APPLIED 2026-08-03; kept as the record. Re-running this set will FAIL its own
    #    "declared text not found" assertion, because the text is already gone. That is the guard.
    ("social_sciences", "ix"): {
        "ch_03_canonical_p07.json": [
            (5, "band:3",
             " This bridges toward the climate change and Punjab floods sections that follow.", "",
             "register/forward",
             "found at C8 by reading the LAST sitting of the 5-period serve, where this unit lands "
             "last and the sentence is simply false; at 6 it is half false (the floods section is "
             "dropped). The discussion it closes — monsoon variability as both sustenance and risk — "
             "is complete without it, so the trailing sentence goes whole"),
        ],
    },
    # ── S3 · science · secondary · ch 8 "Journey Inside the Atom" (2026-08-06) ──────
    # THE FIRST LIBRARY AUTHORED WITH THE REGISTER ALREADY IN ITS CONSTITUTION.
    # SS·VIII's 7 hits came from a library generated BEFORE its P1 amendment landed — the
    # model was never told the three bans. Here LP v1.1 carried the register at authoring
    # and the model still broke it 3 times in 48 bands: better than SS·secondary's 9 under
    # v1.10, and still not zero. Prohibition is not enforcement; the machine gate is.
    # Both compacts scan CLEAN — all three hits are in the standard canonical.
    # Every edit below is a pure DELETION: each sentence reads correctly without the struck
    # clause. No text is authored and nothing is replaced.
    # ── S4 · mathematics · secondary · IX ch 4 "Exploring Algebraic Identities" (2026-08-08) ──
    # SIX forward references, ZERO clock quantities — a distribution no earlier stage produced.
    # SS·VIII was 3 forward / 4 clock, science·IX was 1 forward / 2 clock. Here the clock ban
    # held perfectly across 132 bands and the forward ban failed six times, five of them in the
    # standard canonical. p08 scans CLEAN.
    #
    # WHY, and it is worth recording because it points at the BRIEF rather than the model:
    # every hit is a pedagogical SIGNPOST, not the boilerplate the ban's examples name. None says
    # "in the next period"; they say "the companion identity to be derived in the factorisation
    # unit", "the following unit will formalise", "that is the subject of the next unit". The
    # register block (LP v1.1, present at authoring) and the brief's self-containment bullet both
    # forbid this, so prohibition-with-examples was not the gap — the gap is that neither text
    # says what to write INSTEAD when a unit genuinely ends mid-idea, and a model with teaching
    # instincts fills that silence with a promise.
    #
    # Two hits deserve their own note. U13's "Preview that the synthesis unit will connect all
    # such proof moves" is the model PARAPHRASING ITS OWN BRIEF: the standard brief tells it, in
    # detail, that unit 14 exists and draws the chapter together, then forbids mentioning it —
    # and U13 is the unit immediately before it. U10's "Preview:" is a formatting convention the
    # model invented; nothing in either text uses that word.
    #
    # All six are pure DELETIONS. Every sentence reads correctly without the struck clause and no
    # text is authored. Note edit 6 deliberately removes only the two forward words rather than
    # the sentence: the self-study book_ref pointer it carries is something LP Rule 10 explicitly
    # invites, so striking the whole sentence would delete compliant pedagogy to fix a register
    # breach.
    ("mathematics", "ix"): {
        "ch_04_canonical.json": [
            (2, "band:3",
             ", previewing the companion identity to be derived in the factorisation unit", "",
             "register/forward",
             "the b -> -b substitution and writing the result on the board IS the teaching act "
             "and closes on its own ground. Naming what a later unit derives is false for any "
             "teacher whose X ends here, and for any class that borrowed this unit as its "
             "closing sitting"),
            (5, "teacher_notes",
             " that the following unit will formalise symbolically", "",
             "register/forward",
             "the note's point — the tile model gives concrete meaning to the abstract "
             "middle-term split — is complete without it. The relative clause is the only "
             "forward element in the field; the misconception warning and the no-book_ref "
             "statement after it both stand untouched"),
            (7, "band:2",
             "—that is the subject of the next unit", "",
             "register/forward",
             "'Record the pattern without proving the general case' is a legitimate and "
             "deliberate stopping point — the think-and-reflect prompt asks students to test "
             "x^4-y^4 and x^5-y^5, not to prove. Leaving the generalisation open is correct; "
             "promising who closes it is not"),
            (10, "band:3",
             " Preview: the next unit extends this to factorisation of the same breadth.", "",
             "register/forward",
             "trailing sentence on a consolidation band. The share-and-record move is the "
             "whole activity. This is also the 'Preview:' convention the model invented, which "
             "appears nowhere in the constitution or the brief"),
            (13, "band:3",
             " Preview that the synthesis unit will connect all such proof moves across the "
             "chapter.", "",
             "register/forward",
             "the proof-steps consolidation closes cleanly at 'collect terms, conclude'. This "
             "is the brief-paraphrase hit: the standard brief describes unit 14 to the model in "
             "detail and then bans naming it, and this is the unit immediately before it"),
        ],
        "ch_04_canonical_p11.json": [
            (7, "teacher_notes",
             " before the next unit", "",
             "register/forward",
             "the ONLY hit in either compact. Deleting just these three words leaves 'Students "
             "who want to see a further application can read Example 15, p.85 independently' — "
             "an optional self-study book_ref pointer, which LP Rule 10 explicitly invites. "
             "Striking the whole sentence would remove compliant pedagogy to fix a register "
             "breach, so the timing phrase alone goes"),
        ],
    },
    ("science", "ix"): {
        "ch_08_canonical.json": [
            (5, "band:3",
             " — that rule is the subject of a later unit", "",
             "register/forward",
             "the Bohr consolidation names the open question — how many electrons a shell "
             "holds — which is the teaching act and stands alone. Promising that a LATER "
             "unit answers it is false for any teacher whose X ends at this unit, and for "
             "any class that borrowed this unit as its closing sitting"),
            (7, "band:0",
             " for three minutes", "",
             "register/clock",
             "the IUPAC symbol-invention task is 'work individually', which is the "
             "instruction; the platform scales this band's minutes to whatever sitting "
             "carries it, so a stated three minutes is silently falsified"),
            (12, "band:0",
             " for five minutes", "",
             "register/clock",
             "same pattern in the synthesis unit's opening — 'students work individually "
             "listing everything they would need to know' is complete and unfalsifiable; "
             "the number is not"),
        ],
    },
}

DEFAULT_SET = ("social_sciences", "viii")


def _get_set(unit, locator, new=None):
    """Read (new=None) or write the located string on a unit."""
    if locator == "teacher_notes":
        if new is None:
            return unit.get("teacher_notes", "")
        unit["teacher_notes"] = new
    elif locator.startswith("band:"):
        b = unit["time_bands"][int(locator.split(":")[1])]
        if new is None:
            return b.get("activity", "")
        b["activity"] = new
    elif locator.startswith("homework:"):
        i = int(locator.split(":")[1])
        if new is None:
            return unit["homework"][i]
        unit["homework"][i] = new
    else:
        raise SystemExit(f"unknown locator {locator}")
    return None


def apply_file(lib, fname, edits, dry):
    path = lib / fname
    if not path.is_file():
        raise SystemExit(f"missing: {path}")
    plan = json.loads(path.read_text(encoding="utf-8"))
    units = {u["period_number"]: u for u in plan["result"]["lesson_plan"]["periods"]}
    before = len([h for h in scan_plan(plan) if h["ban"]])
    done = []
    for unit_no, loc, old, new, rule, note in edits:
        u = units.get(unit_no)
        if u is None:
            raise SystemExit(f"{fname}: no unit {unit_no}")
        cur = _get_set(u, loc)
        if old not in cur:
            raise SystemExit(
                f"{fname} U{unit_no} {loc}: declared text not found — the artefact has changed "
                f"since this repair was written. Re-read it, do not force.\n  wanted: {old!r}")
        if not dry:
            _get_set(u, loc, cur.replace(old, new, 1))
        done.append({"unit": unit_no, "field": loc, "rule": rule,
                     "removed": old.strip(), "replaced_with": new.strip(), "note": note})
    after_hits = [h for h in scan_plan(plan) if h["ban"]]
    if not dry:
        gc = plan.setdefault("genon_canonical", {})
        gc.setdefault("repairs", []).append({
            "at": datetime.now().isoformat(timespec="seconds"),
            "tool": "genon/repair_register.py v1.4",
            "reason": "register backfill (founder ruling 2026-08-02; testing.md C3 / ARV-D-011..013, ARV-D-026)",
            "edits": done,
            "ban_hits_before": before, "ban_hits_after": len(after_hits),
        })
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return before, len(after_hits), done, plan


def _arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    dry = "--apply" not in sys.argv
    subject = _arg("--subject", DEFAULT_SET[0])
    grade = _arg("--grade", DEFAULT_SET[1])
    key = (subject, grade)
    if key not in REPAIRS:
        raise SystemExit(f"no declared repair set for {key}; have {sorted(REPAIRS)}")
    repairs = REPAIRS[key]
    lib = SAVED / subject / grade
    print(f"repair set {subject} {grade} -> {lib.relative_to(REPO)}/")
    if not dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        for fname in repairs:
            shutil.copy2(lib / fname, BACKUP / f"{grade}_{fname[:-5]}_{ts}.json")
        print(f"backed up {len(repairs)} file(s) -> {BACKUP.relative_to(REPO)}/")
    total_after = 0
    for fname, edits in repairs.items():
        before, after, done, plan = apply_file(lib, fname, edits, dry)
        total_after += after
        print(f"\n=== {fname} — {len(done)} edit(s); ban hits {before} -> {after}"
              f"{' (DRY RUN, nothing written)' if dry else ''}")
        for d in done:
            print(f"  U{d['unit']:<3} {d['field']:<16} [{d['rule']}]")
            print(f"        - {d['removed']}")
            if d['replaced_with']:
                print(f"        + {d['replaced_with']}")
        if after:
            report([h for h in scan_plan(plan) if h["ban"]], f"{fname} SURVIVING")
    print(f"\nTOTAL surviving ban hits across the library: {total_after}")
    # A repaired canonical invalidates every plan derived from it (ARV-D-034): the serve cache
    # keys on the canonical's ledger_ts, which a repair does not change, so a stale plan would
    # otherwise keep being served. Rebuilding one costs ~11 ms.
    if not dry:
        chapters = sorted({int(f.split("_")[1]) for f in repairs})
        for ch in chapters:
            purge(subject, grade, ch, reason="genon/repair_register.py")
    if dry:
        print("dry run — re-run with --apply to write.")
    return 1 if total_after else 0


if __name__ == "__main__":
    sys.exit(main())
