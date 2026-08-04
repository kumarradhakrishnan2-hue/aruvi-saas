#!/usr/bin/env python3
"""One-shot tracker write: S2 (social_sciences · middle) C9, C10, C11 + two defect rows.

    python3 genon/out/tracker_update_s2_c9c11.py

Idempotent: re-running overwrites the same keys with the same values.
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-04T22:10:00"


def step(status, comment, by="Claude"):
    return {"status": status, "by": by, "at": NOW, "comment": comment}


C9 = """[e14 2026-08-04 - PASS] Anchoring checked on ALL TWELVE served plans on disk, not a \
sample. Method: each item's provenance rebuilt by matching its full JSON body (minus the \
mutable period_ref / unscheduled / scheduling_note) back to the canonical it was authored in, \
then the anchor checked against where that unit actually landed. 59 distinct item keys across \
the library, ZERO ambiguous - so every verdict below is an identity, not an inference.

1. PREFIX REMAP - PASS. Every item whose anchor unit is served points at that unit's SITTING \
number. 200 served-anchored items across 12 plans, 0 errors. No item carries an empty \
period_ref anywhere (the pre-e13 orphan state is gone).

2. THE BORROWED UNIT BRINGS ITS OWN ITEMS - PASS, and the two cross-variant cases are the ones \
that matter:
   45m12       chosen p13, fill sitting 12 = TOP:16, 2 items, home TOP  <- CROSS-VARIANT
   60m3-45m9   chosen p13, fill sitting 12 = TOP:16, 2 items, home TOP  <- CROSS-VARIANT
   45m14 / 45m15 / 45m9   self-fill, items from the chosen plan's own unit
   In both cross-variant plans the closing sitting carries the TOP canonical's two items, \
anchored to sitting 12 - not p13's, and not the top's own unit-16 numbering.

3. UNSERVED AND DROPPED - PASS.
   (a) no empty period_ref anywhere;
   (b) unserved counts recomputed independently from the chosen variant's item list against the \
served units: reported == computed on ALL TWELVE (45m12 2/2 · 45m14 3/3 · 45m15 1/1 · 60m12 2/2 \
· 60m14 3/3 · 60m3-45m9 2/2 · 45m17, 45m8, 45m9, 60m16 all 0/0);
   (c) 45m9 - 1 dropped sitting (10), 3 items flagged unscheduled all anchored inside it, and \
2 handoff rows restored AND flagged. 45m8 - 2 dropped sittings (9, 10), 5 items flagged, 5 \
handoff rows restored and flagged;
   (d) exports omit exactly the unscheduled items - confirmed in api/main.py:1118 \
(`export_items = [i for i in ... if not i.get("unscheduled")]`) feeding assessment_to_view, \
while GET /view keeps them via dropped_lp. The e09/e13 split as specified; the RENDERED proof \
belongs to C12.

4. NO CROSS-VARIANT REFERENCES OF ANY OTHER KIND - PASS on all twelve. period_ref is always a \
length-one array inside the plan's own sitting range; every chapter_section names a section \
this plan teaches; no unit/period/sitting numbers leak into student-facing question_text, task \
or scaffold; the legacy phase_ref / band_refs / band_id keys are absent everywhere.

TWO NOTES, NEITHER A DEFECT:
 * THE LENDER-vs-PLAN NUMBERING DISTINCTION IS NOT EXERCISED HERE. C9.3(c) requires dropped \
items to be anchored to the dropped unit's sitting number IN THIS PLAN, "never the lender's own \
numbering". Both below-floor serves are SELF-FILL prefixes of p10, so the two numberings \
coincide ([10] and [9,10]). The rule holds trivially; it is not proven. SS-secondary proved it \
properly. Worth watching: e14 makes self-fill the normal case, so this may go untested \
campaign-wide unless a chapter produces a below-floor CROSS-PLAN fill.
 * THREE MCQs carry question_text of exactly "Refer to the table provided." - the whole question \
lives in visual_stimulus and the options. Coherent (the options are full propositions) and \
arguably the Rule 8 orienting-stem convention bleeding into MCQ, but a stem that asks nothing is \
a legibility question. Carried to the C3 record, not filed.

EXIT: zero mis-anchored items; every unserved/dropped item accounted for."""


C10 = """[e14 2026-08-04 - PASS on all five] Verified against the artefacts on disk and the \
code paths; the two steps needing a live API request are noted per check.

