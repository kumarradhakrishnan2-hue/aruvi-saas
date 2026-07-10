"""Shared normalization helpers used by subject plugins (not subject-specific).

Lives here so visual-stimulus typing is defined ONCE — the prototype's recurring class of
bug was a renderer dumping raw SVG/markup as prose. Subjects classify; the renderer trusts
the type.
"""
from __future__ import annotations

import re
from typing import Any, List

from .view_model import Phase, StimulusType, VisualStimulus


def classify_stimulus(raw: str) -> VisualStimulus:
    """SVG > pipe-table > prose. Returns a typed VisualStimulus the renderer keys off.

    Table detection accepts TWO-column tables (one `|` per line), not just 3+ columns:
    the earlier rule (`any line has >= 2 pipes`) silently mis-typed 2-column tables — very
    common in assessment stimuli ("Region | Density", "Planet | Weight") — as PROSE, so the
    renderer dumped raw pipes. A block is a table when it has >= 2 pipe-bearing lines that
    dominate the block (>= half the non-empty lines). The old single-line >= 2-pipe rule is
    kept as a strict superset, so no previously-detected table regresses. Verse/prose (no
    pipes, e.g. EXTRACT_ANALYSIS extracts) stays PROSE."""
    s = (raw or "").strip()
    if not s:
        return VisualStimulus(StimulusType.NONE, "")
    if s.lower().startswith("<svg") and "</svg>" in s.lower():
        return VisualStimulus(StimulusType.SVG, s)
    lines = [ln for ln in s.splitlines() if ln.strip()]
    pipe_lines = [ln for ln in lines if "|" in ln]
    if (len(pipe_lines) >= 2 and len(pipe_lines) * 2 >= len(lines)) \
            or any(ln.count("|") >= 2 for ln in lines):
        return VisualStimulus(StimulusType.TABLE, s)
    return VisualStimulus(StimulusType.PROSE, s)


def parse_table(raw: str) -> dict:
    """Split pipe-delimited table text into {'header': [...], 'rows': [[...]]}.

    THE single place a pipe-table string is split into cells — every renderer (HTML/PDF
    export, the React on-screen view, the assessment 3b view) consumes this structure and
    NEVER re-splits the raw string itself (the recurring drift-bug class). Row 0 is the
    header; remaining lines are body rows. Empty/blank lines are dropped."""
    lines = [ln for ln in (raw or "").splitlines() if ln.strip()]
    cells = [[c.strip() for c in ln.split("|")] for ln in lines]
    if not cells:
        return {"header": [], "rows": []}
    return {"header": cells[0], "rows": cells[1:]}


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


# ── Phases: the timed spine (layout decision 2026-07-09) ──────────────────────────

_BAND_RE = re.compile(r"(\d+)\s*(?:–|—|-|to)\s*(\d+)")  # "0–5", "0-10", "0 to 5"


def parse_minutes_band(raw: Any) -> tuple:
    """Parse a raw minutes band string into (start_min, end_min) ints.

    The saved-plan library drifts between en-dash ("0–5"), hyphen ("0-10"), em-dash and
    spaced forms; key names drift too, but the band format is the same. Returns
    (None, None) when no range is found — the Phase then keeps only its raw `label`."""
    m = _BAND_RE.search(str(raw or ""))
    if not m:
        return None, None
    start, end = int(m.group(1)), int(m.group(2))
    if end < start:                      # defensive: a generator typo like "30–4"
        return None, None
    return start, end


def phases_from(bands: Any) -> List[Phase]:
    """Normalize raw phases/time_bands ({minutes, description|activity}) into typed Phases.

    This is where the minutes STOP being strings: parsed once, carried as ints. Every
    subject's timed spine goes through here — 'phases' (Science/English/Maths-prep+middle)
    and 'time_bands' (SS/TWAU/Maths-secondary) are the same shape apart from the text key."""
    out: List[Phase] = []
    for b in bands or []:
        if isinstance(b, dict):
            raw_min = str(b.get("minutes", "") or "")
            text = str(b.get("description") or b.get("activity") or "").strip()
            if not text and not raw_min:
                continue
            start, end = parse_minutes_band(raw_min)
            out.append(Phase(text=text, start_min=start, end_min=end, label=raw_min))
        elif str(b).strip():
            out.append(Phase(text=str(b).strip()))
    return out


def phase_tiling_issues(phases: List[Phase], duration_minutes: Any) -> List[str]:
    """Best-effort validation that phases tile 0 → the period's duration.

    Returns human-readable issue strings (empty list = clean). Never raises — saved plans
    are carried as-is; this feeds tests and any future generation-time QA, not rendering."""
    issues: List[str] = []
    if not phases:
        return ["no phases"]
    parsed = [(p.start_min, p.end_min) for p in phases]
    if any(s is None or e is None for s, e in parsed):
        return [f"unparseable band(s): {[p.label for p in phases if p.start_min is None]}"]
    if parsed[0][0] != 0:
        issues.append(f"first phase starts at {parsed[0][0]}, not 0")
    for (s1, e1), (s2, e2) in zip(parsed, parsed[1:]):
        if s2 != e1:
            issues.append(f"gap/overlap: {e1} -> {s2}")
    if duration_minutes and parsed[-1][1] != duration_minutes:
        issues.append(f"last phase ends at {parsed[-1][1]}, period is {duration_minutes} min")
    return issues
