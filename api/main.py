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
from aruvi_core import subjects, engine
from aruvi_core.allocate import allocate_for_subject, allocate_schedule_for_subject
from aruvi_core.view_model import ViewModel
from aruvi_core.adapters.allocation_repository_file import AllocationRepositoryFileImpl

from . import data, config

app = FastAPI(title="Aruvi API", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# Initialize the allocation repository (file-based for now; Supabase adapter comes later).
allocation_repo = AllocationRepositoryFileImpl(config.DATA_DIR)


class PeriodRow(BaseModel):
    minutes: int
    count: int


class AllocateRequest(BaseModel):
    # Either a multi-row schedule (preferred) or a single total (back-compat).
    period_rows: Optional[List[PeriodRow]] = None
    total_periods: Optional[int] = None
    # Optional subset of chapters to allocate across (teacher deselected some in the UI).
    # None/omitted = allocate across every chapter mapping, as before.
    chapter_numbers: Optional[List[Any]] = None


class SaveAllocationRequest(BaseModel):
    # Subject name (e.g., "science", "mathematics")
    subject: str
    # Grade (as integer, e.g., 7)
    grade: int
    # Dict mapping chapter number (as string) to periods allocated (as int).
    # E.g., {"1": 5, "2": 6, "3": 4}
    allocation: Dict[str, int]


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

    if req.chapter_numbers is not None:
        keep = {str(n) for n in req.chapter_numbers}
        mappings = [m for m in mappings if str(m.get("chapter_number")) in keep]
        if not mappings:
            raise HTTPException(status_code=422, detail="No chapters selected.")

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


@app.post("/subjects/{subject}/{grade}/save_allocation")
def save_allocation(subject: str, grade: str, req: SaveAllocationRequest) -> Dict[str, Any]:
    """Save allocation data to the Persistent Annual Allocation Register.

    Merges the provided allocation into the existing register for the subject/grade.
    Chapters in the allocation overwrite existing allocations; untouched chapters persist.

    Returns the updated Annual Allocation Summary.
    """
    _subject(subject)
    try:
        engine.save_allocation(
            subject_name=subject,
            grade=int(grade),
            chapters_allocation=req.allocation,
            allocation_repo=allocation_repo,
        )
        summary = engine.get_allocation_summary(
            subject_name=subject,
            grade=int(grade),
            allocation_repo=allocation_repo,
        )
        return {
            "subject": subject,
            "grade": grade,
            "status": "saved",
            "summary": {
                "chapters_allocated": summary.chapters_allocated,
                "chapters_remaining": summary.chapters_remaining,
                "total_planned_periods": summary.total_planned_periods,
                "total_planned_time_minutes": summary.total_planned_time_minutes,
            },
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save allocation: {str(e)}")


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
