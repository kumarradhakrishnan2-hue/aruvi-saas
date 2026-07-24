#!/usr/bin/env python3
"""Offline harness: builds a synthetic (greedy) delta for the target matrix and runs it
through apply_delta — proves validators + rebuild + remaps before any API spend."""
import json
import sys
import apply_delta as ad


def synth_delta(plan, matrix):
    periods = plan["result"]["lesson_plan"]["periods"]
    order, lookup = ad.build_source_index(periods)
    lengths = []
    for k in order:
        a, z = ad.parse_band(k[1])
        lengths.append(z - a)
    total_old = sum(lengths)
    total_new = sum(d * c for d, c in matrix)
    scale = total_new / total_old
    scaled = [max(3, round(l * scale)) for l in lengths]
    # trim/pad to exact total from the largest bands
    diff = sum(scaled) - total_new
    i = 0
    idx_by_size = sorted(range(len(scaled)), key=lambda i: -scaled[i])
    while diff != 0:
        j = idx_by_size[i % len(scaled)]
        if diff > 0 and scaled[j] > 3:
            scaled[j] -= 1; diff -= 1
        elif diff < 0:
            scaled[j] += 1; diff += 1
        i += 1

    durs = [d for d, c in matrix for _ in range(c)]
    new_periods = []
    bi = 0
    carry = None  # (key, remaining_len) for a split band
    for n, dur in enumerate(durs, 1):
        cur = 0
        bands = []
        seam = None
        while cur < dur:
            if carry:
                k, rem = carry
                take = min(rem, dur - cur)
                bands.append({"minutes": f"{cur}-{cur+take}",
                              "from": {"old_period": k[0], "band": k[1]}, "part": "b"})
                cur += take
                carry = None
                seam = "Open by recapping where the previous period stopped mid-activity."
                continue
            k = order[bi]; L = scaled[bi]
            if cur + L <= dur:
                bands.append({"minutes": f"{cur}-{cur+L}",
                              "from": {"old_period": k[0], "band": k[1]}})
                cur += L; bi += 1
            else:
                take = dur - cur
                bands.append({"minutes": f"{cur}-{dur}",
                              "from": {"old_period": k[0], "band": k[1]}, "part": "a"})
                carry = (k, L - take)
                bi += 1
                cur = dur
        srcs = {b["from"]["old_period"] for b in bands}
        new_periods.append({"n": n, "duration": dur, "bands": bands,
                            "title": "Merged unit" if len(srcs) > 1 else None,
                            "seam_note": seam})
    assert bi == len(order) and carry is None, "packer failed to consume all bands"
    return {"target_check": {"periods": len(durs), "total_minutes": total_new},
            "new_periods": new_periods}


if __name__ == "__main__":
    src, spec = sys.argv[1], sys.argv[2]
    plan = json.load(open(src))
    matrix = ad.parse_matrix(spec)
    delta = synth_delta(plan, matrix)
    json.dump(delta, open("/tmp/synth_delta.json", "w"), indent=2)
    print("synthetic delta:", len(json.dumps(delta)) // 4, "~tokens")
    adapted = ad.adapt(plan, delta, matrix, provenance={"mode": "dry-run"})
    json.dump(adapted, open("/tmp/adapted_dryrun.json", "w"), ensure_ascii=False, indent=2)
    ps = adapted["result"]["lesson_plan"]["periods"]
    print(f"OK  {len(ps)} periods rebuilt")
    for p in ps[:4]:
        tb = p["time_bands"]
        print(f"  P{p['period_number']} {p['period_duration_minutes']}min "
              f"bands={len(tb)} last={tb[-1]['minutes']} title={p['activity_title'][:40]!r}")
    hw = [p["period_number"] for p in ps if p["homework"]]
    print("homework now in:", hw)
    refs = sorted({r for it in adapted["result"]["assessment_items"] for r in it["period_ref"]})
    print("assessment refs span:", refs)
    # negative tests: corrupt deltas must be rejected
    import copy
    bad = copy.deepcopy(delta); bad["new_periods"][0]["bands"].pop(1)
    try:
        ad.adapt(plan, bad, matrix); print("FAIL: missing-band delta accepted")
    except ad.DeltaError: print("negative test 1 (missing band): rejected ✓")
    bad = copy.deepcopy(delta)
    b0 = bad["new_periods"][0]["bands"]; b0[0], b0[1] = b0[1], b0[0]
    try:
        ad.adapt(plan, bad, matrix); print("FAIL: reordered delta accepted")
    except ad.DeltaError: print("negative test 2 (reorder): rejected ✓")
    bad = copy.deepcopy(delta)
    bad["new_periods"][3]["bands"][-1]["minutes"] = "30-44"
    try:
        ad.adapt(plan, bad, matrix); print("FAIL: bad-sum delta accepted")
    except ad.DeltaError: print("negative test 3 (bad sum): rejected ✓")
