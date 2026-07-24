#!/usr/bin/env python3
"""Aruvi partition engine.

Deterministic: phase stream + duration matrix -> full renderer-compatible saved
plan. No LLM. Role-aware boundary choice via DP:
  cost of cutting after a phase: consolidation 0 · development 2 · hook 6
  cost of splitting inside a phase: 10 (avoided unless a period cannot be filled)
Periods are filled to EXACT duration by proportional rescale of their phases
(integer, min 3 min). Seam notes are formulaic navigation text flagged
seam_pending_llm — the only non-verbatim text, clearly marked.

Usage: python3 partition.py <stream.json> <matrix e.g. 12x45 | 10x40+4x30> <out_plan.json>
"""
import json
import sys

CUT_COST = {"consolidation": 0, "development": 2, "hook": 6}
SPLIT_COST = 10
FILL_TOL = 0.18  # a period may draw 82–118% of its target minutes before rescale


def parse_matrix(spec):
    rows = []
    for part in spec.split("+"):
        c, d = part.lower().split("x")
        rows.append((int(d), int(c)))
    return rows


def choose_cuts(phases, durations, tol=FILL_TOL):
    """DP over (phase boundary, period index) minimizing boundary cost.
    Returns list of per-period phase-index ranges [(start, end_exclusive), ...]."""
    n = len(phases)
    total_src = sum(p["minutes"] for p in phases)
    total_tgt = sum(durations)
    scale = total_tgt / total_src
    pref = [0]
    for p in phases:
        pref.append(pref[-1] + p["minutes"] * scale)  # scaled cumulative minutes

    INF = float("inf")
    K = len(durations)
    # dp[k][i]: min cost to place first k periods consuming first i phases
    dp = [[INF] * (n + 1) for _ in range(K + 1)]
    back = [[None] * (n + 1) for _ in range(K + 1)]
    dp[0][0] = 0.0
    tgt_pref = [0]
    for d in durations:
        tgt_pref.append(tgt_pref[-1] + d)
    for k in range(1, K + 1):
        for i in range(1, n + 1):
            got_end = pref[i]
            want_end = tgt_pref[k]
            # pacing drift: soft cost only — the take-window below is the hard bound
            drift = abs(got_end - want_end) / durations[k - 1]
            for j in range(0, i):
                if dp[k - 1][j] == INF:
                    continue
                take = pref[i] - pref[j]
                if not (durations[k - 1] * (1 - tol) <= take <= durations[k - 1] * (1 + tol)):
                    continue
                cut = 0.0 if (i == n) else CUT_COST[phases[i - 1]["role"]]
                cost = dp[k - 1][j] + cut + drift * 4
                if cost < dp[k][i]:
                    dp[k][i] = cost
                    back[k][i] = j
    if dp[K][n] == INF:
        return None  # no whole-phase solution; caller will split
    ranges = []
    i = n
    for k in range(K, 0, -1):
        j = back[k][i]
        ranges.append((j, i))
        i = j
    return list(reversed(ranges))


def split_fallback(phases, durations):
    """Sequential fill allowing mid-phase splits (guaranteed feasible)."""
    total_src = sum(p["minutes"] for p in phases)
    scale = sum(durations) / total_src
    remaining = [max(3.0, p["minutes"] * scale) for p in phases]
    # normalise to exact total
    f = sum(durations) / sum(remaining)
    remaining = [r * f for r in remaining]
    out = []
    i = 0
    for dur in durations:
        need = dur
        parts = []
        while need > 1e-6 and i < len(phases):
            take = min(remaining[i], need)
            parts.append((i, take, take < remaining[i] - 1e-6))
            remaining[i] -= take
            need -= take
            if remaining[i] <= 1e-6:
                i += 1
        out.append(parts)
    return out


def integerise(parts, dur):
    mins = [max(3, round(m)) for _, m, _ in parts]
    diff = sum(mins) - dur
    order = sorted(range(len(mins)), key=lambda k: -mins[k])
    k = 0
    while diff != 0:
        j = order[k % len(mins)]
        if diff > 0 and mins[j] > 3:
            mins[j] -= 1; diff -= 1
        elif diff < 0:
            mins[j] += 1; diff += 1
        k += 1
    return mins


