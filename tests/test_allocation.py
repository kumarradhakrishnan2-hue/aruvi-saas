"""
Parity tests for the Persistent Annual Allocation Register (file adapter).

The register is per-user/tenant STATE keyed by (tenant_id, user_id, subject, grade), and
must maintain cumulative curriculum-planning state:
  - First save: initialize register with chapters.
  - Second save: merge new chapters, preserve old.
  - Overwrite save: replace allocation for chapters that appear in both saves.
  - Tenant isolation: two teachers' registers for the same subject·grade are independent.

Each value is a full AllocationRecord ({chapter_title, weight, periods_by_duration,
total_periods, total_minutes}) — the "redraw-ready" schema the API/engine actually use.

Run standalone:  python3 tests/test_allocation.py     (also pytest-compatible)
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.adapters.allocation_repository_file import AllocationRepositoryFileImpl  # noqa: E402

# Default identity used by most tests (auth stubbed → tenant == user).
T, U = "Kumar1", "Kumar1"


def _rec(periods, minutes_per=45, title="", weight=0):
    """Build a minimal AllocationRecord for `periods` periods at one duration."""
    return {
        "chapter_title": title,
        "weight": weight,
        "periods_by_duration": {str(minutes_per): periods},
        "total_periods": periods,
        "total_minutes": periods * minutes_per,
    }


def test_first_allocation_initializes_register():
    """First save to empty register: chapters 1-4 are allocated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        allocation = {"1": _rec(5), "2": _rec(6), "3": _rec(4), "4": _rec(7)}
        repo.save_allocation(T, U, "science", "vii", allocation)
        register = repo.load_register(T, U, "science", "vii")
        assert register == allocation, f"Expected {allocation}, got {register}"
        print("✓ First allocation initializes register correctly")


def test_second_allocation_merges_new_chapters():
    """Second save: allocate chapters 5-7 while preserving chapters 1-4."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        first = {"1": _rec(5), "2": _rec(6), "3": _rec(4), "4": _rec(7)}
        repo.save_allocation(T, U, "science", "vii", first)
        second = {"5": _rec(8), "6": _rec(5), "7": _rec(6)}
        repo.save_allocation(T, U, "science", "vii", second)
        register = repo.load_register(T, U, "science", "vii")
        assert register == {**first, **second}
        print("✓ Second allocation merges new chapters while preserving old")


def test_overwrite_allocation_replaces_for_existing_chapters():
    """Overwrite save: chapter 4 was 7 periods, re-allocate to 5."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        first = {"1": _rec(5), "2": _rec(6), "3": _rec(4), "4": _rec(7)}
        repo.save_allocation(T, U, "science", "vii", first)
        repo.save_allocation(T, U, "science", "vii", {"4": _rec(5)})
        register = repo.load_register(T, U, "science", "vii")
        assert register["4"]["total_periods"] == 5 and register["1"]["total_periods"] == 5
        print("✓ Overwrite allocation replaces existing chapters correctly")


def test_summary_reflects_merged_state():
    """Summary should always reflect the cumulative register state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        repo.save_allocation(T, U, "science", "vii", {"1": _rec(5), "2": _rec(6), "3": _rec(4)})
        s1 = repo.get_summary(T, U, "science", "vii")
        assert s1.chapters_allocated == 3
        assert s1.total_planned_periods == 15
        assert s1.total_planned_time_minutes == 15 * 45
        repo.save_allocation(T, U, "science", "vii", {"4": _rec(7), "5": _rec(8)})
        s2 = repo.get_summary(T, U, "science", "vii")
        assert s2.chapters_allocated == 5
        assert s2.total_planned_periods == 30
        print("✓ Summary reflects cumulative merged state")


def test_empty_register_summary():
    """Summary for a non-existent register should have zeros."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        s = repo.get_summary(T, U, "science", "vii")
        assert s.chapters_allocated == 0 and s.total_planned_periods == 0
        print("✓ Empty register summary is all zeros")


def test_persistence_across_instances():
    """Data persists across different repo instances."""
    tmpdir = tempfile.mkdtemp()
    try:
        repo1 = AllocationRepositoryFileImpl(tmpdir)
        alloc = {"1": _rec(5), "2": _rec(6)}
        repo1.save_allocation(T, U, "science", "vii", alloc)
        repo2 = AllocationRepositoryFileImpl(tmpdir)
        assert repo2.load_register(T, U, "science", "vii") == alloc
        print("✓ Data persists across repository instances")
    finally:
        shutil.rmtree(tmpdir)


def test_multiple_subjects_and_grades():
    """Separate registers for different subjects/grades, same teacher."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        repo.save_allocation(T, U, "science", "vii", {"1": _rec(5)})
        repo.save_allocation(T, U, "science", "vi", {"1": _rec(4)})
        repo.save_allocation(T, U, "mathematics", "vii", {"1": _rec(7)})
        assert repo.load_register(T, U, "science", "vii")["1"]["total_periods"] == 5
        assert repo.load_register(T, U, "science", "vi")["1"]["total_periods"] == 4
        assert repo.load_register(T, U, "mathematics", "vii")["1"]["total_periods"] == 7
        print("✓ Separate registers for different subjects/grades")


def test_tenant_isolation():
    """Two teachers' registers for the SAME subject·grade are independent."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        repo.save_allocation("Kumar1", "Kumar1", "science", "vii", {"1": _rec(5)})
        repo.save_allocation("Priya2", "Priya2", "science", "vii", {"1": _rec(9)})
        k = repo.load_register("Kumar1", "Kumar1", "science", "vii")
        p = repo.load_register("Priya2", "Priya2", "science", "vii")
        assert k["1"]["total_periods"] == 5, "Kumar1 must keep his own allocation"
        assert p["1"]["total_periods"] == 9, "Priya2 has an independent allocation"
        # A third teacher sees nothing.
        assert repo.load_register("Anya3", "Anya3", "science", "vii") == {}
        print("✓ Allocation registers are isolated by tenant + user")


def test_clear_is_scoped_and_safe():
    """clear_register erases only that teacher's register; re-clear is a no-op."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)
        repo.save_allocation("Kumar1", "Kumar1", "science", "vii", {"1": _rec(5)})
        repo.save_allocation("Priya2", "Priya2", "science", "vii", {"1": _rec(9)})
        repo.clear_register("Kumar1", "Kumar1", "science", "vii")
        assert repo.load_register("Kumar1", "Kumar1", "science", "vii") == {}
        assert repo.load_register("Priya2", "Priya2", "science", "vii")["1"]["total_periods"] == 9
        repo.clear_register("Kumar1", "Kumar1", "science", "vii")  # no-op, must not raise
        print("✓ clear is tenant-scoped and idempotent")


if __name__ == "__main__":
    test_first_allocation_initializes_register()
    test_second_allocation_merges_new_chapters()
    test_overwrite_allocation_replaces_for_existing_chapters()
    test_summary_reflects_merged_state()
    test_empty_register_summary()
    test_persistence_across_instances()
    test_multiple_subjects_and_grades()
    test_tenant_isolation()
    test_clear_is_scoped_and_safe()
    print("\n✅ All allocation tests passed!")
