"""One-shot migration for administrative-architecture Steps 0 + 1 (2026-08-22).

Re-files the existing on-disk dev data into year-scoped addressing and creates the
account + academic-year records the new identity layer reads:

  BEFORE   data/{kind}/{tenant}/{user}/<files>
  AFTER    data/{kind}/{tenant}/{user}/{year}/<files>      (the four year-scoped kinds)
           data/accounts/{tenant}/{user}/account.json       (new, Step 0)
           data/academic_years/{tenant}/{user}/years.json   (new, Step 1)

Year-scoped kinds: section_state, allocations, prepared_plans, plan_archive.
NOT touched: readiness/ (the teaching profile carries across years, spec §2.7) and
accounts / academic_years themselves.

IDEMPOTENT by construction — safe to re-run any number of times:
  * a {user} dir whose direct children are ONLY year-shaped dirs (NNNN-NN) is already
    migrated and is skipped;
  * account.json / years.json are only created when absent, never overwritten;
  * nothing is ever deleted — files are MOVED (os.rename within the same filesystem),
    and junk (.DS_Store) is left where it lies.

Identities are discovered across ALL Bucket-B kinds (union) so an account that exists
only under prepared_plans/ (kumar9/10/11 in the dev data) is not stranded.

Run from the repo root:  python3 aruvi-scripts/migrate_step01.py
Honours ARUVI_STATE_DIR like the app itself (api/config.py).
"""
import json
import os
import re
import sys
from datetime import date, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api import config  # noqa: E402  (dependency-free; derives STATE_DIR)

YEAR_SCOPED_KINDS = ["section_state", "allocations", "prepared_plans", "plan_archive"]
ALL_KINDS = YEAR_SCOPED_KINDS + ["readiness"]  # readiness counts for identity discovery only
_YEAR_RE = re.compile(r"^\d{4}-\d{2}$")


def default_year_id(today: date | None = None) -> str:
    """The academic year today falls in, April-anchored — matches api.main's bootstrap
    so the migrated folders and the first live request agree on the label."""
    today = today or date.today()
    start = today.year if today.month >= 4 else today.year - 1
    return f"{start}-{str(start + 1)[-2:]}"


def _is_junk(p: Path) -> bool:
    return p.name.startswith(".")  # .DS_Store and friends


def migrate_year_scope(state_dir: Path, year_id: str, report: list) -> None:
    """Move each {kind}/{tenant}/{user}'s direct contents into {user}/{year_id}/."""
    for kind in YEAR_SCOPED_KINDS:
        kind_dir = state_dir / kind
        if not kind_dir.is_dir():
            continue
        for tenant_dir in sorted(p for p in kind_dir.iterdir() if p.is_dir()):
            for user_dir in sorted(p for p in tenant_dir.iterdir() if p.is_dir()):
                entries = [p for p in user_dir.iterdir() if not _is_junk(p)]
                to_move = [p for p in entries
                           if not (p.is_dir() and _YEAR_RE.match(p.name))]
                if not to_move:
                    continue  # already migrated (or empty) — idempotent skip
                dest = user_dir / year_id
                dest.mkdir(exist_ok=True)
                for p in to_move:
                    target = dest / p.name
                    if target.exists():
                        report.append(f"  !! SKIP {p} — {target} already exists")
                        continue
                    os.rename(p, target)
                report.append(f"  moved {kind}/{tenant_dir.name}/{user_dir.name}: "
                              f"{len(to_move)} entr{'y' if len(to_move) == 1 else 'ies'} "
                              f"→ {year_id}/")


def discover_identities(state_dir: Path) -> set:
    """Every (tenant, user) pair present under any Bucket-B kind."""
    found = set()
    for kind in ALL_KINDS:
        kind_dir = state_dir / kind
        if not kind_dir.is_dir():
            continue
        for tenant_dir in (p for p in kind_dir.iterdir() if p.is_dir()):
            for user_dir in (p for p in tenant_dir.iterdir() if p.is_dir()):
                found.add((tenant_dir.name, user_dir.name))
    return found


def ensure_records(state_dir: Path, tenant: str, user: str, year_id: str,
                   report: list) -> None:
    """Create account.json and years.json for an identity if absent (never overwrite)."""
    now = datetime.now(timezone.utc).isoformat()

    acct_path = state_dir / "accounts" / tenant / user / "account.json"
    if not acct_path.exists():
        acct_path.parent.mkdir(parents=True, exist_ok=True)
        with open(acct_path, "w") as f:
            json.dump({
                "account_id": user, "tenant_id": tenant, "display_name": user,
                "email": "", "phone": "", "locale": "en-IN", "school_name": "",
                "status": "active", "created_at": now, "consent": {}, "notify": {},
            }, f, indent=2)
        report.append(f"  account created: {tenant}/{user}")

    years_path = state_dir / "academic_years" / tenant / user / "years.json"
    if not years_path.exists():
        start = int(year_id[:4])
        years_path.parent.mkdir(parents=True, exist_ok=True)
        with open(years_path, "w") as f:
            json.dump({
                "years": [{"year_id": year_id,
                           "starts_on": f"{start}-04-01",
                           "ends_on": f"{start + 1}-03-31",
                           "is_current": True}],
                "updated_at": now,
            }, f, indent=2)
        report.append(f"  year {year_id} opened: {tenant}/{user}")


def main() -> int:
    state_dir = Path(config.STATE_DIR)
    year_id = default_year_id()
    report: list = []
    print(f"Step 0+1 migration — state dir {state_dir}, year {year_id}")

    migrate_year_scope(state_dir, year_id, report)
    for tenant, user in sorted(discover_identities(state_dir)):
        ensure_records(state_dir, tenant, user, year_id, report)

    if report:
        print("\n".join(report))
        print(f"Done — {len(report)} action(s).")
    else:
        print("Nothing to do — already migrated.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
