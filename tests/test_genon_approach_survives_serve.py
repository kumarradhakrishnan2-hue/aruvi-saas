#!/usr/bin/env python3
"""ARV-D-086 regression — the pedagogical approach line must survive a SERVE.

Found at S4's C6 (2026-08-09). Every canonical on disk carried its approach correctly and
every C-step up to C5 passed, because none of them reads a SERVED plan. Eight of eleven
stages were serving lesson plans with an empty "how do I run this?" line — the one canonical
line CLAUDE.md §3(b) defines — because `compile._MODELLED` swallowed the five subject key
names before `serve._period_from_unit` could splice them back.

Two properties are locked here, and they are different:

  1. `carriers.unit_approaches` reads ALL FIVE authored key names. (Unit-level.)
  2. A plan that goes through compile → serve → the subject's own port comes out with a
     NON-EMPTY approach on every unit. (End-to-end — this is the one that would have
     caught the defect; property 1 alone would not have, because the ports read the
     authored key, not the normalized one.)

Stdlib only. Needs ARUVI_DATA_DIR=$PWD/data/cloud/content for the end-to-end half; that half
skips itself, loudly, when no library is on disk.

    ARUVI_DATA_DIR=$PWD/data/cloud/content python3 tests/test_genon_approach_survives_serve.py
"""
import os
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1]))

from aruvi_core.genon import carriers, compile as gcompile, serve  # noqa: E402

FAILURES = []


def check(label, cond, detail=""):
    if cond:
        print(f"  ok    {label}")
    else:
        FAILURES.append(f"{label} — {detail}")
        print(f"  FAIL  {label} — {detail}")


# ── 1 · every authored key name is read ────────────────────────────────────────────
print("unit_approaches reads all five authored key names")
CASES = [
    ("social_sciences", {"pedagogical_approaches": ["Inquiry", "Project work"]},
     ["Inquiry", "Project work"]),
    ("english (dict, unique first-seen)",
     {"pedagogical_methods": {"Reading": "Guided reading", "Writing": "Process writing",
                              "Speaking": "Guided reading"}},
     ["Guided reading", "Process writing"]),
    ("science", {"pedagogical_approach": "Inquiry approach"}, ["Inquiry approach"]),
    ("mathematics", {"pedagogical_method": "Deductive"}, ["Deductive"]),
    ("the_world_around_us", {"dominant_mode": "Hands-on Investigation"},
     ["Hands-on Investigation"]),
]
for label, period, want in CASES:
    got = carriers.unit_approaches(period)
    check(label, got == want, f"got {got!r}, want {want!r}")

check("a period with no approach key yields []", carriers.unit_approaches({"x": 1}) == [])
check("blank values are not emitted as approaches",
      carriers.unit_approaches({"pedagogical_method": "   "}) == [])

# ── 2 · the authored key is NOT swallowed by compile ───────────────────────────────
print("\nthe authored key rides in extra rather than being modelled away")
for key in ("pedagogical_method", "pedagogical_methods", "pedagogical_approach",
            "pedagogical_approaches", "dominant_mode"):
    check(f"{key} is not in compile._MODELLED", key not in gcompile._MODELLED,
          "modelled keys are stripped from extra and never spliced back")

# ── 3 · END TO END: compile -> serve -> port, approach non-empty on every unit ──────
print("\nend-to-end: a served plan renders an approach on every unit")
import json  # noqa: E402

ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANS = pathlib.Path(os.environ.get("ARUVI_DATA_DIR", ROOT / "data/cloud/content")) / "saved_plans"

LIBRARIES = [
    ("mathematics", "ix", 4, 13),
    ("science", "ix", 8, 13),
    ("science", "viii", 6, 11),
    ("social_sciences", "ix", 3, 11),
]


def approaches_of(view):
    out = []

    def walk(group):
        for period in getattr(group, "periods", []) or []:
            out.append((getattr(period, "approach", "") or "").strip())
        for child in getattr(group, "groups", []) or []:
            walk(child)

    for group in view.groups:
        walk(group)
    return out


ran = 0
for subject, grade, chapter, periods in LIBRARIES:
    folder = PLANS / subject / grade
    files = sorted(folder.glob(f"ch_{chapter:02d}_canonical*.json"))
    if not files:
        print(f"  skip  {subject}/{grade} ch{chapter} — no library on disk")
        continue
    ran += 1
    __import__(f"aruvi_core.subjects.{subject}")
    from aruvi_core.subjects import get as get_subject

    streams = [gcompile.compile_stream(json.loads(f.read_text(encoding="utf-8")))
               for f in files]
    served = serve.serve_plan(streams, serve.parse_matrix(f"{periods}x50"))
    view = get_subject(subject).lesson_plan_to_view(
        served["result"], grade=grade,
        chapter={"chapter_number": chapter, "chapter_title": ""})
    found = approaches_of(view)
    empty = [i + 1 for i, a in enumerate(found) if not a]
    check(f"{subject}/{grade} ch{chapter} served at {periods} periods",
          found and not empty,
          f"{len(empty)} of {len(found)} units have an EMPTY approach (units {empty[:6]})")

if not ran:
    print("  NOTE: no libraries found — the end-to-end half did not run. Set "
          "ARUVI_DATA_DIR=$PWD/data/cloud/content")

print()
if FAILURES:
    print(f"{len(FAILURES)} FAILURE(S):")
    for f in FAILURES:
        print(f"  - {f}")
    sys.exit(1)
print("all approach-survives-serve checks passed")