1. FILENAMES - PASS. Library: ch_03_canonical.json + ch_03_canonical_p13/_p10.json, and the KK \
suffix matches the unit count in both compacts. Served: all TWELVE files conform to \
ch_NN_<matrix>_e<ENGINE>_c<CHOSEN-variant-version>, matrix duration-aggregated LONGEST-FIRST \
(60m3-45m9), and the version token is the CHOSEN variant's, not the top's - proven by the pairs \
that differ: 45m12 and 60m3-45m9 key on c20260804162039 (p13) even though the TOP lent the \
synthesis unit; 45m9/45m8 key on c20260804162946 (p10); 45m14/45m15/45m17/60m14/60m16 key on \
c20260804161018 (top).

2. CACHE HIT + THE PURGE THAT KEEPS IT HONEST.
   (a) the hit path is api/main.py:969 - `load_saved_plan` returns the file and the handler \
returns `cached: true` WITHOUT calling serve_plan or save_generated_plan, so the file cannot be \
rewritten; only prepared_plans_repo.mark runs. Code-verified. The mtime assertion is Kumar's \
one live re-request.
   (b) purge_derived is wired into all three repair tools - repair_register.py, \
normalize_options.py and repair_anchors.py - and PRINTS what it removed \
("== derived plans invalidated by ... ==", one line per file, then the ~11 ms rebuild note), \
and raises SystemExit if any unlink fails so a stale plan can never survive silently. Confirmed \
live this session: the sandbox could not unlink and the tool STOPPED rather than reporting \
success. ONE LATENT BUG FOUND - see ARV-D-050.

3. NO OVERWRITE ACROSS ENGINE VERSIONS - PASS. 5 e13 files sit untouched beside 7 e14 files for \
this chapter. This check was N/A for SS-middle before the e14 bump (e13 was the first engine to \
serve VIII ch 3); it is satisfiable now ONLY because those e13 files were kept - a deletion \
proposed earlier in the session was reversed for exactly this reason.

4. DETERMINISM - PASS, and stronger than the step asks. Serving the same matrix twice in-process \
is byte-identical after dropping saved_at (45m12 · 60m3-45m9 · 45m9 · 45m16). Better: a fresh \
serve is byte-identical to THE FILE THE API ALREADY WROTE for 45m12, 60m3-45m9 and 45m14 - so \
determinism holds across processes and across the API/engine boundary, not just within one run.

5. QUARANTINE INVISIBLE TO SERVING - PASS (simulated at the library-glob level rather than by \
moving the file, since the sandbox cannot unlink). With p13 withheld the library reads [16, 10] \
instead of [16, 13, 10], and serving falls to the next-highest surviving variant: X=12 \
variant_used 13 -> 16, X=13 identity(13) -> fill(16), X=14 unchanged at 16. Asserted \
programmatically that the string "p13" appears NOWHERE in any response payload. Kumar's live \
mv-and-restore is the remaining confirmation.

EXIT: all five hold; two live confirmations (2a mtime, 5 mv/restore) outstanding on the \
founder's machine, neither expected to differ."""


C11 = """[e14 2026-08-04 - PASS, ~3 ms against a 5000 ms budget] Timed the CACHE-MISS path \
in-process: load all three canonicals from disk -> compile_stream each -> select -> adapt \
(scale + disperse + remap assessment) -> serialize the payload the API writes. 7 runs per \
matrix, median reported.

   45m12      synthesis borrow        median 3.3 ms   (min 3.1 / max 3.9)   108 KB
   60m3-45m9  mixed duration, borrow  median 3.1 ms   (min 3.0 / max 3.6)   108 KB
   45m9       below floor, 1 drop     median 3.1 ms   (min 3.0 / max 3.4)   102 KB
   45m14      fill/single             median 3.2 ms   (min 3.1 / max 3.5)   105 KB
   45m16      identity-shape          median 3.3 ms   (min 3.1 / max 3.5)   125 KB

Flat across every serve class - the borrow, the mixed matrix and the below-floor drop cost the \
same as a plain prefix, which is what "serving is SELECTION, never composition" should look \
like in a timer. Three orders of magnitude inside the budget, and consistent with the ~11 ms \
rebuild figure the purge note quotes (that figure includes the file write).

SCOPE, STATED HONESTLY: this measures the engine, not the socket. The API adds HTTP framing, \
_current_identity, the prepared-register write and one ~108 KB file write. Those are I/O of the \
same order, so the end-to-end figure should land in the tens of milliseconds - but the step asks \
for `curl -w '%{time_total}'` on a real cache-miss request and that is Kumar's to run. Recorded \
as the engine figure; if the curl comes back anywhere near 5 s the gap is HTTP/filesystem, not \
selection, and should be investigated as its own defect.

EXIT: < 5 s comfortably; actual figure recorded either way."""


