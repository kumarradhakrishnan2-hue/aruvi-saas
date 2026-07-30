"""Tier-1 polish: the record must never overstate or misreport what happened.

Guards the three failure modes fixed on 2026-07-25 in aruvi_core/genon/polish.run_polish:
  1. An unparseable model reply used to be silently converted into a clean
     "nothing needed changing" record (validate_delta overwrote the rejection dict,
     the empty dict read as all-clear, the loop broke without retrying).
  2. The retry replaced the accepted set wholesale, so a partial second reply
     discarded periods that had already validated in round 1.
  3. periods_polished counted all-null delta entries ("keep mine") as polished.

Plus the unchanged happy path: one call when the first reply validates, and the
token/cost accounting. No network, no API key spend — the anthropic client is faked.

Run:  python3 tests/test_genon_polish.py
(stdlib only, like every other suite)
"""
import copy
import json
import os
import sys
import types

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ["ANTHROPIC_API_KEY"] = "test-not-a-real-key"

from aruvi_core.genon import polish as P

FAILURES = []


def check(label, cond, detail=""):
    print(("PASS  " if cond else "FAIL  ") + label + (("  <- " + detail) if not cond and detail else ""))
    if not cond:
        FAILURES.append(label)


# ── fixture: a partitioned plan shaped like the engine's output ──────────────
def _period(n, title, note, anchors):
    return {
        "period_number": n,
        "activity_title": title,
        "teacher_notes": note,
        "section_anchor": " / ".join(anchors),
        "time_bands": [
            {"minutes": "0-25", "activity": f"opening activity of period {n}"},
            {"minutes": "25-50", "activity": f"closing activity of period {n}"},
        ],
    }


def make_plan():
    """Three flagged periods: a seam, a merge, and a seam+merge."""
    periods = [
        _period(1, "Diversity in India", "A plain note with no seam.", ["Unit A"]),
        _period(2, "Diversity in India — continued",
                "This period continues the previous unit.\n\nWatch for the usual confusion.",
                ["Unit A"]),
        _period(3, "Unit B, then Unit C", "A stacked note from two units.", ["Unit B", "Unit C"]),
        _period(4, "Unit D — continued",
                "This period continues the previous unit.\n\nMore stacked note text.",
                ["Unit D", "Unit E"]),
    ]
    return {
        "subject": "social_sciences", "grade": "ix",
        "chapter_number": 5, "chapter_title": "Test Chapter",
        "result": {"lesson_plan": {"periods": periods}},
    }


PLAN = make_plan()
FLAGGED = P.build_polish_request(copy.deepcopy(PLAN))
NS = [f["n"] for f in FLAGGED]
check("fixture flags the seam/merged periods only", NS == [2, 3, 4], str(NS))
check("fixture marks seam periods", [f["n"] for f in FLAGGED if f["needs_seam_note"]] == [2, 4])


# ── fake model replies ──────────────────────────────────────────────────────
def good(f):
    """A delta entry that passes validate_delta for flagged period f."""
    return {"n": f["n"], "title": "A tidy title", "seam_note": None,
            "teacher_note": "We stopped at the map task; resume by comparing the two panels. "
                            + " ".join(["word"] * 8)}


def bad(f):
    """Busts the word budget -> must be rejected."""
    return {"n": f["n"], "title": "x", "seam_note": None,
            "teacher_note": "We stopped at the map task; resume now. " + " ".join(["padding"] * 300)}


class FakeClient:
    """Replies from a script, one entry per attempt. 'RAW' = unparseable reply."""

    def __init__(self, script):
        self.script, self.calls = script, []

    @property
    def messages(self):
        return self

    def create(self, **kw):
        self.calls.append(kw["messages"][0]["content"])
        payload = self.script[min(len(self.calls) - 1, len(self.script) - 1)]
        text = "not json at all {{{" if payload == "RAW" else json.dumps(payload)
        return types.SimpleNamespace(
            content=[types.SimpleNamespace(type="text", text=text)],
            usage=types.SimpleNamespace(input_tokens=1000, output_tokens=500))


def run(script):
    fake = types.ModuleType("anthropic")
    client = FakeClient(script)
    fake.Anthropic = lambda *a, **k: client
    sys.modules["anthropic"] = fake
    plan = copy.deepcopy(PLAN)
    return P.run_polish(plan), plan, client


