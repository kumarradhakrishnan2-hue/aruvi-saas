#!/usr/bin/env python3
"""build_library.py — ONE Terminal command builds a chapter's whole variant library.

    python3 genon/build_library.py social_sciences ix 3

Why Terminal: the Cowork sandbox proxy blocks credentialed API calls in every mode
(proven 2026-08-01 — an x-api-key request never leaves the sandbox), so the metered
Sonnet-4.6 generations must run here, where runtime_data/anthropic.key works.
Everything deterministic runs here too, so the whole mechanical pipeline is one
command; the Cowork session's job is what remains — reading the certification
report at the human gate.

Steps (stops on the first failure; each is idempotent to re-run):
  1. top canonical (LP + assessment)          — generate_canonical.py, metered
  2. annotate master_plan.json                — variant_plans.py (row finalizes)
  3. variant briefs                            — written to genon/out/briefs/
  4. each compact variant (LP + assessment)    — generate_canonical.py --variant, metered
  5. re-annotate + DETERMINISTIC CERTIFICATION — compile, registry/first-visit/closing
     checks, serve sweep, projected-vs-actual diff
  6. report                                    — genon/out/library_reports/ch_NN_<ts>.md
     (the Cowork session presents this at the Step 6 human gate; approval is the
     founder's, never this script's)

    --certify-only   skip generations; run steps 2-6 on whatever library exists
"""
from __future__ import annotations

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent            # genon/
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

from aruvi_core.genon import compile_stream, serve_plan            # noqa: E402
from aruvi_core.genon.serve import (                               # noqa: E402
    _norm, section_registry, unit_range,
)
import variant_plans as vp_mod                                     # noqa: E402
from register_scan import scan_plan, scanned_fields                # noqa: E402

from aruvi_core.grades import stage_for                            # noqa: E402

KLASS = {"iii": "III", "iv": "IV", "v": "V", "vi": "VI", "vii": "VII",
         "viii": "VIII", "ix": "IX", "x": "X"}

# ── EXACT ITEM COUNTS PER COMPETENCY WEIGHT (2026-08-02) ─────────────────────────
# Added at SS·secondary C4 / ARV-D-019: the p07 variant shipped 17 items where its
# own constitution mandates 18 (a Substantive competency lost its third slot), and
# the eight structural checks could not see it — the miss surfaced only because a
# Cowork session counted by hand, which will not happen across 926 authoring runs.
#
# ADVISORY, NOT A GATE (founder ruling the same day): slot misses are generation
# variance, priced below a ~Rs 37 regeneration, and ch 3's p07 is accepted as
# authored. So this reports and never sets ok=False — the point is to turn a silent
# miss into a visible rate. Promote it to a gate by passing the flag through note()
# instead of lines.append(), once the founder prices the rate.
#
# One row per subject·stage, filled from that stage's assessment constitution as it
# is amended at its own P2. A stage with no row falls back to the library's own
# modal count per weight label, which still catches a variant disagreeing with its
# siblings (exactly the p07 shape) without knowing any constitution.
EXACT_ITEM_COUNTS = {
    # SS·secondary assessment v1.6 Rule 4 — Central 1 MCQ + 1 SCR + 1 SOURCE_INTERPRETATION
    # + 1 ECR + 1 Open Task · Substantive 1 MCQ + 1 SCR + 1 (SI or ECR) · Present 1 MCQ + 1 SCR.
    ("social_sciences", "secondary"): {"Central": 5, "Substantive": 3, "Present": 2},
}


def run(label, argv):
    print(f"\n== {label} ==")
    r = subprocess.run([sys.executable] + argv, cwd=REPO)
    if r.returncode != 0:
        raise SystemExit(f"STOP: {label} failed (exit {r.returncode}); "
                         "fix and re-run — completed steps are idempotent.")


def lib_dir_of(subject, grade):
    return REPO / "data" / "content" / "saved_plans" / subject / grade


