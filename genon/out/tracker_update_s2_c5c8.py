#!/usr/bin/env python3
"""One-shot tracker write: S2 (social_sciences · middle) C5-C8, the e14 defect rows,
and the amendment to S1's C8 that e14 forces.

Run from the repo root with the API STOPPED (or just reload the page after — the API
load-modifies-saves per request, so a concurrent tick merges fine):

    python3 genon/out/tracker_update_s2_c5c8.py

Idempotent: re-running overwrites the same keys with the same values.
"""
import json
from datetime import datetime, timezone
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-04T21:05:00"


def step(status, comment, by="Claude"):
    return {"status": status, "by": by, "at": NOW, "comment": comment}


C5 = """[e14 RE-VERIFIED 2026-08-04 - PASS] Report read: genon/out/library_reports/\
social_sciences_viii_ch03_20260804_201201.md (byte-identical to 185153 apart from the \
timestamp; the 201201 run is the post-e14 re-certification required by testing.md S9). \
DETERMINISTIC CHECKS ALL PASS; backup/quarantine is EMPTY repo-wide (0 files).

Every gate re-derived INDEPENDENTLY from the artefacts, not taken from the report:
 1 library complete - files [canonical, p13, p10] vs canonical_plan.counts [16,13,10]; \
basis authored_standard, provisional false, registry_sections 11, authored [16,13,10]. \
Dispersion arithmetic checked: A=16, floor=round(0.6x16)=10, A-C=6 >= 4 -> {16, ceil(26/2)=13, 10}.
 2 compiles - NOT VISIBLE in the report (load_library only emits a line on FAILURE, the \
same reporting gap logged at SS-secondary C5). Verified here by calling compile_stream on \
all three: 16 / 13 / 10 units, clean.
 3 anchors verbatim - 0 unresolved against the 11-section registry, all three files.
 4 first-visit order - 0 violations. Revisit tails present and legal (top U13 and U15; p13 U12 and U13).
 5 coverage - frontier reaches section 10 of 10 in all three. The standard reaches it at \
U14, i.e. before A-1 = 15 and before the synthesis.
 6 synthesis-anchor gate - top: token on U16 only and U16 is last; p13/p10: token absent entirely.
 7 serve sweep - X=8..18 = floor-2 .. top+2, reproduced exactly, no exception at any X.
 8 no defensive truncation - explicit PASS for all eleven; Case 3 never entered.
 9 register clean - 0 ban hits per file, scan proven to have REACHED the text (64 / 52 / 40 \
bands read, plus titles, notes, homework).
 9a MCQ options in arrangement order - PASS on all three; unarranged() returns [] independently.
 10 item counts per competency (ADVISORY) - one miss, see below.

SWEEP UNDER e14 (self-preference; the pre-e14 sweep differed at X=11 and X=14 only):
  8 fill/single -2s | 9 fill/single -1s | 10 identity | 11 fill/single | 12 synthesis \
| 13 identity | 14 fill/single | 15 synthesis | 16 identity | 17-18 surrender.
Zero drops anywhere inside [floor 10, top 16]; drops occur only below the floor, as declared.

ADVISORY MISS carried to C4: ch_03_canonical_p13.json ships 19 items where 20 are mandated \
- C-9.1 (Present) carries 1 MCQ, assessment v2.4 lines 51-53 mandate 2; both siblings carry 2. \
ARV-D-019 applies (generation variance, hand back-fill forbidden by S7, regeneration is a \
founder call on cost). Verdict unaffected by the basis: EXACT_ITEM_COUNTS has no \
("social_sciences","middle") row so the census fell back to the derived modal \
{Central 5, Substantive 3, Present 2} - which is IDENTICAL to what v2.4 mandates. The missing \
table row is bookkeeping, not a wrong reading; ARV-D-048 filed.

EXIT: report says ALL PASS; quarantine empty."""


