"""
Tests for the Step 0+1 one-shot migration (aruvi-scripts/migrate_step01.py):
legacy {kind}/{tenant}/{user}/<files> trees move into {user}/{year}/, account and
academic-year records are created for every discovered identity, and re-running is a
complete no-op (idempotency — the promise that makes the script safe to run twice).

Run standalone:  python3 tests/test_migration.py     (also pytest-compatible)
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys
import tempfile
from pathlib import Path

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, _ROOT)

# Load the script as a module (its folder name "aruvi-scripts" is not importable).
_spec = importlib.util.spec_from_file_location(
    "migrate_step01", os.path.join(_ROOT, "aruvi-scripts", "migrate_step01.py"))
mig = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(mig)

YEAR = "2026-27"


def _legacy_tree(root: Path) -> None:
    """A miniature of the real pre-migration dev data: three kinds populated for kumar1,
    prepared_plans only for kumar9 (the stranded-identity case), readiness un-scoped."""
    (root / "section_state" / "kumar1" / "kumar1").mkdir(parents=True)
    (root / "section_state" / "kumar1" / "kumar1" / "state.json").write_text(
        json.dumps({"science_vii_7A": {"chapter": "3", "unit_index": 5, "done": False}}))
    (root / "allocations" / "kumar1" / "kumar1" / "science" / "vii").mkdir(parents=True)
    (root / "allocations" / "kumar1" / "kumar1" / "science" / "vii" / "allocation.json"
     ).write_text(json.dumps({"1": {"total_periods": 5}}))
    (root / "prepared_plans" / "kumar9" / "kumar9").mkdir(parents=True)
    (root / "prepared_plans" / "kumar9" / "kumar9" / "prepared.json").write_text(
        json.dumps({"science/vii/ch_03.json": "2026-07-05T00:00:00+00:00"}))
    (root / "readiness" / "kumar1" / "kumar1").mkdir(parents=True)
    (root / "readiness" / "kumar1" / "kumar1" / "profile.json").write_text(
        json.dumps({"subjects": [{"name": "Science"}]}))
    (root / "section_state" / ".DS_Store").write_text("junk")


def _run(root: Path) -> list:
    report: list = []
    mig.migrate_year_scope(root, YEAR, report)
    for tenant, user in sorted(mig.discover_identities(root)):
        mig.ensure_records(root, tenant, user, YEAR, report)
    return report


def test_migration_moves_and_creates():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _legacy_tree(root)
        report = _run(root)
        assert report, "first run must do work"

        # Year-scoped kinds moved under {year}/ with contents intact.
        moved = root / "section_state" / "kumar1" / "kumar1" / YEAR / "state.json"
        assert moved.exists()
        assert json.loads(moved.read_text())["science_vii_7A"]["unit_index"] == 5
        assert not (root / "section_state" / "kumar1" / "kumar1" / "state.json").exists()
        assert (root / "allocations" / "kumar1" / "kumar1" / YEAR / "science" / "vii"
                / "allocation.json").exists()
        assert (root / "prepared_plans" / "kumar9" / "kumar9" / YEAR / "prepared.json").exists()

        # Readiness is NOT year-scoped — untouched in place.
        assert (root / "readiness" / "kumar1" / "kumar1" / "profile.json").exists()

        # Accounts + years created for BOTH identities (kumar9 found via prepared only).
        for who in ("kumar1", "kumar9"):
            acct = json.loads((root / "accounts" / who / who / "account.json").read_text())
            assert acct["account_id"] == who and acct["tenant_id"] == who
            years = json.loads((root / "academic_years" / who / who / "years.json").read_text())
            assert years["years"][0]["year_id"] == YEAR and years["years"][0]["is_current"]
        print("✓ Migration moves teaching state and creates account/year records")


def test_migration_is_idempotent():
    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _legacy_tree(root)
        _run(root)
        snapshot = sorted(str(p.relative_to(root)) for p in root.rglob("*"))
        report2 = _run(root)
        assert report2 == [], f"second run must be a no-op, got: {report2}"
        assert sorted(str(p.relative_to(root)) for p in root.rglob("*")) == snapshot
        print("✓ Second run is a complete no-op")


def test_migrated_tree_is_what_adapters_read():
    """The moved files land exactly where the year-scoped adapters now look."""
    from aruvi_core.adapters.section_state_repository_file import SectionStateRepositoryFileImpl
    from aruvi_core.adapters.allocation_repository_file import AllocationRepositoryFileImpl
    from aruvi_core.adapters.prepared_plans_repository_file import PreparedPlansRepositoryFileImpl

    with tempfile.TemporaryDirectory() as tmp:
        root = Path(tmp)
        _legacy_tree(root)
        _run(root)
        assert SectionStateRepositoryFileImpl(tmp).load_all(
            "kumar1", "kumar1", YEAR)["science_vii_7A"]["chapter"] == "3"
        assert AllocationRepositoryFileImpl(tmp).load_register(
            "kumar1", "kumar1", YEAR, "science", "vii")["1"]["total_periods"] == 5
        assert "science/vii/ch_03.json" in PreparedPlansRepositoryFileImpl(tmp).load_all(
            "kumar9", "kumar9", YEAR)
        print("✓ Adapters read the migrated data at the new addresses")


def test_default_year_formula():
    from datetime import date
    assert mig.default_year_id(date(2026, 8, 22)) == "2026-27"
    assert mig.default_year_id(date(2027, 2, 1)) == "2026-27", "Jan–Mar belongs to prior April"
    assert mig.default_year_id(date(2027, 4, 1)) == "2027-28"
    print("✓ April-anchored year label formula")


if __name__ == "__main__":
    test_migration_moves_and_creates()
    test_migration_is_idempotent()
    test_migrated_tree_is_what_adapters_read()
    test_default_year_formula()
    print("\n✅ All migration tests passed!")