def item_census(raw):
    """{c_code: (weight_label, n_items)} from a saved plan's assessment_items,
    plus the set of non-Incidental competencies its handoff says must be assessed.
    Weight-label spelling is the constitution's own (Central/Substantive/Present);
    a competency the handoff carries but the assessment never touches comes back
    with n = 0, which is the loudest version of the same defect."""
    r = raw.get("result", raw)
    census, order = {}, []
    for it in r.get("assessment_items") or []:
        code = ((it.get("competency") or {}).get("c_code") or "").strip()
        if not code:
            continue
        if code not in census:
            census[code] = [str(it.get("weight_label") or "").strip(), 0]
            order.append(code)
        census[code][1] += 1
    handoff = r.get("coverage_handoff")
    if isinstance(handoff, dict):
        for code, v in handoff.items():
            if not isinstance(v, dict):
                continue
            if str(v.get("weight", "")).strip() in ("0", "Incidental", "incidental"):
                continue
            if code not in census:
                census[code] = ["(from handoff)", 0]
                order.append(code)
    return [(c, census[c][0], census[c][1]) for c in order]


def load_library(subject, grade, ch, lines, fails):
    lib_dir = lib_dir_of(subject, grade)
    paths = [lib_dir / f"ch_{ch:02d}_canonical.json"]
    paths += sorted(lib_dir.glob(f"ch_{ch:02d}_canonical_p*.json"))
    streams = []
    for p in paths:
        if not p.is_file():
            continue
        try:
            streams.append((p.name, compile_stream(json.loads(p.read_text()))))
        except Exception as e:                     # noqa: BLE001
            lines.append(f"FAIL  {p.name}: does not compile — {e}")
            fails.add(p.name)
    streams.sort(key=lambda t: -len(t[1]["units"]))
    return streams


