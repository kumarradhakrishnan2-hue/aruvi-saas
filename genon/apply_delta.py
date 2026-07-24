#!/usr/bin/env python3
"""Gen-on-gen deterministic applier.

Takes a certified pre-warm saved plan + a compact adaptation delta (emitted by the
model per genon_adaptation_doc.md) and rebuilds a full, renderer-compatible saved
plan for the new duration matrix. All content is copied verbatim from the source;
the only new text admitted is the delta's seam_note fields.

Usage:  python3 apply_delta.py <source_plan.json> <delta.json> <out_plan.json>
"""
import json
import sys
from collections import OrderedDict


def parse_band(s):
    a, b = str(s).replace("–", "-").split("-")
    return int(a), int(b)


class DeltaError(Exception):
    pass


def band_key(old_period, band):
    return (int(old_period), str(band))


def build_source_index(periods):
    """Global reading-order list of band identities + lookup to band dicts."""
    order = []
    lookup = {}
    for p in periods:
        for tb in p["time_bands"]:
            k = band_key(p["period_number"], tb["minutes"])
            if k in lookup:
                raise DeltaError(f"duplicate source band {k}")
            lookup[k] = tb
            order.append(k)
    return order, lookup


def validate_delta(delta, periods, new_matrix):
    """new_matrix: list of (duration, count) rows, e.g. [(45, 12)]."""
    expected_counts = sum(c for _, c in new_matrix)
    expected_total = sum(d * c for d, c in new_matrix)
    problems = []

    nps = delta.get("new_periods") or []
    if len(nps) != expected_counts:
        problems.append(f"expected {expected_counts} new periods, got {len(nps)}")

    # duration multiset must match the matrix
    want = sorted(d for d, c in new_matrix for _ in range(c))
    got = sorted(int(np["duration"]) for np in nps)
    if want != got:
        problems.append(f"duration mix mismatch: want {want} got {got}")

    # numbering 1..N in order
    nums = [int(np["n"]) for np in nps]
    if nums != list(range(1, len(nps) + 1)):
        problems.append(f"new period numbering not 1..N in order: {nums}")

    # per-period contiguity + sums
    for np in nps:
        dur = int(np["duration"])
        cur = 0
        for b in np["bands"]:
            a, z = parse_band(b["minutes"])
            if a != cur:
                problems.append(f"period {np['n']}: band {b['minutes']} not contiguous (expected start {cur})")
            if z <= a:
                problems.append(f"period {np['n']}: band {b['minutes']} non-positive")
            cur = z
        if cur != dur:
            problems.append(f"period {np['n']}: bands sum to {cur}, duration is {dur}")

    # global order + exact consumption (splits: same band twice, consecutive, parts a then b)
    src_order, _ = build_source_index(periods)
    consumed = []
    for np in nps:
        for b in np["bands"]:
            k = band_key(b["from"]["old_period"], b["from"]["band"])
            part = b.get("part")
            consumed.append((k, part))
    i = 0
    walked = []
    while i < len(consumed):
        k, part = consumed[i]
        if part == "a":
            if i + 1 >= len(consumed) or consumed[i + 1][0] != k or consumed[i + 1][1] != "b":
                problems.append(f"split band {k}: part 'a' not followed by part 'b'")
                walked.append(k)
                i += 1
                continue
            walked.append(k)
            i += 2
        elif part == "b":
            problems.append(f"split band {k}: part 'b' without preceding part 'a'")
            walked.append(k)
            i += 1
        else:
            walked.append(k)
            i += 1
    if walked != src_order:
        missing = [k for k in src_order if k not in walked]
        extra = [k for k in walked if k not in src_order]
        dupes = [k for k in set(walked) if walked.count(k) > 1]
        problems.append(
            "source bands not consumed exactly once in reading order"
            + (f"; missing={missing}" if missing else "")
            + (f"; unknown={extra}" if extra else "")
            + (f"; duplicated={dupes}" if dupes else "")
            + ("" if (missing or extra or dupes) else "; (ordering violation)")
        )
    return problems


def uniq(seq):
    out = []
    for x in seq:
        if x and x not in out:
            out.append(x)
    return out


