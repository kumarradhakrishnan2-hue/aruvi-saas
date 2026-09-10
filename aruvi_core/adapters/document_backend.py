"""The document backend — ONE storage seam under every Bucket-B repository (Track C, 2026-09-09).

WHY THIS EXISTS. Every file adapter in this folder was the same shape: domain logic
(merge rules, timestamps, series counters, self-heal) wrapped around its own private
copy of "read the JSON at this path / write it atomically / delete it / list a folder".
The disk was already a document store — the folder path IS the key. So the move to
Postgres is not fifteen rewrites; it is that private copy, lifted out once, with two
implementations behind it:

  FileBackend      — today's layout, byte for byte (data/cloud/state/…), same atomic
                     temp-file + os.replace writes, same raw_decode self-heal. The default,
                     so every local run and every stdlib test is unchanged.
  PostgresBackend  — one `documents` table, `body jsonb`, keyed by the SAME '/'-joined
                     key the file layout used. Supabase Postgres is the cloud home
                     (CLOUD_DATA_MODEL.md §0). Migration = copy every key from one
                     backend to the other; there is no second schema to reason about.

THE PORTS STAY INDIVIDUAL. `AccountRepository`, `SectionHistoryRepository`, … are still
fifteen contracts, still implemented by the fifteen classes beside this file, and the
API and engine still talk to those. Only the bottom of each class changed: it addresses
`self.backend` by key instead of `open()` by path. A store that one day needs real
columns (analytics, relational queries) graduates to its own table BEHIND ITS OWN PORT,
one at a time, and nothing above notices.

KEY DISCIPLINE. A key is the relative path the file layout would have used:
  `section_state/{tenant}/{user}/{year}/state.json`, `accounts/{t}/{u}/account.json`,
  `invoices/_series/2026-27.json`, `consents/_ledger/{tenant}.json`.
The Postgres row also carries `kind`/`tenant_id`/`user_id`/`year_id` PARSED from the key
(best effort, for RLS and ops queries), but the key is the identity. A second segment
that starts with `_` (`_series`, `_ledger`) is NOT a tenant — that is exactly the
"outside the tenant shape, so the erase traversal cannot reach it" rule the folder
layout encoded, carried over as a NULL tenant column.

LOCKING. `lock(name)` serialises a read-modify-write. FileBackend: a per-name
threading.Lock (one process, as before). PostgresBackend: the same thread lock PLUS a
transaction-scoped advisory lock on the name, and every get/put inside the block runs
on that transaction's connection — so two API instances writing the same document can
no longer lose each other's update, which the file adapters' comments always said was
"the DB row-lock, later". That later is now.
"""
from __future__ import annotations

import json
import os
import tempfile
import threading
from contextlib import contextmanager
from pathlib import Path
from typing import Any, Dict, Iterator, List, Optional, Union

# Key parsing ─────────────────────────────────────────────────────────────────────
YEAR_KINDS = ("plan_notes", "section_state", "section_history", "allocations",
              "prepared_plans", "plan_archive")


def slug(s: str) -> str:
    """Key-safe slug for a tenant/user/year id (defends against path traversal). ONE
    copy now — every adapter used to carry its own, byte-identical."""
    s = str(s).strip() or "local"
    # Leading/trailing underscores are stripped too (the consent ledger's stricter rule,
    # now universal): a `_`-prefixed second segment means "not a tenant" (`_series`,
    # `_ledger`), so no tenant id may ever slug to one.
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-_") or "local"


def _norm(key: str) -> str:
    k = str(key or "").strip().strip("/")
    if ".." in k.split("/"):
        raise ValueError(f"key escapes the store: {key!r}")
    return k


def parse_key(key: str) -> Dict[str, Optional[str]]:
    """kind / tenant_id / user_id / year_id from a key, best effort; None where the
    layout has no such segment (series, ledgers, tenant-only stores)."""
    seg = _norm(key).split("/")
    kind = seg[0] if seg else None
    tenant = seg[1] if len(seg) > 2 and not seg[1].startswith("_") else None
    user: Optional[str] = None
    year: Optional[str] = None
    if tenant is not None:
        if kind == "entitlements":           # entitlements/{tenant}/entitlement.json
            user = None
        elif len(seg) > 3:                   # {kind}/{t}/{u}/…
            user = seg[2]
            if kind in YEAR_KINDS and len(seg) > 4:
                year = seg[3]
    return {"kind": kind, "tenant_id": tenant, "user_id": user, "year_id": year}


