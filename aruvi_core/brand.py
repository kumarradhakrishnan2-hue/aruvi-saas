"""The MEYY wordmark for every surface that is not the web app (2026-09-03).

The web renders it live as an inline SVG (`web/app/components/MeyyMark.jsx`). PDFs
(xhtml2pdf), Word documents (python-docx) and email (Gmail on a school Android) cannot be
relied on to render SVG, so those three surfaces use ONE shipped raster —
`aruvi_core/brand/meyy-wordmark-pine.png` — pine stroke and the brand's red dots on a
transparent ground, drawn from the SAME paths as MeyyMark.jsx (`WORDMARK_SVG` below is the
source of record; `render_png()` regenerates the file when the mark changes, and needs
cairosvg only at that authoring moment — never at runtime). Bundled beside the fonts in
`aruvi_core/fonts/` for the same reason they are: a deploy with no system dependencies.

Geometry: the source viewBox is 0 0 400 110; this raster is TRIMMED to the ink
(x 12.5–385.5, y 0–102.5), so the M's edge is the image's edge and the letters' baseline is
the image's bottom — an inline picture then sits on the text baseline beside its kicker, as
the typeset "Meyy." used to. Aspect ratio is `WORDMARK_ASPECT` (width / height ≈ 3.64).

Sizing rule of thumb: the letters are 73 / 102.5 ≈ 0.71 of the image height, so to match a
serif at N pt (cap height ≈ 0.7 N) use an image height ≈ N.
"""

from __future__ import annotations

import io
import os
from typing import Any

# ── the mark, as drawn ────────────────────────────────────────────────────────────────
PINE = "#164436"          # stroke on paper (the web's --pine-d)
BRAND_RED = "#d63a2f"     # the two dots, the brand's own red (paper); the web bar lifts it

_PATHS = (
    '<path d="M20 95V22L62 66L104 22V95"/>'                                   # M
    '<path d="M148 22h64M148 58h64M148 94h64"/>'                              # E
    '<path d="M268 95V60L240 26M268 60l28-34M350 95V60L322 26M350 60l28-34"/>'  # Y Y
)
_TRIM_X, _TRIM_W, _TRIM_H = 12.5, 373.0, 102.5
WORDMARK_ASPECT = _TRIM_W / _TRIM_H


def wordmark_svg(stroke: str = PINE, dot: str = BRAND_RED, width: int | None = None,
                 height: int | None = None) -> str:
    """The wordmark as a standalone SVG document, trimmed to the ink."""
    size = ""
    if width and height:
        size = f' width="{width}" height="{height}"'
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{_TRIM_X} 0 {_TRIM_W} {_TRIM_H}"'
        f'{size} fill="none" stroke="{stroke}" stroke-width="15" stroke-linecap="round" '
        f'stroke-linejoin="round" role="img" aria-label="MEYY">'
        f'{_PATHS}'
        f'<circle cx="268" cy="9" r="9" fill="{dot}" stroke="none"/>'
        f'<circle cx="350" cy="9" r="9" fill="{dot}" stroke="none"/>'
        f'</svg>'
    )


WORDMARK_SVG = wordmark_svg()

# ── the shipped raster ────────────────────────────────────────────────────────────────
_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "brand")
PNG_NAME = "meyy-wordmark-pine.png"
PNG_PATH = os.path.join(_DIR, PNG_NAME).replace("\\", "/")
_PNG_SCALE = 4            # 1492 × 410 px — crisp at any print size the exports use


def wordmark_png_path() -> str:
    """Absolute path to the shipped PNG — what xhtml2pdf's <img src> wants (the fonts
    are referenced the same way, see pdf_fonts.py)."""
    return PNG_PATH


def wordmark_png_bytes() -> bytes:
    with open(PNG_PATH, "rb") as f:
        return f.read()


def render_png(path: str = PNG_PATH) -> str:
    """AUTHORING-TIME ONLY: regenerate the shipped raster from WORDMARK_SVG. Needs
    cairosvg (not a runtime dependency — the runtime only reads the file)."""
    import cairosvg  # noqa: WPS433 — deliberate late import
    w, h = round(_TRIM_W * _PNG_SCALE), round(_TRIM_H * _PNG_SCALE)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    cairosvg.svg2png(bytestring=wordmark_svg(width=w, height=h).encode("utf-8"),
                     write_to=path, output_width=w, output_height=h)
    return path


# ── per-surface helpers ───────────────────────────────────────────────────────────────
def pdf_img_html(height_pt: float = 16.0, extra_style: str = "") -> str:
    """An <img> for the xhtml2pdf templates, sized by HEIGHT in points (width follows
    the aspect). Both dimensions are stated because xhtml2pdf sizes replaced elements
    from their attributes, not from the file's pixel size.

    ⚠️ `align="top"` is load-bearing and deliberately NOT `baseline`. Measured on
    2026-09-03 against the typeset "Meyy." it replaces: xhtml2pdf maps an inline image's
    `baseline` to `bottom` (tags.py, "absbottom"/"baseline" → "bottom"), which hangs the
    picture 0.2 × its own height BELOW the text baseline — the kicker beside it then read
    as centred on the mark rather than sharing its baseline. In `imgVRange` the `top`
    case is `fontSize − h`, and for an inline image fontSize IS its draw height, so `top`
    computes to exactly zero: the image's bottom on the baseline, as the old text was.
    CSS `vertical-align` is no alternative — every keyword AND every length crashes the
    library (`imgVRange` receives a tuple) — so the HTML attribute is the only lever."""
    w = round(height_pt * WORDMARK_ASPECT, 1)
    return (f'<img src="{PNG_PATH}" alt="Meyy" align="top" '
            f'style="width:{w}pt;height:{height_pt}pt;{extra_style}"/>')


def add_wordmark(paragraph: Any, height_pt: float = 17.0) -> Any:
    """python-docx: append the wordmark as an inline picture run on `paragraph`. Returns
    the run so a caller can keep adding text (the LESSON STUDIO kicker) after it."""
    from docx.shared import Pt  # noqa: WPS433 — python-docx is optional at import time
    run = paragraph.add_run()
    run.add_picture(io.BytesIO(wordmark_png_bytes()), height=Pt(height_pt))
    return run


EMAIL_CID = "meyy-wordmark"   # the Content-ID the HTML templates reference


def email_inline_attachment() -> Any:
    """The wordmark as a CID inline image for the HTML emails. A `cid:` reference is the
    one form of inline image every major client (Gmail included) renders; data: URIs are
    stripped by Gmail and a hosted URL would need an origin Aruvi does not yet have."""
    from aruvi_core.ports import Attachment
    return Attachment(filename=PNG_NAME, content=wordmark_png_bytes(),
                      mime_type="image/png", content_id=EMAIL_CID)


def email_img_html(height_px: int = 24, extra_style: str = "") -> str:
    """The <img> that pairs with `email_inline_attachment()`. Width and height are stated
    as attributes (what mail clients honour) and `alt` carries the name for the client
    that has images off."""
    w = round(height_px * WORDMARK_ASPECT)
    return (f'<img src="cid:{EMAIL_CID}" width="{w}" height="{height_px}" alt="Meyy" '
            f'style="display:inline-block;vertical-align:baseline;border:0;{extra_style}"/>')