def certify(subject, grade, ch, row):
    lines = []
    fails = set()                       # file names with STRUCTURAL failures →
    ok = True                           # quarantined (founder doctrine 2026-08-01:
                                        # good files stay live; only failed ones move)

    def note(flag, msg, fname=None):
        nonlocal ok
        ok = ok and flag
        lines.append(("PASS  " if flag else "FAIL  ") + msg)
        if not flag and fname:
            fails.add(fname)

    lib = load_library(subject, grade, ch, lines, fails)
    if not lib:
        raise SystemExit("STOP: no library on disk to certify.")
    top_name, top = lib[0]
    reg = section_registry(top)
    ridx = {_norm(a): i for i, a in enumerate(reg)}
    vp = row["variant_plan"]

    note(len(lib) == len(vp["counts"]),
         f"library complete: {[n for n, _ in lib]} vs plan {vp['counts']}")
    for name, s in lib:
        rr = [unit_range(u, ridx) for u in s["units"]]
        note(all(r is not None for r in rr),
             f"{name}: every anchor verbatim in the top registry", name)
        okorder, seen_hi = True, -1
        for r in rr:
            if r is None:
                okorder = False
                continue
            if r[1] > seen_hi:                    # this unit advances the frontier
                if r[0] > seen_hi + 1:            # …but skipped a section
                    okorder = False
                seen_hi = r[1]
        note(okorder, f"{name}: first-visit order follows the registry", name)
        note(seen_hi == len(reg) - 1,
             f"{name}: coverage reaches the final registry section", name)
        k = len(s["units"])
        if str(k) in vp["closing_spans"]:
            span = vp["closing_spans"][str(k)]
            want = {_norm(a) for a in reg[-span:]}
            got = {_norm(a) for a in
                   str(s["units"][-1]["section_anchor"]).split(" / ")}
            note(got == want,
                 f"{name}: closing unit anchors exactly its mandated last-{span} span",
                 name)

    # ── REGISTER GATE (2026-08-02) ────────────────────────────────────────────────
    # The register is stated as a prohibition in every constitution and the ch 3 pilot
    # proved a prohibition is not enforcement (testing.md C3: 9 breaches under v1.10,
    # which bans them in terms). Detection lives here, in code, where it is not a matter
    # of the model's attention. genon/repair_register.py is the intended response.
    #
    # A register hit FAILS certification but does NOT quarantine (founder call, 2026-08-02):
    # quarantine exists for files whose STRUCTURE breaks serving. A register breach makes
    # serving WRONG, not impossible, and the file is repairable in place — pulling it out of
    # the library would lose a good plan over a clause.
    for name, s_ in lib:
        raw = json.loads((lib_dir_of(subject, grade) / name).read_text())
        bans = [h for h in scan_plan(raw) if h["ban"]]
        seen = scanned_fields(raw)
        # A plan whose band array we cannot read would report "clean" having been SKIPPED.
        # The scanner knows time_bands[] and phases[] (with activity/description); anything
        # else is a new shape and must fail loudly rather than pass silently.
        bands_read = seen.get("time_bands", 0) + seen.get("phases", 0)
        note(bands_read > 0,
             f"{name}: register scan reached the band text ({bands_read} band(s) read: "
             f"{ {k: v for k, v in seen.items()} })", name)
        note(not bans, f"{name}: register clean ({len(bans)} ban hit(s))")
        for h in bans[:8]:
            lines.append(f"      U{h['unit']} {h['field']} [{h['family']}] {h['excerpt']}")
        if bans:
            lines.append("      -> declare the fixes in genon/repair_register.py and re-run "
                         "--certify-only; do NOT hand-edit the artefact")

    # ── ASSESSMENT ITEM COUNTS — ADVISORY (2026-08-02, testing.md C4 / ARV-D-019) ──
    # See EXACT_ITEM_COUNTS above for why this reports rather than gates.
    censuses = {name: item_census(json.loads((lib_dir_of(subject, grade) / name).read_text()))
                for name, _ in lib}
    table = EXACT_ITEM_COUNTS.get((subject, stage_for(grade)))
    basis = "constitution"
    if not table:                       # no row for this stage yet — derive from the library
        seen = {}
        for cen in censuses.values():
            for _c, w, n in cen:
                seen.setdefault(w, []).append(n)
        table = {w: max(set(ns), key=ns.count) for w, ns in seen.items() if w}
        basis = "derived (modal count across this library — no constitution row yet)"
    says = "constitution says" if basis == "constitution" else "its siblings carry"
    short = 0
    lines.append("")
    lines.append(f"item counts per competency — ADVISORY, does not gate; basis: {basis}")
    lines.append(f"      expected {json.dumps(table, sort_keys=True)}")
    for name, cen in censuses.items():
        got = sum(n for _c, _w, n in cen)
        want = sum(table.get(w, n) for _c, w, n in cen)
        misses = [(c, w, n, table[w]) for c, w, n in cen
                  if w in table and n != table[w]]
        short += len(misses)
        lines.append(f"      {name}: {got} items vs {want} expected"
                     + ("" if not misses else "  <-- MISS"))
        for c, w, n, exp in misses:
            lines.append(f"          {c} ({w}) has {n}, {says} {exp}")
    if short:
        lines.append(f"      -> {short} competenc(ies) off the mandated count. Generation "
                     "variance, accepted by default (ARV-D-019); a hand back-fill is "
                     "forbidden (testing.md §7) — the only fix is regeneration, and that "
                     "is a founder call on cost, not a certification failure.")

    # serve sweep + projected-vs-actual
    floor = row["floor_periods_at_standard"]
    top_n = len(top["units"])
    dur = top["units"][0]["authored_duration_minutes"]
    streams = [s for _, s in lib]
    sweep = {}
    for x in range(max(1, floor - 2), top_n + 3):
        try:
            p = serve_plan(streams, [(dur, x)])
            g = p["genon"]
            fill = g["slot_fill"]
            mode = ("surrender" if g["surrendered_periods"]
                    else "identity" if not fill else fill["mode"])
            sweep[x] = mode
        except Exception as e:                     # noqa: BLE001
            sweep[x] = f"ERROR: {e}"
            note(False, f"serve X={x} raised: {e}")
    full_modes = {"identity", "exact", "superset", "synthesis", "surrender"}
    projected = vp.get("full_coverage") or [None, None]
    for x, mode in sweep.items():
        if projected[0] is not None and projected[0] <= x <= (projected[1] or 0):
            note(mode in full_modes,
                 f"X={x}: projected full, served '{mode}'")
    lines.append("")
    lines.append("serve sweep: " + json.dumps(sweep))
    return ok, lines, sweep, fails


