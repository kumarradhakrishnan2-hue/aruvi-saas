"""ReadinessRepository over the document backend (file or Postgres — Track C, 2026-09-09).

Persists a teacher's readiness teaching profile as one JSON document at key
readiness/{tenant_id}/{user_id}/profile.json.

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
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from aruvi_core.ports import ReadinessProfile, ReadinessRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug


# Keys that form the denormalized active-subject projection. They must never be
# persisted — see CLOUD_DATA_MODEL.md §2.1 / §5. We strip them on save defensively
# so that even if the frontend sends the whole payload, only the canonical
# subjects[] (plus metadata) ever lands on disk.
_PROJECTION_KEYS = ("subject", "grades", "grids", "durations", "budget", "activeSubjectIndex")


class ReadinessRepositoryFileImpl(ReadinessRepository):
    """Readiness teaching-profile store over a document backend."""

    def __init__(self, data_dir):
        """
        Args:
            data_dir: a DocumentBackend, or a directory (→ FileBackend, e.g. ARUVI_STATE_DIR).
        """
        self.backend = as_backend(data_dir)

    def _key(self, tenant_id: str, user_id: str) -> str:
        return f"readiness/{_slug(tenant_id)}/{_slug(user_id)}/profile.json"

    # File-backend diagnostics (tests inspect the raw document on disk).
    def _profile_path(self, tenant_id: str, user_id: str):
        return self.backend._path(self._key(tenant_id, user_id))

    @property
    def readiness_dir(self):
        return self.backend.root / "readiness"

    def load_profile(self, tenant_id: str, user_id: str) -> Optional[ReadinessProfile]:
        """Load the saved readiness profile, or None if none exists yet."""
        raw = self.backend.get_json(self._key(tenant_id, user_id))
        return raw if isinstance(raw, dict) else None

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

        self.backend.put_json(self._key(tenant_id, user_id), record)

    def clear_profile(self, tenant_id: str, user_id: str) -> None:
        """Erase the teacher's readiness profile. No-op if it doesn't exist (the file
        backend leaves an empty document on mounts that forbid unlink — which the API
        reads as not-ready — so "start setup over" never 500s)."""
        self.backend.delete(self._key(tenant_id, user_id))
