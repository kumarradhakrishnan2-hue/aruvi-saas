"""File-based implementation of ReadinessRepository.

Persists a teacher's readiness teaching profile as JSON at
ARUVI_DATA_DIR/readiness/{tenant_id}/{user_id}/profile.json.

What is stored is the CANONICAL `subjects[]` array only (see CLOUD_DATA_MODEL.md §2.1):
each element is a self-contained per-subject record — name, durations, grades (with
sections + per-grade durations), the weekly grid, and the annual budget. The
denormalized "active subject" projection the React component also emits
(subject/grades/grids/durations/budget at the top level) is DELIBERATELY dropped on
save — it is derived sugar regenerated on read, never source of truth
(CLOUD_DATA_MODEL.md §5 invariant). Stripping it here is the one guard that keeps the
on-disk shape a clean drop-in for the Supabase `readiness_*` tables.

Every profile is keyed by tenant_id + user_id. With no auth yet both stub to "local";
Phase 4 swaps the values from the Supabase auth token with no schema change.

Save semantics are full-replace (readiness setup is re-run whole), unlike the
allocation register which merges chapter-by-chapter.
"""
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, Optional

from aruvi_core.ports import ReadinessProfile, ReadinessRepository


# Keys that form the denormalized active-subject projection. They must never be
# persisted — see CLOUD_DATA_MODEL.md §2.1 / §5. We strip them on save defensively
# so that even if the frontend sends the whole payload, only the canonical
# subjects[] (plus metadata) ever lands on disk.
_PROJECTION_KEYS = ("subject", "grades", "grids", "durations", "budget", "activeSubjectIndex")


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class ReadinessRepositoryFileImpl(ReadinessRepository):
    """File-based readiness teaching-profile store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the readiness/ folder lives (e.g., ARUVI_DATA_DIR).
        """
        self.data_dir = Path(data_dir)
        self.readiness_dir = self.data_dir / "readiness"

    def _profile_path(self, tenant_id: str, user_id: str) -> Path:
        """Return the path to a teacher's readiness profile file."""
        return self.readiness_dir / _slug(tenant_id) / _slug(user_id) / "profile.json"

    def load_profile(self, tenant_id: str, user_id: str) -> Optional[ReadinessProfile]:
        """Load the saved readiness profile, or None if none exists yet."""
        path = self._profile_path(tenant_id, user_id)
        if not path.exists():
            return None
        try:
            with open(path, "r") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to load readiness profile from {path}: {e}")

    def save_profile(self, tenant_id: str, user_id: str,
                     profile: ReadinessProfile) -> None:
        """Persist the readiness profile (full replace).

        Only the canonical subjects[] is kept; the denormalized active-subject
        projection is stripped before writing.
        """
        record: Dict[str, Any] = {
            "subjects": (profile or {}).get("subjects", []),
            "tenant_id": _slug(tenant_id),
            "user_id": _slug(user_id),
            "updated_at": datetime.now(timezone.utc).isoformat(),
        }
        # Defensive strip — never let the projection reach disk.
        for k in _PROJECTION_KEYS:
            record.pop(k, None)

        path = self._profile_path(tenant_id, user_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(path, "w") as f:
                json.dump(record, f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save readiness profile to {path}: {e}")

    def clear_profile(self, tenant_id: str, user_id: str) -> None:
        """Erase the teacher's readiness profile. No-op if it doesn't exist.

        Prefers removing the file. On filesystems where unlink is not permitted (some
        read-restricted mounts allow create/overwrite but not delete), falls back to
        overwriting with an empty profile — which the API reads as not-ready — so the
        "start setup over" action never 500s.
        """
        path = self._profile_path(tenant_id, user_id)
        if not path.exists():
            return
        try:
            path.unlink()
        except OSError:
            with open(path, "w") as f:
                json.dump({"subjects": [], "tenant_id": _slug(tenant_id),
                           "user_id": _slug(user_id),
                           "updated_at": datetime.now(timezone.utc).isoformat()}, f, indent=2)