def _first_clause(text, limit=110):
    """First sentence of a band's activity, trimmed — used verbatim in tier-0 seam notes."""
    t = str(text or "").strip()
    for stop in (". ", "? ", "! "):
        i = t.find(stop)
        if 0 < i < limit:
            return t[: i + 1]
    return (t[:limit].rsplit(" ", 1)[0] + "…") if len(t) > limit else t


def uniq(seq):
    out = []
    for x in seq:
        if x and x not in out:
            out.append(x)
    return out


def _tier0_title(units_map, src_units, opens_mid):
    parts = []
    for k, u in enumerate(src_units):
        t = units_map[u]["activity_title"]
        if k == 0 and opens_mid:
            t += " \u2014 continued"
        parts.append(t)
    return parts[0] if len(parts) == 1 else ", then ".join(parts)



# ── compression doctrine (2026-07-23): stretch uncapped · rescale to 0.8 ·
#    role-weighted compression 0.6-0.8 (dev pacing floor 0.8; hooks/consolidations
#    absorb, evenly across units; deep consolidations demote to homework) ·
#    below 0.6 drop trailing units, Rule-4-style coverage note ──
RESCALE_FLOOR = 0.8
COVERAGE_FLOOR = 0.6
DEV_PACE_FLOOR = 0.8
BAND_MIN = 3.0
DEMOTE_BELOW = 0.35  # hc scale under which trailing consolidations demote


def plan_compression(stream, target):
    phases = stream["phases"]
    units = stream["units"]
    total = sum(p["minutes"] for p in phases)
    ratio = target / total

    dropped_units = []
    kept_units = list(units)
    kept = list(phases)
    if ratio < COVERAGE_FLOOR:
        while len(kept_units) > 1:
            rem = sum(p["minutes"] for p in kept)
            if target / rem >= COVERAGE_FLOOR:
                break
            u = kept_units.pop()          # drop trailing unit (Rule 4 order)
            dropped_units.append(u["unit"])
            kept = [p for p in kept if p["unit"] != u["unit"]]
    rem_total = sum(p["minutes"] for p in kept)
    r2 = target / rem_total

    demoted = []
    if r2 >= RESCALE_FLOOR:
        regime = "stretch" if r2 > 1.0 else "rescale"
        eff = {p["phase_id"]: p["minutes"] * r2 for p in kept}
        hc_scale = dev_scale = round(r2, 3)
    else:
        regime = "role-weighted"
        def hc(p): return p["role"] in ("hook", "consolidation")
        while True:
            dev_total = sum(p["minutes"] for p in kept if not hc(p))
            hc_total = sum(p["minutes"] for p in kept if hc(p))
            hc_scale = (target - DEV_PACE_FLOOR * dev_total) / hc_total if hc_total else 1.0
            cons = [p for p in kept if p["role"] == "consolidation"]
            if hc_scale >= DEMOTE_BELOW or not cons:
                break
            worst = cons[-1]              # deepest squeeze: demote trailing consolidation
            demoted.append(worst)
            kept = [p for p in kept if p["phase_id"] != worst["phase_id"]]
        eff = {}
        for p in kept:
            e = p["minutes"] * (DEV_PACE_FLOOR if not hc(p) else hc_scale)
            eff[p["phase_id"]] = max(BAND_MIN, e)
        f = target / sum(eff.values())    # exact-fit normalization
        eff = {k: v * f for k, v in eff.items()}
        dev_scale = round(DEV_PACE_FLOOR * f, 3); hc_scale = round(max(hc_scale, 0) * f, 3)

    info = {"ratio": round(ratio, 3), "regime": regime,
            "dev_scale": dev_scale, "hc_scale": hc_scale,
            "demoted_to_homework": [p["phase_id"] for p in demoted],
            "dropped_units": dropped_units}
    return kept, eff, demoted, dropped_units, info


