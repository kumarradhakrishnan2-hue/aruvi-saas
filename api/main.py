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

from fastapi import Depends, FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
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
from aruvi_core.adapters.readiness_repository_file import ReadinessRepositoryFileImpl
from aruvi_core.grades import stage_for, UnknownGradeError
from aruvi_core.report_competency import build_report as build_competency_report
# NOTE: the PDF/DOCX exporters are imported lazily inside their endpoints (not here)
# so a missing optional dependency (weasyprint, python-docx) can never break API
# startup — only the export endpoints would error, with a clear message.

from . import data, config

app = FastAPI(title="Aruvi API", version="0.1.0")
app.add_middleware(
    CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"],
)

# Initialize the allocation repository. The allocation register is per-user/tenant STATE
# (Bucket B), so it writes to STATE_DIR (aruvi-saas/data/allocations/) — NOT the read-only
# content dir. (Previously it wrote into the prototype content mirror; moved here so all
# user data lives under data/.) File-based now; Supabase adapter swaps in behind the same
# AllocationRepository port at Phase 4.
allocation_repo = AllocationRepositoryFileImpl(config.STATE_DIR)

# Initialize the readiness teaching-profile repository. This is per-user/tenant STATE
# (Bucket B), so it writes to STATE_DIR (aruvi-saas/data/) — NOT the read-only content
# mirror in DATA_DIR. File-based for now; the Supabase adapter swaps in at Phase 4 behind
# the same ReadinessRepository port, replacing this folder. (See CLOUD_DATA_MODEL.md §0/§2.)
readiness_repo = ReadinessRepositoryFileImpl(config.STATE_DIR)


# Identity. No password stage yet: the caller's user ID arrives in the X-Aruvi-User
# request header (set by the login portal, sent on every API call). Each user ID is its
# own individual-teacher tenant, so tenant_id == user_id (matches the ICP "individual
# teacher = a tenant with one user", CLOUD_DATA_MODEL.md §3). Phase 4 replaces the header
# read with the (tenant_id, user_id) decoded from the Supabase auth token via the
# AuthProvider port — this one function is the only thing that changes.
#
# Falls back to "local" when no header is present (e.g. health checks, curl) so nothing
# 500s; a real teacher always has one because the frontend gates the app behind login.
def _current_identity(x_aruvi_user: Optional[str] = Header(default=None)) -> tuple[str, str]:
    """Return (tenant_id, user_id) for the caller, from the X-Aruvi-User header."""
    uid = (x_aruvi_user or "").strip() or "local"
    return (uid, uid)


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
    # Grade as the roman-numeral string used everywhere else in the API ("vii"), not an
    # integer — stage_for()/grades.py and the /chapters and /allocate endpoints all key
    # off this same roman string. (req.subject/req.grade are echoed back only; the path
    # params {subject}/{grade} are what's actually used to read/write the register.)
    grade: str
    # Dict mapping chapter number (as string) to a full allocation record:
    # {chapter_title, weight, periods_by_duration: {minutes_str: count}, total_periods,
    # total_minutes}. The full record (not just a period total) is stored so the saved
    # register is "redraw-ready" for the frontend's final-allocation table.
    allocation: Dict[str, Dict[str, Any]]


class ReadinessRequest(BaseModel):
    """Body for POST /readiness — the teacher's readiness teaching profile.

    Only `subjects` (the canonical self-contained per-subject array emitted by
    Readiness.jsx) is persisted. The frontend may also send the denormalized
    active-subject projection (subject/grades/grids/durations/budget); it is ignored
    here and stripped by the adapter — see CLOUD_DATA_MODEL.md §2.1.
    """
    subjects: List[Dict[str, Any]] = []


class AllocationReportRequest(BaseModel):
    """Request body for the allocation-report export endpoints.

    The frontend sends the allocation result only; the API enriches each chapter
    with its competencies (code + description + justification) from the mappings
    and the framework glossary, server-side. `grade` is the roman string ("vii").
    `period_types` is [{minutes, count}]. `chapters` is the allocate output:
    [{chapter_number, chapter_title, periods_by_duration {min:count}, total_periods,
      total_minutes, weight}].
    """
    subject: str
    grade: str
    generated_at: Optional[str] = None
    notes: Optional[str] = None
    period_types: List[Dict[str, Any]] = []
    chapters: List[Dict[str, Any]] = []


