"""
API smoke test (FastAPI TestClient) — exercises the bridge end-to-end against local data.

Run standalone:  python3 tests/test_api.py
"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi.testclient import TestClient  # noqa: E402

from api.main import app  # noqa: E402

client = TestClient(app)


def test_health_and_subjects():
    assert client.get("/health").json() == {"status": "ok"}
    subs = client.get("/subjects").json()["subjects"]
    assert set(subs) >= {"science", "english", "mathematics", "social_sciences", "the_world_around_us"}


def test_chapters_and_allocate():
    ch = client.get("/subjects/social_sciences/vii/chapters").json()
    assert len(ch["chapters"]) == 12
    assert all("weight" in c for c in ch["chapters"])

    alloc = client.post("/subjects/social_sciences/vii/allocate", json={"total_periods": 50}).json()
    assert sum(a["periods"] for a in alloc["allocations"]) == 50


def test_plan_view_returns_view_model():
    plans = client.get("/plans/science/vii").json()["plans"]
    assert plans, "expected at least one saved science plan"
    fn = plans[0]["filename"]
    view = client.get(f"/plans/science/vii/{fn}/view").json()["view"]
    # canonical view model shape, structure preserved
    assert "lesson_plan" in view and "assessment" in view
    assert view["lesson_plan"]["groups"]
    assert view["lesson_plan"]["groups"][0]["type"] == "progression_stage"


def test_generate_is_deferred():
    r = client.post("/subjects/science/vii/generate")
    assert r.status_code == 501 and r.json()["status"] == "deferred"


if __name__ == "__main__":
    test_health_and_subjects()
    test_chapters_and_allocate()
    test_plan_view_returns_view_model()
    test_generate_is_deferred()
    print("OK — API: subjects, chapters+allocate (sum exact), plan view returns the canonical "
          "view model, generate correctly deferred.")
