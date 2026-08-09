#!/usr/bin/env python3
"""repair_c3.py v1.0 — 2026-08-09

Repairs the C3 defects that can be repaired without re-authoring, on an installed library.

Two kinds of pass, deliberately kept apart, because they scale differently:

  GENERIC passes derive the correct value from an AUTHORITATIVE SOURCE — the chapter summary,
  the Pedagogy document, the mapping JSON, the schema. They take no per-chapter input and are
  intended to run over the whole corpus at the mass pre-warm, exactly as STEP 6 does for option
  order. Adding a chapter costs nothing.

  DECLARED passes apply a hand-written table of old → new strings for one chapter. They do NOT
  generalise: a register phrasing or a word-count rewrite needs language, per instance. They are
  here so this chapter's repair is reproducible and auditable, and so the shared plumbing
  (backup · refuse-on-drift · declared repairs[] · idempotent) is written once.

Every pass refuses rather than guesses: if the value on disk matches neither the expected old
nor the already-repaired new, the file is left alone and the run reports it.

Run from the repo root:
    python3 genon/repair_c3.py mathematics ix 4 --dry-run
    python3 genon/repair_c3.py mathematics ix 4
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import re
import shutil
import sys

TOOL = "genon/repair_c3.py v1.0"
ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANS = ROOT / "data/content/saved_plans"
CHAPTERS = ROOT / "data/content/chapters"
BACKUP = ROOT / "backup/c3_repair"

# The Pedagogy document's method names, verbatim. Source of truth for ARV-D-071.
PEDAGOGY_METHODS = ["Play-way", "Discovery/Inquiry", "Problem solving", "Inductive", "Deductive"]

# Rule 8's closing requirement, in the constitution's own words.
SUBSTITUTION_CLAUSE = (
    " The teacher may substitute any other format from the Mathematics open-task menu."
)

# Both forms observed in the corpus: a bare parenthetical "(E-3)" and a narrated one
# "(from E-1)". The book_ref always precedes it, so both are pure deletion.
ID_IN_PROSE = re.compile(r"\s*\((?:from\s+)?(?:WE|E)-\d+\)")


# =======================================================================================
# GENERIC PASSES — corpus-safe, source-derived, no per-chapter input
# =======================================================================================

def pass_method_label(result, ctx):
    """ARV-D-071 — pedagogical_method named exactly as the Pedagogy document writes it."""
    edits = []
    lookup = {m.lower(): m for m in PEDAGOGY_METHODS}
    for period in result["lesson_plan"]["periods"]:
        current = period.get("pedagogical_method") or ""
        correct = lookup.get(current.lower())
        if correct and correct != current:
            edits.append({"unit": period["period_number"], "field": "pedagogical_method",
                          "old": current, "new": correct})
            period["pedagogical_method"] = correct
    return edits


def pass_strip_internal_ids(result, ctx):
    """ARV-D-073 — Rule 9 P5: no WE-N / E-N in teacher-facing text; the book_ref is already
    there, so the parenthetical is pure deletion."""
    edits = []
    for period in result["lesson_plan"]["periods"]:
        unit = period["period_number"]

        for idx, band in enumerate(period.get("time_bands", [])):
            cleaned = ID_IN_PROSE.sub("", band["activity"])
            if cleaned != band["activity"]:
                edits.append({"unit": unit, "field": f"time_bands[{idx}].activity",
                              "old": band["activity"], "new": cleaned})
                band["activity"] = cleaned

        for idx, item in enumerate(period.get("homework", [])):
            cleaned = ID_IN_PROSE.sub("", item)
            if cleaned != item:
                edits.append({"unit": unit, "field": f"homework[{idx}]",
                              "old": item, "new": cleaned})
                period["homework"][idx] = cleaned

        for field in ("teacher_notes", "activity_title"):
            cleaned = ID_IN_PROSE.sub("", period.get(field, ""))
            if cleaned != period.get(field, ""):
                edits.append({"unit": unit, "field": field,
                              "old": period[field], "new": cleaned})
                period[field] = cleaned
    return edits


def pass_verbatim_descriptions(result, ctx):
    """ARV-D-077 — A3: textbook item description is verbatim from the summary. The summary IS
    the authority, so this is a copy, not a judgement."""
    edits = []
    canon = ctx["summary_items"]
    for period in result["lesson_plan"]["periods"]:
        for idx, item in enumerate(period.get("textbook_items_in_class", [])):
            source = canon.get(item.get("id"))
            if not source:
                continue
            want = source.get("description")
            if want and item.get("description") != want:
                edits.append({"unit": period["period_number"],
                              "field": f"textbook_items_in_class[{idx}].description",
                              "old": item.get("description"), "new": want})
                item["description"] = want
    return edits


def pass_guide_shape(result, ctx):
    """ARV-D-083 — A1: 'Populate every field; empty strings and empty arrays are not permitted
    for required fields.' Rule 9 defines ONE guide sub-block per question type. Sub-blocks for
    other types are set to null, which is the shape the other two canonicals already use."""
    edits = []
    for pos, item in enumerate(iter_items(result), 1):
        guide = item.get("guide")
        if not isinstance(guide, dict):
            continue
        keep = item.get("question_type")
        for key, block in list(guide.items()):
            if key == keep or block is None:
                continue
            if isinstance(block, dict):
                empties = sum(1 for v in block.values() if v in ("", [], {}))
                # learning_outcome is a duplicate of the kept block's own; everything else in a
                # foreign block must be empty for it to be safely prunable. A foreign block
                # carrying real content is a different defect and is not ours to delete.
                substantive = {k: v for k, v in block.items() if k != "learning_outcome"}
                if any(v not in ("", [], {}, None) for v in substantive.values()):
                    continue
                edits.append({"item": pos, "field": f"guide.{key}",
                              "old": f"<{len(block)} keys, {empties} empty>", "new": None})
                guide[key] = None
    return edits


def pass_open_task_substitution(result, ctx):
    """ARV-D-082 — Rule 8 requires the guide to state that the teacher may substitute any other
    menu format. Fixed sentence, so it is computable."""
    edits = []
    for pos, item in enumerate(iter_items(result), 1):
        if item.get("question_type") != "OPEN_TASK":
            continue
        block = (item.get("guide") or {}).get("OPEN_TASK")
        if not isinstance(block, dict):
            continue
        rationale = block.get("format_rationale") or ""
        if "substitute" in rationale.lower():
            continue
        new = rationale.rstrip() + SUBSTITUTION_CLAUSE
        edits.append({"item": pos, "field": "guide.OPEN_TASK.format_rationale",
                      "old": rationale, "new": new})
        block["format_rationale"] = new
    return edits


GENERIC_PASSES = [
    ("ARV-D-071", "method label verbatim from the Pedagogy document", pass_method_label),
    ("ARV-D-073", "internal WE-N / E-N ids out of teacher-facing text", pass_strip_internal_ids),
    ("ARV-D-077", "textbook descriptions verbatim from the summary", pass_verbatim_descriptions),
    ("ARV-D-083", "one guide sub-block per question type; no empty required fields",
     pass_guide_shape),
    ("ARV-D-082", "Rule 8 substitution statement present in OPEN_TASK guides",
     pass_open_task_substitution),
]


# =======================================================================================
# DECLARED EDITS — this chapter only; each one needed language or a judgement
# =======================================================================================

# ARV-D-069 · the register's three bans. Forward reference and completion language rewritten to
#   stand on their own ground; the calendar word removed.
# ARV-D-070 · Rule 10 continuity by CONTENT, never by position. In every case the content is
#   already named, so the repair is deletion of the positional clause.
DECLARED = {
    "ch_04_canonical.json": {
        "ARV-D-069": [
            {"unit": 3, "field": "time_bands[2].activity",
             "old": "— that is the focal error today.",
             "new": "— that is the focal error to watch for."},
        ],
        "ARV-D-070": [
            {"unit": 12, "field": "time_bands[0].activity",
             "old": "Students who judged the derivations in the previous unit share their "
                    "verdicts",
             "new": "Students who judged these two derivations share their verdicts"},
            {"unit": 12, "field": "time_bands[2].activity",
             "old": "not finished in the previous unit,",
             "new": "not yet finished,"},
        ],
        "ARV-D-030": [
            {"row": 7, "field": "section_context",
             "old": "binomial cube identities, sum and difference of cubes, three-variable cube "
                    "identity, factorisation and numerical application",
             "new": "binomial cube identities, sum and difference of cubes, three-variable cube "
                    "identity"},
            {"row": 9, "field": "section_context",
             "old": "integrative identity selection, expansion, factorisation, rational "
                    "simplification, geometric and numerical application across the chapter",
             "new": "integrative identity selection, expansion, factorisation, and rational "
                    "simplification across the chapter"},
        ],
        "ARV-D-074": [
            {"row": 6, "field": "period_numbers", "old": [8, 9], "new": [8]},
            {"row": 7, "field": "period_numbers", "old": [10, 11, 12], "new": [10, 11]},
        ],
        "ARV-D-075": [
            {"row": 5, "field": "c_code", "old": "C-9.3", "new": "C-3.1"},
        ],
    },
    "ch_04_canonical_p12.json": {
        "ARV-D-069": [
            {"unit": 7, "field": "teacher_notes",
             "old": "two skills that will recur when simplifying rational expressions",
             "new": "two skills that also underpin the simplification of rational expressions"},
            {"unit": 7, "field": "teacher_notes",
             "old": "may be set for later self-study once section 4.7 has been taught.",
             "new": "may be set for self-study by students who have already met the cube "
                    "identities."},
            {"unit": 7, "field": "homework[0]",
             "old": "End of Chapter Q1, p.88 — complete any remaining parts (vii)–(ix) after "
                    "section 4.7 is covered.",
             "new": "End of Chapter Q1, p.88 — complete any remaining parts (vii)–(ix), which "
                    "draw on the cube identities."},
            {"unit": 12, "field": "teacher_notes",
             "old": "a natural place for a final unit that advances coverage",
             "new": "a natural place for a unit that advances coverage"},
        ],
        "ARV-D-070": [
            {"unit": 3, "field": "teacher_notes",
             "old": "Having derived (a+b)² in the previous unit, this unit runs",
             "new": "Having derived (a+b)², this unit runs"},
            {"unit": 6, "field": "teacher_notes",
             "old": "Having seen middle-term splitting via the tile model in the previous unit, "
                    "students now",
             "new": "Having seen middle-term splitting via the tile model, students now"},
            {"unit": 9, "field": "teacher_notes",
             "old": "Having derived the binomial-cube identities in the previous unit, this unit",
             "new": "Having derived the binomial-cube identities, this unit"},
            {"unit": 11, "field": "teacher_notes",
             "old": "a higher demand than the rational-expression simplification of the previous "
                    "unit.",
             "new": "a higher demand than rational-expression simplification."},
        ],
    },
    "ch_04_canonical_p09.json": {
        "ARV-D-070": [
            {"unit": 2, "field": "time_bands[0].activity",
             "old": "Revisit the identity (a+b)^2 = a^2+2ab+b^2 from the previous unit's work and "
                    "pose",
             "new": "Revisit the identity (a+b)^2 = a^2+2ab+b^2 and pose"},
            {"unit": 9, "field": "time_bands[2].activity",
             "old": "for any items not completed in the previous unit.",
             "new": "for any items not yet completed."},
        ],
        "ARV-D-030": [
            {"row": 5, "field": "section_context",
             "old": "x^2, x, and unit tiles; rectangle model for (x+3)(x+4) and (2x+3)(3x+1); "
                    "middle-term split validated spatially",
             "new": "x^2, x, and unit tiles; rectangle model validating the middle-term split "
                    "spatially"},
        ],
        "ARV-D-075": [
            {"row": 5, "field": "c_code", "old": "C-9.3", "new": "C-3.1"},
            {"row": 6, "field": "c_code", "old": "C-3.1", "new": "C-9.3"},
        ],
    },
}


# =======================================================================================
# plumbing
# =======================================================================================

def iter_items(obj):
    if isinstance(obj, dict):
        if isinstance(obj.get("questions"), list):
            yield from obj["questions"]
        if isinstance(obj.get("assessment_items"), list):
            yield from obj["assessment_items"]
        for value in obj.values():
            yield from iter_items(value)
    elif isinstance(obj, list):
        for value in obj:
            yield from iter_items(value)


def unit_of(result, number):
    for period in result["lesson_plan"]["periods"]:
        if period["period_number"] == number:
            return period
    raise KeyError(f"no unit {number}")


def get_nested(container, field):
    match = re.fullmatch(r"(\w+)\[(\d+)\](?:\.(\w+))?", field)
    if not match:
        return container[field]
    name, idx, leaf = match.group(1), int(match.group(2)), match.group(3)
    target = container[name][idx]
    return target[leaf] if leaf else target


def set_nested(container, field, value):
    match = re.fullmatch(r"(\w+)\[(\d+)\](?:\.(\w+))?", field)
    if not match:
        container[field] = value
        return
    name, idx, leaf = match.group(1), int(match.group(2)), match.group(3)
    if leaf:
        container[name][idx][leaf] = value
    else:
        container[name][idx] = value


def apply_declared(result, table, filename):
    """Substring replacement inside a named field, or whole-value replacement for non-strings."""
    edits, refusals = [], []
    for defect, entries in table.items():
        for entry in entries:
            if "row" in entry:
                rows = [r for r in result["coverage_handoff"]
                        if r["section_number"] == entry["row"]]
                if not rows:
                    refusals.append(f"{filename}: no handoff row {entry['row']}")
                    continue
                container, label = rows[0], f"sec#{entry['row']}"
            else:
                container, label = unit_of(result, entry["unit"]), f"U{entry['unit']}"

            current = get_nested(container, entry["field"])

            if isinstance(entry["old"], str):
                # Order matters: `new` is often a PREFIX of `old` (a shortened label), so the
                # already-repaired test must run only after the old text is ruled out.
                if entry["old"] in (current or ""):
                    updated = current.replace(entry["old"], entry["new"])
                elif entry["new"] in (current or ""):
                    continue                              # already repaired
                else:
                    refusals.append(
                        f"{filename} {label}.{entry['field']}: expected text absent — "
                        f"{entry['old'][:60]!r}")
                    continue
            else:
                if current == entry["new"]:
                    continue
                if current != entry["old"]:
                    refusals.append(
                        f"{filename} {label}.{entry['field']}: expected {entry['old']!r}, "
                        f"found {current!r}")
                    continue
                updated = entry["new"]

            set_nested(container, entry["field"], updated)
            edits.append({"defect": defect, "where": label, "field": entry["field"],
                          "old": entry["old"], "new": entry["new"]})
    return edits, refusals


def load_summary_items(subject, grade, chapter):
    path = CHAPTERS / subject / grade / "summaries" / f"ch_{chapter:02d}_summary.json"
    if not path.exists():
        return {}
    summary = json.loads(path.read_text(encoding="utf-8"))
    out = {}
    for key in ("enumerated_worked_examples", "enumerated_exercises"):
        for item in summary.get(key, []):
            out[item["id"]] = item
    return out


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("subject")
    parser.add_argument("grade")
    parser.add_argument("chapter", type=int)
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    folder = PLANS / args.subject / args.grade
    files = sorted(folder.glob(f"ch_{args.chapter:02d}_canonical*.json"))
    if not files:
        print(f"no library at {folder}")
        return 1

    ctx = {"summary_items": load_summary_items(args.subject, args.grade, args.chapter)}
    now = datetime.datetime.now().replace(microsecond=0).isoformat()
    stamp = now.replace("-", "").replace(":", "").replace("T", "_")
    refused_any = False

    for path in files:
        doc = json.loads(path.read_text(encoding="utf-8"))
        result = doc["result"]
        by_defect = {}

        for defect, label, fn in GENERIC_PASSES:
            edits = fn(result, ctx)
            if edits:
                by_defect.setdefault(defect, {"label": label, "edits": []})["edits"].extend(edits)

        declared, refusals = apply_declared(result, DECLARED.get(path.name, {}), path.name)
        for edit in declared:
            by_defect.setdefault(edit["defect"], {"label": "declared edit", "edits": []})
            by_defect[edit["defect"]]["edits"].append(
                {k: v for k, v in edit.items() if k != "defect"})
        for line in refusals:
            refused_any = True
            print(f"  REFUSED {line}")

        if not by_defect:
            print(f"OK    {path.name} — nothing to repair")
            continue

        summary = ", ".join(f"{d} ×{len(v['edits'])}" for d, v in sorted(by_defect.items()))
        if args.dry_run:
            print(f"WOULD REPAIR {path.name} — {summary}")
            continue

        backup_dir = BACKUP / stamp
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy(path, backup_dir / path.name)

        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": TOOL,
            "at": now,
            "reason": "C3 defect repair (testing.md C3 · S4 mathematics·secondary). Generic "
                      "passes derive their value from the summary, the Pedagogy document or the "
                      "schema; declared edits are hand-written per instance and listed with "
                      "their defect id. No pedagogical content was regenerated: register and "
                      "continuity edits delete or rephrase a clause whose content is already "
                      "named, and word-count edits shorten a label without adding a fact.",
            "defects": {d: {"note": v["label"], "edits": v["edits"]}
                        for d, v in sorted(by_defect.items())},
        })

        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"REPAIRED {path.name} — {summary}")

    if not args.dry_run:
        print(f"\nbackups: backup/c3_repair/{stamp}/")
    return 1 if refused_any else 0


if __name__ == "__main__":
    sys.exit(main())
