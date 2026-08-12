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

v1.5, 2026-08-09 (S4): ch 4 was RE-AUTHORED (corrected summary + LP v1.2 + 15 periods), so the
v1.4 declarations are void — their text lives in an archived file. They are kept under a
3-tuple SUPERSEDED key as the cost record and replaced, at the live 2-tuple key, by the
re-author's two hits. Forward references fell 5 -> 2 on a plan one unit LONGER, which is the
first evidence that the summary fix reduces register pressure rather than just relabelling it.
A third scanner hit was a false positive and was fixed at source instead: "the square root of
the last term" is a polynomial term, and register_scan.py now treats "last term" as advisory.
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
    # ── S4 · mathematics IX ch 4, THE RE-AUTHORED LIBRARY (2026-08-09) ────────────
    # The 2026-08-08 library was superseded: its summary attributed all nine end-of-chapter
    # items to 4.1, so three consolidation units wore the "Introduction" label. With the
    # summary corrected the model produced no consolidation units at all — it spent the extra
    # period deepening sections instead — and the plan runs monotonically 4.1 -> 4.8 + synthesis.
    #
    # FORWARD REFERENCES FELL 5 -> 2 across that change, on a plan one unit LONGER. Both
    # survivors are the same construction as before: a trailing clause promising what a later
    # unit will do. Both are pure deletions; the sentence carries its teaching point without
    # the promise. A third scanner hit was a FALSE POSITIVE and is fixed at source rather than
    # repaired here — U3's "the square root of the last term" is a polynomial term, and
    # register_scan.py's calendar pattern now treats "last term" as advisory (v1.1, same day).
    # LIVE set — only what is still UNAPPLIED. The top's two edits were applied at 10:02, before
    # the resume bought the compacts, so they now sit under the APPLIED key below: leaving them
    # here would make the whole set fail its own "declared text not found" guard on the first
    # edit and block the p12 repair. Once applied, a declaration is a record, not an instruction.
    ("mathematics", "ix"): {
        "ch_04_canonical_p12.json": [
            (9, "band:3",
             " for the next unit's work", "",
             "register/forward",
             "the inspect-and-identify move on two of End of Chapter Q3's expressions is "
             "complete in itself, and recording the identifications is good practice whether or "
             "not anything follows. At 12 units this unit can be somebody's last sitting — the "
             "sweep serves X=12 as an identity and X=13 as a fill off this plan — so promising "
             "a next unit's work is false for those classes"),
        ],
    },

    # ── APPLIED 2026-08-09 10:02 to the re-authored top, before the compacts existed.
    #    Kept as the record; re-running would fail the guard, which is the guard working.
    ("mathematics", "ix", "APPLIED-top-20260809"): {
        "ch_04_canonical.json": [
            (7, "band:3",
             " — that follows in the next unit", "",
             "register/forward",
             "the algebra-tile band closes on its own ground: the general form (px+a)(qx+b) is "
             "NOTED without full development, which is the teaching decision. Naming where the "
             "development happens is false for any teacher whose X ends here, and for any class "
             "that borrowed this unit as its closing sitting"),
            (10, "band:3",
             " for the next unit", "",
             "register/forward",
             "raising the (x-y)-as-a-factor question as a conjecture is the whole move, and the "
             "think-and-reflect prompt is deliberately left open (LP Rule 4 folds it into the "
             "period). 'raised as a conjecture' stands; who resolves it is not this unit's to say"),
        ],
        # The compacts, added after the 2026-08-09 resume bought p12 and p09. p09 scanned
        # CLEAN; p12 carried one hit, of the same family as the top's two.
        "ch_04_canonical_p12.json": [
            (9, "band:3",
             " for the next unit's work", "",
             "register/forward",
             "the inspect-and-identify move on two of End of Chapter Q3's expressions is "
             "complete in itself, and recording the identifications is good practice whether or "
             "not anything follows. At 12 units this unit can be somebody's last sitting — the "
             "sweep serves X=12 as an identity and X=13 as a fill off this plan — so promising "
             "a next unit's work is false for those classes"),
        ],
    },

    # ── SUPERSEDED — applied 2026-08-08 to the library now in
    #    backup/superseded_libraries/mathematics_ix_ch04_20260809_094739/. Kept as the record of
    #    what that library cost in repairs (5 forward refs in the top, 1 in p11, 0 clock
    #    quantities across 132 bands). These declarations must NEVER be re-run: their text lives
    #    in an archived file, and the key they were stored under now holds the re-author's set.
    ("mathematics", "ix", "SUPERSEDED-20260808"): {
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
    # ── v1.6, 2026-08-12 · S5 · the_world_around_us · preparatory · WAVE 1 of the corpus ──
    # Eleven hits across ten of the 31 standards authored in the first Message-Batches wave
    # (batch msgbatch_01Exqedy…, ₹438.72). Composition: 5 clock quantities, 4 calendar
    # references, 1 completion phrase, 1 forward reference. FOUNDER RULING 2026-08-12:
    # back-fill ALL ELEVEN, including the two I read as false positives — a library that
    # scans to zero is a cleaner invariant than one carrying three standing "known and
    # accepted" hits that every future certification re-raises.
    #
    # All eleven are PURE DELETIONS. No sentence is rewritten, no clause invented; each one
    # reads correctly with the offending words struck, which is what the ban asks for.
    #
    # Two are worth naming because they are NOT the boilerplate the bans' examples describe:
    #   * v ch09 U3 is the only structurally real one — the teacher note points at "the globe
    #     task on Textbook p. 151", which lives in U4. X varies, so a class served 11 or 8
    #     units never reaches it and the bridge dangles. Same family as ARV-D-119.
    #   * v ch08 U3's "now that students have seen threads up close" refers to THIS unit's own
    #     6-24 band, so nothing is assumed about another unit. Repaired under the ruling above,
    #     recorded here as scanner-shape rather than dependency, so the corpus statistics do
    #     not learn a defect that was not one.
    # The four calendar hits are classroom talk ("could you do this tomorrow?"), not scheduling
    # claims — but the Calendar Purge is absolute and the fix is one word each.
    ("the_world_around_us", "iii", "SUPERSEDED_wave1_applied_20260812"): {
        "ch_11_canonical.json": [
            (16, "band:4",
             " this week", "",
             "register/calendar",
             "'ask one elder at home about one object' is the whole task; the week is a "
             "calendar Aruvi does not model and cannot honour"),
        ],
    },
    ("the_world_around_us", "iv", "SUPERSEDED_wave1_applied_20260812"): {
        "ch_04_canonical.json": [
            (11, "band:2",
             " this week", "",
             "register/calendar",
             "'Is this action something we could actually do?' is the question; feasibility "
             "does not need a week to be a real question"),
        ],
        "ch_08_canonical.json": [
            (6, "band:2",
             "the easiest to start tomorrow?", "the easiest to start?",
             "register/calendar",
             "the reflection is about ease, not timing; 'tomorrow' is unknowable at authoring"),
            (11, "band:1",
             " do tomorrow?", " do?",
             "register/calendar",
             "same family, same unit's group discussion — 'could you actually do this?' "
             "carries the whole pedagogical intent"),
        ],
        "ch_09_canonical.json": [
            (9, "band:2",
             " for a few minutes", "",
             "register/clock",
             "'students work in pairs, then share with the class' is the instruction; the "
             "band's own 20-32 minutes carry the time and are rescaled per sitting"),
        ],
    },
    ("the_world_around_us", "v", "SUPERSEDED_wave1_applied_20260812"): {
        "ch_01_canonical.json": [
            (12, "band:0",
             " for two minutes", "",
             "register/clock",
             "the architect prompt and the board-notes list stand alone; a stated two minutes "
             "is falsified the moment the unit is served at any other duration"),
        ],
        "ch_04_canonical.json": [
            (7, "band:0",
             " for two minutes", "",
             "register/clock",
             "'brainstorm individually, then share ideas with a partner' is complete"),
        ],
        "ch_06_canonical.json": [
            (15, "band:0",
             " for 2–3 minutes", "",
             "register/clock",
             "'write without stopping' IS the instruction — the urgency is in the phrasing, "
             "not the number (note the en dash: a ranged quantity, ARV-D-026's shape)"),
        ],
        "ch_08_canonical.json": [
            (3, "band:3",
             " now that students have seen threads up close", "",
             "register/completion",
             "SCANNER SHAPE, NOT A DEPENDENCY: the magnifying-glass examination is this same "
             "unit's 6-24 band, so nothing about another unit is assumed. Struck under the "
             "2026-08-12 all-eleven ruling; 'asks what that phrase might mean' is unchanged "
             "teaching"),
        ],
        "ch_09_canonical.json": [
            (3, "teacher_notes",
             " This bridges to the globe task on Textbook p. 151 and keeps the inquiry open.", "",
             "register/forward",
             "THE ONE STRUCTURALLY REAL HIT. The globe task is U4; a class served 11 or 8 "
             "units never reaches it. The question before it — 'when it is night here, what "
             "is happening on the other side of the Earth?' — is exactly the open inquiry "
             "the deleted sentence claimed to keep open, and the inclusivity note that "
             "follows is untouched"),
        ],
        "ch_10_canonical.json": [
            (7, "band:1",
             " for a few minutes", "",
             "register/clock",
             "'students discuss in pairs, then share with the class' is the instruction; the "
             "sugar-and-chilli connection at the end of the band is untouched"),
        ],
    },
    # ── v1.7, 2026-08-12 · S5 · the_world_around_us · WAVE 2 (the 59 compacts) ───────
    # 21 hits after one scanner fix (below), across 16 compact files. Composition: 9 clock,
    # 7 calendar, 4 forward, 1 completion — the same families as wave 1, at a similar rate
    # (10 of 31 tops, 16 of 59 compacts). All pure deletions.
    #
    # ONE HIT WAS FIXED AT SOURCE INSTEAD, and it matters: iv ch03 p10 U9 "half the class
    # will be plants and animals, the other half will be forest visitors" is a GROUPING, not
    # a clock quantity. register_scan's `half the (session|period|class)` pattern was written
    # for session length and "class" is a homonym. Repairing it would have struck correct
    # pedagogy to satisfy a regex, so "half the class" is now ADVISORY in register_scan.py —
    # the S4 "last term" treatment. 22 ban hits became 21.
    #
    # Two are worth reading rather than skimming:
    #   * iv ch07 p11 U8 "Boats are kept safe on desks for the exhibition in the following
    #     unit" — the ARV-D-119 family again, now pointing FORWARD: on a short serve the
    #     exhibition never happens and the boats wait for nothing.
    #   * iv ch06 p15 U2 "Now that we have seen who helps the grain" — completion language
    #     about a PRIOR unit's activity. The sentence's own opening already says the teacher
    #     revisits earlier board words, which is a legal backward reference; only the
    #     completion claim goes.
    ("the_world_around_us", "iii"): {
        "ch_03_canonical_p06.json": [
            (6, "band:4", " for one or two minutes", "", "register/clock",
             "the gallery walk is the activity; its band carries 35-40 and is rescaled"),
        ],
        "ch_03_canonical_p08.json": [
            (8, "teacher_notes", " tomorrow", "", "register/calendar",
             "'if a new student joined your school and could not read the signs' is the "
             "whole thought experiment; the day is not part of it"),
        ],
        "ch_04_canonical_p08.json": [
            (3, "teacher_notes", " this week", "", "register/calendar",
             "'ask which grains the children ate' — the grain-grass discovery needs no week"),
        ],
        "ch_05_canonical_p08.json": [
            (7, "band:0", " for a few minutes", "", "register/clock",
             "'students discuss in pairs, recalling what they have observed' stands"),
        ],
        "ch_12_canonical_p13.json": [
            (4, "band:1", " for a few minutes", "", "register/clock",
             "'groups talk, then a speaker shares one idea' is the instruction"),
            (6, "band:3", " this week", "", "register/calendar",
             "'which of these will I try?' is the private commitment; the week narrows it "
             "to a calendar the platform does not model"),
        ],
    },
    ("the_world_around_us", "iv", "SUPERSEDED_wave2_applied_20260812"): {
        "ch_01_canonical_p06.json": [
            (4, "band:1", " for two minutes", "", "register/clock",
             "'students think quietly, then share in groups of three' is complete"),
        ],
        "ch_03_canonical_p13.json": [
            (3, "band:3", " as a bridge to the section's content on water-dwelling animals",
             "", "register/forward",
             "the naming task and the reflective question that follows are the teaching; "
             "the bridge promises content this serve may not reach"),
        ],
        "ch_06_canonical_p11.json": [
            (5, "band:0", " for a quiet two minutes", "", "register/clock",
             "'observe the park scene picture without talking' keeps the quiet instruction "
             "and drops only the quantity"),
        ],
        "ch_06_canonical_p15.json": [
            (2, "band:0", "Now that we have seen who helps the grain, let's think",
             "Let's think", "register/completion",
             "the band already opens by revisiting earlier board words — a legal backward "
             "reference. Only the completion claim goes"),
            (6, "band:3", " this week", "", "register/calendar",
             "'one specific change they will make in how they handle food at home' is the "
             "commitment"),
        ],
        "ch_07_canonical_p11.json": [
            (8, "band:4", " Boats are kept safe on desks for the exhibition in the following unit.",
             "", "register/forward",
             "ARV-D-119's shape pointing forward: on a short serve the exhibition never "
             "comes. The notebook note is the unit's own closing act"),
        ],
        "ch_10_canonical_p08.json": [
            (7, "band:2", " without claiming the chapter is complete", "",
             "register/completion",
             "authorial aside to the teacher; the consolidation sentence reads better "
             "without a disclaimer about completeness"),
        ],
    },
    # p11 was in QUARANTINE when the wave-2 set ran (first-visit order, ARV-D-1xx), so its
    # own calendar hit could not be repaired with its siblings. Restored and reordered by
    # repair_unit_order.py the same day; its unit numbering shifted, so the hit that the
    # certification report showed at U9 is now U8 — declared here against the CURRENT file.
    ("the_world_around_us", "iv"): {
        "ch_08_canonical_p11.json": [
            (8, "band:1", " tomorrow morning", "", "register/calendar",
             "'what exactly will you do differently?' is the prompt that makes a vague step "
             "specific; the morning is a calendar Aruvi does not model"),
        ],
    },
    ("the_world_around_us", "v", "SUPERSEDED_wave2_applied_20260812"): {
        "ch_01_canonical_p08.json": [
            (3, "band:1", " for a few minutes", "", "register/clock",
             "'students watch the inside of the bag and begin filling the I Observe column'"),
        ],
        "ch_01_canonical_p11.json": [
            (10, "band:2", " for a few minutes", "", "register/clock",
             "'pairs discuss, then share' — the scribing that follows is the real content"),
        ],
        "ch_02_canonical_p13.json": [
            (8, "band:2", " this week", "", "register/calendar",
             "'at least one action they could start, not just in principle' keeps the "
             "concreteness the week was carrying"),
            (9, "band:3", " These notes will be used in the role-play in the next unit of work on this section.",
             "", "register/forward",
             "the note-taking is complete in itself; the role-play may be a unit this "
             "class never reaches"),
        ],
        "ch_04_canonical_p10.json": [
            (9, "band:3", " this week", "", "register/calendar",
             "'one behaviour they will practise in school' is the commitment"),
        ],
        "ch_04_canonical_p13.json": [
            (11, "band:1", " for two minutes", "", "register/clock",
             "'students think individually, then write their action on their leaf shape'"),
        ],
        "ch_09_canonical_p07.json": [
            (3, "band:3", " The chart remains posted on the wall for the following unit.",
             "", "register/forward",
             "leaving the chart up is fine; SAYING it is for the following unit is the "
             "breach, because there may not be one"),
        ],
        "ch_09_canonical_p10.json": [
            (5, "band:3", " before the next unit's work", "", "register/forward",
             "'a brief oral pause that plants the idea of seasonality' is the whole move"),
        ],
    },
}

DEFAULT_SET = ("social_sciences", "viii")


# The teacher-note field is NOT called the same thing on every stage (2026-08-12, S5): SS
# carries `teacher_notes`, TWAU carries `teacher_facilitation_note`. Reading only the first
# returns "" on TWAU, which surfaces as "declared text not found" — a repair refused for a
# reason that has nothing to do with the text. Same shape as the carrier seams in validate()
# and the certifier: ask which field this artefact actually uses.
_NOTE_FIELDS = ("teacher_notes", "teacher_facilitation_note")


def _note_field(unit) -> str:
    for f in _NOTE_FIELDS:
        if f in unit:
            return f
    return _NOTE_FIELDS[0]


def _get_set(unit, locator, new=None):
    """Read (new=None) or write the located string on a unit."""
    if locator == "teacher_notes":
        f = _note_field(unit)
        if new is None:
            return unit.get(f, "")
        unit[f] = new
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
            "tool": "genon/repair_register.py v1.5",
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