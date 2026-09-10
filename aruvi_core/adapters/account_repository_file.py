"""AccountRepository over the document backend (file or Postgres — Track C, 2026-09-09).

Persists a teacher's account + tenant record as one JSON document at key
accounts/{tenant_id}/{user_id}/account.json (user_id == account_id) — on disk under
ARUVI_STATE_DIR, or as a row of the `documents` table; see document_backend.py.

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
from dataclasses import asdict
from typing import Optional

from aruvi_core.ports import Account, AccountRepository
from aruvi_core.adapters.document_backend import as_backend, slug as _slug


class AccountRepositoryFileImpl(AccountRepository):
    """Account + tenant record store over a document backend."""

    def __init__(self, data_dir):
        """
        Args:
            data_dir: a DocumentBackend, or a directory (→ FileBackend at that root,
                      e.g. ARUVI_STATE_DIR — every existing call site and test).
        """
        self.backend = as_backend(data_dir)

    def _key(self, tenant_id: str, user_id: str) -> str:
        return f"accounts/{_slug(tenant_id)}/{_slug(user_id)}/account.json"

    def load(self, tenant_id: str, user_id: str) -> Optional[Account]:
        """Load an account record, or None if the caller has none yet."""
        raw = self.backend.get_json(self._key(tenant_id, user_id))
        if raw is None:
            return None
        if not isinstance(raw, dict):
            raise ValueError(f"Malformed account record at {self._key(tenant_id, user_id)}")
        return self._from_raw(raw)

    def save(self, account: Account) -> None:
        """Create or fully replace an account record (small, always written whole)."""
        self.backend.put_json(self._key(account.tenant_id, account.account_id), asdict(account))

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

        Empty emails never match — dev accounts have no email. The file backend scans
        every account document; the Postgres backend answers from an expression index
        on lower(body->>'email') (document_backend.SCHEMA_SQL) through `find_by_field`.
        """
        needle = (email or "").strip().lower()
        if not needle:
            return []
        finder = getattr(self.backend, "find_by_field", None)
        if finder is not None:
            raws = finder("accounts", "email", needle)
        else:
            raws = []
            for key in self.backend.list_keys("accounts"):
                if not key.endswith("/account.json"):
                    continue
                raw = self.backend.get_json(key)
                if isinstance(raw, dict) and str(raw.get("email", "")).strip().lower() == needle:
                    raws.append(raw)
        return [self._from_raw(r) for r in raws if isinstance(r, dict)]

    def delete(self, tenant_id: str, user_id: str) -> None:
        """Remove the account record (administrative_architecture.md §2.6 — only the
        record itself; the full erase traversal is Step 4's DataRightsService). No-op if
        absent (the file backend leaves an empty document on mounts that forbid
        unlink, so the action never errors)."""
        self.backend.delete(self._key(tenant_id, user_id))

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
            # Absent before 2026-09-04 — empty means "no notice version recorded".
            privacy_notice=dict(raw.get("privacy_notice") or {}),
        )
