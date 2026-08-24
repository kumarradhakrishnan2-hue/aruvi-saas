"""
Tests for administrative-architecture Step 5: the entitlement seam.

Model under test (docs/subscription_model_discussion.md §0): billing unit = teacher ×
subject-stage, unlimited within scope; trial capped by CHAPTERS (any 3, all
subject-stages open), unlimited re-serves per chapter, no time limit; gate in front of
generation only; enforcement behind a flag (default OFF); founder operates via
ManualBillingProvider with no gateway.

Run standalone:  python3 tests/test_entitlement.py     (also pytest-compatible)
"""
from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Throwaway state dir BEFORE importing api.main (see test_account.py).
_TMP_STATE = tempfile.mkdtemp(prefix="aruvi-test-state-")
os.environ.setdefault("ARUVI_STATE_DIR", _TMP_STATE)

from aruvi_core.ports import Entitlement  # noqa: E402
from aruvi_core.adapters.entitlement_repository_file import EntitlementRepositoryFileImpl  # noqa: E402
from aruvi_core.adapters.manual_billing_provider import ManualBillingProvider  # noqa: E402


def test_repo_roundtrip_and_tenant_isolation():
    with tempfile.TemporaryDirectory() as tmp:
        repo = EntitlementRepositoryFileImpl(tmp)
        assert repo.load("Kumar1") is None
        ent = Entitlement(plan_id="individual_annual", status="active",
                          valid_until="2027-08-22", source="manual",
                          scopes=["social_sciences/middle"])
        repo.save("Kumar1", ent)
        assert repo.load("Kumar1") == ent
        assert repo.load("Priya2") is None, "tenant-keyed, isolated"
        print("✓ Entitlement repo roundtrip + tenant isolation")


def test_manual_billing_provider():
    """The Step-5 'done' test: grant, expire, revoke — no gateway."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = EntitlementRepositoryFileImpl(tmp)
        p = ManualBillingProvider(repo)
        r = p.create_subscription("Kumar1", "individual_annual",
                                  scopes=["social_sciences/middle"])
        assert r["status"] == "active" and r["valid_until"]
        assert repo.load("Kumar1").scopes == ["social_sciences/middle"]
        assert p.fetch_status("Kumar1")["status"] == "active"
        assert p.cancel("Kumar1")["status"] == "expired"
        assert repo.load("Kumar1").status == "expired"
        assert p.fetch_status("Nobody")["status"] == "none"
        try:
            p.verify_webhook(b"", "")
            assert False, "manual provider must refuse webhooks loudly"
        except NotImplementedError:
            pass
        print("✓ ManualBillingProvider grants, expires, revokes without a gateway")


def _gate(tenant, subject="social_sciences", grade="ix", chapter=3):
    """Call the api gate; returns None on allow, the HTTP detail string on block."""
    from fastapi import HTTPException
    from api import main as api_main
    try:
        api_main._check_entitlement(tenant, subject, grade, chapter)
        return None
    except HTTPException as e:
        return str(e.detail)


def test_gate_off_by_default():
    from api import config
    assert config.ENTITLEMENT_ENFORCED is False, "dev default must be OFF"
    assert _gate("AnyoneAtAll") is None
    print("✓ Enforcement is off by default; nothing is gated")


def test_trial_chapter_cap_and_free_reserves():
    """With enforcement ON: 3 chapters allowed, unlimited re-serves of those 3, the
    4th blocked with a plain-words message that speaks in chapters."""
    from api import config, main as api_main
    config.ENTITLEMENT_ENFORCED = True
    try:
        t = "TrialTeacher"
        # Chapters 1..3: allowed and counted (count happens after a successful serve).
        for ch in (1, 2, 3):
            assert _gate(t, chapter=ch) is None
            api_main._count_trial_chapter(t, "social_sciences", "ix", ch)
        ent = api_main.entitlement_repo.load(t)
        assert ent.status == "trial" and len(ent.trial_chapters) == 3
        # Re-serve of a counted chapter, any subject-stage: free, forever.
        assert _gate(t, chapter=2) is None
        api_main._count_trial_chapter(t, "social_sciences", "ix", 2)  # idempotent
        assert len(api_main.entitlement_repo.load(t).trial_chapters) == 3
        # A 4th chapter: blocked, message in chapters (never "generations"/"scope").
        msg = _gate(t, chapter=4)
        assert msg and "chapters" in msg and "generation" not in msg.lower()
        # Trial spans ALL subject-stages — the 4th is blocked in another subject too.
        assert _gate(t, subject="science", grade="vii", chapter=1)
        print("✓ Trial: any 3 chapters, unlimited re-serves, 4th blocked plainly")
    finally:
        config.ENTITLEMENT_ENFORCED = False


def test_paid_scope_and_expiry():
    from api import config, main as api_main
    config.ENTITLEMENT_ENFORCED = True
    try:
        t = "PaidTeacher"
        api_main.billing_provider.create_subscription(
            t, "individual_annual", scopes=["social_sciences/secondary"])
        # In scope: SS grade ix is secondary → unlimited, nothing counted.
        assert _gate(t, subject="social_sciences", grade="ix", chapter=9) is None
        api_main._count_trial_chapter(t, "social_sciences", "ix", 9)
        assert api_main.entitlement_repo.load(t).trial_chapters == [], \
            "paid serves never touch the trial counter"
        # Out of scope: SS middle (grade vii) blocked with the add-subject message.
        msg = _gate(t, subject="social_sciences", grade="vii", chapter=1)
        assert msg and "different subject" in msg
        # Expired-by-date: blocked with the renewal message.
        ent = api_main.entitlement_repo.load(t)
        ent.valid_until = "2020-01-01"
        api_main.entitlement_repo.save(t, ent)
        msg = _gate(t, subject="social_sciences", grade="ix", chapter=9)
        assert msg and "Renew" in msg and "stays yours" in msg
        # Revoked: blocked.
        api_main.billing_provider.cancel(t)
        assert _gate(t, subject="social_sciences", grade="ix", chapter=9)
        # Enterprise-style "*" scope allows everything.
        api_main.billing_provider.create_subscription(t, "enterprise_annual")
        assert _gate(t, subject="mathematics", grade="vi", chapter=1) is None
        print("✓ Paid: scope-aware, date-aware, revocable; '*' covers all")
    finally:
        config.ENTITLEMENT_ENFORCED = False


def test_entitlement_route():
    """GET /entitlement gives the UI its counter; JIT-starts the trial."""
    from fastapi.testclient import TestClient
    from api import main as api_main

    c = TestClient(api_main.app)
    d = c.get("/entitlement", headers={"X-Aruvi-User": "RouteTeacher"}).json()
    assert d["status"] == "trial" and d["plan_id"] == "trial"
    assert d["trial_chapters_used"] == 0 and d["trial_chapter_cap"] >= 1
    assert d["enforced"] is False
    print("✓ GET /entitlement reports the trial counter and gate state")


if __name__ == "__main__":
    test_repo_roundtrip_and_tenant_isolation()
    test_manual_billing_provider()
    test_gate_off_by_default()
    test_trial_chapter_cap_and_free_reserves()
    test_paid_scope_and_expiry()
    test_entitlement_route()
    print("\n✅ All entitlement tests passed!")
