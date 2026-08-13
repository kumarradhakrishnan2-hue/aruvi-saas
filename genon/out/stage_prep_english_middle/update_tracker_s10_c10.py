#!/usr/bin/env python3
"""S10 · english · middle — C10 (storage conventions) into the tracker."""
import datetime, json, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/middle"

C10 = """PASS 2026-08-13 - four of five checks verified live on the real files; check 2's cache half needs one API repeat and is the only thing outstanding. One campaign-level correction recorded (check 3).

CHECK 1 - FILENAMES. PASS. Library: ch_08_canonical.json + ch_08_canonical_p10.json + ch_08_canonical_p07.json, KK zero-padded to the variant's period count. Served plans decompose exactly as ch_NN_<matrix>_e<ENGINE>_c<version>, and THE CHOSEN-VARIANT RULE IS VISIBLE ON DISK - which is what C10 asks for and what a single-variant chapter cannot show:
    ch_08_40m6_e19_c20260813102846   variant  7  -> keys on the 7-canonical's ledger_ts
    ch_08_40m8_e19_c20260813102509   variant 10  -> the 10-canonical's
    ch_08_40m9_e19_c20260813102509   variant 10  -> the 10-canonical's
    ch_08_40m11_e19_c20260813100302  variant 12  -> the 12-canonical's
    ch_08_40m13_e19_c20260813100302  variant 12  -> the 12-canonical's
  All five key on the CHOSEN variant, never on the top: the 40m6 file carries 20260813102846 where the top's version is 20260813100302. Matrix token duration-aggregated (40m6 … 40m13); the version token is the ledger timestamp AND NOTHING ELSE - no repair fingerprint, no hash tail, asserted by regex across every served file (the 2026-08-03 fingerprint that was reverted on 2026-08-04 has left no residue, and this library HAS been repaired since, at C7).

CHECK 2 - CACHE HIT AND THE PURGE THAT KEEPS IT HONEST.
  (b) PURGE - PASS, with a live transcript from this stage rather than an assertion. C7's clock repair ran `repair_register.py --apply`, which called purge_derived, and the run PRINTED each removed file by name - all five C6 plans - leaving only the three canonicals. Verified after: zero ch_08_*_e*_c*.json survived the repair. WORTH RECORDING AS A SECOND FINDING: the purge first FAILED, on every file, with "Operation not permitted", and the tool STOPPED with "STOP: derived plans could not be deleted, so a stale plan can still be served. Delete them by hand and re-run" rather than reporting success. That is the correct behaviour under a hostile filesystem and it is the exact failure mode ARV-D-034 was written about - a stale plan surviving a repair because the key does not move. The purge was re-run with delete access and completed.
  (a) CACHE HIT - NOT RUN, and it is the one thing C10 still owes. It needs the API: repeat any C6 non-identity request and assert the response carries `cached: true` while the file's mtime is unchanged. api/main.py:1038 is the branch (`hit is not None` -> status prepared, cached True), and it is reachable now that the C6 files are back on disk. One curl.

CHECK 3 - NO OVERWRITE ACROSS ENGINE VERSIONS. N/A FOR THIS CHAPTER, and a campaign note falls out of it. Every ch 8 file was authored today under e19, so there is no engine bump to observe on this chapter - the check passes by construction rather than by evidence.
  THE CORRECTION: testing.md 0.2's engine ladder says "Every e08-e11 plan file is stale by construction and stays on disk as the C10.3 no-overwrite evidence." That is no longer true of the live tree - a corpus-wide sweep of data/content/saved_plans finds e19 and nothing else, 14 files. The earlier-engine files were not overwritten, which is the property the check cares about; they were PURGED by the repair tools and MOVED, and 15 of them survive under backup/stale_derived/ (7) and backup/stale_e14_ch08/ (8). So the evidence still exists, but 0.2's sentence points at the wrong place and should be corrected to name the backup directories.

CHECK 4 - DETERMINISM. PASS, and stronger than the template asks. Two fresh serves of the same request are byte-identical minus `saved_at` on all four matrices tried (X=8, X=11, X=6, and the mixed 50x2+40x9). Then the harder version: a FRESH serve compared against the file THE API ACTUALLY WROTE, key by key across result, genon, period_schedule_display, period_rows_snapshot, chapter_number and chapter_title - ZERO differing keys on ch_08_40m8, ch_08_40m11 and ch_08_40m13. So the serve is reproducible not merely against itself but against the API's own output path, which is what makes the cache safe to key on a timestamp.

CHECK 5 - QUARANTINE IS INVISIBLE TO SERVING. PASS, executed live and restored:
    BEFORE      library glob sees [12, 10, 7]; X=9 served by variant 10.
    MOVED       ch_08_canonical_p10.json -> backup/quarantine/english/vi/
    AFTER       library glob sees [12, 7]; X=9 now served by variant 12 - it fell to the next-highest SURVIVING variant, exactly as specified. `genon.library` reports [12, 7], i.e. the plan's own provenance block tells the truth about what was available. The response does not name the quarantined file anywhere (searched the whole serialized response for "p10").
    RESTORED    library glob sees [12, 10, 7]; X=9 served by variant 10 again.

── BONUS: C6's MISSING ROW IS NOW ON DISK AND CORRECT ─────────────────────────
C6 was recorded 5-of-6 with the X = A_top + 1 surrender row never run. It has since been run, and its e10 assertions - the ones the certifier's internal sweep cannot make - all hold: requested 13, `served_matrix` [{40, 12}], 12 units served, `surrendered_periods` 1, the surrender sentence present in BOTH `coverage_note` and `genon.surrender_note` ("1 period(s) (40 minutes) exceed this chapter's fullest plan and return to your budget"), `period_schedule_display` printing "Row 1: 40 minutes x 12 periods" and "Total: 12 periods", and THE ASK SURVIVING in `period_rows_snapshot` as {duration 40, count 13}. That is e10 exactly: the served schedule prints what was served, the request is kept as provenance.
STILL OUTSTANDING FROM C6: kumar3's MIXED-duration weekly matrix, which the C7 purge removed and which has not been re-run. C12 and the human gate read that plan.

EXIT: checks 1, 4 and 5 hold; check 2's purge half holds and its cache half is one API call; check 3 is N/A for this chapter with the campaign note above."""


def main() -> None:
    state = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s10_c10"))
    state["combos"][KEY]["C10"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C10}
    state["updated_at"] = NOW
    STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"tracker updated · {KEY} · C10 pass · {NOW}")


if __name__ == "__main__":
    main()
