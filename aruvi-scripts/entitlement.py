"""Founder entitlement CLI — grant, expire, revoke and inspect access with no gateway.

Administrative architecture Step 5's "done" test: the founder can operate subscriptions
by hand. Runs against the same file adapters the API uses (honours ARUVI_STATE_DIR).

Usage (from the repo root):
  python3 aruvi-scripts/entitlement.py status  <tenant>
  python3 aruvi-scripts/entitlement.py grant   <tenant> [--plan individual_annual]
          [--scopes social_sciences/middle,science/secondary | --scopes "*"]
          [--until YYYY-MM-DD] [--source manual]
  python3 aruvi-scripts/entitlement.py revoke  <tenant>          # expire now
  python3 aruvi-scripts/entitlement.py trial-reset <tenant>      # fresh 3-chapter trial

Scopes are "{subject}/{stage}" (stage: preparatory | middle | secondary); "*" = all.
`grant` with no --scopes grants "*". `trial-reset` is a testing aid for the persona
runs — it hands the tenant a brand-new trial as if she had never generated.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from api import config  # noqa: E402
from aruvi_core.ports import Entitlement  # noqa: E402
from aruvi_core.adapters.entitlement_repository_file import EntitlementRepositoryFileImpl  # noqa: E402
from aruvi_core.adapters.manual_billing_provider import ManualBillingProvider  # noqa: E402


def main() -> int:
    ap = argparse.ArgumentParser(description="Founder entitlement operations (no gateway).")
    ap.add_argument("action", choices=["status", "grant", "revoke", "trial-reset"])
    ap.add_argument("tenant", help="tenant id (== user id for individual teachers)")
    ap.add_argument("--plan", default="individual_annual")
    ap.add_argument("--scopes", default="*",
                    help='comma-separated "{subject}/{stage}" entries, or "*"')
    ap.add_argument("--until", default="", help="ISO date; default = +365 days")
    ap.add_argument("--source", default="manual",
                    choices=["manual", "web", "ios", "android"])
    args = ap.parse_args()

    repo = EntitlementRepositoryFileImpl(config.STATE_DIR)
    provider = ManualBillingProvider(repo)

    if args.action == "status":
        print(json.dumps(provider.fetch_status(args.tenant), indent=2))
    elif args.action == "grant":
        scopes = ["*"] if args.scopes.strip() == "*" else [
            s.strip() for s in args.scopes.split(",") if s.strip()]
        print(json.dumps(provider.create_subscription(
            args.tenant, args.plan, scopes=scopes,
            valid_until=args.until, source=args.source), indent=2))
    elif args.action == "revoke":
        print(json.dumps(provider.cancel(args.tenant), indent=2))
    elif args.action == "trial-reset":
        repo.save(args.tenant, Entitlement(plan_id="trial", status="trial",
                                           source="trial", scopes=["*"]))
        print(json.dumps(provider.fetch_status(args.tenant), indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
