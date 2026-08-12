#!/usr/bin/env python3
"""batch_api.py — author canonicals through the Message Batches API at HALF PRICE (v1.0, 2026-08-12).

    python3 genon/batch_api.py submit  the_world_around_us v iv iii --wave top
    python3 genon/batch_api.py status  <manifest.json>            # or --latest
    python3 genon/batch_api.py collect <manifest.json>
    python3 genon/batch_build.py the_world_around_us v iv iii --certify-only   # free steps
    python3 genon/batch_api.py submit  the_world_around_us v iv iii --wave compact
    ... status / collect / certify again

WHY THIS EXISTS. `batch_build.py` is a loop of ordinary synchronous calls: full price,
one at a time, ~8 hours for S5's 90 runs. The Message Batches API takes all the requests
as ONE asynchronous job, bills input and output at 50%, and runs them concurrently — most
batches finish inside an hour. Same model, same prompts, same artefacts; the only thing
that changes is how the request is delivered and what it costs.

TWO WAVES, AND WHY IT CANNOT BE ONE. A chapter's compact canonicals are authored against
the STANDARD's own section registry — `variant_plans.briefs_for` reads the standard off
disk and refuses when the row is still provisional. So the compacts of a chapter cannot be
written until that chapter's standard exists. The corpus therefore goes in two waves:
    wave 1  `--wave top`      31 standards          (TWAU: 31 requests)
    wave 2  `--wave compact`  their 59 compacts     (after wave 1 is collected + annotated)
Each wave is one batch. Anything else would be a guess at a brief that does not exist yet.

WHAT IS SHARED WITH THE SYNC PATH, deliberately: prompt assembly and post-processing are
`generate_canonical.prepare_job` / `finish_generation` — the same functions `cmd_one` calls,
extracted for this script. Parse-with-repair, the validator, the library install and both
logs are therefore identical by construction, not by inspection. The ONLY difference is
`price_mult=0.5` and `mode="batch"` in the ledger.

PROMPT CACHING is ON by default here (`--no-cache` to disable). Every request in a wave
shares the same stage constitution and pedagogy blocks, `prompt_assembly` already marks
them with a 1h TTL, and the batch docs recommend exactly this for a job of shared-context
requests. Cache reads bill at 0.1x and stack with the batch discount.

SAFETY. Nothing is paid for twice: `submit` skips any canonical already installed, exactly
as `build_library.py` does, and refuses to submit a wave whose manifest is already open.
`collect` is idempotent — a result already installed is skipped unless `--redo`. Results
stay retrievable for 29 days, so a collect can be re-run.
"""
from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(HERE))

import batch_build as bb                                          # noqa: E402  (worklist)
import generate_canonical as gc                                   # noqa: E402  (the two halves)
import prompt_assembly as pa                                      # noqa: E402
import variant_plans as vp                                        # noqa: E402
from aruvi_core.genon.carriers import (                           # noqa: E402
    CarrierNotImplemented, require_carrier,
)

VALUE_FLAGS = bb.VALUE_FLAGS + ("--wave", "--every")

BATCHES = HERE / "out" / "batches"
BRIEFS = HERE / "out" / "briefs"
MODEL = gc.GENERATION_MODEL if hasattr(gc, "GENERATION_MODEL") else "claude-sonnet-4-6"
# Batch pricing is exactly half of standard (docs: Batch processing → Pricing).
PRICE_MULT = 0.5


# ── custom_id ↔ job identity ────────────────────────────────────────────────────
# The API constrains custom_id to ^[a-zA-Z0-9_-]{1,64}$ and does NOT guarantee result
# order, so this string is the only link between an answer and the chapter that asked
# for it. Keep it decodable and keep it short: subject folders are long.
SUBJ_ABBR = {"the_world_around_us": "twau", "social_sciences": "ss", "science": "sci",
             "mathematics": "math", "english": "eng"}
ABBR_SUBJ = {v: k for k, v in SUBJ_ABBR.items()}


def make_cid(subject: str, grade: str, ch: int, variant: int | None) -> str:
    return f"{SUBJ_ABBR.get(subject, subject)}-{grade}-{ch:02d}-" + \
           (f"p{variant:02d}" if variant else "top")


def read_cid(cid: str) -> tuple[str, str, int, int | None]:
    abbr, grade, ch, kind = cid.split("-")
    return (ABBR_SUBJ.get(abbr, abbr), grade, int(ch),
            None if kind == "top" else int(kind[1:]))


