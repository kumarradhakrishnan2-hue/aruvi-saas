"""Embedded Unicode fonts for the PDF exporters.

xhtml2pdf's built-in Helvetica / Times are Latin-1 only, so glyphs like ₹ (Rupee) and
Indian-language diacritics (ā, ṇ, …) render as tofu (dark squares). We embed DejaVu Sans /
Serif — which cover those glyphs — and register them UNDER the names the exporters already
use ("Helvetica" for body, "Georgia" for display), so no CSS font-family references need to
change: injecting `font_face_css()` at the top of a <style> block is enough.

The TTFs are bundled in aruvi_core/fonts/, so this works on any deploy with no system-font
dependency. Paths are absolute (computed from this file) so xhtml2pdf can open them directly.
"""

from __future__ import annotations

import os

_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "fonts")


def _u(name: str) -> str:
    return os.path.join(_DIR, name).replace("\\", "/")


def font_face_css() -> str:
    """@font-face block mapping "Helvetica" → DejaVu Sans and "Georgia" → DejaVu Serif
    (regular / bold / italic / bold-italic each). Prepend to a report's <style>."""
    return f"""
  @font-face {{ font-family: "Helvetica"; src: url("{_u('DejaVuSans.ttf')}"); }}
  @font-face {{ font-family: "Helvetica"; src: url("{_u('DejaVuSans-Bold.ttf')}"); font-weight: bold; }}
  @font-face {{ font-family: "Helvetica"; src: url("{_u('DejaVuSans-Oblique.ttf')}"); font-style: italic; }}
  @font-face {{ font-family: "Helvetica"; src: url("{_u('DejaVuSans-BoldOblique.ttf')}"); font-weight: bold; font-style: italic; }}
  @font-face {{ font-family: "Georgia"; src: url("{_u('DejaVuSerif.ttf')}"); }}
  @font-face {{ font-family: "Georgia"; src: url("{_u('DejaVuSerif-Bold.ttf')}"); font-weight: bold; }}
  @font-face {{ font-family: "Georgia"; src: url("{_u('DejaVuSerif-Italic.ttf')}"); font-style: italic; }}
  @font-face {{ font-family: "Georgia"; src: url("{_u('DejaVuSerif-BoldItalic.ttf')}"); font-weight: bold; font-style: italic; }}
"""
