#!/usr/bin/env python3
"""repair_leaked_deliberation.py v1.0 — 2026-08-09

Repairs installed canonical files where the MODEL'S OWN SELF-CORRECTION survived into a
shipped, human-facing field — and, in both known cases, a wrong or degenerate value shipped
beside it.

Found at S4's C3 (maths) and by the corpus-wide sweep that followed it (science). Two hits in
the 16 installed canonical files; both are item 4, which is coincidence.

  ARV-D-084  mathematics/ix/ch_04_canonical.json     item 4  expected_answer + method_one_line
  ARV-D-085  science/ix/ch_08_canonical_p07.json     item 4  question_text + expected_elements

This is a DECLARED IN-PLACE REPAIR at zero cost, in the sense of testing.md C3 / P2's
"standing corpus-repair debt": nothing is regenerated, every edit is recorded field-by-field
in `genon_canonical.repairs[]`, and the script is idempotent — a second run reports
"already repaired" and writes nothing.

Run from the repo root:
    python3 genon/repair_leaked_deliberation.py            # apply
    python3 genon/repair_leaked_deliberation.py --dry-run  # show the diff only
"""
from __future__ import annotations

import argparse
import datetime
import json
import pathlib
import shutil
import sys

TOOL = "genon/repair_leaked_deliberation.py v1.0"
ROOT = pathlib.Path(__file__).resolve().parents[1]
PLANS = ROOT / "data/content/saved_plans"
BACKUP = ROOT / "backup/answer_repair"

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
from purge_derived import purge                                    # noqa: E402

# --------------------------------------------------------------------------------------
# The repair table. Every edit names the item by its 1-based position in the flattened
# question stream (the same index C3's battery and carriers.assessment_items() use), and
# carries the FULL expected old value so a drifted file refuses the edit rather than
# silently mangling it.
# --------------------------------------------------------------------------------------

MATHS_OLD_ANSWER = "8(3m − 2n)^2"
MATHS_NEW_ANSWER = "8(3m − n)^2"

MATHS_OLD_METHOD = (
    "Extract the common factor 8 to get 8(9m^2 − 12mn + n^2) — wait, verify: "
    "9m^2−12mn+n^2... Let me re-check. 72m^2−48mn+8n^2 = 8(9m^2−6mn+n^2). "
    "Check: 9m^2−6mn+n^2 = (3m)^2 − 2(3m)(n) + n^2 = (3m−n)^2. So the answer is "
    "8(3m−n)^2."
)
MATHS_NEW_METHOD = (
    "Extract the common factor 8 to get 8(9m^2 − 6mn + n^2); the trinomial matches "
    "(3m)^2 − 2(3m)(n) + n^2, so it factorises as (3m − n)^2 and the complete "
    "factored form is 8(3m − n)^2."
)

SCIENCE_OLD_STEM = (
    "An atom of phosphorus is represented as ³¹₁₅P. (a) State the number of "
    "protons, neutrons, and electrons in this atom. Show the calculation for neutron count. "
    "(b) A second atom has the symbol ²⁷₁₃Al. Write the full nuclide notation "
    "for an atom of the same element that has 14 neutrons instead of 14 — wait, this atom "
    "has 14 neutrons. Calculate its mass number and write the corrected nuclide notation. "
    "(c) Explain in one sentence why the symbol for iron is Fe and not Ir, using the IUPAC rule "
    "for symbols derived from non-English names."
)
SCIENCE_NEW_STEM = (
    "An atom of phosphorus is represented as ³¹₁₅P. (a) State the number of "
    "protons, neutrons, and electrons in this atom. Show the calculation for neutron count. "
    "(b) A second atom has the symbol ²⁷₁₃Al. Write the full nuclide notation "
    "for an atom of the same element that has 15 neutrons. Calculate its mass number and show "
    "your working. (c) Explain in one sentence why the symbol for iron is Fe and not Ir, using "
    "the IUPAC rule for symbols derived from non-English names."
)

SCIENCE_OLD_ELEMENT = (
    "For aluminium with 14 neutrons: A = Z + neutrons = 13 + 14 = 27; nuclide notation "
    "²⁷₁₃Al — same as the given atom, demonstrating correct application "
    "of A = Z + n."
)
SCIENCE_NEW_ELEMENT = (
    "For aluminium with 15 neutrons: A = Z + neutrons = 13 + 15 = 28; nuclide notation "
    "²⁸₁₃Al — same Z as the given atom but a different A, so it is an "
    "isotope of aluminium."
)

