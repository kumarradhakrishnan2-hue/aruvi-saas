#!/usr/bin/env python3
"""S10 · english · middle — P5.5, the carrier pre-flight, verified before `_NOT_YET` is opened.

`carriers._NOT_YET`'s english entries say the code is in place and name THREE things a
sibling stage must CONFIRM — not re-derive — before deleting its line:

  1. that the stage's spine SET matches the summary's,
  2. that its assessment container is still the spine-grouped list,
  3. that its LP still emits `coverage_handoff` as a spine-keyed DICT
     (what `_ENGLISH_SPINE_CELL` round-trips).

Part 5 of P5.5 (added at S5) asks a fourth question — where does this stage's PERIOD keep its
section anchor, and does `carriers.unit_anchor` find it. S11 answered it for the whole english
family by grep; it is re-asserted here rather than assumed.

Everything is checked against the REAL saved middle corpus, never a fixture invented for the
purpose. Run before the deletion, and again after.
"""
from __future__ import annotations

import glob
import json
import os
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("ARUVI_DATA_DIR", str(ROOT / "data/content"))

from aruvi_core.genon import carriers                      # noqa: E402
from aruvi_core.subjects import english as _en             # noqa: E402  (registers the plugin)

SPINES = ["reading_for_comprehension", "listening", "speaking",
          "writing", "vocabulary_grammar", "beyond_text"]

fails: list[str] = []
notes: list[str] = []


def check(ok: bool, label: str, detail: str = "") -> None:
    print(("  PASS  " if ok else "  FAIL  ") + label + (f"  — {detail}" if detail else ""))
    if not ok:
        fails.append(label)


def load(path: str) -> dict:
    d = json.load(open(path))
    return d.get("result") or d


# ────────────────────────────────────────────────────── 1 · the spine SET
print("\n1 · THE SPINE SET — the constitution's six keys against the summaries' own")
lp_const = (ROOT / "data/content/constitutions/lesson_plan/english/middle/"
            "lesson_plan_constitution.txt").read_text(encoding="utf-8")
missing = [s for s in SPINES if s not in lp_const]
check(not missing, "all six spine keys named in the LP constitution", f"missing {missing}")

seen: set[str] = set()
n_cells = n_ch = 0
for g in ("vi", "vii", "viii"):
    for f in sorted(glob.glob(str(ROOT / f"data/content/chapters/english/{g}/summaries/ch_*.json"))):
        d = json.load(open(f))
        n_ch += 1
        for s in d.get("main_sections") or []:
            for k, v in (s.get("spines") or {}).items():
                seen.add(k)
                if (v or {}).get("tasks_verbatim"):
                    n_cells += 1
check(seen <= set(SPINES), "no summary uses a spine key outside the six",
      f"{n_ch} chapters, {n_cells} taught cells, keys={sorted(seen)}")
check(seen == set(SPINES), "the middle corpus exercises all six",
      f"unused: {sorted(set(SPINES) - seen) or 'none'}")

# ─────────────────────────────────────────── 2 · the assessment container
print("\n2 · THE ASSESSMENT CONTAINER — still the spine-grouped list")
plans = sorted(glob.glob(str(ROOT / "backup/saved_plans/english/vi/*.json"))) \
    + sorted(glob.glob(str(ROOT / "backup/saved_plans/english/vii/*.json"))) \
    + sorted(glob.glob(str(ROOT / "backup/saved_plans/english/viii/*.json")))
check(bool(plans), "saved middle plans on disk", f"{len(plans)} files")
shapes: set[str] = set()
for p in plans:
    raw = load(p).get("assessment_items")
    groups = raw.get("assessment_items", raw) if isinstance(raw, dict) else raw
    if not isinstance(groups, list) or not groups:
        shapes.add("EMPTY/NON-LIST")
        continue
    g0 = groups[0]
    shapes.add("spine_group" if isinstance(g0, dict) and "spine_code" in g0 and "items" in g0
               else f"OTHER:{sorted(g0)[:4] if isinstance(g0, dict) else type(g0).__name__}")
check(shapes == {"spine_group"}, "every saved plan groups items by spine_code", f"shapes={shapes}")

# ────────────────────────────────────────── 3 · the coverage_handoff shape
print("\n3 · THE COVERAGE HANDOFF — still a spine-keyed dict of section_contributions[]")
bad = []
for p in plans:
    h = load(p).get("coverage_handoff")
    if not isinstance(h, dict):
        bad.append((os.path.basename(p), type(h).__name__))
        continue
    if not set(h) <= set(SPINES):
        bad.append((os.path.basename(p), f"extra keys {sorted(set(h) - set(SPINES))}"))
        continue
    for k, blk in h.items():
        if not isinstance(blk, dict) or "section_contributions" not in blk:
            bad.append((os.path.basename(p), f"{k} is not a contributions block"))
