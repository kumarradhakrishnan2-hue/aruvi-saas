#!/usr/bin/env python3
"""register_scan.py — the deterministic gate for THE SELF-CONTAINED REGISTER (v1.0, 2026-08-02).

WHY THIS EXISTS. The register is stated in every LP constitution as a prohibition, and the
SS·IX ch 3 pilot proved a prohibition is not enforcement: the top canonical, authored under
v1.10 which bans it in terms, carried NINE forward-reference/completion breaches (docs/testing.md
C3, defects ARV-D-011..013). This is the failure family the MCQ probe already documented
(rollout brief A9): asking the model to MAINTAIN a constraint across 25k tokens is not the same
as asking it to recognise one sentence. So the constraint moves where it can be enforced — into
code that runs at build time, before a plan can certify.

WHAT IT CHECKS — the v1.10 register's three bans, plus internal-ID leakage:
  forward     · points at a unit that follows, or promises what it will do
  completion  · claims the chapter (or all its sections) has been covered
  calendar    · names a SCHEDULE in days/weeks (tomorrow, next class, this week) — Aruvi keeps
                no calendar and sittings do not map to days. NOTE "today"/"yesterday" are
                ADVISORY, not bans: in a weather chapter "Will it rain today?" and "today's
                newspaper" are content, self-consistent whenever the unit is taught. A gate that
                fails on those would be switched off within a week, so a human judges them.
  clock       · states a quantity of minutes; proportional scaling falsifies it silently
  ids         · competency codes (C-4.2) in teacher-facing text (Rule 10 P bans them in notes;
                Rule 13 makes bands the core teacher-facing product, so a leak there is worse)
  positional  · ADVISORY, not a ban: v1.10 legalised backward references. Flagged only because
                Rule 13 P3 keeps unit-to-unit linking in teacher_notes, and "the previous unit"
                is positional where content-naming was available.

WHAT IT DOES NOT CATCH, stated plainly: paraphrase. "Later in this chapter we shall meet…"
sails through. The scanner carries the floor; a sampled LLM audit at batch level is what finds
new phrasings, and every one it finds should be added to PATTERNS here with a dated note.

Scanned fields are exactly the teacher-facing ones, ACROSS ALL ELEVEN SUBJECT-STAGE SHAPES
(checked 2026-08-02 against every LP constitution): activity_title · teacher_notes, or
`teacher_facilitation_note` where TWAU-preparatory names it that · the band array, which is
`time_bands[]` in the five converted constitutions and still `phases[]` in the six awaiting P3,
with its text under `activity` or `description` · homework[]. section_context and LO rows are
internal and not scanned.

Reading only one shape would be worse than useless — a Group B plan would scan clean because
nothing was read. Every shape is tried, and `scanned_fields()` reports what was actually found.

Vocabulary note: all eleven constitutions name the atomic chunk a "unit" in teacher-facing prose
and reserve "period" for schema/scheduling, so the families below are subject-neutral. Several
give "the previous unit" as a LEGITIMATE cross-reference, which is why backward-positional
phrasing is advisory here rather than a ban.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

# (family, is_ban, compiled pattern). Order is report order.
PATTERNS = [
    ("forward", True, re.compile(r"\bthe (next|following) (unit|lesson|class|session)\b", re.I)),
    ("forward", True, re.compile(r"\bnext unit\b", re.I)),
    ("forward", True, re.compile(r"\blater (unit|units|lessons)\b", re.I)),
    ("forward", True, re.compile(r"\bas we (will|shall) see\b", re.I)),
    ("forward", True, re.compile(r"\bwhat is to come\b", re.I)),
    ("forward", True, re.compile(r"\b(connecting|pointing|looking) (forward|ahead)\b", re.I)),
    ("forward", True, re.compile(r"\bunit (will|would) (show|develop|examine|cover|introduce)\b", re.I)),
    ("forward", True, re.compile(r"\b(develops|develop) (further|mechanistically)\b", re.I)),
    ("forward", True, re.compile(r"\bthread (to pick up|that .{0,40} develops)\b", re.I)),
    ("forward", True, re.compile(r"\bpreviewing\b|\bforeshadow\w*\b", re.I)),
    ("forward", True, re.compile(r"\bfrom the next\b|\bthis unit from the next\b", re.I)),
    ("completion", True, re.compile(r"\bhaving (worked through|covered|completed) (every|all|the whole)\b", re.I)),
    ("completion", True, re.compile(r"\bnow that (we|students|they) have (covered|completed)\b", re.I)),
    ("completion", True, re.compile(r"\bthe chapter is (now )?complete\b", re.I)),
    ("calendar", True, re.compile(r"\btomorrow\b", re.I)),
    ("calendar", True, re.compile(r"\b(this|next|last) (week|month|term)\b", re.I)),
    ("calendar", True, re.compile(r"\b(next|last) class\b", re.I)),
    ("calendar", False, re.compile(r"\b(today|yesterday)\b", re.I)),      # advisory — see header
    ("clock", True, re.compile(r"\bfor (two|three|four|five|six|seven|eight|nine|ten|fifteen|twenty|thirty|\d+) minutes\b", re.I)),
    ("clock", True, re.compile(r"\bthe remaining time\b|\bhalf the (session|period|class)\b", re.I)),
    ("clock", True, re.compile(r"\bin the (first|last) \w+ minutes\b", re.I)),
    ("ids", True, re.compile(r"\(C-\d+\.\d+\)")),
    ("positional", False, re.compile(r"\b(previous|earlier|first|last) unit\b", re.I)),
]


NOTE_KEYS = ("teacher_notes", "teacher_facilitation_note")   # TWAU-prep names it the long way
BAND_KEYS = ("time_bands", "phases")                        # phases[] until P3 converts a stage
BAND_TEXT = ("activity", "description")                     # description[] is the phases-era key


def _fields(unit):
    """The teacher-facing strings of one unit, as (label, text) pairs — shape-agnostic."""
    yield "activity_title", str(unit.get("activity_title") or "")
    for k in NOTE_KEYS:
        if unit.get(k):
            yield k, str(unit[k])
    for bk in BAND_KEYS:
        for i, b in enumerate(unit.get(bk) or []):
            text = next((str(b[t]) for t in BAND_TEXT if b.get(t)), "")
            yield f"{bk}[{i}] {b.get('minutes','?')}", text
    for i, h in enumerate(unit.get("homework") or []):
        yield f"homework[{i}]", h if isinstance(h, str) else json.dumps(h, ensure_ascii=False)


def scanned_fields(plan: dict):
    """Which teacher-facing keys were actually found — so a silent miss is visible.
    A plan reporting 0 bans AND 0 band fields has not been scanned, it has been skipped."""
    periods = ((plan.get("result") or plan).get("lesson_plan") or {}).get("periods") or []
    seen = {}
    for u in periods:
        for label, text in _fields(u):
            key = label.split("[")[0]
            seen[key] = seen.get(key, 0) + (1 if text else 0)
    return seen


_QUOTED = re.compile(r"[\u2018\u2019\u201c\u201d\'\"]([^\u2018\u2019\u201c\u201d\'\"]{0,300}?)[\u2018\u2019\u201c\u201d\'\"]")


def _quoted_spans(text):
    """Character ranges inside quotation marks — specimen sentences, textbook prompts and
    the questions Rule 13 requires bands to state. A calendar word inside one is the
    chapter speaking, not the plan scheduling itself."""
    return [(m.start(1), m.end(1)) for m in _QUOTED.finditer(text)]


def scan_plan(plan: dict):
    """-> list of hits {unit, field, family, ban, match, excerpt}. Empty ban list = clean.

    Two deliberate suppressions, both to keep the gate credible:
      * overlapping matches on one field collapse to the first (several patterns describe the
        same breach; reporting it three times trains people to skim);
      * a CALENDAR hit inside quotation marks drops to advisory (quoted chapter content)."""
    periods = ((plan.get("result") or plan).get("lesson_plan") or {}).get("periods") or []
    hits = []
    for u in periods:
        for field, text in _fields(u):
            quoted = _quoted_spans(text)
            taken = []
            for family, ban, pat in PATTERNS:
                for m in pat.finditer(text):
                    if any(m.start() < e and s_ < m.end() for s_, e in taken):
                        continue                       # already reported as another pattern
                    taken.append((m.start(), m.end()))
                    in_quote = any(s_ <= m.start() and m.end() <= e for s_, e in quoted)
                    a, b = max(0, m.start() - 60), min(len(text), m.end() + 60)
                    hits.append({
                        "unit": u.get("period_number"), "field": field, "family": family,
                        "ban": ban and not (family == "calendar" and in_quote),
                        "quoted": in_quote, "match": m.group(0),
                        "excerpt": ("…" if a else "") + text[a:b].strip() + ("…" if b < len(text) else ""),
                    })
    return hits


def scan_file(path):
    return scan_plan(json.loads(Path(path).read_text(encoding="utf-8")))


def report(hits, name=""):
    """Human-readable block; returns (n_bans, n_advisory)."""
    bans = [h for h in hits if h["ban"]]
    adv = [h for h in hits if not h["ban"]]
    if name:
        print(f"\n--- {name}: {len(bans)} ban hit(s), {len(adv)} advisory")
    for h in bans + adv:
        tag = h["family"].upper() if h["ban"] else h["family"] + " (advisory)"
        print(f"  U{h['unit']:<3} {h['field']:<22} [{tag}] {h['excerpt']}")
    return len(bans), len(adv)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 genon/register_scan.py <plan.json> [more.json ...]")
    total = 0
    for p in sys.argv[1:]:
        n, _ = report(scan_file(p), Path(p).name)
        total += n
    print(f"\nTOTAL ban hits: {total}")
    sys.exit(1 if total else 0)
