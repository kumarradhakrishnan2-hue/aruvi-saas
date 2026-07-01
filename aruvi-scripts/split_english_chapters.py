"""
Split English chapter_summary + mapping files from NCERT "Unit" granularity down to true
instructional chapter granularity, using only data already present in the existing summary/
mapping JSON (no LLM re-run). See CLAUDE.md / conversation 2026-07-01 for the full rationale.

Per the authoring constitution (Project Aruvi/cowork prompts/english/{stage}/
step_1_chapter_summary_and_mapping.md), every English summary already has:
  - main_sections[]  — one entry per REAL chapter, each fully self-contained
                        (own prose_summary/poem_text, own spines{...tasks_verbatim...},
                        own page_range/page_count)
  - competency_reporting.by_spine — spine -> static c_codes (from spine_to_cg.json),
                        keyed by spine name, present only for spines that occur ANYWHERE
                        in the chapter (union across sections)
  - effort_signals    — spine_load/task_density/writing_demand/project_load/effort_index,
                        computed once for the whole chapter (Unit)

This is uniform across preparatory/middle/secondary (verified against all three stage
constitutions). The split below:
  1. Numbers true chapters sequentially in summary-file order, then main_sections order
     within each file (Unit 1's sections first, then Unit 2's, ...).
  2. Titles each true chapter "<section title> (<unit chapter_title>)".
  3. Rebuilds competency_reporting.by_spine per true chapter as the subset of the unit's
     by_spine restricted to spines present in THIS section's own spines{} keys (a subset,
     not invented — by_spine's codes are static per spine name, not section-specific, so
     this is a faithful narrowing, not a guess).
  4. Computes effort_signals FRESH per section (Step 7d of the constitution — chapter-scale
     tiers, NOT the page-count-weighted proration of an earlier draft of this script, which
     was rejected: page count doesn't track actual task/exercise load). See
     `chapter_scale_effort_signals()` below and cowork prompts/english/middle/
     step_1_chapter_summary_and_mapping.md Step 7d for the full rationale.
     *** The four tier functions (tier_spine_load / tier_task_density / tier_writing_demand /
     tier_project_load) below are CALIBRATED ON GRADE VI'S OWN DISTRIBUTION (16 true
     chapters, 2026-07-01) — do NOT reuse blindly for another grade. Recompute the raw
     per-chapter distributions for the new grade first (see the audit workflow in
     MEMORY.md/CLAUDE.md), get sign-off on revised cutoffs, THEN update these functions
     before running the split for that grade. ***
  5. Rebuilds mapping.primary the same way the constitution builds it for a whole chapter —
     walk the canonical spine order, take each present spine's codes, de-dup with
     first-occurrence-wins — just scoped to this section's spines instead of the unit's.

Output goes to a STAGING folder (summaries_split/ mappings_split/) alongside the existing
Unit-level files — nothing existing is overwritten or moved. Review before cutover; only
move summaries_split/mappings_split into the live summaries/mappings folders (deleting the
old Unit-level files first) after explicit approval — that is a separate, deliberate step.
"""
import json
import os
import sys

CANONICAL_SPINE_ORDER = [
    "reading_for_comprehension", "listening", "speaking", "writing",
    "vocabulary_grammar", "beyond_text",
    # preparatory's 5-spine set
    "oracy", "reading", "word_work",
]

ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                     "data", "content", "chapters", "english")


def round_half_up(x):
    import math
    return math.floor(x + 0.5)


def largest_remainder_split(total, shares):
    """Split `total` (int) across `shares` (proportions summing to 1) so parts are ints
    and sum exactly to total."""
    raw = [total * s for s in shares]
    floors = [int(x) for x in raw]
    remainder = total - sum(floors)
    order = sorted(range(len(shares)), key=lambda i: raw[i] - floors[i], reverse=True)
    for i in order[:remainder]:
        floors[i] += 1
    return floors


def build_primary(by_spine, section_spine_keys):
    seen = set()
    out = []
    for spine in CANONICAL_SPINE_ORDER:
        if spine not in section_spine_keys:
            continue
        for code in by_spine.get(spine, []):
            if code not in seen:
                seen.add(code)
                out.append({"c_code": code, "weight": 1})
    return out


# ── Step 7d (Grade VI pilot) — chapter-scale effort signals, computed fresh per section,
# NOT prorated from the Unit total. See Project Aruvi/cowork prompts/english/middle/
# step_1_chapter_summary_and_mapping.md Step 7d for the full rationale + calibration.
def tier_spine_load(cells):
    if cells <= 3: return 1
    if cells <= 5: return 2
    return 3


def tier_task_density(avg):
    if avg <= 2.0: return 1
    if avg <= 2.9: return 2
    return 3


def tier_writing_demand(total):
    if total <= 2: return 0
    if total <= 4: return 1
    return 2


def tier_project_load(items):
    if items <= 1: return 0
    if items == 2: return 1
    if items <= 4: return 2
    return 3