check(not bad, "spine-keyed dict, contributions block per spine", str(bad[:3]))
check(carriers._ENGLISH_SPINE_CELL is not None
      if hasattr(carriers, "_ENGLISH_SPINE_CELL") else False,
      "`_ENGLISH_SPINE_CELL` present in carriers (the third handoff shape)")

# ───────────────────────────── part 5 · where the PERIOD keeps its anchor
print("\n5 · THE UNIT ANCHOR — mediated, because `section_anchor` is nowhere in the LP")
check(lp_const.count("section_anchor") == 0,
      "`section_anchor` absent from the english·middle LP constitution",
      f"count={lp_const.count('section_anchor')}")
subj = carriers._plugin_for("english")
check(hasattr(subj, "genon_unit_anchor"), "plugin exposes `genon_unit_anchor`")
check(carriers.anchor_field_present("english", "vi") is False,
      "`genon_anchor_field_present` is False for middle "
      "(without it top_brief_for demands a field the constitution never defines, at metered STEP 1)")

# ───────────────────────────────── end-to-end on the real saved middle shape
print("\nEND TO END — the anchoring rule on the real saved middle corpus")
print("  (via the plugin's own `genon_assessment` while the gate is still shut; the public")
print("   `carriers.assessment_items` is exercised by the gate check at the end)")
total_items = total_orphans = 0
for p in plans:
    r = load(p)
    periods = (r.get("lesson_plan") or {}).get("periods") or []
    if not periods:
        continue
    items = subj.genon_assessment(r)
    total_items += len(items)

    # independently computed truth: the LAST unit whose (section_id, spine) equals the cell
    by_cell: dict[tuple[str, str], list[int]] = {}
    for i, per in enumerate(periods, start=1):
        sid = str(per.get("section_id") or "").strip()
        for sp in per.get("spines_taught") or []:
            by_cell.setdefault((sid, str(sp).strip()), []).append(i)

    orphans, wrong = [], []
    per_cell: dict[tuple[str, str], list] = {}
    for it in items:
        cell = (str(it.get("source_section_id") or "").strip(),
                str(it.get("source_spine") or "").strip())
        refs = it.get("unit_ref") or []
        if not refs:
            orphans.append(it.get("id"))
            continue
        per_cell.setdefault(cell, []).append((it.get("id"), refs))
    for cell, got in per_cell.items():
        units = by_cell.get(cell) or []
        if not units:
            continue
        if len(got) == 1:
            if got[0][1] != [units[-1]]:
                wrong.append((cell, got[0], f"expected last unit {units[-1]}"))
        elif len(got) == len(units):        # the N-to-N pairing, one item per unit
            for (iid, refs), u in zip(got, units):
                if refs != [u]:
                    wrong.append((cell, (iid, refs), f"N-to-N expected {u}"))
    total_orphans += len(orphans)
    flag = "ok" if not orphans and not wrong else f"ORPHANS {orphans} WRONG {wrong}"
    print(f"    {os.path.basename(p)[:24]:<24} units={len(periods):>2} items={len(items):>2}  {flag}")
    if orphans or wrong:
        fails.append(os.path.basename(p))

check(total_orphans == 0, "zero orphaned items across the middle corpus",
      f"{total_items} items resolved")

# ───────────────────────────────────────────────────── the gate itself
print("\nTHE GATE")
for g in ("vi", "vii", "viii"):
    print(f"  carrier_gap('english',{g!r}) -> {carriers.carrier_gap('english', g)!r}")
gap = carriers.carrier_gap("english", "vi")
notes.append("OPEN" if gap is None else "STILL GATED")
if gap is None:
    # the gate is open — prove the PUBLIC door works, not only the plugin's
    p = plans[-1]
    r = load(p)
    pub = carriers.assessment_items({"subject": "english", "grade": "viii"}, r)
    check(len(pub) == len(subj.genon_assessment(r)) and all(i.get("unit_ref") for i in pub),
          "carriers.assessment_items() resolves through the public door",
          f"{os.path.basename(p)}: {len(pub)} items, all anchored")
    check(carriers.carrier_gap("english", "preparatory") is not None
          and carriers.carrier_gap("english", "iii") is not None,
          "preparatory is STILL gated — the table is stage-granular, not per-subject")

print("\n" + ("ALL CHECKS PASS — " + notes[-1] if not fails
              else f"{len(fails)} FAILURE(S): {fails}"))
sys.exit(1 if fails else 0)
