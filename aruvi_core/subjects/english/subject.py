"""
English subject plugin — the two-axis case (the architecture's hardest stress test).

Organizing structure: OUTER axis = main_sections (a poem/prose/dialogue), INNER axis = the
6-spine cells within each section (Reading, Listening, Speaking, Writing, Vocab/Grammar,
Beyond-the-Text). The prototype emits periods carrying both `section_id`/`section_title` and
`spines_taught[]`, and an assessment ALREADY grouped by spine. NCF compliance is implicit in
the spine structure — there are NO C-codes in the English LP.

This plugin maps that into nested canonical Groups (section -> spine -> periods) so the
shared renderer reproduces the two-axis layout without any English-specific branch.

Prompt assembly strips `tasks_verbatim`/`question_bank` from the summary before sending
(MEMORY #26 / prototype TASK #4): constitution prohibitions alone can't stop the model
copying textbook exercises it can see — so we remove them from context.
"""
from __future__ import annotations

import copy
from typing import Any, Dict, List, Union

from ..base import Subject  # noqa: F401
from ...assessment_norm import from_english
from ...genon.carriers import is_synthesis as _is_synth   # the token OR the boolean (S7)
from ...genon.serve import _ANCHOR_JOINER          # " / " — the V2 multi-section join
from ...link_resolver import norm_code, platform_anchor, stamp
from ...normalize import (
    SYNTHESIS_DISPLAY, as_list, classify_stimulus, normalize_options, phases_from,
)
from ...ports import Prompt
from ...view_model import (
    AssessmentGroup, AssessmentItem, AssessmentView, Group, LessonPlanView, Period,
)


def _spine_label(codes: List[str]) -> str:
    return " + ".join(c.replace("_", " ").title() for c in codes) or "General"


def _task_lines(tasks: Any) -> List[str]:
    """English tasks_in_class are dicts {spine, task_index, task_brief}; show the brief."""
    out: List[str] = []
    for t in tasks or []:
        if isinstance(t, dict):
            txt = t.get("task_brief") or t.get("task") or t.get("brief") or ""
            if txt:
                out.append(str(txt))
        elif str(t).strip():
            out.append(str(t))
    return out


def _homework_text(hw: Any) -> str:
    """Homework may be a plain string OR a list of task dicts (same shape as tasks_in_class)."""
    if isinstance(hw, list):
        return "; ".join(_task_lines(hw))
    return hw or ""


def _phase_lines(phases: Any) -> List[str]:
    out: List[str] = []
    for ph in phases or []:
        if isinstance(ph, dict):
            name = ph.get("phase") or ph.get("phase_name") or ph.get("name") or ""
            desc = ph.get("description") or ph.get("activity") or ""
            line = f"{name}: {desc}".strip(": ").strip()
            if line:
                out.append(line)
        elif str(ph).strip():
            out.append(str(ph))
    return out


def _bands(period: Dict[str, Any]) -> Any:
    """This period's timed spine, under whichever key its constitution version used.

    `time_bands` NEWEST FIRST: P3 converted the secondary LP to `time_bands[{minutes,
    activity}]` at v1.2 (2026-08-12, S11), and the compiler reads exactly that — but the
    whole existing english saved-plan corpus, at every stage, is still on
    `phases[{minutes, description}]`. Reading both is what covers display across the
    changeover; `normalize.phases_from` already accepts either text key, so nothing below
    this line has to know which shape arrived. Same tolerant read, and the same reason, as
    `mathematics/subject.py`.
    """
    tb = period.get("time_bands")
    if isinstance(tb, list) and tb:
        return tb
    return period.get("phases")


# ── 8-rule ROW 7 · the (section × spine) CELL, shared by the app and by genon ──────
def cell_key(section_id: Any, spine: Any) -> str:
    """The composite join key english's row of the verified 8-rule table uses.

    An item carries (`source_section_id`, `source_spine`); a period carries `section_id` and
    a list of `spines_taught[]`. Neither half identifies a cell alone — the constitution's
    own DESIGN PRINCIPLE says bin-packing is across (section × spine) CELLS, not across
    spines — so the key is the pair, normalised on both sides by `link_resolver.norm_code`.
    One function, so the display path and the genon carrier cannot drift into two spellings.
    """
    return f"{norm_code(section_id)}|{norm_code(spine)}"


