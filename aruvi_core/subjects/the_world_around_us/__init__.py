"""The World Around Us subject package. Importing it registers the plugin."""
from __future__ import annotations

from .. import register
from .subject import TheWorldAroundUsSubject

register(TheWorldAroundUsSubject())

__all__ = ["TheWorldAroundUsSubject"]