def quarantine(subject, grade, ch, fails, lines):
    """Founder doctrine (2026-08-01): PASSING files stay live; a file with a
    structural failure is MOVED out of the served library into quarantine —
    backup/quarantine/<subject>/<grade>/ — which doubles as the fix worklist.
    If the TOP canonical fails, the whole library goes with it (the variants'
    registry has no ground without it)."""
    lib_dir = REPO / "data" / "content" / "saved_plans" / subject / grade
    qdir = REPO / "backup" / "quarantine" / subject / grade
    top_name = f"ch_{ch:02d}_canonical.json"
    to_move = set(fails)
    if top_name in to_move:
        to_move |= {p.name for p in lib_dir.glob(f"ch_{ch:02d}_canonical_p*.json")}
        lines.append("NOTE  top canonical failed — the entire library is quarantined "
                     "with it (variants have no registry ground without the top)")
    qdir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    for name in sorted(to_move):
        src = lib_dir / name
        if src.is_file():
            dest = qdir / f"{name[:-5]}_{ts}.json"
            src.replace(dest)
            lines.append(f"QUARANTINED  {name} -> {dest.relative_to(REPO)}")
    return sorted(to_move)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    certify_only = "--certify-only" in sys.argv
    if len(args) != 3:
        raise SystemExit(__doc__)
    subject, grade, ch = args[0], args[1].lower(), int(args[2])
    klass = KLASS[grade]
    gen = str(HERE / "generate_canonical.py")
    vpn = str(HERE / "variant_plans.py")

    bdir = HERE / "out" / "briefs"
    bdir.mkdir(parents=True, exist_ok=True)
    # The TOP canonical gets a brief too (2026-08-02). It used to be the only artefact
    # generated without one — and the only one that breached the register nine times.
    top_bf = bdir / f"ch_{ch:02d}_top.txt"
    top_bf.write_text(vp_mod.top_brief_for(subject, klass, ch), encoding="utf-8")
    print(f"brief written: {top_bf}")

    if not certify_only:
        run("STEP 1 · top canonical (metered, Sonnet 4.6)",
            [gen, "one", subject, grade, str(ch), "--brief", str(top_bf)])
    run("STEP 2 · annotate master plan", [vpn])

    briefs, vp = vp_mod.briefs_for(subject, klass, ch)
    bfiles = {}
    for k, text in briefs.items():
        bf = bdir / f"ch_{ch:02d}_p{k:02d}.txt"
        bf.write_text(text, encoding="utf-8")
        bfiles[k] = bf
        print(f"brief written: {bf}")

    if not certify_only:
        for k, bf in bfiles.items():
            run(f"STEP 4 · {k}-period variant (metered, Sonnet 4.6)",
                [gen, "one", subject, grade, str(ch),
                 "--variant", str(k), "--brief", str(bf)])
        run("STEP 5 · re-annotate on the full library", [vpn])

    mp = json.loads((REPO / "data/content/allocation_norms/master_plan.json").read_text())
    row = next(c for c in mp["combos"][f"{subject}|{klass}"]["chapters"]
               if c["chapter"] == ch)
    ok, lines, sweep, fails = certify(subject, grade, ch, row)
    moved = quarantine(subject, grade, ch, fails, lines) if fails else []

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    rdir = HERE / "out" / "library_reports"
    rdir.mkdir(parents=True, exist_ok=True)
    report = rdir / f"{subject}_{grade}_ch{ch:02d}_{ts}.md"
    report.write_text(
        f"# Library certification · {subject} {klass} ch {ch} · {ts}\n\n"
        f"plan: counts {row['variant_plan']['counts']} · "
        f"spans {row['variant_plan']['closing_spans']} · "
        f"sigma {row['variant_plan']['sigma']} · "
        f"basis {row['variant_plan']['basis']}\n\n"
        + "\n".join(lines)
        + "\n\nDETERMINISTIC CHECKS "
        + ("ALL PASS" if ok else "HAVE FAILURES — do not certify")
        + ((" Failed files are QUARANTINED under backup/quarantine/ (the fix "
            "worklist); regenerate them and re-run --certify-only.")
           if moved else "")
        + ".\nThe HUMAN GATE remains: read the borrowed seams and each closing "
          "synthesis in a Cowork session before calling this chapter certified.\n",
        encoding="utf-8")
    print(f"\n== report: {report.relative_to(REPO)} ==")
    print("deterministic checks:", "ALL PASS" if ok else "FAILURES — see report")
    for name in moved:
        print(f"QUARANTINED (not servable): {name}")
    print("Next: open a Cowork session and ask it to present this report "
          "for the human gate.")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