def rebuild(plan, delta):
    result = plan["result"]
    periods = result["lesson_plan"]["periods"]
    by_num = {p["period_number"]: p for p in periods}
    _, lookup = build_source_index(periods)

    new_periods = []
    # bookkeeping for remaps
    minutes_to_new = {}       # old_period -> {new_n: minutes}
    last_band_new = {}        # old_period -> new_n containing its final source fragment

    for np in delta["new_periods"]:
        n = int(np["n"])
        dur = int(np["duration"])
        src_pnums = uniq([int(b["from"]["old_period"]) for b in np["bands"]])
        contrib = {}
        bands_out = []
        for b in np["bands"]:
            k = band_key(b["from"]["old_period"], b["from"]["band"])
            src = lookup[k]
            a, z = parse_band(b["minutes"])
            text = src["activity"]
            if b.get("part") == "b":
                text = "[Continued] " + text
            bands_out.append({"minutes": f"{a}-{z}", "activity": text})
            contrib[k[0]] = contrib.get(k[0], 0) + (z - a)
            last_band_new[k[0]] = n  # overwritten as later fragments appear
        for pnum, m in contrib.items():
            minutes_to_new.setdefault(pnum, {})[n] = minutes_to_new.setdefault(pnum, {}).get(n, 0) + m

        primary = max(contrib, key=contrib.get)
        srcs = [by_num[p] for p in src_pnums]
        title = np.get("title") or by_num[primary]["activity_title"]
        seam = np.get("seam_note")
        notes = [s.get("teacher_notes", "") for s in srcs if s.get("teacher_notes")]
        teacher_notes = "\n\n[Merged unit] ".join(notes)
        if seam:
            teacher_notes = f"[Seam] {seam}\n\n" + teacher_notes

        newp = {
            "period_number": n,
            "period_duration_minutes": dur,
            "activity_title": title,
            "section_anchor": " / ".join(uniq([s.get("section_anchor") for s in srcs])),
            "materials": uniq([m for s in srcs for m in (s.get("materials") or [])]),
            "visual_aids": "; ".join(uniq([s.get("visual_aids") for s in srcs if isinstance(s.get("visual_aids"), str)])),
            "time_bands": bands_out,
            "section_context": " / ".join(uniq([s.get("section_context") for s in srcs])),
            "pedagogical_approaches": uniq([a for s in srcs for a in (s.get("pedagogical_approaches") or [])]),
            "teacher_notes": teacher_notes,
            "homework": [],  # re-seated below
            "competency_edges": [],
        }
        seen_c = set()
        for s in srcs:
            for e in s.get("competency_edges") or []:
                if e.get("c_code") not in seen_c:
                    seen_c.add(e.get("c_code"))
                    newp["competency_edges"].append(e)
        new_periods.append(newp)

    # homework re-seat: to the new period holding the old period's final fragment
    for p in periods:
        hw = p.get("homework") or []
        if hw:
            target = last_band_new[p["period_number"]]
            new_periods[target - 1]["homework"] = (new_periods[target - 1]["homework"] or []) + hw

    # remap tables
    majority_map = {p: max(d, key=d.get) for p, d in minutes_to_new.items()}
    assess_map = dict(last_band_new)

    new_items = []
    for it in result.get("assessment_items", []):
        it2 = json.loads(json.dumps(it))
        refs = it2.get("period_ref")
        if isinstance(refs, list):
            it2["period_ref"] = sorted(uniq([assess_map[int(r)] for r in refs]))
        elif refs is not None:
            it2["period_ref"] = assess_map[int(refs)]
        new_items.append(it2)

    new_handoff = json.loads(json.dumps(result.get("coverage_handoff", {})))
    for c in new_handoff.values():
        for lo in c.get("los", []):
            if "period_number" in lo:
                lo["period_number"] = majority_map[int(lo["period_number"])]

    return new_periods, new_items, new_handoff, {"majority_map": majority_map, "assess_map": assess_map}


def adapt(plan, delta, new_matrix, provenance=None):
    problems = validate_delta(delta, plan["result"]["lesson_plan"]["periods"], new_matrix)
    if problems:
        raise DeltaError("delta rejected:\n  - " + "\n  - ".join(problems))
    new_periods, new_items, new_handoff, maps = rebuild(plan, delta)

    out = json.loads(json.dumps(plan))
    out["result"]["lesson_plan"]["periods"] = new_periods
    out["result"]["assessment_items"] = new_items
    out["result"]["coverage_handoff"] = new_handoff
    out["period_rows_snapshot"] = [
        {"id": i, "duration": d, "count": c} for i, (d, c) in enumerate(new_matrix)
    ]
    total = sum(d * c for d, c in new_matrix)
    nper = sum(c for _, c in new_matrix)
    rows = "\n".join(
        f"  Row {i+1}: {d} minutes × {c} periods = {d*c} minutes" for i, (d, c) in enumerate(new_matrix)
    )
    out["period_schedule_display"] = (
        f"Period schedule:\n{rows}\nTotal: {nper} periods · {total//60}h {total%60:02d}min"
    )
    out["genon"] = OrderedDict(
        source_file=plan.get("filename"),
        adapted_matrix=[{"duration": d, "count": c} for d, c in new_matrix],
        period_maps=maps,
        provenance=provenance or {},
    )
    return out


def parse_matrix(spec):
    """'12x45' or '10x40+4x30' -> [(45,12),(40,10),(30,4)] as (duration,count)."""
    rows = []
    for part in spec.split("+"):
        c, d = part.lower().split("x")
        rows.append((int(d), int(c)))
    return rows


if __name__ == "__main__":
    src, dlt, outp = sys.argv[1], sys.argv[2], sys.argv[3]
    matrix = parse_matrix(sys.argv[4]) if len(sys.argv) > 4 else [(45, 12)]
    plan = json.load(open(src))
    delta = json.load(open(dlt))
    adapted = adapt(plan, delta, matrix)
    json.dump(adapted, open(outp, "w"), ensure_ascii=False, indent=2)
    print(f"OK  wrote {outp}")
    print(f"    periods: {len(adapted['result']['lesson_plan']['periods'])}")
    print(f"    assessment items remapped: {len(adapted['result']['assessment_items'])}")
