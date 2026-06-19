"""English subject package. Importing it registers the plugin with the core registry."""
from __future__ import annotations

from .. import register
from .subject import EnglishSubject

register(EnglishSubject())

__all__ = ["EnglishSubject"]
