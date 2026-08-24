"""ManualBillingProvider — the founder IS the gateway (Step 5 reference impl).

Implements the BillingProvider port with no vendor: create_subscription writes an
active entitlement, cancel expires it, fetch_status reads it. Real behaviour — grant,
expire, revoke — exercised via aruvi-scripts/entitlement.py, so the subscription
machinery is testable end-to-end before any gateway exists. The partner's Razorpay /
Play Billing / Apple IAP adapters replace THIS CLASS behind the same port and populate
Entitlement.source with the real platform of purchase; nothing above the port changes.

verify_webhook raises: there is no webhook when the founder is the gateway, and a
silent success here would mask a mis-wired gateway integration later.
"""
from datetime import date, timedelta
from typing import Any, Dict, List, Optional

from aruvi_core.ports import BillingProvider, Entitlement, EntitlementRepository


class ManualBillingProvider(BillingProvider):
    """Founder-operated billing: entitlements written by hand, no gateway."""

    def __init__(self, entitlement_repo: EntitlementRepository):
        self.repo = entitlement_repo

    def create_subscription(self, tenant_id: str, plan_id: str,
                            scopes: Optional[List[str]] = None,
                            valid_until: str = "",
                            source: str = "manual") -> Dict[str, Any]:
        """Grant an active subscription. `scopes` defaults to ["*"] (all
        subject-stages) — the founder narrows it for individual subject-stage grants.
        `valid_until` defaults to one year from today (the rolling annual, §2.5)."""
        until = valid_until or (date.today() + timedelta(days=365)).isoformat()
        ent = Entitlement(plan_id=plan_id, status="active", valid_until=until,
                          source=source, scopes=list(scopes) if scopes else ["*"])
        self.repo.save(tenant_id, ent)
        return {"tenant_id": tenant_id, "plan_id": plan_id, "status": "active",
                "valid_until": until, "scopes": ent.scopes}

    def verify_webhook(self, payload: bytes, signature: str) -> Dict[str, Any]:
        raise NotImplementedError(
            "ManualBillingProvider has no webhooks — the founder is the gateway. "
            "A real gateway adapter implements this.")

    def cancel(self, tenant_id: str) -> Dict[str, Any]:
        """Expire the tenant's entitlement (revoke). No-op result if none exists.
        The record is kept, marked expired — an audit trace, not an erasure (erasure
        is Step 4's job and only ever the teacher's own action)."""
        ent = self.repo.load(tenant_id)
        if ent is None:
            return {"tenant_id": tenant_id, "status": "none"}
        ent.status = "expired"
        self.repo.save(tenant_id, ent)
        return {"tenant_id": tenant_id, "status": "expired"}

    def fetch_status(self, tenant_id: str) -> Dict[str, Any]:
        """Current entitlement state, as a plain dict for tooling/routes."""
        ent = self.repo.load(tenant_id)
        if ent is None:
            return {"tenant_id": tenant_id, "status": "none"}
        return {"tenant_id": tenant_id, "plan_id": ent.plan_id, "status": ent.status,
                "valid_until": ent.valid_until, "source": ent.source,
                "scopes": ent.scopes, "trial_chapters": ent.trial_chapters}
