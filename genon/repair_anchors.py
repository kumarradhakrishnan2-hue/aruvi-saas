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

v1.1, 2026-08-17 (S3 · science·IX wave 1): HANDOFF-ROW LABEL edits join the tool (founder
ruling 2026-08-17: extend, not a sibling). The S3 defect family is the check's mirror image:
the UNIT anchors are right (precise slices, correct registry) and the `coverage_handoff`
row's `section_label` names the MERGED assessment cell ("7.6 Simple Machines" over units
anchoring 7.6.1/7.6.2/7.6.3), so the substring test fails in both directions. The truthful
fix is on the handoff side — shorten the label to the common stem of the anchors it routes
to. `period_numbers` are NEVER touched (the science port rejoins LO by period_number, and
which unit receives which items is the routing, which is correct). A handoff edit is
declared with the unit slot set to the string "handoff"; old/new are the row's verbatim
`section_label`. Same assertions: not found verbatim, or found twice -> fail loudly.
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
  # ── S4 · mathematics · IX · W1 wave-1 triage (2026-08-18) ──────────────────────────────
  # ONE FAMILY, TWO CHAPTERS: a unit teaches two (or four) sections and its anchor names
  # only the first. This is the joiner defect in its plainest form — no section is missing
  # from the plan, no teaching changes, the ' / ' between the names was simply never
  # written. C5 check 11 reads it as an omitted section and the handoff/anchor gate reads
  # it as a mis-route; both clear on the same edit.
  #
  # Every `new` string below is quoted from the artefact's own text, not inferred:
  # the unit's title or a band names the second section explicitly. Verified on the
  # quarantined copies before declaring.
  #
  # NOT REPAIRED HERE, deliberately: ch 3 section 3.2.2 has no coverage_handoff row at
  # all. The U4 anchor edit puts it in the registry (which is what check 11 reconciles);
  # creating a handoff row is authoring, not repair, and the advisory "a unit anchors a
  # section the handoff does not route through" is the correct, non-gating signal for it.
  ("mathematics", "ix"): {
    "ch_03_canonical.json": [
        (4, "3.2", "3.2 / 3.2.2", "V2/joiner",
         "the unit title is 'Zero as a Number: Brahmagupta's Rules and the Bakhśhālī "
         "Manuscript' — 3.2.2's exact subject; band 10-22 states Brahmagupta's definition "
         "and derives the three laws, band 36-50 examines the Bakhśhālī bindu. 3.2 (the "
         "placeholder-vs-number distinction) is band 0-10. Both sections, one unit."),
        (12, "3.5", "3.5 / 3.5.1", "V2/joiner",
         "band 10-30 reads 'Teacher presents the eight-step proof by contradiction FROM "
         "SECTION 3.5.1'; band 30-42 runs its think-and-reflect. The handoff already "
         "routes 3.5.1 to U12 — only the anchor disagreed."),
        (16, "3.6.2", "3.6.2 / 3.6.3 / 3.6", "V2/joiner",
         "the unit's own teacher note states it: 'This unit covers both the cyclic-number "
         "curiosity (3.6.2) and the irrational-decimal contrast (3.6.3) and closes with "
         "the real-line definition (3.6).' Band 28-40 introduces 3.6.3 by name; band 40-50 "
         "is the 3.6 closure. The handoff routes all three to U16."),
        ("handoff-route", ("3.7", (16,)), [17], "V2/handoff-route",
         "3.7 'Conclusion: The Never-Ending Journey' is not taught in U16 — U16 ends on "
         "the R = Q ∪ I closure of 3.6. It is taught in U17, the synthesis unit, whose "
         "final band reads 'Section 3.7 open question: the teacher poses √(-1)'. The row "
         "is re-pointed at the unit that teaches it. ANCHOR-AT-LAST-UNIT holds and is the "
         "reason this is safe: 3.7 is a single-unit section, its last routed unit moves "
         "16 -> 17, and 17 is the final unit of the canonical, so nothing can be pushed "
         "past the end of a serve. Paired with the synthesis carve-out added to the "
         "agreement gate the same day: a row routed to the synthesis unit is reported, "
         "not failed. "
         "CORRECTED 2026-08-18, same day, by the verification pass: this rationale first "
         "read '3.7 anchors no assessment item (the chapter's items stop at 3.6)' and that "
         "was WRONG. The chapter has 23 items and item section_number 19 / section_ref 3.7 "
         "(N ⊂ Z ⊂ Q, √(-1)) resolves through the handoff, so its unit_ref moved [16] -> "
         "[17] with the row. Measured downstream: at X=17 the item simply lands on the "
         "sitting that teaches it; at X<=16 it is DROPPED where before it rode a unit that "
         "never taught 3.7 (assessment_items_unserved 1 -> 2). Read as a correction — an "
         "item now tests taught content or is declared unserved, never neither — but it is "
         "a real behaviour change and the founder ruled on it knowing the true version."),
    ],
    "ch_07_canonical.json": [
        (2, "7.1.1", "7.1.1 / 7.1.2", "V2/joiner",
         "the handoff routes 7.1.2 'The Probability Scale' to U2, and U2's band 28-50 reads "
         "'Introduce the probability scale (section 7.1.2) formally' — the section named in "
         "the unit's own text. Bands 0-10 and 10-28 are 7.1.1 (randomness, random "
         "experiment, rainfall). Both sections, one unit. (The 'read and assign values on "
         "the probability scale' wording quoted in the first draft of this note is the "
         "HANDOFF ROW's implied_lo, not a field of U2 — corrected 2026-08-18.)"),
        # 7.3 'Elements of Probability: Sample Spaces and Events' is NOT repaired and is
        # not a defect: it is a PARENT container whose children 7.3.1 (Sample Space) and
        # 7.3.2 (Events) anchor at U7 and U8 respectively, and it carries no handoff row.
        # Check 11 counts a parent with no anchor of its own as unnamed; teaching it as
        # its two children is the correct pedagogy, not an omission.
    ],
  },

  # ── S2 · social_sciences · VIII · ch 8 "World Geography: Some Glimpses" — THE STANDARD WAS
  #    THE DEFECT (F1 finding, 2026-08-16). Nine units re-anchored; authored by Fable 5 against
  #    a constrained prompt (docs/testing_artefacts/PROMPT_reanchor_ss_viii_ch08.md), verified
  #    here before application.
  #
  # FOUND AT THE HUMAN GATE, NOT BY A CHECK, and that is the point: this chapter certified ALL
  # PASS while seven of its thirteen units carried the wrong section name. The registry is
  # DERIVED from the standard, so a self-consistent mislabelling is invisible to every
  # deterministic test — anchors were verbatim (they are, in the registry they themselves
  # created), first-visit order held, coverage reached the end. It surfaced only when the F1
  # borrow-seam pack put a unit labelled `North America` next to a title reading "Australia's
  # Deserts, the Spinifex People, and Antarctica".
  #
  # NOT a clean off-by-one: U12 is a BACKWARD REVISIT of Asia (its band says it teaches "the
  # chapter's dedicated mountain-roles passage in the Asia section") wearing Australia's label,
  # and U4/U5/U6 each teach TWO sections where the standard named one.
  #
  # THE CONSEQUENCE THAT MATTERS: restoring U4 and U5 puts "Ocean currents", "Ocean trenches"
  # and "Smaller water bodies and waterways" into the registry — the exact three names the
  # COMPACTS had anchored and which were repaired AWAY from them earlier the same day, on the
  # reasoning that the top's selection is the contract. The compacts were right; they were
  # describing a chapter the standard had mislabelled. Those three edits are therefore REVERTED
  # below, and the lesson is recorded rather than quietly fixed: "align the compact to the top"
  # is only sound while the top is trustworthy, and nothing in the deterministic set can tell
  # you when it is not.
  #
  # Verified on copies before declaring: all 9 old strings resolve verbatim · registry 12 -> 15
  # · p11 returns 15/15 coverage, 0 unknown anchors, 0 order-breaks · p08 returns 13/15 (it
  # genuinely does not teach currents or trenches at 8 periods) and still reaches the final
  # registry section.
  ("social_sciences", "viii"): {
    "ch_08_canonical.json": [
        (4, "The oceans", "The oceans / Ocean currents / Ocean trenches", "V2/mis-anchored",
         "the five-ocean survey plus currents and the deepest places — the title 'Five Oceans, "
         "Currents, and the Deepest Places on Earth' names all three"),
        (5, "The Great Barrier Reef",
         "The Great Barrier Reef / Smaller water bodies and waterways", "V2/mis-anchored",
         "the band introduces the reef but the title 'Reefs, Seas, Gulfs, and Canals — Smaller "
         "Marine Formations' shows it also teaches the smaller water bodies and waterways"),
        (6, "The Continents: Variety on Land",
         "The Continents: Variety on Land / Asia", "V2/mis-anchored",
         "opens with the continent definition and landform types, then 'Orient students to the "
         "Asia section'; the title 'Asia's Roof, Deserts, and Steppes' confirms both"),
        (7, "Asia", "Europe", "V2/mis-anchored",
         "title 'Urals, the European Plain, and the Alps — Europe's Landform Triangle'; the "
         "band introduces the Urals as the Europe-Asia boundary"),
        (8, "Europe", "Africa", "V2/mis-anchored",
         "title 'Africa: Sahara, Savannah, and the Nile'; the band opens on the Sahara as the "
         "largest hot desert"),
        (9, "Africa", "South America", "V2/mis-anchored",
         "title 'Andes, Amazon, and Atacama — South America's Extremes'; the band introduces "
         "the Andes and Mount Aconcagua"),
        (10, "South America", "North America", "V2/mis-anchored",
         "title names the Colorado Plateau, Rockies, Appalachians and Great Lakes; the band "
         "opens on the Colorado Plateau and Grand Canyon"),
        (11, "North America", "The Australian Continent", "V2/mis-anchored",
         "title 'Australia's Deserts, the Spinifex People, and Antarctica'; the Antarctica "
         "case serves that section's 'not all deserts are hot' corrective"),
        (12, "The Australian Continent", "Asia", "V2/mis-anchored",
         "a BACKWARD REVISIT: the band states it 'focuses on the chapter's dedicated "
         "mountain-roles passage in the Asia section', so it anchors back to Asia, not forward"),
    ],
    # ── the three reverts. `old` is what the earlier repair left on disk.
    "ch_08_canonical_p08.json": [
        (3, "The oceans", "Smaller water bodies and waterways", "V2/revert-to-authored",
         "restores the compact's own authored anchor, now that the standard names the section"),
    ],
    "ch_08_canonical_p11.json": [
        (3, "The oceans", "Ocean currents / Ocean trenches", "V2/revert-to-authored",
         "restores the compact's own authored anchor; this unit was the 'orphan' — it was "
         "never orphaned, its section simply did not exist in a mislabelled registry"),
        (4, "The Great Barrier Reef",
         "The Great Barrier Reef / Smaller water bodies and waterways", "V2/revert-to-authored",
         "restores the token dropped when the registry lacked the section"),
    ],
  },
  # ── APPLIED 2026-08-16 (wave-2 token-drops) — retired to a 3-tuple key so the ch 8 set above
  #    owns the live one. ch 8's two entries here are SUPERSEDED by the reverts, not merely
  #    applied: they were correct against a registry that was itself wrong.
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
  ("social_sciences", "viii", "APPLIED-20260816-tokendrops"): {
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
  # ── S3 · science · IX · BATCH WAVE 1 — HANDOFF-ROW LABEL RE-STEMS (2026-08-17, v1.1) ──
  # 16 mis-routed units across 4 standards (certification 20260817_1006*), ALL one family:
  # the handoff row's `section_label` names the merged assessment CELL while the units
  # anchor precise slices, so the substring test fails in both directions. The routing
  # (`period_numbers`) is pedagogically correct in every case and is not touched; each
  # label is shortened to the common stem of the anchors it routes to. Every new stem was
  # verified against serve._norm and every routed unit's anchor tokens before declaring.
  # The full cell description survives in each row's `section_context`.
  # ch 02 and ch 12 are in quarantine — apply_file repairs the quarantined copy and
  # writes it back under its library name, which IS the restoration (trap 1: the whole
  # library is re-scanned at the follow-up --certify-only).
  # APPLIED 2026-08-17 (all four chapters; re-certified 20260817_1040 clean); renamed so
  # the wave-2 set below owns the live key.
  ("science", "ix", "APPLIED-20260817-wave1"): {
    "ch_02_canonical.json": [
        ("handoff",
         "Section 2.3.1 – Organelles: Nucleus, Ribosomes, ER, Golgi Apparatus, Lysosomes",
         "Section 2.3.1 – Organelles",
         "handoff/label-stem",
         "routes U6 (nucleus and ribosomes) + U7 (ER, Golgi, lysosomes); the stem is the "
         "prefix both anchors share"),
        ("handoff",
         "Section 2.4 and 2.4.1 – Cell Growth, Division: Mitosis and Meiosis",
         "Section 2.4",
         "handoff/label-stem",
         "routes U10 (2.4 – how do normal cells grow and divide?) + U11 (2.4.1 – mitosis "
         "and meiosis); 'Section 2.4' is a stem of both"),
        ("handoff",
         "Section 2.5 and 2.5.1 – Cell Theory, Lifespan, Cancer, and Cell Culture",
         "Section 2.5",
         "handoff/label-stem",
         "routes U12 (2.5 – cell theory) + U13/U14 (2.5.1 – lifespan / cell culture); "
         "'Section 2.5' is a stem of all three"),
    ],
    "ch_04_canonical.json": [
        ("handoff",
         "4.4.1 Uniform circular motion",
         "4.4",
         "handoff/label-stem",
         "routes U12 (4.4 motion in a plane) + U13-15/19-20 (4.4.1 uniform circular "
         "motion); only the bare '4.4' stems both — the cell genuinely spans parent and "
         "child section"),
    ],
    "ch_07_canonical.json": [
        ("handoff",
         "7.6 Simple Machines",
         "7.6",
         "handoff/label-stem",
         "routes U13 (7.6 simple machines) + U14-19 (7.6.1 pulley / 7.6.2 inclined plane "
         "/ 7.6.3 lever); '7.6' stems all four anchors"),
    ],
    "ch_12_canonical.json": [
        ("handoff",
         "12.6.1–12.6.3 Monera, Protista and Fungi",
         "12.6.1 Kingdom Monera",
         "handoff/label-stem",
         "routes U8, whose single anchor is the ' / '-joined triple (monera / protista / "
         "fungi); the check splits anchors into tokens and needs any one match, so the "
         "first kingdom's stem is the honest minimal label — the row's section_context "
         "still records all three kingdoms"),
        ("handoff",
         "12.6.5 Kingdom Animalia — Invertebrates",
         "12.6.5 Kingdom Animalia",
         "handoff/label-stem",
         "routes U10 (12.6.5 kingdom animalia — multicellular, heterotrophic eukaryotes); "
         "dropping the '— Invertebrates' qualifier leaves the shared stem"),
    ],
  },
  # ── S3 · science · IX · BATCH WAVE 2 (the COMPACTS) — 2026-08-17, v1.2 ──────────────
  # ch 4 p13: the FIRST true route correction (founder ruling 2026-08-17). The 4.4.1 row
  # routes [11, 12, 13], but U12 is a pure graphs+kinematics consolidation — its own note
  # says it "weaves together 4.2.2, 4.2.3, 4.3", its anchor carries exactly those three
  # tokens, and the unit contains zero occurrences of "circular", "4.4" or "plane". An
  # item routed there lands on a sitting that never taught its section. U12 is struck;
  # U11 (first teach) and U13 (closing consolidation, 4.4.1 token in its anchor) remain.
  # ANCHOR-AT-LAST-UNIT: the section's last routed unit is U13 before and after the edit,
  # so no item moves.
  ("science", "ix"): {
    "ch_04_canonical_p13.json": [
        ("handoff-route",
         ("4.4.1 Uniform circular motion", [11, 12, 13]),
         [11, 13],
         "handoff/route",
         "U12 verifiably does not teach 4.4.1 (0 hits for circular/4.4/plane; anchor and "
         "note both name only 4.2.2/4.2.3/4.3); last routed unit stays U13, so item "
         "anchoring is unmoved"),
    ],
    # ch 8 p07: the SS·viii ch 8 family in miniature — the unit's TEACHING is right and its
    # LABEL is short. U3's closing band presents "Bohr's 1913 resolution: electrons occupy
    # fixed-energy stationary states (shells K, L, M, N)… resolving the collapse problem" —
    # that IS section 8.2.3, and the handoff row correctly routes 8.2.3's cell to U3. The
    # anchor named only 8.2.2. Extending it to the ' / '-joined pair (both tokens verbatim
    # from the top registry) clears, in one edit: the mis-route, the first-visit skip of
    # 8.2.3, and the OMITS advisory.
    "ch_08_canonical_p07.json": [
        (3,
         "8.2.2 Testing Thomson's model: The gold foil experiment",
         "8.2.2 Testing Thomson's model: The gold foil experiment / "
         "8.2.3 Bohr's model of the atom",
         "V2/mis-anchored",
         "the 35-50 band teaches Bohr's stationary states after Rutherford; the handoff "
         "already routes 8.2.3 -> [3]; both tokens verbatim in the top registry"),
    ],
    # ch 12 p12: U9 anchored "12.7.1 The hierarchical nature of classification" — a REAL
    # summary section the top never anchored, so it is outside the registry (the runbook's
    # "section missing from registry" family). Check 11 never flagged the top's omission:
    # its 17-vs-17 count coincides because the registry counts 12.6.5 twice while the
    # summary counts 12.7.1. Serving validates compact anchors ⊆ top registry, so X=10 and
    # X=11 raised SERVE INVALID. FOUNDER RULING 2026-08-17: align the compact to the top —
    # strip the foreign token; the hierarchy teaching stays in U9 as its opening bands
    # (units may teach more than their anchor names). The handoff row's label is left as
    # authored: the new anchor is a substring of it, so the agreement check passes, and its
    # section_context keeps the full cell description.
    "ch_12_canonical_p12.json": [
        (9,
         "12.7.1 The hierarchical nature of classification / "
         "12.8 Scientific Naming — The Binomial System",
         "12.8 Scientific Naming — The Binomial System",
         "V2/registry-omission",
         "the top registry has no 12.7.1; one label edit clears anchor-verbatim, "
         "first-visit and both SERVE INVALIDs; no teaching text changes"),
    ],
  },
}


