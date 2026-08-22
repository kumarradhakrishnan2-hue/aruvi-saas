"""
Tests for administrative-architecture Step 0: the Account record, its file adapter,
the HeaderAuthProvider reference impl, and the JIT identity path in api/main.py.

Run standalone:  python3 tests/test_account.py     (also pytest-compatible)
"""
from __future__ import annotations

import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Point the API at a throwaway state dir BEFORE importing api.main, so the JIT identity
# test never writes into the repo's real data/. (config reads the env var at import.)
_TMP_STATE = tempfile.mkdtemp(prefix="aruvi-test-state-")
os.environ["ARUVI_STATE_DIR"] = _TMP_STATE

from aruvi_core.ports import Account, Identity  # noqa: E402
from aruvi_core.adapters.account_repository_file import AccountRepositoryFileImpl  # noqa: E402
from aruvi_core.adapters.header_auth_provider import HeaderAuthProvider  # noqa: E402


def _acct(aid="Kumar1", tid=None, email=""):
    return Account(account_id=aid, tenant_id=tid or aid, display_name=aid, email=email)


def test_save_load_roundtrip():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AccountRepositoryFileImpl(tmp)
        a = _acct("Kumar1", email="k@example.com")
        repo.save(a)
        got = repo.load("Kumar1", "Kumar1")
        assert got == a
        assert repo.load("Nobody", "Nobody") is None
        print("✓ Account save/load roundtrip")


def test_tenant_and_user_are_separate_values():
    """A school tenant owning two accounts files them apart (the Step-0 point)."""
    with tempfile.TemporaryDirectory() as tmp:
        repo = AccountRepositoryFileImpl(tmp)
        repo.save(Account(account_id="teacherA", tenant_id="school9", display_name="A"))
        repo.save(Account(account_id="teacherB", tenant_id="school9", display_name="B"))
        assert repo.load("school9", "teacherA").display_name == "A"
        assert repo.load("school9", "teacherB").display_name == "B"
        assert repo.load("teacherA", "teacherA") is None  # not filed under self-tenant
        print("✓ tenant_id and user_id address independently")


def test_find_by_email():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AccountRepositoryFileImpl(tmp)
        repo.save(_acct("Kumar1", email="K@Example.com"))
        repo.save(_acct("Priya2"))  # no email
        hit = repo.find_by_email("k@example.com")
        assert hit is not None and hit.account_id == "Kumar1", "case-insensitive match"
        assert repo.find_by_email("") is None, "empty email never matches"
        assert repo.find_by_email("missing@example.com") is None
        print("✓ find_by_email is case-insensitive and empty-safe")


def test_delete():
    with tempfile.TemporaryDirectory() as tmp:
        repo = AccountRepositoryFileImpl(tmp)
        repo.save(_acct("Kumar1"))
        repo.delete("Kumar1", "Kumar1")
        assert repo.load("Kumar1", "Kumar1") is None
        repo.delete("Kumar1", "Kumar1")  # no-op, must not raise
        print("✓ delete removes the record and re-delete is a no-op")


def test_header_auth_provider():
    p = HeaderAuthProvider()
    i = p.verify_token("Kumar1")
    assert i == Identity(user_id="Kumar1", tenant_id="Kumar1", role="teacher")
    assert p.verify_token("").user_id == "local", "blank header falls back to local"
    assert "/" not in p.verify_token("../evil").user_id, "traversal is slugged away"
    print("✓ HeaderAuthProvider maps the header to an Identity")


def test_jit_identity_creates_account():
    """_current_identity resolves through the account record, JIT-creating it on the
    first-ever request — the 'any user ID signs in' dev behaviour, now durable."""
    from api import main as api_main

    tenant_id, user_id = api_main._current_identity("Kumar77")
    assert (tenant_id, user_id) == ("Kumar77", "Kumar77")
    acct = api_main.account_repo.load("Kumar77", "Kumar77")
    assert acct is not None and acct.status == "active" and acct.created_at
    # Second call reads the same account, does not re-create.
    created_at = acct.created_at
    api_main._current_identity("Kumar77")
    assert api_main.account_repo.load("Kumar77", "Kumar77").created_at == created_at
    print("✓ Identity JIT-creates a durable account exactly once")


if __name__ == "__main__":
    test_save_load_roundtrip()
    test_tenant_and_user_are_separate_values()
    test_find_by_email()
    test_delete()
    test_header_auth_provider()
    test_jit_identity_creates_account()
    print("\n✅ All account tests passed!")
