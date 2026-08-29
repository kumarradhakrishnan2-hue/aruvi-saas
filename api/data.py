"""Content access for the runtime — the certified lesson library, chapter mappings,
framework glossaries, allocation norms, the master plan.

★ EVERY READ HERE GOES THROUGH THE STORAGE PORT (2026-08-29). It did not used to.
This module read the content tree directly with open()/os.listdir/os.path.isdir —
about twenty call sites — which made Storage the one declared-and-bypassed seam in
ports.py, and the one provider a partner could not swap by writing a single adapter.
Nothing was broken by it; a filesystem is a fine content store for one machine. But
the object-store migration was a refactor disguised as a config change, and this
module is where the disguise lived.

THE RULE, now that it holds: no os.path, no open(), no os.listdir against DATA_DIR
below this line. A path is a KEY — a '/'-joined string relative to the content root —
and aruvi_core/adapters/storage_file.py is the only code allowed to turn one into a
filesystem path. Adding a read means adding a port call, never a convenient open().

THE ONE DELIBERATE EXCEPTION is append_token_log, and its own docstring says why:
it appends a row to the founder's cost notebook under runtime_data/, which is not
Bucket A content, is not read by the runtime, and cannot be appended to in an object
store anyway. It stays on local disk on purpose.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from aruvi_core.adapters.storage_file import LocalStorage

from .config import DATA_DIR, LP_YEAR

# The content store. Constructed here rather than injected because this module IS the
# content-access layer — api/main.py's provider block re-exports it as `storage` so the
# seam is visible where every other provider is chosen, and a swap is one line there
# plus this default. A caller wanting a different store passes it to set_storage().
#
# ★ IT FOLLOWS `DATA_DIR`, AND THAT IS NOT A CONVENIENCE. Half a dozen tests redirect
# the content root by rebinding `data.DATA_DIR` to a tmpdir mid-run — the established
# idiom in this repo — and a store built once at import would keep serving the real
# library while the test wrote into the tmpdir. `_st()` rebuilds when the root moves,
# so that idiom keeps working unchanged.
#
# ★ AND IT CLEARS THE CACHES WHEN IT REBUILDS, which is load-bearing in a way the old
# code never had to think about: cache keys used to be ABSOLUTE paths, so two roots
# could not collide. Keys are now root-RELATIVE, so "saved_plans/x/y/ch_01.json" names a
# different object under a tmpdir than under the real content tree. Without the clear, a
# redirect would be served a stale stream compiled from the other root.
_storage = LocalStorage(DATA_DIR)
_storage_root = DATA_DIR
_storage_explicit = False


def _st():
    """The live content store, rebuilt if DATA_DIR has been rebound since."""
    global _storage, _storage_root
    if not _storage_explicit and _storage_root != DATA_DIR:
        _storage = LocalStorage(DATA_DIR)
        _storage_root = DATA_DIR
        _clear_content_caches()
    return _storage


def _clear_content_caches() -> None:
    global _master_plan_cache, _ncf_norms_cache
    _stream_cache.clear()
    _master_plan_cache = None
    _ncf_norms_cache = None


def set_storage(store) -> None:
    """Swap the content store. The object-store cutover calls this once, at startup,
    from api/main.py's provider block — after which nothing else in the product knows
    or cares where the library lives. Also what lets a test run the engine against a
    fake with no filesystem at all.

    An explicitly-set store PINS: it is never replaced by the DATA_DIR-follow above,
    because a caller who named a store means it, and silently swapping it back to a
    local one on the next config change would be the worst kind of surprise."""
    global _storage, _storage_explicit
    _storage = store
    _storage_explicit = True
    _clear_content_caches()


def storage():
    """The live content store, for the few readers outside this module."""
    return _st()


# ── The lesson-plan library, foldered by EDITION YEAR (§2.2, 2026-08-27) ────────
# saved_plans/{subject}/{grade}/{lp_year}/ch_NN_*.json
#
# Read config.LP_YEAR's comment first — it says which of Aruvi's two "years" this is
# (the LIBRARY's edition, Bucket A) and why the year is a label and never a cache key.
#
# ONE function puts the year in the path. Every other reader in this file goes through
# it, so an edition bump is a config change, not a search-and-replace across eight call
# sites — which is what the flat layout had become by the time it held 961 files.

def lp_library_prefix(subject: str, grade: str, year: Optional[str] = None) -> str:
    """The KEY PREFIX holding one subject·grade's plan library for one edition year.

    Falls back to the LEGACY FLAT prefix (saved_plans/{subject}/{grade}) when the year
    folder does not exist but the flat one does. That fallback is not decoration: it
    keeps a half-migrated tree, an un-migrated clone and every test fixture that builds
    a flat folder all working, and it is what makes migrate_lp_year.py safe to run in
    stages rather than as one irreversible move.

    Delete the fallback only once no flat tree exists anywhere — and note that "anywhere"
    includes a partner's checkout, not just this machine.

    ★ Returns a KEY, not a path (2026-08-29). It used to return an absolute directory,
    which is what made every caller below reach for os.path.join and then open(). The
    emptiness tests are now list_subprefixes() rather than isdir(), which says the same
    thing in the vocabulary an object store can answer: "is there anything stored under
    this prefix?" rather than "does this folder exist?".
    """
    y = (year or LP_YEAR).strip()
    base = f"saved_plans/{subject}/{grade}"
    dated = f"{base}/{y}"
    subs = _st().list_subprefixes(base)
    if y in subs:
        return dated
    # Migrated tree that simply has nothing for this subject·grade yet → still answer
    # with the dated prefix, so a WRITE lands in the right edition rather than recreating
    # the flat layout underneath it.
    if subs:
        return dated
    if _st().list_prefix(base, ".json"):
        return base          # legacy flat tree, pre-migration
    return dated             # nothing exists yet → new writes are foldered


def lp_library_dir(subject: str, grade: str, year: Optional[str] = None) -> str:
    """The library prefix as an absolute filesystem path — LOCAL STORE ONLY.

    Retained for tests and local tooling that need a real directory. No read path in
    this module calls it any more; they all work in keys. On a non-local store this
    raises AttributeError, which is the correct and loud answer."""
    return _st().local_path(lp_library_prefix(subject, grade, year))


def lp_library_years(subject: str, grade: str) -> List[str]:
    """Edition years present for this subject·grade, newest first. A flat legacy tree
    reports no years at all — it is un-editioned, not year zero."""
    out = [e for e in _st().list_subprefixes(f"saved_plans/{subject}/{grade}")
           if _looks_like_year(e)]
    return sorted(out, reverse=True)


def _looks_like_year(name: str) -> bool:
    """"2026-27" — the AcademicYear.year_id shape, reused so the two years are at least
    written the same way even though they mean different things."""
    parts = str(name).split("-")
    return (len(parts) == 2 and len(parts[0]) == 4 and len(parts[1]) == 2
            and parts[0].isdigit() and parts[1].isdigit())


def plan_lp_year(saved: Dict[str, Any]) -> Optional[str]:
    """The edition a saved plan came from, or None for a pre-stamp file.

    Canonicals carry it in their genon_canonical block; served plans inherit it into
    their own `genon` block at serve time. None means "authored before the stamp
    existed", which the UI must render as silence — never as a guess.
    """
    for block in ("genon_canonical", "genon"):
        b = saved.get(block)
        if isinstance(b, dict) and b.get("academic_year"):
            return str(b["academic_year"])
    return None


_ncf_norms_cache: Optional[Dict[str, Any]] = None


def load_ncf_period_norms() -> Dict[str, Any]:
    """National Curricular Framework period norms (periods/year by subject·stage), founder-
    supplied Bucket A content. Cached in-process; file only changes via a manual edit."""
    global _ncf_norms_cache
    if _ncf_norms_cache is None:
        try:
            doc = _st().get_json("allocation_norms/ncf_period_norms.json") or {}
            _ncf_norms_cache = doc.get("subjects", {})
        except Exception:
            _ncf_norms_cache = {}
    return _ncf_norms_cache


def ncf_total_periods(subject: str, stage: str) -> Optional[int]:
    """The NCF-recommended total periods/year for this subject·stage, or None if the norm
    table has no figure for that combination (e.g. Science has none for preparatory)."""
    v = load_ncf_period_norms().get(subject, {}).get(stage)
    return int(v) if v is not None else None


def list_grades(subject: str) -> List[str]:
    return _st().list_subprefixes(f"chapters/{subject}")


def load_mappings(subject: str, grade: str) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for key in _st().list_prefix(f"chapters/{subject}/{grade}/mappings",
                                    "_mapping.json"):
        try:
            doc = _st().get_json(key)
        except Exception:
            continue
        if doc is not None:
            out.append(doc)
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
    prefix = f"framework/{subject}/{stage}"
    out: Dict[str, str] = {}
    for key in _st().list_prefix(prefix, ".json"):
        if not key[len(prefix) + 1:].startswith("competency_descriptions"):
            continue
        try:
            doc = _st().get_json(key)
        except Exception:
            continue
        if doc is not None:
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
    try:
        return _st().get_json(f"framework/english/{stage}/spine_to_cg.json") or {}
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


def list_saved_plans(subject: str, grade: str,
                     year: Optional[str] = None) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for key in _st().list_prefix(lp_library_prefix(subject, grade, year), ".json"):
        try:
            s = _st().get_json(key)
        except Exception:
            continue
        if s is None:
            continue
        out.append({"filename": key.rsplit("/", 1)[-1],
                    "chapter_number": s.get("chapter_number"),
                    "chapter_title": s.get("chapter_title"), "saved_at": s.get("saved_at"),
                    "is_canonical": s.get("plan_status") == "canonical",
                    "lp_year": plan_lp_year(s),
                    "duration_label": duration_label(s)})
    out.sort(key=lambda p: (p.get("chapter_number") or 0, p.get("saved_at") or ""))
    return out


def load_saved_plan(subject: str, grade: str, filename: str,
                    year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    # guard against path traversal
    if "/" in filename or "\\" in filename or ".." in filename:
        return None
    doc = _st().get_json(f"{lp_library_prefix(subject, grade, year)}/{filename}")
    if doc is not None:
        return doc
    # A plan she is still teaching may belong to an EARLIER edition (§2.3: a plan
    # attached to a section is immutable for the life of that attachment). Opening it
    # must not depend on it being the current edition, so look back through the years
    # before giving up. Newest first — an identical filename in two editions means the
    # chapter was carried, and the current edition's copy is the right answer.
    for y in lp_library_years(subject, grade):
        doc = _st().get_json(f"saved_plans/{subject}/{grade}/{y}/{filename}")
        if doc is not None:
            return doc
    return None


# ── master allocation plan (2026-07-25) ─────────────────────────────────────────
# data/cloud/content/allocation_norms/master_plan.json — derived from the founder's
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
    key = "allocation_norms/master_plan.json"
    token = _st().version_token(key)     # opaque; compared, never parsed
    if token is None:
        return None
    if _master_plan_cache and _master_plan_cache[0] == token:
        return _master_plan_cache[1]
    doc = _st().get_json(key)
    if doc is None:
        return None
    _master_plan_cache = (token, doc)
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


def master_canonical_plan(subject: str, grade: str, chapter_number: int) -> Optional[Dict[str, Any]]:
    """The chapter's canonical plan from master_plan.json (genon/variant_plans.py
    v2.0, 2026-08-03): the canonical counts to author (counts[0] = the standard,
    then equal-dispersion points down to the floor — architecture §0.2), which of
    them are on disk, and whether the row is provisional (standard not yet
    authored). No sigma, no closing spans — canonicals are authored free; the
    standard alone carries the synthesis-anchor mandate. None when no row exists."""
    combo = master_combo(subject, grade)
    for row in (combo or {}).get("chapters", []) or []:
        if row.get("chapter") == chapter_number:
            return row.get("canonical_plan")
    return None


# ── genon canonicals (relocated 2026-07-25, founder decision) ───────────────────
# data/cloud/content/ is the home of ALL crucial server content, and saved_plans/ is the
# home of lesson plans — so the certified canonicals live THERE, as ordinary
# saved-plan files named ch_NN_canonical.json (plan_status "canonical"). The genon/
# folder holds engine code only, never content. The phase stream is DERIVED: it is
# compiled on demand from the canonical (strict v0.3) and memo-cached per file
# mtime — no separate stream artifact on disk.

def duration_label(saved: Dict[str, Any]) -> Optional[str]:
    """Small-letter duration line under a plan's name, e.g. "45 min × 12" or
    "40 min × 10 · 30 min × 4".

    EVERY plan carries one, library canonicals included (founder, 2026-08-02).
    This REVERSES the 2026-07-25 naming rule ("the canonical goes by its chapter
    name alone"), which was written when a chapter had exactly ONE canonical and
    the label's only job was to mark a plan as adapted. Under the variant-canonical
    architecture a chapter is a LIBRARY — ch 3 is {12, 9, 7} — and three files that
    all render as "Atmosphere and Climate" with no small print are indistinguishable
    in My Lessons, which is a teacher-facing defect, not a naming preference.
    """
    g = saved.get("genon") or {}
    # served_matrix (2026-08-01): the periods ACTUALLY used — a surrendered request
    # labels 12, not the 13 asked. Falls back to the requested matrix for older files.
    matrix = g.get("served_matrix") or g.get("matrix")
    # Library canonicals carry no `genon` block at all (they are authored, not served);
    # their schedule is the authored standard row in period_rows_snapshot. Served plans
    # never reach this line, so the e10 "print what was served, not what was asked"
    # rule above is untouched.
    if not matrix:
        matrix = saved.get("period_rows_snapshot")
    if not matrix:
        return None
    try:
        return " · ".join(f"{int(m['duration'])} min × {int(m['count'])}" for m in matrix)
    except (KeyError, TypeError, ValueError):
        return None


def _canonical_key(subject: str, grade: str, chapter_number: int,
                   year: Optional[str] = None) -> str:
    return (f"{lp_library_prefix(subject, grade, year)}"
            f"/ch_{int(chapter_number):02d}_canonical.json")


def append_token_log(call_type: str, subject: str, grade: str, chapter_number,
                     chapter_title: str, input_tokens: int, output_tokens: int,
                     cost_inr: float) -> None:
    """Append a paid-run row to the founder's unified cost notebook —
    THIS repo's runtime_data/token_log.csv (fresh log started 2026-07-25, seeded
    with the first ch 5 canonical run; the pre-genon prototype history is archived
    alongside as token_log_old.csv). BEST-EFFORT ONLY: any error is swallowed —
    serving the teacher never waits on bookkeeping.

    ★ THE ONE FUNCTION IN THIS MODULE THAT TOUCHES THE FILESYSTEM DIRECTLY, and it is
    a decision, not an oversight (founder, 2026-08-29). Three reasons it stays out of
    the Storage port: it writes under runtime_data/, not DATA_DIR, so it is not Bucket
    A content at all; nothing in the runtime ever reads it back; and it APPENDS, which
    an object store cannot do — a key is written whole or not at all, so honouring the
    seam here would mean re-uploading the entire notebook once per generated plan.

    If this ever needs to leave the founder's machine, it belongs in STATE_DIR as a
    proper store with its own port, not bolted onto the content seam."""
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


def canonical_version_token(subject: str, grade: str,
                            chapter_number: int) -> Optional[str]:
    """Opaque change-token for a chapter's top canonical, or None if absent.

    Was `canonical_mtime`, returning a float from os.path.getmtime. Renamed rather
    than adapted because the return type changed meaning: a token is compared for
    equality and nothing else, where a float invited ordering ("is this newer than").
    No caller in api/, aruvi_core/ or tests/ referenced the old function — it was
    already dead — so this is a rename with no call sites to chase."""
    return _st().version_token(_canonical_key(subject, grade, chapter_number))


# ── deterministic plan keys (founder decision 2026-07-26) ───────────────────────
# An adapted plan is a CACHE ENTRY, not an event: its filename is derived from what
# actually determines its bytes — chapter, duration matrix, canonical version, engine
# version. Same request from any teacher -> same key -> the entry is served, not
# regenerated. Per-teacher visibility stays where it belongs: the prepared-plans
# register (CLOUD_DATA_MODEL §2.3, reference-not-copy). This is the on-disk stand-in
# for the Bucket-A output cache in §1, so the Supabase migration is a storage swap,
# not a redesign.

GENON_ENGINE_VERSION = "19"     # BUMP when compile/serve change the OUTPUT
# e19 (2026-08-10, S7 · C6) — THE SYNTHESIS FLAG SURVIVES THE SERVE. `synthesis` is a
# MODELLED key, so compile stripped it from `extra`, and `serve._period_from_unit` never
# put it back: every served synthesis unit arrived flagless. On a MEDIATED-anchor stage
# (maths middle/prep) `carriers.is_synthesis` then read False, the port fell through to
# `textbook_segments[0]`, and the closing whole-chapter unit was labelled "Equilateral
# Triangles (Revisit)". The canonical on disk read "Synthesis"; the SERVED plan — the one
# a teacher opens — did not. Served bytes change (one key), so the version moves and every
# _e18_ plan is stale by construction rather than overwritten.
# 18 (2026-08-09): THE APPROACH LINE SURVIVES A SERVE (ARV-D-086, found at S4's C6).
# compile.py's `_MODELLED` listed all five approach key names, which removed them from
# `unit["extra"]` — so serve spliced back none of them and the served period carried only
# the NORMALIZED `pedagogical_approaches`. Four of the five subject ports read the key their
# own constitution emits, so only social_sciences (whose authored key happens to share that
# name) rendered an approach at all: EIGHT of eleven stages served every plan with an empty
# "how do I run this?" line — CLAUDE.md §3(b)'s single canonical line, absent from the only
# artefact a teacher sees, while every canonical on disk carried it correctly. Invisible to
# C1–C5 because none of them reads a served plan; C6 exists for exactly this. Fix: the
# approach keys are no longer modelled, so each subject's own key rides in `extra` verbatim
# (no port change, no subject branching), and `carriers.unit_approaches` now reads all five
# names rather than three. Served bytes change for maths, science, english and TWAU —
# hence the bump. Every `_e17_` plan file is stale by construction and stays on disk.
# 17 (2026-08-07): PLAN GRANULARITY — serving is per-CANONICAL where the subject plugin
# says so. Spec: docs/science_middle_stage_serve.md. science·middle is the corpus's one
# structural exception: its units belong to a cognitive progression arc (LP Rule 1) and a
# stage's implied LO is the outcome of the COMPLETE stage (Rule 5), so no prefix of a
# canonical is a valid plan — truncating mid-arc would test a class on an operation it
# was taught part of, with no honest way to name what is missing. Truncation dies, and
# borrowing with it. That stage is served by whole-canonical SELECTION: identity at X=K,
# K complete + the top's synthesis unit at X=K+1, truncation with declared drops only
# BELOW the lowest canonical, surrender only above the top. No fill, no choice set, no
# section registry. The engine never learns a subject's name — Subject.genon_serve_
# granularity / genon_has_section_axis declare it and carriers.py asks (CLAUDE.md §3);
# compile.py's `section_anchor` read is mediated through the same seam, and the synthesis
# unit is carried by an explicit boolean where there is no anchor field to hold the token.
# Canonical counts for such a stage step down by 2 (genon/master_plan.py), which is what
# makes "no surrender inside the band" true rather than hoped-for; certify enforces it.
# ALL TEN OTHER STAGES ARE BIT-IDENTICAL — verified against the three authored libraries.
# 16 (2026-08-06): A BORROWED UNIT'S COVERAGE ROW TRAVELS WITH IT (ARV-D-064, S1).
# The serve output gains the lender's handoff entry for the borrowed sitting, so the
# LO its questions test is present in the plan that asks them — the rule the dropped-
# unit path has always followed ("their questions are in the plan, so their LOs must
# be too"), applied to the served borrow it had skipped. Paired with the display-side
# half of the same defect: assessment anchoring now READS the platform's stamp
# (link_resolver.platform_anchor) instead of re-deriving it through a plan-local
# mediating key. Safe to carry the row verbatim because the engine handoff is keyed on
# the section LABEL, not on section_number. Cache: founder ruling 2026-08-06 — no
# non-canonical variant is kept permanently, so re-keying costs a re-serve.
# 14 (2026-08-04): SELF-PREFERENCE IN THE Xth-UNIT TIE-BREAK (architecture v2.1
# §0.4). fill_slot's Case-2 sort gains `0 if c["self"] else 1` between reach and
# pacing distance, so the CHOSEN plan's own candidate wins every tie it enters.
# Before this the identity candidate carried no privilege at all and the engine
# borrowed a stranger's closing unit while the plan being served had its own,
# equally first-exposure: SS·IX X=8 (p10's own U8 lost to p07 U7 on |7−8| <
# |10−8|), SS·VIII X=11 (p10 U10 over p13's own U11) and X=14 (p13 U11 over the
# top's own U14). Continuity, not correctness — every candidate is first-exposure
# and therefore safe, which is why nothing broke; but the home unit is written for
# THIS arc and names the content the class just had. Tie-break only: it sits below
# reach, so a home unit that re-crosses still loses to a foreign forward-reaching
# one. Raised at SS·IX's C8 (2026-08-03) and not adopted; recurred at SS·VIII.
# Only Case-2 fills change; identity, synthesis, surrender and below-floor serves
# are byte-identical. Every e13 entry is stale by construction.
# 13 (2026-08-03): UNSERVED ASSESSMENT ITEMS ARE ABSENT (ARV-D-037) — backfilled
# entry; the bump shipped without one. An item whose anchor unit is not scheduled
# used to keep its place with period_ref=[] plus a scheduling_note: it rendered
# NOWHERE on screen (LessonView attaches items by anchor unit) while the EXPORT
# walked assessment_items flat and printed it — 7 of 20 questions on the 8-period
# serve, about units the class never had. The rule now: an item whose unit is not
# in the plan is not in the plan. Count reports in genon.assessment_items_unserved;
# a DROPPED unit's items stay, anchored to the dropped unit's sitting number in
# this plan and flagged unscheduled, and exports omit exactly those.
# 12 (2026-08-03): THE Xth-UNIT CHOICE SET (architecture §0, v2.0) — the fill
# ladder (exact/superset/suffix + lendable-unit walk-back) is replaced by
# first-exposure selection: slot X borrows, from ANY canonical, the unit that
# FIRST deals the next-due section M (preference: forward reach without
# re-cross > M alone > backward combinations). Case 1 borrows the standard's
# mandated `synthesis` unit (reserved anchor token, new); dropped units are
# re-sourced from the LENDER's subsequent units; Case-3 truncation shows no
# drops and asks for the reference canonical's count. Root cause ARV-D-025:
# solver-mandated closing spans imported the lending plan's priors into the
# borrowing plan — the jumpy Xth unit; sigma/closing_spans/variant_solver are
# retired, canonical counts come from equal dispersion over [floor, standard].
# Every e11 entry is stale by construction.
# 11 (2026-08-02): LENDABLE UNIT — the fill ladder no longer offers a variant's
# trailing SYNTHESIS unit. A unit that only re-anchors sections an earlier unit of
# its own plan already taught is written to be met at the end of ITS OWN plan
# ("having traced the full arc…", "rank the factors from the case study"), so
# borrowing it into a foreign prefix produced sittings that assumed lessons the
# class never had — ARV-D-023, found at C7: the 50m x 10 serve carried NO coverage
# note because section coverage was formally complete. Anchoring is not teaching.
# serve.lendable_unit() walks back to the unit that first introduced those sections;
# synthesis mode (prefix already covers the registry) still borrows units[-1], where
# a synthesis assumes nothing false. Side effect: the TOP canonical becomes lendable
# for the first time (its last unit never reached the final section), which is why
# X=8 on SS·IX ch 3 improves from superset to exact.
# 10 (2026-08-01): teacher-facing time prints show the SERVED schedule, never the
# request — period_schedule_display and duration_label build from genon.served_matrix
# (surrendered 13-ask prints 12; request kept as provenance in genon.matrix).
# 09 (2026-08-01): DROPPED SECTIONS — a below-floor serve carries its unreached units
# verbatim in result.dropped_units (unscheduled, authored minutes as guidance), per the
# founder's "give her access to it" ruling. Online-only: the /view endpoint renders them
# through the subject adapter (view.dropped_lp); exports deliberately omit them. The
# result shape changes for every plan (key present, null above floor), so every e08
# entry is stale by construction. Same-day fold (no surrendered e09 artefact existed):
# surrender now files in section_coverage_note — the same generation-time channel as
# drops, per the founder's ruling; genon.surrender_note stays as provenance.
# 08 (2026-07-31): THE PARTITION ENGINE IS RETIRED — replaced by the variant-serve
# engine (docs/variant_canonical_architecture.md). A chapter is a library of variant
# canonicals; a request is served by next-highest selection, the X-1+1 slot-fill
# ladder, and proportional per-unit duration scaling. No DP, no compression regimes,
# no role weighting, no handoff text. Every e07 entry is stale by construction.
# Same-day second pass (no e08 artefact existed yet, so no re-bump): the band
# declaration layer is retired too — compile v0.5 derives band ids positionally and
# anchors assessment items at UNIT level (unit_ref from period_ref, legacy phase_ref
# fallback); serve v1.1 consumes unit_ref.
# 07 (2026-07-29): the seam-polish path is REMOVED (test campaign step 0, docs/testing.md
# §2) — no LLM anywhere in the partition path, and the cache-key shape loses the `_p`
# variant. Plan bytes are unchanged for unpolished runs, but the key namespace changes,
# so every e06 entry is retired rather than overwritten.
# 06 (2026-07-28): a sitting holding 3+ units draws its container text from the adjacent
# pair carrying the most of its MINUTES, not the last pair. Titles and notes change on
# wide spans, which appear wherever the compression ratio is tight.
# 05 (2026-07-28): a mixed-duration matrix is sequenced as a repeating WEEK with the
# longer periods at maximum dispersion, instead of row-by-row (all 50s, then all 60s).
# Every period boundary moves, so every mixed-matrix e04 key is stale by construction.
# Single-duration matrices are unaffected in content but re-key with the bump.
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
        # NOTE (ARV-D-034, resolved differently on 2026-08-04). An in-place repair changes the
        # bytes a serve produces without changing ledger_ts, so a plan derived BEFORE the repair
        # would otherwise be served from cache forever — measured on the pilot, where the
        # 8-period plan carried a repaired-away register breach for four hours.
        # A repair fingerprint in this key was tried and REVERTED (founder): it made every
        # served filename carry a hash tail nobody could read. The invariant now lives in the
        # repair tools instead — `genon/purge_derived.py` deletes the chapter's derived plans
        # whenever a canonical is repaired, so a stale entry cannot exist to be served.
        # If you are tempted to re-key here, read that file first: the choice is where the
        # invalidation lives, not whether it exists.
    import hashlib
    blob = json.dumps(canonical.get("result"), ensure_ascii=False, sort_keys=True).encode()
    return hashlib.sha1(blob).hexdigest()[:12]


def genon_plan_filename(chapter_number, matrix, canonical: Dict[str, Any]) -> str:
    """e.g. ch_05_50m16_e07_c20260726112240.json  (16 x 50 min, engine 07,
    that canonical run). Never collides with ch_NN_canonical.json."""
    return (f"ch_{int(chapter_number):02d}_{norm_matrix(matrix)}"
            f"_e{GENON_ENGINE_VERSION}_c{canonical_version(canonical)}.json")


def genon_chapters(subject: str, grade: str, year: Optional[str] = None) -> List[int]:
    """Chapter numbers with a certified canonical for this subject·grade, in the
    current edition (or `year`)."""
    out: List[int] = []
    for key in _st().list_prefix(lp_library_prefix(subject, grade, year),
                                    "_canonical.json"):
        name = key.rsplit("/", 1)[-1]
        if name.startswith("ch_"):
            try:
                out.append(int(name[3:5]))
            except ValueError:
                pass
    return out


def load_genon_canonical(subject: str, grade: str, chapter_number: int,
                         year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    return _st().get_json(_canonical_key(subject, grade, chapter_number, year))


def load_genon_library(subject: str, grade: str, chapter_number: int,
                       year: Optional[str] = None) -> List[Dict[str, Any]]:
    """The chapter's VARIANT LIBRARY: the top canonical (ch_NN_canonical.json) plus
    any compact variants (ch_NN_canonical_pKK.json — the same section list authored
    at KK periods). Sorted by period count, richest first. Empty when no canonical.

    Scoped to ONE edition: a chapter's library is the set of counts authored together
    against one constitution, so mixing editions here would let the serve engine borrow
    an Xth unit across a version boundary (variant_canonical_architecture §0.4)."""
    out: List[Dict[str, Any]] = []
    top = load_genon_canonical(subject, grade, chapter_number, year)
    if top is not None:
        out.append(top)
    for key in _variant_keys(subject, grade, chapter_number, year):
        doc = _st().get_json(key)
        if doc is not None:
            out.append(doc)

    def _count(c):
        row = (c.get("period_rows_snapshot") or c.get("period_schedule")
               or (c.get("result") or {}).get("period_schedule") or [{}])
        row = row[0] if isinstance(row, list) else {}
        return int(row.get("count") or row.get("period_count")
                   or len(((c.get("result") or {}).get("lesson_plan") or {}).get("periods") or []))

    out.sort(key=_count, reverse=True)
    return out


_stream_cache: Dict[str, Any] = {}   # key -> (version_token, stream)


def _variant_keys(subject: str, grade: str, chapter_number: int,
                  year: Optional[str] = None) -> List[str]:
    """Sorted keys of a chapter's COMPACT variants (ch_NN_canonical_pKK.json).

    One definition, used by load_genon_library and load_genon_streams alike — they
    each carried their own copy of the prefix test, which is two chances to disagree
    about what belongs in a chapter's library."""
    stem = f"ch_{int(chapter_number):02d}_canonical_p"
    prefix = lp_library_prefix(subject, grade, year)
    return [k for k in _st().list_prefix(prefix, ".json")
            if k.rsplit("/", 1)[-1].startswith(stem)]


