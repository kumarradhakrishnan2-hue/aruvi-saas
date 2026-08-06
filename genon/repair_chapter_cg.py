#!/usr/bin/env python3
"""repair_chapter_cg.py — write the missing top-level `chapter_cg` onto an LP artefact (v1.0, 2026-08-06).

WHY (ARV-D-055, found at S3 · science · secondary C3). Amendment A3 requires the LP JSON to
carry `chapter_cg` — "parent Curricular Goal from competency mapping JSON; chosen once at
chapter level, identical for all sections (auditability)". Every file in the science IX ch 8
library came back with it **null**, while each file's own assessment JSON carried
`chapter_cg: "CG-1"` correctly. So the value was known to the model and simply not written to
the LP side.

SAME SAFETY DOCTRINE as repair_register.py / repair_anchors.py, and this script is narrower
than either:
  * it writes ONE named field, and only where that field is currently absent or null. A file
    whose chapter_cg is already set is left untouched and reported as skipped.
  * the value is not invented and not copied from prose: it is read from the chapter's
    COMPETENCY MAPPING JSON (`primary[0].cg`), the constitutional source A3 names. The
    assessment JSON's value is cross-checked and a mismatch FAILS the run rather than
    choosing a winner.
  * nothing else in the artefact is touched — no teaching text, no anchors, no items.
  * the artefact records what was done in genon_canonical.repairs[], so corpus statistics can
    separate generation quality from repair quality.

    python3 genon/repair_chapter_cg.py science ix 8            # dry run
    python3 genon/repair_chapter_cg.py science ix 8 --apply    # back up, apply, record
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))

SAVED = REPO / "data" / "content" / "saved_plans"
BACKUP = REPO / "backup" / "chapter_cg_repair"
TOOL = "genon/repair_chapter_cg.py v1.0"


def mapping_cg(subject: str, grade: str, ch: int) -> str:
    m = json.loads((REPO / "data/content/chapters" / subject / grade / "mappings"
                    / f"ch_{ch:02d}_mapping.json").read_text(encoding="utf-8"))
    prim = m.get("primary") or []
    cgs = sorted({str(p.get("cg") or "").strip() for p in prim if p.get("cg")})
    if len(cgs) != 1:
        raise SystemExit(f"mapping does not name exactly one parent CG: {cgs} — "
                         "A3 says the chapter CG is chosen ONCE; resolve by hand.")
    return cgs[0]


def main() -> int:
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    apply = "--apply" in sys.argv
    if len(args) != 3:
        raise SystemExit(__doc__)
    subject, grade, ch = args[0], args[1].lower(), int(args[2])

    cg = mapping_cg(subject, grade, ch)
    lib = SAVED / subject / grade
    files = sorted(lib.glob(f"ch_{ch:02d}_canonical*.json"))
    if not files:
        raise SystemExit(f"no library at {lib}")
    print(f"chapter CG from the mapping: {cg!r}   ({len(files)} file(s))\n")

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    touched = 0
    for f in files:
        doc = json.loads(f.read_text(encoding="utf-8"))
        r = doc.get("result", doc)
        cur = r.get("chapter_cg")
        acg = (r.get("assessment_items") or {})
        acg = acg.get("chapter_cg") if isinstance(acg, dict) else None
        if acg and str(acg).strip() != cg:
            raise SystemExit(f"{f.name}: assessment says {acg!r} but the mapping says {cg!r} — "
                             "a mismatch is a content question, not a serialization repair.")
        if str(cur or "").strip():
            print(f"  {f.name}: already set ({cur!r}) — skipped")
            continue
        print(f"  {f.name}: chapter_cg {cur!r} -> {cg!r}"
              + (f"   (assessment side already carried {acg!r})" if acg else ""))
        touched += 1
        if not apply:
            continue
        BACKUP.mkdir(parents=True, exist_ok=True)
        shutil.copy2(f, BACKUP / f"{grade}_{f.stem}_{stamp}.json")
        r["chapter_cg"] = cg
        gc = doc.setdefault("genon_canonical", {})
        gc.setdefault("repairs", []).append({
            "tool": TOOL, "at": datetime.now().isoformat(timespec="seconds"),
            "reason": "ARV-D-055 — Amendment A3 requires chapter_cg on the LP JSON; the "
                      "generated artefact left it null while its own assessment JSON carried "
                      "it correctly",
            "edits": [{"field": "result.chapter_cg", "old": cur, "new": cg,
                       "source": f"data/content/chapters/{subject}/{grade}/mappings/"
                                 f"ch_{ch:02d}_mapping.json primary[].cg"}],
        })
        f.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")

    if apply and touched:
        from purge_derived import purge
        purge(subject, grade, ch, reason=TOOL)
        print(f"\nbacked up to backup/chapter_cg_repair/ · {touched} file(s) written")
    elif not apply:
        print(f"\ndry run — {touched} file(s) would change; re-run with --apply to write.")
    else:
        print("\nnothing to do.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
