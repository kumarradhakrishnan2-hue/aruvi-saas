#!/usr/bin/env python3
"""test_mcq_convention.py — cheap live probe of the Rule 7 MCQ option-order convention.

Authors ONLY the MCQ items (one per competency) from the chapter's existing LO handoff
rows, under the LIVE assessment constitution's Rule 2 + Rule 7 + guide spec — then checks
mechanically whether the emitted options are in arrangement order (alphabetical by text,
ascending for numeric), where the correct answer landed, and whether the guide's option
letters stayed consistent with the arrangement.

Costs roughly Rs 5–8 against Rs 46 for a full chapter regeneration.

Honest caveat (printed with the result): authoring 6 MCQs in isolation is a lighter load
than emitting them 30k tokens into a full generation. A pass here means the clause steers
the task; the position effect is only settled by the next full run.

Usage:  python3 genon/test_mcq_convention.py [subject grade chapter]
        (defaults: social_sciences ix 3; needs ANTHROPIC_API_KEY)
"""
from __future__ import annotations

import json
import os
import re
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(REPO))
from aruvi_core.grades import stage_for  # noqa: E402

MODEL = "claude-sonnet-4-6"
USD_IN, USD_OUT, INR = 3.0, 15.0, 92.0


def block(text: str, start_pat: str, end_pat: str = r"\n={10,}") -> str:
    m = re.search(start_pat, text)
    e = re.search(end_pat, text[m.end():])
    return text[m.start(): m.end() + e.start()]


def number(t: str):
    m = re.match(r"^[^\d\-]{0,3}(-?\d[\d,]*\.?\d*)", t.strip())
    return float(m.group(1).replace(",", "")) if m else None


def arranged(options: list[dict]) -> tuple[bool, str]:
    """Is this option list in the Rule 7 arrangement? (labels A–D in order, texts
    alphabetical — or ascending where every option is numeric.)"""
    if [o.get("label") for o in options] != ["A", "B", "C", "D"]:
        return False, "labels not A–D in order"
    texts = [str(o.get("text", "")) for o in options]
    nums = [number(t) for t in texts]
    if all(n is not None for n in nums):
        return (nums == sorted(nums)), ("ascending" if nums == sorted(nums)
                                        else f"not ascending {nums}")
    norm = [re.sub(r"^[\"'\s]+", "", t).lower() for t in texts]
    if norm == sorted(norm):
        return True, "alphabetical"
    order = [sorted(norm).index(n) + 1 for n in norm]
    return False, f"not alphabetical (sort positions {order})"


