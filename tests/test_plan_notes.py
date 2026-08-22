"""
Tests for administrative-architecture Step 3: PlanNoteRepository (chapter notes),
its file adapter, and the /plan-notes API routes.

The rules under test (spec §2.4 + founder 2026-08-22):
  * one note per CHAPTER per academic year (key = subject/grade/chapter_number);
  * saving empty text IS deleting — no separate lifecycle, no version history;
  * anti-clobber: an older updated_at is refused (StaleNoteWrite / HTTP 409 carrying
    the newer copy), equal timestamps are accepted;
  * year + tenant isolation, like every other teaching-state repo.

Run standalone:  python3 tests/test_plan_notes.py     (also pytest-compatible)
"""
from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Throwaway state dir BEFORE importing api.main (see test_account.py).
_TMP_STATE = tempfile.mkdtemp(prefix="aruvi-test-state-")
os.environ.setdefault("ARUVI_STATE_DIR", _TMP_STATE)

from aruvi_core.ports import PlanNote, StaleNoteWrite  # noqa: E402
from aruvi_core.adapters.plan_note_repository_file import PlanNoteRepositoryFileImpl  # noqa: E402

T, U, Y = "Kumar1", "Kumar1", "2026-27"
KEY = "science/vii/3"


def _note(text, at="2026-08-22T10:00:00+00:00", key=KEY):
    return PlanNote(note_key=key, text=text, updated_at=at)


def test_save_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        repo = PlanNoteRepositoryFileImpl(tmp)
        repo.save(T, U, Y, _note("Bring the shipwreck cards."))
        got = repo.load(T, U, Y, KEY)
        assert got is not None and got.text == "Bring the shipwreck cards."
        assert repo.load(T, U, Y, "science/vii/4") is None
        assert set(repo.load_all(T, U, Y)) == {KEY}
        print("✓ Note save/load roundtrip")


def test_empty_text_deletes():
    """Editing to empty IS the delete flow — the note vanishes, no tombstone."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = PlanNoteRepositoryFileImpl(tmp)
        repo.save(T, U, Y, _note("something"))
        repo.save(T, U, Y, _note("   ", at="2026-08-22T11:00:00+00:00"))
        assert repo.load(T, U, Y, KEY) is None
        assert repo.load_all(T, U, Y) == {}
        # Deleting a note that never existed: quiet no-op, never an error.
        repo.save(T, U, Y, _note("", key="science/vii/9"))
        print("✓ Saving empty text deletes the note")


def test_stale_write_refused_equal_accepted():
    with tempfile.TemporaryDirectory() as tmp:
        repo = PlanNoteRepositoryFileImpl(tmp)
        repo.save(T, U, Y, _note("laptop edit", at="2026-08-22T11:00:00+00:00"))
        try:
            repo.save(T, U, Y, _note("stale phone edit", at="2026-08-22T09:00:00+00:00"))
            assert False, "expected StaleNoteWrite"
        except StaleNoteWrite:
            pass
        assert repo.load(T, U, Y, KEY).text == "laptop edit", "newer copy survived"
        # Equal timestamp: idempotent re-save, accepted.
        repo.save(T, U, Y, _note("laptop edit v2", at="2026-08-22T11:00:00+00:00"))
        assert repo.load(T, U, Y, KEY).text == "laptop edit v2"
        print("✓ Older write refused, newer kept, equal accepted")


def test_no_history_anywhere():
    """After edits, the store holds exactly one text per key — nothing to recover."""
    import json
    with tempfile.TemporaryDirectory() as tmp:
        repo = PlanNoteRepositoryFileImpl(tmp)
        repo.save(T, U, Y, _note("first", at="2026-08-22T10:00:00+00:00"))
        repo.save(T, U, Y, _note("second", at="2026-08-22T11:00:00+00:00"))
        raw = json.load(open(repo._path(T, U, Y)))
        assert raw == {KEY: {"text": "second", "updated_at": "2026-08-22T11:00:00+00:00"}}
        assert "first" not in json.dumps(raw)
        print("✓ No version history exists on disk")


def test_year_and_tenant_isolation():
    with tempfile.TemporaryDirectory() as tmp:
        repo = PlanNoteRepositoryFileImpl(tmp)
        repo.save(T, U, "2026-27", _note("this year"))
        assert repo.load_all(T, U, "2027-28") == {}, "new year starts with empty notes"
        repo.save(T, U, "2027-28", _note("next year", at="2027-06-01T00:00:00+00:00"))
        assert repo.load(T, U, "2026-27", KEY).text == "this year", "old note stays put"
        assert repo.load_all("Priya2", "Priya2", "2026-27") == {}
        repo.delete(T, U, "2026-27", KEY)
        assert repo.load(T, U, "2026-27", KEY) is None
        assert repo.load(T, U, "2027-28", KEY).text == "next year"
        print("✓ Notes are isolated by year and tenant")


def test_api_routes():
    """End-to-end through FastAPI: save → list → stale 409 with the newer copy →
    empty-text delete. Uses the throwaway state dir set at import."""
    from fastapi.testclient import TestClient
    from api.main import app

    c = TestClient(app)
    h = {"X-Aruvi-User": "NotesKumar"}
    body = {"subject": "science", "grade": "vii", "chapter": "3",
            "text": "Bring the cards.", "updated_at": "2026-08-22T10:00:00+00:00"}
    assert c.post("/plan-notes", json=body, headers=h).json()["status"] == "saved"
    notes = c.get("/plan-notes", headers=h).json()["notes"]
    assert notes["science/vii/3"]["text"] == "Bring the cards."
    # Stale write → 409 carrying the newer copy.
    r = c.post("/plan-notes", json={**body, "text": "old phone",
                                    "updated_at": "2026-08-22T09:00:00+00:00"}, headers=h)
    assert r.status_code == 409
    assert r.json()["detail"]["note"]["text"] == "Bring the cards."
    # Empty text deletes.
    r = c.post("/plan-notes", json={**body, "text": "",
                                    "updated_at": "2026-08-22T11:00:00+00:00"}, headers=h)
    assert r.json()["status"] == "deleted"
    assert c.get("/plan-notes", headers=h).json()["notes"] == {}
    # Traversal-ish chapter identity is rejected.
    assert c.post("/plan-notes", json={**body, "chapter": "../evil"},
                  headers=h).status_code == 400
    # Another teacher sees nothing.
    assert c.get("/plan-notes", headers={"X-Aruvi-User": "OtherKumar"}).json()["notes"] == {}
    print("✓ /plan-notes routes: save, list, 409-with-newer, delete, isolation")


if __name__ == "__main__":
    test_save_load_roundtrip()
    test_empty_text_deletes()
    test_stale_write_refused_equal_accepted()
    test_no_history_anywhere()
    test_year_and_tenant_isolation()
    test_api_routes()
    print("\n✅ All plan-note tests passed!")