def build_plan(stream, matrix):
    durations = [d for d, c in matrix for _ in range(c)]
    kept, eff, demoted, dropped_units, cinfo = plan_compression(stream, sum(durations))
    phases = [dict(p, minutes=eff[p["phase_id"]]) for p in kept]
    units = {u["unit"]: u for u in stream["units"] if u["unit"] not in dropped_units}

    ranges = None
    tol_used = None
    for tol in (0.18, 0.25, 0.33):
        ranges = choose_cuts(phases, durations, tol)
        if ranges is not None:
            tol_used = tol
            break
    if ranges is not None:
        period_parts = [[(i, phases[i]["minutes"], False) for i in range(a, b)] for a, b in ranges]
        # rescale each period to exact duration below
        split_used = False
    else:
        period_parts = split_fallback(phases, durations)
        split_used = True

    new_periods = []
    phase_to_period = {}
    seams = []
    for n, (parts, dur) in enumerate(zip(period_parts, durations), 1):
        mins = integerise(parts, dur)
        cur = 0
        bands = []
        for (idx, _, is_partial), m in zip(parts, mins):
            ph = phases[idx]
            frag = phase_to_period.get(ph["phase_id"]) is not None
            text = ("[Continued] " if frag else "") + ph["activity"]
            bands.append({"band_id": ph["phase_id"], "minutes": f"{cur}-{cur+m}",
                          "activity": text, "role": ph["role"]})
            phase_to_period[ph["phase_id"]] = n  # last period touching this phase
            cur += m
        src_units = uniq([phases[idx]["unit"] for idx, _, _ in parts])
        prev_unit_open = phases[parts[0][0]]["unit"]
        opens_mid = parts[0][0] > 0 and phases[parts[0][0] - 1]["unit"] == prev_unit_open
        seam = None
        if opens_mid:
            prev_act = phases[parts[0][0] - 1]["activity"]
            seam = ("This period continues the unit begun last time, which closed with: "
                    f"\u201c{_first_clause(prev_act)}\u201d Briefly revisit that before resuming.")
            seams.append(n)
        contrib = {}
        for (idx, _, _), m in zip(parts, mins):
            contrib[phases[idx]["unit"]] = contrib.get(phases[idx]["unit"], 0) + m
        primary = max(contrib, key=contrib.get)
        srcs = [units[u] for u in src_units]
        notes = [s["teacher_notes"] for s in srcs if s["teacher_notes"]]
        teacher_notes = "\n\n[Next unit] ".join(notes)
        if seam:
            teacher_notes = seam + "\n\n" + teacher_notes
        new_periods.append({
            "period_number": n,
            "period_duration_minutes": dur,
            "activity_title": _tier0_title(units, src_units, opens_mid),
            "section_anchor": " / ".join(uniq([s["section_anchor"] for s in srcs])),
            "materials": uniq([m for s in srcs for m in s["materials"]]),
            "visual_aids": "; ".join(uniq([s["visual_aids"] for s in srcs
                                           if isinstance(s.get("visual_aids"), str)])) or None,
            "time_bands": bands,
            "section_context": " / ".join(uniq([s["section_context"] for s in srcs])),
            "pedagogical_approaches": uniq([a for s in srcs for a in s["pedagogical_approaches"]]),
            "teacher_notes": teacher_notes,
            "homework": [],
            "competency_edges": [e for s in srcs for e in s["competency_edges"]
                                 if units[primary] is s or True][:0],  # filled below
        })
    # competency edges: each unit's edges live on the period holding the unit's LAST phase
    for u in stream["units"]:
        if u["unit"] in dropped_units:
            continue
        last_p = max(phase_to_period[pid] for pid in u["phase_ids"] if pid in phase_to_period)
        tgt = new_periods[last_p - 1]
        tgt["competency_edges"].extend(u["competency_edges"])
        if u["homework"]:
            tgt["homework"] = (tgt["homework"] or []) + u["homework"]

    # derived anchors
    items = []
    for it in stream["assessment_items"]:
        it2 = json.loads(json.dumps(it))
        refs = it2.get("phase_ref") or []
        live = [phase_to_period[r] for r in refs if r in phase_to_period]
        if refs and not live:
            it2["period_ref"] = []
            it2["scheduling_note"] = "anchor unit not scheduled in this plan (time budget)"
        else:
            it2["period_ref"] = [max(live)] if live else it2.get("period_ref")
        items.append(it2)
    handoff = json.loads(json.dumps(stream["coverage_handoff"]))
    unit_last_period = {u["unit"]: max(phase_to_period[pid] for pid in u["phase_ids"] if pid in phase_to_period)
                        for u in stream["units"] if u["unit"] not in dropped_units}
    for c in handoff.values():
        kept_los = [lo for lo in c.get("los", []) if int(lo.get("period_number", -1)) in unit_last_period]
        for lo in kept_los:
            lo["period_number"] = unit_last_period[int(lo["period_number"])]
        c["los"] = kept_los

    total = sum(d * c for d, c in matrix)
    nper = sum(c for _, c in matrix)
    rows = "\n".join(f"  Row {i+1}: {d} minutes × {c} periods = {d*c} minutes"
                     for i, (d, c) in enumerate(matrix))
    coverage_note = ""
    if dropped_units:
        names = [u["section_anchor"] for u in stream["units"] if u["unit"] in dropped_units]
        coverage_note = ("Time budget below this chapter's coverage floor: the following "
                         "sections could not be scheduled — " + "; ".join(names))
    plan = {
        "filename": None,
        "saved_at": None,
        "grade": stream["meta"]["grade"],
        "subject": stream["meta"]["subject"],
        "chapter_number": stream["meta"]["chapter_number"],
        "chapter_title": stream["meta"]["chapter_title"],
        "period_schedule_display": f"Period schedule:\n{rows}\nTotal: {nper} periods · {total//60}h {total%60:02d}min",
        "period_rows_snapshot": [{"id": i, "duration": d, "count": c}
                                 for i, (d, c) in enumerate(matrix)],
        "plan_status": "adapted",
        "result": {
            "lesson_plan": {"periods": new_periods},
            "coverage_handoff": handoff,
            "assessment_items": items,
            "section_coverage_note": coverage_note or None,
        },
        "genon": {
            "engine": "partition v0.3 (deterministic, role-aware, 3-regime compression)",
            "compression": cinfo,
            "stream_source": stream["meta"].get("source_file"),
            "matrix": [{"duration": d, "count": c} for d, c in matrix],
            "seam_periods_tier0_polished": seams,
            "seam_llm_pass_available": True,
            "split_fallback_used": split_used,
            "fill_tolerance_used": tol_used,
        },
    }

    # validation
    probs = []
    for p in plan["result"]["lesson_plan"]["periods"]:
        cur = 0
        for b in p["time_bands"]:
            a, z = (int(x) for x in b["minutes"].split("-"))
            if a != cur: probs.append(f"P{p['period_number']} gap at {b['minutes']}")
            cur = z
        if cur != p["period_duration_minutes"]:
            probs.append(f"P{p['period_number']} sums {cur} != {p['period_duration_minutes']}")
    consumed = [b["band_id"] for p in new_periods for b in p["time_bands"]]
    expected = [ph["phase_id"] for ph in phases]  # phases already = kept, post-compression
    if uniq(consumed) != expected:
        probs.append("phase order/coverage violated")
    if probs:
        raise SystemExit("PARTITION INVALID:\n  " + "\n  ".join(probs))
    return plan


if __name__ == "__main__":
    stream = json.load(open(sys.argv[1]))
    matrix = parse_matrix(sys.argv[2])
    plan = build_plan(stream, matrix)
    json.dump(plan, open(sys.argv[3], "w"), ensure_ascii=False, indent=2)
    ps = plan["result"]["lesson_plan"]["periods"]
    g = plan["genon"]
    print(f"OK  {sys.argv[2]}: {len(ps)} periods | regime {g['compression']['regime']} "
          f"(ratio {g['compression']['ratio']}, dev x{g['compression']['dev_scale']}, "
          f"hc x{g['compression']['hc_scale']}) | demoted {len(g['compression']['demoted_to_homework'])} "
          f"| dropped units {g['compression']['dropped_units']} | seams {g['seam_periods_tier0_polished']}"
          f"{' (split fallback)' if g['split_fallback_used'] else ' (whole-phase cuts)'}")