REPAIRS = [
    {
        "path": "mathematics/ix/ch_04_canonical.json",
        "defect": "ARV-D-084",
        "reason": (
            "ARV-D-084 (S1, testing.md C3) — item 4 shipped a WRONG verified answer with "
            "the model's own re-derivation left visible beside it. 8(3m − 2n)^2 expands to "
            "72m^2 − 96mn + 32n^2, not the stem's 72m^2 − 48mn + 8n^2; the correct "
            "factorisation is 8(3m − n)^2 — which method_one_line itself arrived at "
            "after a 'wait, verify... Let me re-check' aside, and which the item's own guide "
            "already names in its inclusivity note. The repair adopts the value the file was "
            "already carrying in two of its three places and removes the deliberation. No "
            "pedagogical content is invented: the stem, the identity taught and the guide are "
            "untouched."
        ),
        "edits": [
            {"item": 4, "field": "expected_answer",
             "old": MATHS_OLD_ANSWER, "new": MATHS_NEW_ANSWER},
            {"item": 4, "field": "method_one_line",
             "old": MATHS_OLD_METHOD, "new": MATHS_NEW_METHOD},
        ],
    },
    {
        "path": "science/ix/ch_08_canonical_p07.json",
        "defect": "ARV-D-085",
        "reason": (
            "ARV-D-085 (S1, opened by the 2026-08-09 corpus sweep off ARV-D-084) — item "
            "4(b) shipped the model's self-correction inside the STUDENT-FACING stem ('that has "
            "14 neutrons instead of 14 — wait, this atom has 14 neutrons'), and the answer "
            "key had settled the stumble the wrong way: it resolved (b) to "
            "²⁷₁₃Al, the same atom the stem hands the student, making the "
            "part unanswerable as written and pointless as keyed. Founder ruling 2026-08-09: "
            "restore the isotope teaching point the phrase 'the corrected nuclide notation' was "
            "reaching for — 15 neutrons, A = 28. The LO ('determine the subatomic particle "
            "composition of an atom from given nuclear data'), the section anchor, the "
            "competency and parts (a) and (c) are untouched."
        ),
        "edits": [
            {"item": 4, "field": "question_text",
             "old": SCIENCE_OLD_STEM, "new": SCIENCE_NEW_STEM},
            {"item": 4, "field": "expected_elements[1]",
             "old": SCIENCE_OLD_ELEMENT, "new": SCIENCE_NEW_ELEMENT},
        ],
    },
]


# --------------------------------------------------------------------------------------
# Item access — the flattened question stream, in the order carriers.assessment_items()
# walks it, so an item number here means what it means in the C3 artefact.
# --------------------------------------------------------------------------------------

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


def read_field(item: dict, field: str):
    if field.endswith("]") and "[" in field:
        name, idx = field[:-1].split("[")
        return item[name][int(idx)]
    return item[field]


def write_field(item: dict, field: str, value) -> None:
    if field.endswith("]") and "[" in field:
        name, idx = field[:-1].split("[")
        item[name][int(idx)] = value
    else:
        item[field] = value


def apply_file(spec: dict, stamp: str, now: str, dry_run: bool) -> str:
    path = PLANS / spec["path"]
    if not path.exists():
        return f"SKIP  {spec['path']} — not on disk"

    doc = json.loads(path.read_text(encoding="utf-8"))
    items = list(iter_items(doc))

    already = 0
    pending = []
    for edit in spec["edits"]:
        item = items[edit["item"] - 1]
        current = read_field(item, edit["field"])
        if current == edit["new"]:
            already += 1
        elif current == edit["old"]:
            pending.append((item, edit))
        else:
            return (f"REFUSED {spec['path']} — item {edit['item']}.{edit['field']} matches "
                    f"neither the expected old nor the new value; the file has drifted and "
                    f"must be inspected by hand.\n         on disk: {current!r}")

    if not pending:
        return f"OK    {spec['path']} — already repaired ({already}/{len(spec['edits'])} fields)"

    if dry_run:
        lines = [f"WOULD REPAIR {spec['path']} ({spec['defect']})"]
        for _, edit in pending:
            lines.append(f"    item {edit['item']} · {edit['field']}")
            lines.append(f"      - {edit['old']}")
            lines.append(f"      + {edit['new']}")
        return "\n".join(lines)

    backup_dir = BACKUP / stamp
    backup_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy(path, backup_dir / path.name)

    for item, edit in pending:
        write_field(item, edit["field"], edit["new"])

    doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
        "tool": TOOL,
        "at": now,
        "reason": spec["reason"],
        "edits": [
            {"item": e["item"], "field": e["field"], "old": e["old"], "new": e["new"]}
            for _, e in pending
        ],
    })

    path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
    return (f"REPAIRED {spec['path']} — {len(pending)} field(s), {spec['defect']}; "
            f"backup {backup_dir.relative_to(ROOT)}/{path.name}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true",
                        help="show the edits without writing")
    args = parser.parse_args()

    now = datetime.datetime.now().replace(microsecond=0).isoformat()
    stamp = now.replace("-", "").replace(":", "").replace("T", "_")

    failed = False
    touched = set()
    for spec in REPAIRS:
        line = apply_file(spec, stamp, now, args.dry_run)
        if line.startswith("REFUSED"):
            failed = True
        if line.startswith("REPAIRED"):
            subject, grade, name = spec["path"].split("/")
            touched.add((subject, grade, int(name.split("_")[1])))
        print(line)
    # PURGE THE DERIVED PLANS (testing.md C10.2b, ARV-D-034) — an in-place repair does not
    # move the cache key, so pre-repair bytes would keep being served. Found missing at S4's C10.
    for subject, grade, ch in sorted(touched):
        purge(subject, grade, ch, reason=f"{TOOL} — leaked-deliberation repair")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
