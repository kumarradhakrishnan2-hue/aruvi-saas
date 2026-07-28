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


# ── the calibrated standard: durations + per-chapter recommendations ────────────
# Founder decision 2026-07-26. Two different tables were being conflated:
#
#   ncf_period_norms.json   — the NCF adaptation. Annual totals by subject·STAGE,
#                             expressed in a flat 40-minute period (see its _meta.unit).
#   master_plan.json        — OUR calibrated standard. Annual budgets by subject·CLASS
#                             from the founder's workbook, spread per chapter by effort
#                             weight, at class-banded standard durations (40 ≤VII / 45
#                             VIII / 50 IX — genon/master_plan.py's std_duration, the
#                             same bands the certified canonicals were authored at,
#                             e.g. SS IX ch 5 = 21×50).
#
# The two disagree, sometimes badly (SS IX: 245 calibrated periods vs 150 NCF; TWAU
# preparatory the other way, 140 vs 300). Everything a teacher sees as a DEFAULT now
# reads the master plan first and falls back to the NCF norms only where the master
# plan has no row for that subject·class. The NCF figure is still surfaced alongside
# on the budget screen — it is a published norm, not a bug — but it no longer drives
# any default.

# Class X has no master-plan row yet (no chapter weights in the workbook), but it sits
# in the same secondary band as IX, so the DURATION band extends to it. Period counts
# for X still fall back to the NCF norms until the workbook carries its chapters.
_STANDARD_DURATION_BY_CLASS = {"III": 40, "IV": 40, "V": 40, "VI": 40, "VII": 40,
                               "VIII": 45, "IX": 50, "X": 50}
FALLBACK_STANDARD_DURATION = 40   # unknown grade → the NCF flat period


def standard_duration_minutes(grade: str, subject: Optional[str] = None) -> int:
    """The calibrated standard class duration in minutes for this grade. Prefers the
    master plan's own `standard_duration_minutes` for the subject·class (so the file
    stays authoritative if a band ever moves), else the class band, else 40."""
    if subject:
        combo = master_combo(subject, grade)
        if combo and combo.get("standard_duration_minutes"):
            return int(combo["standard_duration_minutes"])
    roman = _ROMAN_BY_SLUG.get((grade or "").lower())
    return _STANDARD_DURATION_BY_CLASS.get(roman, FALLBACK_STANDARD_DURATION)


def master_annual_budget(subject: str, grade: str) -> Optional[int]:
    """The calibrated annual period budget for this subject·class, or None when the
    master plan has no row for it."""
    combo = master_combo(subject, grade)
    v = (combo or {}).get("annual_budget_periods")
    return int(v) if v is not None else None


def master_recommended_periods(subject: str, grade: str) -> Dict[Any, int]:
    """{chapter_number: recommended_periods} from the master plan — the calibrated
    per-chapter figure (its share of the annual budget by effort weight, largest
    remainder). Empty dict when there is no row for this subject·class."""
    combo = master_combo(subject, grade)
    out: Dict[Any, int] = {}
    for row in (combo or {}).get("chapters", []) or []:
        n, p = row.get("chapter"), row.get("recommended_periods")
        if n is not None and p is not None:
            out[n] = int(p)
    return out


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


def append_token_log(call_type: str, subject: str, grade: str, chapter_number,
                     chapter_title: str, input_tokens: int, output_tokens: int,
                     cost_inr: float) -> None:
    """Append a paid-run row to the founder's unified cost notebook —
    THIS repo's runtime_data/token_log.csv (fresh log started 2026-07-25, seeded
    with the first ch 5 canonical run; the pre-genon prototype history is archived
    alongside as token_log_old.csv). BEST-EFFORT ONLY: any error is swallowed —
    serving the teacher never waits on bookkeeping."""
    try:
        import csv
        from datetime import datetime
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        path = os.environ.get("ARUVI_TOKEN_LOG") or os.path.join(
            repo_root, "runtime_data", "token_log.csv")
        if not os.path.isfile(path):
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", newline="", encoding="utf-8") as f:
                f.write("timestamp,call_type,subject,grade,chapter_number,chapter_title,"
                        "input_tokens,output_tokens,total_tokens,cost_inr,"
                        "cache_write_input_tokens,cache_read_input_tokens\n")
        with open(path, "a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([
                datetime.now().isoformat(timespec="seconds"), call_type, subject, grade,
                chapter_number, chapter_title, input_tokens, output_tokens,
                int(input_tokens) + int(output_tokens), round(float(cost_inr), 4), 0, 0,
            ])
    except Exception:
        pass


