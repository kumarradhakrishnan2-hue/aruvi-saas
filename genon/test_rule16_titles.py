#!/usr/bin/env python3
"""test_rule16_titles.py — cheap live probe of the Rule 16 derived-title amendment.

Instead of regenerating a whole chapter (~Rs 46), this sends ONLY the existing
unit_handoff teacher_notes (which the first live run got right) plus the LIVE
Rule 16 text and the SELF-CONTAINED REGISTER block, and asks the model to derive
the titles — exactly the task v1.6 defines. Then it runs the REAL validator
(aruvi_core.genon.partition.validate_unit_handoff) on the result, so pass/fail
is judged by the same code the generator uses. ~3k tokens in / ~0.5k out ≈ Rs 1.

Honest caveat (also printed): this validates the rule text and the derivation
task in isolation. It does NOT reproduce the position effect of a full 30k-token
generation — the final proof is still the next full chapter run; this probe is
the fast iteration loop that decides whether that Rs 46 is worth spending yet.

Usage:  python3 genon/test_rule16_titles.py [subject grade chapter]
        (defaults: social_sciences ix 3; needs ANTHROPIC_API_KEY)
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent            # genon/
REPO = HERE.parent
sys.path.insert(0, str(REPO))
from aruvi_core.genon.partition import handoff_vocab, validate_unit_handoff  # noqa: E402
from aruvi_core.grades import stage_for  # noqa: E402

MODEL = "claude-sonnet-4-6"
USD_IN, USD_OUT, INR = 3.0, 15.0, 92.0


def extract_block(text: str, start_pat: str, end_pat: str) -> str:
    m = re.search(start_pat, text)
    e = re.search(end_pat, text[m.end():])
    return text[m.start(): m.end() + e.start()]


def main() -> int:
    subject = sys.argv[1] if len(sys.argv) > 1 else "social_sciences"
    grade = sys.argv[2] if len(sys.argv) > 2 else "ix"
    ch = int(sys.argv[3]) if len(sys.argv) > 3 else 3

    canon = json.loads((REPO / "data" / "content" / "saved_plans" / subject / grade /
                        f"ch_{ch:02d}_canonical.json").read_text(encoding="utf-8"))
    result = canon.get("result", canon)
    handoff = result["unit_handoff"]
    periods = result["lesson_plan"]["periods"]
    titles_by_period = {p["period_number"]: p["activity_title"] for p in periods}

    stage = stage_for(grade)
    const = (REPO / "data" / "content" / "constitutions" / "lesson_plan" / subject /
             stage / "lesson_plan_constitution.txt").read_text(encoding="utf-8")
    register = extract_block(const, r"THE SELF-CONTAINED REGISTER", r"\n\n")
    rule16 = extract_block(const, r"RULE 16 · UNIT HANDOFF", r"={10,}")
    version = const.splitlines()[0]

    notes_payload = {k: {"units": f"{titles_by_period[int(k.split('-')[0])]} → "
                                  f"{titles_by_period[int(k.split('-')[1])]}",
                         "teacher_notes": v["teacher_notes"]}
                     for k, v in handoff.items()}

    system = (f"{version}\n\n{register}\n\n{rule16}\n\n"
              "You are performing ONLY the title-derivation half of Rule 16. The "
              "teacher_notes below are already authored and are authoritative — do not "
              "rewrite them. For each adjacent pair, derive the title exactly as the "
              "rule defines: the note's opening pivot restated as one noun phrase, "
              "readable back out of the note's first sentence, obeying every "
              "prohibition. Output ONLY a JSON object mapping each pair key to its "
              "title string. No markdown fences, no commentary.")
    user = json.dumps(notes_payload, ensure_ascii=False, indent=1)

    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(model=MODEL, max_tokens=2000,
                                 system=system,
                                 messages=[{"role": "user", "content": user}])
    out = msg.content[0].text.strip()
    if out.startswith("```"):
        out = out.split("\n", 1)[1].rsplit("```", 1)[0]
    titles = json.loads(out)

    # Rebuild the handoff with the probe's titles + the existing notes, and run the
    # REAL validator over it — same code path as generate_canonical.py.
    probe_handoff = {k: {"title": titles.get(k, ""), "teacher_notes": handoff[k]["teacher_notes"]}
                     for k in handoff}
    problems = validate_unit_handoff(probe_handoff, len(periods), handoff_vocab(periods))
    title_problems = [p for p in problems if "title" in p]

    it, ot = msg.usage.input_tokens, msg.usage.output_tokens
    cost = (it * USD_IN + ot * USD_OUT) / 1e6 * INR
    print(f"probe: {subject}/{grade}/ch{ch} · {version.split('·')[-1].strip()} · {MODEL}")
    for k in sorted(titles, key=lambda x: int(x.split("-")[0])):
        bad = [p for p in title_problems if p.startswith(f"unit_handoff {k}:")]
        print(f"  {'FAIL' if bad else 'ok  '} {k}: {titles[k]}" +
              (f"   <- {bad[0].split(':', 1)[1].strip()}" if bad else ""))
    n_fail = len({p.split(':')[0] for p in title_problems})
    print(f"\ntitle verdict : {len(titles) - n_fail}/{len(titles)} clean "
          f"(was 1/11 under v1.5)")
    if problems and not title_problems:
        print("note: validator raised non-title findings (pre-existing):",
              problems[:3])
    print(f"cost          : {it:,} in / {ot:,} out = Rs {cost:.2f}")
    print("caveat        : isolated-task probe — the position effect of a full "
          "generation is untested until the next full chapter run.")

    # founder's cost notebook, best-effort
    try:
        sys.path.insert(0, str(REPO))
        from api.data import append_token_log
        append_token_log("rule16_probe", subject, grade, ch,
                         canon.get("chapter_title", ""), it, ot, cost)
    except Exception:
        pass
    return 1 if n_fail else 0


if __name__ == "__main__":
    sys.exit(main())
