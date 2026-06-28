"""
Readiness persistence test — the teaching profile survives a session cut.

Covers the file-backed ReadinessRepository (the seam Phase 4 swaps for Supabase):
  - round-trip: save → load returns the canonical subjects[] verbatim
  - the denormalized active-subject projection is NEVER written to disk
    (CLOUD_DATA_MODEL.md §2.1 / §5 invariant), even if the caller sends it
  - tenant/user keying isolates profiles (the multi-tenancy guarantee, stubbed today)
  - clear removes it; load on a fresh teacher returns None ("not ready")
  - id slugging defends against path traversal

Run standalone:  python3 tests/test_readiness.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.adapters.readiness_repository_file import (  # noqa: E402
    ReadinessRepositoryFileImpl,
)

# A realistic canonical payload — one subject, two grades, sections + durations + grid + budget.
SUBJECTS = [
    {
        "name": "Science",
        "durations": [45, 60],
        "grades": [
            {"grade": "VI", "sections": [{"tag": "6A", "sec": "A"}, {"tag": "6B", "sec": "B"}],
             "durations": [45]},
            {"grade": "VII", "sections": [{"tag": "7A", "sec": "A"}], "durations": [45, 60]},
        ],
        "grids": [[[0, -1, 0, -1, 0, -1]], [[0, 1, -1, 0, -1, -1]]],
        "budget": {"0": {"method": "weeks", "value": 36}, "1": {"method": "periods", "value": 210}},
    }
]

# What a careless frontend might POST: canonical subjects[] PLUS the denormalized projection.
PAYLOAD_WITH_PROJECTION = {
    "subjects": SUBJECTS,
    "activeSubjectIndex": 0,
    "subject": "Science",
    "grades": SUBJECTS[0]["grades"],
    "durations": [[45], [45, 60]],
    "grids": SUBJECTS[0]["grids"],
    "budget": SUBJECTS[0]["budget"],
}

PROJECTION_KEYS = ("subject", "grades", "grids", "durations", "budget", "activeSubjectIndex")


def _repo(d):
    return ReadinessRepositoryFileImpl(d)


def test_round_trip():
    with tempfile.TemporaryDirectory() as d:
        repo = _repo(d)
        assert repo.load_profile("local", "local") is None, "fresh teacher should be not-ready"
        repo.save_profile("local", "local", {"subjects": SUBJECTS})
        loaded = repo.load_profile("local", "local")
        assert loaded is not None
        assert loaded["subjects"] == SUBJECTS, "subjects[] must round-trip verbatim"
        assert loaded["tenant_id"] == "local" and loaded["user_id"] == "local"
        assert "updated_at" in loaded
    print("✓ round-trip preserves canonical subjects[]")


def test_projection_never_persisted():
    with tempfile.TemporaryDirectory() as d:
        repo = _repo(d)
        repo.save_profile("local", "local", PAYLOAD_WITH_PROJECTION)
        # Inspect the raw file — the projection keys must be absent on disk.
        path = repo._profile_path("local", "local")
        raw = json.load(open(path))
        for k in PROJECTION_KEYS:
            assert k not in raw, f"projection key {k!r} must not be persisted (CLOUD_DATA_MODEL §5)"
        assert raw["subjects"] == SUBJECTS, "canonical subjects[] still stored intact"
    print("✓ denormalized active-subject projection is stripped before disk")


def test_tenant_user_isolation():
    with tempfile.TemporaryDirectory() as d:
        repo = _repo(d)
        repo.save_profile("schoolA", "teacher1", {"subjects": SUBJECTS})
        # A different user / tenant sees nothing — the multi-tenancy guarantee.
        assert repo.load_profile("schoolA", "teacher2") is None
        assert repo.load_profile("schoolB", "teacher1") is None
        assert repo.load_profile("schoolA", "teacher1")["subjects"] == SUBJECTS
    print("✓ profiles are isolated by tenant_id + user_id")


def test_clear():
    with tempfile.TemporaryDirectory() as d:
        repo = _repo(d)
        repo.save_profile("local", "local", {"subjects": SUBJECTS})
        assert repo.load_profile("local", "local") is not None
        repo.clear_profile("local", "local")
        assert repo.load_profile("local", "local") is None
        repo.clear_profile("local", "local")  # no-op, must not raise
    print("✓ clear erases the profile; re-clear is a safe no-op")


def test_id_slug_safety():
    with tempfile.TemporaryDirectory() as d:
        repo = _repo(d)
        # A malicious id must not escape the readiness/ directory.
        repo.save_profile("../../etc", "../../../root", {"subjects": SUBJECTS})
        path = repo._profile_path("../../etc", "../../../root").resolve()
        base = (repo.readiness_dir).resolve()
        assert str(path).startswith(str(base)), "slugged path must stay under readiness/"
    print("✓ tenant/user ids are slugged — no path traversal")


def test_empty_subjects_is_not_ready():
    with tempfile.TemporaryDirectory() as d:
        repo = _repo(d)
        repo.save_profile("local", "local", {"subjects": []})
        loaded = repo.load_profile("local", "local")
        # A file exists but with no subjects — the API derives ready=False from this.
        assert loaded["subjects"] == []
    print("✓ empty subjects[] persists but reads as not-ready")


if __name__ == "__main__":
    test_round_trip()
    test_projection_never_persisted()
    test_tenant_user_isolation()
    test_clear()
    test_id_slug_safety()
    test_empty_subjects_is_not_ready()
    print("\nAll readiness persistence tests passed.")