def chapter_scale_effort_signals(sec):
    spines = sec.get("spines", {})
    n_cells = len(spines)
    total_tasks = sum(len(c.get("tasks_verbatim", [])) for c in spines.values())
    td_avg = total_tasks / n_cells if n_cells else 0

    wd_total = 0
    for spine_name in ("writing", "beyond_text"):
        cell = spines.get(spine_name, {})
        for t in cell.get("tasks_verbatim", []):
            wd_total += max(1, len(t.get("question_bank", [])))

    bt = spines.get("beyond_text", {})
    bt_items = sum(max(1, len(t.get("question_bank", []))) for t in bt.get("tasks_verbatim", []))

    sl, td, wd, pl = (tier_spine_load(n_cells), tier_task_density(td_avg),
                       tier_writing_demand(wd_total), tier_project_load(bt_items))
    ei = round(sl * 2 + td * 1.5 + wd * 1.5 + pl * 1, 1)
    return {"spine_load": sl, "task_density": td, "writing_demand": wd,
            "project_load": pl, "effort_index": ei}


def split_grade(grade):
    summ_dir = os.path.join(ROOT, grade, "summaries")
    map_dir = os.path.join(ROOT, grade, "mappings")
    out_summ_dir = os.path.join(ROOT, grade, "summaries_split")
    out_map_dir = os.path.join(ROOT, grade, "mappings_split")
    os.makedirs(out_summ_dir, exist_ok=True)
    os.makedirs(out_map_dir, exist_ok=True)

    files = sorted(f for f in os.listdir(summ_dir) if f.endswith("_summary.json"))
    true_num = 0
    report = []

    for f in files:
        summ = json.load(open(os.path.join(summ_dir, f)))
        map_f = f.replace("_summary.json", "_mapping.json")
        mapping = json.load(open(os.path.join(map_dir, map_f)))
        unit_title = summ["chapter_title"]
        unit_num = summ["chapter_number"]
        sections = summ.get("main_sections", [])
        total_pages = sum(s.get("page_count", 0) for s in sections) or 1
        by_spine = summ.get("competency_reporting", {}).get("by_spine", {})

        for i, sec in enumerate(sections):
            true_num += 1
            sec_title = sec.get("title", "")
            new_title = f"{sec_title} ({unit_title})"
            sec_spine_keys = set(sec.get("spines", {}).keys())

            # Step 7d (Grade VI pilot): chapter-scale effort signals computed fresh from
            # this section's own counts — not prorated from the Unit total.
            effort_signals = chapter_scale_effort_signals(sec)

            new_summary = {
                "subject": summ["subject"],
                "stage": summ["stage"],
                "grade": summ["grade"],
                "chapter_number": true_num,
                "chapter_title": new_title,
                "main_sections": [sec],
                "competency_reporting": {
                    "by_spine": {k: v for k, v in by_spine.items() if k in sec_spine_keys}
                },
                "effort_signals": effort_signals,
                "_source_unit": {
                    "unit_chapter_number": unit_num,
                    "unit_chapter_title": unit_title,
                    "section_id": sec.get("section_id"),
                    "page_count": sec.get("page_count"),
                    "page_share_of_unit": round(sec.get("page_count", 0) / total_pages, 4),
                },
            }
            out_summ_path = os.path.join(out_summ_dir, f"ch_{true_num:02d}_summary.json")
            json.dump(new_summary, open(out_summ_path, "w"), indent=2, ensure_ascii=False)

            primary = build_primary(by_spine, sec_spine_keys)
            new_mapping = {
                "stage": mapping["stage"],
                "subject": mapping["subject"],
                "grade": mapping["grade"],
                "chapter_number": true_num,
                "chapter_title": new_title,
                "summary_path": f"mirror/chapters/english/{grade}/summaries_split/ch_{true_num:02d}_summary.json",
                "primary": primary,
                "incidental": [],
                "spine_load": new_summary["effort_signals"]["spine_load"],
                "task_density": new_summary["effort_signals"]["task_density"],
                "writing_demand": new_summary["effort_signals"]["writing_demand"],
                "project_load": new_summary["effort_signals"]["project_load"],
                "effort_index": new_summary["effort_signals"]["effort_index"],
                "chapter_weight": None,
            }
            out_map_path = os.path.join(out_map_dir, f"ch_{true_num:02d}_mapping.json")
            json.dump(new_mapping, open(out_map_path, "w"), indent=2, ensure_ascii=False)

            report.append((true_num, new_title, sec.get("page_count"), new_summary["effort_signals"]["effort_index"]))

    return report


if __name__ == "__main__":
    grade = sys.argv[1] if len(sys.argv) > 1 else "vi"
    rep = split_grade(grade)
    print(f"grade {grade}: {len(rep)} true chapters written")
    for r in rep:
        print(f"  ch_{r[0]:02d}  {r[1]!r:60s} pages={r[2]:>3}  effort_index={r[3]}")
