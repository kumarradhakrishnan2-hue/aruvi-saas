"""File-backed reference implementation of DataRightsService (Step 4: export + erase).

One traversal, two directions. EXPORT walks every Bucket-B store a teacher owns —
account, academic years, teaching profile, and per year: chapter notes, allocations,
section state, prepared register, archive flags — and renders it as one editable Word
document (export_data_rights_docx.build_export_docx). ERASE walks the same path
destructively (account record last) and returns an ErasureReceipt naming what was kept
and why (§2.6: backups ≤30 days, statutory tax records, shared content).

Reads go through the same file adapters the API uses, so the walk can never drift from
what the app actually stores. The ONE filesystem-level read is enumerating which
subject·grade allocation registers exist for a year (the AllocationRepository port
addresses by subject·grade and deliberately has no listing method); the partner's DB
adapter replaces that with a WHERE tenant_id=… scan — which is also the isolation
proof: if this traversal can reach another tenant's row, RLS was never real.

Erase notes:
  * shutil.rmtree per {kind}/{tenant}/{user} — a folder boundary, exactly what the
    Step-1 re-filing bought us. Nothing outside the identity's folders is touched.
  * The user ID is NOT reserved afterwards: signing in again JIT-creates a fresh empty
    account (founder 2026-08-22 — a tombstone would itself be a remnant).
  * Idempotent: erasing an empty identity returns an empty `erased` list, no error.
"""
import re
import shutil
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional, Tuple

from aruvi_core.ports import DataRightsService, ErasureReceipt
from aruvi_core.adapters.account_repository_file import AccountRepositoryFileImpl
from aruvi_core.adapters.academic_year_repository_file import AcademicYearRepositoryFileImpl
from aruvi_core.adapters.readiness_repository_file import ReadinessRepositoryFileImpl
from aruvi_core.adapters.allocation_repository_file import AllocationRepositoryFileImpl
from aruvi_core.adapters.section_state_repository_file import SectionStateRepositoryFileImpl
from aruvi_core.adapters.plan_archive_repository_file import PlanArchiveRepositoryFileImpl
from aruvi_core.adapters.prepared_plans_repository_file import PreparedPlansRepositoryFileImpl
from aruvi_core.adapters.plan_note_repository_file import PlanNoteRepositoryFileImpl


def _slug(s: str) -> str:
    """Filesystem-safe slug — must match the repository adapters'."""
    s = str(s).strip() or "local"
    return "".join(c if c.isalnum() or c in "-_" else "-" for c in s).strip("-") or "local"


# The year-scoped teaching-state kinds, in erase order. readiness (the profile) is
# tenant-keyed but NOT year-scoped; accounts/academic_years are handled explicitly.
_YEAR_KINDS = ("plan_notes", "section_state", "allocations", "prepared_plans", "plan_archive")

# §2.6 verbatim — the receipt's wording is pinned by test_data_rights and must match
# what the privacy policy promises. Change both together or neither.
_KEPT = [
    {"what": "Disaster-recovery backups",
     "why": "Deleted from the live system immediately; purged from backups within 30 days."},
    {"what": "Tax records for payments made",
     "why": "GST invoices carry a statutory retention period and outlive the account."},
    {"what": "Shared lesson-plan library content",
     "why": "Lesson plans are Aruvi's shared library, not personal data; your account "
            "held references to them, and those references are erased."},
]


# Grade slugs as they appear inside section keys ("{subjectSlug}_{gradeSlug}_{tag}").
_GRADE_SLUGS = {"iii", "iv", "v", "vi", "vii", "viii", "ix", "x"}


def _parse_section_key(key: str) -> Tuple[str, str, str]:
    """"the_world_around_us_iv_4A" → ("the_world_around_us", "iv", "4A"). The subject
    slug itself contains underscores, so parse from the RIGHT: last token is the
    section tag, the token before it must be a grade slug. Unparseable keys come back
    whole as the subject so nothing is ever dropped from an export."""
    toks = (key or "").split("_")
    if len(toks) >= 3 and toks[-2].lower() in _GRADE_SLUGS:
        return "_".join(toks[:-2]), toks[-2].lower(), toks[-1]
    return key or "", "", ""


def _chapter_num_from_file(filename: str) -> Optional[int]:
    """"ch_05_canonical.json" → 5 (the live shape); a bare "3" → 3 (older rows).
    None when neither form matches — the row still exports, chapter shown as "—"."""
    s = str(filename or "")
    m = re.match(r"ch_(\d+)", s)
    if m:
        return int(m.group(1))
    try:
        return int(s)
    except ValueError:
        return None


