#!/usr/bin/env python3
"""S11 — C10 (storage conventions) + ARV-D-137, the re-author cache gap."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()
KEY = "english/secondary"

C10 = """CHECKED 2026-08-12 - 1, 4 and 5 PASS; 3 is N/A with reason; 2 FAILS as ARV-D-137 (S2). Full artefact: docs/testing_artefacts/c10_english_ix_ch07.md

1 FILENAMES - PASS, and the chosen-variant rule is proven live on all seven served plans: 50m9 and 50m11 key on p10's ledger ts (142824), 50m12/13/15 and the mixed 60m2-50m13 on p14's (142352), 50m16 on the top's (141916). Matrix duration-aggregated LONGEST-FIRST on the mixed week. Library files ch_07_canonical.json + _p14 + _p10, KK zero-padded, no collision with the served pattern.

2 CACHE HIT AND PURGE - FAIL, and it fails on exactly what this stage spent Rs 28.74 fixing. (a) The hit itself is correct by code: api/main.py computes the filename and returns cached: true from the file, discarding the freshly served plan; the HTTP half (flag + unchanged mtime) is owed to a run with uvicorn up. (b) THE PURGE IS THE GAP. purge_derived is called from normalize_options, repair_register, repair_anchors, repair_leaked_deliberation and repair_item_type - EVERY REPAIR TOOL AND NO GENERATOR. canonical_version()'s docstring says regenerating 'therefore produces a NEW key', and that is true only of the CHOSEN variant: a served plan can contain a unit BORROWED from another canonical, and the key does not name the lender. MEASURED: X=11 keys on p10 (c20260812142824) and X=15 on p14 (c20260812142352) - both files still on disk, both still containing 'complete the draft article', so BOTH WOULD BE SERVED FROM CACHE WITH THE WITHDRAWN SYNTHESIS. X=16 is safe only because its chosen variant IS the re-authored top, so its key moved to c20260812154258. ARV-D-034's family on the one path the 2026-08-04 fix did not cover: that fix moved invalidation into the repair tools, and a regeneration is not a repair.

3 NO OVERWRITE ACROSS ENGINE VERSIONS - N/A with reason: this is the first english chapter ever built, so no earlier-engine file exists to preserve and all seven served plans are e19. What the re-author demonstrates is the same property from the other side - it rewrote ch_07_canonical.json in place (library files are not version-keyed) and left every served file untouched, which is precisely why check 2 fails. The two rules are in tension and the resolution is that stale derived plans must be DELETED, never overwritten.

4 DETERMINISM - PASS. The same request served twice in-process is byte-identical except saved_at.

5 QUARANTINE INVISIBLE TO SERVING - PASS. Withholding p14 from the library moves X=12, 13 and 15 from variant 14 to variant 17, the key changes to that variant's version, and no response names the withheld file.

IMMEDIATE ACTION FOR THIS CHAPTER: delete the three served plans built from the old top - 50m11 (c...142824), 50m15 (c...142352) and 50m16 (c...141916). The other four (X=9, 12, 13 and the mixed week) carry no borrowed unit from the top and are unaffected; checked rather than assumed."""

DEFECT = {
    "id": "ARV-D-137", "combo": KEY, "step": "C10", "severity": "S2",
    "owner": "founder", "status": "open",
    "title": ("re-authoring a canonical does not purge the derived plans that BORROWED from "
              "it — the cache key names the chosen variant, never the lender"),
    "evidence": (
        "Measured on this chapter immediately after the ARV-D-136 re-author of the top:\n"
        "  X=11 -> key ch_07_50m11_e19_c20260812142824 (p10's version) — file ON DISK, and it "
        "still contains 'complete the draft article'\n"
        "  X=15 -> key ch_07_50m15_e19_c20260812142352 (p14's version) — same\n"
        "  X=16 -> key moved to c20260812154258 (the top IS its chosen variant) — safe\n\n"
        "So the two serves ARV-D-136 was raised about, and which cost Rs 28.74 to fix, are the "
        "two that would still be handed to a teacher unfixed — `api/main.py` returns the cached "
        "file and discards the correct plan it just computed.\n\n"
        "ROOT CAUSE. `purge_derived` is wired into every REPAIR tool (normalize_options, "
        "repair_register, repair_anchors, repair_leaked_deliberation, repair_item_type) and "
        "into no GENERATOR. `canonical_version()`'s docstring — 'regenerating the canonical "
        "therefore produces a NEW key' — holds only for the chosen variant; a served plan can "
        "carry a unit BORROWED from another canonical, and the key does not name the lender. "
        "Re-author the lender and the content changes while the key stands still. This is "
        "ARV-D-034's family (stale bytes served because the key did not move) on the one path "
        "the 2026-08-04 fix did not cover.\n\n"
        "REMEDY, founder call: (1) call `purge_derived` from `generate_canonical`'s install "
        "path, exactly as every repair tool does — consistent with the doctrine, and the cost "
        "is already accepted in writing ('a teacher holding a purged plan loses that file and "
        "re-prepares'); or (2) name the lender in the key (`c<chosen>` + `b<lender>`), which "
        "re-keys only borrow-bearing plans but hangs a second token off the filename, the very "
        "thing reverted on 2026-08-04 for readability.\n\n"
        "IMMEDIATE, for this chapter: delete ch_07_50m11_e19_c20260812142824.json, "
        "ch_07_50m15_e19_c20260812142352.json and ch_07_50m16_e19_c20260812141916.json. The "
        "other four served plans carry no borrowed unit from the top and are unaffected."),
}


def main():
    st = json.loads(STATE.read_text(encoding="utf-8"))
    shutil.copyfile(STATE, STATE.with_suffix(".json.bak_pre_s11_c10"))
    st["combos"][KEY]["C10"] = {"status": "fail", "by": "Claude", "at": NOW, "comment": C10}
    assert DEFECT["id"] not in {d.get("id") for d in st["defects"]}
    DEFECT.update({"opened": NOW, "closed": None, "at": NOW})
    st["defects"].append(DEFECT)
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, indent=1, ensure_ascii=False), encoding="utf-8")
    print(f"C10 FAIL recorded · {DEFECT['id']} opened · {NOW}")


if __name__ == "__main__":
    main()
