"""EntitlementRepository over the document backend (file or Postgres — Track C, 2026-09-09).

Persists a tenant's entitlement as one JSON document at key
entitlements/{tenant_id}/entitlement.json — keyed by TENANT only
(the subscription belongs to the tenant, every user under it rides it), and NOT
year-scoped (a subscription is rolling, admin architecture §2.5).

Shape follows the ports.Entitlement dataclass exactly; unknown/missing fields tolerate
dataclass growth the same way the account adapter does. The partner's cloud adapter
(one row per tenant, written by their BillingProvider webhook handler) swaps in behind
the same port.
"""
from dataclasses import asdict
from typing import Optional

from aruvi_core.ports import Entitlement, EntitlementRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug


class EntitlementRepositoryFileImpl(EntitlementRepository):
    """Per-tenant entitlement store over a document backend."""

    def __init__(self, data_dir):
        """
        Args:
            data_dir: a DocumentBackend, or a directory (→ FileBackend, e.g. ARUVI_STATE_DIR).
        """
        self.backend = as_backend(data_dir)

    def _key(self, tenant_id: str) -> str:
        return f"entitlements/{_slug(tenant_id)}/entitlement.json"

    def load(self, tenant_id: str) -> Optional[Entitlement]:
        """The tenant's entitlement, or None if never granted."""
        raw = self.backend.get_json(self._key(tenant_id))
        if raw is None:
            return None
        if not isinstance(raw, dict):
            raw = {}
        return Entitlement(
            plan_id=str(raw.get("plan_id", "")),
            status=str(raw.get("status", "expired")),
            valid_until=str(raw.get("valid_until", "")),
            source=str(raw.get("source", "")),
            scopes=list(raw.get("scopes") or []),
            trial_chapters=list(raw.get("trial_chapters") or []),
            # Per-scope expiry (2026-08-26). Absent on every record written before it —
            # those scopes fall back to the entitlement-level valid_until, which is what
            # they have always meant. No migration script: the fallback IS the migration,
            # and the next grant stamps real dates.
            scope_valid_until={str(k): str(v) for k, v
                               in (raw.get("scope_valid_until") or {}).items()},
        )

    def save(self, tenant_id: str, ent: Entitlement) -> None:
        """Create or fully replace the tenant's entitlement."""
        self.backend.put_json(self._key(tenant_id), asdict(ent))
