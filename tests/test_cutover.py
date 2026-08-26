"""Tests for administrative-architecture Step 2: the academic-year cutover.

The spec's own success test is "June works" (administrative_architecture.md §Step 2), and
the only way to know that before June is to simulate the calendar — which is what
ARUVI_TODAY exists for. These tests walk a teacher across a year boundary and pin the four
promises the founder made when he specified it:

  1. last year's plans stay readable, under their own year;
  2. this year starts empty — section attachments and pointers cleared;
  3. the class list (subjects/classes/sections/periods) carries forward untouched;
  4. notes stay with the plans they were written against.

Plus the two that keep it safe: nothing happens before the cutover date, and tapping
twice does nothing the second time.

Run standalone:  python3 tests/test_cutover.py     (also pytest-compatible)
"""
from __future__ import annotations

import os
import sys
import tempfile
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

_TMP_STATE = tempfile.mkdtemp(prefix="aruvi-test-cutover-")
os.environ.setdefault("ARUVI_STATE_DIR", _TMP_STATE)

from aruvi_core.adapters.year_cutover_file import YearCutoverFileImpl  # noqa: E402
from aruvi_core.ports import CutoverResult, YearCutover                # noqa: E402

PROFILE = {"subjects": [{
    "name": "Social Sciences",
    "grades": [{"grade": "IX", "sections": [{"tag": "9A", "sec": "A"},
                                            {"tag": "9B", "sec": "B"}],
                "durations": [50], "periods_per_week": 6,
                "ppw_by_duration": {"50": 6}, "ppw_anchor": 50}],
    "grids": [[[-1] * 6, [-1] * 6]],
    "budget": {"0": {"method": "periods", "value": 245}},
}]}


def test_year_arithmetic():
    n = YearCutoverFileImpl.next_year_id
    assert n("2026-27") == "2027-28"
    assert n("2027-28") == "2028-29"
    assert n("2099-00") == "2100-01"
    assert n("nonsense") == "nonsense", "a hand-edited year must never crash a session"
    s, e = YearCutoverFileImpl.year_bounds("2027-28")
    assert s == "2027-04-01" and e == "2028-03-31"
    assert YearCutoverFileImpl.cutover_date("2027-28") == date(2027, 6, 1)
    assert YearCutoverFileImpl.cutover_date("2027-28", "05-15") == date(2027, 5, 15)
    print("✓ Year arithmetic: next year, April bounds, configurable cutover date")


def test_adapter_satisfies_the_port():
    assert isinstance(YearCutoverFileImpl(None, None, None, None), YearCutover)
    print("✓ YearCutoverFileImpl satisfies the YearCutover protocol")


def _client(today: str):
    """A TestClient with the service's idea of 'today' overridden.

    NOTE the ordering trap this exposed while being written: a teacher's FIRST request
    bootstraps her year from the simulated date, so she must be created inside the year
    she is supposed to be finishing. Set the clock, then create her — not the reverse."""
    from fastapi.testclient import TestClient
    from api import main as api_main, config as api_config
    api_config.SIMULATED_TODAY = today
    return TestClient(api_main.app), api_main


def _set_today(today: str):
    """Move the clock without rebuilding the client."""
    from api import config as api_config
    api_config.SIMULATED_TODAY = today