class DocumentBackend:
    """The interface. Subclasses implement the underscored primitives."""

    # ── JSON documents ──
    def get_json(self, key: str) -> Optional[Any]:
        raise NotImplementedError

    def put_json(self, key: str, doc: Any) -> None:
        raise NotImplementedError

    # ── opaque bytes (invoice PDFs) ──
    def get_bytes(self, key: str) -> Optional[bytes]:
        raise NotImplementedError

    def put_bytes(self, key: str, data: bytes) -> None:
        raise NotImplementedError

    # ── existence / removal ──
    def exists(self, key: str) -> bool:
        raise NotImplementedError

    def delete(self, key: str) -> bool:
        """Remove one document. False if it was not there."""
        raise NotImplementedError

    def delete_prefix(self, prefix: str) -> bool:
        """Remove everything under `prefix/`. False if nothing was there."""
        raise NotImplementedError

    # ── enumeration ──
    def list_keys(self, prefix: str) -> List[str]:
        """Every key under `prefix/` (any depth), sorted."""
        raise NotImplementedError

    def list_children(self, prefix: str) -> List[str]:
        """Immediate child NAMES under `prefix/` — the next path segment, distinct,
        sorted — whether that segment is a 'folder' or a document."""
        keys = self.list_keys(prefix)
        p = _norm(prefix)
        n = len(p) + 1 if p else 0
        return sorted({k[n:].split("/", 1)[0] for k in keys if k[n:]})

    # ── locking ──
    @contextmanager
    def lock(self, name: str) -> Iterator[None]:
        raise NotImplementedError

    # ── description, for boot logs ──
    def describe(self) -> str:
        return self.__class__.__name__


# ── File backend ───────────────────────────────────────────────────────────────────
class FileBackend(DocumentBackend):
    """The folder tree under a root — the layout every Bucket-B store has used since
    2026-06-28, unchanged."""

    def __init__(self, root: Union[str, Path]):
        self.root = Path(root)
        self._locks: Dict[str, threading.RLock] = {}
        self._locks_guard = threading.Lock()

    def describe(self) -> str:
        return f"files at {self.root}"

    def _path(self, key: str) -> Path:
        return self.root.joinpath(*_norm(key).split("/"))

    # JSON
    def get_json(self, key: str) -> Optional[Any]:
        path = self._path(key)
        if not path.exists():
            return None
        try:
            with open(path, "r", encoding="utf-8") as f:
                return json.load(f)
        except IOError:
            return None
        except json.JSONDecodeError:
            # SELF-HEAL (2026-07-03 rule): a file torn by the legacy non-atomic write
            # typically carries a stray trailing brace. raw_decode keeps the valid
            # leading object so a corrupt file still returns the REAL rows rather than
            # nothing; the next put_json rewrites it cleanly.
            try:
                with open(path, "r", encoding="utf-8") as f:
                    raw = f.read()
                obj, _ = json.JSONDecoder().raw_decode(raw.lstrip())
                return obj
            except Exception:
                return None

    def put_json(self, key: str, doc: Any) -> None:
        self._write_atomic(key, json.dumps(doc, indent=2, ensure_ascii=False).encode("utf-8"))

    # bytes
    def get_bytes(self, key: str) -> Optional[bytes]:
        path = self._path(key)
        if not path.exists():
            return None
        try:
            with open(path, "rb") as f:
                return f.read()
        except IOError:
            return None

    def put_bytes(self, key: str, data: bytes) -> None:
        self._write_atomic(key, bytes(data))

    def _write_atomic(self, key: str, payload: bytes) -> None:
        """Temp file in the same folder, fsync, os.replace — a reader sees the whole
        old document or the whole new one, never a torn one. Falls back to an in-place
        write on mounts that refuse the sidecar (repair_ppw.py learnt this)."""
        path = self._path(key)
        path.parent.mkdir(parents=True, exist_ok=True)
        tmp = None
        try:
            fd, tmp = tempfile.mkstemp(dir=str(path.parent), prefix=".doc-", suffix=".tmp")
            with os.fdopen(fd, "wb") as f:
                f.write(payload)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
            tmp = None
        except OSError:
            with open(path, "wb") as f:
                f.write(payload)
        finally:
            if tmp is not None and os.path.exists(tmp):
                try:
                    os.remove(tmp)
                except OSError:
                    pass

    # existence / removal
    def exists(self, key: str) -> bool:
        return self._path(key).is_file()

    def delete(self, key: str) -> bool:
        path = self._path(key)
        if not path.is_file():
            return False
        try:
            path.unlink()
        except OSError:
            # mounts that allow overwrite but not unlink → leave an empty document
            with open(path, "w", encoding="utf-8") as f:
                f.write("{}")
            return True
        self._tidy(path.parent)
        return True

    def delete_prefix(self, prefix: str) -> bool:
        import shutil
        path = self._path(prefix)
        if not path.is_dir():
            return False
        shutil.rmtree(path)
        self._tidy(path.parent)
        return True

    def _tidy(self, folder: Path) -> None:
        """Remove now-empty ancestors up to (never including) the store root — an
        empty folder named after a teacher is still a remnant (data_rights rule)."""
        try:
            while folder != self.root and folder.is_dir() and not any(folder.iterdir()):
                folder.rmdir()
                folder = folder.parent
        except OSError:
            pass

    # enumeration
    def list_keys(self, prefix: str) -> List[str]:
        base = self._path(prefix) if _norm(prefix) else self.root
        if not base.is_dir():
            return []
        out = []
        for p in base.rglob("*"):
            if p.is_file() and not p.name.startswith("."):
                out.append(p.relative_to(self.root).as_posix())
        return sorted(out)

    def list_children(self, prefix: str) -> List[str]:
        base = self._path(prefix) if _norm(prefix) else self.root
        if not base.is_dir():
            return []
        return sorted(p.name for p in base.iterdir() if not p.name.startswith("."))

    # locking
    @contextmanager
    def lock(self, name: str) -> Iterator[None]:
        with self._locks_guard:
            lk = self._locks.setdefault(name, threading.RLock())
        with lk:
            yield