def rel(p: Path) -> str:
    """Repo-relative when it can be — a manifest outside the tree must not crash a
    collect that has already installed its results."""
    try:
        return str(Path(p).relative_to(REPO))
    except ValueError:
        return str(p)


def client():
    import anthropic
    key = os.environ.get("ANTHROPIC_API_KEY")
    if not key:
        kf = REPO / "runtime_data" / "anthropic.key"
        if kf.is_file():
            key = kf.read_text(encoding="utf-8").strip()
    if not key:
        raise SystemExit("No API key: set ANTHROPIC_API_KEY or runtime_data/anthropic.key")
    return anthropic.Anthropic(api_key=key)


def installed_path(subject: str, grade: str, ch: int, variant: int | None) -> Path:
    lib = bb.bl.lib_dir_of(subject, grade)
    return lib / (f"ch_{ch:02d}_canonical_p{variant:02d}.json" if variant
                  else f"ch_{ch:02d}_canonical.json")


# ── submit ──────────────────────────────────────────────────────────────────────
def build_requests(subject: str, grades: list[str], only, wave: str, redo: bool):
    """[(custom_id, job, brief_path)] for the wave. Skips anything already installed."""
    work, skipped = bb.build_worklist(subject, grades, only)
    BRIEFS.mkdir(parents=True, exist_ok=True)
    out, notes = [], list(skipped)
    for w in work:
        grade, ch, counts = w["grade"], w["ch"], w["counts"]
        klass = bb.bl.KLASS[grade]
        if wave == "top":
            if not redo and installed_path(subject, grade, ch, None).is_file():
                notes.append((grade, ch, "standard already installed"))
                continue
            bf = BRIEFS / f"ch_{ch:02d}_top.txt"
            bf.write_text(vp.top_brief_for(subject, klass, ch), encoding="utf-8")
            job = gc.prepare_job(subject, grade, ch, brief=str(bf), quiet=True)
            if job is None:
                notes.append((grade, ch, "prepare_job refused"))
                continue
            out.append((make_cid(subject, grade, ch, None), job, bf))
        else:
            # A compact's brief needs the standard on disk and the row annotated. If the
            # standard is missing, this chapter simply is not ready for wave 2 — say so
            # rather than submitting a request whose brief would be a fiction.
            if not installed_path(subject, grade, ch, None).is_file():
                notes.append((grade, ch, "no standard on disk — wave 1 first"))
                continue
            try:
                briefs, _plan = vp.briefs_for(subject, klass, ch)
            except SystemExit as e:
                notes.append((grade, ch, f"briefs_for refused: {e}"))
                continue
            for k, text in briefs.items():
                if not redo and installed_path(subject, grade, ch, k).is_file():
                    notes.append((grade, ch, f"p{k:02d} already installed"))
                    continue
                bf = BRIEFS / f"ch_{ch:02d}_p{k:02d}.txt"
                bf.write_text(text, encoding="utf-8")
                job = gc.prepare_job(subject, grade, ch, variant=k, brief=str(bf), quiet=True)
                if job is None:
                    notes.append((grade, ch, f"p{k:02d} prepare_job refused"))
                    continue
                out.append((make_cid(subject, grade, ch, k), job, bf))
        _ = counts
    return out, notes


