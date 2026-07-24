#!/usr/bin/env python3
"""Tier-1 seam polish — the ONLY LLM step in the partition pipeline.

Scope is fenced: the model may rewrite ONLY (a) seam opening notes and (b) titles
of continued/merged periods — the fields the partition engine was forced to
synthesize. It receives the surrounding verbatim bands for context and returns a
compact JSON delta; code applies it. Phase text is never sent for rewriting and
never touched.

Usage: ANTHROPIC_API_KEY=... python3 polish_seams.py <plan.json> <out_plan.json>
"""
import json
import os
import sys
import time

MODEL = os.environ.get("GENON_MODEL", "claude-sonnet-4-6")
IN_1K, OUT_1K, INR = 0.003, 0.015, 92.0

SYSTEM = """You polish the seams of an adapted Aruvi lesson plan. The plan's content is
certified and untouchable — you are given it only as context. You rewrite exactly two
kinds of container text, nothing else:

1. seam_note — 1–2 sentences opening a period that continues mid-unit from the previous
   period. Navigation language only: orient the teacher on where the arc stopped and how
   to resume. You may reference ONLY activities visible in the context bands. NO new
   content, facts, examples, questions, or tasks. Do not use the words "period" or
   "seam" — teachers see "unit" language. Write flowing prose, no brackets or labels.

2. title — a natural period title for continued/merged periods. Derive it from the
   source unit titles given; blend, do not invent new topic language. Keep under 70
   characters where possible. Avoid mechanical joins like "A, then B" — write it the
   way a teacher would name the session.

3. teacher_note — rewrite the period's FULL teacher note as ONE flowing note within the
   stated word_budget (a hard cap). The current note mechanically stacks the source
   units' notes and is too long. Condense, do not merely truncate. Priority order when
   space runs out: (a) the continuation orientation (where the arc stopped, how to
   resume) where one applies; (b) each source unit's named student confusion — these
   are certified content, keep one per unit; (c) one facilitation pointer or hook.
   Drop repetition and connective padding first. Every fact must come from the current
   note — condense only, never add. No "[Next unit]" or bracketed markers.
   HARD REQUIREMENT: when needs_seam_note is true, the teacher_note MUST BEGIN with one
   short continuation clause (max 20 words) saying where the previous session stopped
   and what to resume — this outranks everything else in the priority order.

Return ONLY raw JSON:
{"periods": [{"n": <int>, "title": <string|null>, "seam_note": <string|null>, "teacher_note": <string|null>}]}
null keeps the existing value. Cover every period in the request. Where you write
teacher_note, fold the seam orientation INTO it and set seam_note to null."""


def build_request(plan):
    ps = plan["result"]["lesson_plan"]["periods"]
    flagged = []
    for i, p in enumerate(ps):
        continued = "— continued" in p["activity_title"] or ", then " in p["activity_title"]
        seam = p["teacher_notes"].startswith("This period continues")
        if not (continued or seam):
            continue
        prev_close = ps[i - 1]["time_bands"][-1]["activity"] if i else None
        n_units = len(p["section_anchor"].split(" / "))
        flagged.append({
            "n": p["period_number"],
            "current_title": p["activity_title"],
            "source_unit_titles": p["section_anchor"].split(" / "),
            "needs_seam_note": seam,
            "previous_period_closing_activity": prev_close,
            "this_period_opening_activity": p["time_bands"][0]["activity"],
            "current_teacher_note": p["teacher_notes"],
            "word_budget": min(100, 75 + 15 * (n_units - 1)),
        })
    return flagged


def apply_polish(plan, delta):
    ps = plan["result"]["lesson_plan"]["periods"]
    by_n = {p["period_number"]: p for p in ps}
    changed = []
    for d in delta.get("periods", []):
        p = by_n[int(d["n"])]
        if d.get("title"):
            p["activity_title"] = d["title"].strip()
        if d.get("teacher_note"):
            p["teacher_notes"] = d["teacher_note"].strip()
        elif d.get("seam_note") and p["teacher_notes"].startswith("This period continues"):
            head, _, rest = p["teacher_notes"].partition("\n\n")
            p["teacher_notes"] = d["seam_note"].strip() + "\n\n" + rest
        changed.append(int(d["n"]))
    return changed


def main():
    src, outp = sys.argv[1], sys.argv[2]
    plan = json.load(open(src))
    flagged = build_request(plan)
    user = ("Polish these flagged periods of an adapted lesson plan "
            f"({plan['subject']}, {plan['grade']}, ch {plan['chapter_number']} — "
            f"{plan['chapter_title']}):\n\n" + json.dumps(flagged, ensure_ascii=False)
            + "\n\nReturn the JSON delta now.")

    import anthropic
    t0 = time.time()
    resp = anthropic.Anthropic().messages.create(
        model=MODEL, max_tokens=3000, temperature=0.3,
        system=SYSTEM, messages=[{"role": "user", "content": user}])
    wall = time.time() - t0
    text = "".join(b.text for b in resp.content if b.type == "text").strip()
    if text.startswith("```"):
        text = text.split("```")[1].removeprefix("json")
    delta = json.loads(text[text.find("{"): text.rfind("}") + 1])

    changed = apply_polish(plan, delta)
    u = resp.usage
    cost = (u.input_tokens / 1000 * IN_1K + u.output_tokens / 1000 * OUT_1K) * INR
    plan["genon"]["seam_polish"] = {
        "tier": 1, "model": MODEL, "periods_polished": changed,
        "wall_seconds": round(wall, 1), "input_tokens": u.input_tokens,
        "output_tokens": u.output_tokens, "cost_inr": round(cost, 2),
    }
    json.dump(plan, open(outp, "w"), ensure_ascii=False, indent=2)
    print(f"OK  polished periods {changed} | {wall:.1f}s | "
          f"in {u.input_tokens} / out {u.output_tokens} | Rs. {cost:.2f}")


if __name__ == "__main__":
    main()
