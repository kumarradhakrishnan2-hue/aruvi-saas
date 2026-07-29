"""Test-campaign tracker state — docs/testing.md §6a.

Persists the 25-combo certification campaign's tick-offs, comments, provenance
records and defect register INSIDE Aruvi itself (Bucket-B-style state under
STATE_DIR/testing/), so the tracker UI (docs/testing_tracker.html, also served at
GET /api/testing/tracker) survives restarts and both actors see one register.

Deliberately schema-light: the UI owns the checklist DEFINITIONS (which steps
exist); this store holds only what was recorded against them, keyed by
scope → key → step. Campaign-tooling only — no teacher-facing surface, no LLM,
no tenancy (the campaign register is shared by design between the two actors).
"""
from __future__ import annotations

import json
import os
import threading
from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse, PlainTextResponse
from pydantic import BaseModel

from .config import STATE_DIR

router = APIRouter(prefix="/api/testing", tags=["testing-campaign"])

_LOCK = threading.Lock()
_SCOPES = ("step0", "stages", "combos", "cross")


def _state_path() -> str:
    return os.path.join(STATE_DIR, "testing", "campaign_state.json")


def _default_state() -> Dict[str, Any]:
    return {
        "version": 1,
        "campaign": "aruvi-25-combo-certification",
        "updated_at": None,
        # scope → key → step → {status, comment, by, at, ...extras (e.g. provenance)}
        "step0": {},     # key "campaign" → {"0.1": {...}}
        "stages": {},    # key "english/preparatory" → {"P1": {...}}
        "combos": {},    # key "english/iii" → {"C1": {...}, "provenance": {...}}
        "cross": {},     # key "campaign" → {"X1": {...}}
        "defects": [],   # [{id, combo, step, severity, title, evidence, owner, status, opened, closed, notes}]
    }


def _load() -> Dict[str, Any]:
    p = _state_path()
    if not os.path.isfile(p):
        return _default_state()
    try:
        with open(p, encoding="utf-8") as f:
            state = json.load(f)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Campaign state unreadable: {e}")
    base = _default_state()
    base.update(state if isinstance(state, dict) else {})
    return base


def _save(state: Dict[str, Any]) -> None:
    """Atomic write (tmp + rename) so a crash mid-write never corrupts the register."""
    state["updated_at"] = datetime.now().isoformat(timespec="seconds")
    p = _state_path()
    os.makedirs(os.path.dirname(p), exist_ok=True)
    tmp = p + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
    os.replace(tmp, p)


@router.get("/campaign")
def get_campaign() -> Dict[str, Any]:
    """The whole campaign state. The tracker UI loads this on open."""
    with _LOCK:
        return _load()


class FullState(BaseModel):
    state: Dict[str, Any]


@router.put("/campaign")
def put_campaign(req: FullState) -> Dict[str, Any]:
    """Full replace — the tracker's 'restore from export' path. Item-level writes
    should prefer POST /campaign/item, which cannot clobber concurrent edits."""
    with _LOCK:
        base = _default_state()
        base.update(req.state or {})
        _save(base)
        return {"status": "saved", "updated_at": base["updated_at"]}


class ItemPatch(BaseModel):
    """One recorded observation against one checklist step.

    scope: step0 | stages | combos | cross
    key:   "campaign" for step0/cross; "english/preparatory" for stages;
           "english/iii" for combos
    step:  "0.1" | "P1".."P4" | "SIGN" | "C1".."C13" | "X1".."X3" | "provenance"
    patch: merged into the stored item (status / comment / by / any extra fields;
           set a field to null to delete it). `at` is stamped server-side.
    """
    scope: str
    key: str
    step: str
    patch: Dict[str, Any] = {}


@router.post("/campaign/item")
def post_item(req: ItemPatch) -> Dict[str, Any]:
    if req.scope not in _SCOPES:
        raise HTTPException(status_code=400, detail=f"Unknown scope: {req.scope}")
    if not req.key or not req.step:
        raise HTTPException(status_code=400, detail="key and step are required.")
    with _LOCK:
        state = _load()
        bucket = state[req.scope].setdefault(req.key, {})
        item = bucket.setdefault(req.step, {})
        for k, v in (req.patch or {}).items():
            if v is None:
                item.pop(k, None)
            else:
                item[k] = v
        item["at"] = datetime.now().isoformat(timespec="seconds")
        _save(state)
        return {"status": "saved", "item": item, "updated_at": state["updated_at"]}


