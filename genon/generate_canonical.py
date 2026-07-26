#!/usr/bin/env python3
"""generate_canonical.py — one CLI for canonical LP+assessment generation.

Sync mode (this version — HANDOVER step-4 execution design):

    python3 generate_canonical.py one <subject> <grade> <chapter> [options]

    e.g.  python3 generate_canonical.py one social_sciences ix 5
          python3 generate_canonical.py one social_sciences ix 5 --dry
          python3 generate_canonical.py one social_sciences ix 5 \
              --lp-const genon/amended/originals/lesson_plan_constitution_v1.0.txt \
              --assess-const genon/amended/originals/assessment_constitution_v1.1_pre_phase_ref.txt \
              --tag control_v10        # the v1.0 control test

Prompt assembly is delegated ENTIRELY to prompt_assembly.py (the verbatim
prototype wrapper) — this file only resolves inputs, makes the API call,
validates, saves, and logs. Batch mode (Message Batches API, 50% discount)
is deliberately deferred until the mass pre-warm sweep.

Defaults per the genon master plan:
- duration  = class-standard (40 ≤ VII, 45 VIII, 50 IX)
- period count = recommended_periods from genon/master_plan.json
- model = the certified generation model (claude-sonnet-4-6, thinking off —
  llm_client.py's certified baseline)

Requires ANTHROPIC_API_KEY in the environment for live runs (never --dry).
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import sys
import time
from datetime import datetime
from pathlib import Path

import prompt_assembly as pa

HERE = Path(__file__).resolve().parent           # genon/
REPO = HERE.parent                                # aruvi-saas/
OUT_DIR = HERE / "out" / "canonical"
LEDGER = HERE / "ledger.csv"

# Certified generation config — mirrors Project Aruvi llm_client.py
# (2026-07-15 regression cycle): Sonnet 4.6, thinking off.
GENERATION_MODEL = "claude-sonnet-4-6"
MAX_TOKENS_LPA = 64000
MAX_TOKENS_LP_ONLY = 32000

# ₹ economics (HANDOVER): $3/M input, $15/M output, ₹92/$ — override via flags.
USD_PER_M_INPUT = 3.0
USD_PER_M_OUTPUT = 15.0
INR_PER_USD = 92.0

FOLDER_TO_SUBJECT = {
    "social_sciences": "Social Science",
    "mathematics": "Mathematics",
    "science": "Science",
    "english": "English",
    "the_world_around_us": "The World Around Us",
}
ROMAN = {"iii": "III", "iv": "IV", "v": "V", "vi": "VI", "vii": "VII",
         "viii": "VIII", "ix": "IX", "x": "X"}


def std_duration(grade_folder: str) -> int:
    n = ["iii", "iv", "v", "vi", "vii", "viii", "ix", "x"].index(grade_folder) + 3
    if n <= 7:
        return 40
    if n == 8:
        return 45
    return 50


def master_plan_entry(subject_folder: str, grade_folder: str, chapter: int) -> dict | None:
    # master_plan.json lives with the other allocation sources (founder layout, 2026-07-25)
    mp = REPO / "data" / "content" / "allocation_norms" / "master_plan.json"
    if not mp.exists():
        return None
    combos = json.loads(mp.read_text(encoding="utf-8"))["combos"]
    combo = combos.get(f"{subject_folder}|{ROMAN[grade_folder]}")
    if not combo:
        return None
    for row in combo["chapters"]:
        if row["chapter"] == chapter:
            return row
    return None


def strip_fences(text: str) -> str:
    t = text.strip()
    if t.startswith("```"):
        t = t.split("\n", 1)[1] if "\n" in t else t
        if t.rstrip().endswith("```"):
            t = t.rstrip()[:-3]
    return t.strip()


def validate(parsed: dict, expected_periods: int, expect_v11: bool) -> list[str]:
    problems = []
    periods = parsed.get("lesson_plan", {}).get("periods", [])
    if len(periods) != expected_periods:
        problems.append(f"period count {len(periods)} != scheduled {expected_periods}")
    if not parsed.get("coverage_handoff"):
        problems.append("coverage_handoff missing/empty")
    if expect_v11:
        # LP v1.2: role lives in the Rule-15 role_handoff sibling; earlier v1.1.x
        # canonicals carried it inline on each band — accept either, require one.
        rh = parsed.get("role_handoff") or {}
        all_ids = []
        for p in periods:
            for b in p.get("time_bands", []):
                if not b.get("band_id"):
                    problems.append(f"P{p.get('period_number')}: band missing band_id")
                else:
                    all_ids.append(b["band_id"])
                role = rh.get(b.get("band_id")) or b.get("role")
                if role not in ("hook", "development", "consolidation"):
                    problems.append(f"P{p.get('period_number')}: band {b.get('band_id')} role {role!r}")
            for e in p.get("competency_edges", []):
                if not e.get("band_refs"):
                    problems.append(f"P{p.get('period_number')}: edge {e.get('c_code')} missing band_refs")
        extra = [k for k in rh if k not in all_ids]
        if extra:
            problems.append(f"role_handoff names unknown bands: {extra[:5]}")
        for c_code, blk in (parsed.get("coverage_handoff") or {}).items():
            for lo in blk.get("los", []):
                if not lo.get("band_refs"):
                    problems.append(f"handoff {c_code}: LO row missing band_refs")
        for item in parsed.get("assessment_items", []) or []:
            if isinstance(item, dict) and not item.get("phase_ref"):
                problems.append(f"assessment item {item.get('id', '?')} missing phase_ref")
    return problems[:40]


def log_ledger(row: dict) -> None:
    new = not LEDGER.exists()
    with LEDGER.open("a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(row.keys()))
        if new:
            w.writeheader()
        w.writerow(row)


# The founder's unified cost notebook (2026-07-25): every paid run ALSO appends to
# THIS repo's runtime_data/token_log.csv (fresh log started 2026-07-25, seeded with
# the first ch 5 canonical run; the pre-genon prototype history is archived
# alongside as token_log_old.csv). Best-effort — bookkeeping never breaks a run.
TOKEN_LOG = REPO / "runtime_data" / "token_log.csv"
_TOKEN_LOG_HEADER = ("timestamp,call_type,subject,grade,chapter_number,chapter_title,"
                     "input_tokens,output_tokens,total_tokens,cost_inr,"
                     "cache_write_input_tokens,cache_read_input_tokens")


def log_token_log(call_type, subject, grade, ch, title, it, ot, cost_inr) -> None:
    try:
        TOKEN_LOG.parent.mkdir(parents=True, exist_ok=True)
        if not TOKEN_LOG.exists():
            TOKEN_LOG.write_text(_TOKEN_LOG_HEADER + "\n", encoding="utf-8")
        with TOKEN_LOG.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                datetime.now().isoformat(timespec="seconds"), call_type, subject, grade,
                ch, title, it, ot, it + ot, round(cost_inr, 4), 0, 0,
            ])
    except Exception:
        pass


def cmd_one(args) -> int:
    subject_folder = args.subject
    grade_folder = args.grade.lower()
    ch = args.chapter
    subject = FOLDER_TO_SUBJECT[subject_folder]
    grade = f"Grade {ROMAN[grade_folder]}"

    mp_row = master_plan_entry(subject_folder, grade_folder, ch)
    duration = args.duration or std_duration(grade_folder)
    count = args.periods or (mp_row and mp_row["recommended_periods"])
    if not count:
        print("No period count: not in master_plan.json — pass --periods.", file=sys.stderr)
        return 2
    if mp_row and mp_row.get("placeholder"):
        print(f"REFUSING: chapter {ch} is a placeholder (awaiting NCERT release).", file=sys.stderr)
        return 2

    title = args.title or (mp_row and str(mp_row["title"]).split(": ", 1)[-1]) or ""
    chapter = {"chapter_number": ch, "chapter_title": title}
    paths = pa.resolve_paths(grade, subject, ch)
    if args.lp_const:
        paths["lp_constitution"] = Path(args.lp_const)
    if args.assess_const:
        paths["assessment_const"] = Path(args.assess_const)
    for k, p in paths.items():
        if not Path(p).exists() and not (k == "assessment_const" and args.lp_only):
            print(f"MISSING input {k}: {p}", file=sys.stderr)
            return 2

    period_sched = pa.standard_row_schedule(duration, count)
    system_blocks, user_blocks = pa.build_lpa_prompts(
        grade, subject, chapter, period_sched, paths,
        include_assessment=not args.lp_only,
    )

    lp_text = Path(paths["lp_constitution"]).read_text(encoding="utf-8")
    expect_v11 = "RULE 14" in lp_text
    sys_chars = sum(len(b["text"]) for b in system_blocks)
    usr_chars = sum(len(b["text"]) for b in user_blocks)
    print(f"{subject} · {grade} · ch {ch} — {count} × {duration} min "
          f"({'LP+A' if not args.lp_only else 'LP only'}; "
          f"constitution {'v1.1 genon' if expect_v11 else 'pre-genon'})")
    print(f"  schedule : {period_sched.splitlines()[-1]}")
    print(f"  system   : {sys_chars:,} chars   user: {usr_chars:,} chars")

    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    tag = f"_{args.tag}" if args.tag else ""
    out_dir = OUT_DIR / subject_folder / grade_folder
    out_dir.mkdir(parents=True, exist_ok=True)

    if args.dry:
        dump = out_dir / f"ch_{ch:02d}{tag}_{ts}_promptdump.json"
        dump.write_text(json.dumps(
            {"model": args.model, "max_tokens": MAX_TOKENS_LP_ONLY if args.lp_only else MAX_TOKENS_LPA,
             "system": system_blocks, "messages": [{"role": "user", "content": user_blocks}]},
            ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  DRY RUN — prompt dump: {dump}")
        return 0

    import anthropic  # only needed live
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    max_tokens = MAX_TOKENS_LP_ONLY if args.lp_only else MAX_TOKENS_LPA
    t0 = time.time()
    with client.messages.stream(
        model=args.model,
        max_tokens=max_tokens,
        system=system_blocks,
        messages=[{"role": "user", "content": user_blocks}],
    ) as s:
        # Live progress: chars streamed + rough period counter + elapsed,
        # updated in place. ~4 chars/token; periods counted by their key
        # appearing in the stream.
        parts = []
        chars = 0
        last = 0.0
        for chunk in s.text_stream:
            parts.append(chunk)
            chars += len(chunk)
            now = time.time()
            if now - last >= 1.0:
                last = now
                mm, ss = divmod(int(now - t0), 60)
                sofar = "".join(parts)
                # Stage-aware progress: periods → coverage handoff → role handoff →
                # assessment items (schema emission order). period_number also appears
                # on handoff LO rows, so the period counter is capped at the schedule;
                # items are counted by their period_ref key, which only items carry.
                ai = sofar.find('"assessment_items"')
                if ai != -1:
                    n_items = sofar.count('"period_ref"', ai)
                    stage = f"periods {count}/{count} · assessment item {n_items}"
                elif '"role_handoff"' in sofar:
                    stage = f"periods {count}/{count} · role handoff"
                elif '"coverage_handoff"' in sofar:
                    n_los = max(0, sofar.count('"period_number"') - count)
                    stage = f"periods {count}/{count} · handoff LO {n_los}"
                else:
                    done = sofar.count('"period_number"')
                    stage = f"period {min(done, count)}/{count}"
                sys.stderr.write(
                    f"\r  streaming: {chars:>8,} chars · ~{chars // 4:>6,} tokens · "
                    f"{stage} · {mm:02d}:{ss:02d}   "
                )
                sys.stderr.flush()
        sys.stderr.write("\n")
        full = "".join(parts)
        final = s.get_final_message()
    elapsed = time.time() - t0
    it, ot = final.usage.input_tokens, final.usage.output_tokens
    cost_inr = (it * USD_PER_M_INPUT + ot * USD_PER_M_OUTPUT) / 1e6 * INR_PER_USD

    raw_path = out_dir / f"ch_{ch:02d}{tag}_{ts}_raw.txt"
    raw_path.write_text(full, encoding="utf-8")

    # Parse — with bounded auto-repair for the model's one known serialization
    # glitch: naked (unescaped) double quotes inside a JSON string (the 2026-07-26
    # run lost its canonical to 4 of them). Each repair escapes exactly ONE quote
    # pair — provably content-neutral — and is recorded in the ledger. Any other
    # defect still fails hard: nothing else is auto-touched.
    text = strip_fences(full)
    parsed, problems, repairs = None, [], []
    for _ in range(10):
        try:
            parsed = json.loads(text)
            break
        except json.JSONDecodeError as e:
            q1 = text.rfind('"', 0, e.pos)
            q2 = text.find('"', e.pos)
            if q1 == -1 or q2 == -1 or q2 - q1 > 300:
                problems = [f"JSON parse error: {e}"]
                break
            repairs.append(text[q1 + 1:q2][:50])
            text = text[:q1] + '\\"' + text[q1 + 1:q2] + '\\"' + text[q2 + 1:]
    if parsed is not None:
        problems = validate(parsed, count, expect_v11)
        if repairs:
            print(f"  auto-repaired {len(repairs)} naked inner quote(s): "
                  + "; ".join(repr(r) for r in repairs[:4]))
    elif not problems:
        problems = ["output is not valid JSON"]
    status = "ok" if not problems else "problems"
    repair_note = [f"auto-repaired {len(repairs)} naked quotes"] if repairs else []
    if parsed is not None:
        canon_path = out_dir / f"ch_{ch:02d}{tag}_{ts}_canonical.json"
        canon_path.write_text(json.dumps(parsed, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"  saved    : {canon_path}")
    print(f"  tokens   : {it:,} in / {ot:,} out · ₹{cost_inr:.2f} · {elapsed:.1f}s · {status}")
    for p in problems:
        print(f"  ⚠ {p}")

    log_token_log("canonical_generation", subject_folder, grade_folder, ch, title,
                  it, ot, cost_inr)
    log_ledger({
        "ts": ts, "mode": "one", "tag": args.tag or "", "model": args.model,
        "subject": subject_folder, "grade": grade_folder, "chapter": ch,
        "schedule": f"{count}x{duration}", "lp_only": args.lp_only,
        "constitution": "v1.1" if expect_v11 else "pre-genon",
        "input_tokens": it, "output_tokens": ot,
        "cost_inr": round(cost_inr, 2), "seconds": round(elapsed, 1),
        "status": status, "problems": "; ".join(repair_note + problems)[:400],
        "raw_file": raw_path.name,
    })
    return 0 if status == "ok" else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    one = sub.add_parser("one", help="single supervised sync generation")
    one.add_argument("subject", choices=sorted(FOLDER_TO_SUBJECT))
    one.add_argument("grade", help="grade folder, e.g. ix")
    one.add_argument("chapter", type=int)
    one.add_argument("--periods", type=int, help="override period count (default: master plan)")
    one.add_argument("--duration", type=int, help="override duration (default: class standard)")
    one.add_argument("--title", help="override chapter title")
    one.add_argument("--lp-only", action="store_true", help="LP only (no assessment)")
    one.add_argument("--lp-const", help="override LP constitution path (control tests)")
    one.add_argument("--assess-const", help="override assessment constitution path")
    one.add_argument("--model", default=GENERATION_MODEL)
    one.add_argument("--tag", help="filename/ledger tag, e.g. control_v10")
    one.add_argument("--dry", action="store_true", help="assemble + dump prompt, no API call")
    one.set_defaults(fn=cmd_one)
    args = ap.parse_args()
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