# ── 1. garbled first reply retries, and says so ─────────────────────────────
rec, plan, cl = run(["RAW", {"periods": [good(f) for f in FLAGGED]}])
check("garbled reply triggers the retry", len(cl.calls) == 2, f"{len(cl.calls)} call(s)")
check("parse failure is counted", rec["parse_failures"] == 1, str(rec["parse_failures"]))
check("all periods polished after the retry", rec["periods_polished"] == NS, str(rec["periods_polished"]))
check("nothing falsely left on tier-0", rec["tier0_kept"] == [], str(rec["tier0_kept"]))

# ── 2. two garbled replies must NOT look like a clean no-op ────────────────
rec, plan, cl = run(["RAW", "RAW"])
check("both attempts used", len(cl.calls) == 2)
check("both parse failures counted", rec["parse_failures"] == 2, str(rec["parse_failures"]))
check("nothing claimed as polished", rec["periods_polished"] == [])
check("every flagged period reported kept", rec["tier0_kept"] == sorted(NS), str(rec["tier0_kept"]))
check("the reason survives into the record",
      bool(rec["tier0_reasons"]) and set(rec["tier0_reasons"].values()) == {"unparseable delta"})
check("candidates listed, so polished + kept adds up", rec["flagged"] == NS, str(rec.get("flagged")))

# ── 3. a partial retry keeps round-1 wins ──────────────────────────────────
r1 = {"periods": [good(FLAGGED[0]), good(FLAGGED[1]), bad(FLAGGED[2])]}
r2 = {"periods": [good(FLAGGED[2])]}          # ONLY the corrected period
rec, plan, cl = run([r1, r2])
check("round-1 accepted periods survive the retry", rec["periods_polished"] == NS,
      str(rec["periods_polished"]))
check("no false tier-0 report after a partial retry", rec["tier0_kept"] == [], str(rec["tier0_kept"]))
by_n = {p["period_number"]: p for p in plan["result"]["lesson_plan"]["periods"]}
check("a round-1 period really carries the new text", by_n[NS[0]]["activity_title"] == "A tidy title")
check("unflagged periods are untouched",
      by_n[1]["activity_title"] == "Diversity in India" and by_n[1]["teacher_notes"].startswith("A plain"))

# ── 4. all-null entries are not "polished" ─────────────────────────────────
merged_only = [f for f in FLAGGED if not f["needs_seam_note"]]
nulls = {"periods": [{"n": f["n"], "title": None, "seam_note": None, "teacher_note": None}
                     for f in merged_only]}
rec, plan, cl = run([nulls, nulls])
check("all-null entries excluded from periods_polished", rec["periods_polished"] == [],
      str(rec["periods_polished"]))

# ── 5. happy path unchanged ────────────────────────────────────────────────
rec, plan, cl = run([{"periods": [good(f) for f in FLAGGED]}])
check("single call when the first reply validates", len(cl.calls) == 1, f"{len(cl.calls)} call(s)")
expected_cost = round((1000 / 1000 * P.IN_1K + 500 / 1000 * P.OUT_1K) * P.INR, 2)
check("token and cost accounting intact",
      rec["input_tokens"] == 1000 and rec["output_tokens"] == 500 and rec["cost_inr"] == expected_cost,
      str(rec["cost_inr"]))

# ── 6. phase text is never touched (the standing invariant) ────────────────
rec, plan, cl = run([{"periods": [good(f) for f in FLAGGED]}])
before = [p["time_bands"] for p in PLAN["result"]["lesson_plan"]["periods"]]
after = [p["time_bands"] for p in plan["result"]["lesson_plan"]["periods"]]
check("band text identical before and after polish", before == after)

# ── 7. no seams -> explicit no-op record, no API call ──────────────────────
plain = copy.deepcopy(PLAN)
plain["result"]["lesson_plan"]["periods"] = [_period(1, "Plain", "Plain note.", ["Unit A"])]
fake = types.ModuleType("anthropic")
cl = FakeClient([{"periods": []}])
fake.Anthropic = lambda *a, **k: cl
sys.modules["anthropic"] = fake
rec = P.run_polish(plain)
check("nothing flagged -> no model call", len(cl.calls) == 0, f"{len(cl.calls)} call(s)")
check("nothing flagged -> labelled no-op record", rec.get("note", "").startswith("no seams"))

print("\n" + ("ALL PASS" if not FAILURES else "FAILURES: " + ", ".join(FAILURES)))
sys.exit(1 if FAILURES else 0)