def test_the_whole_june_walk():
    """★ The spec's "June works", start to finish, on a simulated calendar."""
    uid = "CutoverKumar"
    h = {"X-Aruvi-User": uid}

    # ── August 2026: she joins, so her year is 2026-27 ─────────────────────────
    c, api_main = _client("2026-08-01")
    c.post("/readiness", json={"subjects": PROFILE["subjects"]}, headers=h)
    c.post("/plans-prepared", json={"subject": "social_sciences", "grade": "IX",
                                    "filename": "ch_01_canonical.json", "periods": 21},
           headers=h)
    c.post("/section-state", json={"section_key": "social_sciences_ix_9A",
                                   "chapter": "ch_01_canonical.json", "unit_index": 7},
           headers=h)
    c.post("/plan-notes", json={"subject": "social_sciences", "grade": "IX",
                                "chapter": "1", "text": "9A needed two extra periods.",
                                "updated_at": "2027-04-20T10:00:00+00:00"}, headers=h)

    # ── April 2027: still her year; the next one is not on offer ───────────────
    _set_today("2027-04-20")
    y = c.get("/academic-year", headers=h).json()
    assert y["current_year"] == "2026-27" and y["next_year"] == "2027-28"
    assert y["cleanup_due"] is False, "April is not June — the year has not turned"
    assert y["cutover_date"] == "2027-06-01"

    # ── 1 June 2027: ARUVI ROLLS HER YEAR ITSELF (founder, 2026-08-26) ─────────
    # The year is Aruvi's boundary, not a preference: it turns on the date for everyone.
    # But her TRACKING is carried across, so nothing breaks mid-chapter.
    _set_today("2027-06-01")
    y = c.get("/academic-year", headers=h).json()
    assert y["current_year"] == "2027-28", "the year turns on the date, unasked"
    assert "2026-27" in y["prior_years"]
    assert y["cleanup_due"] is True, "her carried tracking is waiting on her"

    # Her bindings survived the roll — she can finish what she was part-way through.
    carried = c.get("/section-state", headers=h).json()["states"]
    assert carried["social_sciences_ix_9A"]["chapter"] == "ch_01_canonical.json"
    assert carried["social_sciences_ix_9A"]["unit_index"] == 7, "her place is kept"

    # And her card now says WHICH VERSION she is teaching: prepared last year, not this.
    plans = c.get("/plans/social_sciences/IX", headers=h).json()["plans"]
    ch1 = next(p for p in plans if p["filename"] == "ch_01_canonical.json")
    assert ch1["prepared_source_year"] == "2026-27", "the year stamp is derived"
    # …and it is NOT this year's work, which is what keeps it in the prior-year folder
    # instead of this year's list. (Setting prepared=True here once emptied the folder
    # and pulled every one of last year's lessons back into the main list.)
    assert ch1["prepared"] is False, "last year's plan belongs to last year's folder"

    # The clean-up is the only thing left, and it is hers alone.
    assert c.post("/academic-year/cutover", json={},
                  headers=h).status_code == 400, "confirmation required"

    # ── She confirms the fresh start ───────────────────────────────────────────
    r = c.post("/academic-year/cutover", json={"confirm": True}, headers=h).json()
    assert r["status"] == "cutover"
    assert r["closed_year"] == "2026-27" and r["opened_year"] == "2027-28"
    # Only 9A was ever tracked (9B exists in her profile but she never bound a chapter),
    # and clearing counts TRACKING, not sections owned — her profile is untouched.
    assert r["sections_cleared"] == 1, "the one tracked section cleared"
    assert r["plans_archived"] == 1

    # 1 · Last year's plans stay readable, under their own year.
    old = c.get("/plans-prepared?year_id=2026-27", headers=h).json()["prepared"]
    assert "social_sciences/IX/ch_01_canonical.json" in old

    # 2 · This year starts empty — attachments and pointers cleared.
    assert c.get("/plans-prepared", headers=h).json()["prepared"] == {}
    assert c.get("/section-state", headers=h).json()["states"] == {}

    # 3 · The class list carries forward untouched (readiness is NOT year-scoped).
    prof = c.get("/readiness", headers=h).json()["readiness"]["subjects"]
    assert [s["name"] for s in prof] == ["Social Sciences"]
    assert [x["tag"] for x in prof[0]["grades"][0]["sections"]] == ["9A", "9B"]
    assert prof[0]["grades"][0]["periods_per_week"] == 6

    # 4 · Notes stay with the plans they were written against.
    assert c.get("/plan-notes", headers=h).json()["notes"] == {}, "new year, no notes"
    old_notes = c.get("/plan-notes?year_id=2026-27", headers=h).json()["notes"]
    assert old_notes["social_sciences/ix/1"]["text"] == "9A needed two extra periods."

    # And the year status now reads as the new year, with the old one listed.
    y = c.get("/academic-year", headers=h).json()
    assert y["current_year"] == "2027-28"
    assert "2026-27" in y["prior_years"]
    assert y["cleanup_due"] is False, "she has started fresh; stop asking"
    print("✓ The June walk: offered on the date, hers to confirm, then last year "
          "readable · this year empty · class list carried · notes left behind")


def test_tapping_twice_is_safe():
    """"A teacher WILL tap twice" — administrative_architecture.md §Step 2."""
    uid = "TwiceKumar"
    h = {"X-Aruvi-User": uid}
    c, _ = _client("2026-08-01")                 # she joins in 2026-27 (see _client)
    c.post("/readiness", json={"subjects": PROFILE["subjects"]}, headers=h)
    c.post("/section-state", json={"section_key": "social_sciences_ix_9A",
                                   "chapter": "ch_01_canonical.json"}, headers=h)
    _set_today("2027-06-10")
    c.get("/academic-year", headers=h)           # the roll happens here, unasked
    first = c.post("/academic-year/cutover", json={"confirm": True}, headers=h).json()
    assert first["already_done"] is False and first["opened_year"] == "2027-28"

    # She works in the new year...
    c.post("/section-state", json={"section_key": "social_sciences_ix_9A",
                                   "chapter": "ch_02_canonical.json"}, headers=h)
    # ...then taps again.
    # THE POINT: she works in the new year, then taps again. A second clear would wipe
    # the tracking she has just started — so it must report already_done and do nothing.
    second = c.post("/academic-year/cutover", json={"confirm": True}, headers=h).json()
    assert second["already_done"] is True
    assert second["opened_year"] == "2027-28", "no third year invented"
    assert c.get("/section-state", headers=h).json()["states"], "second tap wiped nothing"
    print("✓ Tapping twice reports already_done and destroys nothing")


def test_simulated_date_is_visible_and_optional():
    """The override must be honest about itself, and harmless when malformed/unset."""
    from api import config as api_config
    c, _ = _client("2027-06-01")
    y = c.get("/academic-year", headers={"X-Aruvi-User": "FlagKumar"}).json()
    assert y["simulated"] is True and y["today"] == "2027-06-01"

    api_config.SIMULATED_TODAY = "not-a-date"       # ignored, never fatal
    y = c.get("/academic-year", headers={"X-Aruvi-User": "FlagKumar"}).json()
    assert y["today"] == date.today().isoformat()

    api_config.SIMULATED_TODAY = ""                  # production
    y = c.get("/academic-year", headers={"X-Aruvi-User": "FlagKumar"}).json()
    assert y["simulated"] is False and y["today"] == date.today().isoformat()
    print("✓ Simulated date reports itself, ignores nonsense, and is off by default")


if __name__ == "__main__":
    test_year_arithmetic()
    test_adapter_satisfies_the_port()
    test_the_whole_june_walk()
    test_tapping_twice_is_safe()
    test_simulated_date_is_visible_and_optional()
    print("\n✅ All cutover tests passed!")