def cmd_submit(argv) -> int:
    args, flags, vals = bb.parse_argv(argv, VALUE_FLAGS)
    if len(args) < 2:
        raise SystemExit(__doc__)
    subject, grades = args[0], [g.lower() for g in args[1:]]
    wave = vals.get("--wave", "top")
    if wave not in ("top", "compact"):
        raise SystemExit("--wave must be 'top' or 'compact'")
    only = bb.parse_chapter_filter(vals["--chapters"]) if "--chapters" in vals else None
    dry = "--dry" in flags
    redo = "--redo" in flags
    if "--no-cache" not in flags:
        pa.USE_PROMPT_CACHE = True          # 1h TTL blocks; recommended for batches

    for g in grades:
        if g not in bb.bl.KLASS:
            raise SystemExit(f"unknown grade: {g}")
        try:
            require_carrier(subject, g)
        except CarrierNotImplemented as e:
            raise SystemExit(f"STOP before spending — {e}")

    reqs, notes = build_requests(subject, grades, only, wave, redo)
    print(f"\n=== BATCH SUBMIT · {subject} · {', '.join(grades)} · wave {wave} ===")
    for cid, job, _bf in reqs:
        print(f"  {cid}  {job['count']:>2} × {job['duration']} min  {job['title'][:36]}")
    for g, c, why in notes:
        print(f"  skip {g} ch {c} — {why}")
    est_in = sum(j["sys_chars"] + j["usr_chars"] for _c, j, _b in reqs) / 4
    print(f"\nrequests {len(reqs)} · ~{est_in/1000:.0f}k input tokens (uncached worst case) · "
          f"cache {'ON (1h)' if pa.USE_PROMPT_CACHE else 'OFF'} · price 50% of standard")
    if not reqs:
        print("Nothing to submit.")
        return 0
    if dry:
        BATCHES.mkdir(parents=True, exist_ok=True)
        p = BATCHES / f"DRY_{subject}_{wave}_{datetime.now():%Y%m%d_%H%M%S}.json"
        p.write_text(json.dumps(
            [{"custom_id": cid,
              "params": {"model": MODEL, "max_tokens": job["max_tokens"],
                         "system": job["system_blocks"],
                         "messages": [{"role": "user", "content": job["user_blocks"]}]}}
             for cid, job, _bf in reqs], ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"--dry: request payload written, nothing submitted → {rel(p)}")
        return 0

    requests = [{"custom_id": cid,
                 "params": {"model": MODEL, "max_tokens": job["max_tokens"],
                            "system": job["system_blocks"],
                            "messages": [{"role": "user", "content": job["user_blocks"]}]}}
                for cid, job, _bf in reqs]
    batch = client().messages.batches.create(requests=requests)
    BATCHES.mkdir(parents=True, exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    man = BATCHES / f"{subject}_{wave}_{stamp}.json"
    man.write_text(json.dumps({
        "batch_id": batch.id, "created_at": stamp, "subject": subject, "grades": grades,
        "wave": wave, "model": MODEL, "cache": bool(pa.USE_PROMPT_CACHE),
        "jobs": {cid: {"grade": j["grade_folder"], "chapter": j["ch"],
                       "variant": j["variant"], "count": j["count"],
                       "duration": j["duration"], "title": j["title"],
                       "brief": str(bf.relative_to(REPO))}
                 for cid, j, bf in reqs},
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nbatch {batch.id} submitted · {len(requests)} request(s)")
    print(f"manifest: {rel(man)}")
    print(f"next: python3 genon/batch_api.py status {rel(man)}")
    return 0


# ── status ──────────────────────────────────────────────────────────────────────
def latest_manifest() -> Path:
    """Newest by MTIME, not by name (2026-08-12). Sorting by filename made `--latest` pick
    wave 1's `..._top_...` over wave 2's `..._compact_...` — 'c' sorts before 't' — so the
    status of a fresh batch was read off the previous one, with a plausible-looking answer.
    A default that silently reads the wrong object is worse than no default."""
    mans = [m for m in BATCHES.glob("*.json")
            if not m.name.startswith("DRY_") and not m.name.endswith(".collected.json")]
    if not mans:
        raise SystemExit("no manifests in genon/out/batches/")
    return max(mans, key=lambda p: p.stat().st_mtime)


def cmd_status(argv) -> int:
    args, flags, vals = bb.parse_argv(argv, VALUE_FLAGS)
    man = Path(args[0]) if args else latest_manifest()
    if not man.is_absolute():
        man = REPO / man
    m = json.loads(man.read_text())
    watch = "--watch" in flags
    every = int(vals.get("--every", 60))
    while True:
        b = client().messages.batches.retrieve(m["batch_id"])
        c = b.request_counts
        print(f"{datetime.now():%H:%M:%S}  {b.processing_status}  "
              f"processing {c.processing} · succeeded {c.succeeded} · errored {c.errored} "
              f"· canceled {c.canceled} · expired {c.expired}")
        if b.processing_status == "ended":
            print(f"\nended. next: python3 genon/batch_api.py collect {rel(man)}")
            return 0
        if not watch:
            return 0
        time.sleep(every)


# ── collect ─────────────────────────────────────────────────────────────────────
def cmd_collect(argv) -> int:
    args, flags, vals = bb.parse_argv(argv, VALUE_FLAGS)
    man = Path(args[0]) if args else latest_manifest()
    if not man.is_absolute():
        man = REPO / man
    m = json.loads(man.read_text())
    redo = "--redo" in flags
    subject, jobs = m["subject"], m["jobs"]
    cl = client()
    b = cl.messages.batches.retrieve(m["batch_id"])
    if b.processing_status != "ended":
        raise SystemExit(f"batch {m['batch_id']} is {b.processing_status} — not ready. "
                         "Run `status --watch` first.")

    rows, spend = [], 0.0
    for result in cl.messages.batches.results(m["batch_id"]):
        cid = result.custom_id
        meta = jobs.get(cid)
        if meta is None:
            print(f"  ?? unknown custom_id in results: {cid}")
            continue
        subj, grade, ch, variant = read_cid(cid)
        kind = result.result.type
        if kind != "succeeded":
            err = getattr(getattr(result.result, "error", None), "type", kind)
            print(f"  {cid}: {kind.upper()} ({err}) — not billed; resubmit this one")
            rows.append((cid, kind, 0.0, str(err)))
            continue
        if not redo and installed_path(subject, grade, ch, variant).is_file():
            print(f"  {cid}: already installed — skipped (--redo to overwrite)")
            rows.append((cid, "skipped", 0.0, "already installed"))
            continue

        msg = result.result.message
        full = "".join(blk.text for blk in msg.content if getattr(blk, "type", "") == "text")
        u = msg.usage
        fresh = getattr(u, "input_tokens", 0) or 0
        c_write = getattr(u, "cache_creation_input_tokens", 0) or 0
        c_read = getattr(u, "cache_read_input_tokens", 0) or 0
        it = fresh + c_write + c_read                    # for the record: total input
        ot = getattr(u, "output_tokens", 0) or 0
        # PRICED INPUT, not counted input. With caching on, the three input classes bill
        # at different rates — a cache READ is 0.1x and a cache WRITE 1.25x — so summing
        # them and applying the base rate (what finish_generation does by default, and
        # what the sync path has always done because it never cached) would overstate the
        # bill by ~50% on a warm wave. The batch multiplier applies on top of all three.
        it_billed = fresh + 1.25 * c_write + 0.1 * c_read
        cost = (it_billed * gc.USD_PER_M_INPUT + ot * gc.USD_PER_M_OUTPUT) / 1e6 * \
            gc.INR_PER_USD * PRICE_MULT
        # Rebuild the job exactly as it was submitted, so validation knows the period
        # count and the install knows the variant. The brief is on disk from submit.
        job = gc.prepare_job(subject, grade, ch, variant=variant,
                             brief=str(REPO / meta["brief"]), quiet=True)
        if job is None:
            print(f"  {cid}: prepare_job refused at collect — result kept in the batch only")
            rows.append((cid, "refused", 0.0, "prepare_job"))
            continue
        print(f"\n  == {cid} · {job['title'][:40]} ==")
        ts = f"{m['created_at']}_{cid.replace('-', '_')}"
        if c_read or c_write:
            print(f"  cache    : {c_read:,} read (0.1x) · {c_write:,} written (1.25x) · "
                  f"{fresh:,} fresh")
        status, problems = gc.finish_generation(
            job, full, it, ot, 0.0, model=m["model"], ts=ts, mode="batch",
            cost_inr=cost)
        spend += cost
        rows.append((cid, status, round(cost, 2), "; ".join(problems)[:120]))

    print(f"\n=== COLLECTED {len(rows)} result(s) · ₹{spend:.2f} "
          f"(sync would have been ₹{spend*2:.2f}) ===")
    for cid, status, cost, note in rows:
        print(f"  {cid:<18} {status:<9} ₹{cost:<7} {note}")
    bad = [r for r in rows if r[1] not in ("ok", "skipped")]
    report = man.with_suffix(".collected.json")
    report.write_text(json.dumps(
        {"batch_id": m["batch_id"], "wave": m["wave"], "spend_inr": round(spend, 2),
         "rows": rows}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nreport: {rel(report)}")
    print("next: python3 genon/batch_build.py " + subject + " " + " ".join(m["grades"]) +
          " --certify-only   (free: annotate, arrange options, certify, report)")
    if m["wave"] == "top" and not bad:
        print("then:  python3 genon/batch_api.py submit " + subject + " " +
              " ".join(m["grades"]) + " --wave compact")
    return 1 if bad else 0


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        raise SystemExit(__doc__)
    cmd, rest = sys.argv[1], sys.argv[2:]
    if cmd == "submit":
        return cmd_submit(rest)
    if cmd == "status":
        return cmd_status(rest)
    if cmd == "collect":
        return cmd_collect(rest)
    raise SystemExit(f"unknown command {cmd!r}\n{__doc__}")


if __name__ == "__main__":
    sys.exit(main())
