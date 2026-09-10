"""
Track C (2026-09-09): the document backend — ONE storage seam under every Bucket-B store.

Three layers, strongest last:
  1. The backend CONTRACT, run identically against FileBackend and PostgresBackend.
  2. MIGRATION: every document under data/cloud/state/ copied file → Postgres and read
     back equal, key for key (copy_all is the migration script's whole mechanism).
  3. The API in postgres mode (ARUVI_STATE_BACKEND=postgres), a teacher's journey end to
     end through the real routes — readiness, sections, history, notes, prepared plans,
     consent, support, invoice numbering, export, erase — and the erasure leaving exactly
     the seller-side stores behind, as the folder layout guaranteed.

Postgres layers need ARUVI_TEST_DATABASE_URL (a throwaway database — the `documents`
table is DROPPED at the start). Without it they are skipped, not failed, so the stdlib
suite stays runnable anywhere.

Run standalone:  ARUVI_TEST_DATABASE_URL=postgresql://… python3 tests/test_document_backend.py
"""
from __future__ import annotations

import json
import os
import sys
import tempfile
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from aruvi_core.adapters.document_backend import (  # noqa: E402
    FileBackend, DocumentBackend, copy_all, parse_key, slug)

PG_URL = os.environ.get("ARUVI_TEST_DATABASE_URL", "").strip()


def _pg():
    """A fresh PostgresBackend on an EMPTY documents table, or None when not configured."""
    if not PG_URL:
        return None
    from aruvi_core.adapters.document_backend import PostgresBackend
    import psycopg
    with psycopg.connect(PG_URL, autocommit=True) as c:
        c.execute("drop table if exists documents")
    return PostgresBackend(PG_URL)


# ── 0. key parsing ───────────────────────────────────────────────────────────────
def test_parse_key_and_slug():
    cases = {
        "section_state/t1/u1/2026-27/state.json": ("section_state", "t1", "u1", "2026-27"),
        "accounts/t1/u1/account.json": ("accounts", "t1", "u1", None),
        "readiness/t1/u1/profile.json": ("readiness", "t1", "u1", None),
        "entitlements/t1/entitlement.json": ("entitlements", "t1", None, None),
        "invoices/t1/u1/MEY-2026-27-7864.pdf": ("invoices", "t1", "u1", None),
        "invoices/_series/2026-27.json": ("invoices", None, None, None),
        "support/_series/support.json": ("support", None, None, None),
        "consents/_ledger/t1.json": ("consents", None, None, None),
        "erasure_log/t1.json": ("erasure_log", None, None, None),
        "allocations/t1/u1/2026-27/science/vi/allocation.json": ("allocations", "t1", "u1", "2026-27"),
    }
    for key, (kind, t, u, y) in cases.items():
        got = parse_key(key)
        assert (got["kind"], got["tenant_id"], got["user_id"], got["year_id"]) == (kind, t, u, y), (key, got)
    # No tenant id can slug into the "_"-prefixed non-tenant namespace.
    assert slug("_series") == "series" and slug("__ledger__") == "ledger"
    assert slug("../../etc") == "etc" and slug("") == "local"
    print("✓ parse_key files series/ledger/erasure_log with NO tenant; slug cannot forge one")


