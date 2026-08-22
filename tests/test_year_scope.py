"""
Cross-year isolation tests for the year-scoped repositories (Step 1): section state,
plan archive, prepared plans. (Allocations are covered in test_allocation.py.)

The Step-1 guarantee under test: two academic years never see each other's teaching
state, so cutover is a folder boundary — never a data rewrite.

Run standalone:  python3 tests/test_year_scope.py     (also pytest-compatible)
"""
from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.adapters.section_state_repository_file import SectionStateRepositoryFileImpl  # noqa: E402
from aruvi_core.adapters.plan_archive_repository_file import PlanArchiveRepositoryFileImpl  # noqa: E402
from aruvi_core.adapters.prepared_plans_repository_file import PreparedPlansRepositoryFileImpl  # noqa: E402

T, U = "Kumar1", "Kumar1"
Y1, Y2 = "2026-27", "2027-28"
KEY = "science/vii/ch_03_plan.json"


def test_section_state_year_isolation():
    with tempfile.TemporaryDirectory() as tmp:
        repo = SectionStateRepositoryFileImpl(tmp)
        repo.save_one(T, U, Y1, "science_vii_7A", "3", 5, False)
        repo.save_one(T, U, Y2, "science_vii_7A", "1", 0, False)
        assert repo.load_all(T, U, Y1)["science_vii_7A"]["chapter"] == "3"
        assert repo.load_all(T, U, Y2)["science_vii_7A"]["chapter"] == "1"
        # clear_all is year-scoped: wiping the new year leaves the old year's archive.
        repo.clear_all(T, U, Y2)
        assert repo.load_all(T, U, Y2) == {}
        assert repo.load_all(T, U, Y1)["science_vii_7A"]["unit_index"] == 5
        # delete_one likewise.
        repo.delete_one(T, U, Y1, "science_vii_7A")
        assert repo.load_all(T, U, Y1) == {}
        print("✓ Section state is isolated by academic year")


def test_plan_archive_year_isolation():
    with tempfile.TemporaryDirectory() as tmp:
        repo = PlanArchiveRepositoryFileImpl(tmp)
        repo.archive(T, U, Y1, KEY)
        assert KEY in repo.load_all(T, U, Y1)
        assert repo.load_all(T, U, Y2) == {}, "the new year starts unarchived"
        repo.restore(T, U, Y2, KEY)  # cross-year restore is a no-op, not a leak
        assert KEY in repo.load_all(T, U, Y1)
        repo.restore(T, U, Y1, KEY)
        assert repo.load_all(T, U, Y1) == {}
        print("✓ Plan archive is isolated by academic year")


def test_prepared_plans_year_isolation():
    with tempfile.TemporaryDirectory() as tmp:
        repo = PreparedPlansRepositoryFileImpl(tmp)
        repo.mark(T, U, Y1, KEY, 16)
        assert repo.load_all(T, U, Y1)[KEY]["periods"] == 16
        assert repo.load_all(T, U, Y2) == {}, "the new year's My Lessons starts fresh"
        repo.mark(T, U, Y2, KEY, 21)
        assert repo.load_all(T, U, Y1)[KEY]["periods"] == 16, "old year untouched"
        assert repo.load_all(T, U, Y2)[KEY]["periods"] == 21
        print("✓ Prepared register is isolated by academic year")


def test_cross_tenant_with_distinct_tenant_user():
    """Belt-and-braces: year scoping must not weaken tenant isolation, including when
    tenant_id != user_id (possible for the first time after Step 0)."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = PreparedPlansRepositoryFileImpl(tmp)
        repo.mark("school9", "teacherA", Y1, KEY, 10)
        assert repo.load_all("school9", "teacherB", Y1) == {}
        assert repo.load_all("teacherA", "teacherA", Y1) == {}
        assert repo.load_all("school9", "teacherA", Y1)[KEY]["periods"] == 10
        print("✓ Tenant/user isolation holds under year scoping")


if __name__ == "__main__":
    test_section_state_year_isolation()
    test_plan_archive_year_isolation()
    test_prepared_plans_year_isolation()
    test_cross_tenant_with_distinct_tenant_user()
    print("\n✅ All year-scope tests passed!")