class DataRightsServiceFileImpl(DataRightsService):
    """File-backed export/erase traversal over the Bucket-B stores."""

    def __init__(self, data_dir: str,
                 chapter_title: Optional[Callable[[str, str, int], str]] = None):
        """
        Args:
            data_dir: Base directory holding the Bucket-B folders (e.g. ARUVI_STATE_DIR).
            chapter_title: optional resolver (subject_slug, grade_slug, chapter_number)
                → display title, injected by the API layer from the shared content
                store (Bucket A). The service itself never reads content — this seam
                keeps the Bucket split intact. Absent (tests, bare use), chapter
                titles simply render empty.
        """
        self.chapter_title = chapter_title
        self.data_dir = Path(data_dir)
        self.accounts = AccountRepositoryFileImpl(data_dir)
        self.years = AcademicYearRepositoryFileImpl(data_dir)
        self.readiness = ReadinessRepositoryFileImpl(data_dir)
        self.allocations = AllocationRepositoryFileImpl(data_dir)
        self.sections = SectionStateRepositoryFileImpl(data_dir)
        self.archive = PlanArchiveRepositoryFileImpl(data_dir)
        self.prepared = PreparedPlansRepositoryFileImpl(data_dir)
        self.notes = PlanNoteRepositoryFileImpl(data_dir)

    # ── the one traversal ─────────────────────────────────────────────────────────

    def _year_ids(self, tenant_id: str, user_id: str) -> List[str]:
        """Every year that exists for this identity: the opened years, plus any year
        folder present on disk under a teaching kind (belt-and-braces — data must
        never be invisible to its owner because a year record went missing)."""
        ids = [y.year_id for y in self.years.list_years(tenant_id, user_id)]
        for kind in _YEAR_KINDS:
            d = self.data_dir / kind / _slug(tenant_id) / _slug(user_id)
            if d.is_dir():
                for p in d.iterdir():
                    if p.is_dir() and p.name not in ids:
                        ids.append(p.name)
        return sorted(ids)

    def _allocation_registers(self, tenant_id: str, user_id: str,
                              year_id: str) -> Dict[str, Any]:
        """{"subject/grade": register} for one year — enumerated from the folder
        layout, loaded through the port."""
        out: Dict[str, Any] = {}
        base = (self.data_dir / "allocations" / _slug(tenant_id) / _slug(user_id)
                / _slug(year_id))
        if not base.is_dir():
            return out
        for reg_file in sorted(base.glob("*/*/allocation.json")):
            subject, grade = reg_file.parent.parent.name, reg_file.parent.name
            reg = self.allocations.load_register(tenant_id, user_id, year_id, subject, grade)
            if reg:
                out[f"{subject}/{grade}"] = reg
        return out

    def _gather(self, tenant_id: str, user_id: str) -> Dict[str, Any]:
        """Everything this teacher owns, as one plain-dict payload."""
        acct = self.accounts.load(tenant_id, user_id)
        payload: Dict[str, Any] = {
            "exported_at": datetime.now(timezone.utc).isoformat(),
            "account": asdict(acct) if acct else None,
            "profile": self.readiness.load_profile(tenant_id, user_id),
            "years": [],
        }
        for year_id in self._year_ids(tenant_id, user_id):
            notes = self.notes.load_all(tenant_id, user_id, year_id)
            states = self.sections.load_all(tenant_id, user_id, year_id)
            payload["years"].append({
                "year_id": year_id,
                "notes": {k: {"text": n.text, "updated_at": n.updated_at,
                              "chapter_title": self._title_for_key(k)}
                          for k, n in notes.items()},
                "teaching": self._teaching_rows(states),
                # Raw stores ride along for completeness (the erase walk and any future
                # machine-readable export); the Word renderer shows the reader-facing
                # `teaching` rows instead — no filenames, no period internals (founder,
                # 2026-08-22).
                "allocations": self._allocation_registers(tenant_id, user_id, year_id),
                "section_state": states,
                "prepared": self.prepared.load_all(tenant_id, user_id, year_id),
                "archived": self.archive.load_all(tenant_id, user_id, year_id),
            })
        return payload

    def _title_for_key(self, note_key: str) -> str:
        """Chapter display title for a note key "subject/grade/chapter" — via the
        injected content resolver; empty when unresolvable."""
        parts = (note_key or "").split("/")
        if self.chapter_title and len(parts) == 3:
            try:
                return self.chapter_title(parts[0], parts[1], int(parts[2])) or ""
            except (TypeError, ValueError):
                return ""
        return ""

    def _teaching_rows(self, states: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Reader-facing teaching-state rows, one per subject·grade·chapter, with the
        sections teaching it and each section's plain-words status. Deliberately free
        of filenames, canonical identities and period counts."""
        grouped: Dict[Tuple[str, str, Optional[int]], Dict[str, Any]] = {}
        for key in sorted(states):
            st = states[key] or {}
            subject, grade, tag = _parse_section_key(key)
            num = _chapter_num_from_file(st.get("chapter"))
            gk = (subject, grade, num)
            row = grouped.setdefault(gk, {
                "subject": subject, "grade": grade, "chapter_number": num,
                "chapter_title": (self.chapter_title(subject, grade, num) or ""
                                  if self.chapter_title and num else ""),
                "sections": [],
            })
            if st.get("done"):
                status = "completed"
            elif st.get("unit_index") is None:
                status = "started"
            else:
                status = f"at Learning Unit {int(st['unit_index']) + 1}"
            row["sections"].append({"tag": tag or key, "status": status})
        return list(grouped.values())

    # ── export ────────────────────────────────────────────────────────────────────

    def export(self, tenant_id: str, user_id: str, fmt: str = "docx") -> bytes:
        """One document with everything she owns (never the shared library), as Word
        (default, editable) or PDF — the same payload through two renderers, so the
        two formats can never disagree on content. Lazy imports so a missing
        python-docx/xhtml2pdf breaks only this feature, with a clear message — the
        same posture as the allocation exporters."""
        payload = self._gather(tenant_id, user_id)
        fmt = (fmt or "docx").strip().lower()
        if fmt == "docx":
            from aruvi_core.export_data_rights_docx import build_export_docx
            return build_export_docx(payload)
        if fmt == "pdf":
            from aruvi_core.export_data_rights_pdf import export_data_rights_pdf
            return export_data_rights_pdf(payload)
        raise ValueError(f"Unknown export format {fmt!r} — use 'docx' or 'pdf'.")

    # ── erase ─────────────────────────────────────────────────────────────────────

    def _rm(self, path: Path, stop: Path) -> bool:
        """Remove a folder if present, then climb: remove each now-empty ancestor up
        to (never including) `stop`, the store root — an empty folder named after her
        is still a remnant. A school tenant with other teachers keeps its folder
        (non-empty, so the climb halts there). Returns whether anything was removed."""
        if not path.is_dir():
            return False
        shutil.rmtree(path)
        parent = path.parent
        try:
            while parent != stop and parent.is_dir() and not any(parent.iterdir()):
                parent.rmdir()
                parent = parent.parent
        except OSError:
            pass  # never let tidying the shell fail the erasure itself
        return True

    def erase(self, tenant_id: str, user_id: str) -> ErasureReceipt:
        """Destroy everything export() reaches — teaching state per year, profile,
        year records, account record LAST — and name what was kept and why."""
        t, u = _slug(tenant_id), _slug(user_id)
        erased: List[str] = []
        label = {"plan_notes": "chapter notes", "section_state": "section progress",
                 "allocations": "period allocations", "prepared_plans": "prepared plans",
                 "plan_archive": "archived-plan flags"}
        year_ids = self._year_ids(tenant_id, user_id)
        for kind in _YEAR_KINDS:
            root = self.data_dir / kind
            for year_id in year_ids:
                if self._rm(root / t / u / _slug(year_id), stop=root):
                    erased.append(f"{label[kind]} ({year_id})")
            self._rm(root / t / u, stop=root)   # any stray un-year-scoped leftovers
        if self._rm(self.data_dir / "readiness" / t / u, stop=self.data_dir / "readiness"):
            erased.append("teaching profile")
        if self._rm(self.data_dir / "academic_years" / t / u,
                    stop=self.data_dir / "academic_years"):
            erased.append("academic-year records")
        # Account record LAST — identity must outlive its data during the walk.
        if self.accounts.load(tenant_id, user_id) is not None:
            self._rm(self.data_dir / "accounts" / t / u, stop=self.data_dir / "accounts")
            erased.append("account record")
        return ErasureReceipt(
            erased=erased,
            kept=[dict(k) for k in _KEPT] if erased else [],
            erased_at=datetime.now(timezone.utc).isoformat(),
        )
