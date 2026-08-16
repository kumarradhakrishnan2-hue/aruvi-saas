#!/usr/bin/env python3
"""repair_anchors.py — repair V2 section-anchor SERIALIZATION in an authored library (v1.0, 2026-08-03).

WHY THIS EXISTS, AND WHY IT IS NOT repair_register.py. The SS·IX ch 3 library (12/10/7) was
certified against a CORRUPTED registry: all three canonicals wrote the same two-section anchor
joined with a semicolon —

    "Weather and Climate; Elements of Weather and Climate"

— where V2 mandates " / " (serve._ANCHOR_JOINER). A semicolon is not split, so the string
entered section_registry as ONE opaque section. The derived registry still counted 9 entries
(which is why `registry_sections: 9` passed), but it carried a phantom composite at index 3,
had no standalone "Weather and Climate", and displaced "Elements of Weather and Climate" two
slots past its true position. Consequences: p10 was quarantined for a first-visit-order
"skip" that does not exist; X=8 reported a phantom dropped section; X=9 served a redundant
re-teach where the Case 1 synthesis belongs.

repair_register.py's docstring draws the line this script respects: STRUCTURAL and
PEDAGOGICAL defects — including "an anchor that names the wrong section" — are out of scope
there, because repairing them as text hygiene would launder content changes. This is neither.
The anchors name the RIGHT sections in the RIGHT order; only the DELIMITER between them is
wrong. Nothing about what is taught changes. That is a serialization repair, and it gets its
own tool so the two classes of edit never blur.

SAME SAFETY DOCTRINE as repair_register.py:
  * every edit is a STATED (old -> new) pair. No rule-based rewrite, no model authors text.
    A general "replace any separator with ' / '" normalizer is deliberately NOT what this
    does — that is a generated rewrite, and it would silently "fix" anchors nobody read.
  * if `old` is not found verbatim the file is left untouched and the run fails loudly.
  * the artefact records what was done in genon_canonical.repairs[], so corpus statistics can
    still separate generation quality from repair quality.
  * the registry is re-derived and printed after the write, because the whole point of the
    repair is the registry — a repair that leaves it wrong must be visible immediately.

    python3 genon/repair_anchors.py           # dry run: show the declared edits + both registries
    python3 genon/repair_anchors.py --apply   # back up, apply, record, re-derive
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from purge_derived import purge                                  # noqa: E402

from aruvi_core.genon import compile_stream                        # noqa: E402
from aruvi_core.genon.serve import (                               # noqa: E402
    _norm, is_synthesis_unit, section_registry, unit_range,
)

SAVED = REPO / "data" / "content" / "saved_plans"
QUAR = REPO / "backup" / "quarantine"
LIB = SAVED / "social_sciences" / "ix"          # rebound by main() per --subject/--grade
BACKUP = REPO / "backup" / "anchor_repair"
CHAPTER = 3                                     # rebound by main(); registry_of_library reads it

# THE ANCHOR FIELD IS NOT CALLED THE SAME THING ON EVERY STAGE (2026-08-12, S5). SS writes
# `section_anchor`; TWAU writes `section_ref` and the plugin mediates it. Reading only the
# first returns "" on TWAU, so every declared repair would refuse with "text not found" for a
# reason that has nothing to do with the text — the same seam `validate()`, the certifier and
# repair_register.py all had to grow.
_ANCHOR_FIELDS = ("section_anchor", "section_ref")


def _anchor_field(unit) -> str:
    for f in _ANCHOR_FIELDS:
        if f in unit:
            return f
    return _ANCHOR_FIELDS[0]

# ── the declared edits ───────────────────────────────────────────────────────────
# file -> [(unit_number, old_anchor, new_anchor, rule_broken, note)]
#
# Note p07 U3: the author wrote the semicolon composite AND then appended the standalone
# section — evidence the two sections were understood as two. A naive ";"->" / " swap would
# leave "Elements of Weather and Climate" duplicated in the anchor; the declared repair emits
# the clean two-section form instead. unit_range would have tolerated the duplicate (it takes
# min/max), but a duplicate anchor is not what V2 says and the next reader would trip on it.
REPAIRS = {
  # ── S2 · social_sciences · VIII · BATCH WAVE 2 TOKEN-DROPS — founder ruling 2026-08-16.
  # Six compacts were quarantined for anchoring sections the top registry does not contain.
  # Diagnosed unit by unit before any edit: of the eleven offending units, NINE also carry a
  # VALID registry anchor — the stray name sits BESIDE a correct one, at a finer granularity
  # than the standard chose. Those nine are dropped here. The other two — viii ch 8 p08 U3
  # ("Smaller water bodies and waterways") and p11 U3 ("Ocean currents / Ocean trenches") —
  # carry NO valid anchor and were first called unfixable orphans bound for F1. They are not:
  # see the note above their declarations. Both are re-anchored to the parent section the
  # registry already carries, and NOTHING from this wave now goes to F1 on anchor grounds.
  #
  # WHAT THIS DOES AND DOES NOT DO. Every dropped token names a real heading in the chapter
  # summary — the compacts did not invent content, the standards omitted it (15 of 41 chapters
  # omit at least one real summary section; 14 of those 15 are class VIII). The founder ruled
  # on 2026-08-16 that the top's editorial selection IS the contract, that a section the top
  # folds in is in all likelihood integrated into the lesson anyway, and that the only concern
  # is jump risk from compact-top anchor misalignment. So: the TEACHING STAYS — not a band,
  # note or item is touched — and only the claim that it constitutes its own registry section
  # is withdrawn, which is what restores the borrow math.
  ("social_sciences", "viii"): {
    "ch_07_canonical_p07.json": [
        (1,
         "Introduction / Factors of Production",
         "Introduction",
         "V2/unregistered-section",
         "the chapter's own title used as a second token beside a correct 'Introduction'. "
         "The four-way classification it labels is taught inside the unit and stays there; "
         "only the label goes | dropped: Factors of Production"),
    ],
    # ── THE TWO "ORPHANS", RESOLVED 2026-08-16 (founder). I had called these unfixable —
    # a unit whose ONLY label is unregistered, so dropping it leaves the unit unplaceable and
    # the choice is re-author or rule it accepted. That was wrong, and the founder named why:
    # the registry already carries the parent section, "The Blue of the Blue Planet, the
    # Oceans" / "The oceans". Ocean currents, ocean trenches and smaller water bodies are all
    # that section's material, so the label is not dropped — it is REPLACED by the section that
    # contains it. Same ruling as the token-drops (the top's selection is the contract, the
    # teaching stays put), applied to a whole label instead of a stray one.
    # Verified before declaring: both files come back 0 unknown anchors, 0 order-breaks, 12/12
    # coverage. No jump risk remains and neither file needs re-authoring — Rs 0 against the
    # ~Rs 27 a re-author would have cost, on a roll that might have returned a fresh defect.
    "ch_08_canonical_p08.json": [
        (3,
         "Smaller water bodies and waterways",
         "The oceans",
         "V2/unregistered-section",
         "the unit's only label, and not a registry section. Its material belongs to the "
         "oceans section the compact already teaches at U2, so the unit is re-anchored there "
         "rather than left unplaceable"),
    ],
    "ch_08_canonical_p11.json": [
        (3,
         "Ocean currents / Ocean trenches",
         "The oceans",
         "V2/unregistered-section",
         "same case in the sibling compact: currents and trenches are ocean-section material, "
         "not sections of their own"),
        # U4's token-drop ("The Great Barrier Reef / Smaller water bodies and waterways" ->
        # "The Great Barrier Reef") was APPLIED on 2026-08-16 and is removed from the live set:
        # re-declaring it fails the "declared text not found" guard, which is the guard doing
        # its job on an already-repaired file.
    ],
    "ch_10_canonical_p07.json": [
        (7,
         "Churches in India / Colonial Architecture / Before we move on …",
         "Before we move on …",
         "V2/unregistered-section",
         "two summary headings the standard never named, appended to the chapter's closing "
         "section. The church and colonial material remains in the unit; it is no longer "
         "claimed as its own registry section | dropped: Churches in India; Colonial "
         "Architecture"),
    ],
    "ch_10_canonical_p10.json": [
        (9,
         "Traditional Houses / Churches in India / Colonial Architecture",
         "Traditional Houses",
         "V2/unregistered-section",
         "same two tokens as p07, here beside Traditional Houses | dropped: Churches in "
         "India; Colonial Architecture"),
    ],
    "ch_12_canonical_p08.json": [
        (3,
         "Right to equality / Right to freedom / Right to life",
         "Right to equality / Right to freedom",
         "V2/unregistered-section",
         "finer-grained rights/duties headings than the registry carries; each sits beside "
         "the registry section that contains it | dropped: Right to life"),
        (4,
         "Right against exploitation / Right to freedom of religion / Cultural and educational rights / Right to constitutional remedies / Key Constitutional Articles That Guide Our Rights",
         "Right to freedom of religion / Key Constitutional Articles That Guide Our Rights",
         "V2/unregistered-section",
         "finer-grained rights/duties headings than the registry carries; each sits beside "
         "the registry section that contains it | dropped: Right against exploitation; "
         "Cultural and educational rights; Right to constitutional remedies"),
        (5,
         "Duties / What are duties? / Understanding duties",
         "Duties / Understanding duties",
         "V2/unregistered-section",
         "finer-grained rights/duties headings than the registry carries; each sits beside "
         "the registry section that contains it | dropped: What are duties?"),
        (7,
         "Discrimination / Understanding discrimination / Visible and invisible discrimination",
         "Discrimination",
         "V2/unregistered-section",
         "finer-grained rights/duties headings than the registry carries; each sits beside "
         "the registry section that contains it | dropped: Understanding discrimination; "
         "Visible and invisible discrimination"),
        (8,
         "Inclusion / Understanding inclusion",
         "Inclusion",
         "V2/unregistered-section",
         "finer-grained rights/duties headings than the registry carries; each sits beside "
         "the registry section that contains it | dropped: Understanding inclusion"),
    ],
  },
  # ── S2 · social_sciences · VI · ch 7 "India's Cultural Roots" — ONE-OFF, founder ruling
  #    2026-08-16. NOT the joiner family, and the difference matters enough to state.
  #
  # U18–U21 anchored ASPECT COMPOSITES, semicolon-joined:
  #    "Buddhism — ahimsa; Jainism — ahimsa extended to all living beings"
  # The first instinct — swap ';' for ' / ' as everywhere else in this file — is WRONG here
  # and was checked before being declared: splitting these four strings yields ELEVEN new
  # registry entries instead of four, so ch_07_canonical_p13's coverage failure goes from
  # omitting 4 cells to omitting 11. The delimiter was never the defect.
  #
  # The defect is GRANULARITY. Units 1–17 anchor sections; 18–21 anchor aspects OF sections
  # already taught. Their own teacher notes say so — "drawing on the full Buddhist and Jain
  # sections", "synthesises the contributions thread", "uses the full chapter's range" — they
  # are comparative revisit units wearing first-exposure anchors. So they are re-anchored to
  # the sections they revisit. Registry 21 → 17; p13 then covers all 17 and certifies.
  #
  # SAFE BECAUSE, checked not assumed: every entry named below is FIRST visited in U1–U17,
  # so all four units remain pure backward revisits — no first-visit order changes, no cell
  # loses its first exposure, and the standard still reaches the final registry section before
  # its synthesis unit (U22, untouched). Nothing inside any unit is edited: not a band, not a
  # note, not an item. Only the anchor string changes.
  #
  # WHICH entry each aspect maps to is a JUDGEMENT (the registry has no bare "Jainism" or
  # "Folk and Tribal Roots" head — every family is split into lettered sub-sections), and it
  # is recorded per edit below. Because these are revisits, a different defensible choice
  # would change which entries are back-referenced and nothing else.
  ("social_sciences", "vi"): {
    "ch_07_canonical.json": [
        (18,
         "Buddhism — ahimsa; Jainism — ahimsa extended to all living beings",
         "Buddhism / Jainism — Mahāvīra's life and the meaning of 'Jain'",
         "V2/granularity",
         "comparative ahimsa unit. Buddhism -> the section head [6]; the Jain formulation of "
         "ahimsa is doctrine introduced with Mahāvīra, so [9] carries it"),
        (19,
         "The Vedas — UNESCO recognition; Buddhism — spread across Asia; "
         "Jainism — anekāntavāda as intellectual contribution",
         "The Vedas and Vedic Culture — a. What are the Vedas? / Buddhism / "
         "Jainism — Jainism's historical influence and the Chārvāka school",
         "V2/granularity",
         "the 'contributions to humanity' thread. UNESCO recognition is of Vedic chanting, so "
         "it revisits [1]; anekāntavāda as an INTELLECTUAL contribution sits with Jainism's "
         "historical influence [11]"),
        (20,
         "Buddhism — enduring influence; Jainism — rock-cut caves and monasteries; "
         "Folk and Tribal Roots — continued tribal worship practices",
         "Buddhism / Jainism — Rohineya's story and Jain monasticism / "
         "Folk and Tribal Roots — tribal sacred concepts: Toda, Donyipolo, Singbonga",
         "V2/granularity",
         "the persistence argument. Monasteries -> the monasticism section [10]; continued "
         "tribal worship -> the tribal sacred concepts section [15]"),
        (21,
         "Buddhism — ahimsa and the Sangha; Jainism — anekāntavāda; "
         "Folk and Tribal Roots — mutual exchange; Vedic schools — brahman and ātman",
         "Buddhism / Jainism — Jainism's historical influence and the Chārvāka school / "
         "Folk and Tribal Roots — mutual interaction: Jagannath, tribal epics, shared sacred "
         "concepts / The Vedas and Vedic Culture — c. Vedic schools of thought "
         "(yajña and Upaniṣhads)",
         "V2/granularity",
         "the four-tradition role play. 'mutual exchange' is the Jagannath/tribal-epics "
         "section [14]; brahman and ātman are Upaniṣhadic, so [3]"),
    ],
    # The 18-period compact COMPRESSES the standard's U18–U21 into one unit and carries all
    # four composites in a single anchor. It certifies today, and it would BREAK the moment
    # the standard's registry changes under it — the four strings it names would no longer
    # exist. Found by checking the siblings before applying, not by watching it fail after.
    # The replacement is the union of the four re-anchorings above, deduplicated, in registry
    # order; every entry is first visited earlier in this same compact, so U18 stays a pure
    # backward revisit.
    "ch_07_canonical_p18.json": [
        (18,
         "Buddhism — ahimsa; Jainism — ahimsa extended to all living beings / "
         "The Vedas — UNESCO recognition; Buddhism — spread across Asia; "
         "Jainism — anekāntavāda as intellectual contribution / "
         "Buddhism — enduring influence; Jainism — rock-cut caves and monasteries; "
         "Folk and Tribal Roots — continued tribal worship practices / "
         "Buddhism — ahimsa and the Sangha; Jainism — anekāntavāda; "
         "Folk and Tribal Roots — mutual exchange; Vedic schools — brahman and ātman",
         "The Vedas and Vedic Culture — a. What are the Vedas? / "
         "The Vedas and Vedic Culture — c. Vedic schools of thought (yajña and Upaniṣhads) / "
         "Buddhism / Jainism — Mahāvīra's life and the meaning of 'Jain' / "
         "Jainism — Rohineya's story and Jain monasticism / "
         "Jainism — Jainism's historical influence and the Chārvāka school / "
         "Folk and Tribal Roots — mutual interaction: Jagannath, tribal epics, shared sacred "
         "concepts / Folk and Tribal Roots — tribal sacred concepts: Toda, Donyipolo, "
         "Singbonga",
         "V2/granularity",
         "one unit doing the work of the standard's four; the anchor becomes the union of "
         "their re-anchorings so the compact keeps naming exactly what it revisits"),
    ],
  },
  # ── S2 · social_sciences · VII · ch 3 "Climates of India" — SAME one-off ruling, 2026-08-16.
  # Presented as an ORDER defect: p13 and p17 both teach Topography at position 7, beside the
  # other Factors, while the registry put it at index 12 — first visited only at the top's U16,
  # inside its consolidation phase. The obvious reading is that the compacts jumped.
  #
  # They did not. The top's U6 is titled "Winds AND TOPOGRAPHY: How Moving Air and Landforms
  # Shape Climate" and its own note says it "covers two factors together because the chapter
  # treats them as complementary — winds carry air masses, and topography either channels or
  # blocks them". It TEACHES topography and anchors only Winds. U16 is an application unit
  # ("Having studied topography as one of five climate factors, this unit requires students to
  # apply multiple factors together"), so it was carrying a first-exposure anchor for content
  # it revisits.
  #
  # So this is under-labelling, not misordering, and the fix is ONE token — no unit is moved,
  # no compact is touched. Verified on copies before declaring: registry stays 13, Topography
  # moves to index 6, and all three files return 0 unknown anchors, 0 order-breaks, 13/13
  # coverage. U16's Topography anchor becomes a legal backward revisit.
  ("social_sciences", "vii"): {
    "ch_03_canonical.json": [
        (6,
         "Factors Determining the Climate — Winds",
         "Factors Determining the Climate — Winds / "
         "Factors Determining the Climate — Topography",
         "V2/granularity",
         "the unit teaches both factors and its title says so; anchoring only Winds pushed "
         "Topography's first exposure to U16 and made two correct compacts look like they "
         "jumped"),
    ],
  },

  ("social_sciences", "ix"): {
    "ch_03_canonical.json": [
        (4,
         "Weather and Climate; Elements of Weather and Climate",
         "Weather and Climate / Elements of Weather and Climate",
         "V2/joiner",
         "two-section unit; ';' is not the mandated joiner, so the registry read it as one "
         "opaque section. Sections named and their order are unchanged."),
    ],
    "ch_03_canonical_p10.json": [
        (4,
         "Weather and Climate; Elements of Weather and Climate",
         "Weather and Climate / Elements of Weather and Climate",
         "V2/joiner",
         "same slip as the standard canonical. THIS is the edit that clears p10's false "
         "first-visit-order failure: its U9 is an ordinary backward revisit of Elements "
         "(legal under the §4 frontier rule), not a skip."),
    ],
    "ch_03_canonical_p07.json": [
        (3,
         "Weather and Climate; Elements of Weather and Climate / Elements of Weather and Climate",
         "Weather and Climate / Elements of Weather and Climate",
         "V2/joiner",
         "semicolon composite plus a redundant repeat of the second section; the clean "
         "two-section form is emitted. Unit coverage is unchanged (sections 3-4)."),
    ],
    # ── ch 2 + ch 8 · THE STANDARD UNDER-NAMED ITS OWN SECTIONS (2026-08-12) ──────
    # THE FIRST TIME A COMPACT CAUGHT A DEFECT IN THE PLAN IT WAS AUTHORED FROM, and the
    # reason it deserves this much comment is that the machine blamed the wrong file.
    #
    # ch_02_p09 and ch_08_p04 were QUARANTINED on "every anchor verbatim in the top registry"
    # + "first-visit order". Both had anchored sections the registry did not contain. Every one
    # of those sections is a real heading in the chapter summary (ch 2 "Running Water" at offset
    # 6232; ch 8 "What to Produce and for Whom?" 4573, "How to Produce?" 5836, "Economic Systems
    # and How Choices are Made" 6725, "Market Economy" 8031). The STANDARDS teach them and say
    # so in their own unit titles — ch 2 U5 is titled "Agents of Gradation AND RUNNING WATER:
    # Valley to Delta", ch 8 U5 is "Planned AND MARKET Economies", ch 8 U4 is "The Three Key
    # Questions — What, How, and For Whom to Produce" — and then anchor one section each. The
    # registry is derived from those anchors, so the omission was invisible to certification:
    # runbook §4 trap 5, "the check cannot see what it is built from".
    #
    # ch 8's registry held 6 of the chapter's 10 sections. MARKET ECONOMY — a whole section of
    # an economics chapter — was not in it.
    #
    # WHY THIS IS ANCHOR HYGIENE AND NOT A LAUNDERED CONTENT CHANGE (the line this tool's
    # docstring draws): no teaching text is touched and no unit changes what it covers. Each
    # edit names sections the unit ALREADY teaches, in registry order. Verified band by band:
    # ch 2 U5 bands 8-30/30-42 teach the running-water course sequence, V-shaped valley to
    # delta; ch 8 U4 bands 10-26/26-40 teach what-to-produce and how-to-produce; ch 8 U5 band
    # 26-40 teaches the market economy from Fig. 8.7 with the referee analogy and examples.
    #
    # WORTH RECORDING FOR THE MECHANISM, not just the fix: p04's brief SHOWED it the 6-section
    # registry and said anchors MUST be drawn verbatim from that list. It named seven sections
    # anyway, three of them absent from its brief, because it had read the summary. The compact
    # was right about the chapter and was quarantined for it. Cheap check for next time: diff
    # every canonical's anchor set against its siblings' and flag disagreement — that alone
    # would have caught both chapters automatically, at no cost, before either was quarantined.
    # p07 carries the SAME under-naming as its standard, and only became visible once the
    # standard's registry gained Running Water: p07 U4 is titled "Rivers at Work: Valleys,
    # Waterfalls, Meanders, and Deltas" and teaches V-shaped valleys, waterfalls, meanders,
    # oxbows and deltas, while anchoring 'Agents of Gradation' — which U3 has already
    # first-visited. So the anchor names a section already open and leaves the section it
    # actually deals unnamed, which read as "skips s3". Anchored correctly the plan runs
    # monotone s0,s0,s1+s2,s3,s4+s5+s6,s7,s8.
    # THE PATTERN IS NOW THREE-FOR-THREE ACROSS TWO CHAPTERS (ch2 top, ch2 p07, ch8 top):
    # where a chapter has a PARENT section with named children, this stage's model anchors the
    # parent and teaches the child. That is a brief-level gap, not nine independent slips —
    # nothing in the brief says a unit teaching a sub-section must anchor the sub-section.
    "ch_02_canonical_p07.json": [
        (4,
         "Agents of Gradation",
         "Running Water",
         "V2/registry-omission",
         "the unit deals Running Water and nothing else; Agents of Gradation was first "
         "visited at U3 and is not re-opened here"),
    ],
    # p04 — the quarantined compact, repaired on the way back in. apply_file() reads the
    # quarantined copy when the library copy is absent and writes it back under its proper
    # library name, so this declaration IS the restore.
    #
    # p04 carries the SAME parent-for-child under-naming as the standard, in the same chapter:
    # U4 is titled "How Economies Organise Answers: Planned, MARKET, and Mixed Systems" and its
    # band 10-27 teaches the market economy outright — "Then shift to the market economy: demand
    # and supply settle what, how, and how much to produce; the government acts like a referee",
    # with examples (United States, Japan, Hong Kong) and a comparative pair-question — and its
    # band 40-50 poses the LET'S EXPLORE from the Market Economy section by name. The section is
    # taught; only the anchor omitted it. Corrected, p04 anchors 10 of 10 registry sections and
    # nothing is dropped.
    #
    # WORTH BEING EXACT ABOUT, because the word matters here: a canonical never "drops" a
    # section. Dropping is a SERVE-time act (§0.4 Case 2's dropped sections riding from the
    # lender, Case 3's declared truncation). p04 was authored FREE at 4 periods as a complete
    # plan for the whole chapter — not a compression of the 7-period standard — so a missing
    # section would be a defect, never a feature, and a difference in DEPTH from the standard is
    # neither. Reading the two side by side as though one were cut from the other is the retired
    # partition engine's frame.
    "ch_08_canonical_p04.json": [
        (4,
         "Economic Systems and How Choices are Made / Planned Economy / Mixed Economy",
         "Economic Systems and How Choices are Made / Planned Economy / Market Economy / "
         "Mixed Economy",
         "V2/registry-omission",
         "Market Economy inserted in registry order (7 / 8 / 9 / 10) as the brief requires; "
         "the unit already teaches it in band 10-27"),
    ],
    # ── ch 4 "Early Humans and Beginning of Civilisation" · WAVE 1 (2026-08-12) ───
    # NOT A MODEL SLIP, and worth being explicit about because the repair record is also the
    # evidence base for whether to change the MECHANISM. "a. The Sumerians" is the ch 4
    # summary's OWN sub-heading, verbatim (ch_04_summary.txt offsets 12709 / 14965), and the
    # summary really does place "The Beginning of Writing" between a. and b. The model
    # transcribed its source correctly on both counts. This is a NORMALISATION at the founder's
    # instruction (2026-08-12), not a defect repair: a registry section is a name, and textbook
    # list lettering is enumeration, not name.
    #
    # THE RISK THIS CARRIES, stated so the next reader can check it rather than rediscover it:
    # ch 4's compacts are authored in wave 2 from THIS registry, but the model also reads the
    # lettered summary. If a compact writes "a. The Sumerians" it will fail "every anchor
    # verbatim in the top registry" — a failure caused by this normalisation, not by the
    # compact. It is free to repair there too (same tool, same declaration shape), but read
    # ch 4's wave-2 anchor failures in that light before treating them as authoring defects.
    "ch_04_canonical.json": [
        (12, "a. The Sumerians", "The Sumerians", "V2/lettering",
         "textbook enumeration stripped; the section named is unchanged and its position "
         "in the registry (after Mesopotamian Civilisation) is unchanged"),
        (14, "b. The Akkadians", "The Akkadians", "V2/lettering",
         "same normalisation. Note the a./b. pair is split by 'The Beginning of Writing' in "
         "the SUMMARY too — that ordering is the source's, not the model's, and is left alone"),
    ],
    # ── ch 6 "Democracy" · BATCH WAVE 1 (2026-08-12) ─────────────────────────────
    # Three ';' composites, found by reading the derived registry against the summary —
    # NOT by certification, which passed ch 6 on "every anchor verbatim in the top
    # registry" and "first-visit order follows the registry". Both checks compare the
    # registry to the anchors it was derived FROM, so a malformed joiner is invisible to
    # them by construction (runbook §4 trap 5). This is the third stage to produce this
    # exact defect after SS·IX ch 3 and TWAU wave 2.
    #
    # THE SECTION NAMES ARE NOT INVENTED. ch 6's summary has "Principles of Democracy" as
    # a SECTION with seven named sub-sections under it, and this plan's own convention for
    # a sub-section anchor is "Principles of Democracy — X" (U4, U5, U7 all write it that
    # way, unjoined). So the repaired form repeats the parent prefix on both sides rather
    # than emitting a bare "Rule of Law": splitting to a form the other 16 units do not use
    # would put two spellings of the same convention in one registry.
    #
    # U18 IS THE ONE THAT MATTERS FOR WAVE 2. Its composite names Separation of Powers and
    # Accountability and Transparency — both ALREADY registered, at U5 and U6. Unsplit, the
    # pair entered the registry as a SEVENTEENTH opaque section that exists nowhere in the
    # chapter, and every compact brief for ch 6 would have been built to cover it. Split, U18
    # is what it actually is: an ordinary backward revisit of two taught sections, legal under
    # LP v1.10, contributing nothing new to the registry. Registry goes 16 -> 17 real
    # sections and loses the phantom. No unit's teaching content is touched.
    "ch_06_canonical.json": [
        (3,
         "Principles of Democracy — Popular Sovereignty; Rule of Law",
         "Principles of Democracy — Popular Sovereignty / Principles of Democracy — Rule of Law",
         "V2/joiner",
         "two adjacent sub-sections of Principles of Democracy, in summary order; ';' is "
         "not the mandated joiner so the registry read them as one"),
        (6,
         "Principles of Democracy — Accountability and Transparency; Multi-Party System",
         "Principles of Democracy — Accountability and Transparency / Principles of "
         "Democracy — Multi-Party System",
         "V2/joiner",
         "same slip, same two-sub-section shape; both names are verbatim summary "
         "sub-headings"),
        (18,
         "Principles of Democracy — Separation of Powers; Accountability and Transparency",
         "Principles of Democracy — Separation of Powers / Principles of Democracy — "
         "Accountability and Transparency",
         "V2/joiner",
         "THE CONSEQUENTIAL ONE: both halves are already registry sections (U5, U6), so "
         "unsplit this composite invented a phantom 17th section that every ch 6 compact "
         "brief would have been told to cover. Split, U18 is a legal backward revisit"),
    ],
  },

  # APPLIED 2026-08-12 · SS·IX ch 2 standard. Kept as the cost/decision record, held at a
  # 3-tuple key so main()'s (subject, grade) lookup cannot re-run it — re-running would fail
  # its own "declared text not found" guard and block the p07 edit behind it.
  ("social_sciences", "ix", "APPLIED-20260812-ch02-ch08-tops"): {
    "ch_02_canonical.json": [
        (5,
         "Agents of Gradation",
         "Agents of Gradation / Running Water",
         "V2/registry-omission",
         "U5's own title names Running Water; bands 8-30 and 30-42 teach the full upper/middle/"
         "lower course sequence. Registry 8 -> 9 sections; Running Water enters at position 4, "
         "its summary order (Agents of Gradation 5321 < Running Water 6232 < Waves and Currents "
         "7904), so first-visit order is unchanged"),
    ],
    "ch_08_canonical.json": [
        (4,
         "Key Questions in Economics",
         "Key Questions in Economics / What to Produce and for Whom? / How to Produce?",
         "V2/registry-omission",
         "U4 is titled 'The Three Key Questions — What, How, and For Whom to Produce' and its "
         "bands work through both sub-sections explicitly (crop example for what-to-produce, "
         "Fig. 8.6 factors of production for how-to-produce, and the THINK ABOUT IT is taken "
         "from the 'What to Produce and for Whom?' section by name)"),
        (5,
         "Planned Economy",
         "Economic Systems and How Choices are Made / Planned Economy / Market Economy",
         "V2/registry-omission",
         "THE SERIOUS ONE. U5 is titled 'Planned and Market Economies — Two Models of Answering "
         "the Three Questions'; band 26-40 introduces the market economy from Fig. 8.7 with the "
         "chapter's referee analogy, and band 40-50 has students build a Planned vs Market "
         "comparison table. 'Economic Systems and How Choices are Made' is the parent section "
         "whose framing question U5 band 0-12 opens on. Registry 6 -> 10 sections"),
    ],
  },

  # ── v1.6, 2026-08-12 · S5 · the_world_around_us · WAVE 2 (the compacts) ──────────
  # Four hits, three files, ONE defect: the mandated " / " joiner written as ";" or ",".
  # Exactly the ARV-D-011 shape this tool was built for — and, as there, the corrupted
  # composite ALSO produced the file's first-visit-order failure, because a joined string
  # the registry cannot split enters it as one opaque section. Repairing the joiner is
  # expected to clear both FAILs; nothing about which sections are taught, or in what
  # order, changes.
  #
  # iv ch09 U8 is the interesting one and the reason a naive normalizer would be unsafe:
  # this chapter's section TITLES CONTAIN COMMAS ("On the Seashore, with Chandni"), so
  # splitting the anchor on "," yields four fragments that match nothing. The declared pair
  # below was derived by matching registry entries as verbatim SUBSTRINGS — both appear,
  # in registry order, and the repair states the result rather than computing it at apply
  # time.
  ("the_world_around_us", "iii"): {
    "ch_08_canonical_p04.json": [
        (3,
         "We Eat Different Things; Where does food come from?",
         "We Eat Different Things / Where does food come from?",
         "V2/joiner",
         "';' composite of two real, adjacent registry sections"),
    ],
  },
  ("the_world_around_us", "iv"): {
    "ch_09_canonical_p10.json": [
        (8,
         "On the Seashore, with Chandni, In the Mountains, with Nayan",
         "On the Seashore, with Chandni / In the Mountains, with Nayan",
         "V2/joiner",
         "',' composite of registry sections 4 and 5, whose own titles carry commas — the "
         "split point is the one that leaves both entries verbatim"),
    ],
  },
  ("the_world_around_us", "v"): {
    # ── ch 08, 2026-08-12: a REAL SECTION MISSING FROM THE REGISTRY ─────────────────
    # Not a delimiter this time, so it is declared with its evidence and was ruled by the
    # founder, not by this tool's usual "only the separator is wrong" licence.
    #
    # The chapter has six sections; the top anchors five. 'Recycle' — the textbook's closing
    # reflection section (pp. 143-144: "We should not throw old clothes away, why?", the
    # cloth-observation table, the silk life-cycle ordering) — is named ONLY by U10, the
    # synthesis, and the registry excludes synthesis units by design (§0.3). So Recycle
    # disappears from the registry, and the two compacts that teach it as an ordinary closing
    # unit (p06 U6 "Cloth That Lives On", p08 U8 "Give Cloth a Second Life") fail
    # anchor-verbatim — while skipping it would have failed coverage. They could not pass.
    #
    # THE EVIDENCE FOR THE REPAIR, which is about what U9 already does: its title is
    # "Embroidery Stories and the Cloth We Recycle", and its closing band (36-40) has
    # students write "One way my family or community reuses old cloth is…" — Recycle content,
    # in a unit anchored only to Stitch and Decorate. The join states what the unit teaches.
    #
    # THE COST, STATED: the top gives Recycle one 4-minute band plus its synthesis, where a
    # compact gives it a whole unit. The anchor is generous, not false. Re-authoring the top
    # (~Rs 40 with its compacts) was the alternative and was declined: a clean chapter should
    # not be re-rolled to fix a label.
    #
    # THE GENERAL FINDING, logged beyond this chapter: excluding the synthesis anchor from
    # the registry is safe where the synthesis carries the reserved TOKEN, and lossy where the
    # carrier is a BOOLEAN and the unit can name a real section (TWAU, and any stage like it).
    # ARV-D-118's family, surfacing a second way.
    "ch_08_canonical.json": [
        (9,
         "Stitch and Decorate",
         "Stitch and Decorate / Recycle",
         "V2/registry-omission",
         "U9 already teaches both: the embroidery gallery walk (Stitch and Decorate) and a "
         "closing band on reusing old cloth (Recycle). Naming the second section puts it in "
         "the registry at the position the textbook gives it, and lets the compacts' Recycle "
         "units anchor verbatim"),
    ],
    "ch_10_canonical_p10.json": [
        (6,
         "Story 4: The Sweet Story of Sugar!, Story 5: The Mexican Marigold Moves into India!",
         "Story 4: The Sweet Story of Sugar! / Story 5: The Mexican Marigold Moves into India!",
         "V2/joiner",
         "',' composite of two adjacent registry stories"),
        (8,
         "Story 6: The Cows that Went to Brazil!, Web of Life",
         "Story 6: The Cows that Went to Brazil! / Web of Life",
         "V2/joiner",
         "same file, same slip; 'Web of Life' is the chapter's closing registry section"),
    ],
  },
}


def registry_of_library():
    """Compile the library and derive the registry from the top canonical, exactly as
    build_library.certify does — so what is printed here is what certification will see."""
    nn = f"ch_{CHAPTER:02d}"
    paths = [LIB / f"{nn}_canonical.json"] + sorted(LIB.glob(f"{nn}_canonical_p*.json"))
    lib = [(p.name, compile_stream(json.loads(p.read_text(encoding="utf-8"))))
           for p in paths if p.is_file()]
    lib.sort(key=lambda t: -len(t[1]["units"]))
    reg = section_registry(lib[0][1])
    return lib, reg


def first_visit_check(lib, reg):
    ridx = {_norm(a): i for i, a in enumerate(reg)}
    out = []
    for name, s in lib:
        seen, bad = -1, []
        for u in [x for x in s["units"] if not is_synthesis_unit(x)]:
            r = unit_range(u, ridx)
            if r is None:
                bad.append((u["unit"], "anchor not in registry"))
                continue
            if r[1] > seen:
                if r[0] > seen + 1:
                    bad.append((u["unit"], f"skips s{seen + 1}"))
                seen = r[1]
        out.append((name, bad, seen, len(reg) - 1))
    return out


def show_registry(label):
    lib, reg = registry_of_library()
    print(f"\n{label} — registry ({len(reg)} sections):")
    for i, s in enumerate(reg):
        print(f"    {i}  {s}")
    print(f"{label} — first-visit order:")
    for name, bad, seen, last in first_visit_check(lib, reg):
        print(f"    {name:<28} {'OK' if not bad else 'FAIL ' + str(bad):<34} "
              f"frontier {seen}/{last}")
    return reg


def apply_file(fname, edits, dry):
    path = LIB / fname
    if not path.is_file():
        # QUARANTINE (2026-08-12): build_library moves a failed canonical out of the library,
        # so the file a repair targets is usually not where the library keeps it. Repair the
        # quarantined copy and put it back under its proper name — the same route
        # repair_item_type.py takes, for the same reason.
        qs = sorted((QUAR / LIB.parent.name / LIB.name).glob(fname[:-5] + "_*.json"))
        if not qs:
            raise SystemExit(f"missing: {path} (and nothing quarantined for it)")
        print(f"  (library copy absent — repairing quarantined {qs[-1].name})")
        path_src = qs[-1]
    else:
        path_src = path
    plan = json.loads(path_src.read_text(encoding="utf-8"))
    units = {u["period_number"]: u for u in plan["result"]["lesson_plan"]["periods"]}
    done = []
    for unit_no, old, new, rule, note in edits:
        u = units.get(unit_no)
        if u is None:
            raise SystemExit(f"{fname}: no unit {unit_no}")
        fld = _anchor_field(u)
        cur = u.get(fld) or ""
        if cur != old:
            raise SystemExit(
                f"{fname} U{unit_no} section_anchor: declared text not found — the artefact "
                f"has changed since this repair was written. Re-read it, do not force.\n"
                f"  wanted: {old!r}\n  found : {cur!r}")
        if not dry:
            u[fld] = new
        done.append({"unit": unit_no, "field": fld, "rule": rule,
                     "removed": old, "replaced_with": new, "note": note})
    if not dry:
        gc = plan.setdefault("genon_canonical", {})
        gc.setdefault("repairs", []).append({
            "at": datetime.now().isoformat(timespec="seconds"),
            "tool": "genon/repair_anchors.py v1.0",
            "reason": "V2 section-anchor joiner repair (';' read as one opaque registry "
                      "section; corrupted the derived registry, falsely quarantined p10, "
                      "and mis-served X=8/X=9)",
            "edits": done,
        })
        path.write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")
    return done


def _arg(flag, default):
    return sys.argv[sys.argv.index(flag) + 1] if flag in sys.argv else default


def main():
    global LIB, CHAPTER
    dry = "--apply" not in sys.argv
    subject = _arg("--subject", "social_sciences")
    grade = _arg("--grade", "ix")
    CHAPTER = int(_arg("--chapter", "3"))
    key = (subject, grade)
    if key not in REPAIRS:
        raise SystemExit(f"no declared set for {key}; have {sorted(REPAIRS)}")
    LIB = SAVED / subject / grade
    repairs = {f: e for f, e in REPAIRS[key].items()
               if int(f.split("_")[1]) == CHAPTER}
    if not repairs:
        raise SystemExit(f"no declared edits for {subject} {grade} ch {CHAPTER}; "
                         f"chapters in this set: "
                         f"{sorted({int(f.split('_')[1]) for f in REPAIRS[key]})}")
    print(f"repair set {subject} {grade} ch {CHAPTER} -> {LIB.relative_to(REPO)}/")
    show_registry("BEFORE")
    if not dry:
        BACKUP.mkdir(parents=True, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        for fname in repairs:
            src = LIB / fname
            if src.is_file():
                shutil.copy2(src, BACKUP / f"{grade}_{fname[:-5]}_{ts}.json")
        print(f"\nbacked up the library copies present -> {BACKUP.relative_to(REPO)}/")
    print()
    for fname, edits in repairs.items():
        done = apply_file(fname, edits, dry)
        print(f"=== {fname} — {len(done)} edit(s)"
              f"{' (DRY RUN, nothing written)' if dry else ''}")
        for d in done:
            print(f"  U{d['unit']:<3} section_anchor   [{d['rule']}]")
            print(f"        - {d['removed']}")
            print(f"        + {d['replaced_with']}")
    if dry:
        print("\ndry run — re-run with --apply to write.")
        return 0
    # A repaired canonical invalidates every plan derived from it (ARV-D-034) — the serve
    # cache keys on the canonical's ledger_ts, which a repair does not move.
    purge(subject, grade, CHAPTER, reason="genon/repair_anchors.py")
    reg = show_registry("AFTER")
    bad = [b for _, b, _, _ in first_visit_check(*registry_of_library()) if b]
    print(f"\nregistry is {len(reg)} sections; "
          f"{'ALL plans pass first-visit order.' if not bad else 'FAILURES REMAIN — read above.'}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
