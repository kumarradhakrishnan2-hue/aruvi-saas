"""anchor_resolver — where a maths middle/preparatory assessment item belongs.

ONE RESOLVER, BOTH PATHS (2026-08-19, S7 · ARV-D-181). The display side
(`subject.py::_middle_assess`) and the serve side (`subject.py::genon_assessment` via
`genon.carriers`) each used to run their own join. English learned at S11 that two joins
are one drift away from disagreeing about which sitting a question belongs to, and lifted
its resolution into a single `cell_resolver` both paths call. This is that, for maths.

WHY THE SECTION JOIN WAS WRONG HERE, in one paragraph. The old rule held an item until its
SECTION closed — right where a section is a topic (social sciences, TWAU: a sitting or two),
wrong here. Maths middle sections are BANNERS: median 6 per chapter against secondary's 10,
and 2.4 sittings each. Measured over the 39 standard canonicals, 553 items: only 199 of 540
sittings carried a question (37%) at 2.8 items apiece, against 76% for maths SECONDARY and
100% for TWAU. vii ch 14 put 15 items on U11 and 7 on U16 and nothing across the other 15
sittings. The cost is not tidiness: a plan served at three-quarter length kept 57% of its
items and at half length 35% — a teacher lost questions FASTER than she lost teaching — and
three chapters handed a half-length class no questions at all.

WHAT THE STAGE ACTUALLY INDEXES ON (founder, 2026-08-19). Not sections — COMPLEXITY, and the
marker of complexity is the textbook exercise. LP Rule 3 assigns each period one anchor from
that period's own `textbook_items_in_class[]`; the assessment constitution then writes one
item per goal in `coverage_handoff` and seeds each item's `exercise` companion FROM that
anchor. So the item already names a period — through the anchor — and we were reading a
different field. On 541 of 553 items the item's `exercise.book_ref` IS a handoff
`anchor_book_ref`, exactly.

THE RULE: an item anchors at the sitting where its handoff anchor is FIRST worked.

First-working is unique by construction, so there is nothing to disambiguate. (An earlier
draft of this reconstructed Rule 3's claim-walk to decide between an anchor's several
appearances; that machinery was unnecessary and is not here.) 98% of first appearances are
in-class work, so the first working is the teaching moment; the lone homework-first case
(viii ch 11 E-1) is benign.

TWO CLASSES FALL BACK TO THE SECTION RULE, both settled by founder ruling and neither a
compromise:

  * THE CAPSTONES (25 items). Their anchor is worked ONLY in the synthesis unit. 23 of 25
    are C-band `apply` on the chapter's LAST section — they are the second, deeper item the
    handoff carries for that section, and its anchor is the culminating exercise, which the
    closer is the only sitting to work. The section rule already places 20 of them one
    sitting before the closer, so the two rules differ by a single sitting. Letting them sit
    ON the synthesis would make this the first stage in the campaign whose closer holds
    assessment — a borrow path never once exercised (ZERO items anchor to a synthesis
    anywhere in the corpus: 3,115 items, 225 chapters) — for no teaching gain.
  * THE COMPANIONLESS (12 items). Eleven carry `{"book_ref": "", "description": ""}` and one
    names an exercise that is not a handoff anchor. Nothing to join on. Generation quality,
    recorded as ARV-D-184, not repaired.

MEASURED EFFECT, standard canonicals: sittings carrying a question 37% -> 82%; items per
such sitting 2.8 -> 1.2; retention at three-quarter length 57% -> 77%. vi ch 5 goes from 4
sittings to 23 of 25.

NOTHING NEW IS ASKED OF THE MODEL and no constitution changes: every field read here is
already authored and already certified. Preparatory is the same shape under other names —
handoff `tasks[].task_id` against period `tasks_in_class[].id` — and is carried by the same
code, keyed off `anchor_fields`.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional, Tuple

# MIDDLE and PREPARATORY name the same three facts differently. Nothing else varies, so the
# stage is a table row rather than a branch (CLAUDE.md §3).
#   handoff cluster key   → the list inside each cluster
#   anchor id / book ref  → the fields on a handoff entry
#   period item lists     → where a period records the textbook items it works
_FIELDS = {
    "middle": {
        "entries": "goals",
        "anchor_id": "anchor_id",
        "book_ref": "anchor_book_ref",
        "period_lists": ("textbook_items_in_class", "homework"),
        "item_id": "id",
    },
    "preparatory": {
        "entries": "tasks",
        "anchor_id": "task_id",
        "book_ref": "book_ref",
        "period_lists": ("tasks_in_class", "homework"),
        "item_id": "id",
    },
}


def _norm(s: Any) -> str:
    return " ".join(str(s or "").split()).lower()


def _handoff_entries(handoff: Any, stage: str) -> List[Dict[str, Any]]:
    """Flatten the goal/intent clusters to a list of entries. Shape-tolerant by design:
    a stage that arrives with a plain list of entries is read as-is rather than refused,
    because the cluster wrapper is a container detail, not part of the join."""
    key = _FIELDS[stage]["entries"]
    out: List[Dict[str, Any]] = []
    if isinstance(handoff, dict):
        for block in handoff.values():
            if isinstance(block, dict):
                out.extend(e for e in (block.get(key) or []) if isinstance(e, dict))
    elif isinstance(handoff, list):
        out.extend(e for e in handoff if isinstance(e, dict))
    return out


def first_working(periods: List[Dict[str, Any]], stage: str,
                  is_synthesis) -> Dict[str, int]:
    """{anchor_id: the number of the FIRST NON-SYNTHESIS sitting that works it}.

    The synthesis unit is skipped here rather than filtered by the caller, and that is the
    whole of the capstone fallback: an anchor worked only in the closer simply never enters
    this map, so `resolve` returns None for it and the caller falls back to the section
    rule. No special case, no list of exceptions.
    """
    f = _FIELDS[stage]
    out: Dict[str, int] = {}
    for p in periods or []:
        if is_synthesis(p):
            continue
        n = p.get("period_number")
        if n is None:
            continue
        for key in f["period_lists"]:
            for t in (p.get(key) or []):
                if not isinstance(t, dict):
                    continue
                tid = t.get(f["item_id"])
                if tid and tid not in out:          # FIRST working wins; later repeats do not
                    out[tid] = int(n)
    return out


def build(*, periods, handoff, stage: str, is_synthesis) -> "Resolver":
    """The two callers reach the same two facts by different routes — the display side has
    them unpacked in `link_context`, the serve side has the whole `result` — so this takes
    the FACTS, not a container. `from_result` is the serve-side convenience."""
    return Resolver(_handoff_entries(handoff, stage),
                    first_working(periods, stage, is_synthesis), stage)


def from_result(result: Dict[str, Any], *, stage: str, is_synthesis) -> "Resolver":
    lp = (result or {}).get("lesson_plan") or {}
    return build(periods=lp.get("periods") or [],
                 handoff=(result or {}).get("coverage_handoff"),
                 stage=stage, is_synthesis=is_synthesis)


class Resolver:
    """Item -> sitting, or None when the caller must fall back to the section rule."""

    def __init__(self, entries: List[Dict[str, Any]], firsts: Dict[str, int], stage: str):
        f = _FIELDS[stage]
        self._by_ref: Dict[str, str] = {}
        for e in entries:
            ref, aid = _norm(e.get(f["book_ref"])), e.get(f["anchor_id"])
            # A blank book_ref is not a key. Eleven items carry one (ARV-D-184) and mapping
            # them together would anchor every one of them at whichever entry landed last.
            if ref and aid:
                self._by_ref.setdefault(ref, aid)
        self._firsts = firsts

    def resolve(self, item: Dict[str, Any]) -> Optional[int]:
        ex = item.get("exercise")
        ref = _norm(ex.get("book_ref")) if isinstance(ex, dict) else ""
        if not ref:
            return None                       # companionless — section rule
        aid = self._by_ref.get(ref)
        if not aid:
            return None                       # names no handoff anchor — section rule
        return self._firsts.get(aid)          # None when worked only in the synthesis

    def stats(self) -> Tuple[int, int]:
        return len(self._by_ref), len(self._firsts)