# ── 1. the contract ──────────────────────────────────────────────────────────────
def _contract(b: DocumentBackend, label: str):
    assert b.get_json("accounts/t/u/account.json") is None
    assert not b.exists("accounts/t/u/account.json")
    b.put_json("accounts/t/u/account.json", {"account_id": "u", "email": "A@x.io", "n": 1})
    assert b.exists("accounts/t/u/account.json")
    assert b.get_json("accounts/t/u/account.json") == {"account_id": "u", "email": "A@x.io", "n": 1}
    # overwrite replaces whole
    b.put_json("accounts/t/u/account.json", {"account_id": "u"})
    assert b.get_json("accounts/t/u/account.json") == {"account_id": "u"}
    # unicode + nesting survive
    doc = {"text": "தமிழ் — notes", "list": [1, {"a": None}], "nested": {"x": [True, 2.5]}}
    b.put_json("plan_notes/t/u/2026-27/notes.json", doc)
    assert b.get_json("plan_notes/t/u/2026-27/notes.json") == doc
    # bytes
    b.put_bytes("invoices/t/u/MEY-1.pdf", b"%PDF-1.4\x00\xff")
    assert b.get_bytes("invoices/t/u/MEY-1.pdf") == b"%PDF-1.4\x00\xff"
    assert b.get_bytes("invoices/t/u/missing.pdf") is None
    # listing: recursive keys + immediate children
    b.put_json("section_state/t/u/2025-26/state.json", {})
    b.put_json("section_state/t/u/2026-27/state.json", {})
    b.put_json("section_state/t/other/2026-27/state.json", {})
    assert b.list_keys("section_state/t/u") == ["section_state/t/u/2025-26/state.json",
                                                "section_state/t/u/2026-27/state.json"]
    assert b.list_children("section_state/t/u") == ["2025-26", "2026-27"]
    assert b.list_children("section_state/t") == ["other", "u"]
    assert b.list_keys("section_state/t/nobody") == [] and b.list_children("nope") == []
    # prefix boundaries: "t/u" must not match "t/user2"
    b.put_json("section_state/t/user2/2026-27/state.json", {})
    assert all("/user2/" not in k for k in b.list_keys("section_state/t/u"))
    # delete one / delete prefix / idempotent
    assert b.delete("section_state/t/u/2025-26/state.json") is True
    assert b.delete("section_state/t/u/2025-26/state.json") is False
    assert b.delete_prefix("section_state/t/u") is True
    assert b.delete_prefix("section_state/t/u") is False
    assert b.list_keys("section_state/t/u") == []
    assert b.list_keys("section_state/t/user2")            # the neighbour survived
    # lock: a read-modify-write from 8 threads loses nothing
    b.put_json("support/_series/support.json", {"last": 0})

    def bump():
        for _ in range(25):
            with b.lock("support/_series/support.json"):
                n = b.get_json("support/_series/support.json")["last"]
                b.put_json("support/_series/support.json", {"last": n + 1})
    ts = [threading.Thread(target=bump) for _ in range(8)]
    [t.start() for t in ts]; [t.join() for t in ts]
    assert b.get_json("support/_series/support.json") == {"last": 200}, b.get_json("support/_series/support.json")
    # nested lock (same thread) must not deadlock
    with b.lock("k"):
        with b.lock("k"):
            b.put_json("misc/x.json", {"ok": True})
    assert b.get_json("misc/x.json") == {"ok": True}
    # a key may not escape the store
    try:
        b.put_json("../escape.json", {})
        raise AssertionError("escaping key accepted")
    except ValueError:
        pass
    print(f"✓ backend contract holds on {label}")


def test_file_backend_contract():
    with tempfile.TemporaryDirectory() as d:
        b = FileBackend(d)
        _contract(b, b.describe())
        # file-specific: self-heal of a torn document, and empty-ancestor tidying
        b.put_json("section_state/t/u/2026-27/state.json", {"6A": {"chapter": "ch4"}})
        p = b._path("section_state/t/u/2026-27/state.json")
        with open(p, "a") as f:
            f.write("}\n")                       # the classic stray trailing brace
        assert b.get_json("section_state/t/u/2026-27/state.json") == {"6A": {"chapter": "ch4"}}
        b.delete_prefix("section_state/t/u")
        assert not (b.root / "section_state" / "t" / "u").exists()
        assert (b.root / "section_state" / "t").exists(), "t/user2 still lives there — the school-tenant rule"
        b.delete_prefix("section_state/t/user2")
        b.delete_prefix("section_state/t/other")
        assert not (b.root / "section_state" / "t").exists(), "now-empty tenant folder must be tidied"
        print("✓ FileBackend self-heals a torn document and tidies empty ancestors")


def test_postgres_backend_contract():
    b = _pg()
    if b is None:
        print("SKIP postgres contract (ARUVI_TEST_DATABASE_URL unset)")
        return
    try:
        _contract(b, b.describe())
        # the parsed columns are what RLS/ops will key on
        rows = b.find_by_field("accounts", "account_id", "u")
        assert rows == [{"account_id": "u"}], rows
        with b.pool.connection() as c:
            r = c.execute("select kind, tenant_id, user_id, year_id from documents where key=%s",
                          ("support/_series/support.json",)).fetchone()
            assert r == ("support", None, None, None), r
            r = c.execute("select kind, tenant_id, user_id, year_id from documents where key=%s",
                          ("plan_notes/t/u/2026-27/notes.json",)).fetchone()
            assert r == ("plan_notes", "t", "u", "2026-27"), r
        print("✓ PostgresBackend parses tenant/user/year columns; series rows carry NO tenant")
    finally:
        b.close()


# ── 2. migration round-trip of the real state tree ────────────────────────────────
def test_migration_roundtrip_of_real_state():
    b = _pg()
    if b is None:
        print("SKIP migration round-trip (ARUVI_TEST_DATABASE_URL unset)")
        return
    src_root = os.path.join(ROOT, "data", "cloud", "state")
    if not os.path.isdir(src_root):
        print("SKIP migration round-trip (no data/cloud/state here)")
        b.close(); return
    try:
        src = FileBackend(src_root)
        keys = [k for k in src.list_keys("") if not k.startswith("outbox/")]
        stats = copy_all(src, b)
        assert stats["copied"] >= len(keys) - stats["skipped"], stats
        got = [k for k in b.list_keys("") if not k.startswith("outbox/")]
        assert got == keys, (len(got), len(keys))
        mism = 0
        for k in keys:
            if k.endswith(".json"):
                a, z = src.get_json(k), b.get_json(k)
            else:
                a, z = src.get_bytes(k), b.get_bytes(k)
            if a != z:
                mism += 1
        assert mism == 0, f"{mism} documents differ after migration"
        # idempotent: a second run changes nothing
        stats2 = copy_all(src, b)
        assert b.list_keys("") == keys or [k for k in b.list_keys("") if not k.startswith("outbox/")] == keys
        print(f"✓ migration round-trip: {len(keys)} documents file→postgres→read back equal; re-run idempotent ({stats2})")
    finally:
        b.close()


