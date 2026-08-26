"""File-based implementation of AccountRepository.

Persists a teacher's account + tenant record as JSON at
ARUVI_STATE_DIR/accounts/{tenant_id}/{user_id}/account.json (user_id == account_id).

This is administrative_architecture.md Step 0's reference adapter: the durable record
that billing, privacy, notifications and the institutional tier all hang off. It is
deliberately NOT year-scoped — the subscription is rolling (§2.5) — and it is NOT the
teaching profile (that stays in ReadinessRepository, un-year-scoped for its own reason:
the class list carries across years, §2.7).

`tenant_id` and `account_id` are stored as SEPARATE fields that today happen to be
equal (an individual teacher is her own tenant). Nothing in this adapter assumes they
match — that is the whole point of Step 0.

The partner's cloud adapter swaps in behind the same AccountRepository port;
`api/main.py:_current_identity()` is the only caller that resolves a request to an
Account, so identity derivation never scatters.
"""
import json
from dataclasses import asdict
from pathlib import Path
from typing import Optional

from aruvi_core.ports import Account, AccountRepository


def _slug(s: str) -> str:
    """Filesystem-safe slug for a tenant/user id (defends against path traversal)."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class AccountRepositoryFileImpl(AccountRepository):
    """File-based account + tenant record store."""

    def __init__(self, data_dir: str):
        """
        Args:
            data_dir: Base directory where the accounts/ folder lives (e.g. ARUVI_STATE_DIR).
        """
        self.data_dir = Path(data_dir)
        self.accounts_dir = self.data_dir / "accounts"

    def _path(self, tenant_id: str, user_id: str) -> Path:
        return self.accounts_dir / _slug(tenant_id) / _slug(user_id) / "account.json"

    def load(self, tenant_id: str, user_id: str) -> Optional[Account]:
        """Load an account record, or None if the caller has none yet."""
        path = self._path(tenant_id, user_id)
        if not path.exists():
            return None
        try:
            with open(path, "r") as f:
                raw = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            raise ValueError(f"Failed to load account from {path}: {e}")
        return self._from_raw(raw)

    def save(self, account: Account) -> None:
        """Create or fully replace an account record (small, always written whole)."""
        path = self._path(account.tenant_id, account.account_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        try:
            with open(path, "w") as f:
                json.dump(asdict(account), f, indent=2)
        except IOError as e:
            raise ValueError(f"Failed to save account to {path}: {e}")

    def find_by_email(self, email: str) -> Optional[Account]:
        """Look an account up by email (case-insensitive), or None.

        ★ AMBIGUITY IS None, NOT "the first one" (2026-08-26). Email sign-in resolves an
        address to the account it belongs to, so returning an arbitrary winner when two
        accounts share an address would sign a teacher into SOMEONE ELSE'S data. Nothing
        enforces email uniqueness at the file layer (two mobiles can register the same
        address, deliberately or by typo), so a duplicate is a real state — and the only
        safe answer to "whose account is this?" is "I cannot tell". Callers fall back to
        the mobile, which is always unambiguous.
        """
        matches = self.find_all_by_email(email)
        return matches[0] if len(matches) == 1 else None

    def find_all_by_email(self, email: str) -> list:
        """Every account carrying this email (case-insensitive). Ordinarily 0 or 1; a
        longer list means the address is shared and cannot identify anyone on its own.

        Empty emails never match — dev accounts have no email. A linear scan over the
        account files is fine for the reference adapter; the partner's DB adapter does
        this with an index (and can enforce a UNIQUE constraint the file store cannot).
        """
        needle = (email or "").strip().lower()
        if not needle or not self.accounts_dir.exists():
            return []
        found = []
        for path in sorted(self.accounts_dir.glob("*/*/account.json")):
            try:
                with open(path, "r") as f:
                    raw = json.load(f)
            except (json.JSONDecodeError, IOError):
                continue  # one corrupt record must not break lookup for everyone
            if str(raw.get("email", "")).strip().lower() == needle:
                found.append(self._from_raw(raw))
        return found

    def delete(self, tenant_id: str, user_id: str) -> None:
        """Remove the account record (administrative_architecture.md §2.6 — only the
        record itself; the full erase traversal is Step 4's DataRightsService). No-op if
        absent. On mounts that forbid unlink, falls back to overwriting with a
        pending_deletion tombstone so the action never errors."""
        path = self._path(tenant_id, user_id)
        if not path.exists():
            return
        try:
            path.unlink()
        except OSError:
            with open(path, "w") as f:
                json.dump({"account_id": _slug(user_id), "tenant_id": _slug(tenant_id),
                           "display_name": "", "status": "pending_deletion"}, f, indent=2)

    @staticmethod
    def _from_raw(raw: dict) -> Account:
        """Build an Account from stored JSON, tolerating missing optional fields so old
        records survive dataclass growth."""
        return Account(
            account_id=str(raw.get("account_id", "")),
            tenant_id=str(raw.get("tenant_id", "")),
            display_name=str(raw.get("display_name", "")),
            email=str(raw.get("email", "")),
            phone=str(raw.get("phone", "")),
            locale=str(raw.get("locale", "en-IN")),
            school_name=str(raw.get("school_name", "")),
            role=str(raw.get("role", "")),
            state=str(raw.get("state", "")),
            city=str(raw.get("city", "")),
            status=str(raw.get("status", "active")),
            created_at=str(raw.get("created_at", "")),
            consent=dict(raw.get("consent") or {}),
            notify=dict(raw.get("notify") or {}),
            # Absent on every record written before 2026-08-26 — an empty string there
            # correctly means "never offered", so old accounts get their one offer.
            tour_offered_at=str(raw.get("tour_offered_at") or ""),
        )
