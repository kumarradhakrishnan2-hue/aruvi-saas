"""
Tests for administrative-architecture Step 1: the AcademicYear record, its file adapter,
and the API's server-side year resolution (bootstrap on first touch).

Run standalone:  python3 tests/test_academic_year.py     (also pytest-compatible)
"""
from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Throwaway state dir BEFORE importing api.main (see test_account.py).
_TMP_STATE = tempfile.mkdtemp(prefix="aruvi-test-state-")
os.environ.setdefault("ARUVI_STATE_DIR", _TMP_STATE)

from aruvi_core.ports import AcademicYear  # noqa: E402
from aruvi_core.adapters.academic_year_repository_file import AcademicYearRepositoryFileImpl  # noqa: E402

T, U = "Kumar1", "Kumar1"


def _year(yid="2026-27", current=True):
    start = int(yid[:4])
    return AcademicYear(year_id=yid, starts_on=f"{start}-04-01",
                        ends_on=f"{start + 1}-03-31", is_current=current)


def test_empty_store():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AcademicYearRepositoryFileImpl(tmp)
        assert repo.current(T, U) is None
        assert repo.list_years(T, U) == []
        print("✓ Empty store: no current year, empty list")


def test_open_and_current():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AcademicYearRepositoryFileImpl(tmp)
        repo.open_year(T, U, _year("2026-27"))
        cur = repo.current(T, U)
        assert cur is not None and cur.year_id == "2026-27" and cur.is_current
        print("✓ open_year + current roundtrip")


def test_one_current_always():
    """Opening a new current year clears the old flag; set_current flips it back."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = AcademicYearRepositoryFileImpl(tmp)
        repo.open_year(T, U, _year("2026-27"))
        repo.open_year(T, U, _year("2027-28"))
        assert repo.current(T, U).year_id == "2027-28"
        flags = [y.is_current for y in repo.list_years(T, U)]
        assert flags.count(True) == 1, "exactly one current year, always"
        repo.set_current(T, U, "2026-27")
        assert repo.current(T, U).year_id == "2026-27"
        assert [y.is_current for y in repo.list_years(T, U)].count(True) == 1
        print("✓ Exactly one current year is maintained")


def test_open_is_idempotent_and_ordered():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AcademicYearRepositoryFileImpl(tmp)
        repo.open_year(T, U, _year("2027-28"))
        repo.open_year(T, U, _year("2026-27"))
        repo.open_year(T, U, _year("2026-27"))  # re-open: update, not duplicate
        years = repo.list_years(T, U)
        assert [y.year_id for y in years] == ["2026-27", "2027-28"], "oldest first"
        print("✓ open_year is idempotent; listing is oldest-first")


def test_set_current_unknown_year_raises():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AcademicYearRepositoryFileImpl(tmp)
        repo.open_year(T, U, _year("2026-27"))
        try:
            repo.set_current(T, U, "2031-32")
            assert False, "expected ValueError for a never-opened year"
        except ValueError:
            pass
        print("✓ set_current refuses a never-opened year")


def test_tenant_isolation():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AcademicYearRepositoryFileImpl(tmp)
        repo.open_year("Kumar1", "Kumar1", _year("2026-27"))
        assert repo.current("Priya2", "Priya2") is None
        print("✓ Year stores are isolated by tenant + user")


def test_api_resolve_year_bootstraps():
    """_resolve_year returns the explicit param when given, else bootstraps the
    April-anchored default year on first touch and reuses it afterwards."""
    from api import main as api_main

    assert api_main._resolve_year("Kumar88", "Kumar88", "2030-31") == "2030-31"
    y1 = api_main._resolve_year("Kumar88", "Kumar88")
    assert api_main.academic_year_repo.current("Kumar88", "Kumar88").year_id == y1
    assert api_main._resolve_year("Kumar88", "Kumar88") == y1, "stable across calls"
    # The default label matches the April-anchored formula.
    dflt = api_main._default_academic_year()
    assert dflt.year_id == y1 and dflt.starts_on.endswith("-04-01")
    print("✓ API year resolution bootstraps once and stays stable")


if __name__ == "__main__":
    test_empty_store()
    test_open_and_current()
    test_one_current_always()
    test_open_is_idempotent_and_ordered()
    test_set_current_unknown_year_raises()
    test_tenant_isolation()
    test_api_resolve_year_bootstraps()
    print("\n✅ All academic-year tests passed!")
