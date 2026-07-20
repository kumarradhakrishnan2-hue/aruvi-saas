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
                                "chapter_title": s.get("chapter_title"), "saved_at": s.get("saved_at")})
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
