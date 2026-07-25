"""Local-disk data access (mappings + saved plans). A stand-in for the cloud content
store / DB; isolated here so swapping it later touches only this file."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from .config import DATA_DIR


def _isdir(*parts) -> bool:
    return os.path.isdir(os.path.join(DATA_DIR, *parts))


_ncf_norms_cache: Optional[Dict[str, Any]] = None


def load_ncf_period_norms() -> Dict[str, Any]:
    """National Curricular Framework period norms (periods/year by subject·stage), founder-
    supplied Bucket A content. Cached in-process; file only changes via a manual edit."""
    global _ncf_norms_cache
    if _ncf_norms_cache is None:
        p = os.path.join(DATA_DIR, "allocation_norms", "ncf_period_norms.json")
        try:
            _ncf_norms_cache = json.load(open(p)).get("subjects", {})
        except Exception:
            _ncf_norms_cache = {}
    return _ncf_norms_cache


def ncf_total_periods(subject: str, stage: str) -> Optional[int]:
    """The NCF-recommended total periods/year for this subject·stage, or None if the norm
    table has no figure for that combination (e.g. Science has none for preparatory)."""
    v = load_ncf_period_norms().get(subject, {}).get(stage)
    return int(v) if v is not None else None


def list_grades(subject: str) -> List[str]:
    base = os.path.join(DATA_DIR, "chapters", subject)
    if not os.path.isdir(base):
        return []
    return sorted(d for d in os.listdir(base) if os.path.isdir(os.path.join(base, d)))


def load_mappings(subject: str, grade: str) -> List[Dict[str, Any]]:
    d = os.path.join(DATA_DIR, "chapters", subject, grade, "mappings")
    out: List[Dict[str, Any]] = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith("_mapping.json"):
                try:
                    out.append(json.load(open(os.path.join(d, f))))
                except Exception:
                    pass
    out.sort(key=lambda m: m.get("chapter_number", 0))
    return out


def load_competency_descriptions(subject: str, grade: str) -> Dict[str, str]:
    """Flatten the framework's competency-description glossary into {code: description}.

    The file lives at framework/{subject}/{stage}/competency_descriptions_*.json and is
    nested as curricular_goals[CG-x].competency_codes[C-x.y] = "description". Mapping JSONs
    only carry the code + justification, so the human-readable competency text comes from
    here. Returns {} if the glossary is missing (report then shows the code alone).
    """
    from aruvi_core.grades import stage_for, UnknownGradeError
    try:
        stage = stage_for(grade)
    except UnknownGradeError:
        return {}
    d = os.path.join(DATA_DIR, "framework", subject, stage)
    if not os.path.isdir(d):
        return {}
    out: Dict[str, str] = {}
    for f in sorted(os.listdir(d)):
        if f.startswith("competency_descriptions") and f.endswith(".json"):
            try:
                doc = json.load(open(os.path.join(d, f)))
            except Exception:
                continue
            out.update(_flatten_descriptions(doc))
    return out


def load_english_spine_map(grade: str) -> Dict[str, Any]:
    """The standardized English spine → section → competency map (spine_to_cg.json) for the
    grade's stage. English carries the SAME competencies in every chapter, so the LP presents
    this fixed spine table instead of the per-chapter targeted competencies other subjects
    generate. Returns {} if the file is missing (LP then omits the competency table)."""
    from aruvi_core.grades import stage_for, UnknownGradeError
    try:
        stage = stage_for(grade)
    except UnknownGradeError:
        return {}
    p = os.path.join(DATA_DIR, "framework", "english", stage, "spine_to_cg.json")
    if not os.path.isfile(p):
        return {}
    try:
        return json.load(open(p))
    except Exception:
        return {}


def _flatten_descriptions(doc: Dict[str, Any]) -> Dict[str, str]:
    """Flatten a competency-descriptions doc to {code: description}, tolerating the
    three schemas in the data:

      1. curricular_goals as a DICT  (english, mathematics):
         {"CG-1": {"competency_codes": {"C-1.1": "desc", ...}}, ...}
      2. curricular_goals as a LIST  (science, the_world_around_us):
         [{"cg_code": "...", "competencies": [{"code": "C-1.1", "description": "..."}]}, ...]
      3. flat top-level map          (social_sciences):
         {"C-1.1": "desc", "C-1.2": "desc", ...}  (curricular_goals absent/None)
    """
    out: Dict[str, str] = {}
    cg = doc.get("curricular_goals")

    if isinstance(cg, dict):  # schema 1
        for goal in cg.values():
            if isinstance(goal, dict):
                for code, desc in (goal.get("competency_codes") or {}).items():
                    out[code] = desc
    elif isinstance(cg, list):  # schema 2
        for goal in cg:
            if not isinstance(goal, dict):
                continue
            comps = goal.get("competencies") or goal.get("competency_codes")
            if isinstance(comps, dict):
                out.update({k: v for k, v in comps.items() if isinstance(v, str)})
            elif isinstance(comps, list):
                for c in comps:
                    if isinstance(c, dict):
                        code = c.get("code") or c.get("c_code")
                        if code:
                            out[code] = c.get("description", "")
    else:  # schema 3 — flat {code: description} at the top level
        for k, v in doc.items():
            if isinstance(v, str) and k not in ("subject", "stage", "source"):
                out[k] = v
    return out


def list_saved_plans(subject: str, grade: str) -> List[Dict[str, Any]]:
    d = os.path.join(DATA_DIR, "saved_plans", subject, grade)
    out: List[Dict[str, Any]] = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.endswith(".json"):
                try:
                    s = json.load(open(os.path.join(d, f)))
                    out.append({"filename": f, "chapter_number": s.get("chapter_number"),
                                "chapter_title": s.get("chapter_title"), "saved_at": s.get("saved_at"),
                                "is_canonical": s.get("plan_status") == "canonical",
                                "duration_label": duration_label(s)})
                except Exception:
                    pass
    out.sort(key=lambda p: (p.get("chapter_number") or 0, p.get("saved_at") or ""))
    return out


def load_saved_plan(subject: str, grade: str, filename: str) -> Optional[Dict[str, Any]]:
    # guard against path traversal
    if "/" in filename or "\\" in filename or ".." in filename:
        return None
    p = os.path.join(DATA_DIR, "saved_plans", subject, grade, filename)
    if not os.path.isfile(p):
        return None
    return json.load(open(p))


# ── master allocation plan (2026-07-25) ─────────────────────────────────────────
# data/content/allocation_norms/master_plan.json — derived from the founder's
# allocation workbook (ncf_chapterwise_period_allocation.xlsx) by genon/master_plan.py.
# It knows the FULL syllabus per subject·grade, INCLUDING placeholder chapters that
# have no content yet — so it is the single source for allocation numerators
# (chapter effort weight) and denominators (total syllabus weight). The mappings-
# derived chapter list must never be the denominator: it only sees chapters with
# content, which inflates every suggestion until the full book lands.

_ROMAN_BY_SLUG = {"iii": "III", "iv": "IV", "v": "V", "vi": "VI", "vii": "VII",
                  "viii": "VIII", "ix": "IX", "x": "X"}
_master_plan_cache: Optional[tuple] = None   # (mtime, doc)


def load_master_plan() -> Optional[Dict[str, Any]]:
    global _master_plan_cache
    p = os.path.join(DATA_DIR, "allocation_norms", "master_plan.json")
    if not os.path.isfile(p):
        return None
    mtime = os.path.getmtime(p)
    if _master_plan_cache and _master_plan_cache[0] == mtime:
        return _master_plan_cache[1]
    doc = json.load(open(p))
    _master_plan_cache = (mtime, doc)
    return doc


def master_combo(subject: str, grade: str) -> Optional[Dict[str, Any]]:
    """The master plan's record for a subject·grade (grade as slug, e.g. 'ix')."""
    doc = load_master_plan()
    if not doc:
        return None
    roman = _ROMAN_BY_SLUG.get((grade or "").lower())
    return (doc.get("combos") or {}).get(f"{subject}|{roman}") if roman else None