def _disperse(units: List[int], n: int) -> List[List[int]]:
    """Cut `units` (sorted, deduped) into `n` contiguous blocks by EVEN DISPERSION.

    Largest-remainder, the same shape `genon/master_plan.canonical_periods` uses: base =
    M // n, and the first M % n blocks take one extra unit, so the earlier blocks are the
    longer ones and the closing block always ends on the cell's last unit. `stamp()` anchors
    each item at the LAST unit of its own block, so with n = 2 over eight units the pair lands
    on units 4 and 8 rather than both on 8.

    Caller guarantees M >= n >= 2. Documented and tested in `cell_resolver`.
    """
    m, out, i = len(units), [], 0
    base, rem = divmod(m, n)
    for b in range(n):
        size = base + (1 if b < rem else 0)
        out.append(units[i:i + size])
        i += size
    return out


def _backfill(units: List[int], n: int) -> List[List[int]]:
    """N items over M units with 2 <= M < N: anchor BACKWARDS FROM THE CLOSE, one item per
    unit, and pile the surplus (the EARLIEST items) on the cell's first unit.

    ADDED 2026-08-15 (S11·W1, founder ruling: back-fill to close, do not touch the
    constitution). `cell_resolver`'s dispersion guard is `M >= N`, and everything failing it
    fell to the shared-span branch, whose comment reads "MORE items than units — anchoring at
    the close then does the right thing". That is true of the case the branch was written for
    (M == 1: there is no other unit to reach). It is NOT true once M >= 2. The english
    preparatory W1 corpus produced two cells where it visibly is not — iii ch 3 (A, oracy),
    three units [4, 5, 6] and four items, and iii ch 15 (B, word_work), two units [4, 5] and
    four — and in both every item collapsed onto the closing unit while the earlier sittings,
    which teach that very cell, carried no Assess tab at all.

    Both arose the same way: TWO authored pairs sharing one (section × spine) address, the
    cell key being coarser than `source_lo`. Whether the upstream double-filing is worth
    changing is a separate question and deliberately not answered here — the resolver should
    behave sanely either way.

    WHY BACKWARDS and not `_disperse`'s forward largest-remainder. Rule 8A scopes the LAST
    item of a cell to that cell's completion, so the invariant the shared-span branch was
    protecting is real and must survive: **the final item anchors at the cell's close**.
    Dealing forward would break it whenever the remainder fell the other way. Filling from the
    close backwards keeps it by construction, and the overflow lands on the cell's FIRST unit,
    which is where the earliest-authored (lowest-rung) items belong anyway.

        [4, 5, 6] × 4 items -> [[4], [4], [5], [6]]
        [4, 5]    × 4 items -> [[4], [4], [4], [5]]

    Caller guarantees 2 <= M < N. Tested in `cell_resolver`.
    """
    m = len(units)
    return [[units[max(m - 1 - (n - 1 - i), 0)]] for i in range(n)]


