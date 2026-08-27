"""Founder erase CLI — wipe one teacher exactly as POST /data-rights/erase does.

Runs the SAME DataRightsServiceFileImpl.erase() the API route runs, against the same
file adapters (honours ARUVI_STATE_DIR), so it can never drift from what a teacher's
own "delete my account" button does — and it works with the API stopped.

Usage (from the repo root):
  python3 aruvi-scripts/erase.py <user> [--yes] [--with-consent]

  --yes           skip the typed confirmation (scripts only — there is no undo)
  --with-consent  ALSO delete the consent-ledger row outright.

                  ★ Rarely needed since 2026-08-27. A plain erase now SUPERSEDES the
                  ledger (stamps `superseded_at`) instead of leaving it standing, so an
                  erased teacher who returns DOES re-take the six ticks — which is what
                  this flag used to exist to simulate. The row is retained as evidence
                  (agreement §G) but no longer binds. Use --with-consent only when you
                  want no trace of the signature at all, e.g. to test the ledger's own
                  creation. Never appropriate in production.

tenant_id == user_id for individual teachers (the ICP), which is what makes the
subscription/entitlement record part of the wipe.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import config  # noqa: E402
from aruvi_core.adapters.data_rights_service_file import DataRightsServiceFileImpl  # noqa: E402
from aruvi_core.adapters.consent_repository_file import ConsentRepositoryFileImpl  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Erase one teacher's account and all her data.")
    ap.add_argument("user", help="user id (== tenant id for an individual teacher)")
    ap.add_argument("--yes", action="store_true", help="skip the typed confirmation")
    ap.add_argument("--with-consent", action="store_true",
                    help="also delete the retained consent-ledger entry (testing only)")
    args = ap.parse_args()
    tenant = user = args.user

    if not args.yes:
        print(f"This permanently erases EVERYTHING for '{user}': profile, notes, section "
              f"progress, allocations, prepared plans, subscription and account record.")
        print(f"State dir: {config.STATE_DIR}")
        if input('Type "erase" to confirm: ').strip().lower() != "erase":
            print("aborted — nothing was touched.")
            return 1

    service = DataRightsServiceFileImpl(config.STATE_DIR)
    receipt = service.erase(tenant, user)

    out = {
        "status": "erased" if receipt.erased else "nothing_to_erase",
        "erased": receipt.erased,
        "kept": [k["what"] for k in receipt.kept],
        "erased_at": receipt.erased_at,
    }

    if args.with_consent:
        path = ConsentRepositoryFileImpl(config.STATE_DIR)._path(tenant)
        if path.exists():
            path.unlink()
            out["consent_ledger"] = "deleted outright (testing) — no trace of the signature"
        else:
            out["consent_ledger"] = "none on file"
    else:
        # Kept as evidence, but no longer in force — see the module docstring.
        out["consent_ledger"] = ("retained as evidence (agreement §G) and SUPERSEDED "
                                 "— she WILL re-take the ticks")

    print(json.dumps(out, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