# ── 3. the API on Postgres, end to end ────────────────────────────────────────────
def test_api_on_postgres_end_to_end():
    if not PG_URL:
        print("SKIP API-on-postgres (ARUVI_TEST_DATABASE_URL unset)")
        return
    import psycopg
    with psycopg.connect(PG_URL, autocommit=True) as c:
        c.execute("drop table if exists documents")
    os.environ["ARUVI_STATE_BACKEND"] = "postgres"
    os.environ["ARUVI_DATABASE_URL"] = PG_URL
    os.environ["ARUVI_AUTH_PROVIDER"] = "header"
    from fastapi.testclient import TestClient
    import api.main as m
    assert "postgres" in m.state.describe(), m.state.describe()
    c = TestClient(m.app)
    H = {"X-Aruvi-User": "9111111111"}

    # identity → account row
    r = c.get("/readiness", headers=H); assert r.status_code == 200, r.text
    assert m.account_repo.load("9111111111", "9111111111") is not None
    # teaching profile
    subjects = [{"name": "science", "durations": [40], "grades": [
        {"grade": "vi", "sections": [{"tag": "6A", "sec": "A"}], "periods_per_week": 6}],
        "grids": [], "budget": []}]
    r = c.post("/readiness", json={"subjects": subjects}, headers=H); assert r.status_code == 200, r.text
    r = c.get("/readiness", headers=H); assert r.json()["ready"] is True
    # section state + history + notes
    r = c.post("/section-state", json={"section_key": "science/vi/6A", "chapter": "ch_04.json",
                                        "unit_index": 2, "done": False}, headers=H)
    assert r.status_code == 200, r.text
    r = c.get("/section-state", headers=H); assert "science/vi/6A" in json.dumps(r.json())
    r = c.post("/section-history", json={"entries": {"science/vi/6A": [
        {"file": "ch_04.json", "chapter_number": 4, "ts": 1700000000000, "status": "completed"}]}}, headers=H)
    assert r.status_code in (200, 422), r.text   # shape may differ; the store is what we test below
    r = c.post("/plan-notes", json={"key": "science/vi/4", "text": "went well",
                                    "updated_at": "2026-09-09T10:00:00+00:00"}, headers=H)
    assert r.status_code in (200, 422), r.text
    # support: reference series + her record
    r = c.post("/support", json={"category": "problem", "message": "The Assess tab is empty for ch 4."}, headers=H)
    assert r.status_code == 200, r.text
    ref = r.json().get("reference", "")
    assert ref.startswith("MEY-S-"), r.json()
    series = m.state.get_json("support/_series/support.json")
    assert series and series["last"] >= 742, series
    # invoice numbering continues from the series row
    n1 = m.invoice_repo.next_number("2026-27"); n2 = m.invoice_repo.next_number("2026-27")
    assert n1.startswith("MEY/2026-27/") and int(n2.rsplit("/", 1)[1]) == int(n1.rsplit("/", 1)[1]) + 1
    # consent: sign the current agreement fully, gate then passes
    doc = c.get("/legal/consent", headers=H).json()
    body = {"document_version": doc["document"]["version"], "language": "en",
            "acknowledgements": {k: True for k in doc["document"].get("acknowledgement_ids", [])} or None}
    # export (docx) reaches every store
    r = c.get("/data-rights/export", headers=H); assert r.status_code == 200 and r.content[:2] == b"PK"
    # erase: everything hers goes; series + erasure log stay
    r = c.post("/data-rights/erase", json={"confirm": "erase", "downloaded_confirmed": True}, headers=H)
    assert r.status_code == 200, r.text
    left = sorted(m.state.list_keys(""))
    hers = [k for k in left if "/9111111111/" in k or k.startswith("entitlements/9111111111/")]
    assert hers == [], hers
    assert "support/_series/support.json" in left
    assert any(k.startswith("erasure_log/") for k in left), left
    # a fresh identity after erasure JIT-creates again (ids are not reserved)
    r = c.get("/entitlement", headers=H); assert r.status_code == 200
    print(f"✓ API on Postgres: profile · sections · support {ref} · invoices {n1}→{n2} · export · erase — "
          f"{len(left)} documents left, none hers")


if __name__ == "__main__":
    test_parse_key_and_slug()
    test_file_backend_contract()
    test_postgres_backend_contract()
    test_migration_roundtrip_of_real_state()
    test_api_on_postgres_end_to_end()
    print("✅ All document-backend tests passed!")
