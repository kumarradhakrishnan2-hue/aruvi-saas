"""Aruvi partition engine — ported VERBATIM from the genon lab (partition.py v0.3).

Deterministic: phase stream + duration matrix -> full renderer-compatible saved
plan. No LLM. Role-aware boundary choice via DP; three-regime compression
doctrine (stretch / rescale / role-weighted / unit-drop below the 0.6 floor).
Seam notes are formulaic navigation text (tier-0); tier-1 LLM polish is a
separate, optional pass (polish.py). Only the CLI wrapper was dropped and
SystemExit became PartitionError; every algorithmic line is the lab's.
"""
from __future__ import annotations

import json


class PartitionError(RuntimeError):
    """The partition failed validation — never serve an invalid plan."""


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


def uniq(seq):
    out = []
    for x in seq:
        if x and x not in out:
            out.append(x)
    return out


# ── container text: SELECTED, never composed (LP v1.3 Rule 16, 2026-07-28) ──
#
# A period is always a CONTIGUOUS run of units — the DP cuts a linear phase stream, so
# non-contiguity is structurally impossible. Every period therefore falls into one of
# three cases, and the canonical's N-1 adjacent-pair table covers all of them:
#
#   1 unit    -> the unit's own authored title and notes, untouched.
#   2 units   -> the (a,b) entry: written for exactly this joint.
#   3+ units  -> the LAST adjacent pair in the span. In a three-unit period the middle
#                unit is present in full while the opening unit contributes only its
#                tail, so (b,c) names where the substance is; (a,b) would name a fragment.
#
# The entry is deliberately CUT-INVARIANT: it does not know how much of either unit this
# period holds, and must not pretend to (Rule 16 prohibition 2). Orientation is carried
# by naming the content the sitting pivots on, which stays true at every cut — the
# doctrine LP v1.2.1 settled for authored notes, applied here to container text.
#
# What this replaced: a mechanical "A — continued, then B" title; a seam clause reading
# "This period continues the unit begun last time, which closed with: <quoted band
# fragment>" (period language plus a calendar word — both forbidden by the very
# constitution this engine enforces on the model, and the quote truncated on any
# abbreviation, "Display Fig."); and a "[Next unit]" note concatenation. All three then
# had to be repaired by an LLM at request time, at cost, latency, and risk of failure.
# The fallbacks below fire ONLY for a canonical predating Rule 16, and every miss is
# recorded in genon.handoff_missing so a degraded plan is never mistaken for a good one.


def select_container_text(unit_handoff, units_map, src_units):
    """Title + teacher notes for one period. Returns (title, notes, key, hit).

    key is the handoff entry consulted, or None for the single-unit case (which needs
    no handoff). hit is False when a key was needed but the table did not supply it.
    """
    if len(src_units) == 1:
        u = units_map[src_units[0]]
        return u["activity_title"], u["teacher_notes"], None, True
    a, b = src_units[-2], src_units[-1]      # last adjacent pair — see note above
    entry = (unit_handoff or {}).get("%d-%d" % (a, b)) or {}
    title = (entry.get("title") or "").strip()
    notes = (entry.get("teacher_notes") or "").strip()
    key = "%d-%d" % (a, b)
    if title and notes:
        return title, notes, key, True
    srcs = [units_map[u] for u in src_units]
    return (title or " / ".join(units_map[u]["activity_title"] for u in src_units),
            notes or "\n\n".join(s["teacher_notes"] for s in srcs if s["teacher_notes"]),
            key, False)

# Rule 16 (LP v1.3): what the table must contain. Lives beside the selector that
# consumes it so the two halves of the contract cannot drift. Called by the
# generator's certification gate —
# a canonical without it forces the partitioner onto its degraded join fallback, and a
# title that is merely the two source titles spliced is the exact failure the rule exists
# to prevent, so both are caught here rather than discovered in a teacher's plan.
HANDOFF_JOINERS = (" and ", " & ", ", then ", " into ", " plus ", " with ", " / ", " — ", " -- ")


def validate_unit_handoff(uh, n_units: int) -> list[str]:
    if not uh:
        return ["unit_handoff missing (Rule 16)"]
    problems = []
    want = [f"{i}-{i+1}" for i in range(1, n_units)]
    missing = [k for k in want if k not in uh]
    if missing:
        problems.append(f"unit_handoff missing {len(missing)} pair(s): {missing[:5]}")
    extra = [k for k in uh if k not in want]
    if extra:
        problems.append(f"unit_handoff has non-adjacent/unknown pairs: {extra[:5]}")
    if list(uh) != [k for k in want if k in uh]:
        problems.append("unit_handoff entries out of plan order")
    for k in want:
        e = uh.get(k) or {}
        title, note = (e.get("title") or "").strip(), (e.get("teacher_notes") or "").strip()
        if not title:
            problems.append(f"unit_handoff {k}: missing title")
        elif any(j in f" {title} " for j in HANDOFF_JOINERS):
            problems.append(f"unit_handoff {k}: title uses a banned joiner — {title!r}")
        if not note:
            problems.append(f"unit_handoff {k}: missing teacher_notes")
        elif len(note.split()) > 99:            # 90-word budget + 10% grace
            problems.append(f"unit_handoff {k}: teacher_notes {len(note.split())} words > 90")
    return problems




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
    unit_handoff = stream.get("unit_handoff") or {}

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
    mid_unit_openings = []          # periods that open inside a unit — reporting only
    handoff_used, handoff_missing = [], []
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
        # opens_mid is now REPORTING ONLY — the container text no longer varies with it.
        # It stays because it is the honest measure of how hard a matrix cuts the chapter.
        if parts[0][0] > 0 and phases[parts[0][0] - 1]["unit"] == phases[parts[0][0]]["unit"]:
            mid_unit_openings.append(n)
        contrib = {}
        for (idx, _, _), m in zip(parts, mins):
            contrib[phases[idx]["unit"]] = contrib.get(phases[idx]["unit"], 0) + m
        primary = max(contrib, key=contrib.get)
        srcs = [units[u] for u in src_units]
        title, teacher_notes, hkey, hit = select_container_text(unit_handoff, units, src_units)
        if hkey is not None:
            (handoff_used if hit else handoff_missing).append(hkey)
        new_periods.append({
            "period_number": n,
            "period_duration_minutes": dur,
            "activity_title": title,
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
            "mid_unit_openings": mid_unit_openings,
            "handoff_used": handoff_used,
            "handoff_missing": handoff_missing,
            "container_text": ("selected from unit_handoff (LP v1.3 Rule 16)"
                               if not handoff_missing else
                               "PARTIAL — %d period(s) fell back to a mechanical join; "
                               "this canonical predates Rule 16" % len(handoff_missing)),
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
        raise PartitionError("PARTITION INVALID:\n  " + "\n  ".join(probs))
    return plan