C6 = """[e14 2026-08-04 - PASS] Every row of the C6 table returned as expected. Library \
{16,13,10} authored at 45 min (class VIII standard), floor 10, registry 11 sections, engine e14.

  X = each canonical's own count | kumar1 | 45m16 / 45m13 / 45m10 -> identity: true, the \
canonical's own filename, NO new file saved. Evidence is the prepared register (identity \
saves nothing by design), marked 14:11-14:12.
  X between two canonicals (complete fill) | kumar3 | 45m14 -> mode fill / fill_class single, \
self_fill TRUE, variant_used 16, provenance TOP:1..TOP:14 (a pure prefix under e14), \
uncovered_sections empty, no coverage note, 3 unserved items (top U15+U16), tiling exact.
  X where the prefix completes coverage early | kumar2 | 45m12 -> mode synthesis, \
borrowed_from 16 = THE STANDARD'S `synthesis` UNIT, note reads "Every section is covered; \
the closing sitting draws the chapter together in one synthesis." 2 unserved items (p13 U12+U13).
  X = A_top + 1 | kumar2 | 45m17 -> surrendered_periods 1, surrender sentence in \
coverage_note (e09 channel) with surrender_note as provenance, and the SERVED schedule \
prints "45 minutes x 16 periods" not the 17 asked (e10); the request survives in genon.matrix.
  X = floor - 1 | kumar2 | 45m9 -> mode fill with uncovered_sections ["The Maratha legacy"], \
coverage_note names it, result.dropped_units carries 1 unit flagged unscheduled SOURCED FROM \
THE LENDER (e12), assessment_items_unscheduled 3. Also ran 45m8 (2 drops, 5 unscheduled items).
  mixed-duration weekly matrix | kumar3 | 60m3+45m9 = 12 -> mode synthesis, borrowed_from 16, \
self_fill FALSE (the one genuine cross-plan borrow in the band), provenance p13:1..p13:11 + \
TOP:16. duration_sequence [45,45,60,45,45,45,60,45,45,45,60,45]: shortest sitting OPENS the \
week, the three 60s are interior and NEVER adjacent, last sitting short. scale 1.0 / 1.333, \
TILING EXACT on all 12 sittings. This is the plan C8/C9/C12 inspect.

THE IDENTITY NUANCE asserted deliberately: 60m16 does NOT fire identity (the rule matches the \
AGGREGATED matrix against a variant's standard row, so {60:16} misses {45:16}); the top is \
served whole at scale 1.333 and a file IS written. Exact tiling asserted there, not identity.

FILENAMES follow C10.1: matrix duration-aggregated longest-first (60m3-45m9), version = the \
CHOSEN variant's canonical_version, not the lender's - 60m3-45m9 keys on c20260804162039 (p13) \
even though the top lent the synthesis unit.

EXIT: every row returned as expected; responses recorded."""


C7 = """[e14 2026-08-04 - PASS, one item verified by hand rather than by the gate]

(a) THE MACHINE GATE: the certification report reads "register clean (0 ban hit(s))" for all \
three library files, and the scan is proven to have REACHED the band text (64 / 52 / 40 bands, \
plus activity_title, teacher_notes, homework). Re-run independently this session via \
genon/register_scan.py on the three canonicals AND on every served plan: 0 ban hits everywhere.

(b) ADVISORY HITS RULED ON - nine in total, all benign, none promoted to a defect:
  - 4 POSITIONAL, all backward: top U3 notes "The previous unit covered Shivaji's military \
campaigns through Purandar"; top U3 band 8-22 "the previous unit's geography"; top U5 notes \
"The northward expansion narrative from the previous unit"; top U7 notes "The civilian \
administration established in the previous unit". Backward reference is LEGAL under the v1.10 \
re-cut (which SS-middle carries at LP v2.8); none of the four also names a clock quantity or a \
calendar word, which is the only thing that would make a backward reference a defect. Style \
note, not a breach: Rule 10 asks continuity to be named by CONTENT rather than position, and \
these name position - carried to C3's register/tone column, not filed here.
  - 4 CALENDAR, all the classroom "today", not a schedule: p13 U7 band 0-8 "today we look at \
how the Marathas maintained law and order"; p13 U12 band 0-10 "Today we look at three sources"; \
p10 U2 band 34-45 "the events studied today"; p13 U9 notes "the Maheshwar handloom tradition \
(which continues today)" - the last is chapter CONTENT. testing.md C5.9 names exactly this \
class of hit as advisory by design ("a gate that failed on 'Will it rain today?' would be \
switched off in a week").

(c) READ FOR WHAT REGEX CANNOT SEE - swept all three canonicals and all served plans for \
paraphrased forward reference ("later in this chapter", "that follow", "bridges toward", \
"sets up", "leads into"), for opening moves that assume a specific prior activity, and for \
closing units that imply completion without saying so. NOTHING FOUND. The contrast with \
SS-secondary is worth recording: that library produced ARV-D-038 (a forward reference TRUE in \
the canonical and FALSE the moment a serve ended on that unit). This library's units close on \
their own ground. No new pattern for register_scan.py.

DROPPED UNITS - VERIFIED BY HAND, NOT BY THE GATE. C7 explicitly covers result.dropped_units \
("which a teacher reads on screen"), and ARV-D-036 (OPEN) proves register_scan does not read \
them: scanned_fields() walks lesson_plan.periods only. I read both dropped units on the 45m9 \
and 45m8 serves directly - "Thanjavur: A Syncretic Kingdom at the Southern Frontier" and \
"The Maratha Legacy: Sovereignty, Governance, and Seeds of Freedom" - titles, notes, bands and \
homework: clean, no clock quantity, no forward reference, no calendar word. The second one's \
note is exemplary for a self-study block: "designed to stand independently - students who \
arrive at this unit without the earlier ones can engage with the legacy claims using the \
summary." PASS stands on that manual read; ARV-D-036 stays open.

EXIT: zero live-ban hits; every advisory ruled on; no defect opened."""


