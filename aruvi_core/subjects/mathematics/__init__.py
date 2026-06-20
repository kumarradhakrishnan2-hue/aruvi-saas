"""Mathematics subject package. Importing it registers the plugin (one plugin, stage-aware)."""
from __future__ import annotations

from .. import register
from .subject import MathematicsSubject

register(MathematicsSubject())

__all__ = ["MathematicsSubject"]