def canonical_mtime(subject: str, grade: str, chapter_number: int) -> Optional[float]:
    p = _canonical_path(subject, grade, chapter_number)
    return os.path.getmtime(p) if os.path.isfile(p) else None


# ── deterministic plan keys (founder decision 2026-07-26) ───────────────────────
# An adapted plan is a CACHE ENTRY, not an event: its filename is derived from what
# actually determines its bytes — chapter, duration matrix, canonical version, engine
# version, and whether the seam polish was applied. Same request from any teacher ->
# same key -> the entry is served, not regenerated (partition is free; the polish
# tokens are the spend the cache saves). Per-teacher visibility stays where it
# belongs: the prepared-plans register (CLOUD_DATA_MODEL §2.3, reference-not-copy).
# This is the on-disk stand-in for the Bucket-A output cache in §1, so the Supabase
# migration is a storage swap, not a redesign.

GENON_ENGINE_VERSION = "04"     # BUMP when compile/partition/polish change the OUTPUT
# 04 (2026-07-28): container text is SELECTED from the canonical's Rule-16 unit_handoff
# instead of composed at partition time. Titles and teacher notes change for every period
# that spans a unit boundary, so every pre-existing e03 key is stale by construction —
# the bump is what stops a teacher being served yesterday's mechanical join from cache.


def norm_matrix(matrix) -> str:
    """Duration matrix -> canonical string. Rows are aggregated by duration and sorted
    longest-first, so 17x50 and 10x50+7x50 yield the SAME key — a teacher must not miss
    her own cache entry because of how she typed the rows."""
    agg: Dict[int, int] = {}
    for d_, c_ in matrix:
        d_, c_ = int(d_), int(c_)
        if d_ > 0 and c_ > 0:
            agg[d_] = agg.get(d_, 0) + c_
    return "-".join(f"{d}m{agg[d]}" for d in sorted(agg, reverse=True))


def canonical_version(canonical: Dict[str, Any]) -> str:
    """Short stable id for the canonical a plan derives from: its ledger timestamp when
    the generator stamped one, else a content hash. Regenerating the canonical therefore
    produces a NEW key — a teacher mid-chapter never has her plan rewritten underneath
    her; the new plan is a new entry, offered, not substituted."""
    gc = canonical.get("genon_canonical") or {}
    ts = "".join(ch for ch in str(gc.get("ledger_ts") or "") if ch.isalnum())
    if ts:
        # ledger_ts identifies the GENERATION RUN. A companion table amended afterwards
        # (a Rule-16 back-fill onto a pre-v1.3 canonical) changes the bytes a partition
        # produces without changing the run, so it needs its own revision in the key —
        # otherwise the amended canonical is served from a cache entry cut before it.
        # Canonicals generated under v1.3 emit unit_handoff in the run itself and carry
        # no handoff_rev, so their keys stay clean.
        rev = "".join(ch for ch in str(gc.get("handoff_rev") or "") if ch.isalnum())
        return f"{ts}h{rev}" if rev else ts
    import hashlib
    blob = json.dumps(canonical.get("result"), ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha1(blob).hexdigest()[:12]


def genon_plan_filename(chapter_number, matrix, canonical: Dict[str, Any],
                        polished: bool) -> str:
    """e.g. ch_05_50m16_e04_c20260726112240.json  (16 x 50 min, engine v0.4,
    that canonical run). Never collides with ch_NN_canonical.json."""
    return (f"ch_{int(chapter_number):02d}_{norm_matrix(matrix)}"
            f"_e{GENON_ENGINE_VERSION}_c{canonical_version(canonical)}"
            f"{'_p' if polished else ''}.json")


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


def save_generated_plan(subject: str, grade: str, plan: Dict[str, Any],
                       filename: Optional[str] = None) -> str:
    """Persist a genon-adapted plan into the saved-plans library; returns the filename.

    Adapted plans join the same library the viewer/exporters read; per-teacher
    visibility comes from the prepared-plans register, not from where the file sits.

    `filename` is the deterministic key (genon_plan_filename) — the same request
    rewrites the same entry rather than accumulating near-identical copies. Without
    one, the legacy timestamp naming applies.
    """
    from datetime import datetime
    d = os.path.join(DATA_DIR, "saved_plans", subject, grade)
    os.makedirs(d, exist_ok=True)
    if not filename:
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
