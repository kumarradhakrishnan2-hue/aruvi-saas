"""The shared renderer — view model -> HTML (one renderer for all subjects)."""
from __future__ import annotations

from .html import render_assessment, render_lesson_plan, render_view, render_view_fragment

__all__ = ["render_view", "render_view_fragment", "render_lesson_plan", "render_assessment"]
