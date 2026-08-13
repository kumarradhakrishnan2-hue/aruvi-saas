#!/usr/bin/env python3
"""S9 · english · preparatory — P5.5, the carrier pre-flight, before `_NOT_YET` is opened.

This is the LAST entry in `carriers._NOT_YET`. The note S11 wrote and S10 confirmed says the
code is in place and names THREE things a sibling stage must CONFIRM — not re-derive — before
deleting its line, plus ONE difference specific to this stage:

  1. that the stage's spine SET matches the summary's — and preparatory's is FIVE, not six
     (listening and speaking are merged into `oracy`, and there is no `vocabulary_grammar`;
     the prep-native key is `word_work`). This is the difference the note calls out by name.
  2. that its assessment container is still the spine-grouped list,
  3. that its LP still emits `coverage_handoff` as a spine-keyed DICT
     (what `_ENGLISH_SPINE_CELL` round-trips).

Part 5 of P5.5 (added at S5) asks a fourth question — where does this stage's PERIOD keep its
section anchor, and does `carriers.unit_anchor` find it. S11 answered it for the whole english
family by grep; it is re-asserted here rather than assumed.

Everything is checked against the REAL saved preparatory corpus, never a fixture invented for
the purpose. Run before the deletion, and again after.
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

# FIVE, not six — the one difference `_NOT_YET` told this stage to check.
SPINES = ["reading", "oracy", "writing", "word_work", "beyond_text"]
MIDDLE_SPINES = ["reading_for_comprehension", "listening", "speaking",
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
print("\n1 · THE SPINE SET — preparatory carries FIVE keys, and they are its own")
lp_const = (ROOT / "data/content/constitutions/lesson_plan/english/preparatory/"
            "lesson_plan_constitution.txt").read_text(encoding="utf-8")
missing = [s for s in SPINES if s not in lp_const]
check(not missing, "all five prep spine keys named in the LP constitution", f"missing {missing}")
# A middle spine key would leak as a KEY, not as prose: preparatory legitimately says
# "oracy (merged listening+speaking)" and "no separate listening spine at prep". So look
# for the backticked/quoted key forms the schema and handoff would use.
borrowed = [s for s in MIDDLE_SPINES if s not in SPINES
            and (f"`{s}`" in lp_const or f'"{s}"' in lp_const)]
check(not borrowed, "no MIDDLE spine key leaks into the preparatory constitution as a KEY",
      f"found {borrowed}")

seen: set[str] = set()
n_cells = n_ch = n_bad = 0
unreadable: list[str] = []
for g in ("iii", "iv", "v"):
    for f in sorted(glob.glob(str(ROOT / f"data/content/chapters/english/{g}/summaries/ch_*.json"))):
        try:
            d = json.load(open(f))
        except Exception:                                   # noqa: BLE001
            unreadable.append(f"{g}/{os.path.basename(f)}")
            n_bad += 1
            continue
        n_ch += 1
        for s in d.get("main_sections") or []:
            for k, v in (s.get("spines") or {}).items():
                seen.add(k)
                if (v or {}).get("tasks_verbatim"):
                    n_cells += 1
check(seen <= set(SPINES), "no summary uses a spine key outside the five",
      f"{n_ch} chapters, {n_cells} taught cells, keys={sorted(seen)}")
check(seen == set(SPINES), "the preparatory corpus exercises all five",
      f"unused: {sorted(set(SPINES) - seen) or 'none'}")
if unreadable:
    # NOT a carrier failure — recorded so the sign-off can raise it as a corpus defect.
    print(f"  NOTE  {n_bad} summary file(s) are not parseable JSON and were skipped: "
          f"{unreadable}")
    notes.append(f"unreadable summaries: {unreadable}")

# ─────────────────────────────────────────── 2 · the assessment container
print("\n2 · THE ASSESSMENT CONTAINER — still the spine-grouped list")
plans = sorted(glob.glob(str(ROOT / "backup/saved_plans/english/iii/*.json"))) \
    + sorted(glob.glob(str(ROOT / "backup/saved_plans/english/iv/*.json"))) \
    + sorted(glob.glob(str(ROOT / "backup/saved_plans/english/v/*.json")))
check(bool(plans), "saved preparatory plans on disk", f"{len(plans)} files")
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
check(getattr(carriers, "_ENGLISH_SPINE_CELL", None) is not None,
      "`_ENGLISH_SPINE_CELL` present in carriers (the third handoff shape)")

# ───────────────────────────── part 5 · where the PERIOD keeps its anchor
print("\n5 · THE UNIT ANCHOR — mediated, because `section_anchor` is nowhere in the LP")
check(lp_const.count("section_anchor") == 0,
      "`section_anchor` absent from the english·preparatory LP constitution",
      f"count={lp_const.count('section_anchor')}")
subj = carriers._plugin_for("english")
check(hasattr(subj, "genon_unit_anchor"), "plugin exposes `genon_unit_anchor`")
check(carriers.anchor_field_present("english", "iii") is False,
      "`genon_anchor_field_present` is False for preparatory "
      "(without it top_brief_for demands a field the constitution never defines, "
      "at metered STEP 1)")
# the composite token is built, and it is the CELL — prove it on a real period
_per = (load(plans[0]).get("lesson_plan") or {}).get("periods") or []
if _per:
    tok = subj.genon_unit_anchor(_per[0], "iii")
    check(isinstance(tok, str) and "|" in tok,
          "`genon_unit_anchor` returns the composite cell token", f"{tok!r}")

# ───────────────────────────── end-to-end on the real saved preparatory shape
print("\nEND TO END — the anchoring rule on the real saved preparatory corpus")
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

check(total_orphans == 0, "zero orphaned items across the preparatory corpus",
      f"{total_items} items resolved")

# ───────────────────────────────────────────────────── the gate itself
print("\nTHE GATE")
for g in ("iii", "iv", "v"):
    print(f"  carrier_gap('english',{g!r}) -> {carriers.carrier_gap('english', g)!r}")
gap = carriers.carrier_gap("english", "iii")
notes.append("OPEN" if gap is None else "STILL GATED")
if gap is None:
    # the gate is open — prove the PUBLIC door works, not only the plugin's
    p = plans[-1]
    r = load(p)
    pub = carriers.assessment_items({"subject": "english", "grade": "v"}, r)
    check(len(pub) == len(subj.genon_assessment(r)) and all(i.get("unit_ref") for i in pub),
          "carriers.assessment_items() resolves through the public door",
          f"{os.path.basename(p)}: {len(pub)} items, all anchored")
    check(carriers.carrier_gap("english", "vi") is None
          and carriers.carrier_gap("english", "ix") is None,
          "the whole english family is now carried — `_NOT_YET` holds no english entry")
    check(not carriers._NOT_YET,
          "`_NOT_YET` is EMPTY — every subject·stage in the campaign is carried",
          f"remaining: {sorted(carriers._NOT_YET)}")

print("\n" + ("ALL CHECKS PASS — " + notes[-1] if not fails
              else f"{len(fails)} FAILURE(S): {fails}"))
sys.exit(1 if fails else 0)
