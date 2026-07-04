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
from aruvi_core.adapters.section_state_repository_file import SectionStateRepositoryFileImpl
from aruvi_core.adapters.plan_archive_repository_file import PlanArchiveRepositoryFileImpl
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

# Per-section teaching-state repository (which chapter a section tracks + how far along +
# done). Bucket-B STATE, so it also writes to STATE_DIR (data/section_state/). Moving this
# off the browser's localStorage is what makes tracking/progress follow a teacher across
# devices (CLOUD_DATA_MODEL.md §2.4). File-based now; Supabase adapter swaps in at Phase 4
# behind the same SectionStateRepository port.
section_state_repo = SectionStateRepositoryFileImpl(config.STATE_DIR)

# Plan-archive repository — which saved plans a teacher has archived from My Lessons (to
# declutter without ever hard-deleting a costly, back-referenced plan). A per-tenant FLAG, not
# a physical move (the plan asset is shared read-only content in DATA_DIR), so it's Bucket-B
# STATE under STATE_DIR (data/plan_archive/). File-based now; a Supabase adapter (an
# `archived_at` column / small `plan_archive` table) swaps in at Phase 4 behind the same
# PlanArchiveRepository port. (Design decision 2026-07-04 — no hard delete anywhere.)
plan_archive_repo = PlanArchiveRepositoryFileImpl(config.STATE_DIR)


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
    # When true, the server cascade-deletes the allocation registers for any subject·grade the
    # edit removed (the teacher saw the named warning and accepted). When false/omitted, a
    # destructive edit is REFUSED with HTTP 409 + the impact list so the UI can warn first.
    # Additive edits (nothing removed) save regardless.
    cascade: bool = False


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


# ── Readiness ↔ allocation slug bridge + cascade ────────────────────────────────
# The readiness profile stores display values (subject "Science", grade "VII"); the
# allocation register is keyed by engine slugs ("science", "vii"). A profile edit that
# removes a subject/grade/section can orphan downstream work (a saved allocation register
# per subject·grade; an in-progress lesson pointer per section). These helpers diff old vs
# new, report the impact, and (on confirm) cascade-delete exactly the removed scope.
def _subject_slug(name: str) -> str:
    return str(name or "").strip().lower().replace(" ", "_")


def _grade_slug(grade: str) -> str:
    return str(grade or "").strip().lower()


def _profile_index(subjects_list: List[Dict[str, Any]]) -> Dict[str, Dict[str, Any]]:
    """Index subjects[] by slug → {grades: {grade_slug: [section_tags]}} for diffing."""
    out: Dict[str, Dict[str, Any]] = {}
    for s in subjects_list or []:
        ss = _subject_slug(s.get("name"))
        if not ss:
            continue
        grades: Dict[str, List[str]] = {}
        for g in s.get("grades", []) or []:
            gs = _grade_slug(g.get("grade"))
            if not gs:
                continue
            grades[gs] = [str((sec or {}).get("tag", "")) for sec in (g.get("sections") or [])]
        out[ss] = {"grades": grades}
    return out