def main():
    st = json.loads(STATE.read_text())
    mid = st["combos"]["social_sciences/middle"]
    mid["C9"] = step("pass", C9)
    mid["C10"] = step("pass", C10)
    mid["C11"] = step("pass", C11)

    defects = [
        {
            "id": "ARV-D-050", "combo": "campaign", "step": "C10", "severity": "S3",
            "owner": "Kumar", "status": "open",
            "opened": NOW, "closed": None, "at": NOW,
            "title": "repair_anchors.py calls purge_derived with a HARDCODED "
                     "social_sciences/ix/3 — reuse on any other chapter purges the wrong one",
            "evidence": "genon/repair_anchors.py:197 — "
                        "`purge(\"social_sciences\", \"ix\", 3, reason=…)`, and LIB is likewise "
                        "pinned to data/content/saved_plans/social_sciences/ix. The other two "
                        "repair tools take subject/grade/chapter as arguments.",
            "notes": "Harmless today because the script is a one-off written for SS·IX ch 3. "
                     "But it is the ARV-D-034 failure mode with a twist: pointed at another "
                     "chapter it would delete SS·IX ch 3's derived plans while leaving the "
                     "chapter it just repaired serving pre-repair bytes — a silent wrong "
                     "answer, and the purge would PRINT a confident success. Either "
                     "parameterise it like the other two tools, or make it refuse to run "
                     "outside SS·IX ch 3.",
        },
        {
            "id": "ARV-D-051", "combo": "campaign", "step": "C9", "severity": "S2",
            "owner": "Claude", "status": "closed",
            "opened": NOW, "closed": NOW, "at": NOW,
            "title": "Ragged assessment tables: a non-data line inside the pipe payload was "
                     "read as the header, so columns did not line up — online AND in PDF/Word",
            "evidence": "Founder-reported on SS·VIII ch 3's Maratha-navy MCQ: the payload "
                        "opens with a 2-cell TITLE row ('Maratha Naval Institution: Two "
                        "Functions | Evidence from the Chapter') above the real 3-cell header, "
                        "so every renderer built a 2-column head over a 3-column body. A "
                        "corpus scan found the same class of fault in 5 items: SS·VIII "
                        "canonical Q10 (leading title) and SS·IX canonical Q3/Q11 + p10 "
                        "Q3/Q14 (trailing one-cell '— Adapted from …' attribution rows).",
            "notes": "Root cause: the generator puts NON-DATA lines inside the pipe payload "
                     "and the schema rule is 'first row = header'. Fixed at the single shared "
                     "split point, normalize.parse_table, so one change reaches all four "
                     "renderers: a leading row strictly narrower than the body's modal width "
                     "becomes `caption` (cells joined ' · ' so a two-level head keeps every "
                     "word); a trailing one-cell line opening with a dash or Adapted from / "
                     "Based on / Source: becomes `source_note`; whatever survives is PADDED "
                     "to one width, never truncated. render/html.py, export_assessment_pdf.py "
                     "(+2 CSS rules), export_docx.py and LessonView.jsx (+2 CSS rules) now "
                     "print caption above and source note below, so no text is lost. "
                     "Corpus re-scan: 0 ragged tables, down from 5. Five new tests in "
                     "tests/test_stimulus.py, including a guard that a genuine 2-column "
                     "table's first row stays the header. OPEN FOLLOW-UP (not filed): an "
                     "advisory certification line counting non-uniform payloads would turn "
                     "this into a visible rate across the 926 authoring runs.",
        },
    ]
    st["defects"] = [x for x in st["defects"] if x["id"] not in {d["id"] for d in defects}]
    st["defects"].extend(defects)

    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2))
    print("wrote", STATE)
    for k in ("C9", "C10", "C11"):
        print("  social_sciences/middle %s -> %s (%d chars)"
              % (k, mid[k]["status"], len(mid[k]["comment"])))
    for d in defects:
        print("  defect %s -> %s (%s)" % (d["id"], d["status"], d["severity"]))
    print("  steps now:", list(mid))


if __name__ == "__main__":
    raise SystemExit(main())
