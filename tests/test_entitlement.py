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

# ★ The checkout gate now needs a signature (2026-08-27) — the user agreement's six
# ticks are taken before the subject cart, so every checkout test must sign first.
# Imported from test_consent rather than re-derived: the tick ids belong to the
# document, and two tests guessing at them is two tests that can drift from it.
from tests.test_consent import accept_current  # noqa: E402



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
        # Expired-by-date: blocked with the renewal message. The date that decides is
        # the SCOPE'S OWN (2026-08-26) — see test_per_scope_validity for why.
        ent = api_main.entitlement_repo.load(t)
        ent.scope_valid_until["social_sciences/secondary"] = "2020-01-01"
        api_main.entitlement_repo.save(t, ent)
        msg = _gate(t, subject="social_sciences", grade="ix", chapter=9)
        assert msg and "Renew" in msg and "stays yours" in msg
        # LEGACY RECORD (written before per-scope dates existed): no scope_valid_until,
        # so the entitlement-level date must still decide. The fallback IS the migration.
        ent.scope_valid_until = {}
        ent.valid_until = "2020-01-01"
        api_main.entitlement_repo.save(t, ent)
        msg = _gate(t, subject="social_sciences", grade="ix", chapter=9)
        assert msg and "Renew" in msg, "a legacy single-date record must still expire"
        # Revoked: blocked.
        api_main.billing_provider.cancel(t)
        assert _gate(t, subject="social_sciences", grade="ix", chapter=9)
        # Enterprise-style "*" scope allows everything.
        api_main.billing_provider.create_subscription(t, "enterprise_annual")
        assert _gate(t, subject="mathematics", grade="vi", chapter=1) is None
        print("✓ Paid: scope-aware, date-aware, revocable; '*' covers all")
    finally:
        config.ENTITLEMENT_ENFORCED = False


def test_lapsed_lockout_productivity():
    """§2.5 as amended (founder persona pass, 2026-08-24): an EXPIRED subscription
    keeps her plans (reads/export stay open) but locks the productivity tools —
    profile writes and section tracking 402. Trial teachers are untouched."""
    from fastapi.testclient import TestClient
    from api import config, main as api_main

    config.ENTITLEMENT_ENFORCED = True
    try:
        c = TestClient(api_main.app)
        h = {"X-Aruvi-User": "LapsedLock"}
        api_main.billing_provider.create_subscription("LapsedLock", "individual_annual")
        api_main.billing_provider.cancel("LapsedLock")
        assert c.post("/readiness", json={"subjects": []}, headers=h).status_code == 402
        assert c.post("/section-state", json={"section_key": "s", "chapter": "c"},
                      headers=h).status_code == 402
        assert c.delete("/section-state/s", headers=h).status_code == 402
        assert c.delete("/readiness", headers=h).status_code == 402
        # Reads and data rights stay fully open (plans are hers).
        assert c.get("/section-state", headers=h).status_code == 200
        assert c.get("/plans-prepared", headers=h).status_code == 200
        assert c.get("/data-rights/export", headers=h).status_code == 200
        # A trial teacher is untouched by the lockout.
        h2 = {"X-Aruvi-User": "TrialLock"}
        assert c.post("/section-state", json={"section_key": "s", "chapter": "c"},
                      headers=h2).status_code == 200
        print("✓ Lapsed: productivity locked, plans/reads/export open, trial untouched")
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


def test_per_scope_validity_and_addition():
    """★ 2026-08-26 — subscriptions ADD, and each carries its own expiry.

    Reported live by the founder: "I purchased science middle and science secondary,
    then added English middle, and the English addition overwrote the previous
    subscriptions." create_subscription wrote a whole new entitlement, so the second
    purchase silently destroyed the first — she paid ₹500 and lost two subjects.

    Four properties, each of which was false before:
      1. a later purchase KEEPS what she already holds;
      2. each scope expires on its OWN date (added in November → next November);
      3. one scope running out does not lapse her — the tracker and profile stay open
         while ANY scope is live (founder's call: she is still a paying customer, and
         the productivity tools are not per-subject);
      4. generation is refused per scope, naming that scope and its own end date.
    """
    from api import config, main as api_main
    config.ENTITLEMENT_ENFORCED = True
    try:
        t = "AdderTeacher"
        api_main.billing_provider.create_subscription(
            t, "individual_annual", scopes=["science/middle", "science/secondary"],
            valid_until="2027-08-26")
        api_main.billing_provider.create_subscription(
            t, "individual_annual", scopes=["english/middle"],
            valid_until="2027-11-02")
        ent = api_main.entitlement_repo.load(t)
        assert ent.scopes == ["science/middle", "science/secondary", "english/middle"], \
            f"an addition must not overwrite: {ent.scopes}"
        assert ent.scope_valid_until["science/middle"] == "2027-08-26"
        assert ent.scope_valid_until["english/middle"] == "2027-11-02"
        assert ent.valid_until == "2027-11-02", "top-level date is the LATEST, derived"

        # One runs out. She keeps the others, and she is NOT lapsed.
        ent.scope_valid_until["english/middle"] = "2020-01-01"
        api_main.entitlement_repo.save(t, ent)
        today = "2026-08-26"
        assert api_main._live_scopes(ent, today) == ["science/middle", "science/secondary"]
        assert api_main._entitlement_lapsed(ent, today) is False, \
            "one expired subject must not take away the tracker she still pays for"
        assert _gate(t, subject="science", grade="vii", chapter=1) is None
        msg = _gate(t, subject="english", grade="vii", chapter=1)
        assert msg and "English · Middle" in msg and "01-Jan-2020" in msg, msg

        # All of them run out → lapsed, and the productivity gate closes.
        for s in list(ent.scope_valid_until):
            ent.scope_valid_until[s] = "2020-01-01"
        api_main.entitlement_repo.save(t, ent)
        assert api_main._live_scopes(ent, today) == []
        assert api_main._entitlement_lapsed(ent, today) is True
        print("✓ Subscriptions add, expire per scope, and lapse only when none is live")
    finally:
        config.ENTITLEMENT_ENFORCED = False