# ── genon canonicals (relocated 2026-07-25, founder decision) ───────────────────
# data/content/ is the home of ALL crucial server content, and saved_plans/ is the
# home of lesson plans — so the certified canonicals live THERE, as ordinary
# saved-plan files named ch_NN_canonical.json (plan_status "canonical"). The genon/
# folder holds engine code only, never content. The phase stream is DERIVED: it is
# compiled on demand from the canonical (strict v0.3) and memo-cached per file
# mtime — no separate stream artifact on disk.

def duration_label(saved: Dict[str, Any]) -> Optional[str]:
    """Small-letter duration line for ADAPTED plans, e.g. "45 min × 12" or
    "40 min × 10 · 30 min × 4". The canonical (and any plan whose matrix matches
    the canonical's standard row) shows no label — it goes by its chapter name
    alone (founder naming rule, 2026-07-25)."""
    g = saved.get("genon") or {}
    matrix = g.get("matrix")
    if not matrix:
        return None
    return " · ".join(f"{m['duration']} min × {m['count']}" for m in matrix)


def _canonical_path(subject: str, grade: str, chapter_number: int) -> str:
    return os.path.join(DATA_DIR, "saved_plans", subject, grade,
                        f"ch_{int(chapter_number):02d}_canonical.json")


def canonical_mtime(subject: str, grade: str, chapter_number: int) -> Optional[float]:
    p = _canonical_path(subject, grade, chapter_number)
    return os.path.getmtime(p) if os.path.isfile(p) else None