def cell_resolver(periods: List[Dict[str, Any]], spine_groups: Any):
    """Return `resolve(item) -> [period numbers]` for row 7, pairing INCLUDED.

    Lifted verbatim out of `assessment_to_view` at S11 (2026-08-12) so that genon's carrier
    runs the SAME resolution the app has been running since 2026-07-11, rather than a second
    join that would look equivalent and drift. Two behaviours it must keep:

    THE N-TO-N PAIRING (2026-07-11), GENERALISED TO EVEN DISPERSION (2026-08-12). The coarse
    (section, spine) join cannot tell a real SPAN — one item re-tested across several units, a
    genuine set — from SEVERAL items that merely share a cell, one per topic-unit (word_work
    taught as Collective Nouns in U4 and Position Words in U5, with a MATCH item and a FILL_IN
    item). Giving every item the union collapsed them all onto the closing unit and surfaced
    the collective-nouns item under the prepositions unit. So when a cell has N items and M
    units with M >= N >= 2, the M units are cut into N CONTIGUOUS BLOCKS by even dispersion
    (largest-remainder: the first M%N blocks take one extra unit) and item i takes block i.
    Items are authored in slot/topic order, units are in teaching order.

    M == N is the original N-to-N case and falls out of the same arithmetic — every block is
    one unit long — so there is one code path, not two that could drift.

    M > N is what the english PAIR needs (assessment constitutions english/secondary v1.6,
    english/middle v3.6, english/preparatory v1.4, 2026-08-12). A cell now emits TWO items —
    a lower-rung slot 1 and a higher-rung slot 2 — and a Reading cell is routinely taught over
    eight units. Handing both the union anchored both at the close: the ratio doubled but the
    coverage did not, and eleven of seventeen units still had no Assess tab. Dealing blocks
    puts slot 1 at the end of the cell's first half and slot 2 at the close. Rule 8A of each of
    those constitutions is what licenses this — it declares slot 1 scoped to the cell's early
    teaching and slot 2 to its completion, so the split is authored-for, not imposed.

    M < N OVER MORE THAN ONE UNIT BACK-FILLS TO THE CLOSE (2026-08-15, S11·W1, founder). The
    shared-span branch below used to take this shape too, on the reasoning that more items than
    units "cannot be dealt". That holds at M == 1 and nowhere else: english·preparatory W1 threw
    two cells at M = 3 / N = 4 and M = 2 / N = 4 where every item collapsed onto the closing
    unit and the earlier sittings that teach the cell showed no Assess tab. `_backfill` anchors
    one item per unit BACKWARDS from the close and piles the surplus on the cell's first unit,
    which keeps Rule 8A's real invariant — the last item lands at the cell's completion.

    Every other shape — one item over many units (a true span), or a cell taught in a SINGLE
    unit — keeps the full set, and anchoring at the close then does the right thing.

    STANDING CAVEAT (carried from 2026-07-11, and now load-bearing): dispersion assumes items
    are authored in teaching order. Rule 2 of all three constitutions now MANDATES that order
    ("slot 1 precedes slot 2; never interleave two contributions' items") rather than relying
    on it being incidentally true, which is what makes M > N safe to deal.

    THE SECTION-WIDE FALLBACK. A cell with no matching unit falls back to any unit of its
    section, so an item still anchors somewhere rather than vanishing from the teacher's view.

    SYNTHESIS UNITS ARE NOT INDEXED. A closing unit revisits several cells without teaching
    one, so indexing it would make it the LAST unit of every cell it names and collapse the
    whole chapter's items onto it — the defect S7 met on maths·middle ch 7 (carriers.py
    documents it at `items_by_period_field`). Third site, same seam.
    """
    period_index: Dict[str, List[int]] = {}
    section_index: Dict[str, List[int]] = {}      # section_id → all its units (fallback)
    for p in periods or []:
        pn = p.get("period_number")
        if pn is None or _is_synth(p):
            continue
        sid = norm_code(p.get("section_id"))
        section_index.setdefault(sid, []).append(int(pn))
        for sp in (p.get("spines_taught") or []):
            period_index.setdefault(cell_key(p.get("section_id"), sp), []).append(int(pn))

    key_items: Dict[str, List[dict]] = {}
    for sg in spine_groups or []:
        for it in (sg.get("items") if isinstance(sg, dict) else None) or []:
            key_items.setdefault(
                cell_key(it.get("source_section_id"), it.get("source_spine")), []).append(it)

    key_periods: Dict[str, List[List[int]]] = {}  # key → unit-lists aligned to key_items[key]
    for k, its in key_items.items():
        sid = k.split("|", 1)[0]
        exact = period_index.get(k)
        uniq = sorted(set(exact)) if exact else []
        if exact and len(its) >= 2 and len(uniq) >= len(its):
            key_periods[k] = _disperse(uniq, len(its))     # N-to-N (M==N) / blocks (M>N)
        elif exact and len(its) >= 2 and len(uniq) >= 2:
            key_periods[k] = _backfill(uniq, len(its))     # M<N over >1 unit: fill to close
        else:
            span = exact if exact else section_index.get(sid, [])
            key_periods[k] = [span for _ in its]           # true span / fallback: shared set

    pos: Dict[str, int] = {}

    def resolve(item: Dict[str, Any]) -> List[int]:
        k = cell_key(item.get("source_section_id"), item.get("source_spine"))
        i = pos.get(k, 0)
        pos[k] = i + 1                # advanced even when the caller discards the answer,
        lists = key_periods.get(k) or []          # so a stamped item never shifts its siblings
        return list(lists[i]) if i < len(lists) else []

    return resolve