def load_genon_stream(subject: str, grade: str, chapter_number: int,
                      year: Optional[str] = None) -> Optional[Dict[str, Any]]:
    """The top canonical's phase stream, compiled (strict, declared-only).
    Memo-cached per object version, so the millisecond serve path never pays the
    compile twice for an unchanged canonical."""
    return _compiled(_canonical_key(subject, grade, chapter_number, year))


def _compiled(key: str) -> Optional[Dict[str, Any]]:
    token = _st().version_token(key)
    if token is None:
        return None
    hit = _stream_cache.get(key)
    if hit and hit[0] == token:
        return hit[1]
    doc = _st().get_json(key)
    if doc is None:
        return None
    from aruvi_core.genon import compile_stream
    stream = compile_stream(doc)
    _stream_cache[key] = (token, stream)
    return stream


def load_genon_streams(subject: str, grade: str, chapter_number: int,
                       year: Optional[str] = None) -> List[Dict[str, Any]]:
    """Compiled streams for the chapter's whole variant library, richest first.
    Empty list when the chapter has no canonical at all. One edition only — see
    load_genon_library."""
    keys = [_canonical_key(subject, grade, chapter_number, year)]
    keys += _variant_keys(subject, grade, chapter_number, year)
    streams = [s for s in (_compiled(k) for k in keys) if s is not None]
    streams.sort(key=lambda s: -len(s.get("units") or []))
    return streams


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
    # Writes always land in the CURRENT edition: a served plan is derived from the
    # canonical the teacher was just given, and that is by definition the current one.
    prefix = lp_library_prefix(subject, grade)
    if not filename:
        nn = f"{int(plan.get('chapter_number') or 0):02d}"
        ts = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"ch_{nn}_{ts}.json"
        seq = 1
        while _st().exists(f"{prefix}/{filename}"):     # same-second uniqueness
            filename = f"ch_{nn}_{ts}_{seq}.json"
            seq += 1
    plan["filename"] = filename
    plan["saved_at"] = datetime.now().isoformat(timespec="seconds")
    # indent=2 + ensure_ascii=False preserved exactly: the library is read by humans
    # and diffed by the authoring tools, and a reformatting write would show up as
    # every file changing.
    _st().put_bytes(f"{prefix}/{filename}",
                       json.dumps(plan, ensure_ascii=False, indent=2).encode("utf-8"),
                       "application/json")
    return filename
