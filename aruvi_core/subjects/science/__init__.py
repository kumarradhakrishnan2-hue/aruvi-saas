"""Science subject package. Importing it registers the plugin with the core registry.

Content (constitution / pedagogy text) is injected by the service layer at startup via a
re-registered instance; the default instance registered here is sufficient for the
normalizer (which needs no constitution) and for tests.
"""
from __future__ import annotations

from .. import register
from .subject import ScienceSubject, classify_stimulus

register(ScienceSubject())

__all__ = ["ScienceSubject", "classify_stimulus"]
