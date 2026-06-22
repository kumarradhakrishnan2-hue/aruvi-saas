"""File-based implementation of AllocationRepository.

Persists the Persistent Annual Allocation Register as JSON at
ARUVI_DATA_DIR/allocations/{subject}/{grade}/allocation.json.

Merge semantics: chapters in the new allocation overwrite existing allocations
for those chapters; chapters not in the new allocation retain their previous
allocations.
"""
import json
from pathlib import Path
from typing import Dict, Optional, Union

from aruvi_core.ports import AllocationRepository, AllocationSummary
from aruvi_core.grades import stage_for


class AllocationRepositoryFileImpl(AllocationRepository):
    """File-based Persistent Annual Allocation Register."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where allocations/ folder lives (e.g., ARUVI_DATA_DIR).
        """
        self.data_dir = Path(data_dir)
        self.allocations_dir = self.data_dir / "allocations"

    def _register_path(self, subject: str, grade: Union[str, int]) -> Path:
        """Return the path to the allocation register file."""
        return self.allocations_dir / subject / str(grade) / "allocation.json"

    def load_register(self, subject: str, grade: Union[str, int]) -> Dict[str, int]:
        """Load the Annual Allocation Register.

        Returns empty dict if no register exists yet.
        """
        path = self._register_path(subject, grade)
        if not path.exists():
            return {}

        try:
            with open(path, "r") as f:
                data = json.load(f)
            # Ensure all values are integers (chapters allocated periods)
            return {str(k): int(v) for k, v in data.items()}
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to load allocation register from {path}: {e}")

    def save_allocation(self, subject: str, grade: Union[str, int], chapters_allocation: Dict[str, int]) -> None:
        """Save allocation data, merging into the existing register.

        Chapters in chapters_allocation overwrite existing allocations for those chapters.
        Chapters not in chapters_allocation retain their previous allocations.
        """
        # Load existing register
        existing = self.load_register(subject, grade)

        # Merge: update with new allocations, preserve untouched chapters
        merged = {**existing, **chapters_allocation}

        # Ensure path exists
        path = self._register_path(subject, grade)
        path.parent.mkdir(parents=True, exist_ok=True)

        # Write merged register
        try:
            with open(path, "w") as f:
                json.dump(merged, f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save allocation register to {path}: {e}")

    def get_summary(self, subject: str, grade: Union[str, int]) -> AllocationSummary:
        """Return a summary of the current register state."""
        register = self.load_register(subject, grade)

        # Count allocated chapters
        chapters_allocated = len(register)

        # Total periods allocated
        total_periods = sum(register.values())

        # Get stage to determine total chapters for "remaining" count
        # grade can be int or string; convert to string for stage_for()
        stage = stage_for(str(grade))

        # For now, we don't have a centralized "total chapters per subject/stage" mapping.
        # Rough heuristic: assume 12 chapters for middle/secondary, fewer for preparatory.
        # This will be refined once we have the full subject specs.
        if stage == "preparatory":
            total_chapters_estimate = 8  # Typical for preparatory
        elif stage == "middle":
            total_chapters_estimate = 12  # Typical for middle
        else:  # secondary
            total_chapters_estimate = 12  # Typical for secondary

        chapters_remaining = max(0, total_chapters_estimate - chapters_allocated)

        # Assume standard period duration; this can be refined with metadata later.
        # For now, 1 period = 45 minutes (common in Indian schools).
        minutes_per_period = 45
        total_time_minutes = total_periods * minutes_per_period

        return AllocationSummary(
            chapters_allocated=chapters_allocated,
            chapters_remaining=chapters_remaining,
            total_planned_periods=total_periods,
            total_planned_time_minutes=total_time_minutes,
        )