def _subject(name: str):
    try:
        return subjects.get(name)
    except Exception:
        raise HTTPException(status_code=404, detail=f"Unknown subject: {name}")


@app.get("/health")
def health() -> Dict[str, str]:
    # `report` marker bumps when the report code changes — lets you confirm the
    # server is running the latest code (curl localhost:8000/health).
    return {"status": "ok", "report": "competency-v6-rules"}


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


@app.get("/subjects/{subject}/{grade}/allocation")
def get_allocation(subject: str, grade: str,
                   identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """Load this teacher's Persistent Annual Allocation Register for a subject/grade.

    Scoped to X-Aruvi-User: two teachers' registers for the same subject·grade are
    independent. Returns the full saved register so the frontend can rehydrate its
    final-allocation view on page load — surviving a server restart or a fresh
    browser/profile, not just a localStorage cache in the same browser.
    """
    _subject(subject)
    tenant_id, user_id = identity
    register = engine.get_allocation_register(
        tenant_id=tenant_id,
        user_id=user_id,
        subject_name=subject,
        grade=grade,
        allocation_repo=allocation_repo,
    )
    return {"subject": subject, "grade": grade, "allocation": register}


@app.post("/subjects/{subject}/{grade}/save_allocation")
def save_allocation(subject: str, grade: str, req: SaveAllocationRequest,
                    identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """Save allocation data to this teacher's Persistent Annual Allocation Register.

    Merges the provided allocation into the existing register for the subject/grade,
    scoped to X-Aruvi-User. Chapters in the allocation overwrite existing allocations;
    untouched chapters persist.

    Returns the updated Annual Allocation Summary.
    """
    _subject(subject)
    tenant_id, user_id = identity
    try:
        engine.save_allocation(
            tenant_id=tenant_id,
            user_id=user_id,
            subject_name=subject,
            grade=grade,
            chapters_allocation=req.allocation,
            allocation_repo=allocation_repo,
        )
        summary = engine.get_allocation_summary(
            tenant_id=tenant_id,
            user_id=user_id,
            subject_name=subject,
            grade=grade,
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


@app.delete("/subjects/{subject}/{grade}/allocation")
def delete_allocation(subject: str, grade: str,
                      identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """Erase this teacher's saved Annual Allocation Register for a subject/grade — the
    server-side half of the "Reset allocations" action (the frontend also clears its
    localStorage cache). Scoped to X-Aruvi-User."""
    _subject(subject)
    tenant_id, user_id = identity
    engine.clear_allocation_register(
        tenant_id=tenant_id,
        user_id=user_id,
        subject_name=subject,
        grade=grade,
        allocation_repo=allocation_repo,
    )
    return {"subject": subject, "grade": grade, "status": "cleared"}


@app.get("/readiness")
def get_readiness(identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """Load the current teacher's readiness teaching profile (per X-Aruvi-User).

    Returns {"ready": bool, "readiness": {subjects:[...]} | None}. `ready` is derived
    server-side as "a saved profile with at least one subject exists" — the frontend's
    old front-end-only `ready` flag now rehydrates from here, so the subject/grades/
    sections/durations a teacher entered survive a refresh, a server restart, or a fresh
    browser. Phase 4 keys this per user/tenant from the auth token (CLOUD_DATA_MODEL §2.1).
    """
    tenant_id, user_id = identity
    profile = readiness_repo.load_profile(tenant_id, user_id)
    ready = bool(profile and profile.get("subjects"))
    return {"ready": ready, "readiness": profile}


@app.post("/readiness")
def save_readiness(req: ReadinessRequest,
                   identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """Persist the current teacher's readiness teaching profile (full replace, per user).

    Stores only the canonical subjects[]; the denormalized projection is stripped by
    the adapter. Called by the shell on Readiness onComplete so the setup is never lost.
    """
    tenant_id, user_id = identity
    try:
        readiness_repo.save_profile(tenant_id, user_id, {"subjects": req.subjects})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save readiness: {str(e)}")
    saved = readiness_repo.load_profile(tenant_id, user_id)
    return {"status": "saved", "ready": bool(saved and saved.get("subjects")),
            "readiness": saved}


@app.delete("/readiness")
def clear_readiness(identity: tuple = Depends(_current_identity)) -> Dict[str, str]:
    """Erase the current teacher's readiness profile (the "start setup over" action)."""
    tenant_id, user_id = identity
    readiness_repo.clear_profile(tenant_id, user_id)
    return {"status": "cleared"}


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


def _safe_name(s: str) -> str:
    """Filename-safe slug for the Content-Disposition header."""
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in str(s)).strip("-").lower()


def _build_report(req: "AllocationReportRequest"):
    """Assemble the full per-chapter competency report from the request + server data.

    The request carries only the allocation (periods per chapter); competencies and
    their descriptions/justifications are loaded here from the mappings and the
    framework glossary so the frontend never has to ship them.
    """
    from datetime import datetime
    _subject(req.subject)  # 404 on unknown subject
    try:
        stage = stage_for(req.grade)
    except UnknownGradeError:
        raise HTTPException(status_code=422, detail=f"Unknown grade: {req.grade}")

    mappings = data.load_mappings(req.subject, req.grade)
    mappings_by_chapter = {int(m.get("chapter_number")): m for m in mappings
                           if m.get("chapter_number") is not None}
    descriptions = data.load_competency_descriptions(req.subject, req.grade)

    generated_at = datetime.now()
    if req.generated_at:
        try:
            generated_at = datetime.fromisoformat(req.generated_at)
        except ValueError:
            pass

    return build_competency_report(
        subject=req.subject,
        grade=req.grade,
        stage=stage,
        period_types=req.period_types,
        chapters_alloc=req.chapters,
        mappings_by_chapter=mappings_by_chapter,
        descriptions=descriptions,
        generated_at=generated_at,
        notes=req.notes,
    )


@app.post("/api/allocation/export-pdf")
def export_allocation_pdf(req: AllocationReportRequest) -> StreamingResponse:
    """Export the allocation report as a PDF binary."""
    try:
        from aruvi_core.export_allocation_pdf import export_allocation_report_pdf
        pdf_bytes = export_allocation_report_pdf(_build_report(req))
        fname = f"allocation-report-grade-{req.grade}-{_safe_name(req.subject)}.pdf"
        return StreamingResponse(
            iter([pdf_bytes]),
            media_type="application/pdf",
            headers={"Content-Disposition": f'attachment; filename="{fname}"'},
        )
    except HTTPException:
        raise  # let 404/422 from _build_report pass through unchanged
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print("\n[export-pdf] FAILED:\n" + tb, flush=True)  # full traceback to server console
        last = tb.strip().splitlines()
        where = next((l.strip() for l in reversed(last) if "aruvi" in l or "api/" in l), "")
        raise HTTPException(status_code=500, detail=f"PDF export failed: {e}  [{where}]")


@app.post("/api/allocation/export-docx")
def export_allocation_docx(req: AllocationReportRequest) -> StreamingResponse:
    """Export the allocation report as a DOCX (Word) binary."""
    try:
        from aruvi_core.export_allocation_docx import export_allocation_report_docx
        docx_bytes = export_allocation_report_docx(_build_report(req))
        fname = f"allocation-report-grade-{req.grade}-{_safe_name(req.subject)}.docx"
        return StreamingResponse(
            iter([docx_bytes]),
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
            headers={"Content-Disposition": f'attachment; filename="{fname}"'},
        )
    except HTTPException:
        raise  # let 404/422 from _build_report pass through unchanged
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        print("\n[export-docx] FAILED:\n" + tb, flush=True)
        last = tb.strip().splitlines()
        where = next((l.strip() for l in reversed(last) if "aruvi" in l or "api/" in l), "")
        raise HTTPException(status_code=500, detail=f"DOCX export failed: {e}  [{where}]")
