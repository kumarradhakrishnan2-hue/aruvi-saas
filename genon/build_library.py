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

KLASS = {"iii": "III", "iv": "IV", "v": "V", "vi": "VI", "vii": "VII",
         "viii": "VIII", "ix": "IX", "x": "X"}


def run(label, argv):
    print(f"\n== {label} ==")
    r = subprocess.run([sys.executable] + argv, cwd=REPO)
    if r.returncode != 0:
        raise SystemExit(f"STOP: {label} failed (exit {r.returncode}); "
                         "fix and re-run — completed steps are idempotent.")


def load_library(subject, grade, ch, lines, fails):
    lib_dir = REPO / "data" / "content" / "saved_plans" / subject / grade
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

    if not certify_only:
        run("STEP 1 · top canonical (metered, Sonnet 4.6)",
            [gen, "one", subject, grade, str(ch)])
    run("STEP 2 · annotate master plan", [vpn])

    briefs, vp = vp_mod.briefs_for(subject, klass, ch)
    bdir = HERE / "out" / "briefs"
    bdir.mkdir(parents=True, exist_ok=True)
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
