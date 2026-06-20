"""Shared normalization helpers used by subject plugins (not subject-specific).

Lives here so visual-stimulus typing is defined ONCE — the prototype's recurring class of
bug was a renderer dumping raw SVG/markup as prose. Subjects classify; the renderer trusts
the type.
"""
from __future__ import annotations

from typing import Any, List

from .view_model import StimulusType, VisualStimulus


def classify_stimulus(raw: str) -> VisualStimulus:
    """SVG > pipe-table > prose. Returns a typed VisualStimulus the renderer keys off."""
    s = (raw or "").strip()
    if not s:
        return VisualStimulus(StimulusType.NONE, "")
    if s.lower().startswith("<svg") and "</svg>" in s.lower():
        return VisualStimulus(StimulusType.SVG, s)
    if any(line.count("|") >= 2 for line in s.splitlines()):
        return VisualStimulus(StimulusType.TABLE, s)
    return VisualStimulus(StimulusType.PROSE, s)


def normalize_options(raw: Any) -> tuple:
    """Options may be plain strings OR dicts like {label, text, is_correct}.
    Return (list_of_display_texts, answer_label) so the renderer shows clean text and can
    mark the correct one. Generic — used by every subject."""
    options: List[str] = []
    answer = ""
    for o in raw or []:
        if isinstance(o, dict):
            txt = o.get("text") or o.get("option") or o.get("label") or ""
            options.append(str(txt))
            if o.get("is_correct"):
                answer = str(o.get("label") or txt)
        elif str(o).strip():
            options.append(str(o))
    return options, answer


def as_list(v: Any) -> List[str]:
    """Coerce a string / list / None field into a clean list of non-empty strings."""
    if v is None or v == "":
        return []
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    return [str(v)]


_TEXTISH = ("text", "activity", "description", "task_brief", "item", "prompt")


def text_lines(items: Any) -> List[str]:
    """Turn a list of strings OR dicts into display lines, pulling the first text-ish field
    from dicts (or 'ref'+'title' for textbook segments). Avoids dumping raw dicts."""
    out: List[str] = []
    for it in items or []:
        if isinstance(it, dict):
            picked = next((str(it[f]) for f in _TEXTISH if it.get(f)), "")
            if not picked:
                picked = " ".join(str(it[k]) for k in ("ref", "title") if it.get(k))
            if picked:
                out.append(picked)
        elif str(it).strip():
            out.append(str(it))
    return out


def band_lines(bands: Any) -> List[str]:
    """Time bands / phases shaped like {minutes, description|activity} -> 'mins: text'."""
    out: List[str] = []
    for b in bands or []:
        if isinstance(b, dict):
            mins = b.get("minutes", "")
            desc = b.get("description") or b.get("activity") or ""
            line = f"{mins}: {desc}".strip(": ").strip()
            if line:
                out.append(line)
        elif str(b).strip():
            out.append(str(b))
    return out
