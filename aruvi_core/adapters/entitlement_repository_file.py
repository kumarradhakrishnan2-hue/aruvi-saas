"""File-based implementation of EntitlementRepository.

Persists a tenant's entitlement as JSON at
ARUVI_STATE_DIR/entitlements/{tenant_id}/entitlement.json — keyed by TENANT only
(the subscription belongs to the tenant, every user under it rides it), and NOT
year-scoped (a subscription is rolling, admin architecture §2.5).

Shape follows the ports.Entitlement dataclass exactly; unknown/missing fields tolerate
dataclass growth the same way the account adapter does. The partner's cloud adapter
(one row per tenant, written by their BillingProvider webhook handler) swaps in behind
the same port.
"""
import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from aruvi_core.ports import Entitlement, EntitlementRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class EntitlementRepositoryFileImpl(EntitlementRepository):
    """File-based per-tenant entitlement store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the entitlements/ folder lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.base_dir = self.data_dir / "entitlements"

    def _path(self, tenant_id: str) -> Path:
        return self.base_dir / _slug(tenant_id) / "entitlement.json"

    def load(self, tenant_id: str) -> Optional[Entitlement]:
        """The tenant's entitlement, or None if never granted."""
        path = self._path(tenant_id)
        if not path.exists():
            return None
        try:
            with open(path, "r") as f:
                raw = json.load(f) or {}
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to load entitlement from {path}: {e}")
        return Entitlement(
            plan_id=str(raw.get("plan_id", "")),
            status=str(raw.get("status", "expired")),
            valid_until=str(raw.get("valid_until", "")),
            source=str(raw.get("source", "")),
            scopes=list(raw.get("scopes") or []),
            trial_chapters=list(raw.get("trial_chapters") or []),
        )

    def save(self, tenant_id: str, ent: Entitlement) -> None:
        """Create or fully replace the tenant's entitlement."""
        path = self._path(tenant_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(path, "w") as f:
                json.dump(asdict(ent), f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save entitlement to {path}: {e}")