def test_cannot_rebuy_a_live_scope():
    """A scope she already holds, still running, is not for sale — the chooser omits it
    and checkout refuses it with the date it runs to (founder, 2026-08-26: renewal is
    for something that has ENDED; selling her a year she already owns is not a renewal).
    The trial's "*" is not a holding, or the first purchase could never happen."""
    from fastapi.testclient import TestClient
    from api import main as api_main

    c = TestClient(api_main.app, raise_server_exceptions=False)
    H = {"X-Aruvi-User": "RebuyTeacher"}
    body = {"scopes": ["science/middle"], "name": "T", "email": "", "role": "Teacher",
            "state": "Kerala", "city": "Kochi", "school": ""}
    accept_current(c, H)          # the agreement gate (2026-08-27)
    assert c.post("/onboarding/checkout", headers=H, json=body).status_code == 200
    r = c.post("/onboarding/checkout", headers=H, json=body)
    assert r.status_code == 409, r.status_code
    assert "already have" in r.json()["detail"] and "Science · Middle" in r.json()["detail"]
    # A DIFFERENT scope still goes through, and the first survives it.
    body2 = dict(body, scopes=["english/middle"])
    assert c.post("/onboarding/checkout", headers=H, json=body2).status_code == 200
    scopes = api_main.entitlement_repo.load("RebuyTeacher").scopes
    assert scopes == ["science/middle", "english/middle"], scopes
    print("✓ A live scope cannot be re-bought; a new one adds without disturbing it")


def test_trial_purge_on_first_purchase():
    """★ 2026-08-26 evening — the trial purge, and the morning's rule it reverses.

    Founder: *"If a teacher does trial of subjects {x,y} but subscribes first time to
    subjects <> {x,y}, the trial chapters must be purged once and for all. The {x,y}
    stands there in My Lessons with no use, clogging the space for a trial reason that
    is no longer valid."* Every card of such a subject is a door that no longer opens:
    she cannot prepare in it, track it, or add sections to it.

    Three properties:
      1. a subject she trialled and did NOT buy loses its prepared records, section
         state and notes;
      2. a subject she trialled and DID buy keeps all three — that is what a trial is
         for, and it is the half the paywall still promises;
      3. purging happens on the FIRST purchase only; a later addition touches nothing.
    """
    from fastapi.testclient import TestClient
    from api import main as api_main

    c = TestClient(api_main.app, raise_server_exceptions=False)
    t = u = "PurgeTeacher"
    H = {"X-Aruvi-User": t}
    c.get("/entitlement", headers=H)                      # JIT-start the trial
    year = api_main._resolve_year(t, u)
    for key, sec in (("english/vi/ch_01.json", "english_vi_A"),
                     ("science/vi/ch_02.json", "science_vi_A")):
        api_main.prepared_plans_repo.mark(t, u, year, key, 10)
    from datetime import datetime, timezone
    from aruvi_core.ports import PlanNote
    api_main.section_state_repo.save_one(t, u, year, "english_vi_A", "1", 0, False)
    api_main.section_state_repo.save_one(t, u, year, "science_vi_A", "2", 0, False)
    now = datetime.now(timezone.utc).isoformat()
    for k, txt in (("english/vi/1", "trial note"), ("science/vi/2", "kept note")):
        api_main.plan_note_repo.save(t, u, year, PlanNote(note_key=k, text=txt,
                                                          updated_at=now))

    # She buys SCIENCE only.
    accept_current(c, H)          # the agreement gate (2026-08-27)
    r = c.post("/onboarding/checkout", headers=H, json={
        "scopes": ["science/middle"], "name": "P", "email": "", "role": "Teacher",
        "state": "Kerala", "city": "Kochi", "school": ""})
    assert r.status_code == 200, r.json()

    prepared = api_main.prepared_plans_repo.load_all(t, u, year)
    assert "science/vi/ch_02.json" in prepared, "a subject she BOUGHT keeps its plans"
    assert "english/vi/ch_01.json" not in prepared, "the un-bought trial subject is purged"
    sections = api_main.section_state_repo.load_all(t, u, year)
    assert "science_vi_A" in sections and "english_vi_A" not in sections
    notes = api_main.plan_note_repo.load_all(t, u, year)
    assert "science/vi/2" in notes and "english/vi/1" not in notes

    # A LATER addition purges nothing — science's records survive buying English.
    r = c.post("/onboarding/checkout", headers=H, json={
        "scopes": ["english/middle"], "name": "P", "email": "", "role": "Teacher",
        "state": "Kerala", "city": "Kochi", "school": ""})
    assert r.status_code == 200 and r.json()["purged"] == {}
    assert "science/vi/ch_02.json" in api_main.prepared_plans_repo.load_all(t, u, year)
    print("✓ Trial purge: un-bought subjects cleared once, bought ones untouched")


if __name__ == "__main__":
    test_repo_roundtrip_and_tenant_isolation()
    test_manual_billing_provider()
    test_gate_off_by_default()
    test_trial_chapter_cap_and_free_reserves()
    test_paid_scope_and_expiry()
    test_per_scope_validity_and_addition()
    test_cannot_rebuy_a_live_scope()
    test_trial_purge_on_first_purchase()
    test_lapsed_lockout_productivity()
    test_entitlement_route()
    print("\n✅ All entitlement tests passed!")