def main() -> int:
    subject = sys.argv[1] if len(sys.argv) > 1 else "social_sciences"
    grade = sys.argv[2] if len(sys.argv) > 2 else "ix"
    ch = int(sys.argv[3]) if len(sys.argv) > 3 else 3
    stage = stage_for(grade)

    canon = json.loads((REPO / "data" / "content" / "saved_plans" / subject / grade /
                        f"ch_{ch:02d}_canonical.json").read_text(encoding="utf-8"))
    result = canon.get("result", canon)
    handoff = result["coverage_handoff"]
    existing = [i for i in result.get("assessment_items", [])
                if i.get("question_type") == "MCQ"]

    summary = (REPO / "data" / "content" / "chapters" / subject / grade / "summaries" /
               f"ch_{ch:02d}_summary.txt").read_text(encoding="utf-8")
    const_path = (REPO / "data" / "content" / "constitutions" / "assessment" / subject /
                  stage / "assessment_constitution.txt")
    const = const_path.read_text(encoding="utf-8")
    version = const.splitlines()[0]
    rules = "\n\n".join([block(const, r"RULE 2 · EDGE INHERITANCE"),
                         block(const, r"RULE 7 · MCQ DESIGN"),
                         block(const, r"RULE 10 · GUIDE LAYER")])

    # One MCQ per competency, on the LO the certified assessment used for its MCQ slot.
    slots = []
    for it in existing:
        code = it["competency"]["c_code"]
        blk = handoff.get(code, {})
        lo = next((l for l in blk.get("los", [])
                   if l["implied_lo"] == it["implied_lo"]), None) or (blk.get("los") or [{}])[0]
        slots.append({"c_code": code, "cg": blk.get("cg"),
                      "competency_text": blk.get("competency_text"),
                      "implied_lo": lo.get("implied_lo"),
                      "cognitive_demand": lo.get("cognitive_demand"),
                      "section_anchor": lo.get("section_anchor"),
                      "section_context": lo.get("section_context")})

    system = (f"{version}\n\n{rules}\n\n"
              "You are authoring ONLY the MCQ slot — one MCQ per LO row supplied, in the "
              "order given. Obey Rule 2 (content from section_context and the Chapter "
              "Summary), Rule 7 in full including the option-order convention, and Rule 10's "
              "guide.MCQ. Output ONLY a JSON array; each element: "
              '{"c_code": str, "question_text": str, "options": [{"label","text",'
              '"is_correct"} x4], "cognitive_demand": str, '
              '"guide": {"MCQ": {"what_each_option_reveals": {label: str}}}}. '
              "No markdown fences, no commentary.")
    user = ("CHAPTER SUMMARY\n" + summary + "\n\nLO ROWS\n"
            + json.dumps(slots, ensure_ascii=False, indent=1))

    import anthropic
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    msg = client.messages.create(model=MODEL, max_tokens=8000, system=system,
                                 messages=[{"role": "user", "content": user}])
    out = msg.content[0].text.strip()
    if out.startswith("```"):
        out = out.split("\n", 1)[1].rsplit("```", 1)[0]
    items = json.loads(out)

    print(f"probe: {subject}/{grade}/ch{ch} · {version.split('·')[-1].strip()} · {MODEL}")
    n_ok = 0
    labels = []
    for it in items:
        opts = it.get("options", [])
        ok, why = arranged(opts)
        n_ok += ok
        correct = next((o["label"] for o in opts if o.get("is_correct")), "?")
        labels.append(correct)
        shape = (len(opts) == 4 and sum(bool(o.get("is_correct")) for o in opts) == 1)
        guide = set((it.get("guide", {}).get("MCQ", {})
                     .get("what_each_option_reveals") or {}).keys())
        want = {o["label"] for o in opts if not o.get("is_correct")}
        notes = []
        if not shape:
            notes.append("SHAPE: not 4 options / one correct")
        if guide != want:
            notes.append(f"GUIDE labels {sorted(guide)} != non-correct {sorted(want)}")
        print(f"  {'ok  ' if ok else 'FAIL'} {it.get('c_code','?'):>6}: order={why:<34} "
              f"correct={correct}" + ("  | " + "; ".join(notes) if notes else ""))
        if not ok:
            for o in opts:
                print(f"           {o.get('label')}. {'*' if o.get('is_correct') else ' '} "
                      f"{str(o.get('text',''))[:74]}")

    old = [next(o["label"] for o in i["options"] if o["is_correct"]) for i in existing]
    it_, ot_ = msg.usage.input_tokens, msg.usage.output_tokens
    cost = (it_ * USD_IN + ot_ * USD_OUT) / 1e6 * INR
    print(f"\narrangement   : {n_ok}/{len(items)} in convention order")
    print(f"correct labels: {labels}  spread {dict(Counter(labels))}"
          f"   (certified run under the old prohibition: {old} "
          f"spread {dict(Counter(old))})")
    print(f"cost          : {it_:,} in / {ot_:,} out = Rs {cost:.2f}")
    print("verdict       : the rule is judged on ARRANGEMENT, not on letter spread — "
          "an uneven spread with every item arranged is a PASS.")
    print("caveat        : isolated-task probe; the position effect of a full 30k-token "
          "generation is untested until the next full chapter run.")

    try:
        from api.data import append_token_log
        append_token_log("mcq_probe", subject, grade, ch,
                         canon.get("chapter_title", ""), it_, ot_, cost)
    except Exception:
        pass
    return 0 if n_ok == len(items) else 1


if __name__ == "__main__":
    sys.exit(main())