class EnglishSubject:
    name = "english"

    def __init__(self, *, lp_constitution: str = "", assessment_constitution: str = "",
                 pedagogy: str = "") -> None:
        self._lp_const = lp_constitution
        self._assess_const = assessment_constitution
        self._pedagogy = pedagogy

    # ── Prompt assembly ─────────────────────────────────────────────────────────
    def build_lesson_plan_prompt(self, *, grade, chapter, summary, mapping, period_profile) -> Prompt:
        summary = self._strip_contamination(summary)
        system = (
            "You are Aruvi's English lesson plan generator. The Lesson Plan Constitution "
            "below is binding.\n\n"
            f"=== ENGLISH LESSON PLAN CONSTITUTION ===\n{self._lp_const}\n"
        )
        user = (
            f"=== PEDAGOGY ===\n{self._pedagogy}\n\n"
            f"=== CHAPTER SUMMARY ===\n{summary}\n\n"
            f"=== MAPPING (effort index) ===\n{mapping}\n\n"
            f"=== TEACHER PERIOD SCHEDULE ===\n{period_profile}\n\n"
            "=== INSTRUCTIONS ===\nWalk main_sections in textbook order, then spines within "
            "each section. Periods carry `section_id`, `section_title`, and `spines_taught[]`. "
            "Do NOT emit C-codes. Output a single valid JSON object with `lesson_plan.periods[]` "
            "and `coverage_handoff`. Raw JSON only — no markdown."
        )
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    def build_assessment_prompt(self, *, grade, chapter, summary, mapping, lesson_plan) -> Prompt:
        summary = self._strip_contamination(summary)
        system = (
            "You are Aruvi's English assessment generator. The Assessment Constitution below "
            "is binding.\n\n"
            f"=== ENGLISH ASSESSMENT CONSTITUTION ===\n{self._assess_const}\n"
        )
        user = (
            f"=== CHAPTER SUMMARY ===\n{summary}\n\n"
            f"=== LESSON PLAN (section x spine handoff) ===\n{lesson_plan}\n\n"
            "Generate one original item per (section x spine) implied_lo, grounded in section "
            "text. Group items by spine. Raw JSON only with an `assessment_items` array of "
            "spine groups."
        )
        return Prompt(system=system, messages=[{"role": "user", "content": user}], cache_system=True)

    @staticmethod
    def _strip_contamination(summary: Any) -> Any:
        """Remove tasks_verbatim / question_bank everywhere in the summary (MEMORY #26)."""
        if not isinstance(summary, (dict, list)):
            return summary
        s = copy.deepcopy(summary)

        def strip(o: Any) -> None:
            if isinstance(o, dict):
                o.pop("tasks_verbatim", None)
                o.pop("question_bank", None)
                for v in o.values():
                    strip(v)
            elif isinstance(o, list):
                for v in o:
                    strip(v)

        strip(s)
        return s

    def chapter_weight(self, mapping):
        return float(mapping.get("effort_index") or 0)

    def allocation_basis(self, grade):
        return {"basis": "effort index", "factors": [
            "The language spines a chapter exercises — reading, listening, speaking, "
            "writing, vocabulary & grammar, and beyond-the-text",
            "How densely tasks are packed",
            "The writing demand",
            "Any project work",
        ]}

    # ── Validation ──────────────────────────────────────────────────────────────
    def validate(self, raw: Dict[str, Any]) -> Dict[str, Any]:
        lp = raw.get("lesson_plan", raw)
        if isinstance(lp, dict) and "periods" in lp:
            if not lp["periods"]:
                raise ValueError("English lesson plan has no periods (possible truncation).")
        elif "assessment_items" in raw:
            if not raw["assessment_items"]:
                raise ValueError("English assessment has no items (possible truncation).")
        return raw

    # ── Normalization → canonical view model (nested section -> spine) ──────────
    def lesson_plan_to_view(self, raw: Dict[str, Any], *, grade, chapter) -> LessonPlanView:
        lp = raw.get("lesson_plan", raw)
        periods = lp.get("periods", [])
        sections: List[Group] = []
        sec_index: Dict[str, Group] = {}
        spine_index: Dict[tuple, Group] = {}

        # (spine, section_id) -> implied_lo. English's handoff is a DICT keyed by spine,
        # each holding section_contributions[] — one cell per (section × spine), which is
        # exactly the granularity the LO is authored at. Rejoined here so the lesson plan
        # can show what a spine group builds toward; previously the LO reached only the
        # pair of items Rule 2 generates from each cell. A group taught under several
        # spines carries several LOs — joined in the order the group names them.
        lo_by_cell: Dict[tuple, str] = {}
        ho = raw.get("coverage_handoff") or lp.get("coverage_handoff") or {}
        if isinstance(ho, dict):
            for spine, entry in ho.items():
                if not isinstance(entry, dict):
                    continue
                for c in (entry.get("section_contributions") or []):
                    if isinstance(c, dict) and c.get("implied_lo"):
                        lo_by_cell[(spine, c.get("section_id"))] = str(c["implied_lo"]).strip()

        for p in periods:
            sid = p.get("section_id", "")
            if sid not in sec_index:
                g = Group(type="section", label=p.get("section_title", ""), meta={"section_id": sid})
                sec_index[sid] = g
                sections.append(g)
            spines = p.get("spines_taught") or []
            # THE CLOSING UNIT IS ITS OWN GROUP, LABELLED AS ONE (2026-08-12, S11).
            # A whole-chapter synthesis names the spines it revisits, so grouping on the
            # spine signature alone would file it under "Listening + Writing" — or merge it
            # into a teaching group that happens to carry the same pair. That is ARV-D-016's
            # and ARV-D-101's shape on a fourth port, and the served plan is what the teacher
            # opens. The fact is read through `carriers.is_synthesis`, never off the title.
            if _is_synth(p):
                sig, label = "__synthesis__", SYNTHESIS_DISPLAY
            else:
                sig, label = ("+".join(spines) if spines else "general"), _spine_label(spines)
            key = (sid, sig)
            if key not in spine_index:
                _los: List[str] = []
                for _sp in spines:
                    _lo = lo_by_cell.get((_sp, sid))
                    if _lo and _lo not in _los:
                        _los.append(_lo)
                sg = Group(type="spine", label=label,
                           meta={"spine_codes": spines, "implied_lo": " ".join(_los)})
                spine_index[key] = sg
                sec_index[sid].children.append(sg)
            # approach: pedagogical_methods is a {spine: method} dict — join the
            # UNIQUE methods in first-seen order (prototype step 3). Tolerate the
            # legacy singular pedagogical_method string.
            ped = p.get("pedagogical_methods")
            if isinstance(ped, dict) and ped:
                seen: List[str] = []
                for m in ped.values():
                    m = str(m or "").strip()
                    if m and m not in seen:
                        seen.append(m)
                approach = "; ".join(seen)
            else:
                approach = str(p.get("pedagogical_method") or "").strip()
            spine_index[key].periods.append(Period(
                number=p.get("period_number", 0),
                title=p.get("activity_title", ""),
                approach=approach,
                activities=_task_lines(p.get("tasks_in_class")) + _phase_lines(_bands(p)),
                phases=phases_from(_bands(p)),
                materials=as_list(p.get("materials")),
                teacher_notes=as_list(p.get("teacher_notes")),
                homework=_homework_text(p.get("homework")),
                meta={"pedagogical_methods": p.get("pedagogical_methods", {}),
                      "materials": p.get("materials", ""),
                      "spines_taught": spines,
                      "duration_minutes": p.get("period_duration_minutes")},
            ))

        # ── Singleton-section collapse (2026-07-09) ─────────────────────────────
        # English chapters are now SPLIT into their constituent sections — each
        # saved plan covers exactly one section, so a lone section Group is a
        # redundant wrapper level. Collapse it: spines become the top-level axis.
        # Multi-section plans (older, pre-split saves) keep the full nesting —
        # structure-driven, never a special case downstream.
        if len(sections) == 1:
            return LessonPlanView(
                subject="english", grade=grade,
                chapter_number=chapter.get("chapter_number", 0),
                chapter_title=chapter.get("chapter_title", ""),
                total_periods=len(periods), groups=sections[0].children,
            )

        return LessonPlanView(
            subject="english", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            total_periods=len(periods), groups=sections,
        )

    def assessment_to_view(self, raw: Union[Dict[str, Any], list], *, grade, chapter,
                           link_context: Dict[str, Any] = None) -> AssessmentView:
        # Rule 7 — TWO-key period-field join: the item carries (source_section_id, source_spine);
        # match it to a period where period.section_id == source_section_id AND source_spine is in
        # period.spines_taught[]. LO comes off the item's own source_lo. The join, the N-to-N
        # pairing and the section-wide fallback all live in `cell_resolver` above — ONE copy,
        # shared with `genon_assessment`, so the screen and the served file can never disagree
        # about which sitting an item belongs to (S11, 2026-08-12).
        ctx = link_context or {}
        spine_groups = raw.get("assessment_items", raw) if isinstance(raw, dict) else raw
        resolve = cell_resolver(ctx.get("periods", []) or [], spine_groups)

        groups: List[AssessmentGroup] = []
        for sg in spine_groups or []:
            g = AssessmentGroup(
                type="spine",
                label=sg.get("spine_title") or sg.get("spine_code", ""),
                meta={"spine_code": sg.get("spine_code", "")},
            )
            for it in sg.get("items", []):
                options, answer = normalize_options(it.get("options"))
                lo = it.get("source_lo", "")
                meta = {"source_section_id": it.get("source_section_id", ""),
                        "source_section_title": it.get("source_section_title", ""),
                        "source_spine": it.get("source_spine", ""),
                        "transcript_ref": it.get("transcript_ref", ""),
                        "id": it.get("id", "")}
                # Platform stamp first, the cell resolution as the fallback for an un-served
                # plan (ARV-D-064). `resolve` is called either way, so its pairing counter
                # advances and a stamped item does not shift its siblings.
                resolved = resolve(it)
                linked = platform_anchor(it) or resolved
                stamp(meta, linked, lo)
                g.items.append(AssessmentItem(
                    prompt=it.get("item_stem", ""),
                    item_type=it.get("question_type", ""),
                    options=options,
                    answer=answer,
                    teacher_guide=as_list(it.get("teacher_guide")),
                    implied_lo=lo,
                    visual_stimulus=classify_stimulus(it.get("visual_stimulus", "")),
                    meta=meta,
                    normalized=from_english(it, meta),  # the §2 uniform contract (3b reads this)
                ))
            groups.append(g)
        return AssessmentView(
            subject="english", grade=grade,
            chapter_number=chapter.get("chapter_number", 0),
            chapter_title=chapter.get("chapter_title", ""),
            groups=groups,
        )

    # ── genon: the carrier seam (aruvi_core/genon/carriers.py) ───────────────────
    def genon_has_section_axis(self, grade) -> bool:
        """Yes — but the "section" is the (section × spine) CELL, not a textbook section.

        The platform default, returned explicitly because the fact is easy to get wrong here.
        Post-split every english chapter is ONE main_section, so `section_id` alone is a
        constant and looks like no axis at all; what varies, strictly in the textbook's own
        on-page order and never re-sequenced (Rule 1), is the SPINE. Cells are therefore a
        real, ordered, first-visit axis and a prefix of a canonical is a valid plan — which
        is what keeps this stage at UNIT granularity rather than joining science·middle's
        plan-granularity exception. Flipping this to False would tell the engine these
        chapters have no sections and silently disable the arithmetic their serve depends on.
        """
        return True

    def genon_unit_anchor(self, period, grade=None):
        """This unit's cell anchor, built from the two fields THIS constitution defines.

        `section_id` + `spines_taught[]` → "A|reading_for_comprehension", and a unit teaching
        two adjacent spines reads "A|listening / A|speaking" — the same multi-section join the
        token stages use. Read VERBATIM from the authored fields and built by the SAME
        expression `carriers.period_section_codes` uses, so the anchor a unit reports and the
        code its items join through are equal by construction rather than by agreement.

        Branching is on the PERIOD's shape, not on `stage_for(grade)`: this is called from
        `compile.py`, where the grade comes off the enclosing plan and can be absent. All
        three english stages carry the same two fields, so there is nothing to branch on
        anyway.

        A closing unit that revisits several cells without teaching one returns its cells
        joined, exactly as authored; `carriers.is_synthesis` is what keeps such a unit out of
        the item index, not this method.
        """
        spines = [str(sp or "").strip() for sp in (period.get("spines_taught") or [])]
        sid = str(period.get("section_id") or "").strip()
        seen: List[str] = []
        for sp in spines:
            code = f"{sid}|{sp}"
            if sp and code not in seen:
                seen.append(code)
        return _ANCHOR_JOINER.join(seen) or None

    def genon_anchor_field_present(self, grade) -> bool:
        """No — at any english stage. `grep -c section_anchor` is 0 in all three english LP
        constitutions, which is why `genon_unit_anchor` above exists.

        WHAT IT CHANGES: `variant_plans.top_brief_for` asks this before it writes the standard
        canonical's closing-unit mandate. Where the field exists the mandate is the reserved
        token `synthesis` in it; here there is no field to put a token in, so the mandate is
        the explicit `"synthesis": true` boolean — the carrier science·middle and maths·middle
        already use. Without it the brief would ask an english generation, at metered STEP 1,
        for a field its constitution never defines, and the certifier's synthesis gate would
        then find no closing unit in the library it had already paid for.

        NOT a licence to emit `section_anchor`: the founder ruling of 2026-08-10 stands —
        nothing new may be added to a constitution to feed the serve engine. This reports the
        constitution as it is; it never asks it to change.
        """
        return False

    def genon_item_anchor_family(self, grade) -> str:
        """The 8-rule table's family column (base.py): row 7, the PERIOD-FIELD family, at all
        three stages. Not `handoff` — english's `coverage_handoff` carries no unit numbers at
        all, so there is nothing to bridge through; the cell code IS the join."""
        return "period_field"

    def genon_assessment(self, result: Dict[str, Any]) -> List[Dict[str, Any]]:
        """The genon door onto this subject's row of the verified 8-rule table.

        Nothing is decided here. `assessment_to_view` above already runs row 7 for the app;
        genon needs the SAME rule applied to the RAW item dicts (options, `is_correct`, guide,
        `visual_stimulus` intact — served files and exports read them), where
        `assessment_to_view` returns display objects. So this method restates the row and
        delegates to the one resolver both paths share.

          • ROW 7, the PERIOD-FIELD family, landed 2026-08-12 (S11) and the first row in the
            table whose join key is a PAIR: items are nested inside SPINE groups
            (`[{spine_code, spine_title, items:[…]}, …]`), each leaf carrying
            `source_section_id` + `source_spine`, and the join is that pair against the
            PERIOD's own `section_id` + `spines_taught[]`. There is no `coverage_handoff` in
            the path. The LO exists but is carried ON the item (`source_lo`), so it needs no
            bridge either.

        WHY THIS DELEGATES TO `cell_resolver` AND NOT TO `items_by_period_field`. The family
        helper joins one code against one period field and anchors at the group's last unit.
        Run on english that would be wrong twice over: it cannot express a composite key, and
        it would undo the N-to-N pairing (2026-07-11) that keeps two items sharing a cell on
        their own units — collapsing, say, both Vocabulary/Grammar items onto the last VocGram
        unit, which is precisely the display defect that pairing was written to fix. The
        anchoring RULE — a cell taught across several units anchors at the LAST of them
        (founder 2026-08-05) — still comes from `carriers`, via `items_with_units`; only the
        resolution is the plugin's, and it is the app's own.

        Stage is not read: this method receives only `result`, and the grade lives on the
        enclosing saved PLAN, so a grade read here is `None` on the very call the carrier
        makes (the S4 trap). It does not matter — all three english stages are row 7 on the
        same two period fields, and the spine SET is the only thing that differs, which the
        resolver reads from the data rather than assuming.
        """
        from ...genon.carriers import items_with_units

        raw = result.get("assessment_items")
        spine_groups = raw.get("assessment_items", raw) if isinstance(raw, dict) else raw
        if not isinstance(spine_groups, list):
            spine_groups = []
        periods = ((result.get("lesson_plan") or {}).get("periods")
                   if isinstance(result.get("lesson_plan"), dict) else None)
        if not isinstance(periods, list):
            periods = result.get("periods") if isinstance(result.get("periods"), list) else []
        resolve = cell_resolver(periods, spine_groups)
        flat = [it for sg in spine_groups if isinstance(sg, dict)
                for it in (sg.get("items") or []) if isinstance(it, dict)]
        return items_with_units(flat, lambda n, it: resolve(it))
