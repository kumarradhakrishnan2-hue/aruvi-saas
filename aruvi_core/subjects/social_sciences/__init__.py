"""Social Sciences subject package. Importing it registers the plugin."""
from __future__ import annotations

from .. import register
from .subject import SocialSciencesSubject

register(SocialSciencesSubject())

__all__ = ["SocialSciencesSubject"]
