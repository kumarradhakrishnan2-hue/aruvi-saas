"""Local-disk data access (mappings + saved plans). A stand-in for the cloud content
store / DB; isolated here so swapping it later touches only this file."""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from .config import DATA_DIR


def _isdir(*parts) -> bool:
    return os.path.isdir(os.path.join(DATA_DIR, *parts))


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