C8 = """[e14 2026-08-04 - PASS, zero `jumpy`] Read sitting X-1 and sitting X in full, \
consecutively, as the teacher meets them, on the SERVED plans.

WHAT e14 DID TO THE INSPECTION SURFACE. Under self-preference, NINE of the eleven serves in \
this band are a VERBATIM PREFIX of a single canonical - the X-1 -> X joint is the consecutive \
pair the author wrote, so there is nothing for C8 to rate that C3 did not already read. Before \
e14, X=11 and X=14 each pulled in a foreign closing unit. The band now reduces to exactly two \
transitions plus the below-floor endings.

TRANSITION 1 - X=12, THE ONLY CROSS-PLAN BORROW (p13 U11 -> top U16 synthesis; files \
ch_03_45m12_e14 and the mixed ch_03_60m3-45m9_e14): SERVICEABLE.
Nothing presumes exposure the prefix did not give. Sitting 12 opens "Students receive the \
synthesis wheel with five spokes ... populate each spoke with two specific, concrete pieces of \
evidence from the chapter" - every prompt reaches for chapter content, never for a prior \
activity, and its worked examples (Pratapgad, Kanhoji Angre and the cartaz, \
Rajya-Vyavahara-Kosha, Serfoji II's Dhanwantari Mahal) all sit inside p13's eleven-sitting \
prefix. Its teacher note states the contract outright: "This synthesis unit may be encountered \
by students who covered the chapter's sections through different activities than the canonical \
sequence - so every spoke of the wheel draws on section content, not on any specific prior \
activity." That is the variant brief landing in authored text.
The register shift, named: sitting 11 ALREADY closes on an evaluative written response \
("write a 4-5 sentence reflective response ... What does the arc of their history teach us \
about what makes a political power endure or decline?") and sitting 12's core is another \
("write a 150-200 word synthesis paragraph ... evaluate whether the Maratha state actually \
realised Swarajya"). Two closers back to back, same cognitive move, overlapping content. A \
teacher absorbs it - she frames 12 as the larger version - so this is REDUNDANCY, which S0.4 \
holds to be contextually safe, not jumpiness. No defect.

TRANSITION 2 - X=15, A WITHIN-PLAN SKIP (top U14 -> top U16; U15 omitted; file \
ch_03_45m15_e14): SERVICEABLE. Not named as a class in the C8 template - same plan throughout, \
self_fill true, no foreign priors - but it is NOT a verbatim prefix, so it is inspected. The \
dropped U15 ("Bhakti, Swarajya, and Inclusion: The Cultural Foundations Revisited") is a \
revisit of registry section 0; U16's five spokes draw on Military / Culture / Trade / \
Administration / Legacy, all covered by sittings 1-14. No orphaned reference. Same doubling as \
transition 1, slightly sharper: sitting 14 closes "this is the chapter's interpretive climax" \
and sitting 15 opens the actual climax. Recorded but NOT an engine finding - the doubling is a \
property of the standard canonical's own tail (U14 legacy -> U16 synthesis) and is present at \
X=16, where nothing is borrowed at all.

BELOW-FLOOR ENDINGS - both CLEAN. X=9 (ch_03_45m9_e14): last served sitting closes "what \
questions would a historian need to ask before trusting it? ... how empires record their own \
histories" - a genuine ending, no forward gesture; the coverage note names the missing section \
and the dropped unit is written to stand alone. X=8: closes "whose stories get recorded and \
why it matters" - again a real ending; 2 drops, both named, both self-contained.

CLASSES NOT EXERCISED: fill/forward and fill/backward are N/A - this library produces neither \
at any X in [floor-2, top+2]. Recorded rather than hunted, as at SS-secondary.

EXIT: a rating per inspected transition with quoted evidence; ZERO `jumpy`; no defect opened."""


