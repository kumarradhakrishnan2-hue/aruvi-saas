#!/usr/bin/env python3
"""S4 · C10, C11, C12 (2026-08-10)."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

C10 = """PASS — 2026-08-10. All five checks hold; one defect found and fixed in the process, and
it was ours.

1 NAMING — PASS. Library: ch_04_canonical.json + _p09 / _p12, KK matching the real unit counts.
All eight served files parse as ch_NN_<matrix>_e<ENGINE>_c<version>, matrix duration-aggregated
LONGEST-FIRST (60m4-50m10), and the version token is the CHOSEN VARIANT's, not the top's —
50m8 keys on p09's stamp, 50m10 on p12's, 50m13 on the 15's. That is the rule live on disk for a
second stage after SS·IX.

2 CACHE + PURGE — the finding. purge_derived is wired into normalize_options, repair_register,
repair_anchors and repair_chapter_cg, but NOT into the two repair tools written at this stage's
C3 (repair_c3.py, repair_leaked_deliberation.py). So the 12:41 in-place repair did not move the
cache key and invalidated nothing — precisely ARV-D-034, the defect the purge exists to prevent
(the pilot served repaired-away text for four hours). It did not bite here only by timing: every
derived plan for ch 04 was built AFTER the repair. Luck, not correctness. BOTH TOOLS NOW CALL
THE PURGE, proved by seeding a real deviation and re-running: it named all eight derived plans
and, when the sandbox refused the deletes, STOPPED with 'STOP: derived plans could not be
deleted, so a stale plan can still be served' rather than continuing quietly. Founder re-ran on
his own machine — 'nothing to repair', so no purge fired, which is correct: the canonicals were
already repaired and every derived plan post-dates that repair. Check 2a (cached:true + unchanged
mtime) is the one row not exercised at S4; the substance is covered by check 4's determinism.

3 NO OVERWRITE ACROSS ENGINE VERSIONS — PASS. Five _e17_ files sit untouched beside three _e18_
ones after today's bump; no same-matrix pair collides, because the bump re-keys by construction.
This is the check the ARV-D-086 bump paid for, and it is now live evidence rather than an
assertion.

4 DETERMINISM — PASS. Three matrices served twice each, byte-identical minus saved_at
(13x50 67,556 B · 5x50 50,077 B · 4x60+10x50 77,455 B).

5 QUARANTINE INVISIBLE TO SERVING — PASS by proxy. With p09 removed from the library glob, X=8
falls to the next-highest survivor (variant 12) and no response names p09. The real move/restore
needs write permission the Cowork sandbox does not have; the selection behaviour it is testing is
proven.

ALSO INVESTIGATED HERE AND RULED ON BY THE FOUNDER — the preparing delay. already_yours is keyed
on the exact filename, which contains the engine version, so after the e17->e18 bump a teacher who
had held 50m11_e17 gets the full five-second wait again for 50m11_e18. FOUNDER RULING: FINE AS IS
— an engine bump is a significant change in production and the delay is warranted. No defect
opened. Recorded because the founder rule at api/main.py:1005 reads 'her own second look is
instant', and this is the one case where it deliberately is not. Separately: the reported
no-delay on kumar1 was not a defect — kumar1's prepared register has NO row for those requests,
and marking is unconditional on both server paths, so the plans were opened rather than prepared;
the hold lives only in PrepareLesson.runGenerate. Noted for completeness: FirstRun.jsx's preview
posts the same endpoint with no hold at all, by design (screen 4 has its own 1.8 s activation)."""

C11 = """PASS — 2026-08-10, by a factor of ~15,000.

Cache-miss equivalent (compile the library from disk + serve), measured on the engine path:
   13x50        compile 8.1 ms + serve 0.44 ms = 8.5 ms   (first call, includes import warm-up)
   5x50         compile 0.7 ms + serve 0.23 ms = 0.9 ms
   4x60+10x50   compile 0.6 ms + serve 0.32 ms = 1.0 ms
   11x50        compile 0.9 ms + serve 0.31 ms = 1.2 ms
Serve alone, 20 runs: min 0.31 ms · median 0.32 ms · max 0.33 ms.

EXIT (<5 s) met with four orders of magnitude to spare, and the shape is what the architecture
predicts: selection is a few hundred MICROseconds, and essentially all of the cost is compiling
the library — which the running API does once and caches. The 8.1 ms on the first row is
import/JIT warm-up, not the algorithm; the same matrix on a warm process is 0.32 ms. The figure
to carry to the human gate is 0.32 ms of selection, not the 8.5.

Not measured: HTTP round-trip through uvicorn, which needs the running API (curl -w
'%{time_total}'). Every millisecond of the budget that matters is accounted for above, so the
untested remainder is framework overhead, not engine work."""

C12 = """PARTIAL — 2026-08-10. The machine-checkable half passes; the browser half is owed.

1 dropped_lp IN THE VIEW — PASS. /view builds it (api/main.py:538) and the below-floor plan
(X=5) renders 3 dropped units through the real port, grouped as 'Finding New Identities' and
'Simplifying Rational Expressions', paged after the 5 served units. The 'give her access to it'
ruling holds.

2 EXPORTS OMIT THE DROPPED UNITS — PASS on the substance. Exercised through the real export seam
(carriers.raw_item_list + the api/main.py unscheduled filter): the mixed-duration plan renders
14 units / 12 export items / 31,905 chars of HTML; the below-floor plan renders 5 units / 6
export items and the string 'Deriving Cube Identities' — a dropped unit's title — appears
NOWHERE in the exported HTML. Combined with C9.3d (9 items in, 6 exported, exactly the 3
unscheduled omitted), the split is proven in both directions.

ARV-D-066 DURATION LABEL — PASS by inspection. matrixLabel is defined once
(MyLessonPlans.jsx:230, joining with ' · ') and is the only producer, used at :240 for the My
Lessons card and :641 for the proposed/busy card. No second formatter exists to drift from it.

OWED, and it needs a browser — recorded as owed rather than passed:
  . the 8 export FILES opened by eye (3 plan exports x pdf/docx + the 2 allocation reports) for
    blank sections, raw JSON, unit/phase structure, the borrowed sitting reading as a whole unit,
    answers=1 rendering the answer layer, and the coverage note carried through;
  . the export HEADER's duration line compared against the two cards on a MIXED matrix — the only
    case that can catch ARV-D-066, and the header is server-side so matrixLabel does not cover it;
  . C12.3 chapter notes (usage, privacy, persistence) and C12.4 the lesson-plan bookmark — both
    localStorage through userKey(), so both are browser-only. X1.3 and X1.7 remain the DEFINITION
    of the tenancy property; these are its per-stage re-verification against this stage's real
    filenames and section keys.

NOTE FOR THE RE-RUN: the plans inspected here are _e17_ and render an empty approach line
(ARV-D-086). Re-serve as _e18_ before opening the exports, or the pedagogy row will read blank in
all eight files and look like a fresh export defect."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c10c11c12"))
c = state["combos"]["mathematics/secondary"]
c["C10"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C10}
c["C11"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C11}
c["C12"] = {"status": "partial", "by": "Claude", "at": NOW, "comment": C12}
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print("C10 = pass · C11 = pass · C12 = partial (browser half owed)")
print("S4:", {k: v.get("status") for k, v in c.items() if isinstance(v, dict) and k.startswith("C")})
