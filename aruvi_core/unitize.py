"""Display-time 'period' -> 'unit' cleaner (Lever B, 2026-07-13).

The product renamed the atomic teaching chunk from "period" to "unit". Lever A fixed the
generation source so NEW plans are born saying "unit". Lever B (this module) rescues the
large HISTORIC universe of saved plans WITHOUT backfilling storage: it rewrites the
chunk-referential sense of "period" at the DISPLAY boundary only (ViewModel.to_dict for the
screen, render/html.py for PDF). The saved plans on disk and the engine's normalized view
model stay literally "period"; only what reaches the teacher's eyes says "unit".

WHY THIS IS PATTERN-SCOPED, NOT A FIND-REPLACE
"period" has senses that MUST survive:
  - domain science: "periodic table", "the period of a pendulum", "time period of a wave"
  - punctuation (English grammar): "end the sentence with a period"
  - scheduling: "period budget/schedule/count" (these never appear in the narrative fields
    we clean, but the guards make the function safe to apply to any prose)
So we convert ONLY the teaching-chunk sense, recognised by context:
  - a chunk determiner immediately before: this/that/the/each/every/next/previous/prior/
    following/subsequent/last/first/second/.../final/closing/opening/current/same/other/
    another/multiple/several/consecutive/adjacent/remaining/preceding/succeeding/upcoming/coming
  - OR a number immediately after: "Period 1", "Periods 1 and 2", "from Period 3"
  - OR a duration immediately before: "40-minute period", "the 30-minute period"
and NEVER when:
  - the word is "periodic"/"periodically" (word boundary already excludes these)
  - "period" is followed by " of " (time sense: "period of revolution")
  - "period" is preceded by "time" ("time period")
  - "period" is preceded by a bare "a"/"an" and no number follows (ambiguous: "a period of
    time"; punctuation "a period") -> left untouched
Capitalisation and plural ("Period"->"Unit", "periods"->"units") are preserved.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List

__all__ = ["unitize", "unitize_lesson_plan_dict"]

# Determiners / ref-adjectives that mark the following "period" as a teaching chunk.
_CHUNK_DETERMINERS = {
    "this", "that", "the", "each", "every", "next", "previous", "prior", "following",
    "subsequent", "last", "first", "second", "third", "fourth", "fifth", "sixth",
    "seventh", "eighth", "ninth", "tenth", "final", "closing", "opening", "current",
    "same", "other", "another", "multiple", "several", "consecutive", "adjacent",
    "remaining", "preceding", "succeeding", "upcoming", "coming", "earlier", "later",
    "both", "neighbouring", "neighboring",
}
# Duration words that mark "<n>-minute period" / "<n> minute period".
_DURATION_WORDS = {"minute", "minutes", "min", "mins", "hour", "hours"}

# The word itself, with boundaries. Group 1 = 'period' (any case), group 2 = optional 's'.
# \b after the optional s means "periodic" never matches (next char is a letter).
_PERIOD_RE = re.compile(r"\b(period)(s)?\b", re.IGNORECASE)
# Trailing " of ..." (time sense) — checked on the text AFTER the match.
_OF_AFTER = re.compile(r"^\s+of\b", re.IGNORECASE)
# A number right after the match ("Period 1", "Periods 1-3").
_NUM_AFTER = re.compile(r"^[\s.:]*\d", re.IGNORECASE)
# The IMMEDIATELY preceding word — trailing letters separated from "period" only by spaces
# or hyphens (so "40-minute period" sees "minute", but "35 minutes x 3 periods" does NOT reach
# back over the "x 3" to grab "minutes": the adjacent token there is the number "3").
_PREV_WORD = re.compile(r"([A-Za-z]+)[\s\-]*$")


def _preserve_case(matched_word: str, plural: str) -> str:
    base = "Unit" if matched_word[:1].isupper() else "unit"
    return base + (plural or "")


def unitize(text: str) -> str:
    """Rewrite the teaching-chunk sense of 'period' to 'unit' in a prose string.

    Idempotent and safe on any prose: strings with no chunk-referential 'period' are
    returned unchanged (including 'periodic table', 'time period', 'a period.')."""
    if not text or "period" not in text.lower():
        return text

    def repl(m: "re.Match[str]") -> str:
        word, plural = m.group(1), m.group(2)
        before = text[: m.start()]
        after = text[m.end():]

        # --- exclusions win first ---
        if _OF_AFTER.match(after):                 # "period of revolution" (time sense)
            return m.group(0)
        pm = _PREV_WORD.search(before)
        prev = pm.group(1).lower() if pm else ""
        if prev == "time":                         # "time period"
            return m.group(0)

        num_after = bool(_NUM_AFTER.match(after))   # "Period 1", "periods 1-3"
        # bare a/an with no number → ambiguous ("a period of time", punctuation) → keep
        if prev in ("a", "an") and not num_after:
            return m.group(0)

        # --- conversion triggers ---
        if prev in _CHUNK_DETERMINERS or prev in _DURATION_WORDS or num_after:
            return _preserve_case(word, plural)
        return m.group(0)

    return _PERIOD_RE.sub(repl, text)


def _clean_str(v: Any) -> Any:
    return unitize(v) if isinstance(v, str) else v


def _clean_list(v: Any) -> Any:
    if isinstance(v, list):
        return [unitize(x) if isinstance(x, str) else x for x in v]
    return v


# Narrative fields on a period dict that the teacher reads (never schema/meta/scheduling).
_PERIOD_STR_FIELDS = ("title", "homework")
_PERIOD_LIST_FIELDS = ("activities", "teacher_notes", "materials")


def _clean_period_dict(p: Dict[str, Any]) -> None:
    for f in _PERIOD_STR_FIELDS:
        if f in p:
            p[f] = _clean_str(p[f])
    for f in _PERIOD_LIST_FIELDS:
        if f in p:
            p[f] = _clean_list(p[f])
    # phases: list of {text, ...} — clean the narrative 'text' only
    for ph in p.get("phases") or []:
        if isinstance(ph, dict) and isinstance(ph.get("text"), str):
            ph["text"] = unitize(ph["text"])


def _clean_group_dict(g: Dict[str, Any]) -> None:
    for p in g.get("periods") or []:
        if isinstance(p, dict):
            _clean_period_dict(p)
    for child in g.get("children") or []:
        if isinstance(child, dict):
            _clean_group_dict(child)


def unitize_lesson_plan_dict(lp: Dict[str, Any]) -> Dict[str, Any]:
    """In-place clean of a serialized lesson_plan view (the dict from asdict()).

    Walks groups -> periods (+ nested children) and unitizes only the teacher-facing
    narrative fields. Returns the same dict for convenience."""
    if not isinstance(lp, dict):
        return lp
    for g in lp.get("groups") or []:
        if isinstance(g, dict):
            _clean_group_dict(g)
    return lp