# ── Postgres backend ───────────────────────────────────────────────────────────────
SCHEMA_SQL = """
create table if not exists documents (
  key        text primary key,
  kind       text not null,
  tenant_id  text,
  user_id    text,
  year_id    text,
  body       jsonb,
  blob       bytea,
  updated_at timestamptz not null default now()
);
create index if not exists documents_kind_tenant_idx on documents (kind, tenant_id, user_id);
create index if not exists documents_tenant_idx on documents (tenant_id);
-- accounts.find_all_by_email is the one non-key lookup in the product.
create index if not exists documents_account_email_idx
  on documents ((lower(body->>'email'))) where kind = 'accounts';
-- Defence in depth: the API holds the service role and bypasses RLS; a browser with the
-- anon key must see nothing. No policy = no access for non-owner roles.
alter table documents enable row level security;
"""


class PostgresBackend(DocumentBackend):
    """One `documents` table. Keys, bodies and behaviour identical to FileBackend."""

    def __init__(self, dsn: str, min_size: int = 1, max_size: int = 4,
                 ensure_schema: bool = True):
        try:
            import psycopg  # noqa: F401
            from psycopg_pool import ConnectionPool
        except ImportError as e:  # pragma: no cover
            raise RuntimeError("PostgresBackend needs psycopg[binary,pool] "
                               "(api/requirements.txt)") from e
        self.dsn = dsn
        self.pool = ConnectionPool(dsn, min_size=min_size, max_size=max_size,
                                   kwargs={"autocommit": True}, open=True)
        self._tls = threading.local()
        self._locks: Dict[str, threading.RLock] = {}
        self._locks_guard = threading.Lock()
        if ensure_schema:
            with self.pool.connection() as conn:
                conn.execute(SCHEMA_SQL)

    def describe(self) -> str:
        host = self.dsn.split("@")[-1].split("/")[0] if "@" in self.dsn else "postgres"
        return f"postgres at {host}"

    # A statement runs on the lock-holding transaction's connection when inside
    # lock(), else on a pooled autocommit connection.
    @contextmanager
    def _conn(self):
        held = getattr(self._tls, "conn", None)
        if held is not None:
            yield held
            return
        with self.pool.connection() as conn:
            yield conn

    @staticmethod
    def _cols(key: str) -> Dict[str, Optional[str]]:
        return parse_key(key)

    # JSON
    def get_json(self, key: str) -> Optional[Any]:
        from psycopg.types.json import Jsonb  # noqa: F401  (import check)
        k = _norm(key)
        with self._conn() as conn:
            row = conn.execute("select body from documents where key = %s", (k,)).fetchone()
        return row[0] if row else None

    def put_json(self, key: str, doc: Any) -> None:
        from psycopg.types.json import Jsonb
        k = _norm(key)
        c = self._cols(k)
        with self._conn() as conn:
            conn.execute(
                "insert into documents (key, kind, tenant_id, user_id, year_id, body, blob, updated_at) "
                "values (%s, %s, %s, %s, %s, %s, null, now()) "
                "on conflict (key) do update set body = excluded.body, blob = null, "
                "kind = excluded.kind, tenant_id = excluded.tenant_id, user_id = excluded.user_id, "
                "year_id = excluded.year_id, updated_at = now()",
                (k, c["kind"], c["tenant_id"], c["user_id"], c["year_id"], Jsonb(doc)))

    # bytes
    def get_bytes(self, key: str) -> Optional[bytes]:
        k = _norm(key)
        with self._conn() as conn:
            row = conn.execute("select blob, body from documents where key = %s", (k,)).fetchone()
        if not row:
            return None
        if row[0] is not None:
            return bytes(row[0])
        return json.dumps(row[1], indent=2, ensure_ascii=False).encode("utf-8")

    def put_bytes(self, key: str, data: bytes) -> None:
        k = _norm(key)
        c = self._cols(k)
        with self._conn() as conn:
            conn.execute(
                "insert into documents (key, kind, tenant_id, user_id, year_id, body, blob, updated_at) "
                "values (%s, %s, %s, %s, %s, null, %s, now()) "
                "on conflict (key) do update set blob = excluded.blob, body = null, "
                "kind = excluded.kind, tenant_id = excluded.tenant_id, user_id = excluded.user_id, "
                "year_id = excluded.year_id, updated_at = now()",
                (k, c["kind"], c["tenant_id"], c["user_id"], c["year_id"], bytes(data)))

    # existence / removal
    def exists(self, key: str) -> bool:
        with self._conn() as conn:
            return conn.execute("select 1 from documents where key = %s", (_norm(key),)).fetchone() is not None

    def delete(self, key: str) -> bool:
        with self._conn() as conn:
            cur = conn.execute("delete from documents where key = %s", (_norm(key),))
            return cur.rowcount > 0

    def delete_prefix(self, prefix: str) -> bool:
        p = _norm(prefix)
        with self._conn() as conn:
            if p:
                cur = conn.execute("delete from documents where left(key, %s) = %s",
                                   (len(p) + 1, p + "/"))
            else:
                cur = conn.execute("delete from documents")
            return cur.rowcount > 0

    # enumeration
    def list_keys(self, prefix: str) -> List[str]:
        p = _norm(prefix)
        with self._conn() as conn:
            if p:
                rows = conn.execute("select key from documents where left(key, %s) = %s order by key",
                                    (len(p) + 1, p + "/")).fetchall()
            else:
                rows = conn.execute("select key from documents order by key").fetchall()
        return [r[0] for r in rows]

    def find_by_field(self, kind: str, field: str, value: str) -> List[Any]:
        """Documents of `kind` whose top-level `field` equals `value`, case-insensitively.
        The one non-key lookup the product has (accounts by email); indexed for it."""
        with self._conn() as conn:
            rows = conn.execute(
                "select body from documents where kind = %s and lower(body->>%s) = lower(%s) order by key",
                (kind, field, value)).fetchall()
        return [r[0] for r in rows]

    # locking
    @contextmanager
    def lock(self, name: str) -> Iterator[None]:
        with self._locks_guard:
            lk = self._locks.setdefault(name, threading.RLock())
        with lk:
            if getattr(self._tls, "conn", None) is not None:
                yield            # nested: already inside a locked transaction
                return
            with self.pool.connection() as conn:
                with conn.transaction():
                    conn.execute("select pg_advisory_xact_lock(hashtext(%s))", (name,))
                    self._tls.conn = conn
                    try:
                        yield
                    finally:
                        self._tls.conn = None

    def close(self) -> None:
        self.pool.close()


# ── construction ───────────────────────────────────────────────────────────────────
def as_backend(x: Union[str, Path, DocumentBackend]) -> DocumentBackend:
    """Every repository constructor accepts either a backend or — for compatibility
    with every existing call site and test — a directory, which means FileBackend."""
    if isinstance(x, DocumentBackend):
        return x
    return FileBackend(x)


def copy_all(src: DocumentBackend, dst: DocumentBackend, prefix: str = "",
             overwrite: bool = True) -> Dict[str, int]:
    """Migration in one function: every key under `prefix` from src to dst. Bytes
    documents (invoice PDFs) travel as bytes, everything else as JSON. Idempotent —
    re-running rewrites the same keys."""
    copied = skipped = 0
    for key in src.list_keys(prefix):
        if not overwrite and dst.exists(key):
            skipped += 1
            continue
        if key.endswith(".json"):
            doc = src.get_json(key)
            if doc is None:
                skipped += 1
                continue
            dst.put_json(key, doc)
        else:
            data = src.get_bytes(key)
            if data is None:
                skipped += 1
                continue
            dst.put_bytes(key, data)
        copied += 1
    return {"copied": copied, "skipped": skipped}
