#!/usr/bin/env python3
"""Gen-on-gen live runner.

Sends the pre-warm's timed skeleton + the adaptation doc to the model, receives the
compact delta, applies it deterministically, and reports tokens / cost / wall time.

Usage:
  ANTHROPIC_API_KEY=... python3 run_genon.py <source_plan.json> <matrix e.g. 12x45> <out_dir>
"""
import json
import os
import sys
import time
from pathlib import Path

import apply_delta as ad

MODEL = os.environ.get("GENON_MODEL", "claude-sonnet-4-6")
# rates: app/runtime_data/api_rates.json (claude-sonnet-4-6), USD->INR 92
IN_PER_1K_USD, OUT_PER_1K_USD, USD_INR = 0.003, 0.015, 92.0


def slim_periods(plan):
    """Only what boundary decisions need: numbers, titles, sections, timed bands."""
    keep = ("period_number", "period_duration_minutes", "activity_title",
            "section_anchor", "time_bands")
    return [{k: p[k] for k in keep} for p in plan["result"]["lesson_plan"]["periods"]]


def matrix_str(matrix):
    return " + ".join(f"{c} × {d} min" for d, c in matrix) + \
        f"  (total {sum(d*c for d, c in matrix)} min)"


def build_messages(plan, matrix, doc_text):
    old = plan["period_rows_snapshot"]
    old_matrix = " + ".join(f"{r['count']} × {r['duration']} min" for r in old) + \
        f"  (total {sum(r['count']*r['duration'] for r in old)} min)"
    user = (
        f"OLD_MATRIX: {old_matrix}\n"
        f"NEW_MATRIX: {matrix_str(matrix)}\n\n"
        f"Chapter: {plan['subject']} · grade {plan['grade']} · ch {plan['chapter_number']} — "
        f"{plan['chapter_title']}\n\n"
        "PRE-WARM PERIODS (timed skeleton):\n"
        + json.dumps(slim_periods(plan), ensure_ascii=False)
        + "\n\nEmit the adaptation delta JSON now."
    )
    return doc_text, user


def extract_json(text):
    t = text.strip()
    if t.startswith("```"):
        t = t.split("```")[1]
        if t.startswith("json"):
            t = t[4:]
    start, end = t.find("{"), t.rfind("}")
    return json.loads(t[start:end + 1])


def main():
    src, spec, out_dir = sys.argv[1], sys.argv[2], sys.argv[3]
    out = Path(out_dir); out.mkdir(parents=True, exist_ok=True)
    plan = json.load(open(src))
    matrix = ad.parse_matrix(spec)
    doc = open(Path(__file__).parent / "genon_adaptation_doc.md").read()

    system, user = build_messages(plan, matrix, doc)
    (out / "prompt_user.txt").write_text(user)

    import anthropic
    client = anthropic.Anthropic()
    t0 = time.time()
    resp = client.messages.create(
        model=MODEL,
        max_tokens=8000,
        temperature=0.2,
        system=system,
        messages=[{"role": "user", "content": user}],
    )
    wall = time.time() - t0
    text = "".join(b.text for b in resp.content if b.type == "text")
    (out / "raw_response.txt").write_text(text)

    usage = resp.usage
    cost_inr = (usage.input_tokens / 1000 * IN_PER_1K_USD +
                usage.output_tokens / 1000 * OUT_PER_1K_USD) * USD_INR

    delta = extract_json(text)
    json.dump(delta, open(out / "delta.json", "w"), ensure_ascii=False, indent=2)

    provenance = {
        "model": MODEL, "wall_seconds": round(wall, 1),
        "input_tokens": usage.input_tokens, "output_tokens": usage.output_tokens,
        "cost_inr": round(cost_inr, 2), "doc_version": "genon v0.1",
    }
    adapted = ad.adapt(plan, delta, matrix, provenance=provenance)
    outfile = out / (Path(src).stem + f"_genon_{spec}.json")
    json.dump(adapted, open(outfile, "w"), ensure_ascii=False, indent=2)

    orig = plan["result"]
    print("=== GEN-ON-GEN RUN REPORT ===")
    print(f"model            : {MODEL}")
    print(f"wall time        : {wall:.1f} s")
    print(f"input tokens     : {usage.input_tokens}")
    print(f"output tokens    : {usage.output_tokens}")
    print(f"cost             : Rs. {cost_inr:.2f}")
    print(f"original run     : in {orig.get('input_tokens')} / out {orig.get('output_tokens')}"
          f" / Rs. {orig.get('cost_inr')}")
    if orig.get("cost_inr"):
        print(f"cost ratio       : {cost_inr / orig['cost_inr'] * 100:.1f}% of original")
    print(f"adapted plan     : {outfile}")


if __name__ == "__main__":
    main()
