"""Shared normalization helpers used by subject plugins (not subject-specific).

Lives here so visual-stimulus typing is defined ONCE — the prototype's recurring class of
bug was a renderer dumping raw SVG/markup as prose. Subjects classify; the renderer trusts
the type.
"""
from __future__ import annotations

import re
from typing import Any, List

from .view_model import Phase, StimulusType, VisualStimulus


def classify_stimulus(raw) -> VisualStimulus:
    """SVG > pipe-table > prose. Returns a typed VisualStimulus the renderer keys off.

    Table detection accepts TWO-column tables (one `|` per line), not just 3+ columns:
    the earlier rule (`any line has >= 2 pipes`) silently mis-typed 2-column tables — very
    common in assessment stimuli ("Region | Density", "Planet | Weight") — as PROSE, so the
    renderer dumped raw pipes. A block is a table when it has >= 2 pipe-bearing lines that
    dominate the block (>= half the non-empty lines). The old single-line >= 2-pipe rule is
    kept as a strict superset, so no previously-detected table regresses. Verse/prose (no
    pipes, e.g. EXTRACT_ANALYSIS extracts) stays PROSE.

    Accepts the STRUCTURED `{"type", "payload"}` stimulus shape too (SS secondary,
    constitution v2.7 onward: `source_text` primary-source extracts, and any future
    explicitly-typed visual). This is the single normalization point every subject port and
    assessment_norm funnel through, so dict support lands once for all subjects and both
    renderers. A declared type wins; an unknown/absent one falls back to the string
    heuristics on the payload. Non-string, non-dict input is treated as empty (NONE) rather
    than crashing."""
    if isinstance(raw, dict):
        payload = raw.get("payload", raw.get("content", ""))
        payload = payload if isinstance(payload, str) else ""
        t = str(raw.get("type", "")).strip().lower()
        if not payload.strip():
            return VisualStimulus(StimulusType.NONE, "")
        if t == "svg":
            return VisualStimulus(StimulusType.SVG, payload)
        if t == "table":
            return VisualStimulus(StimulusType.TABLE, payload)
        if t in ("source_text", "source", "extract", "prose", "text", "passage", "quote"):
            return VisualStimulus(StimulusType.PROSE, payload)
        raw = payload  # unknown/absent declared type → let the string heuristics decide
    s = (raw if isinstance(raw, str) else "").strip()
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


_SOURCE_NOTE_OPENERS = ("—", "–", "-", "adapted from", "based on", "source:", "from ")


def _is_source_note(row: List[str]) -> bool:
    """A trailing one-cell line that attributes the table rather than carrying data."""
    if len(row) != 1 or not row[0]:
        return False
    t = row[0].strip().lower()
    return any(t.startswith(p) for p in _SOURCE_NOTE_OPENERS)


def parse_table(raw: str) -> dict:
    """Split pipe-delimited table text into
    {'header': [...], 'rows': [[...]], 'caption': str, 'source_note': str}.

    THE single place a pipe-table string is split into cells — every renderer (HTML/PDF
    export, DOCX, the React on-screen view, the assessment 3b view) consumes this structure
    and NEVER re-splits the raw string itself (the recurring drift-bug class). Row 0 is the
    header; remaining lines are body rows. Empty/blank lines are dropped.

    RAGGED PAYLOADS (2026-08-04, founder-reported on SS·VIII ch 3's Maratha-navy MCQ).
    The generator routinely puts NON-DATA lines inside the pipe payload, and every renderer
    took line 0 as the header and each line's own cell count as its width — so a table whose
    title row held 2 cells above 3-column data rendered a 2-column head over 3-column body,
    online AND in PDF/Word. Two shapes, both now handled HERE so one fix reaches all four
    renderers:
      * a LEADING TITLE row — strictly narrower than the body's modal width — becomes
        `caption` (its cells joined with ' · ', so a spanning two-level head keeps every
        word) and the NEXT row becomes the header;
      * a TRAILING ATTRIBUTION row — one cell opening with a dash or 'Adapted from' /
        'Based on' / 'Source:' — becomes `source_note` (SS·IX carries four of these).
    Whatever survives is then PADDED to a single width so no renderer can emit a broken
    grid. Padding never truncates: a row wider than the header widens the whole table
    instead, because dropping a cell would delete content a teacher is meant to read.

    `caption` and `source_note` are '' when absent, so existing consumers that read only
    'header'/'rows' keep working unchanged."""
    lines = [ln for ln in (raw or "").splitlines() if ln.strip()]
    cells = [[c.strip() for c in ln.split("|")] for ln in lines]
    if not cells:
        return {"header": [], "rows": [], "caption": "", "source_note": ""}

    source_note = ""
    if len(cells) > 1 and _is_source_note(cells[-1]):
        source_note = cells[-1][0].strip()
        cells = cells[:-1]

    caption = ""
    if len(cells) >= 3:
        body_widths = [len(r) for r in cells[1:]]
        modal = max(set(body_widths), key=body_widths.count)
        # Strictly narrower than the body it sits above → a title, not a header row.
        if len(cells[0]) < modal:
            caption = " · ".join(c for c in cells[0] if c)
            cells = cells[1:]

    # WORD BANK (no header): a grid where every cell is a single word — a box of words for a
    # cloze / matching / word-choice task. These have no column semantics, so the first row is
    # NOT a header and must not render bold/filled (every word is the same hierarchy). Data
    # tables always carry at least one multi-word cell (their column labels), so they keep the
    # header. Gated to 3+ columns so ordinary two-column tables (Word | Meaning) are untouched.
    flat = [c for row in cells for c in row if c]
    width = max((len(r) for r in cells), default=0)
    if len(cells) >= 2 and width >= 3 and flat and all(" " not in c for c in flat):
        return {"header": [], "rows": [r + [""] * (width - len(r)) for r in cells],
                "caption": caption, "source_note": source_note}

    def _pad(r):
        return r + [""] * (width - len(r))

    return {"header": _pad(cells[0]), "rows": [_pad(r) for r in cells[1:]],
            "caption": caption, "source_note": source_note}


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
