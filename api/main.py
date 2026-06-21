"""
Aruvi API — the bridge between the web frontend and the Python engine.

Wraps the engine's three jobs over HTTP:
  - Allocate  : distribute a period budget across a subject's chapters (live, no LLM)
  - My Plans  : list saved plans, and serve any plan translated into the canonical view model
  - Generate  : stubbed for now (live generation deferred)

Importing the subject packages registers all five plugins with the engine registry.
Data comes from local disk (api/data.py) for now; live generation and the DB come later.
"""
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel

# Register all subjects (import side-effect).
import aruvi_core.subjects.english          # noqa: F401
import aruvi_core.subjects.mathematics      # noqa: F401
import aruvi_core.subjects.science          # noqa: F401
import aruvi_core.subjects.social_sciences  # noqa: F401
import aruvi_core.subjects.the_world_around_us  # noqa: F401
from aruvi_core import subjects
from aruvi_core.allocate import allocate_for_subject, allocate_schedule_for_subject
from aruvi_core.view_model import ViewModel

from . import data

app = FastAPI(title="Aruvi API", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)


class PeriodRow(BaseModel):
    minutes: int
    count: int


class AllocateRequest(BaseModel):
    # Either a multi-row schedule (preferred) or a single total (back-compat).
    period_rows: Optional[List[PeriodRow]] = None
    total_periods: Optional[int] = None


def _subject(name: str):
    try:
        return subjects.get(name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Unknown subject: {name}")


@app.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}


@app.get("/subjects")
def get_subjects() -> Dict[str, Any]:
    return {"subjects": subjects.available()}


@app.get("/subjects/{subject}/grades")
def get_grades(subject: str) -> Dict[str, Any]:
    _subject(subject)
    return {"subject": subject, "grades": data.list_grades(subject)}


@app.get("/subjects/{subject}/{grade}/chapters")
def get_chapters(subject: str, grade: str) -> Dict[str, Any]:
    sub = _subject(subject)
    chapters = [
        {"chapter_number": m.get("chapter_number"),
         "chapter_title": m.get("chapter_title", ""),
         "weight": sub.chapter_weight(m)}
        for m in data.load_mappings(subject, grade)
    ]
    return {"subject": subject, "grade": grade, "chapters": chapters,
            "allocation_basis": sub.allocation_basis(grade)}


@app.post("/subjects/{subject}/{grade}/allocate")
def post_allocate(subject: str, grade: str, req: AllocateRequest) -> Dict[str, Any]:
    _subject(subject)
    mappings = data.load_mappings(subject, grade)
    if not mappings:
        raise HTTPException(status_code=404, detail="No chapter mappings for that subject/grade.")

    if req.period_rows:
        rows = [r.model_dump() for r in req.period_rows]
        result = allocate_schedule_for_subject(subject, mappings, rows)
        return {"subject": subject, "grade": grade, **result}

    if req.total_periods is not None:  # back-compat single-total path
        allocs = allocate_for_subject(subject, mappings, req.total_periods)
        return {"subject": subject, "grade": grade, "total_periods": req.total_periods,
                "allocations": [a.__dict__ for a in allocs]}

    raise HTTPException(status_code=422, detail="Provide period_rows or total_periods.")


@app.get("/plans/{subject}/{grade}")
def get_plans(subject: str, grade: str) -> Dict[str, Any]:
    _subject(subject)
    return {"subject": subject, "grade": grade, "plans": data.list_saved_plans(subject, grade)}


@app.get("/plans/{subject}/{grade}/{filename}/view")
def get_plan_view(subject: str, grade: str, filename: str) -> Dict[str, Any]:
    sub = _subject(subject)
    saved = data.load_saved_plan(subject, grade, filename)
    if not saved:
        raise HTTPException(status_code=404, detail="Saved plan not found.")
    r = saved.get("result", {})
    chapter = {"chapter_number": saved.get("chapter_number"), "chapter_title": saved.get("chapter_title")}
    g = saved.get("grade", grade)
    lp = sub.lesson_plan_to_view(r.get("lesson_plan", {}), grade=g, chapter=chapter)
    a = sub.assessment_to_view(r.get("assessment_items", []), grade=g, chapter=chapter)
    return {"meta": chapter, "view": ViewModel(lp, a).to_dict()}


@app.post("/subjects/{subject}/{grade}/generate")
def generate(subject: str, grade: str) -> JSONResponse:
    """Stub — live generation is deferred. The frontend treats this as 'coming soon' and
    shows saved plans instead."""
    _subject(subject)
    return JSONResponse(
        status_code=501,
        content={"status": "deferred",
                 "detail": "Live generation is wired but intentionally deferred; "
                           "view a saved plan instead."},
    )
