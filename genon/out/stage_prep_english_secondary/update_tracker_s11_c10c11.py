#!/usr/bin/env python3
"""S11 — C10 closed (purge wired + verified through the API), C11 recorded."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C10_ADD = """

--- C10 CLOSED 2026-08-12, and the failing check is now verified THROUGH THE API. ---
The fix landed: purge_derived is wired into generate_canonical.install_canonical, so every regeneration now invalidates the chapter's derived plans exactly as every repair tool does. Unconditional by design - working out whether THIS canonical lends to any existing plan means reading every derived file and re-running the choice set, which is more machinery than deleting cheap artefacts. If the unlink fails (read-only mount) it warns and the install stands. Regression test in tests/test_genon_plan_key.py asserts install_canonical calls purge with the right chapter and apply=True; suites green.

CHECK 2(a) NOW MEASURED, not read: exercised the real endpoint in-process (fastapi TestClient against the live data root). POST X=11 -> 200, cached=False, file written. REPEAT the identical request -> 200, cached=TRUE, 4.2 ms, and the file's mtime DID NOT CHANGE. That was the one assertion C10 could not make without HTTP.

THE THREE RE-SERVES HAPPENED AS A SIDE EFFECT and they prove the whole chain: X=11, X=15 and X=16 all rebuilt from the RE-AUTHORED top, and none of the three now contains 'complete the draft article'. X=16 landed on the new key c20260812154258; X=11 and X=15 re-keyed on p10/p14 as before but with correct content behind them.

ONE STALE FILE REMAINS, AND IT IS MY ERROR TO NAME: ch_07_60m2-50m13_e19_c20260812142352.json - kumar3's mixed week - still carries the OLD synthesis. At C10 I wrote that the four surviving served plans 'carry no borrowed unit from the top'; that was wrong for the mixed week, which serves 15 sittings and borrows unit 17. I checked the c-token instead of the borrow. Re-serving it will NOT fix it: the key is p14's and does not move, so the request is a cache HIT returning the stale bytes - ARV-D-137's mechanism, still live for this one file. It must be DELETED:
    rm data/content/saved_plans/english/ix/ch_07_60m2-50m13_e19_c20260812142352.json
(The sandbox cannot unlink host-created files. Also strays there: ch_07_60m3-50m9_e19_c20260812142352.json, a 12-period mixed matrix I created while timing C11 - not part of C6's set, safe to delete with it.)"""

C11 = """MEASURED 2026-08-12 - PASS, three orders of magnitude inside budget. Exit is < 5 s; the endpoint answers a CACHE MISS in 8-16 ms.

Exercised the real POST /genon/english/ix/7/plan in-process (fastapi TestClient against the live data root), timed end to end including serve, file write and the prepared-plans register:
    X=11  cache MISS  16.3 ms   (first call - includes the library read and compile of all three canonicals)
    X=15  cache MISS   8.1 ms
    X=16  cache MISS   9.2 ms
    60x3+50x9 (fresh mixed matrix)  cache MISS  8.2 ms
    X=11  repeat, cache HIT  4.2 ms
Engine-only figures for the record: compiling all three canonicals 1.0 ms, serve_plan 0.24-0.34 ms across five runs. So the millisecond claim in testing.md ('selection + one compile should be milliseconds') holds literally, and the API's overhead is the file write and the register mark, not the engine.

DECLARED DEVIATION: measured through the ASGI app rather than over the wire with curl -w, because the Cowork sandbox cannot reach the founder's uvicorn. The difference is the loopback socket - microseconds against a 5-second budget - so the verdict is not in doubt; a curl figure would be tidier evidence, not a different answer."""


def main():
    st = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c10c11"))
    c = st["combos"][KEY]
    c["C10"]["status"] = "pass"
    c["C10"]["at"] = NOW
    c["C10"]["comment"] += C10_ADD
    c["C11"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C11}
    for d in st["defects"]:
        if d.get("id") == "ARV-D-137":
            d["status"] = "closed"; d["closed"] = NOW; d["at"] = NOW
            d["evidence"] += (
                "\n\nCLOSED 2026-08-12. `purge_derived` is now called from "
                "`generate_canonical.install_canonical` — every regeneration invalidates the "
                "chapter's derived plans, as every repair tool already did. Regression test in "
                "`tests/test_genon_plan_key.py` (asserts the call, its chapter and apply=True). "
                "The cache-hit half was then measured through the real endpoint: a repeat "
                "request returns `cached: true` in 4.2 ms with the file's mtime unchanged.\n\n"
                "ONE ARTEFACT OF THIS DEFECT SURVIVES ON DISK and needs a manual delete — "
                "`ch_07_60m2-50m13_e19_c20260812142352.json`, kumar3's mixed week, which borrows "
                "unit 17 and still carries the old synthesis. Re-serving cannot fix it: its key "
                "is p14's and does not move, so the request is a cache hit on the stale bytes. "
                "My C10 note claimed the surviving four served plans carried no borrowed unit "
                "from the top; that was wrong for the mixed week — I checked the c-token instead "
                "of the borrow.")
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"C10 pass · C11 pass · ARV-D-137 closed · {NOW}")


if __name__ == "__main__":
    main()