def _diff_profiles(old_subjects: List[Dict[str, Any]],
                   new_subjects: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Compute what an edit REMOVES (old minus new), normalized to slugs.

    {removed_subjects:[{subject, grades:[...]}], removed_grades:[{subject, grade}],
     removed_sections:[{subject, grade, section}]}. removed_grades excludes grades whose
     whole subject was removed (already accounted for)."""
    old, new = _profile_index(old_subjects), _profile_index(new_subjects)
    rem_subj, rem_grade, rem_sec = [], [], []
    for ss, oinfo in old.items():
        if ss not in new:
            rem_subj.append({"subject": ss, "grades": list(oinfo["grades"].keys())})
            continue
        ninfo = new[ss]
        for gs, osecs in oinfo["grades"].items():
            if gs not in ninfo["grades"]:
                rem_grade.append({"subject": ss, "grade": gs})
                continue
            nsecs = set(ninfo["grades"][gs])
            for tag in osecs:
                if tag and tag not in nsecs:
                    rem_sec.append({"subject": ss, "grade": gs, "section": tag})
    return {"removed_subjects": rem_subj, "removed_grades": rem_grade, "removed_sections": rem_sec}


def _cascade_impact(tenant_id: str, user_id: str, diff: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Name the downstream losses for a removal diff, checking which removed scopes actually
    have a saved allocation register. Sections carry no allocation (subject·grade keyed) but
    orphan their LU pointer — flagged so the frontend clears it."""
    impact: List[Dict[str, Any]] = []

    def reg_count(subj: str, grd: str) -> int:
        try:
            return len(engine.get_allocation_register(
                tenant_id=tenant_id, user_id=user_id, subject_name=subj, grade=grd,
                allocation_repo=allocation_repo))
        except Exception:
            return 0

    for r in diff["removed_subjects"]:
        for gs in r["grades"]:
            impact.append({"scope": "subject", "subject": r["subject"], "grade": gs,
                           "chapters_allocated": reg_count(r["subject"], gs)})
    for r in diff["removed_grades"]:
        impact.append({"scope": "grade", "subject": r["subject"], "grade": r["grade"],
                       "chapters_allocated": reg_count(r["subject"], r["grade"])})
    for r in diff["removed_sections"]:
        impact.append({"scope": "section", "subject": r["subject"], "grade": r["grade"],
                       "section": r["section"], "chapters_allocated": 0,
                       "lu_pointer": f"{r['subject']}_{r['grade']}_{r['section']}"})
    return impact


def _apply_cascade(tenant_id: str, user_id: str, diff: Dict[str, Any]) -> None:
    """Clear the allocation register for every removed subject·grade and removed grade.
    Narrow: only the removed scope; siblings untouched. Sections' LU pointers are
    localStorage (frontend-cleared)."""
    for r in diff["removed_subjects"]:
        for gs in r["grades"]:
            engine.clear_allocation_register(tenant_id=tenant_id, user_id=user_id,
                subject_name=r["subject"], grade=gs, allocation_repo=allocation_repo)
    for r in diff["removed_grades"]:
        engine.clear_allocation_register(tenant_id=tenant_id, user_id=user_id,
            subject_name=r["subject"], grade=r["grade"], allocation_repo=allocation_repo)


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
    mappings = data.load_mappings(subject, grade)
    chapters = [
        {"chapter_number": m.get("chapter_number"),
         "chapter_title": m.get("chapter_title", ""),
         "weight": sub.chapter_weight(m)}
        for m in mappings
    ]

    # NCF-suggested estimated teaching periods per chapter (2026-07-01): the NCF period-norms
    # table (data/content/allocation_norms/ncf_period_norms.json) gives a subject·stage total
    # for the year; we distribute that total across this grade's chapters using the exact same
    # effort-index-weighted allocator the Allocate flow uses, so the per-chapter figure is
    # consistent with how periods actually get allocated. Whole periods only (the allocator's
    # largest-remainder method already lands on integers, never fractional periods). None when
    # the norm table has no figure for this subject·stage (e.g. Science·preparatory).
    try:
        stage = stage_for(grade)
    except UnknownGradeError:
        stage = None
    ncf_total = data.ncf_total_periods(subject, stage) if stage else None
    if ncf_total and mappings:
        allocs = {a.chapter_number: a.periods for a in allocate_for_subject(subject, mappings, ncf_total)}
        for c in chapters:
            c["ncf_estimated_periods"] = allocs.get(c["chapter_number"])
    else:
        for c in chapters:
            c["ncf_estimated_periods"] = None

    return {"subject": subject, "grade": grade, "chapters": chapters,
            "allocation_basis": sub.allocation_basis(grade)}


@app.get("/subjects/{subject}/{grade}/ncf-periods")
def get_ncf_periods(subject: str, grade: str) -> Dict[str, Any]:
    """NCF-recommended total teaching periods for the year for this subject·grade.
    Used by the teaching-profile budget 'estimate' option so the recommendation is the
    National Curricular Framework figure, not a flat heuristic. None when the norm table
    has no value for this subject·stage."""
    _subject(subject)
    try:
        stage = stage_for(grade)
    except UnknownGradeError:
        stage = None
    total = data.ncf_total_periods(subject, stage) if stage else None
    return {"subject": subject, "grade": grade, "stage": stage, "ncf_total_periods": total}


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


def _count_units(groups) -> int:
    """Learning Units in a lesson-plan view = periods across (nested) groups — the same
    flatten LessonView.jsx uses. Counted server-side so plan LISTINGS can drive the
    My Classes card progress rail without the client fetching every full view."""
    n = 0
    for g in groups or []:
        n += len(getattr(g, "periods", None) or [])
        n += _count_units(getattr(g, "children", None) or [])
    return n


@app.get("/plans/{subject}/{grade}")
def get_plans(subject: str, grade: str,
              identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    sub = _subject(subject)
    tenant_id, user_id = identity
    plans = data.list_saved_plans(subject, grade)
    # This teacher's archived plan keys for this subject·grade — so each listing carries its
    # OWN archived flag and the client can split the one list into Active vs Archived views
    # (archive is a flag, not a separate location; see PlanArchiveRepository). Keys are the
    # full `${subject}/${grade}/${filename}` the frontend also uses.
    archived = plan_archive_repo.load_all(tenant_id, user_id)
    # Enrich each listing with total_units (LU count) for the section-card rail. Best-effort:
    # a plan that fails to normalize just ships total_units=None and the card skips its rail.
    for p in plans:
        pkey = f"{subject}/{grade}/{p['filename']}"
        p["archived"] = pkey in archived
        p["archived_at"] = archived.get(pkey)
        p["total_units"] = None
        try:
            saved = data.load_saved_plan(subject, grade, p["filename"]) or {}
            r = saved.get("result", {})
            chapter = {"chapter_number": saved.get("chapter_number"),
                       "chapter_title": saved.get("chapter_title")}
            lp = sub.lesson_plan_to_view(r.get("lesson_plan", {}),
                                         grade=saved.get("grade", grade), chapter=chapter)
            p["total_units"] = _count_units(lp.groups)
        except Exception:
            pass
    return {"subject": subject, "grade": grade, "plans": plans}


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
    _lp = r.get("lesson_plan", {})
    link_context = {"periods": _lp.get("periods", []),
                    "handoff": r.get("coverage_handoff", _lp.get("coverage_handoff", []))}
    a = sub.assessment_to_view(r.get("assessment_items", []), grade=g, chapter=chapter,
                               link_context=link_context)
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


@app.post("/readiness/impact")
def preview_readiness_impact(req: ReadinessRequest,
                             identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """Dry-run a profile edit: report what downstream work the proposed subjects[] would
    DELETE, without saving. The sidebar editor calls this before a destructive save so it can
    show a contextual warning. Returns {destructive, impact:[...]}."""
    tenant_id, user_id = identity
    current = readiness_repo.load_profile(tenant_id, user_id) or {}
    diff = _diff_profiles(current.get("subjects", []), req.subjects)
    impact = _cascade_impact(tenant_id, user_id, diff)
    return {"destructive": bool(impact), "impact": impact}


@app.post("/readiness")
def save_readiness(req: ReadinessRequest,
                   identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """Persist the current teacher's readiness teaching profile (full replace, per user).

    Stores only the canonical subjects[]; the projection is stripped by the adapter.
    Cascade guard: if the edit REMOVES a subject/grade/section with downstream state and
    cascade is not set, refuse with HTTP 409 + the impact list so the UI can warn. With
    cascade=true, clear exactly the removed scopes' registers, then save. Additive edits
    save normally."""
    tenant_id, user_id = identity
    current = readiness_repo.load_profile(tenant_id, user_id) or {}
    diff = _diff_profiles(current.get("subjects", []), req.subjects)
    impact = _cascade_impact(tenant_id, user_id, diff)

    if impact and not req.cascade:
        raise HTTPException(status_code=409, detail={
            "error": "destructive_edit",
            "message": "This edit removes classes that have saved work. Confirm to proceed.",
            "impact": impact,
        })

    try:
        if impact:
            _apply_cascade(tenant_id, user_id, diff)
        readiness_repo.save_profile(tenant_id, user_id, {"subjects": req.subjects})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save readiness: {str(e)}")
    saved = readiness_repo.load_profile(tenant_id, user_id)
    return {"status": "saved", "ready": bool(saved and saved.get("subjects")),
            "cascaded": impact if impact else [], "readiness": saved}


@app.delete("/readiness")
def clear_readiness(identity: tuple = Depends(_current_identity)) -> Dict[str, str]:
    """Erase the current teacher's readiness profile (the "start setup over" action)."""
    tenant_id, user_id = identity
    readiness_repo.clear_profile(tenant_id, user_id)
    return {"status": "cleared"}


# ── Section teaching-state (the lesson pointer) — per-user, cross-device ──────────
# Which chapter each section tracks + how far along (unit_index) + done. Moved off the
# browser's localStorage so tracking/progress follow a teacher to any device
# (CLOUD_DATA_MODEL.md §2.4). localStorage remains a client optimistic cache; these rows
# are authoritative on load/reconcile.
class SectionStateRequest(BaseModel):
    """Body for POST /section-state — a full snapshot of ONE section's execution state."""
    section_key: str
    chapter: str
    unit_index: Optional[int] = None
    done: bool = False


@app.get("/section-state")
def get_section_state(identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """All of this teacher's tracked sections: {"states": {section_key: {chapter,
    unit_index, done, updated_at}}}. The app reconciles these into its localStorage cache on
    load, so a fresh device shows the same tracking/progress the teacher set on another."""
    tenant_id, user_id = identity
    return {"states": section_state_repo.load_all(tenant_id, user_id)}


@app.post("/section-state")
def save_section_state(req: SectionStateRequest,
                       identity: tuple = Depends(_current_identity)) -> Dict[str, str]:
    """Upsert one section's teaching state (full snapshot). Called when a chapter is tracked,
    the pointer advances, or a chapter is marked complete."""
    tenant_id, user_id = identity
    try:
        section_state_repo.save_one(tenant_id, user_id, req.section_key,
                                    req.chapter, req.unit_index, req.done)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save section state: {str(e)}")
    return {"status": "saved"}


@app.delete("/section-state/{section_key}")
def clear_section_state(section_key: str,
                        identity: tuple = Depends(_current_identity)) -> Dict[str, str]:
    """Remove one section's state — the untrack reversal (and the completed-chapter reset)."""
    tenant_id, user_id = identity
    section_state_repo.delete_one(tenant_id, user_id, section_key)
    return {"status": "cleared"}


class PlanArchiveRequest(BaseModel):
    # The plan identity as the frontend keys it: subject slug, grade slug, saved-plan filename.
    subject: str
    grade: str
    filename: str


def _plan_key(subject: str, grade: str, filename: str) -> str:
    """Canonical archive key for a plan. Guards against path-ish junk in the filename so a
    stored key can never smuggle a traversal into a later lookup."""
    if "/" in filename or "\\" in filename or ".." in filename:
        raise HTTPException(status_code=400, detail="Invalid plan filename.")
    return f"{subject}/{grade}/{filename}"


@app.get("/plan-archive")
def get_plan_archive(identity: tuple = Depends(_current_identity)) -> Dict[str, Any]:
    """All of this teacher's archived plan keys: {"archived": {plan_key: archived_at_iso}}.
    The client uses this to render the Archived view (and could split Active/Archived without
    re-reading each /plans call)."""
    tenant_id, user_id = identity
    return {"archived": plan_archive_repo.load_all(tenant_id, user_id)}


@app.post("/plan-archive")
def archive_plan(req: PlanArchiveRequest,
                 identity: tuple = Depends(_current_identity)) -> Dict[str, str]:
    """Archive one plan (declutter without deleting). The UI blocks this for a plan any section
    is actively teaching; the server simply records the flag. Idempotent."""
    tenant_id, user_id = identity
    key = _plan_key(req.subject, req.grade, req.filename)
    try:
        plan_archive_repo.archive(tenant_id, user_id, key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to archive plan: {str(e)}")
    return {"status": "archived"}


@app.delete("/plan-archive")
def restore_plan(req: PlanArchiveRequest,
                 identity: tuple = Depends(_current_identity)) -> Dict[str, str]:
    """Restore one archived plan back into My Lessons. Lossless — the plan's identity and all
    its back-references never moved. No-op if it wasn't archived."""
    tenant_id, user_id = identity
    key = _plan_key(req.subject, req.grade, req.filename)
    try:
        plan_archive_repo.restore(tenant_id, user_id, key)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to restore plan: {str(e)}")
    return {"status": "restored"}


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
