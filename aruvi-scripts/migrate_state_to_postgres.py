#!/usr/bin/env python3
"""Move Bucket B from the folder tree to Postgres — Track C (2026-09-09).

    python3 aruvi-scripts/migrate_state_to_postgres.py --dry-run
    python3 aruvi-scripts/migrate_state_to_postgres.py            # copy + verify
    python3 aruvi-scripts/migrate_state_to_postgres.py --verify   # compare only

Source: the file store at ARUVI_STATE_DIR (default data/cloud/state/).
Target: ARUVI_DATABASE_URL (the Supabase connection string; the `documents` table is
        created if absent — document_backend.SCHEMA_SQL).

There is no schema to design here and nothing to transform: the Postgres backend keys
rows by the SAME '/'-joined key the folder layout used, so migration is `copy_all` —
every document read through FileBackend and written through PostgresBackend, JSON as
jsonb, invoice PDFs as bytea. Idempotent: re-running rewrites the same keys, so a
partial run is finished by running again. `outbox/` (the dev mail spool) is skipped —
it is not teacher state.

VERIFY reads every key back from Postgres and compares it to the file, document by
document, and reports the first difference. Nothing is deleted on either side, ever:
the folder tree stays as the pre-migration snapshot until you choose to remove it.

The API switches with two env vars, on Render or locally:
    ARUVI_STATE_BACKEND=postgres  ARUVI_DATABASE_URL=postgresql://…
and switches BACK by unsetting them — the folder tree is untouched by the migration.
"""
from __future__ import annotations

import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from api import config  # noqa: E402
from aruvi_core.adapters.document_backend import FileBackend, PostgresBackend  # noqa: E402

SKIP_PREFIXES = ("outbox/",)


def _keys(b):
    return [k for k in b.list_keys("") if not k.startswith(SKIP_PREFIXES)]


def verify(src, dst) -> int:
    sk, dk = _keys(src), _keys(dst)
    missing = sorted(set(sk) - set(dk))
    extra = sorted(set(dk) - set(sk))
    diff = []
    for k in sk:
        if k in missing:
            continue
        if k.endswith(".json"):
            same = src.get_json(k) == dst.get_json(k)
        else:
            same = src.get_bytes(k) == dst.get_bytes(k)
        if not same:
            diff.append(k)
    print(f"files: {len(sk)} documents · postgres: {len(dk)} documents")
    print(f"missing in postgres: {len(missing)} · only in postgres: {len(extra)} · differing: {len(diff)}")
    for label, lst in (("missing", missing), ("extra", extra), ("differs", diff)):
        for k in lst[:10]:
            print(f"  {label}: {k}")
    return 0 if not missing and not diff else 1


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="list what would be copied; write nothing")
    ap.add_argument("--verify", action="store_true", help="compare only (no copy)")
    ap.add_argument("--database-url", default=config.DATABASE_URL, help="default: ARUVI_DATABASE_URL")
    ap.add_argument("--state-dir", default=config.STATE_DIR, help="default: ARUVI_STATE_DIR")
    args = ap.parse_args()

    src = FileBackend(args.state_dir)
    keys = _keys(src)
    print(f"source: {src.describe()} — {len(keys)} documents"
          f" ({sum(1 for k in keys if not k.endswith('.json'))} binary)")
    by_kind = {}
    for k in keys:
        by_kind[k.split('/')[0]] = by_kind.get(k.split('/')[0], 0) + 1
    for kind, n in sorted(by_kind.items()):
        print(f"  {kind:18s} {n}")

    if args.dry_run:
        print("dry run — nothing written.")
        return 0
    if not args.database_url:
        print("error: ARUVI_DATABASE_URL (or --database-url) is required", file=sys.stderr)
        return 2

    dst = PostgresBackend(args.database_url)
    try:
        print(f"target: {dst.describe()}")
        if not args.verify:
            stats = _copy_filtered(src, dst)
            print(f"copied {stats['copied']} · skipped {stats['skipped']}")
        return verify(src, dst)
    finally:
        dst.close()


def _copy_filtered(src, dst):
    copied = skipped = 0
    for key in _keys(src):
        if key.endswith(".json"):
            doc = src.get_json(key)
            if doc is None:
                skipped += 1; continue
            dst.put_json(key, doc)
        else:
            data = src.get_bytes(key)
            if data is None:
                skipped += 1; continue
            dst.put_bytes(key, data)
        copied += 1
    return {"copied": copied, "skipped": skipped}


if __name__ == "__main__":
    sys.exit(main())