def main():
    st = json.loads(STATE.read_text())
    mid = st["combos"]["social_sciences/middle"]

    mid["C5"] = step("pass", C5)
    mid["C6"] = step("pass", C6, by="Kumar + Claude")
    mid["C7"] = step("pass", C7)
    mid["C8"] = step("pass", C8)

    prov = mid["provenance"]
    prov["engine"] = ("14 at C5-C8 (authored and first certified under 12; e13 = unserved "
                      "assessment items absent, e14 = SELF-PREFERENCE in the Xth-unit "
                      "tie-break, 2026-08-04). Post-e14 re-certification report "
                      "20260804_201201 is byte-identical to the pre-e14 185153 apart from "
                      "the timestamp, so testing.md S9's cheap path is satisfied.")
    prov["at"] = NOW

    # ── S1's C8: e14 voids one of its two seams ──────────────────────────────
    sec = st["combos"]["social_sciences/secondary"]
    amend = ("\n\n[AMENDED 2026-08-04 at S2's C8 - e14 VOIDS SEAM A.] Self-preference "
             "(architecture v2.1) changes this chapter's X=8 serve: it is now a VERBATIM "
             "p10 prefix (p10 U7 -> p10 U8, consecutive as authored), so Seam A no longer "
             "exists as a seam. Consequences: A1 CLOSES - it WAS the tie-break, now fixed "
             "in code (ARV-D-047). A3 CLOSES - the duplicated organiser came from the "
             "borrowed p07 U7, which is no longer served. A4 must be RE-ADJUDICATED against "
             "the new serve (assessment_items_unserved 5, no drops). A2 SURVIVES unchanged - "
             "the carbon-footprint pledge thread p10 U7 opens is paid off in p10 U10, which "
             "X=8 still does not reach, and that was never about the borrow. SEAM B (X=9, "
             "p10 U8 -> top U12 synthesis) is UNCHANGED under e14; B1 and B2 stand. ACTION: "
             "re-run 50m8 on SS-IX and re-read that one plan before this step is re-signed.")
    if "e14 VOIDS SEAM A" not in str(sec["C8"].get("comment", "")):
        sec["C8"]["comment"] = str(sec["C8"].get("comment", "")) + amend
        sec["C8"]["status"] = "attention"
        sec["C8"]["at"] = NOW

    # ── defect rows ──────────────────────────────────────────────────────────
    defects = [
        {
            "id": "ARV-D-047", "combo": "campaign", "step": "C8", "severity": "S3",
            "owner": "Claude", "status": "closed",
            "opened": "2026-08-03T14:54:00", "closed": NOW, "at": NOW,
            "title": "Xth-unit tie-break had NO self-preference: the engine borrowed a "
                     "stranger's unit while the plan being served had its own",
            "evidence": "fill_slot's Case-2 sort was (overlap==0, overlap, -reach, "
                        "abs(count-requested), -count) — the chosen plan's unit, named "
                        "'the identity candidate' in architecture §0.4, carried no "
                        "privilege at all, so ties fell to pacing distance. SS·IX X=8: "
                        "p10's own U8 lost to p07 U7 on |7−8| < |10−8|, and p10 U8 is "
                        "written for that exact prefix ('The climate change mechanism "
                        "examined in the unit on greenhouse gases and fossil fuels…') "
                        "where p07 U7's back-reference is generic. SS·VIII X=11 (p10 U10 "
                        "over p13's own U11) and X=14 (p13 U11 over the top's own U14).",
            "notes": "Continuity, not correctness — every candidate is first-exposure and "
                     "therefore safe, which is why no gate could see it and nothing broke. "
                     "RAISED at SS·IX's C8 on 2026-08-03 (SEAM_READ_20260803.md finding A1) "
                     "with this exact one-line patch, and NEVER FILED AS A ROW — no ID, no "
                     "owner, no status — so nothing carried it and it recurred at SS·VIII. "
                     "That is the process lesson: a recommendation living only in a "
                     "narrative report has no mechanism to come back. | CLOSED 2026-08-04 "
                     "by architecture v2.1 §0.4 + serve.py e14: `0 if c['self'] else 1` "
                     "inserted between -reach and pacing distance. Tie-break only — below "
                     "reach, so it never promotes a home unit past a better preference "
                     "class (asserted in tests/test_genon_serve.py, with a second case "
                     "proving pacing still governs a tie between two foreigners). After "
                     "the patch EVERY Case-2 fill in both libraries is self_fill:true. "
                     "GENON_ENGINE_VERSION 13→14; canonicals untouched, ₹0.",
        },
        {
            "id": "ARV-D-048", "combo": "campaign", "step": "C5", "severity": "S4",
            "owner": "Kumar", "status": "open",
            "opened": NOW, "closed": None, "at": NOW,
            "title": "EXACT_ITEM_COUNTS has no ('social_sciences','middle') row though its "
                     "P2 is done — the advisory census silently falls back to the modal",
            "evidence": "build_library.py's EXACT_ITEM_COUNTS carries only "
                        "('social_sciences','secondary'). SS·middle's P2 landed assessment "
                        "v2.4 on 2026-08-04, so per testing.md C5.10 the row should exist; "
                        "the report instead prints 'basis: derived (modal count across this "
                        "library — no constitution row yet)'.",
            "notes": "NO WRONG VERDICT HERE: v2.4 lines 51–53 mandate Central 5 (2 MCQ + 1 "
                     "SCR + 1 ECR + 1 Open Task) · Substantive 3 · Present 2, which is "
                     "identical to the derived modal, so p13's C-9.1 miss was caught either "
                     "way. The risk is future: a variant that agrees with its siblings and "
                     "disagrees with the constitution would pass silently. One dict entry.",
        },
        {
            "id": "ARV-D-049", "combo": "campaign", "step": "C10", "severity": "S3",
            "owner": "Claude", "status": "closed",
            "opened": NOW, "closed": NOW, "at": NOW,
            "title": "The engine version is written in two places and they drifted: served "
                     "plans named _e14_ reported 'serve v2.1 / e13' inside",
            "evidence": "api/data.py GENON_ENGINE_VERSION keys the FILENAME; a separate "
                        "hardcoded literal in serve.py stamps genon.engine INSIDE the plan. "
                        "The e14 bump moved the first and not the second. Found by diffing "
                        "ch_03_45m9_e13_… against its e14 twin: the only differences were "
                        "`filename` and `saved_at` — genon.engine was byte-identical and "
                        "said e13 on both.",
            "notes": "No plan was ever served wrongly. The cost is that testing.md §9's "
                     "amber rule reads PROVENANCE, so a plan built by e14 that self-reports "
                     "e13 registers as 'no engine change' — the staleness detector was "
                     "blind, and only a twin-diff could reveal it. | CLOSED 2026-08-04: the "
                     "stamp reads e14 with the change appended, and a comment above it ties "
                     "the two strings together. CARRY-FORWARD: the twelve derived plans on "
                     "disk still carry the stale stamp, and re-requesting will NOT fix them "
                     "— the filename is already _e14_, so the request is a cache HIT. They "
                     "must be deleted first, or left to expire (founder: only the authored "
                     "canonicals survive long-term). Restart the API before the next serve "
                     "so nothing further is written stale.",
        },
    ]
    have = {d["id"] for d in st["defects"]}
    for d in defects:
        if d["id"] in have:
            st["defects"] = [x for x in st["defects"] if x["id"] != d["id"]]
        st["defects"].append(d)

    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2))
    print("wrote", STATE)
    for k in ("C5", "C6", "C7", "C8"):
        print("  social_sciences/middle %s -> %s (%d chars)"
              % (k, mid[k]["status"], len(mid[k]["comment"])))
    print("  social_sciences/secondary C8 ->", sec["C8"]["status"], "(amended)")
    for d in ("ARV-D-047", "ARV-D-048", "ARV-D-049"):
        row = next(x for x in st["defects"] if x["id"] == d)
        print("  defect %s -> %s (%s)" % (d, row["status"], row["severity"]))


if __name__ == "__main__":
    raise SystemExit(main())
