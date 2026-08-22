"""Reference implementation of AuthProvider — the X-Aruvi-User header stub, made a port.

This is the SAME no-password dev identity Aruvi has always run on, now expressed
through the AuthProvider seam so the identity provider is swappable like every other
vendor: the "token" is simply the raw X-Aruvi-User header value, and verifying it means
slugging it and mapping it to an Identity whose tenant_id equals its user_id.

The partner's IdP adapter replaces this class with real token verification behind the
same `verify_token` method. `api/main.py:_current_identity()` is the single caller —
identity derivation lives there and nowhere else (administrative_architecture.md Step 0).
"""
from aruvi_core.ports import AuthProvider, Identity


def _slug(s: str) -> str:
    """Filesystem-safe slug for a user id (defends against path traversal). Matches the
    repository adapters' slug so the identity and the paths it addresses agree."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


class HeaderAuthProvider(AuthProvider):
    """Dev identity provider: the credential IS the user id."""

    def verify_token(self, token: str) -> Identity:
        """Accept any non-empty header value as a signed-in teacher ("local" when
        blank, preserving the pre-auth behaviour). tenant_id == user_id here — the
        individual-teacher stub; the account record is where the two may diverge."""
        uid = _slug(token or "")
        return Identity(user_id=uid, tenant_id=uid, role="teacher")
