"""Tier-1 seam polish — the ONLY LLM step in the partition pipeline.

Ported from the genon lab (polish_seams.py). Scope is fenced: the model may
rewrite ONLY (a) seam opening notes, (b) titles of continued/merged periods,
and (c) the flagged periods' teacher notes condensed to a word budget — the
container fields the partition engine was forced to synthesize. Phase text is
never sent for rewriting and never touched.

The API layer decides whether to run this (needs ANTHROPIC_API_KEY); the
functions here are pure request-building / delta-application so they can be
tested without the network.
"""
from __future__ import annotations

import json
import os
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
   Strip positional references — "the previous unit", "this unit", "the next unit" —
   and express the same continuity by NAMING the content instead ("Having traced the
   Vedic political vocabulary, …"). Position language is true only in the opening
   continuation clause, which comes from the actual partition.
   HARD REQUIREMENT: when needs_seam_note is true, the teacher_note MUST BEGIN with one
   short continuation clause (max 20 words) saying where the previous session stopped
   and what to resume — this outranks everything else in the priority order.

Return ONLY raw JSON:
{"periods": [{"n": <int>, "title": <string|null>, "seam_note": <string|null>, "teacher_note": <string|null>}]}
null keeps the existing value. Cover every period in the request. Where you write
teacher_note, fold the seam orientation INTO it and set seam_note to null."""


def build_polish_request(plan: dict) -> list:
    """The flagged-periods payload the model polishes. Empty list = nothing to polish."""
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


def apply_polish(plan: dict, delta: dict) -> list:
    """Apply the model's JSON delta in place. Returns the period numbers changed."""
    ps = plan["result"]["lesson_plan"]["periods"]
    by_n = {p["period_number"]: p for p in ps}
    changed = []
    for d in delta.get("periods", []):
        p = by_n[int(d["n"])]
        touched = False
        if d.get("title"):
            p["activity_title"] = d["title"].strip()
            touched = True
        if d.get("teacher_note"):
            p["teacher_notes"] = d["teacher_note"].strip()
            touched = True
        elif d.get("seam_note") and p["teacher_notes"].startswith("This period continues"):
            head, _, rest = p["teacher_notes"].partition("\n\n")
            p["teacher_notes"] = d["seam_note"].strip() + "\n\n" + rest
            touched = True
        if touched:                     # an all-null entry means "keep mine" — not a polish
            changed.append(int(d["n"]))
    return changed


def _first_sentence_words(text: str) -> int:
    t = str(text or "").strip()
    for stop in (". ", "? ", "! "):
        i = t.find(stop)
        if i > 0:
            return len(t[:i].split())
    return len(t.split())


def validate_delta(flagged: list, delta: dict) -> tuple:
    """The owed polish validator (HANDOVER): per flagged period, the rewritten
    teacher_note must respect the word budget (10% grace) and — when a seam note is
    needed — open with a short continuation clause (first sentence ≤ 24 words).
    Returns (valid_periods, rejected: {n: reason}); the caller applies only the
    valid subset and keeps tier-0 text for the rest. These are exactly the failure
    modes Haiku showed (dropped clause, busted cap) — now caught by code."""
    by_n = {f["n"]: f for f in flagged}
    valid, rejected = [], {}
    for d in delta.get("periods", []):
        n = int(d.get("n", -1))
        f = by_n.get(n)
        if f is None:
            rejected[n] = "period not in request"
            continue
        note = d.get("teacher_note")
        if note:
            budget = int(f.get("word_budget") or 100)
            words = len(str(note).split())
            if words > budget * 1.1 + 2:
                rejected[n] = f"teacher_note {words} words > budget {budget}"
                continue
            if f.get("needs_seam_note") and _first_sentence_words(note) > 24:
                rejected[n] = "missing/overlong continuation clause"
                continue
        elif f.get("needs_seam_note") and not d.get("seam_note"):
            rejected[n] = "needs seam orientation but delta carries none"
            continue
        valid.append(d)
    return valid, rejected


def run_polish(plan: dict) -> dict:
    """Run the tier-1 LLM pass in place — validated, with tier-0 fallback per period.

    Always-on policy (founder, 2026-07-25): the caller invokes this on every adapted
    plan; it is a no-op when nothing is flagged, and it raises RuntimeError only when
    no API key is configured (the caller records the skip — the plan ships with its
    tier-0 seams either way). A delta that fails validation is retried once with the
    rejection reasons; periods still failing keep their tier-0 text.
    """
    if not os.environ.get("ANTHROPIC_API_KEY"):
        raise RuntimeError("ANTHROPIC_API_KEY not configured on the server")
    flagged = build_polish_request(plan)
    if not flagged:
        rec = {"tier": 1, "model": MODEL, "periods_polished": [],
               "note": "no seams/merged periods to polish"}
        plan.setdefault("genon", {})["seam_polish"] = rec
        return rec

    import anthropic
    client = anthropic.Anthropic()
    base_user = ("Polish these flagged periods of an adapted lesson plan "
                 f"({plan['subject']}, {plan['grade']}, ch {plan['chapter_number']} — "
                 f"{plan['chapter_title']}):\n\n" + json.dumps(flagged, ensure_ascii=False)
                 + "\n\nReturn the JSON delta now.")

    t0 = time.time()
    in_tok = out_tok = 0
    accepted: dict = {}         # n -> validated delta entry; merged ACROSS attempts
    rejected: dict = {}         # n -> reason, for periods still unresolved
    parse_failures = 0
    user = base_user
    for attempt in range(2):
        resp = client.messages.create(
            model=MODEL, max_tokens=3000, temperature=0.3,
            system=SYSTEM, messages=[{"role": "user", "content": user}])
        in_tok += resp.usage.input_tokens
        out_tok += resp.usage.output_tokens
        text = "".join(b.text for b in resp.content if b.type == "text").strip()
        if text.startswith("```"):
            text = text.split("```")[1].removeprefix("json")
        try:
            delta = json.loads(text[text.find("{"): text.rfind("}") + 1])
        except Exception:
            delta = None
        if delta is None:
            # A garbled reply must NOT read as "nothing needed changing": every period not
            # already accepted stays rejected, so the loop retries and the record says why.
            parse_failures += 1
            rejected = {f["n"]: "unparseable delta" for f in flagged
                        if f["n"] not in accepted}
        else:
            valid, rejected = validate_delta(flagged, delta)
            for d in valid:
                accepted[int(d["n"])] = d       # round-1 wins survive a partial retry
            rejected = {n: r for n, r in rejected.items() if n not in accepted}
        if not rejected:
            break
        # One retry, naming what failed. ONLY the failures are resent — the accepted
        # entries are held above, so a partial reply loses nothing and the second call
        # costs a fraction of the first (the old "full delta again" wording doubled
        # both input AND output token spend to fix a single period).
        user = (base_user + "\n\nYour previous delta failed validation on these periods — "
                + json.dumps(rejected) + ". Return a JSON delta covering ONLY these periods, "
                "corrected, respecting the word budgets and the ≤20-word opening "
                "continuation clause. The periods not listed are already accepted — do not resend them.")
    changed = apply_polish(plan, {"periods": [accepted[n] for n in sorted(accepted)]})
    wall = time.time() - t0
    cost = (in_tok / 1000 * IN_1K + out_tok / 1000 * OUT_1K) * INR
    rec = {
        "tier": 1, "model": MODEL,
        "flagged": [f["n"] for f in flagged],   # candidates, so polished + kept always adds up
        "periods_polished": changed,
        "tier0_kept": sorted(rejected),
        "tier0_reasons": {str(k): v for k, v in rejected.items()},
        "parse_failures": parse_failures,
        "wall_seconds": round(wall, 1),
        "input_tokens": in_tok, "output_tokens": out_tok, "cost_inr": round(cost, 2),
    }
    plan.setdefault("genon", {})["seam_polish"] = rec
    return rec