class DefectUpsert(BaseModel):
    """Upsert one defect-register row by id; omit id to open a new ARV-D-NNN."""
    id: Optional[str] = None
    combo: str = ""            # "english/iii", "stage:science/middle", or "campaign"
    step: str = ""             # "C7", "P2", "X1", "0.1", ...
    severity: str = "S3"       # S1..S4 per docs/testing.md §7
    title: str = ""
    evidence: str = ""
    owner: str = ""
    status: str = "open"       # open | fixing | fixed-awaiting-recheck | closed | accepted
    notes: str = ""
    delete: bool = False       # true → remove the row (mis-filed only; prefer status)


@router.post("/campaign/defect")
def post_defect(req: DefectUpsert) -> Dict[str, Any]:
    if req.severity not in ("S1", "S2", "S3", "S4"):
        raise HTTPException(status_code=400, detail=f"Unknown severity: {req.severity}")
    with _LOCK:
        state = _load()
        defects: List[Dict[str, Any]] = state.setdefault("defects", [])
        now = datetime.now().isoformat(timespec="seconds")
        if req.delete:
            if not req.id:
                raise HTTPException(status_code=400, detail="delete needs an id.")
            state["defects"] = [d for d in defects if d.get("id") != req.id]
            _save(state)
            return {"status": "deleted", "id": req.id}
        did = req.id
        if not did:
            n = 1 + max((int(str(d.get("id", "ARV-D-0")).rsplit("-", 1)[-1] or 0)
                         for d in defects if str(d.get("id", "")).startswith("ARV-D-")),
                        default=0)
            did = f"ARV-D-{n:03d}"
        row = next((d for d in defects if d.get("id") == did), None)
        if row is None:
            row = {"id": did, "opened": now, "closed": None}
            defects.append(row)
        row.update({"combo": req.combo, "step": req.step, "severity": req.severity,
                    "title": req.title, "evidence": req.evidence, "owner": req.owner,
                    "status": req.status, "notes": req.notes, "at": now})
        if req.status in ("closed", "accepted") and not row.get("closed"):
            row["closed"] = now
        if req.status not in ("closed", "accepted"):
            row["closed"] = None
        _save(state)
        return {"status": "saved", "defect": row}


def _csv_cell(v: Any) -> str:
    s = "" if v is None else str(v)
    return '"' + s.replace('"', '""') + '"'


@router.get("/campaign/export.csv")
def export_csv() -> PlainTextResponse:
    """Everything recorded, flat — one row per (scope, key, step) plus one per defect —
    for gathering comments later without walking the JSON."""
    with _LOCK:
        state = _load()
    rows = ["kind,id,scope,key,step,status,severity,by_or_owner,at,title,comment,evidence,notes"]
    for scope in _SCOPES:
        for key, steps in (state.get(scope) or {}).items():
            for step, item in (steps or {}).items():
                if step == "provenance":
                    comment = json.dumps(item, ensure_ascii=False)
                    rows.append(",".join(_csv_cell(v) for v in [
                        "provenance", "", scope, key, step, "", "", item.get("by", ""),
                        item.get("at", ""), "", comment, "", ""]))
                    continue
                rows.append(",".join(_csv_cell(v) for v in [
                    "item", "", scope, key, step, item.get("status", ""), "",
                    item.get("by", ""), item.get("at", ""), "",
                    item.get("comment", ""), item.get("evidence", ""), ""]))
    for d in state.get("defects") or []:
        rows.append(",".join(_csv_cell(v) for v in [
            "defect", d.get("id", ""), "", d.get("combo", ""), d.get("step", ""),
            d.get("status", ""), d.get("severity", ""), d.get("owner", ""),
            d.get("at", ""), d.get("title", ""), "", d.get("evidence", ""),
            d.get("notes", "")]))
    return PlainTextResponse("\n".join(rows) + "\n", media_type="text/csv")


@router.get("/tracker")
def tracker_page() -> HTMLResponse:
    """Serve the tracker UI from docs/ so it shares the API's origin (no CORS or
    file:// wrinkles; the page also works opened directly, CORS is open)."""
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(repo_root, "docs", "testing_tracker.html")
    if not os.path.isfile(p):
        raise HTTPException(status_code=404, detail="docs/testing_tracker.html not found.")
    with open(p, encoding="utf-8") as f:
        return HTMLResponse(f.read())
