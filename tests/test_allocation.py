"""
Parity tests for allocation merge semantics in the Persistent Annual Allocation Register.

The register must maintain cumulative curriculum-planning state:
  - First save: initialize register with chapters.
  - Second save: merge new chapters, preserve old.
  - Overwrite save: replace allocation for chapters that appear in both saves.

Run standalone:  python3 tests/test_allocation.py     (also pytest-compatible)
"""
from __future__ import annotations

import json
import os
import shutil
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.adapters.allocation_repository_file import AllocationRepositoryFileImpl  # noqa: E402
from aruvi_core.ports import AllocationSummary  # noqa: E402


def test_first_allocation_initializes_register():
    """First save to empty register: chapters 1-4 are allocated."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)

        # First allocation
        allocation = {"1": 5, "2": 6, "3": 4, "4": 7}
        repo.save_allocation("science", "vii", allocation)

        # Load and verify
        register = repo.load_register("science", "vii")
        assert register == allocation, f"Expected {allocation}, got {register}"
        print("✓ First allocation initializes register correctly")


def test_second_allocation_merges_new_chapters():
    """Second save: allocate chapters 5-7 while preserving chapters 1-4."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)

        # First allocation: chapters 1-4
        first_alloc = {"1": 5, "2": 6, "3": 4, "4": 7}
        repo.save_allocation("science", "vii", first_alloc)

        # Second allocation: chapters 5-7 (new chapters)
        second_alloc = {"5": 8, "6": 5, "7": 6}
        repo.save_allocation("science", "vii", second_alloc)

        # Load and verify: all chapters present, original allocations preserved
        register = repo.load_register("science", "vii")
        expected = {**first_alloc, **second_alloc}
        assert register == expected, f"Expected {expected}, got {register}"
        print("✓ Second allocation merges new chapters while preserving old")


def test_overwrite_allocation_replaces_for_existing_chapters():
    """Overwrite save: chapter 4 was originally 7 periods, re-allocate to 5."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)

        # First allocation: chapter 4 = 7 periods
        first_alloc = {"1": 5, "2": 6, "3": 4, "4": 7}
        repo.save_allocation("science", "vii", first_alloc)

        # Overwrite allocation: chapter 4 = 5 periods
        overwrite_alloc = {"4": 5}
        repo.save_allocation("science", "vii", overwrite_alloc)

        # Load and verify: chapter 4 overwritten, others preserved
        register = repo.load_register("science", "vii")
        expected = {"1": 5, "2": 6, "3": 4, "4": 5}
        assert register == expected, f"Expected {expected}, got {register}"
        print("✓ Overwrite allocation replaces existing chapters correctly")


def test_mixed_overwrite_and_new_chapters():
    """Mixed save: overwrite chapter 2, add new chapter 8."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)

        # First allocation: chapters 1-4
        first_alloc = {"1": 5, "2": 6, "3": 4, "4": 7}
        repo.save_allocation("science", "vii", first_alloc)

        # Mixed save: overwrite chapter 2 and add chapter 8
        mixed_alloc = {"2": 8, "8": 9}
        repo.save_allocation("science", "vii", mixed_alloc)

        # Load and verify
        register = repo.load_register("science", "vii")
        expected = {"1": 5, "2": 8, "3": 4, "4": 7, "8": 9}
        assert register == expected, f"Expected {expected}, got {register}"
        print("✓ Mixed overwrite and new chapters merge correctly")


def test_summary_reflects_merged_state():
    """Summary should always reflect the cumulative register state."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)

        # First allocation
        first_alloc = {"1": 5, "2": 6, "3": 4}
        repo.save_allocation("science", "vii", first_alloc)

        summary1 = repo.get_summary("science", "vii")
        assert summary1.chapters_allocated == 3
        assert summary1.total_planned_periods == 15
        assert summary1.total_planned_time_minutes == 15 * 45  # 45 min per period
        print(f"✓ First summary: {summary1.chapters_allocated} chapters, {summary1.total_planned_periods} periods")

        # Second allocation (new chapters)
        second_alloc = {"4": 7, "5": 8}
        repo.save_allocation("science", "vii", second_alloc)

        summary2 = repo.get_summary("science", "vii")
        assert summary2.chapters_allocated == 5
        assert summary2.total_planned_periods == 30  # 5+6+4+7+8
        assert summary2.total_planned_time_minutes == 30 * 45
        print(f"✓ Second summary: {summary2.chapters_allocated} chapters, {summary2.total_planned_periods} periods")


def test_empty_register_summary():
    """Summary for non-existent register should have zeros."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)

        summary = repo.get_summary("nonexistent_subject", "vii")
        assert summary.chapters_allocated == 0
        assert summary.total_planned_periods == 0
        assert summary.total_planned_time_minutes == 0
        print("✓ Empty register summary is all zeros")


def test_persistence_across_instances():
    """Data persists across different repo instances."""
    tmpdir = tempfile.mkdtemp()
    try:
        # Write with one instance
        repo1 = AllocationRepositoryFileImpl(tmpdir)
        alloc = {"1": 5, "2": 6, "3": 4}
        repo1.save_allocation("science", "vii", alloc)

        # Read with another instance
        repo2 = AllocationRepositoryFileImpl(tmpdir)
        register = repo2.load_register("science", "vii")
        assert register == alloc, f"Data did not persist: expected {alloc}, got {register}"
        print("✓ Data persists across repository instances")
    finally:
        shutil.rmtree(tmpdir)


def test_multiple_subjects_and_grades():
    """Separate registers for different subjects/grades."""
    with tempfile.TemporaryDirectory() as tmpdir:
        repo = AllocationRepositoryFileImpl(tmpdir)

        # Science grade vii
        repo.save_allocation("science", "vii", {"1": 5, "2": 6})

        # Science grade vi
        repo.save_allocation("science", "vi", {"1": 4, "2": 5})

        # Mathematics grade vii
        repo.save_allocation("mathematics", "vii", {"1": 7, "2": 8})

        # Verify each register is independent
        sci7 = repo.load_register("science", "vii")
        sci6 = repo.load_register("science", "vi")
        math7 = repo.load_register("mathematics", "vii")

        assert sci7 == {"1": 5, "2": 6}
        assert sci6 == {"1": 4, "2": 5}
        assert math7 == {"1": 7, "2": 8}
        print("✓ Separate registers for different subjects/grades")


if __name__ == "__main__":
    test_first_allocation_initializes_register()
    test_second_allocation_merges_new_chapters()
    test_overwrite_allocation_replaces_for_existing_chapters()
    test_mixed_overwrite_and_new_chapters()
    test_summary_reflects_merged_state()
    test_empty_register_summary()
    test_persistence_across_instances()
    test_multiple_subjects_and_grades()
    print("\n✅ All allocation tests passed!")
