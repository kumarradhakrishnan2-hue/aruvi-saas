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
# field_locator: "teacher_notes" | "band:<index>" | "homework:<index>" | "materials:<index>"
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
    # ── S2 · social_sciences · MIDDLE · BATCH WAVE 2 (the COMPACTS) — 2026-08-16 ──────
    # 80 compacts bought for Rs 1,422.83 (msgbatch_011ezdQUpviWiYgZmANzzDp4) plus a Rs 28.17
    # re-author of viii ch 15 p14. 134 ban hits over 59 of 143 installed files — 2.3/file,
    # statistically identical to wave 1's 2.25, so the compacts are no worse behaved than the
    # standards they were cut from.
    #
    # DISTRIBUTION: 58 clock / 57 forward / 9 completion / 6 meta-leak / 4 calendar. Two shifts
    # against wave 1 worth recording: COMPLETION goes 1 -> 9, which is what a compact does — it
    # asserts "having worked through every section" on a plan that by construction carries
    # fewer of them; and meta-leak persists at 6 (wave 1: 10), confirming ARV-D-161 is a
    # brief-side habit rather than a one-off draw.
    #
    # FIVE HITS ARE DELIBERATELY NOT DECLARED: the four [calendar] hits (question content, not
    # the teacher's calendar — founder ruling 2026-08-16 to leave them) and viii ch 9 U11's
    # "fired approximately 1,650 rounds FOR ABOUT TEN MINUTES", the duration of the Jallianwala
    # Bagh massacre (ARV-D-162). Those five keep the library census at 5 rather than 0.
    #
    # TWO SPANS WERE NARROWED BY HAND after review, both because the mechanical sentence-span
    # would have deleted teaching rather than a clause: viii ch 4 p15 U14 (the cut removed the
    # comparison task's setup and orphaned "For each they record…") and viii ch 7 p07 U6 (it
    # removed the 2025 mobile-manufacturing fact along with the bridge phrase).
    ("social_sciences", "vi"): {
        # WAVE 2 · 48 edits across 21 file(s)
        "ch_02_canonical_p09.json": [
            (6, "teacher_notes",
             "The contradiction question at the close is deliberately left open: it plants the environmental concern the next unit develops.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ource; the reading annotation makes the "
             "chapter's claim explicit and memorable.…"),
            (8, "band:1",
             " for about eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …but others do not, does it help? What kind of action is needed?' "
             "Groups discuss, then each group nominates a spokesperson to share one key…"),
        ],
        "ch_02_canonical_p12.json": [
            (9, "band:0",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …imate, for life, for people?' Students write their initial "
             "thoughts individually, then share one idea each in a brief whole-class round.…"),
        ],
        "ch_03_canonical_p10.json": [
            (7, "band:2",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …rom irrigation today, and who will face the cost tomorrow?' "
             "Small groups discuss, then share. Teacher draws out the idea that the same techn…"),
        ],
        "ch_03_canonical_p14.json": [
            (10, "band:3",
             "Teacher notes two or three strong responses to read aloud at the start of the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …xplain why these uses together make "
             "rivers central to plains life and culture.'…"),
            (13, "band:1",
             " — confirmed or reclassified now that you have seen it on the map?",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …ssify each: 'The Amazon Basin — mountain, plateau, or plain? "
             "The Tibetan Plateau The Andes — how does the map show they are a range rather t…"),
        ],
        "ch_04_canonical_p09.json": [
            (4, "teacher_notes",
             "The cross-checking discussion at the end is essential preparation for the artefact analysis activity in the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …use they carry written records, distinct "
             "from the broader manuscript tradition.…"),
            (7, "teacher_notes",
             "The comparison with the rock shelter keeps the earlier unit's content live without requiring that unit to have happened.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist | survives: "
             "…gger that made settled life possible in many parts of the world simultaneously.…"),
            (8, "band:3",
             " — a thread the next chapter will pick up.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …es this early progress as preparing the "
             "ground for the emergence of civilisation.…"),
        ],
        "ch_04_canonical_p12.json": [
            (8, "band:3",
             " — to be developed in the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …This plants the question of how social "
             "complexity increases as communities grow.…"),
            (8, "teacher_notes",
             "The collective ownership question at the close connects prehistoric social arrangements to lived experience and sets up the social complexity discussion in the following unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ns form → agriculture becomes possible) "
             "that stretched over thousands of years.…"),
        ],
        "ch_05_canonical_p08.json": [
            (2, "band:1",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …that old, rather than from a map or an inscription?' In pairs, "
             "students discuss, then share. The teacher steers discussion toward the idea…"),
            (6, "teacher_notes",
             "The timeline activity at the close gives students a compact record of the full arc of Indian self-naming they have built across the chapter.",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …the name carries a historically documented geographical and "
             "cultural identity.…"),
        ],
        "ch_06_canonical_p14.json": [
            (9, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …ings that seem to have cultural or symbolic meaning.' Students "
             "sort individually, then compare their groupings with a neighbour. Teacher not…"),
            (14, "teacher_notes",
             "Having worked through all the chapter's content sections, this unit consolidates the source-reading skill that runs through the chapter by presenting six sources of different types together and asking students to reason across them.",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …A common confusion is treating source type as irrelevant — "
             "that all sources are equally useful for all questions; the paired comparison tas…"),
        ],
        "ch_06_canonical_p19.json": [
            (8, "teacher_notes",
             "; the next unit will take up the cultural and symbolic objects from the same section, so this division is intentional and content-driven.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …This unit focuses on everyday objects. "
             "Students often treat stone weights as uninteresting; redirect their attention to "
             "the inference: stand…"),
            (9, "band:3",
             ", raising the question the chapter will take up: when a civilisation 'ends,' does its culture truly disappear?",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ka, the namaste, and the thirsty crow "
             "story all appear in South Asian life today…"),
        ],
        "ch_07_canonical_p18.json": [
            (4, "teacher_notes",
             ", which the next unit will exploit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …of abstraction — the chapter itself uses "
             "stories to make these ideas accessible.…"),
            (6, "band:0",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …that element contributed to the foundations of Hinduism. They "
             "work individually, then compare with a neighbour.…"),
            (9, "band:1",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …ate yajña ritual, the specific framework of brahman-ātman). "
             "Working individually, they then compare with a partner and reconcile differences…"),
            (9, "teacher_notes",
             "The analytical question about diversity of intellectual traditions foreshadows the chapter's broader argument about India's cultural roots.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …prevent this by forcing students to look "
             "for both similarities and differences.…"),
            (10, "band:1",
             " for seven minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …example of how a person might apply it in daily life. Students "
             "work individually, then compare examples with a partner.…"),
        ],
        "ch_08_canonical_p11.json": [
            (6, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Students examine Fig. 8.6 silently, then write in their "
             "notebooks: 'Which story do you think this painting depicts? What details in the "
             "imag…"),
        ],
        "ch_09_canonical_p09.json": [
            (3, "band:1",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …e in action — use situations you have actually seen or "
             "experienced.' Groups work, then each group shares one example; the teacher maps "
             "examp…"),
            (6, "teacher_notes",
             ", which prepares students for the halma and Kamal Parmar examples in the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ically important: it establishes that "
             "communities generate governance structures.…"),
            (9, "band:1",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …al role — your group prepares his response. Each group role- "
             "plays their scenario, then writes two sentences in their notebooks: the value en…"),
        ],
        "ch_09_canonical_p12.json": [
            (4, "teacher_notes",
             ", which the Tenzing story in the next unit complicates.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ussion seeds the distinction between "
             "internalised values and external obligation.…"),
            (12, "teacher_notes",
             "The structured argument paragraph brings the chapter's main analytical threads together without requiring students to have been through every prior unit.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist | survives: "
             "…ly the Tenzing story's depiction of a joint family that is anything but static.…"),
        ],
        "ch_10_canonical_p09.json": [
            (2, "teacher_notes",
             "The annotation task in the final minutes gives students a personal record of the three-organ framework they will apply in later units.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …n the law (police, implementation) while "
             "the judiciary reviews and adjudicates.…"),
            (4, "teacher_notes",
             "; use the Kalam biographical feature introduced in a later unit to preview that even a nominal head can make a significant impact through influence and inspiration.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ter the formal table. A common confusion "
             "is treating 'nominal head' as powerless. The quick-fire function-sorting at the "
             "close consolidates…"),
            (7, "teacher_notes",
             "The table at the close gives students a structured record that also prepares them for the grassroots democracy concept in the following unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …accountable to voters and that the vote "
             "is itself an exercise of citizen power.…"),
        ],
        "ch_10_canonical_p12.json": [
            (2, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …und a single Governance centre rather than one organ at the "
             "top?' Groups discuss, then share. Introduce separation of powers and checks and…"),
            (7, "band:1",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …lly. Which Central functions and resources can you deploy?' Each "
             "group discusses and records three decisions on their decision sheet, citing…"),
            (9, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …e question they have about their partner's answer. Pairs discuss "
             "their questions.…"),
            (10, "band:3",
             "Collect as an ongoing check of understanding before the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …affects the life of an ordinary person in "
             "India.' Students write independently.…"),
            (11, "band:2",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …tes one challenge or question in the margin. Pairs then discuss "
             "their challenges. Bring the class together and collect one strong point and…"),
        ],
        "ch_11_canonical_p11.json": [
            (2, "band:1",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …help us understand the past and the present?' Students first "
             "write individually — possible answers include tracing changes in land ownershi…"),
            (10, "band:0",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …and how it connects to the tier above and below it.' Students "
             "work individually. Teacher circulates to see what students recall fluently an…"),
        ],
        "ch_11_canonical_p15.json": [
            (3, "band:3",
             " — teacher scans responses to gauge understanding before the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ntences in their notebooks: 'The Gram "
             "Sabha matters to rural democracy because…'.…"),
            (7, "teacher_notes",
             "The pair task prepares students for the simulation in the following unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …children versus doing something "
             "structurally responsive — push the distinction.…"),
            (15, "band:0",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …? — what evidence would you give on each side?' Students "
             "brainstorm individually, listing evidence for and against, then share briefly in "
             "pa…"),
        ],
        "ch_12_canonical_p11.json": [
            (7, "teacher_notes",
             " — helps students see the systematic logic of Indian local governance without requiring those units to have been covered in this class.",
             ".",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist | survives: "
             "…side, so noting that parallel — Gram Panchayat, Panchayat Samiti, Zila Panchayat. "
             "A common confusion is thinking that a smaller body like a…"),
        ],
        "ch_13_canonical_p07.json": [
            (1, "teacher_notes",
             "Encouraging students to share their 'hardest to classify' case before the close surfaces the precise boundary the next unit will draw.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …eatly; draw out that significance and "
             "monetary exchange are separate questions.…"),
        ],
        "ch_14_canonical_p05.json": [
            (5, "teacher_notes",
             "Drawing on the AMUL interdependence model and the three-sector definitions built across this chapter, this unit moves from a named case study to the students' own economic environment, making the classification framework personally relevant.",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …A frequent difficulty is students listing only tertiary "
             "activities when they think of their neighbourhood (shops, transport, services) "
             "whil…"),
        ],
        "ch_14_canonical_p07.json": [
            (1, "teacher_notes",
             "The criteria brainstorm at the close sets up the next unit's classification work without pre-empting it.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …her child an economic activity if she is "
             "also a nurse?') surfaces this cleanly.…"),
            (2, "band:3",
             "The teacher collects these slips to gauge understanding before the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …r neighbourhood — and assigns it to a "
             "sector with a one-sentence justification.…"),
            (4, "band:2",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …m the primary sector, and write the finished product. Students "
             "work individually, then share in a quick round-robin. The teacher records nov…"),
            (4, "band:3",
             "; three responses are read aloud to bridge toward the interdependence theme.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ector clothing industry if cotton farming "
             "collapsed. Students write one sentence.…"),
        ],
    },
    ("social_sciences", "vii"): {
        # WAVE 2 · 28 edits across 13 file(s)
        "ch_02_canonical_p05.json": [
            (5, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …claim that needs stronger support from the text. Writers revise "
             "their paragraph based on the partner's marks. Final paragraphs are handed t…"),
        ],
        "ch_02_canonical_p07.json": [
            (1, "teacher_notes",
             "The index-card web is a light diagnostic of prior knowledge and sets up instrument study in later units.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …nal section will show how accumulated "
             "weather data connects to longer patterns.…"),
        ],
        "ch_03_canonical_p17.json": [
            (2, "teacher_notes",
             " — the Western Ghats will be explained as a topographic factor in a later unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …tween Mumbai's tropical wet coast and the "
             "Deccan Plateau immediately to the east.…"),
            (6, "teacher_notes",
             " — a bridge to the monsoon unit ahead.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ht that sea-origin winds are the "
             "mechanism linking wind to moisture and rainfall. The two-factor Rajasthan analysis "
             "invites students to see…"),
        ],
        "ch_04_canonical_p11.json": [
            (6, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …better, lighter, sharper tools make to a farmer? To a soldier?' "
             "They brainstorm and share. The teacher records key words (heavier harvests,…"),
            (8, "band:0",
             ", and the unit will examine both.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ly. The teacher notes that the chapter's "
             "answer involves two interacting systems.…"),
            (11, "teacher_notes",
             "Having worked through all substantive content of the chapter, this unit returns to the chapter itself as an object of analysis, asking students to examine how the text makes historical claims and what evidence underwrites them.",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …A common confusion at this level is treating everything in a "
             "textbook as equally established fact; the excerpts are chosen to represent a r…"),
        ],
        "ch_05_canonical_p11.json": [
            (2, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …ders and craftsmen so that trade actually happens?' Students "
             "brainstorm in pairs, then share. Teacher accepts responses and introduces the w…"),
            (6, "band:3",
             "This closes the founding narrative before the next unit examines the governance philosophy that sustained it.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …cts two contrasting responses and the "
             "class assesses which is better supported.…"),
        ],
        "ch_05_canonical_p15.json": [
            (1, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …s tell us about who holds power and how they hold it?' Students "
             "discuss in pairs, then share observations aloud.…"),
            (8, "band:2",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …what kinds of evidence historians use to reconstruct the past?' "
             "Students discuss, then the teacher draws out the distinction between indigen…"),
            (8, "teacher_notes",
             ", and his Arthaśhāstra will be examined in the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …nals that his expertise in governance and "
             "economics was structural, not tactical. The written comparison must use Dhana "
             "Nanda and Chandragup…"),
            (9, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …name its seven essential parts, what would you include?' "
             "Students suggest ideas. The teacher then has students read the Kauṭilya section "
             "to…"),
        ],
        "ch_06_canonical_p11.json": [
            (3, "teacher_notes",
             "The map-plotting task grounds the trade network spatially before the next unit turns to its social dimensions.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …and toll-cave evidence is the corrective, "
             "and students should reason from both.…"),
        ],
        "ch_07_canonical_p11.json": [
            (2, "band:1",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …a coin tell us that a text might not, and vice versa? Students "
             "work individually, then discuss in groups of three.…"),
        ],
        "ch_09_canonical_p17.json": [
            (10, "teacher_notes",
             ", which will be the focus of the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …y between the ideal of limited kingly "
             "power described here and absolute monarchy.…"),
            (11, "band:0",
             "This links back to the separation-of-powers concept without naming a previous unit — the idea itself does the connecting.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist | survives: "
             "…to the separation of powers?' Students write two sentences on the consequence.…"),
            (14, "band:0",
             " — and says the unit will examine both its ancient and modern forms.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …They write a one-sentence prediction. The "
             "teacher confirms the term — oligarchy.…"),
        ],
        "ch_10_canonical_p15.json": [
            (1, "band:2",
             "— previewing the chapter's inquiry arc without closing any question.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …d under three headings: 'What is it?', "
             "'Why do we need it?', 'How was it made?'…"),
            (15, "band:0",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Rights, Directive Principles, and Fundamental Duties. Students "
             "work individually, then compare with a partner — gaps and disagreements show…"),
        ],
        "ch_11_canonical_p08.json": [
            (6, "band:0",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …his? What might the image tell us about the issuer? Students "
             "write independently, then share one observation each in a quick round.…"),
        ],
        "ch_11_canonical_p11.json": [
            (1, "band:3",
             "; teacher notes responses on the board as a bridge to the problems the barter system creates, which the chapter will explore.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …at might have changed to make them stop "
             "working?' Students propose one idea each.…"),
            (2, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …n getting all three items through barter.' Individuals write "
             "their list silently, then share with a neighbour.…"),
            (7, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …ld traders eventually stop relying on coins alone?' Students "
             "brainstorm in pairs, then share. Teacher lists responses on the board; expected…"),
            (8, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …way the seller could still complete the sale.' Students "
             "brainstorm individually. Collect responses: expected answers include digital "
             "paymen…"),
            (10, "teacher_notes",
             ", asking students to apply the analytical vocabulary built across the chapter to a structured evaluative task — the comparison table format makes the reasoning visible and the recommendation testable.",
             ".",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …This unit draws on the full span of exchange forms the "
             "chapter covers. A common weakness in the recommendation is listing features rather "
             "th…"),
        ],
        "ch_12_canonical_p15.json": [
            (10, "teacher_notes",
             " — a preview of the external effects the next unit addresses.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …it simultaneously benefits the consumer "
             "(electricity bills) and the environment. Weights-and-measures monitoring is a "
             "small but concrete de…"),
            (15, "teacher_notes",
             "This unit asks students to deploy the full consumer quality-assessment toolkit developed across the chapter's closing sections — not introduce new content but apply accumulated knowledge to two fresh scenarios.",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …The cause-effect map for the BEE Star Rating is the "
             "analytical centrepiece: it explicitly connects an individual consumer decision to "
             "envir…"),
        ],
    },
    ("social_sciences", "viii"): {
        # WAVE 2 · 50 edits across 21 file(s)
        "ch_02_canonical_p12.json": [
            (2, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …. Why did it never absorb the entire subcontinent?' Students "
             "brainstorm in pairs, then share. Teacher records responses on the board without…"),
        ],
        "ch_04_canonical_p11.json": [
            (5, "teacher_notes",
             ", which prepares students for the source-analysis work required in later units.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …drain of wealth as an economic argument "
             "grounded in evidence, not mere assertion.…"),
            (6, "band:3",
             "; teacher notes these for the teacher_notes continuity in the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …rom within the colonial administration "
             "itself?' Students offer one response each.…"),
        ],
        "ch_04_canonical_p15.json": [
            (14, "band:1",
             " covered across the chapter",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …verview section and then construct a structured comparison of "
             "the five movements: Sannyasi-Fakir Rebellion, Kol Uprising, Santhal Rebellion,…"),
        ],
        "ch_05_canonical_p07.json": [
            (5, "teacher_notes",
             "The unit's closing note on 'direct election' is a conceptual bridge to the indirect election logic of Rajya Sabha, presidential, and vice-presidential elections that follow.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …d why different election mechanisms exist "
             "for different constitutional offices.…"),
            (7, "band:2",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …one step beyond that mechanism that would be needed.' Students "
             "work individually.…"),
        ],
        "ch_05_canonical_p10.json": [
            (3, "band:1",
             " — hold this for elaboration in a later unit; note only that it governs campaign behaviour.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …oup could contest without registration?' "
             "(3) Enforcing the Model Code of Conduct. (4) Overseeing the entire electoral "
             "process end-to-end. St…"),
            (6, "band:3",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …enge this claim using the logic of how FPTP is designed to "
             "work.' Students write; three or four read aloud. The teacher synthesises: FPTP pr…"),
            (7, "band:3",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …mocratic than the Lok Sabha, or differently democratic?' "
             "Students argue in pairs, then share. The teacher draws out that democratic "
             "legitima…"),
            (9, "band:2",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …not be visible if you only looked at the post-1947 "
             "Constitution.' Students write; this requires them to reason historically, not just "
             "report…"),
            (10, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …e right conclusion given the institutional constraints?' "
             "Students argue in pairs, then share. The teacher ensures both perspectives are "
             "hear…"),
            (10, "band:3",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …ing what you know about the electoral system, how do you "
             "decide?' Students write; two or three share aloud. The teacher closes without "
             "presc…"),
        ],
        "ch_06_canonical_p07.json": [
            (3, "band:1",
             " for about ten minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …concrete example from everyday life where this value can be "
             "felt. Groups discuss, then write their three answers on the slip. Note: the chap…"),
            (7, "band:1",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …lining sittings data, the role of citizens). Two speakers per "
             "group then present each.…"),
        ],
        "ch_06_canonical_p10.json": [
            (1, "band:2",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …m Parliament, who ultimately controls the government?' Students "
             "think-pair-share, then teacher uses student responses to establish Parliamen…"),
            (4, "band:2",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …can amend the Constitution. How do these two ideas sit "
             "together?' Students think individually, write a response, then discuss. Teacher "
             "clari…"),
            (5, "teacher_notes",
             ", which is the foundation for the accountability discussions in the following unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …the Rajya Sabha. The peer-check on the "
             "flowchart reinforces procedural accuracy.…"),
            (6, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …does Parliament give you to demand answers?' Students brainstorm "
             "tools in pairs, then share. Teacher uses responses to introduce the two ac…"),
        ],
        "ch_07_canonical_p07.json": [
            (5, "teacher_notes",
             ", or creates labour previews the interconnection discussion in the next unit without requiring that unit to have occurred.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …t just the cost. The closing question "
             "about whether technology replaces, enables.…"),
            (6, "band:1",
             " as the bridge to the case study",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …troduce India as the world's second- "
             "largest mobile phone manufacturer as of 2025.…"),
        ],
        "ch_07_canonical_p10.json": [
            (1, "teacher_notes",
             ", as the next unit addresses it directly.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …atural resources' input — hold this "
             "tension rather than resolving it prematurely. Encourage students to name specific "
             "local businesses, not…"),
            (4, "band:1",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …her India actually realises its demographic dividend?' Students "
             "discuss in pairs, then share two or three responses.…"),
            (6, "band:3",
             "— leaving this as a question the Entrepreneurship unit will deepen.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …o capital a challenge for small "
             "entrepreneurs but less so for large companies?'…"),
            (7, "band:2",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …lfare tell us about motivations other than money?' Small groups "
             "of three discuss and share one insight each.…"),
            (7, "band:3",
             "Link to the upcoming unit by noting that technology increasingly shapes how entrepreneurs combine the other factors.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …forming the entrepreneurship function — "
             "the difference is scale and formality.'…"),
            (8, "band:3",
             "Close by noting that the next unit examines how all five factors — including technology — work together and sometimes compete within a single production process.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …change.' Take five or six responses "
             "spanning digital and physical technologies.…"),
        ],
        "ch_09_canonical_p10.json": [
            (6, "band:1",
             " for about ten minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …igadier-General Dyer sealing the main exit and firing "
             "approximately 1,650 rounds at a crowd gathered partly for Baisakhi and partly to "
             "prote…"),
        ],
        "ch_09_canonical_p14.json": [
            (2, "band:3",
             "; the teacher underlines the connection between social confidence and political will as a bridge to the sections ahead.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …n they would ask any of these figures if "
             "they could. Two or three are read aloud.…"),
            (5, "band:1",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …d 'independence' carry in 1906 that 'autonomy' avoids? Students "
             "discuss in pairs, then share. The teacher explains the context: Bipin Pal la…"),
            (8, "band:1",
             " for some ten minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Brigadier-General Dyer sealed the main exit and fired "
             "approximately 1,650 rounds, deliberately aiming at the thickest parts of the "
             "crowd; of…"),
            (8, "band:2",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …is concern more about strategy or principle? Students discuss in "
             "groups of three, then share.…"),
            (12, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …mmediately win independence. Does that mean it failed? Students "
             "discuss in pairs.…"),
        ],
        "ch_10_canonical_p07.json": [
            (3, "teacher_notes",
             ", making this section a natural bridge to the chapter's closing argument.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …rvation passage connects the technical "
             "history to a present civic responsibility.…"),
        ],
        "ch_11_canonical_p09.json": [
            (9, "teacher_notes",
             "Having worked through every section — from the justice-law connection and court hierarchy to PIL, High Courts, tribunals, digital tools, and ADR — students now construct a map that integrates all these threads rather than treating them as separate facts.",
             "",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every section it "
             "assumes | survives: …The cause-effect map is the synthesis task; the peer "
             "challenge in the third band ensures students are applying, not merely reproducing. "
             "Wat…"),
        ],
        "ch_11_canonical_p12.json": [
            (3, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …o to first — the Supreme Court or a local court? Why?' Students "
             "discuss in pairs, then share. Teacher uses responses to motivate the idea of…"),
        ],
        "ch_12_canonical_p08.json": [
            (5, "band:3",
             ", preparing for the next unit's rights-duties synthesis.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …son sentence between the constitutional "
             "idea of duty and the traditional concept.…"),
        ],
        "ch_12_canonical_p11.json": [
            (2, "teacher_notes",
             ", which connects to the duties discussion that follows in later units.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …tters as much as the denial — it shows "
             "that citizens who act can change outcomes.…"),
            (5, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …fferently? How should schools handle student opinions? Students "
             "discuss in pairs, then share. Teacher records the principle: freedoms exist…"),
            (7, "teacher_notes",
             "The matching task (duty to right) is the key analytical move that sets up the next unit's 'two sides of the same coin' argument.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ncy; acknowledge it as a genuine "
             "historical question rather than dismissing it.…"),
            (10, "band:3",
             "— opening the question that the next unit answers.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …discrimination blocks rights, what is the "
             "active response? What is inclusion?'…"),
        ],
        "ch_13_canonical_p07.json": [
            (5, "teacher_notes",
             ", which the following unit will develop fully.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ide base to wide middle is the visual "
             "representation of the demographic dividend.…"),
        ],
        "ch_14_canonical_p09.json": [
            (2, "teacher_notes",
             "The chart's two Indian entries give a natural bridge to the urbanisation data in the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …that a compact grey grid signals high "
             "density even without knowing the number.…"),
            (3, "teacher_notes",
             "The historical logic of river-and-route location established here reappears in the Jamshedpur and Mumbai examples in the next unit, so naming these location factors carefully now prevents confusion later.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …A common error is to treat urbanisation "
             "statistics (17 per cent to 40 per cent) as trivia rather than evidence of a "
             "structural shift; ask s…"),
        ],
        "ch_14_canonical_p12.json": [
            (3, "teacher_notes",
             "The interview-planning activity connects national-scale data to local experience without requiring outside coordination this sitting.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist | survives: "
             "…ity's 2012 and 2025 images grounds the abstraction in verifiable visual change.…"),
            (11, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …what are its three most pressing planning problems? Students "
             "write independently, then share. Introduce Singapore: an island city-state that…"),
        ],
        "ch_15_canonical_p10.json": [
            (3, "band:1",
             " for six minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …an), (c) attitude to ritual, and (d) one shared idea. Students "
             "work individually, then compare with a neighbour.…"),
            (7, "band:2",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …uscripts — mean for the production of new knowledge? Students "
             "think individually, then discuss in pairs, then share whole class. Teacher rec…"),
        ],
        "ch_15_canonical_p14.json": [
            (1, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …t mean to let cultures in without being blown off your feet? "
             "Students pair-share, then two or three share with the class. Teacher charts the…"),
            (3, "teacher_notes",
             "The closing analytical question directly bridges to the Sufism unit that follows.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ts alongside Guru Nanak's teachings, "
             "which is itself an example of integration.…"),
            (13, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …on a cultural act rather than just a construction act? Students "
             "discuss in pairs, then share.…"),
        ],
    },
    # ── S2 · social_sciences · MIDDLE · VI/VII/VIII · BATCH WAVE 1 (2026-08-16) ────────
    # 40 standards bought in one job (msgbatch_012rg61LP1SVF4ay2JM34bt2, Rs 881.64), certified
    # free: 90 ban hits over 34 of the 40 files — ~2.25/file against S5's ~1 per 3. The wave is
    # structurally spotless (zero anchor, order, coverage, synthesis, stimulus or item-type
    # failures across 41 chapters), so every hit here is text, and every edit is a deletion.
    #
    # DISTRIBUTION: 42 clock / 33 forward / 10 meta-leak / 2 ids / 2 calendar / 1 completion.
    # Two of those families are NEW to the campaign:
    #
    #   * meta-leak (10) — the model narrating its own compliance INSIDE the artefact:
    #     "…without requiring any earlier unit to have happened", "…without requiring any
    #     particular prior activity to have occurred". This is not a teaching defect and not a
    #     lottery case; it is the brief inviting a proof. The register block tells the model its
    #     units must stand alone, and the model answers in prose addressed to the constitution
    #     rather than to the teacher. Repaired here at the founder's instruction (2026-08-16)
    #     AND logged as a brief-side finding: the next SS·middle constitution pass should say
    #     that self-containment is demonstrated by the unit working, never by asserting it.
    #     Same shape as the S4 note (v1.4) where the model paraphrased the brief's own
    #     description of the synthesis unit — an argument about the BRIEF, not the model.
    #
    #   * ids (2) — leaked competency codes (C-2.2, C-7.3) in a teacher note. Struck as codes
    #     only: the sentence's teaching claim is kept, the mapping apparatus goes.
    #
    # THREE HITS ARE DELIBERATELY NOT DECLARED, and the reasons matter more than the count:
    #   1. viii ch_09 U11 band:0 "fired approximately 1,650 rounds FOR ABOUT TEN MINUTES" —
    #      Jallianwala Bagh. The quantity is the duration of the massacre, not the pacing of an
    #      activity. Repairing it would falsify the history to satisfy a regex, which is the
    #      wrong direction (runbook trap 4). Belongs at the scanner: the clock ban is about
    #      instructions to the teacher, and nothing in the pattern distinguishes an instruction
    #      from a narrated historical event.
    #   2/3. vii ch_11 U4 and viii ch_14 U10 [calendar] — "agrees to pay Rs 300 next week"
    #      (a credit-timing question in From Barter to Money) and "if you were appointed urban
    #      planner for your own town tomorrow". Both are question content, not the teacher's
    #      calendar. Left alone per founder ruling 2026-08-16; they keep the census at 3 until
    #      the scanner is narrowed or they are ruled accepted.
    #
    # One hit needed a locator the tool did not have: vi ch_07 U21 is a clock quantity in a
    # MATERIALS line. `materials:<i>` is added to _get_set in the same change rather than
    # hand-editing the artefact.
    # APPLIED 2026-08-16 (batch wave 1, the standards) — retired to a 3-tuple key so
    # the wave-2 set can own the live ("social_sciences","vi") key. Re-running it
    # would fail its own "declared text not found" guard, which is the guard.
    ("social_sciences", "vi", "APPLIED-20260816-wave1"): {
        # 27 edits across 12 chapter(s)
        "ch_01_canonical.json": [
            (9, "teacher_notes",
             ", requiring no prior draft or material.",
             ".",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …his. The sketch-map task is designed "
             "to be completed and checked within the sitting itself.…"),
        ],
        "ch_02_canonical.json": [
            (4, "teacher_notes",
             "The causal-chain sentence at the close is the conceptual bridge to the water-cycle role oceans play in the 'Oceans and Life' section.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …e visible in daily life; the data strip "
             "on proportions directly disrupts this assumption.…"),
            (8, "teacher_notes",
             ", and it sets up the size-ranking activity in the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …is the chapter's clearest example of "
             "cultural and historical labelling overriding geology.…"),
            (13, "band:0",
             "This primes the normative reasoning the unit will develop.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …blem caused by one person and a problem "
             "that requires collective responsibility to solve?…"),
        ],
        "ch_03_canonical.json": [
            (6, "teacher_notes",
             "The volcanic-origin explanation for the Deccan is important groundwork for the livelihood discussion in the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …and elevated position are the critical "
             "distinguishing markers and need explicit emphasis.…"),
            (12, "band:1",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …and animals would survive in a desert? What features would they "
             "need?' Students brainstorm, then teacher confirms with textbook-level content: "
             "sparse,…"),
        ],
        "ch_05_canonical.json": [
            (1, "teacher_notes",
             "Let students' predictions about name-sources remain tentative so that later units can confirm or correct them.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ty makes clear that the Subcontinent's "
             "boundaries and labels have shifted over millennia.…"),
        ],
        "ch_06_canonical.json": [
            (16, "band:2",
             " They write for approximately ten minutes.",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …with named evidence, and briefly acknowledge why a different "
             "choice could also be argued.…"),
            (20, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …to name this civilisation, what name would you choose and why?' "
             "Students discuss in pairs, then share with the class. Names from the chapter — "
             "Indus,…"),
        ],
        "ch_07_canonical.json": [
            (17, "teacher_notes",
             "The tree metaphor revisit connects this closing directly to the chapter's opening frame without requiring any earlier activity to have occurred.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …gned to make students earn the "
             "conclusion from evidence rather than simply agree with it.…"),
            (21, "materials:1",
             " in the first five minutes",
             "",
             "register/clock",
             "a clock quantity in a MATERIALS line, not a band — the only one in the wave. 'Role "
             "cards prepared by students' is the material; when they were made is the sitting's "
             "business"),
            (22, "band:0",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …nk (the shared concepts), and the branches (what grew from these "
             "roots). Work individually, then we compare.' Students work silently.…"),
        ],
        "ch_08_canonical.json": [
            (3, "band:1",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …se) and 'What differs?' (fabric, weave, dye, print, draping "
             "style). They work individually, then share with a neighbour.…"),
            (10, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …rment, and their major harvest festival. The teacher explains "
             "that each student will speak as that person, describing one thing about their life "
             "that…"),
        ],
        "ch_09_canonical.json": [
            (3, "teacher_notes",
             "This unit grounds the chapter's value framework in students' own family experience before moving to the narrative vignettes in the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …A common confusion is treating dharma as "
             "a religious term exclusively — clarify that the chapter uses it in the sense of "
             "one's duty or right action w…"),
            (5, "teacher_notes",
             "The drama-outline task lets students own the model without requiring a fully performed roleplay within the sitting.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …ion — frame this as the chapter "
             "showing that sevā within a family is not gender-assigned.…"),
        ],
        "ch_10_canonical.json": [
            (1, "band:2",
             " for three to four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …a school rule feels unfair, can students do anything about it?' "
             "Students discuss in pairs, then share. Draw out the idea that citizens — like "
             "student…"),
            (15, "band:3",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …or labelled most clearly, and one element I think could be made "
             "clearer.' Partners revise. Class closes with one final question: 'If you had to "
             "expla…"),
            (15, "teacher_notes",
             " — without requiring any particular prior activity to have occurred.",
             ".",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …vels of Government, and "
             "representative and grassroots democracy from the Democracy section. A common risk "
             "in synthesis work is that students list fact…"),
        ],
        "ch_11_canonical.json": [
            (1, "teacher_notes",
             ", giving you diagnostic information for later units.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …face their intuitions about which level "
             "of government should handle which scale of problem.…"),
            (3, "band:2",
             "This bridges toward the Exemplary Sarpanch cases in a later unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …connect this to what the Gram Sabha means "
             "when it includes women in collective decisions.…"),
            (6, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …about drought — is water management within a Gram Panchayat's "
             "power?' Students brainstorm and share ideas. Then introduce Popatrao Baguji Pawar "
             "and H…"),
            (8, "band:1",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …children formally naming what they need and adults responding?' "
             "Students discuss in pairs, then share the key distinction they arrived at — "
             "ownership…"),
            (10, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …esolutions — what problems do you think they would choose to "
             "address?' Students brainstorm and share four or five ideas. Then introduce the "
             "Children's…"),
            (15, "band:2",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Panchayati Raj system, or is it acceptable variation?' Students "
             "discuss in groups of three, then one spokesperson per group shares the group's "
             "positio…"),
        ],
        "ch_13_canonical.json": [
            (7, "band:3",
             "This prepares the ground for Van Mahotsav in the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …tence answering: 'What must be true about "
             "a community for Swachh Bharat Abhiyan to work?'…"),
        ],
        "ch_14_canonical.json": [
            (2, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Project the chapter's illustrated sector diagram. Students study "
             "it in silence, noting every activity listed under each sector. Teacher then covers "
             "th…"),
        ],
    },
    # APPLIED 2026-08-16 (batch wave 1, the standards) — retired to a 3-tuple key so
    # the wave-2 set can own the live ("social_sciences","vii") key. Re-running it
    # would fail its own "declared text not found" guard, which is the guard.
    ("social_sciences", "vii", "APPLIED-20260816-wave1"): {
        # 32 edits across 10 chapter(s)
        "ch_01_canonical.json": [
            (5, "band:2",
             " for about six minutes total",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …alongside. Class selects the most productive question from each "
             "cluster and discusses both, with students offering reasoning rather than the "
             "teacher s…"),
            (7, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …historically important — for farming, for trade, for cities?' "
             "Students brainstorm in pairs, then share.…"),
            (16, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …and which would allow passage — and from which direction.' "
             "Students study the map silently and mark entry-possible and entry-blocked zones "
             "with symbol…"),
        ],
        "ch_03_canonical.json": [
            (3, "band:2",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …ear; what does that tell us about the role of latitude relative "
             "to seasons?' Pairs discuss, then share answers aloud.…"),
            (3, "teacher_notes",
             "; distinguish them clearly here since altitude is the subject of the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …m. Students may conflate latitude with "
             "altitude (both make places cooler as they increase).…"),
            (7, "band:3",
             "This grounds the mechanism in cultural significance before the next unit explores climate and livelihoods.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …e the subject of classical music in a "
             "farming civilisation?' Students write one sentence.…"),
            (13, "band:3",
             " — it sets up the next unit's deeper engagement with mitigation.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …lifestyles) often conflict with economic "
             "growth goals. This question is not resolved here.…"),
        ],
        "ch_04_canonical.json": [
            (1, "teacher_notes",
             "The two-column chart anchors the contrast and will serve as a reference frame for the sections that follow.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …nd Urbanisation (late Vedic, Buddhist, "
             "Jain) are distinctly later than the Harappan peak.…"),
            (19, "band:0",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …most significant changes the chapter describes in each domain.' "
             "Students work individually, then compare with a partner.…"),
        ],
        "ch_05_canonical.json": [
            (4, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …hy would joining a guild benefit you more than working alone?' "
             "Students think individually, then share.…"),
            (18, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …common and where did they differ in how they built and held "
             "their empires?' Students think.…"),
        ],
        "ch_06_canonical.json": [
            (6, "teacher_notes",
             "The mapping task fixes geographic positions that later units build on.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …conditions produce organised literary "
             "assemblies connects cultural and political history.…"),
            (10, "teacher_notes",
             " (C-2.2)",
             "",
             "register/ids",
             "leaked competency code in prose the teacher reads. The claim — this section is a "
             "primary carrier of cultural continuity — is the teaching point and stands; the "
             "code is mapping apparatus and belongs nowhere near the classroom | survives: …s is "
             "one of two sections the mapping identifies as primary carriers of cultural "
             "continuity, and it also carries the inclusion theme (C-7.3). A common…"),
            (10, "teacher_notes",
             " (C-7.3)",
             "",
             "register/ids",
             "second code in the same sentence, same reason | survives: …s primary carriers of "
             "cultural continuity (C-2.2), and it also carries the inclusion theme. A common "
             "confusion is reading the Indo-Greek period purely…"),
            (12, "teacher_notes",
             "The map task grounds the abstract scale claim in a visual form that the art-school discussion in the next unit can then build on.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ognising it as a deliberate political act "
             "by a ruler governing a vast and diverse empire.…"),
            (18, "teacher_notes",
             "The timeline on the board provides a shared scaffold that makes the breadth of the chapter visible without requiring any particular prior activity to have happened.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …tion on the most important thread of "
             "continuity, not simply enumerate what they remember.…"),
        ],
        "ch_07_canonical.json": [
            (7, "teacher_notes",
             " — the revenue-to-patronage chain students reconstruct here will resurface when they examine Nālandā and the arts in later units.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …etes the economic picture needed to "
             "understand how Gupta cultural achievements were funded. A common confusion is "
             "imagining the Indian Ocean as a peri…"),
            (12, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Display all four images simultaneously. Students observe "
             "silently, then write: 'These four works come from different places and show "
             "different subject…"),
        ],
        "ch_09_canonical.json": [
            (1, "band:1",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …ool had no rules and no one to enforce them, what would happen?' "
             "Students discuss in pairs, then share briefly. The teacher uses this to anchor the "
             "ch…"),
            (6, "band:3",
             " — that distinguishes this system and will be contrasted with the presidential model in the next unit of study.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …tary democracy: it is the indirect "
             "accountability chain — people → legislature → executive.…"),
            (9, "band:3",
             " — and that the next unit will examine Uttaramerur as a second, more detailed case.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ibution to the history of governance — an "
             "early example of merit-based, elected leadership.…"),
            (17, "teacher_notes",
             "The closing teacher note about oligarchy as a tendency previews the challenges section without naming it as the next unit.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …es students to hold both examples "
             "simultaneously rather than treating them as sequential.…"),
            (18, "teacher_notes",
             ", and it requires students to draw on evidence from all the government types covered across the chapter.",
             ".",
             "register/completion",
             "completion claim — untrue in any compact that does not carry every government type "
             "| survives: …This unit is the chapter's explicit comparative argument for "
             "democracy. Having examined monarchy, theocracy, dictatorship, and oligarchy in "
             "detail, st…"),
        ],
        "ch_10_canonical.json": [
            (10, "band:3",
             ", which the next unit will examine.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …ing in their own words) in their "
             "response. Teacher closes by noting the contrast with DPSP.…"),
            (10, "teacher_notes",
             ", setting up a conceptual contrast with DPSP that the following unit will complete.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …his unit introduces justiciability as the "
             "key distinguishing feature of Fundamental Rights. A common confusion: students "
             "often think all constitutiona…"),
            (14, "teacher_notes",
             "The note that 'Socialist' and 'Secular' were added in 1976 connects this unit to the living document concept without requiring that unit to have been taught.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …all religious beliefs and practices "
             "with equal respect') is precise and worth repeating.…"),
            (17, "teacher_notes",
             "The chart activity works as a retrieval and consolidation exercise that sets up the synthesis unit without requiring any specific prior activity to have occurred.",
             "",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …rather than by constitutional "
             "function; the evaluative task forces a functional argument.…"),
            (18, "teacher_notes",
             ", and the teacher's closing statement restates the constitutional design logic without requiring students to have heard any particular unit's framing before.",
             ".",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …nto four columns makes the full "
             "chapter architecture visible as a whole for the first time.…"),
        ],
        "ch_11_canonical.json": [
            (6, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …bout how widespread and durable coin-based exchange became in "
             "India?' Small groups discuss and share one-sentence conclusions.…"),
        ],
        "ch_12_canonical.json": [
            (1, "band:1",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …market near your home? Which require you to go further, or to go "
             "online?' Partners discuss and report back.…"),
            (2, "band:1",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …'You are the buyer — you have ₹25 and want at least a dozen "
             "guavas.' Pairs negotiate aloud and record the price they agreed on (or note if "
             "they could…"),
            (5, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …w does it reach the kitchen of a family in Chennai?' Students "
             "brainstorm in groups of four and write the steps they imagine on strips of paper, "
             "one st…"),
        ],
    },
    # APPLIED 2026-08-16 (batch wave 1, the standards) — retired to a 3-tuple key so
    # the wave-2 set can own the live ("social_sciences","viii") key. Re-running it
    # would fail its own "declared text not found" guard, which is the guard.
    ("social_sciences", "viii", "APPLIED-20260816-wave1"): {
        # 29 edits across 11 chapter(s)
        "ch_01_canonical.json": [
            (11, "band:2",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Gallery: groups post maps and circulate, reading other groups' "
             "work. Each student places a star on the branch they find most analytically "
             "compelling a…"),
        ],
        "ch_02_canonical.json": [
            (3, "band:3",
             " — and that its cultural peak under one ruler will form the next unit's focus.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …her closes by noting that Vijayanagara "
             "became a 'significant political and cultural force'.…"),
            (7, "band:3",
             " — content beyond this chapter but foreshadowed here.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …the post-1707 fragmentation sets the "
             "stage for the Maratha rise and eventual British entry.…"),
            (8, "band:2",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …Groups of four discuss using the prompt card. Each group must "
             "identify: one shared factor across all three forms of resistance, one factor "
             "unique to R…"),
            (11, "teacher_notes",
             " — it differs from European feudalism and from the Mughal mansabdari in important ways that the next unit will develop.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …The non-hereditary nature of the iqta is "
             "the key analytical feature. Students often treat 'tax burden on peasantry' as a "
             "moral statement rather than a…"),
            (15, "band:3",
             " for the remaining minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …y significant, and why? Use one specific example to support your "
             "position.' Students write — this is a take-away prompt, not assessed in this "
             "sitting.…"),
        ],
        "ch_04_canonical.json": [
            (5, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …painting 'The East offering its riches to Britannia' without "
             "commentary. Students observe, then write: (1) Who is depicted and in what posture? "
             "(2) W…"),
            (14, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …eacher displays the 1856 sketch of the Santhal rebels without "
             "commentary. Students observe and write: (1) How are the Santhal rebels depicted — "
             "postur…"),
        ],
        "ch_06_canonical.json": [
            (1, "teacher_notes",
             "Draw students back to their board-listed ideas when later units examine specific mechanisms of that oversight.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …s and guides the government, which is the "
             "architecture the rest of the chapter builds on.…"),
            (2, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …e alone have that made the Constitution-makers add a second?' "
             "Students brainstorm in pairs, then contribute ideas. Teacher lists responses "
             "without eva…"),
        ],
        "ch_07_canonical.json": [
            (9, "band:3",
             ", which sets up the next unit's focus on how factors interact.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …k at their best without some technology?' "
             "Students write one final sentence answering this.…"),
        ],
        "ch_08_canonical.json": [
            (3, "band:1",
             " — these will be revisited in the next unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …terrain mean for ocean currents and for "
             "the creatures that live in the deep?' Hold answers.…"),
            (3, "band:2",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …→ (at least three downstream consequences they can reason out). "
             "Students work individually, then share chains with a partner.…"),
            (3, "teacher_notes",
             "The climate-regulation mechanism here is the foundation for understanding ocean currents in the following unit — name the heat-release principle explicitly so students can recall it when warm and cold currents are explained.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …A common confusion is that rainfall comes "
             "directly 'from rivers or clouds' without students connecting moisture to ocean "
             "evaporation; the step-by-ste…"),
            (5, "teacher_notes",
             " — naming coral bleaching as a human-caused phenomenon keeps that thread explicit without requiring any earlier activity to have occurred.",
             ".",
             "register/meta-leak",
             "the model narrating its own compliance to a reader who does not exist; the "
             "teaching note stands without it | survives: …vances the conservation competency "
             "first raised in the ocean-pollution plankton discussion. Students often confuse a "
             "gulf with a bay; the clearest dis…"),
        ],
        "ch_09_canonical.json": [
            (2, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …states. What advantages might each arrangement have for the "
             "British?' Students think aloud, then the teacher establishes the Crown's 1858 "
             "takeover fro…"),
            (3, "band:3",
             " for eight minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …hanging this practice mattered to a future independent India.' "
             "Students write individually; two volunteers read their responses for class "
             "comment.…"),
            (8, "band:0",
             " for five minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …and 'What do you notice in the boxes on either side of the "
             "daily's title?' Students write, then share. Teacher adds: the same 1906 Calcutta "
             "session d…"),
            (9, "band:3",
             ", previewing the next content threads.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …Ghadar Movement and the 'German Plot' as "
             "further expressions of this revolutionary energy.…"),
            (12, "band:3",
             "Teacher closes by previewing the Civil Disobedience Movement's Salt March as the chosen instrument to implement Purna Swaraj.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …olution, explain why 1929 marked a "
             "decisive turn in the independence movement's demands.'…"),
        ],
        "ch_10_canonical.json": [
            (3, "band:2",
             " for four minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …tionship between religious practice and architectural form?' "
             "Small groups of three discuss, then one member reports. Teacher records key points "
             "on the…"),
            (4, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …: 'How would you carve a cave using only hammers and chisels?' "
             "Students individually write, listing the sequence of steps, the challenges, and "
             "what wo…"),
            (10, "band:0",
             " for three minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …f privacy, convenience, rainfall management and cooling?' "
             "Students brainstorm individually, listing at least one advantage per category, "
             "then share wi…"),
        ],
        "ch_11_canonical.json": [
            # NOTE 2026-08-16: the mechanical span for this hit ran from ", as established…"
            # to the end of the sentence and would have left an unbalanced parenthesis
            # ("…(Supreme Court via SLP under Article 136. The 2023…"). Replaced by the two
            # surgical deletions below, which take the backward dependency and the meta-leak
            # separately and leave the parenthetical closing correctly.
            (11, "teacher_notes",
             ", as established in the earlier unit on Supreme Court jurisdiction",
             "",
             "register/backward",
             "a BACKWARD unit dependency the scanner did not flag, inside the same sentence as "
             "the meta-leak below: the SLP answer is false as written for any served count where "
             "that unit is not present. The parenthetical closes correctly without it | "
             "survives: …tribunal decisions can be challenged; the answer (Supreme Court via SLP "
             "under Article 136) shows how the chapter's sections connect without requiring…"),
            (11, "teacher_notes",
             " without requiring any earlier unit to have happened",
             "",
             "register/meta-leak",
             "the same sentence then narrates its own compliance with the rule it has just "
             "broken | survives: …n the earlier unit on Supreme Court jurisdiction) shows how "
             "the chapter's sections connect. The 2023 legislative renewal is worth noting as "
             "evidence t…"),
        ],
        "ch_12_canonical.json": [
            (3, "teacher_notes",
             "; the reference table in 'Key Constitutional Articles' will give them granular detail in a later unit.",
             ".",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …han retelling. Watch for students who "
             "conflate the six categories with individual articles.…"),
            (5, "band:0",
             " for two minutes",
             "",
             "register/clock",
             "clock quantity struck; the band carries its own minutes and the platform rescales "
             "them | survives: …aised differently? How should schools handle student opinions? "
             "Students think individually, then share responses orally.…"),
        ],
        "ch_13_canonical.json": [
            (4, "teacher_notes",
             "The migration discussion naturally bridges to the resource-strain theme and can be carried into later conversations about urban planning.",
             "",
             "register/forward",
             "forward reference — false for any served count that ends here or borrows a "
             "different unit at this slot | survives: …text's clarification that it is an "
             "average under current conditions is worth dwelling on.…"),
        ],
    },
    # ── APPLIED 2026-08-04 (the VIII ch 3 pilot); MOVED to a 3-tuple SUPERSEDED key on
    #    2026-08-16 so the batch wave-1 set above can own the live ("social_sciences","viii")
    #    key — same pattern as ix/APPLIED-20260803 and mathematics·IX v1.5. It was a DUPLICATE
    #    dict key for one run and silently shadowed the new set (Python keeps the last), which
    #    surfaced as this set's own "declared text not found" guard firing on already-repaired
    #    text. The guard caught it; the key layout is what made it possible.
    ("social_sciences", "viii", "APPLIED-20260804"): {
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
    #    MOVED to a 3-tuple SUPERSEDED key 2026-08-12 so the S-SS·IX wave-1 set below can own
    #    the live ("social_sciences", "ix") key — same pattern as mathematics·IX v1.5.
    ("social_sciences", "ix", "APPLIED-20260803"): {
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
    # ── S-SS · social_sciences · secondary · IX · BATCH WAVE 1 (2026-08-12) ─────────
    # The first set written against a BATCH-authored wave: 8 standards bought in one job
    # (msgbatch_01G73foX7nA3cpHfNCX99Ui9, Rs 193.23), certified free, 14 ban hits over 7 of
    # the 9 chapters. ch 3 (the pilot, authored 2026-08-03) and ch 9 scan clean.
    #
    # DISTRIBUTION, and it is a new one: 9 clock / 2 forward / 2 calendar / 1 completion.
    # Every earlier stage was forward-dominated (maths·IX 6 forward / 0 clock; science·IX
    # 1/2; SS·VIII 3/4). Here the CLOCK ban carries two-thirds of the breach on its own, and
    # every one of the nine is the same sentence shape: "Students work individually for N
    # minutes, then <share|compare>". That is not boilerplate the model reached for — it is
    # the model pacing a band it can already see the length of. Worth taking to the brief:
    # the clock ban is stated, but nothing tells the model how to express intra-band pacing
    # WITHOUT a quantity, and it evidently wants to. All nine deletions leave the grouping
    # ("individually", "in pairs") and the output ("then share", "then compare") standing —
    # the pedagogy is entirely in those, never in the number.
    #
    # ALL THIRTEEN ARE PURE DELETIONS. No text is authored. Struck at the founder's
    # instruction (2026-08-12): clock, forward and calendar. The single COMPLETION hit
    # (ch 1 U13) is deliberately NOT declared here — see the note at the end of this set.
    ("social_sciences", "ix", "APPLIED-20260812-wave1"): {
        # ── forward (2) ──
        "ch_01_canonical.json": [
            (5, "band:3",
             ", previewing the four dedicated discipline sections without naming upcoming units.",
             ".",
             "register/forward",
             "the model breached and self-certified in one clause — it wrote 'without naming "
             "upcoming units' while naming them. The band's teaching act (list four disciplines "
             "against their drought-web branch) is complete at the full stop; the promise is "
             "false in any compact that drops a discipline section"),
        ],
        "ch_04_canonical.json": [
            (8, "teacher_notes",
             " 'cultural continuity' in the civilisation sections that follow.",
             " 'cultural continuity'.",
             "register/forward",
             "the C/N annotation move is justified on its own terms; the pointer to later "
             "civilisation sections is what makes the note false when Mehrgarh is the last "
             "sitting a compact reaches. Deleting the prepositional phrase leaves the "
             "analytical claim intact"),
        ],
        # ── clock (9) — the quantity goes, the grouping and the output stay ──
        "ch_02_canonical.json": [
            (11, "band:1",
             "Students work individually for fifteen minutes, then compare maps in pairs",
             "Students work individually, then compare maps in pairs",
             "register/clock",
             "band is 10-30 at 50 min; proportional scaling to a 40-min serve makes 'fifteen "
             "minutes' silently wrong while the band's own minutes stay correct"),
        ],
        "ch_05_canonical.json": [
            (2, "band:0",
             "Students think independently for two minutes, then share",
             "Students think independently, then share",
             "register/clock",
             "think-pair-share pacing; the quantity is the only scale-dependent token"),
            (21, "band:0",
             "Students work independently for five minutes, then share their labels",
             "Students work independently, then share their labels",
             "register/clock",
             "U21 is the synthesis unit — the one unit a compact borrows verbatim, so a "
             "hard-coded quantity here travels further than anywhere else in the library"),
        ],
        "ch_06_canonical.json": [
            (3, "band:0",
             "Students discuss in pairs for three minutes, then share",
             "Students discuss in pairs, then share",
             "register/clock",
             "opens on the chapter's own THINK ABOUT IT prompt; pairing and share-back carry "
             "the structure without the number"),
            (7, "band:0",
             "Students work individually for seven minutes, then share two examples with the class",
             "Students work individually, then share two examples with the class",
             "register/clock",
             "the output is quantified ('two examples') and that quantity is scale-free — it "
             "is only the minutes that falsify"),
            (17, "band:0",
             "Students write individually for four minutes, then share one action and one "
             "community issue with the class",
             "Students write individually, then share one action and one community issue with "
             "the class",
             "register/clock",
             "scanner marked this quoted=True because the band opens on a quoted prompt; the "
             "match itself sits outside the quotation, so it is a true ban hit"),
        ],
        "ch_07_canonical.json": [
            (4, "band:0",
             "Let students discuss in pairs for two minutes, then take responses",
             "Let students discuss in pairs, then take responses",
             "register/clock",
             "constituency-size provocation; the teacher move is 'take responses', not the clock"),
        ],
        "ch_08_canonical.json": [
            (1, "band:0",
             "one choice they or their family made this week where they could not have both options",
             "one choice they or their family made where they could not have both options",
             "register/calendar",
             "struck at the founder's instruction. Recorded dissent: this reads as the STUDENT'S "
             "own life, not the teaching schedule, which is the same ground on which "
             "'today'/'yesterday' were demoted to advisory. The deletion costs nothing — "
             "'a choice they could not have both ways' is the scarcity example whole — so the "
             "cheaper action was to strike rather than argue"),
            (1, "band:2",
             "students list three things their parents bought this month and classify",
             "students list three things their parents bought and classify",
             "register/calendar",
             "same family and same dissent as U1 band:0; the LET'S EXPLORE task is unchanged "
             "in substance without the window"),
            (5, "band:3",
             "They work individually for five minutes, then compare with a neighbour to catch gaps",
             "They work individually, then compare with a neighbour to catch gaps",
             "register/clock",
             "band is 40-50, the last band of the unit — the one most exposed to scaling"),
            (7, "band:1",
             "Students work individually for ten minutes, then compare with a neighbour",
             "Students work individually, then compare with a neighbour",
             "register/clock",
             "ten minutes of a 16-minute band; at a 40-min serve the band is ~13 and the "
             "quantity crowds out the compare step it is paired with"),
        ],
    },
    # ── S-SS · social_sciences · IX · BATCH WAVE 2 · THE COMPACTS (2026-08-12) ────
    # 14 compacts, 14 ban hits over 8 files — and the SAME distribution as wave 1: 11 clock,
    # 1 forward, 1 calendar (+ the 1 completion left standing in ch 1's standard). Wave 1 was
    # 9 clock of 14. Two independent waves, same dominant family, ~0.8 clock hits per file
    # both times. That is not variance; it is the brief. The clock ban is stated but nothing
    # tells the model how to pace WITHIN a band without a quantity, and every hit takes the
    # same shape: "<group> for N minutes, then <share|compare>". Fix belongs upstream in the
    # SS·secondary LP constitution, not in this file forever.
    #
    # ch 8 p04 U1 REPRODUCED, INDEPENDENTLY, THE EXACT CALENDAR BREACH struck from the ch 8
    # STANDARD earlier today ("things their parents bought this month"). Both were authored
    # free from the same summary, whose LET'S EXPLORE carries the window. Evidence that this
    # one is the SOURCE's phrasing surfacing twice, not a model habit — and a second reason to
    # think the demotion argued in the wave-1 set is the right call. Struck here for
    # consistency with the standard, on the same instruction.
    #
    # All 14 are pure DELETIONS. No text is authored.
    #
    # APPLIED 2026-08-12T20:02. Rotated to its 3-tuple key on 2026-08-13 so the live
    # 2-tuple below can carry the ch 5 declaration; re-running THIS set would fail its own
    # "declared text not found" guard on the first edit, which is the design.
    ("social_sciences", "ix", "APPLIED-20260812-wave2"): {
        "ch_01_canonical_p09.json": [
            (8, "band:0",
             "Students brainstorm silently for two minutes, then share",
             "Students brainstorm silently, then share",
             "register/clock", "silent-brainstorm pacing; grouping and share-back stand"),
        ],
        "ch_01_canonical_p12.json": [
            (5, "band:0",
             "Students brainstorm for two minutes in pairs before any explanation",
             "Students brainstorm in pairs before any explanation",
             "register/clock", "the ordering constraint ('before any explanation') is the "
             "teaching point and is scale-free"),
            (8, "band:0",
             "Students discuss in pairs for three minutes.",
             "Students discuss in pairs.",
             "register/clock", "borewell scenario; the collected word-cluster is the output"),
        ],
        "ch_02_canonical_p07.json": [
            (2, "band:0",
             "Students discuss in pairs for two minutes, then share",
             "Students discuss in pairs, then share",
             "register/clock", "volcanic-ash observation; Varahamihira link is untouched"),
        ],
        "ch_04_canonical_p11.json": [
            (7, "band:0",
             "Students brainstorm individually for two minutes, then share",
             "Students brainstorm individually, then share",
             "register/clock", "THINK ABOUT IT on river civilisations; the two-column record "
             "is the output"),
        ],
        "ch_04_canonical_p15.json": [
            (2, "band:0",
             "Students brainstorm individually for two minutes, then share aloud",
             "Students brainstorm individually, then share aloud",
             "register/clock", "chapter's own opening question"),
            (5, "band:0",
             "Students predict in writing for two minutes, then share",
             "Students predict in writing, then share",
             "register/clock", "'in writing' is the move that matters, not the duration"),
        ],
        "ch_05_canonical_p13.json": [
            (4, "band:2",
             "Each group deliberates for five minutes and presents its position",
             "Each group deliberates and presents its position",
             "register/clock", "sabha/samiti role play; the vote that follows is the output"),
        ],
        "ch_06_canonical_p15.json": [
            (6, "teacher_notes",
             " — a tension the Challenges unit will develop", "",
             "register/forward",
             "the ONLY forward reference in either wave that names another unit outright. The "
             "note's teaching point — distinguishing the media's democratic function from its "
             "platform form — is complete without the promise, and the promise is false in any "
             "plan where this unit is the last sitting"),
            (15, "band:0",
             "Students work individually for eight minutes, then compare with a neighbour",
             "Students work individually, then compare with a neighbour",
             "register/clock", "whole-chapter cause-effect map; the four branches are the spec"),
        ],
        "ch_08_canonical_p04.json": [
            (1, "band:0",
             "students individually list three things their parents bought this month, then classify",
             "students individually list three things their parents bought, then classify",
             "register/calendar",
             "the standard's U1 breach, reproduced independently by the compact from the same "
             "LET'S EXPLORE. Struck for consistency with the standard; the same dissent is "
             "recorded there"),
            (2, "band:3",
             "Students work individually for four minutes, then share in pairs",
             "Students work individually, then share in pairs",
             "register/clock", "garment-factory analytical task"),
            (3, "band:1",
             "Students discuss in pairs for three minutes, then two pairs share their reasoning",
             "Students discuss in pairs, then two pairs share their reasoning",
             "register/clock",
             "THINK ABOUT IT inside the what/for-whom unit; 'two pairs share' is the output "
             "and is scale-free"),
        ],
    },
    # ── S-SS · social_sciences · IX · ch 5 · THE META-CLAUSE (2026-08-13) ────────────
    # ONE edit, and it is not the usual family. The breach is not the model pacing a band or
    # promising a later unit — it is the model NARRATING ITS OWN BRIEF into teacher-facing
    # text: "an integrative question that surveys the chapter's full arc without claiming the
    # chapter is complete". The clause is the compact brief's self-containment instruction,
    # quoted back. It trips the completion pattern on the very words it uses to disclaim
    # completion, which is why a scanner cannot rule on it and a reader can in one look.
    #
    # A PURE DELETION, per the file's own line: nothing is authored. What the teacher is asked
    # to do — the Nāśhik-inscription question, the paragraph-length response with two details
    # from the inscription and one from elsewhere, the written formative check — is untouched
    # and complete without the clause. Worth recording as a pattern for the brief rather than
    # for register_scan.py: a brief phrased as a prohibition ("do not claim the chapter is
    # complete") gives the model a sentence to repeat; the mathematics·IX set already found one
    # hit that was the model paraphrasing the brief's description of the synthesis unit. That is
    # twice now, in two subjects. It is an argument about the BRIEF.
    ("social_sciences", "ix"): {
        "ch_05_canonical_p13.json": [
            (13, "band:3",
             "The teacher closes with an integrative question that surveys the chapter's "
             "full arc without claiming the chapter is complete: 'The Nāśhik inscription",
             "The teacher closes with an integrative question: 'The Nāśhik inscription",
             "register/completion",
             "the compact brief's own self-containment instruction, quoted into the band. The "
             "question, the two-details-plus-one requirement and the formative check all stand"),
        ],
    },
    # NOT DECLARED, and left standing — now by FOUNDER RULING (2026-08-13), where before it was
    # an open question: ch_01 U13 teacher_notes, "Having covered all four disciplines, this unit
    # turns to the chapter's explicit…" — family COMPLETION. The reasoning that made it a
    # judgement call rather than an edit is unchanged and is why the ruling went the way it did:
    # U13 of 15 sits after all four discipline sections in the STANDARD, where the sentence is
    # simply TRUE; it is false only in a compact that drops a discipline, and a compact borrowing
    # U13 borrows this note with it. So the question was never "is this text wrong" but "is the
    # completion ban about the text or about the serve" — and the founder has accepted the text.
    # ACCEPTED, not fixed: `--apply` still reports 1 surviving ban hit in ch_01 and exits 1, and
    # ch_01's certification report still says FAIL. That is the declared state. Anything that
    # reads "SS·IX is clean" must say "one accepted breach" in the same breath.
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
    # APPLIED 2026-08-06 (recorded in the artefact's genon_canonical.repairs[]); renamed
    # 2026-08-17 so the batch wave-1 set below can own the live ("science", "ix") key.
    # Re-running it would fail its own "declared text not found" assertion — the guard.
    ("science", "ix", "APPLIED-20260806-pilot"): {
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
    # ── S3 · science · SECONDARY · BATCH WAVE 1 (the STANDARDS) — 2026-08-17 ──────────
    # 16 ban hits over 9 of the 12 standards bought in batch msgbatch_01PQV9xposrif1tLAfD43a6u
    # (certification 20260817_1006*): 8 forward / 4 clock / 2 completion / 2 meta-leak.
    # 1.33 hits/file — worse than S5's wave 1 (0.35) but under S2's 2.25. Ch 03 scanned clean.
    #
    # Nearly all are PURE DELETIONS of trailing forward-reference appositives or clock
    # quantities. Three spans were narrowed or minimally rearranged BY HAND because the
    # mechanical sentence-span would have deleted teaching (the S2 wave-2 precedent):
    # ch 04 U20 (antecedent swap "them" -> "the motion types"), ch 06 U5 ("for emphasis"
    # replaces the bridge clause so 'is flagged' keeps a complement), ch 06 U20 (clause
    # rearranged around the deletion so the imperative keeps its subject).
    # ch 09 U20 carries ONE unflagged same-family edit (" a second" -> " an"), declared
    # rather than left, because "a second opportunity" presumes an earlier sitting ran the
    # challenge — the same completion family the scanner flagged two sentences later.
    # APPLIED 2026-08-17 (0 surviving hits, re-certified 20260817_1040); renamed so the
    # wave-2 set below owns the live key.
    ("science", "ix", "APPLIED-20260817-wave1"): {
        "ch_01_canonical.json": [
            (4, "band:0",
             " for five minutes", "",
             "register/clock",
             "'Students write individually' is the instruction; the band carries its own "
             "minutes and the platform rescales them"),
            (6, "band:0",
             " for four minutes", "",
             "register/clock",
             "same pattern — 'Students write, then share one idea with a partner' stands "
             "complete without the quantity"),
        ],
        "ch_04_canonical.json": [
            (12, "band:4",
             ", leaving the formal answers to unfold in the next unit", "",
             "register/forward",
             "the teaching act — addressing the collated questions with brief pointer "
             "statements — stands alone; the promise of a NEXT unit is false for any X "
             "ending here. Section 4.4.1 by name is a chapter fact and stays"),
            (20, "teacher_notes",
             "Having worked through all motion types individually, students now synthesise "
             "across them",
             "Students now synthesise across the motion types",
             "register/completion",
             "the completion assertion is false for any served count that dropped a motion "
             "unit; deleting the clause alone orphans 'them', so the antecedent is swapped "
             "in — no new content, the motion types are this unit's own comparison table"),
        ],
        "ch_05_canonical.json": [
            (2, "teacher_notes",
             ", which prepares students to engage seriously with the formulae in the next unit", "",
             "register/forward",
             "trailing appositive; 'the ORS and pesticide scenarios are effective because "
             "they give concentration a tangible consequence' is the complete teaching "
             "point"),
        ],
        "ch_06_canonical.json": [
            (5, "band:4",
             " as a bridge to the law students will formalise next",
             " for emphasis",
             "register/forward",
             "the thought-experiment outcome (frictionless motion continues forever) is "
             "real teaching and must survive; 'is flagged' needs a complement, so the "
             "forward clause is replaced by two neutral words — hand-narrowed, S2 wave-2 "
             "precedent"),
            (20, "teacher_notes",
             "The one-sentence three-law summary at the close is an explicit conceptual "
             "bridge to the synthesis unit; encourage",
             "For the one-sentence three-law summary at the close, encourage",
             "register/forward",
             "the synthesis unit may not be the sitting that follows for any served X; the "
             "clause is rearranged around the deletion so the imperative keeps its subject "
             "— every content word survives, only the bridge claim goes"),
        ],
        "ch_07_canonical.json": [
            (5, "teacher_notes",
             " The connection the chapter makes between mechanical energy and the earlier "
             "study of forces is the conceptual anchor for the next unit on kinetic and "
             "potential energy.", "",
             "register/forward",
             "whole sentence is a planning pointer, not classroom teaching; the note ends "
             "on the chemical-energy redirect, which is complete"),
            (8, "teacher_notes",
             " before the formal derivation of U = mgh in the next unit", "",
             "register/forward",
             "'the rubber band and spring examples are essential for breaking that "
             "narrowness' is the teaching act; when the derivation arrives is not this "
             "unit's claim to make"),
        ],
        "ch_09_canonical.json": [
            (16, "teacher_notes",
             " preparation for the next unit on formula unit mass", "",
             "register/forward",
             "pure truncation: 'The closing sentence linking molecular mass to "
             "covalent-only applicability is important; the distinction between the two "
             "terms matters.' — the distinction survives, the unit pointer goes"),
            (20, "teacher_notes",
             " built across the chapter", "",
             "register/completion",
             "'with enough conceptual grounding to connect their result to Dalton's "
             "theory' stands; the whole-chapter completion claim is false for any served "
             "count below the top"),
            (20, "teacher_notes",
             " a second opportunity", " an opportunity",
             "register/completion",
             "UNFLAGGED same-family edit, declared not left: 'a second opportunity' "
             "presumes an earlier sitting ran the design challenge, which a compact or "
             "borrowed serving may not have"),
        ],
        "ch_10_canonical.json": [
            (5, "teacher_notes",
             " to bridge to the piston analogy", "",
             "register/forward",
             "the question ('what would the compressions and rarefactions correspond "
             "to?') is the teaching act and ends the note cleanly; the piston analogy "
             "lives in another unit"),
        ],
        "ch_11_canonical.json": [
            (7, "teacher_notes",
             " this unit", "",
             "register/meta-leak",
             "'use it to make the inquiry concrete without requiring physical materials' "
             "is complete; 'this unit' is planner vocabulary leaking into the teacher "
             "note"),
            (10, "teacher_notes",
             " without requiring that any earlier unit was taught in any particular way", "",
             "register/meta-leak",
             "the clause is the BRIEF's own self-containment language leaked verbatim "
             "into the note (ARV-D-161 family); 'consolidates the chapter's two main "
             "threads' is the teaching point and stands"),
        ],
        "ch_13_canonical.json": [
            (3, "teacher_notes",
             " The polar-albedo discussion is a natural bridge to the latitude and "
             "Earth's shape content that this chapter presents next.", "",
             "register/forward",
             "whole sentence is a sequencing pointer; the note's albedo/absorption "
             "teaching is untouched"),
            (6, "teacher_notes",
             " for the human-impact discussion in a later unit", "",
             "register/forward",
             "'The 315-to-420 ppm data point is a strong anchor.' stands — the data "
             "point's value does not depend on which sitting discusses human impact"),
        ],
    },
    # ── S3 · science · SECONDARY · BATCH WAVE 2 (the COMPACTS) — 2026-08-17 ───────────
    # 24 compacts bought in msgbatch_0196ajLwMtEnpwdE2LxPVHxt. 23 ban hits over 14 of 24
    # files — 0.96/file, BELOW wave 1's 1.33 (S2's compacts matched their standards at
    # 2.3; science's improved). Distribution: 16 forward / 4 clock / 3 completion, no
    # meta-leak, no calendar. The completion shift wave-1 0 -> 3 on compacts repeats the
    # S2 observation: a compact asserting "across the chapter" is false by construction.
    # All edits are pure deletions except three hand-narrowed spans (ch_05 p15 U12,
    # ch_07 p18 U18, ch_13 p07 U7 — the completion openers, where deleting the clause
    # alone would orphan the sentence's subject; same-word rearrangements, no new
    # content). Backward references ("the previous sitting", "the preceding unit") are
    # the POSITIONAL advisory family, not bans, and are left standing.
    # ── S6 · science · middle · batch WAVE 1 (2026-08-17) ────────────────────────────
    # One clock hit in 36 standards, and it is a homonym: the ranged pattern
    # (`for…{0,20}minutes`) matched "the causal explanation FOR THE 50-MINUTES-later
    # moonrise rule" — the ~50-minute daily lag of moonrise, an astronomical FACT the unit
    # teaches, not class pacing. Founder ruling 2026-08-17: repair the TEXT, keep the
    # scanner strict — the phrasing moves off the pattern ("of the 50-minute-later…",
    # compound-modifier singular), the astronomy is untouched, and the pattern keeps its
    # full reach for the real breaches it was written for.
    # ── S6 · science · middle · wave 3 resynth (2026-08-18) ──────────────────────────
    # The re-authored synthesis units: 4 clock hits in 37 (the §6 brief's no-clock line
    # held for 33). Three are true pacing narration — pure deletions, the band carries
    # its own minutes. The vii ch 12 hit is the moonrise homonym again: 'the Sun
    # vanishing for two minutes at midday' is a HISTORICAL ECLIPSE CARD's content
    # (totality lasts ~2 minutes — the duration is what identifies the event), so per
    # the founder's standing ruling (2026-08-17, twice) the TEXT moves off the pattern
    # and the fact stays: 'vanishing, two minutes long, at midday'.
    ("science", "vi"): {
        "ch_11_canonical.json": [
            (14, "band:0",
             " for two minutes before beginning",
             " before beginning",
             "register/clock",
             "silent reading is the instruction; the band carries its own minutes"),
        ],
    },
    ("science", "vii"): {
        "ch_12_canonical.json": [
            (14, "teacher_notes",
             "the Sun vanishing for two minutes at midday",
             "the Sun vanishing, two minutes long, at midday",
             "register/clock",
             "homonym: eclipse-card content, not pacing — totality's ~2 minutes is the "
             "identifying fact and stays; rephrase clears the for…minutes pattern"),
        ],
    },
    ("science", "viii"): {
        "ch_03_canonical.json": [
            (9, "band:0",
             " for two minutes without writing",
             " without writing",
             "register/clock",
             "read-first-then-clarify is the instruction; the band carries its minutes"),
        ],
        "ch_10_canonical.json": [
            (15, "band:3",
             "Groups write for two minutes.",
             "Groups write.",
             "register/clock",
             "the writing task is the instruction; the band carries its minutes"),
        ],
    },
    # Renamed off the live key 2026-08-18 so the wave-3 set above owns it; applied
    # 2026-08-17 (the moonrise homonym). Re-running it would fail its own guard.
    ("science", "viii", "APPLIED-20260817-wave2"): {
        "ch_11_canonical.json": [
            (6, "band:0",
             "for the 50-minutes-later moonrise rule",
             "of the 50-minute-later moonrise rule",
             "register/clock",
             "homonym, not a breach in substance: the 50-minute moonrise lag is the "
             "unit's content; two-word rephrase clears the ranged-clock pattern with "
             "the fact intact"),
        ],
    },
    ("science", "ix"): {
        "ch_02_canonical_p12.json": [
            (11, "teacher_notes",
             " in the following unit", "",
             "register/forward",
             "'prepares the ground for thinking about contact inhibition and cancer' "
             "stands; where that thinking happens is not this unit's claim"),
        ],
        "ch_03_canonical_p12.json": [
            (8, "band:3",
             " in the next unit", "",
             "register/forward",
             "'before reading Section 3.5' survives — a section is a chapter fact; the "
             "unit pointer is the breach"),
        ],
        "ch_04_canonical_p13.json": [
            (4, "band:0",
             " for three minutes", "",
             "register/clock",
             "'Pairs discuss, then share their proposed method' is the instruction; the "
             "band carries its own minutes"),
        ],
        "ch_04_canonical_p18.json": [
            (12, "teacher_notes",
             " in the following unit", "",
             "register/forward",
             "'The transition to circular motion will build on the recognition…' keeps "
             "the teaching point (circular = simplest 2D case); the unit pointer goes"),
        ],
        "ch_05_canonical_p11.json": [
            (1, "band:3",
             " as ideas that the chapter will develop further", "",
             "register/forward",
             "'connecting both to particle size and light scattering' is complete; the "
             "development promise is false for a served count that ends early"),
            (10, "band:0",
             " for two minutes", "",
             "register/clock",
             "'They observe each, record whether particles are visible' stands; the "
             "band carries its own minutes"),
        ],
        "ch_05_canonical_p15.json": [
            (2, "teacher_notes",
             " before the formulas in the next unit", "",
             "register/forward",
             "'to surface the ratio thinking needed' is the teaching act; when the "
             "formulas arrive is not this unit's claim"),
            (12, "band:2",
             " from either direct observation or the principles established across the "
             "chapter.",
             " from either direct observation or established principles.",
             "register/completion",
             "hand-narrowed rearrangement, same words: the whole-chapter completion "
             "claim is false for any served count below the top; the fill-from-two-"
             "sources instruction survives intact"),
        ],
        "ch_07_canonical_p13.json": [
            (3, "band:3",
             " Students note this as a bridge to the next section's energy content.", "",
             "register/forward",
             "whole sentence is a sequencing pointer; the consolidation ('positive work "
             "adds energy, negative work removes it') is the teaching and stands"),
        ],
        "ch_07_canonical_p18.json": [
            (18, "teacher_notes",
             "Having worked through all the chapter's quantitative content, this unit "
             "asks students to synthesise",
             "This unit asks students to synthesise",
             "register/completion",
             "hand-narrowed: the completion opener is false for any served count that "
             "dropped a quantitative unit; the synthesis instruction keeps its subject"),
        ],
        "ch_08_canonical_p07.json": [
            (2, "band:1",
             " for two minutes", "",
             "register/clock",
             "'Students discuss in pairs, then share' stands; the band carries its own "
             "minutes"),
            (3, "band:1",
             " for three minutes", "",
             "register/clock",
             "'Students reason individually, then share' stands; same pattern"),
            (5, "band:3",
             " and tell students the next unit will show why this structural feature "
             "governs how atoms combine", "",
             "register/forward",
             "'Draw out the answer — filled outermost shell' is the teaching act and "
             "closes cleanly; the promise is false for X ending here"),
        ],
        "ch_09_canonical_p13.json": [
            (5, "teacher_notes",
             " that follow", "",
             "register/forward",
             "minimal cut: 'the conceptual frame that the two bonding sections depend "
             "on' keeps the dependency claim — sections are chapter facts; their "
             "sequence is not this unit's to assert"),
            (11, "teacher_notes",
             " — it is developed fully in the next unit", "",
             "register/forward",
             "'Keep the NaCl counter-example brief here.' is complete advice"),
        ],
        "ch_09_canonical_p18.json": [
            (11, "teacher_notes",
             " in the next unit", "",
             "register/forward",
             "'that distinction will matter immediately' survives without promising "
             "which sitting delivers it"),
            (17, "teacher_notes",
             " and should anchor the opening of the next unit", "",
             "register/forward",
             "'Collect the exit questions genuinely — they will reveal which step most "
             "students are uncertain about' stands complete"),
            (17, "band:3",
             " to inform the next unit's opening", "",
             "register/forward",
             "'Teacher collects the questions.' is the whole classroom act"),
        ],
        "ch_10_canonical_p11.json": [
            (5, "teacher_notes",
             " the class will formalise in the next unit", "",
             "register/forward",
             "'The second written prompt anticipates amplitude and should surface "
             "intuitions' stands"),
            (7, "teacher_notes",
             " (introduced in the next unit)", "",
             "register/forward",
             "'loudness is subjective' is true wherever loudness is taught; the "
             "parenthetical schedules it, which no unit may do"),
            (10, "teacher_notes",
             " The concept map can be left on the board for reference in the next "
             "unit.", "",
             "register/forward",
             "whole sentence is a logistics pointer to a sitting that may never follow "
             "this one"),
        ],
        "ch_11_canonical_p12.json": [
            (7, "teacher_notes",
             " The causal chain task at the close is an important bridge to the "
             "fertilisation content students will encounter next.", "",
             "register/forward",
             "whole sentence is a sequencing pointer; the pollination misconception "
             "teaching above it is untouched"),
        ],
        "ch_13_canonical_p07.json": [
            (7, "teacher_notes",
             "Building on the cycles and sphere interactions covered throughout the "
             "chapter, this unit asks students to evaluate",
             "This unit asks students to evaluate",
             "register/completion",
             "hand-narrowed: the whole-chapter opener is false below the top count; the "
             "evaluation instruction keeps its subject"),
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

    # ── english · VI · ch 8 (S10 · C7, 2026-08-13) ───────────────────────────────────────────
    # TWO CLOCK QUANTITIES, and BOTH WERE INVISIBLE TO THE MACHINE GATE. `register_scan.py`'s
    # clock patterns all key on a digit or on a fixed phrase ("for N minutes", "the remaining
    # time", "half the session", "in the first/last N minutes"); a SPELLED-OUT number attached
    # to anything else sails through. The certification report reads "0 ban hit(s)" on all three
    # files and is wrong on two of them. Found by reading at C7, which is the step whose whole
    # job is to see what the regex cannot.
    #
    # The first one is the sharper of the two because of WHERE it sits: the STANDARD's closing
    # synthesis unit, which is the one unit v2.0 designs to be BORROWED. It is already in the
    # X=11 serve and in kumar3's mixed week, and both happened to land it on a 40-minute sitting,
    # so it is accidentally true today. Served at 50 the same sentence tells the teacher she has
    # forty minutes for a fifty-minute sitting — demonstrated live at C7 (40 -> true, 50 -> false,
    # 60 -> false). That is exactly the silent falsification ban 1 exists to prevent.
    #
    # Both edits are pure DELETIONS of an appositive clause. Nothing is invented, and neither
    # sentence loses a pedagogical claim: "everything they need" is the point, "within these
    # forty minutes" was only ever the packaging, and a discussion "genuinely philosophical" is
    # the judgement the teacher needs — "worth five minutes" is a budget the platform overwrites.
    # The trailing "all within the unit's own minutes" in U12 is deliberately LEFT: it names no
    # quantity, scales with the sitting, and is the honest form of what the removed clause tried
    # to say.
    #
    # FOUNDER RULING 2026-08-13: amend the teacher notes and nothing else. No new scanner
    # pattern, no defect rows, and the 15 other canonicals across social_sciences and
    # mathematics that carry the same shape are deliberately NOT touched here.
    # ── v1.6, 2026-08-14 · S11 · english IX · the wave-1 top canonicals ──────────────
    #
    # 14 ban hits across 9 of the 16 chapters — a higher rate than S5's ~1 per 3 files. The
    # census is what makes this set different from every one before it, so read it before
    # the edits:
    #
    #     meta-leak   6   the model NARRATING the register rule into teacher-facing prose
    #     forward     5   4 of them in ch 7 alone
    #     clock       2
    #     completion  1
    #
    # THE META-LEAK FAMILY IS NEW, AND IT IS NOT A TEACHING DEFECT. Six times the model wrote
    # its own compliance into the plan — "without assuming any specific earlier activity took
    # place", "No prior activity is assumed". The self-contained register asks a unit to make
    # no backward claim; it does not ask the unit to SAY it makes none. The teacher gains
    # nothing from the assurance and loses a sentence to read, and the phrasing itself names
    # "earlier units", which is the very reference the ban exists to remove. Every one is a
    # trailing clause that deletes whole — the sentence before it is the teaching content and
    # stands alone. Five of the six sit on SYNTHESIS units, which is where the constitution
    # presses hardest on independence, so the leak is a predictable consequence of the rule's
    # placement rather than model noise. Worth carrying to the constitution as a prohibition
    # ("do not narrate this rule"), not just repairing here — noted for the human gate.
    #
    # ch 7 IS NOT FROM THIS BATCH. Its 4 forward references are the 2026-08-13 SYNC file that
    # the batch correctly skipped as already-installed, and it has never been through a repair
    # sweep. Its rate (4 hits in 17 units) against the batch's (10 in 143) is the clearest
    # evidence available that the batch path is not worse than the sync path.
    #
    # ONE HIT IS DELIBERATELY LEFT PARTIAL, and it is declared rather than hidden: ch 7 U8's
    # whole band is a preview of what the next unit will feel like. The trailing "so students
    # know what the next unit will feel like" is struck, which removes the unknowable claim,
    # but "names the Critical Reflection tasks ahead and previews the kind of thinking they
    # demand" survives. That residue is STRUCTURAL — the band's teaching purpose is the
    # preview — and this tool must not launder a structural change as text hygiene. It goes
    # to the human gate as a waiver or a re-author decision on ch 7.
    # APPLIED 2026-08-14 to the 15 wave-1 TOP canonicals (14 hits -> 0). Kept as the
    # cost record; stale by design — re-running it fails its own assertion.
    ("english", "ix", "APPLIED-20260814-wave1-tops"): {
        "ch_03_canonical.json": [
            (14, "teacher_notes",
             ", without assuming any specific activity or discussion from earlier units "
             "actually took place", "",
             "register/meta-leak",
             "synthesis unit. 'draws on the story's world and the two texts … as content "
             "students have encountered' is the whole instruction; the assurance that follows "
             "narrates the register rule at the teacher and names 'earlier units' while doing "
             "it"),
        ],
        "ch_04_canonical.json": [
            (6, "band:2",
             "Each student speaks for one to two minutes adopting that vocation's voice",
             "Each student speaks, adopting that vocation's voice",
             "register/clock",
             "the band's own 20–50 carries the time and the platform rescales it; the "
             "speaking task — one vocation per student, in voice — is untouched. The comma "
             "is punctuation the deletion strands, not new text"),
        ],
        "ch_05_canonical.json": [
            (9, "band:3",
             "Students spend the remaining time selecting a craft from their region and "
             "completing notes",
             "Students select a craft from their region and complete notes",
             "register/clock",
             "'the remaining time' is measured against a sitting length the plan does not "
             "know. The task — choose a craft, note at least four of the eight planning "
             "points — is unchanged; only the two verbs the deletion stranded are re-formed"),
        ],
        "ch_07_canonical.json": [
            (2, "band:3",
             " — building a bridge toward the story's setting before reading begins", "",
             "register/forward",
             "the share itself is the teaching act: a surprising word, used in a sentence. "
             "What it bridges TOWARD is unknowable to a plan that may be served at any count"),
            (3, "band:3",
             " before comprehension questions are tackled in the next unit", "",
             "register/forward",
             "'a quick verbal check of first impressions' closes on its own ground"),
            (7, "band:2",
             " — a personal response that anchors the analytical work in the following unit",
             "", "register/forward",
             "the two-to-three sentences on the ending stand as their own output; the "
             "analytical work may sit in the next unit, in a borrowed one, or nowhere"),
            (8, "band:3",
             " — so students know what the next unit will feel like", "",
             "register/forward",
             "PARTIAL BY DESIGN — see the header. This strikes the unknowable claim about the "
             "next unit; the band's preview purpose survives and is referred to the human "
             "gate rather than repaired here"),
        ],
        "ch_08_canonical.json": [
            (7, "teacher_notes",
             " — all without requiring any specific earlier activity to have occurred", "",
             "register/meta-leak",
             "synthesis unit. The three things it brings together are named before the dash; "
             "the assurance is the rule narrated back. The sentences that follow already say "
             "the unit runs without the shiuli research, concretely and usefully"),
        ],
        "ch_11_canonical.json": [
            (8, "teacher_notes",
             " before the writing task in a later unit requires students to include an aside "
             "of their own", "",
             "register/forward",
             "the aside/soliloquy distinction 'is worth pinning down here' — the reason is "
             "the confusion itself, which is true at any count. Whether a later unit demands "
             "an aside depends on what X the teacher is served"),
        ],
        "ch_14_canonical.json": [
            (9, "teacher_notes",
             " — without assuming any specific earlier activity or written work", "",
             "register/meta-leak",
             "synthesis unit. The list of what the debate draws on ends at 'quality over "
             "quantity'; the assurance adds nothing a teacher acts on"),
            (9, "band:0",
             " — without requiring that any particular earlier activity be recalled", "",
             "register/meta-leak",
             "same unit, the opening band. The sentence-completion round and the three images "
             "it surfaces are the activity; the trailing clause is the rule spoken aloud"),
        ],
        "ch_15_canonical.json": [
            (8, "band:0",
             "working through all five sections:", "working through the sections:",
             "register/completion",
             "'all five' asserts a completion the band cannot guarantee once its 0–25 is "
             "rescaled to a shorter sitting. The five are named immediately after the colon, "
             "so nothing is lost — only the promise that every one gets done"),
        ],
        "ch_16_canonical.json": [
            (1, "teacher_notes",
             "No prior activity is assumed; the pre-reading prompts here are entirely "
             "self-contained.",
             "The pre-reading prompts here are entirely self-contained.",
             "register/meta-leak",
             "unit 1 — there IS no prior activity to assume, which is what makes the "
             "assurance pure noise. The second half is a real and useful statement about the "
             "prompts and is kept; only its capital is restored"),
            (9, "band:0",
             " without assuming any specific prior activity", "",
             "register/meta-leak",
             "synthesis unit. 'This surfaces the chapter's analytical work' is the sentence; "
             "the qualifier is the rule narrated"),
        ],
    },
    # ── v1.8, 2026-08-14 · S11 · english IX · the SIX RE-BOUGHT FLOOR COMPACTS ──────
    #
    # 3 ban hits in 6 fresh plans — clock 2, forward 1. The rate is flat against W1
    # (14/15) and W2 (15/23), which is the expected result and worth stating plainly: all
    # three source fixes made this week were to the PIPELINE (STEP 6's compound-item guard,
    # the brief/certifier registry split, normalize_options' scalar answer). Nothing
    # upstream of the model changed, so nothing about the model's output should have.
    # The register families are a CONSTITUTION problem and will keep arriving until the
    # constitution is amended.
    ("english", "ix"): {
        "ch_06_canonical_p05.json": [
            (5, "band:2",
             "spend the remaining time brainstorming three to four guiding research questions",
             "brainstorm three to four guiding research questions",
             "register/clock",
             "the mini-project orientation. 'three to four' is the real bound and it survives; "
             "'the remaining time' measures against a sitting length the plan cannot know"),
        ],
        "ch_08_canonical_p05.json": [
            (4, "band:2", " for two or three minutes", "", "register/clock",
             "'Students prepare for Speaking Activity — I (p.133) individually, noting their "
             "memorable object, song, or place and the five prompts' — the five prompts are "
             "the scope. Note the SAME band already says partners speak 'for an unhurried "
             "stretch', which is how the register wants duration expressed"),
        ],
        "ch_10_canonical_p06.json": [
            (5, "teacher_notes",
             " — the poster creation task in the following unit is a separate, independent act "
             "and students do not need today's slogans to complete it", "",
             "register/forward",
             "the clause is trying to do the register's own work — asserting independence — and "
             "breaks it twice doing so, naming 'the following unit' and 'today'. The sentence "
             "before it stands: the slogan task is a full cycle inside its own minutes, which "
             "is the fact that MAKES it independent. Same shape as the meta-leak family: the "
             "rule narrated instead of obeyed"),
        ],
    },
    # ── v1.7, 2026-08-14 · S11 · english IX · the wave-2 COMPACTS ────────────────────
    #
    # 15 ban hits across 12 of the 23 compacts. The census is the interesting half, read
    # against wave 1's (meta-leak 6 · forward 5 · clock 2 · completion 1):
    #
    #     forward     6      clock       7      meta-leak   1      completion  1
    #
    # THE META-LEAK FAMILY ALL BUT VANISHED — 6 in 15 tops, 1 in 23 compacts. That is not
    # luck: 5 of wave 1's 6 sat on SYNTHESIS units, and a compact has none (§0.3 reserves
    # the token to the standard). It is direct evidence that the leak is produced by the
    # synthesis unit's independence pressure rather than by the register block in general
    # — which is the argument for fixing it in the constitution at the synthesis mandate,
    # not by widening the ban.
    #
    # CLOCK OVERTOOK IT, and for a reason worth recording: 5 of the 7 are "the remaining
    # time" or "for N minutes" inside a band that is doing MORE work than the standard's
    # equivalent, because a compact folds two spines into one unit. The phrase is the
    # model reaching for a way to say "this is the elastic part" — which the platform
    # already handles by rescaling the band. All are pure deletions.
    #
    # All 15 delete or contract without inventing a clause. Where a deletion strands a
    # verb or a preposition the replacement is stated in full and named in its note.
    # APPLIED 2026-08-14 to the 23 wave-2 compacts (15 hits -> 0). Stale by design.
    ("english", "ix", "APPLIED-20260814-wave2-compacts"): {
        "ch_03_canonical_p08.json": [
            (1, "band:3", " before the reading is consolidated in the next unit", "",
             "register/forward",
             "the oral comprehension check is complete in itself; where consolidation "
             "happens depends on the count served"),
            (2, "band:2",
             " This oral consolidation prepares the class for the close-reading work in "
             "the next unit.", "",
             "register/forward",
             "whole trailing sentence. Tracing Sentila's journey aloud is the teaching "
             "act and the band closes on it"),
        ],
        "ch_03_canonical_p11.json": [
            (10, "band:0", " for a few minutes", "", "register/clock",
             "the band's own 0-10 carries it; 'brainstorm individually … and jot down key "
             "words' is unchanged"),
        ],
        "ch_04_canonical_p04.json": [
            (4, "band:0", " for about one to two minutes", "", "register/clock",
             "same speaking activity as the top's U6, same repair. Each student still "
             "'prepares to speak as that vocation's representative'"),
        ],
        "ch_05_canonical_p06.json": [
            (6, "band:3", " within the remaining time", "", "register/clock",
             "'identify their chosen craft and note the first three headings' is the "
             "instruction and the count of headings is the real bound, not the clock"),
        ],
        "ch_06_canonical_p04.json": [
            (4, "band:2",
             "Students spend the remaining time reading the options, asking questions, and "
             "writing",
             "Students read the options, ask questions, and write",
             "register/clock",
             "the three acts and the two-or-three bullet plan survive intact; only the "
             "verbs the deletion stranded are re-formed"),
        ],
        "ch_07_canonical_p14.json": [
            (12, "band:1", " for three minutes", "", "register/clock",
             "'plan their article (key idea per paragraph in two to three words), then "
             "draft all four paragraphs' — the word budget is the real constraint"),
        ],
        "ch_09_canonical_p09.json": [
            (2, "teacher_notes",
             " Having read the interview aloud, students are now well placed to "
             "distinguish fact from opinion in the next unit.", "",
             "register/forward",
             "whole trailing sentence. The two notes before it — the Arjuna/Khel Ratna "
             "confusion and the seven-row fact table — are what the teacher needs"),
        ],
        "ch_10_canonical_p05.json": [
            (2, "teacher_notes", " before the extract-based work in the following unit", "",
             "register/forward",
             "the homework stands on its own stated purpose ('to consolidate unfamiliar "
             "vocabulary'); what follows it is unknowable at authoring"),
        ],
        "ch_13_canonical_p12.json": [
            (12, "teacher_notes",
             "Students who wrote condolence messages in the writing unit will notice the "
             "form overlaps in occasion but diverges sharply in register and length; that "
             "contrast is pedagogically valuable and worth naming aloud.",
             "The condolence message overlaps the telegram in occasion but diverges "
             "sharply in register and length; that contrast is pedagogically valuable and "
             "worth naming aloud.",
             "register/forward",
             "the CONTRAST is real teaching and must survive; only its dependency on "
             "students having written condolence messages in an earlier unit is removed. "
             "The note's own last sentence already says the telegram task stands alone"),
        ],
        "ch_14_canonical_p05.json": [
            (2, "teacher_notes", " before the next unit teaches device analysis further",
             "", "register/forward",
             "phrases (v)-(vii) are set as self-study; the deadline is the reference, and "
             "it names a unit that may not be served"),
        ],
        "ch_14_canonical_p07.json": [
            (6, "band:2", " within the remaining time", "", "register/clock",
             "'writers note feedback and complete or revise their draft' — the peer-response "
             "checklist above it is the real scope"),
        ],
        "ch_15_canonical_p05.json": [
            (2, "teacher_notes",
             "are richer than can be done well in the remaining time; they are set as "
             "homework",
             "are richer than can be done well in class; they are set as homework",
             "register/clock",
             "the JUDGEMENT is the teaching content and is kept — three extended answers do "
             "not fit a sitting. 'in class' says it without measuring against a clock the "
             "plan does not know"),
        ],
        "ch_15_canonical_p07.json": [
            (7, "teacher_notes",
             " Both are completed within this unit so no prior artefact is required.",
             " Both are completed within this unit.",
             "register/meta-leak",
             "the only meta-leak in wave 2. 'Both are completed within this unit' is a real "
             "and useful scoping fact and stays; the assurance drawn from it is the rule "
             "narrated. The sentence after it already says there is no dependency, "
             "concretely"),
            (7, "band:0",
             "told they will complete all five sections in a condensed written-and-drawn "
             "form today",
             "told they will work through the five sections in a condensed "
             "written-and-drawn form",
             "register/completion",
             "same defect as the top's U8 and the same repair. The five are named in the "
             "sentence before, so nothing is lost but the promise that every one is "
             "finished; 'today' also goes, as a calendar reference in the same clause"),
        ],
    },
    # ── SUPERSEDED — applied 2026-08-13 to the S10 PILOT library (english VI ch 8,
    #    "What a Bird Thought"). Moved off the live 2-tuple key 2026-08-15 so the W1
    #    batch set below can own ("english", "vi"); re-running it would fail its own
    #    "declared text not found" assertion, which is the guard working.
    ("english", "vi", "SUPERSEDED_pilot_applied_20260813"): {
        "ch_08_canonical.json": [
            (12, "teacher_notes", " within these forty minutes", "", "register/clock",
             "the synthesis unit is the one unit designed to be borrowed, so its text travels "
             "to sittings of every length; 'has everything they need' survives the deletion"),
        ],
        "ch_08_canonical_p10.json": [
            (9, "teacher_notes", " and worth five minutes", "", "register/clock",
             "'genuinely philosophical' is the judgement the teacher needs; the minute budget "
             "is the platform's to set, not the plan's"),
        ],
    },

    # ══ v1.6, 2026-08-15 · S10 · english MIDDLE · BATCH WAVE 1 (the 45 top canonicals) ══
    #
    # 36 ban hits over 22 of the 46 chapters — ~1 breach per 2 files, against S5's 1-per-3.
    # Family split, and it is the first library where META-LEAK is the LARGEST family:
    # 17 meta-leak · 11 forward · 8 clock. Two founder rulings shape what follows.
    #
    # RULING 1 (2026-08-15) — FIVE HITS ARE NOT REPAIRED, and are not scanner changes
    # either: "ignore it, no repair needed". Three are the `bridges? (to|toward) the`
    # pattern firing where nothing points forward — vi ch 1 U6 "a bridge to the phonics
    # work FROM the speaking unit" (a BACKWARD reference, legal since v1.10), vii ch 2 U10
    # "a genuine bridge to the science curriculum" (cross-curricular), viii ch 6 U1 "bridge
    # to the text" (into this unit's own text). Two are the meta-leak disclaimer regex
    # spanning a semicolon into an unrelated clause — vii ch 2 U9 (the disclaimer's object
    # is "prepared specimens", a materials fact) and vii ch 6 U7 (its object is "revision
    # time"). Left as authored, deliberately, and left flagged: the next english library
    # re-raises them, which is the cheaper error than a pattern quietly narrowed.
    #
    # RULING 2 (2026-08-15) — THE META-LEAK DOCTRINE, stated once and applied to all 15:
    # KEEP THE SCOPING FACT, CUT THE ASSURANCE DRAWN FROM IT. "Both writing tasks begin and
    # conclude within this unit; no prior draft or previously produced material is required"
    # keeps its first clause and loses its second. The first is a fact a teacher acts on;
    # the second tells her there is a version of her lesson in which she could not have.
    # This is the english·IX p07 precedent (wave 2, S11) promoted to a rule.
    #
    # FIVE EDITS BELOW WERE NOT FLAGGED BY THE SCANNER — found by reading the whole note
    # once its flagged sibling was located (vi ch 9 U11, vii ch 4 U12, viii ch 5 U9,
    # viii ch 11 U11, viii ch 12 U9). Every one is a second disclaimer in the SAME
    # teacher_notes as a flagged one. This is runbook trap 1's shape in a new place — the
    # paraphrase that survives the sweep — and it is why the census is read per FILE and
    # not per hit. 31 flagged + 5 read = 36 edits.
    #
    # THE CAUSE IS FIXED SEPARATELY AND UPSTREAM (2026-08-15, same day): the meta-leak was
    # created by `variant_plans._serving_block()` stating self-containment as three
    # prohibitions with their rationale attached, which the model echoed back as
    # teacher-facing prose. Measured: 0 self-containment disclaimers in the 385 units of
    # the pre-brief corpus (backup/saved_plans/) against 67 in 2297 authored units. The
    # brief is reworded positively and gains an explicit "the serve model is never the
    # teacher's business" line. FOUNDER RULING: no constitution is touched for a defect
    # the brief created. So THESE 36 REPAIRS ARE THE LAST OF THEIR KIND ON THIS STAGE —
    # W2's compacts are authored under the corrected brief and are the live test of it.
    ("english", "vi", "SUPERSEDED_W1_applied_20260815"): {
        "ch_03_canonical.json": [
            (8, "teacher_notes", " in the speaking unit", "", "register/forward",
             "the CONTENT ('have spoken with contractions') is the continuity the teacher "
             "needs and it survives whole; 'the speaking unit' is a POSITION, and a class "
             "served a different X may never have had it. v1.10's rule exactly: name the "
             "content already taught, never a unit's existence"),
        ],
        "ch_04_canonical.json": [
            (4, "band:1",
             " then spend the remaining time on a class discussion of the open question",
             " then move to a class discussion of the open question",
             "register/clock",
             "the SEQUENCE (analogy and fill-in quickly, then discussion) is the teaching "
             "act and is kept; 'the remaining time' measures against a budget the platform "
             "rescales, so it is false in every sitting but the authored one"),
            (11, "teacher_notes",
             " — but it begins fresh: no prior discussion or homework is assumed", "",
             "register/meta-leak",
             "the list of what the unit draws on ends at 'the grammar of connection' and "
             "reads better closed there. The scoping fact survives in the NEXT sentence, "
             "which is kept in full: 'The reflective writing in the third band is new work "
             "begun and completed here'"),
        ],
        "ch_06_canonical.json": [
            (6, "teacher_notes",
             " without requiring any prior unit to have occurred", "",
             "register/meta-leak",
             "'keeps the thematic thread alive' is the judgement; the assurance is the "
             "brief narrated back"),
            (7, "teacher_notes",
             " without requiring any specific prior discussion to have taken place", "",
             "register/meta-leak",
             "same shape. 'anchors the abstract discussion in concrete narrative examples' "
             "is the whole of what a teacher acts on"),
            (8, "teacher_notes",
             "; no prior draft or previously produced material is required", "",
             "register/meta-leak",
             "THE DOCTRINE CASE. 'Both writing tasks begin and conclude within this unit' "
             "is a real scoping fact and stays; the clause after the semicolon is the same "
             "fact restated as a promise to the teacher"),
        ],
        "ch_09_canonical.json": [
            (11, "teacher_notes",
             " — so students can connect ideas regardless of which activities their class "
             "covered", "",
             "register/meta-leak",
             "NOT FLAGGED — read alongside its sibling below. 'which activities their class "
             "covered' is the serve model addressed to the teacher; the list of chapter "
             "content before the dash is what she needs"),
            (11, "teacher_notes", ", requiring no prior draft", "",
             "register/meta-leak",
             "the scoping half is kept whole — 'new and complete within this unit: it "
             "begins, develops, and ends here' already says it, concretely and twice"),
        ],
        "ch_12_canonical.json": [
            (6, "teacher_notes",
             " — students can connect across these strands regardless of which units they "
             "previously encountered", "",
             "register/meta-leak",
             "the three strands are named in the sentence and stand; 'which units they "
             "previously encountered' is a fact about OUR selection, not her class"),
        ],
        "ch_13_canonical.json": [
            (5, "band:2", ", each for about two to three minutes", "", "register/clock",
             "a RANGED clock quantity (ARV-D-026's family). 'Five or six students present "
             "to the class' carries the grouping, which is what the band is for"),
        ],
    },
    ("english", "vii", "SUPERSEDED_W1_applied_20260815"): {
        "ch_01_canonical.json": [
            (8, "band:3", " in the following unit", "", "register/forward",
             "the teaching act is collecting the notebooks and commenting; WHEN they come "
             "back is a promise no borrowed sitting can keep"),
        ],
        "ch_02_canonical.json": [
            (1, "band:2", " before the next unit's closer analysis", "",
             "register/forward",
             "'so students can visualise the action' is the reason for the pause and stands "
             "alone. U1 is the likeliest unit of any plan to be somebody's LAST sitting"),
        ],
        "ch_03_canonical.json": [
            (4, "band:0", " for a few minutes", "", "register/clock",
             "'respond freely … to warm up the reflective register' is the instruction; the "
             "band already carries 0-8"),
        ],
        "ch_04_canonical.json": [
            (12, "teacher_notes",
             " — without assuming any particular activity happened in a specific unit", "",
             "register/meta-leak",
             "the three ideas the synthesis draws together are named and kept"),
            (12, "teacher_notes",
             "; no prior writing is continued or handed back", "",
             "register/meta-leak",
             "NOT FLAGGED — the second disclaimer in the same note. 'planned, drafted, and "
             "completed within this unit' is the scoping fact and is kept"),
        ],
        "ch_06_canonical.json": [
            (8, "teacher_notes", " and the next unit", "", "register/forward",
             "'left for self-study' is true in every serve; naming where the rest lands is "
             "true only in this one"),
        ],
        "ch_10_canonical.json": [
            (4, "band:3", " within the remaining time", "", "register/clock",
             "'Students revise' is the act"),
            (7, "band:2", " within the remaining time", "", "register/clock",
             "same phrase, same deletion; the volunteers' share after it is kept and gives "
             "the band its close"),
        ],
        "ch_12_canonical.json": [
            (8, "teacher_notes",
             " without requiring any specific activity from earlier units to have happened "
             "in a particular form", "",
             "register/meta-leak",
             "the four strands students connect are named immediately before and are the "
             "whole of the guidance"),
        ],
    },
    # ══ v1.7, 2026-08-15 · S10 · english MIDDLE · BATCH WAVE 2 (the 72 compacts) ═══════
    #
    # 14 ban hits over 11 files — 7 forward · 3 clock · 1 meta-leak · 1 completion ·
    # 1 calendar. THE HEADLINE IS THE FAMILY THAT DID NOT APPEAR. These 72 files are the
    # first authored under the corrected `variant_plans._serving_block()` (2026-08-15), and
    # meta-leak fell 40.5 → 2.1 per 1000 units against W1's tops: 17 hits became 1. The
    # brief was the cause, exactly as the pre-brief corpus predicted, and rewording it at
    # source did in one edit what 36 declared repairs did after the fact.
    #
    # TWO OF THE 14 ARE NOT DECLARED — they are put to the founder as false positives
    # rather than repaired, because striking them would falsify chapter content (runbook
    # trap 4: a false positive is fixed at the scanner, not in the text):
    #   · vii ch 2 p06 U1 [forward] "foreshadow" — the pre-reading pictures foreshadow the
    #     poem's spider metaphor, and the poem is READ IN THIS SAME UNIT. Nothing points at
    #     another sitting. The pattern has no same-unit exemption.
    #   · vii ch 3 p07 U3 [calendar] "tomorrow" — this is Helen Keller's own argument
    #     ("use their eyes as if tomorrow they might be blind"), paraphrased from p.33. The
    #     word is the ESSAY'S, not a scheduling reference. The scanner drops a calendar hit
    #     to advisory inside quotation marks; this one is a close paraphrase and misses the
    #     exemption by its punctuation alone.
    # A third stays by the 2026-08-15 bridge ruling: viii ch 14 p09 U6's "bridge to the
    # space-travel speaking task". Its unit's REAL breach is declared below.
    #
    # ONE EDIT WAS NOT FLAGGED, same reading discipline as W1: viii ch 14 p09 U6's closing
    # sentence is a plain forward reference AND narrates the constraint, and the scanner
    # stopped at "bridge to the" three clauses earlier. 11 flagged + 1 read = 12 edits.
    ("english", "vi"): {
        "ch_04_canonical_p07.json": [
            (1, "band:3", " that will follow when they return to the text", "",
             "register/forward",
             "holding an image in mind IS the closing act and needs no destination; U1 of a "
             "7-period compact is a likely last sitting"),
        ],
        "ch_05_canonical_p09.json": [
            (2, "teacher_notes",
             " before the more demanding extract analysis in the next unit", "",
             "register/forward",
             "'they build confidence' is the pedagogical point and stands; what it builds "
             "confidence FOR is a claim about a sitting this class may not receive"),
            (8, "teacher_notes", "; no prior material is assumed", "",
             "register/meta-leak",
             "THE ONE SURVIVING META-LEAK IN THE WHOLE WAVE, and it takes the same doctrine "
             "as W1's fifteen: 'All making and displaying happens within this sitting' is "
             "the scoping fact and is kept whole"),
        ],
        "ch_06_canonical_p07.json": [
            (7, "teacher_notes",
             "vocabulary built across the chapter", "the chapter's vocabulary",
             "register/completion",
             "U7 of 7 — the last unit of a compact, where a claim that the chapter was "
             "worked through is exactly what the completion ban exists for. The qualities "
             "are NAMED in the next clause ('loyal, caring, honest'), which is the "
             "content-naming the register asks for, so nothing is lost"),
        ],
        "ch_06_canonical_p10.json": [
            (3, "teacher_notes",
             " are addressed in the following unit", " are not taken up here",
             "register/forward",
             "the W1 viii ch 12 U2 shape, and the same remedy: deleting the clause leaves "
             "'The remaining questions are addressed', which asserts the opposite of the "
             "truth. Stated from this unit's own ground instead"),
            (4, "band:2", " for the remaining time", "", "register/clock",
             "the band already carries its minutes, and the sentence after it ('completed "
             "as homework') is where the work actually lands"),
        ],
    },
    ("english", "vii"): {
        "ch_07_canonical_p05.json": [
            (4, "band:3", " in the remaining time", "", "register/clock",
             "'Writers revise that section' is the act; the peer-response instructions "
             "before it are untouched"),
        ],
        "ch_09_canonical_p08.json": [
            (5, "teacher_notes",
             "; carry-over to a later unit is not intended", "",
             "register/forward",
             "BOTH bans in one clause — a forward reference AND the constraint narrated. "
             "'fully drafted, peer-reviewed, and revised within this sitting' is the "
             "scoping fact, is kept, and already says everything the struck clause said"),
        ],
    },
    ("english", "viii"): {
        "ch_07_canonical_p09.json": [
            (2, "teacher_notes",
             " — the fact-vs-opinion task in the next unit will build on this distinction",
             "", "register/forward",
             "'Watch for students who conflate fact and opinion' is the whole of what the "
             "teacher acts on"),
            (7, "band:3", " to the next unit", "", "register/forward",
             "homework set and answers brought back is the act; WHICH sitting they are "
             "brought to is not this plan's to promise"),
        ],
        "ch_10_canonical_p08.json": [
            (5, "band:0", " for two minutes", "", "register/clock",
             "'Pairs share any prior knowledge' is the act. Note the five guiding points "
             "and the Van Mahotsav framing are untouched"),
        ],
        "ch_14_canonical_p09.json": [
            (6, "teacher_notes",
             " The writing task on dialogue between Deepa and Asma is taken up in the next "
             "sitting and should not be previewed here.", "",
             "register/forward",
             "NOT FLAGGED — the scanner stopped at 'bridge to the' three clauses earlier "
             "(and that hit stands, per the 2026-08-15 bridge ruling). This sentence is the "
             "unit's real breach and is a double one: it names a later sitting AND tells "
             "the teacher what the plan is withholding, which is the brief talking"),
        ],
    },
    ("english", "viii", "SUPERSEDED_W1_applied_20260815"): {
        "ch_01_canonical.json": [
            (7, "band:2", "spend the remaining time drafting", "draft", "register/clock",
             "the OUTLINE and its three parts are the teaching content and are untouched"),
        ],
        "ch_04_canonical.json": [
            (5, "band:1", " for roughly one to two minutes", "", "register/clock",
             "'Presenters speak' and the teacher's one-strength-one-suggestion response are "
             "the act; the duration is the platform's"),
            (8, "teacher_notes",
             " — but it does not assume any specific prior activity happened in any "
             "particular form", "",
             "register/meta-leak",
             "everything the chapter taught is listed before the dash and kept. Note what "
             "is NOT touched two sentences later: 'where they have not done the research, "
             "the class discussion and oral presentations carry the synthesis on their "
             "own' is real differentiation guidance, and 'the board map … requires nothing "
             "prepared in advance' is a materials fact — both stay"),
        ],
        "ch_05_canonical.json": [
            (9, "teacher_notes",
             " without assuming any specific earlier activity has taken place;", "",
             "register/meta-leak",
             "the clause AFTER the semicolon is the good half and is kept — 'every concept "
             "referenced here is grounded in the poem's own lines' is a substantive claim "
             "about the unit's self-sufficiency stated as CONTENT, which is the form the "
             "register wants"),
            (9, "teacher_notes",
             ": students are not continuing an earlier draft but composing a fresh, compact "
             "piece that demonstrates",
             ": a fresh, compact piece that demonstrates",
             "register/meta-leak",
             "NOT FLAGGED — the second disclaimer in the same note. 'designed to begin and "
             "end within this unit' is kept; the negative half is the only clause cut, and "
             "the sentence closes on what the piece IS"),
        ],
        "ch_10_canonical.json": [
            (10, "band:2", " for eight to ten minutes", "", "register/clock",
             "the length spec that MATTERS is kept ('five to seven sentences') — it is a "
             "quantity of work, not of clock. The band's closing sentence, 'Students begin "
             "and complete the piece within this band', is scoping and stays"),
        ],
        "ch_11_canonical.json": [
            (1, "teacher_notes",
             " No prior reading or homework is assumed for this encounter.", "",
             "register/meta-leak",
             "U1 of the plan, and the leak with the least excuse: there IS no prior unit "
             "to assume, which is what makes the assurance pure noise. Nothing is kept "
             "because nothing in the sentence is about the lesson"),
            (11, "teacher_notes",
             " — without assuming any specific prior activity, discussion, or written "
             "piece", "",
             "register/meta-leak",
             "the five strands the synthesis draws together are named and kept"),
            (11, "teacher_notes",
             "; students who have engaged with any part of the chapter will have something "
             "to say, regardless of which path they took through it", "",
             "register/meta-leak",
             "NOT FLAGGED — the second disclaimer in the same note. 'which path they took "
             "through it' is the serve model in plain words. 'designed to begin and close "
             "entirely within this sitting' is kept, and the note still ends on the line "
             "that matters: 'The synthesis is not a test — it is a space to connect'"),
            (11, "band:3", "; no prior draft or homework is assumed", "",
             "register/meta-leak",
             "'Paragraphs are self-contained' is an instruction to students about the "
             "paragraph and stays; the assurance after it is addressed to us"),
        ],
        "ch_12_canonical.json": [
            (1, "teacher_notes", " for a later unit", "", "register/forward",
             "'rich but time-intensive and are set aside' is the judgement the teacher acts "
             "on — she needs to know they are NOT being done here, not where they go"),
            (2, "teacher_notes",
             " are addressed in a later unit", " are not taken up here",
             "register/forward",
             "THE ONE REPLACEMENT IN THIS SET, and it is declared as such. A pure deletion "
             "leaves 'The deeper analytical questions … are addressed.', which asserts the "
             "opposite of the truth. The replacement says the same thing the other four "
             "ch 12 hits say after deletion, from this unit's own ground"),
            (3, "teacher_notes", ", which is explored in a later unit", "",
             "register/forward",
             "the CONNECTION to the fallowing material is the teaching point and is kept; "
             "only its scheduling goes"),
            (7, "teacher_notes",
             " to allow sufficient time in the next unit for the ten-blank production "
             "exercise on tenses", "",
             "register/forward",
             "'The tense identification task is set as homework' stands; the reason is a "
             "claim about a sitting this class may never receive"),
            (9, "teacher_notes", ", not from any assumed prior activity", "",
             "register/meta-leak",
             "'all content from the chapter' is the true and useful half"),
            (9, "teacher_notes", " — no prior draft is assumed", "",
             "register/meta-leak",
             "NOT FLAGGED — the second disclaimer in the same note. 'The journal-entry "
             "writing task begins and ends within this unit' is the scoping fact and is "
             "kept whole"),
        ],
        "ch_14_canonical.json": [
            (11, "teacher_notes",
             " — it may name those concepts freely but must not assume any particular "
             "activity, discussion or written work a student produced in earlier units", "",
             "register/meta-leak",
             "the clearest case in the batch: 'must not assume' is the BRIEF's own "
             "imperative, printed into a note addressed to a teacher, who is not the party "
             "under the obligation. The three strands are named before the dash and kept"),
        ],
    },
    # ══ v1.8, 2026-08-15 · S11 · english PREPARATORY · BATCH WAVE 1 (the 38 tops) ══════
    #
    # 17 ban hits over 14 files — 8 clock · 6 forward · 2 meta-leak · 1 calendar, across
    # 39 chapters. 1 breach per 2.8 files, dead on the runbook's expected 1-in-3, and no
    # family is concentrated in one grade. 16 declared, 1 struck.
    #
    # THE CLOCK FAMILY IS THE HEADLINE, and it is a different shape from every previous
    # stage's. All 8 are a duration written into a READING or DISCUSSION instruction —
    # "re-read silently for two minutes", "brainstorm in pairs for a few minutes" — never
    # the boilerplate "for the remaining time" the earlier sets struck. That is a
    # preparatory-stage tell: at classes III–V the model reaches for a duration because
    # young children need the task bounded, which is correct teaching expressed in the one
    # unit the register cannot carry (proportional scaling falsifies it silently). Every
    # one is a pure deletion — the act, the grouping and the output all stand without it,
    # and the band's own `minutes` already bounds the task. Worth saying at the next
    # stage's brief rather than repairing forever.
    #
    # META-LEAK FELL TO 2, from W1·english-middle's 17. These 38 files were authored under
    # the corrected `variant_plans._serving_block()` (2026-08-15), and this is the second
    # corpus to confirm it: 1.6 per 1000 units here against 40.5 pre-fix. Both survivors
    # are the same shape as vi ch 5 p09 U8 and take the same doctrine — the scoping FACT
    # is kept, the narration of the constraint is struck.
    #
    # ONE IS NOT DECLARED — put to the founder as a false positive rather than repaired,
    # on the precedent set for this exact pattern at S10 (runbook trap 4: a false positive
    # is fixed at the scanner, not in the text):
    #   · iii ch 13 U2 [forward] "foreshadows" — "the tree's warning foreshadows Madhu's
    #     trouble" is narrative structure INSIDE the story, and both the warning and the
    #     trouble are read in this same unit's comprehension work. Nothing points at
    #     another sitting. IDENTICAL in shape to vii ch 2 p06 U1, struck at S10 for the
    #     same reason, and the third time `foreshadow\w*` has fired on literary content
    #     (maths·vii ch 7 U4 is a fourth, in-section). The pattern at register_scan.py:85
    #     bans `previewing` and `foreshadow\w*` together; `previewing` is earning its keep
    #     (v ch 9 U10 below is a true forward reference and IS declared), `foreshadow` has
    #     now produced four hits and no true positive. RECOMMENDED: split `foreshadow\w*`
    #     out to ADVISORY with a dated note, leaving `previewing` a ban. Not done here —
    #     a scanner change is the founder's call, and until it is made iii ch 13 will keep
    #     failing certification on a sentence that should stand.
    #
    # ONE JUDGEMENT CALL, declared but flagged: iv ch 6 U11's "could actually do tomorrow"
    # is a student-facing reflection about acting in their own life, not a claim about when
    # the lesson sits — closer to legal than not. It is repaired anyway because the repair
    # is lossless ("start doing" keeps the soon-and-actionable sense the prompt needs) and
    # leaving a bare calendar word in teacher-facing prose costs more than the edit. It is
    # NOT the S10 Helen Keller shape: that word was the essay's, this one is Aruvi's.
    ("english", "iii", "SUPERSEDED_W1_applied_20260815"): {
        "ch_03_canonical.json": [
            (1, "teacher_notes", "; meaning will deepen across later units", "",
             "register/forward",
             "'Resist the urge to explain every word during the first read' is the whole "
             "instruction and stands alone; where the meaning deepens is a claim about "
             "sittings this class may never receive"),
            (2, "band:0", " for two minutes", "", "register/clock",
             "the re-read is silent and self-limiting, and the band carries 0–6; the "
             "teacher's re-reading of the pit-and-rescue passage after it is untouched"),
        ],
        "ch_08_canonical.json": [
            (4, "band:4", " This bridges to the word-work activity on colour words.", "",
             "register/forward",
             "a 38–40 closing band in an 11-unit plan, and any unit may be a borrowed Xth "
             "or a last sitting. 'Teacher asks what colours the poem mentions and children "
             "call them out' is the complete reflection"),
        ],
    },
    ("english", "iv", "SUPERSEDED_W1_applied_20260815"): {
        "ch_01_canonical.json": [
            (5, "band:1", " for a few minutes", "", "register/clock",
             "'Small groups of three discuss, then each group nominates a spokesperson' "
             "carries the grouping and the output; the 6–22 band carries the time"),
        ],
        "ch_02_canonical.json": [
            (7, "teacher_notes",
             ", which supports the grammar and vocabulary work that follows in later units",
             "", "register/forward",
             "'a light bridge between word recognition and contextual use' already states "
             "what the activity does. What it feeds is the forward claim"),
        ],
        "ch_06_canonical.json": [
            (11, "band:3", " could actually do tomorrow", " could actually start doing",
             "register/calendar",
             "THE JUDGEMENT CALL described in the set header. 'Start doing' keeps the "
             "soon-and-actionable sense the reflection needs without naming a day; the "
             "homework sentence after it is untouched"),
        ],
        "ch_08_canonical.json": [
            (2, "band:0", " for two minutes", "", "register/clock",
             "'skim pp. 73–76 quietly, then invite one student to retell' is the act; the "
             "'in two sentences' bound on the retell is the real constraint and stands"),
            (3, "band:0", " for four minutes", "", "register/clock",
             "same unit-pair, same shape — 'paying attention to the sequence of match "
             "events' is what actually directs the re-read"),
        ],
        "ch_10_canonical.json": [
            (9, "band:3", " for a few minutes", "", "register/clock",
             "the gallery walk is bounded by the sticky-note each student leaves, not by "
             "a duration"),
        ],
    },
    ("english", "v", "SUPERSEDED_W1_applied_20260815"): {
        "ch_01_canonical.json": [
            (10, "band:2", " for two minutes", "", "register/clock",
             "'Pairs discuss their guesses in whispers' is the act, and the band's own "
             "22–35 holds the time; the riddle, the withheld answer and the debate stand"),
        ],
        "ch_02_canonical.json": [
            (10, "band:0", " for two minutes", "", "register/clock",
             "'Students discuss in pairs to warm up for writing' keeps the purpose, which "
             "is what the band is for"),
            (16, "teacher_notes", " No prior artefact or draft is needed; each", " Each",
             "register/meta-leak",
             "ONE OF THE TWO SURVIVORS, and the vi ch 5 p09 U8 shape exactly: 'each "
             "mini-task begins and closes within its own few minutes' IS the scoping fact "
             "and is kept whole. What is struck is the sentence that narrates the "
             "constraint to a teacher who is not the party under it"),
        ],
        "ch_03_canonical.json": [
            (4, "band:0", " for a few minutes", "", "register/clock",
             "the brainstorm is bounded by the share-out that follows it, and the five "
             "expected answers (boat, bridge, ferry, stepping stones, swimming) stand"),
        ],
        "ch_05_canonical.json": [
            (11, "band:4",
             " without requiring any particular prior activity to have happened", "",
             "register/meta-leak",
             "the second survivor. 'This brief round-the-room closing celebrates the "
             "chapter's ideas' is the whole of what the teacher does; the trailing clause "
             "is the brief's independence requirement read back to her"),
        ],
        "ch_09_canonical.json": [
            (10, "teacher_notes",
             ", previewing the writing and beyond-text tasks that follow", "",
             "register/forward",
             "the true positive that earns `previewing` its place as a ban — it names two "
             "later sittings by their spine. 'Extends the poem's single-tool imagery "
             "(spade, lantern) to a much wider world of vocations' is the observation, and "
             "the stethoscope example after it is untouched"),
        ],
        "ch_10_canonical.json": [
            (1, "teacher_notes", " — comprehension tasks come in the next unit", "",
             "register/forward",
             "U1 of an 11-unit plan and a likely first exposure either way. 'This is the "
             "text-encounter unit for the chapter, so unhurried reading aloud is the "
             "priority' says why without naming what follows"),
        ],
    },
    # ══ v1.9, 2026-08-15 · S11 · english PREPARATORY · BATCH WAVE 2 (the 70 compacts) ══
    #
    # 32 ban hits over 24 of the 70 compacts — 19 clock · 9 forward · 2 completion ·
    # 2 meta-leak. 1 breach per 2.9 files, statistically identical to W1's 1-per-2.8 on the
    # tops. (The stage census reads 33/25 because it also counts iii ch 13's `foreshadows`,
    # a TOP, ruled ignore by the founder 2026-08-15.) 29 declared, 3 struck.
    #
    # CLOCK IS AGAIN THE LARGEST FAMILY AND AGAIN THE SAME SHAPE — 19 of 32, every one a
    # duration inside a reading or discussion instruction ("discuss in pairs for two
    # minutes", "think quietly for two minutes"), never the "for the remaining time"
    # boilerplate the middle-stage sets struck. Two waves now say the same thing: at classes
    # III–V the model bounds a task with a duration because young children need it bounded,
    # which is correct teaching in the one unit the register cannot carry. It is 19 of 32
    # here after 8 of 17 in W1, so the pressure RISES on compacts — a shorter plan makes
    # every band feel tighter. This is a BRIEF problem, not a model problem, and the next
    # preparatory stage should say so in the brief rather than pay for 27 repairs again.
    #
    # META-LEAK HELD AT 2, exactly as in W1, on 70 files instead of 38 — 1.6 → 0.9 per 1000
    # units. Third corpus confirming the corrected `variant_plans._serving_block()`
    # (2026-08-15). Both are the vi ch 5 p09 U8 shape and take the same doctrine.
    #
    # COMPLETION APPEARED FOR THE FIRST TIME AT THIS STAGE — 2 hits, both in a compact's
    # CLOSING unit ("built across the chapter"). It is absent from W1's tops for a
    # structural reason worth recording: a top's closing unit is the mandated `synthesis`,
    # which the completion ban EXEMPTS by design (build_library.py, "licensed to assume the
    # chapter's CONTENT has been taught"). A compact is FORBIDDEN a synthesis anchor, so its
    # last unit does the same summing-up job with none of the licence. Expect this family on
    # every compact wave; it will never show on a top.
    #
    # THREE ARE NOT DECLARED — all three the `bridges? (toward|towards|to) the` pattern
    # (register_scan.py:184), and all three pointing somewhere that is NOT a later sitting
    # (runbook trap 4: a false positive is fixed at the scanner, not in the text):
    #   · iv ch 11 p09 U6 band:2 "Bridge to the body-part task" — the body-part task is
    #     band:3 OF THE SAME UNIT, 18–20 → 20–35. Two minutes later, same sitting.
    #   · iv ch 5 p08 U8 "a natural bridge to the adverb work explored EARLIER in the
    #     chapter" — a BACKWARD reference, which v1.10 legalised outright. The pattern
    #     matches on "bridge to the" and never reads the direction word four tokens on.
    #   · iii ch 9 p07 U3 "an oral bridge to the story's THEME, not an assessed task" — the
    #     destination is a theme, not a unit, and the clause says in terms that nothing is
    #     being deferred.
    # The 2026-08-15 bridge ruling is NOT disturbed: viii ch 14 p09 U6's "bridge to the
    # space-travel speaking task" named a real later sitting and rightly stands. These three
    # do not. RECOMMENDED: do not fire when the destination is qualified backward
    # ("earlier", "in the previous"), and the same-unit case argues for reading the band
    # index. Deliberately NOT word-swapped to dodge the regex — "bridge" → "link" would
    # clean the corpus while leaving the pattern broken for the next stage to rediscover.
    ("english", "iii"): {
        "ch_03_canonical_p10.json": [
            (10, "teacher_notes", " built across the chapter", "", "register/completion",
             "the first of the two completion hits. U10 of a p10 compact is its LAST unit "
             "but carries no synthesis licence. The five strands are NAMED in the same "
             "sentence and all survive; what goes is the claim that a chapter was worked "
             "through, which is false whenever this plan is a teacher's first exposure"),
        ],
        "ch_04_canonical_p09.json": [
            (2, "band:0", " for two minutes", "", "register/clock",
             "'re-read pp.25–28 silently, then asks Who are the four friends' is the whole "
             "move; the band's own 0–6 holds the time"),
        ],
        "ch_08_canonical_p09.json": [
            (4, "teacher_notes", " that follows later", "", "register/forward",
             "'links the poem to the word-work on describing words' is a true statement "
             "about the chapter's shape; WHEN that word-work happens is the breach"),
        ],
        "ch_12_canonical_p07.json": [
            (4, "band:1", " for two minutes", "", "register/clock",
             "the thinking is bounded by the turn that follows it — 'each takes a short "
             "turn' — and the sentence frame is untouched"),
        ],
        "ch_16_canonical_p07.json": [
            (1, "teacher_notes", " before answering questions in a later unit", "",
             "register/forward",
             "'worth slowing down on so students absorb the meaning' is the instruction "
             "and stands alone; the Chanda Mama / Sun warning after it is untouched"),
            (3, "band:2", " for two minutes", "", "register/clock",
             "'Students work in pairs, then share with the class' keeps the structure; the "
             "'I can see…' frame is the real scaffold and stays"),
        ],
        "ch_17_canonical_p09.json": [
            (3, "band:1", " for five minutes", "", "register/clock",
             "the brainstorm is bounded by its own output — a list of 10 items — and by the "
             "pair-into-four move that follows"),
        ],
    },
    ("english", "iv"): {
        "ch_01_canonical_p10.json": [
            (10, "band:3", " built across the chapter", "", "register/completion",
             "the second completion hit, same shape and same remedy. 'This revisits the "
             "recitation and oracy work' is true of any sitting that reaches U10; that it "
             "was built across a whole chapter is not"),
        ],
        "ch_02_canonical_p11.json": [
            (5, "band:1", " for two minutes", "", "register/clock",
             "the two probing questions after it ('What did Kamala say…') are what actually "
             "shapes the discussion and are untouched"),
        ],
        "ch_06_canonical_p07.json": [
            (3, "band:0", " for a few minutes", "", "register/clock",
             "the two named discussion questions bound the task; the board-charting closes it"),
        ],
        "ch_06_canonical_p10.json": [
            (2, "band:3", " for two minutes", "", "register/clock",
             "FOUR HITS IN ONE FILE, the batch's densest, and all four the same reading- or "
             "discussion-duration shape. 'Students revisit the text independently to check "
             "one answer they are unsure about' is self-bounding"),
            (3, "band:2", " for two minutes", "", "register/clock",
             "the prompt is named in full before it; the board list closes it"),
            (8, "band:0", " for two minutes", "", "register/clock",
             "'study the five-panel picture story silently' is bounded by the panels "
             "themselves — five — and by the eliciting that follows"),
            (10, "band:1", " for three minutes", "", "register/clock",
             "the four charted answers (large-print notes, reading aloud, sitting nearer "
             "the board, describing pictures) are the real shape of this band"),
        ],
        "ch_10_canonical_p09.json": [
            (2, "band:1", " for two minutes", "", "register/clock",
             "bounded by the board list of swing materials the pairs feed"),
        ],
    },
    ("english", "v"): {
        "ch_03_canonical_p13.json": [
            (1, "teacher_notes", "; comprehension tasks follow in a later unit", "",
             "register/forward",
             "'This first encounter is entirely about sound and feel' already scopes the "
             "sitting from its own ground; the anaphoric-'But' note after it is the "
             "teaching and is untouched"),
            (3, "band:2", " for a few minutes", "", "register/clock",
             "'Pairs talk; then each pair shares one idea with the class' carries the whole "
             "structure"),
            (13, "band:1", " for five minutes", "", "register/clock",
             "the two groups and their assigned topics bound the task; the spokesperson "
             "share-out closes it"),
        ],
        "ch_04_canonical_p09.json": [
            (8, "band:2", " for two minutes", "", "register/clock",
             "bounded by 'then share in pairs' and the four-or-five report-backs"),
            (9, "teacher_notes", " without requiring any prior sitting to have occurred", "",
             "register/meta-leak",
             "ONE OF THE TWO SURVIVORS. 'The closing connection to the narrative theme of "
             "freedom and the natural world gives this final sitting its own coherent "
             "meaning' IS the scoping fact and is kept whole; the trailing clause is the "
             "brief's independence requirement read back to a teacher who is not the party "
             "under it"),
        ],
        "ch_05_canonical_p07.json": [
            (3, "teacher_notes", " in a later unit on that spine", "", "register/forward",
             "'the tongue twisters' repeated fr cluster will naturally lead into word-work "
             "on consonant patterns' is a true observation about the material; naming the "
             "sitting it lands in is the breach"),
        ],
        "ch_05_canonical_p09.json": [
            (3, "band:0", " for a couple of minutes", "", "register/clock",
             "a RANGED-adjacent phrasing the pattern list already covers; 'Children turn to "
             "a partner and share, then two pairs report' is the move"),
        ],
        "ch_06_canonical_p08.json": [
            (1, "teacher_notes",
             " Comprehension questions are reserved for the next unit so that listening and "
             "reading are unhurried here.", " Keep listening and reading unhurried here.",
             "register/forward",
             "THE ONE EDIT THAT REPLACES RATHER THAN DELETES. Deleting the sentence would "
             "lose 'unhurried', which is the actual instruction to the teacher — so the "
             "instruction is restated from this unit's own ground and only the deferral "
             "claim goes. The Oorani / Panam Keni / Tanka pronunciation note is untouched"),
            (8, "teacher_notes", " without requiring any preparation from an earlier unit", "",
             "register/meta-leak",
             "the second survivor. 'Brings the chapter's informational and imaginative "
             "strands together' is the whole of what the closing reflection does; the "
             "self-study flag on Task A after it is untouched"),
        ],
        "ch_06_canonical_p11.json": [
            (3, "band:2", " for two minutes", "", "register/clock",
             "bounded by the partner share and the four-to-five presentations"),
        ],
        "ch_07_canonical_p11.json": [
            (3, "band:1", " for two minutes", "", "register/clock",
             "the named prompt bounds it; the board note of varied reasons closes it"),
        ],
        "ch_07_canonical_p15.json": [
            (1, "teacher_notes", ", as word meaning is explored in a later unit", "",
             "register/forward",
             "'point them out without defining them fully yet' is the complete instruction "
             "— 'yet' already does the deferring without naming a sitting"),
        ],
        "ch_08_canonical_p08.json": [
            (2, "band:2", " for two minutes", "", "register/clock",
             "the two named questions bound the discussion; the board consolidation closes it"),
        ],
        "ch_09_canonical_p15.json": [
            (7, "band:2", " for two minutes", "", "register/clock",
             "'Students think quietly, then share in pairs first' keeps the two-stage shape "
             "the band is built on"),
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
    elif locator.startswith("materials:"):
        i = int(locator.split(":")[1])
        if new is None:
            return unit["materials"][i]
        unit["materials"][i] = new
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