def genon_chapters(subject: str, grade: str) -> List[int]:
    """Chapter numbers with a certified canonical for this subject·grade."""
    d = os.path.join(DATA_DIR, "saved_plans", subject, grade)
    out: List[int] = []
    if os.path.isdir(d):
        for f in sorted(os.listdir(d)):
            if f.startswith("ch_") and f.endswith("_canonical.json"):
                try:
                    out.append(int(f[3:5]))
                except ValueError:
                    pass
    return out


def load_genon_canonical(subject: str, grade: str, chapter_number: int) -> Optional[Dict[str, Any]]:
    p = _canonical_path(subject, grade, chapter_number)
    if not os.path.isfile(p):
        return None
    return json.load(open(p))


_stream_cache: Dict[str, Any] = {}   # path -> (mtime, stream)


def load_genon_stream(subject: str, grade: str, chapter_number: int) -> Optional[Dict[str, Any]]:
    """The chapter's phase stream, compiled (strict, declared-only) from its canonical.
    Memo-cached per file mtime, so the millisecond partition path never pays the
    compile twice for an unchanged canonical."""
    p = _canonical_path(subject, grade, chapter_number)
    if not os.path.isfile(p):
        return None
    mtime = os.path.getmtime(p)
    hit = _stream_cache.get(p)
    if hit and hit[0] == mtime:
        return hit[1]
    from aruvi_core.genon import compile_stream
    stream = compile_stream(json.load(open(p)))
    _stream_cache[p] = (mtime, stream)
    return stream


def save_generated_plan(subject: str, grade: str, plan: Dict[str, Any]) -> str:
    """Persist a genon-adapted plan into the saved-plans library; returns the filename.

    Adapted plans join the same library the viewer/exporters read; per-teacher
    visibility comes from the prepared-plans register, not from where the file sits.
    """
    from datetime import datetime
    d = os.path.join(DATA_DIR, "saved_plans", subject, grade)
    os.makedirs(d, exist_ok=True)
    nn = f"{int(plan.get('chapter_number') or 0):02d}"
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"ch_{nn}_{ts}.json"
    seq = 1
    while os.path.exists(os.path.join(d, filename)):   # same-second uniqueness
        filename = f"ch_{nn}_{ts}_{seq}.json"
        seq += 1
    plan["filename"] = filename
    plan["saved_at"] = datetime.now().isoformat(timespec="seconds")
    with open(os.path.join(d, filename), "w") as f:
        json.dump(plan, f, ensure_ascii=False, indent=2)
    return filename