def registry_of_library():
    """Compile the library and derive the registry from the top canonical, exactly as
    build_library.certify does — so what is printed here is what certification will see.
    v1.1: a file absent from the library is read from its newest quarantined copy (the
    same route apply_file takes) so the BEFORE registry of a quarantined chapter prints
    instead of raising."""
    nn = f"ch_{CHAPTER:02d}"
    paths = [LIB / f"{nn}_canonical.json"] + sorted(LIB.glob(f"{nn}_canonical_p*.json"))
    lib = []
    for p in paths:
        src = p
        if not p.is_file():
            qs = sorted((QUAR / LIB.parent.name / LIB.name).glob(p.name[:-5] + "_*.json"))
            if not qs:
                continue
            src = qs[-1]
        lib.append((p.name, compile_stream(json.loads(src.read_text(encoding="utf-8")))))
    if not lib:
        raise SystemExit(f"no canonical for ch {CHAPTER} in the library or quarantine")
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


def handoff_agreement():
    """Mirror build_library's handoff/anchor gate for this chapter's library — a handoff
    repair that leaves the agreement broken must be visible immediately (v1.1)."""
    nn = f"ch_{CHAPTER:02d}"
    paths = [LIB / f"{nn}_canonical.json"] + sorted(LIB.glob(f"{nn}_canonical_p*.json"))
    out = []
    for p in paths:
        if not p.is_file():
            continue
        raw = json.loads(p.read_text(encoding="utf-8"))
        s = compile_stream(raw)
        anchors_of = {}
        for u in s["units"]:
            raw_u = next((x for x in raw["result"]["lesson_plan"]["periods"]
                          if x.get("period_number") == u["unit"]), {})
            a = raw_u.get("section_anchor") or raw_u.get("section_ref") or ""
            anchors_of[u["unit"]] = ({"synthesis"} if is_synthesis_unit(u)
                                     else {_norm(t) for t in a.split(" / ")})
        mis = []
        for e in (raw["result"].get("coverage_handoff") or []):
            if not isinstance(e, dict):
                continue
            ref = _norm(e.get("section_ref") or e.get("section_label")
                        or e.get("section_title") or "")
            for pn in [int(x) for x in (e.get("period_numbers") or []) if x is not None]:
                have = anchors_of.get(pn)
                if have is None:
                    mis.append(f"U{pn} (no such unit) <- {ref or '?'}")
                elif have == {"synthesis"}:
                    continue          # synthesis carve-out — mirrors build_library (2026-08-18)
                elif ref and not any(ref in a or a in ref for a in have):
                    mis.append(f"U{pn} anchors {sorted(have)} <- routed {ref!r}")
        out.append((p.name, mis))
    return out


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
        if unit_no == "handoff-route":
            # v1.2 handoff ROUTE edit (founder ruling 2026-08-17, ch 4 p13): strike a unit
            # from a row's period_numbers when the unit verifiably does not teach the row's
            # section. old = (verbatim section_label, exact current period_numbers);
            # new = the corrected list. The anchor-at-last-unit invariant must be argued in
            # the note — an edit that moves a section's LAST routed unit moves its items.
            label, old_pns = old
            # TRAP 6 (runbook §4): the row's label field differs by stage. SS·IX carries
            # `section_label`; mathematics·IX carries `section_ref` + `section_title` and no
            # label at all, so a matcher that reads one key finds zero rows and the repair
            # refuses with "declared text not found" against text that is plainly there.
            # Read through the same seam the agreement check reads through (2026-08-18).
            def _rowlabel(e):
                return (e.get("section_label") or e.get("section_ref")
                        or e.get("section_title") or "")
            rows = [e for e in (plan["result"].get("coverage_handoff") or [])
                    if isinstance(e, dict) and _rowlabel(e) == label
                    and [int(x) for x in (e.get("period_numbers") or [])] == list(old_pns)]
            if len(rows) != 1:
                raise SystemExit(
                    f"{fname} handoff-route: declared (label, period_numbers) matched "
                    f"{len(rows)} row(s), need exactly 1 — the artefact has changed since "
                    f"this repair was written. Re-read it, do not force.\n"
                    f"  wanted: {label!r} {list(old_pns)!r}")
            if not dry:
                rows[0]["period_numbers"] = list(new)
            done.append({"unit": "handoff-route", "field": "period_numbers", "rule": rule,
                         "removed": f"{label!r} {list(old_pns)!r}",
                         "replaced_with": f"{list(new)!r}", "note": note})
            continue
        if unit_no == "handoff":
            # v1.1 handoff-row label edit: locate the row by its verbatim section_label.
            rows = [e for e in (plan["result"].get("coverage_handoff") or [])
                    if isinstance(e, dict) and e.get("section_label") == old]
            if len(rows) != 1:
                raise SystemExit(
                    f"{fname} handoff: declared label matched {len(rows)} row(s), need "
                    f"exactly 1 — the artefact has changed since this repair was written. "
                    f"Re-read it, do not force.\n  wanted: {old!r}")
            if not dry:
                rows[0]["section_label"] = new
            done.append({"unit": "handoff", "field": "section_label", "rule": rule,
                         "removed": old, "replaced_with": new, "note": note})
            continue
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
        kinds = {str(d["unit"]).startswith("handoff") for d in done}
        reason = ("handoff-row repair (label re-stem and/or route correction; unit "
                  "anchors stand untouched — certification's handoff/anchor agreement "
                  "gate, 2026-08-17)"
                  if kinds == {True} else
                  "V2 section-anchor joiner repair (';' read as one opaque registry "
                  "section; corrupted the derived registry, falsely quarantined p10, "
                  "and mis-served X=8/X=9)")
        gc = plan.setdefault("genon_canonical", {})
        gc.setdefault("repairs", []).append({
            "at": datetime.now().isoformat(timespec="seconds"),
            "tool": "genon/repair_anchors.py v1.1",
            "reason": reason,
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
            loc = "handoff row" if d["unit"] == "handoff" else f"U{d['unit']}"
            print(f"  {loc:<12} {d['field']:<16} [{d['rule']}]")
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
    ho_bad = 0
    print("handoff/anchor agreement:")
    for name, mis in handoff_agreement():
        ho_bad += len(mis)
        print(f"    {name:<28} {'OK' if not mis else f'{len(mis)} mis-route(s)'}")
        for m in mis:
            print(f"        {m}")
    return 1 if (bad or ho_bad) else 0


if __name__ == "__main__":
    sys.exit(main())
