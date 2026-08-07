"""Genon: annotate master_plan.json with a per-chapter CANONICAL PLAN — v2.0 (2026-08-03).

v2.0 (architecture §0) RETIRES the reverse-deduction solver, sigma, and the mandated
closing spans. The pilot proved the mandate wrong at its root (ARV-D-025): a compact's
mandated closing synthesis imported the assumption that the BORROWING plan's class had
the lending plan's own priors for those sections — jumpiness by construction. Canonicals
are now authored FREE at counts fixed by pure arithmetic (equal dispersion over
[floor, standard], master_plan.py `canonical_periods`); the ONE surviving mandate is the
standard canonical's closing whole-chapter synthesis, `section_anchor` exactly the
reserved token `synthesis`. The serve engine picks slot X from first-exposure units
(serve.py e12, §0.4) — safety comes from the RIGHT PICK, not from a mandate on the lender.

This script's two jobs:
  * annotate — write each chapter row's `canonical_plan` {counts, provisional, basis,
    registry_sections, authored} into master_plan.json (idempotent; drops any stale
    v1.x `variant_plan`). provisional=True until the standard canonical is on disk.
  * briefs — compose the standard brief (self-containment + the synthesis-anchor
    mandate) and the compact briefs (free authoring: registry discipline + total
    coverage, NO closing mandate).

Re-run after any canonical is authored/regenerated or the floor policy changes:
    python3 genon/variant_plans.py
    python3 genon/variant_plans.py brief <subject> <CLASS> <ch>
"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from aruvi_core.genon import compile_stream                      # noqa: E402
from aruvi_core.genon.serve import section_registry              # noqa: E402

MP = os.path.join(ROOT, "data/content/allocation_norms/master_plan.json")
SAVED = os.path.join(ROOT, "data/content/saved_plans")

GRADE_KEY = {"III": "iii", "IV": "iv", "V": "v", "VI": "vi", "VII": "vii",
             "VIII": "viii", "IX": "ix", "X": "x"}


def canonical_counts(a, c):
    """Equal dispersion over [floor, standard] — keep in lockstep with
    genon/master_plan.py canonical_periods() (that script can't be imported:
    it runs its workbook pass on import). Rows written by master_plan.py
    v2.0 already carry `canonical_periods`; this is the fallback."""
    a, c = int(a), int(c)
    if c >= a - 1:
        return [a]
    if a - c < 4:
        return [a, c]
    return [a, (a + c + 1) // 2, c]


def library_paths(subject, klass, chapter):
    d = os.path.join(SAVED, subject, GRADE_KEY.get(klass, klass.lower()))
    ch = int(chapter)
    return (os.path.join(d, f"ch_{ch:02d}_canonical.json"),
            lambda k: os.path.join(d, f"ch_{ch:02d}_canonical_p{k:02d}.json"))


def standard_registry(subject, klass, chapter):
    """The chapter's section registry from the AUTHORED standard canonical
    (the synthesis token is excluded by section_registry itself). None when
    the standard is not on disk or does not compile."""
    top_path, _ = library_paths(subject, klass, chapter)
    if not os.path.isfile(top_path):
        return None
    try:
        return section_registry(compile_stream(json.load(open(top_path))))
    except Exception:                                # noqa: BLE001
        return None


# ── briefs ────────────────────────────────────────────────────────────────────

def _serving_block():
    """The serving facts every canonical must be authored against — identical
    for the standard and the compacts, because under §0.4 ANY unit that
    first-deals a section may be borrowed as another plan's closing sitting."""
    return [
        "- ITS UNITS ARE SERVED WHOLE AND IN PARTS. A teacher whose budget differs "
        "receives another plan's first X-1 units followed by ONE unit borrowed from "
        "this plan — the unit that FIRST introduces the section her class has reached. "
        "So ANY unit of this plan may be somebody's last sitting, met by a class that "
        "never had the units before it.",
        "- Therefore every unit CLOSES ON ITS OWN GROUND: it names no other unit, "
        "promises nothing that follows it, and never claims the chapter has been "
        "covered. Where continuity helps, name the CONTENT already taught — the idea, "
        "text, method or phenomenon — never a unit's position or existence.",
        "- MATERIALS, OPENING MOVES AND HOMEWORK ARE PER-UNIT. No unit may require "
        "that another unit was taught, or that its homework was set, in order to run.",
    ]


def _is_plan_granularity(subject, klass):
    """Does this subject·stage serve at PLAN granularity? Asked of the subject plugin,
    exactly as the engine asks it — never a name check here either."""
    try:
        sys.path.insert(0, ROOT)
        from aruvi_core.genon.carriers import serve_granularity
        return serve_granularity(subject, klass) == "plan"
    except Exception:                                       # noqa: BLE001
        return False


def _arc_brief(count, dur, chapter, standard):
    """The brief for a PLAN-GRANULARITY stage (science·middle;
    docs/science_middle_stage_serve.md). Two things make it different from the
    section-axis briefs, and both follow from the same fact — the plan's axis is the
    chapter's cognitive progression arc, derived fresh from the summary at generation
    time, not the textbook's section list.

    1. THERE IS NO REGISTRY, and none is supplied. Arcs may differ freely between this
       chapter's own canonicals in stage count, labels and structure; nothing is shared
       and nothing is ever borrowed between them (founder, 2026-08-07). Each canonical
       is authored as if it were the only plan of this chapter.
    2. EVERY CANONICAL IS COMPLETE BY CONSTRUCTION. It is not "cover all sections" here
       — the constitution's own Rules 1, 2 and 5 already require every arc stage to be
       taught and the final stage to reach the dissolution test's operation. The brief
       only has to say that the plan will never be cut, so it must be whole at this
       count."""
    lines = [
        f"CANONICAL BRIEF — {count} periods (platform-computed; binding)",
        "",
        f"- This is a COMPLETE, self-sufficient lesson plan for the whole chapter at "
        f"{count} units x {dur} minutes (period_schedule: exactly one row "
        f"{{{dur}, {count}}}). It is NOT a compression, summary or edit of any other "
        f"plan of this chapter — author it from the chapter summary as if it were the "
        f"only plan, deriving its cognitive progression arc afresh at this length.",
        "- THE ARC IS YOURS AT THIS COUNT. Stage count, stage labels and the shape of "
        "the progression are decided by this chapter's content AT THIS BUDGET; they "
        "need not match any other plan of this chapter, and nothing is ever borrowed "
        "between them. The one fixed point is the terminus: the final stage must "
        "correspond to the operation named in the dissolution test sentence.",
        "- THE PLAN IS SERVED WHOLE OR NOT AT ALL. This platform never cuts a plan of "
        "this stage mid-arc, so every stage you open must be completed inside these "
        f"{count} units. There is no coverage note and no budget shortfall available: "
        "an arc that does not close at this count is an authoring failure.",
        "- MATERIALS, OPENING MOVES AND HOMEWORK ARE PER-UNIT. No unit may require "
        "that another unit's homework was set in order to run. Forward and backward "
        "references BETWEEN THE UNITS OF THIS PLAN are welcome — they are always "
        "served together (LP constitution v2.2, THE SELF-CONTAINED REGISTER).",
        "- NO CLOCK QUANTITY and NO CALENDAR TIME in any band or note: the platform "
        "scales band minutes to the sitting that carries them, and keeps no calendar.",
    ]
    if standard:
        lines += [
            f"- THE SYNTHESIS MANDATE (this plan alone carries it): unit {count}, the "
            "final unit, is a WHOLE-CHAPTER SYNTHESIS and carries the field "
            '`\"synthesis\": true` on its period object (this stage has no '
            "section_anchor field, so the boolean is how the platform recognises it). "
            "It draws the entire chapter together as a real unit-arc.",
            "- THAT UNIT TRAVELS. It is the ONE unit of this chapter the platform may "
            "serve into a companion canonical's plan — a class that covered this same "
            "chapter through a DIFFERENT arc, with different stages and different "
            "activities. So it may assume the chapter's CONTENT has been taught and "
            "that the class has reached the dissolution test's operation, and it may "
            "name concepts. It must NOT assume any particular earlier stage, activity, "
            "reading, discussion, homework or material actually happened, and must not "
            "name a stage label.",
            f"- COVERAGE COMPLETES BEFORE THE SYNTHESIS: the full arc is taught across "
            f"units 1..{count - 1}.",
            f"- Save as: ch_{int(chapter):02d}_canonical.json",
        ]
    else:
        lines += [
            "- NO SYNTHESIS UNIT. The closing whole-chapter synthesis is reserved to "
            "this chapter's STANDARD canonical; never emit `\"synthesis\": true` here. "
            "End the plan the way this count teaches best.",
            f"- The assessment for this plan is generated from THIS plan's "
            f"coverage_handoff in the normal way; it references no other plan of this "
            f"chapter.",
            f"- Save as: ch_{int(chapter):02d}_canonical_p{count:02d}.json",
        ]
    return "\n".join(lines) + "\n"


def top_brief_for(subject, klass, chapter):
    """The STANDARD canonical's brief — platform-composed, prepended to the
    generation prompt (v2.0: gains the synthesis-anchor mandate, §0.3)."""
    mp = json.load(open(MP))
    combo = mp["combos"][f"{subject}|{klass}"]
    row = next(c for c in combo["chapters"] if c["chapter"] == int(chapter))
    dur = combo["standard_duration_minutes"]
    count = int(row["recommended_periods"])
    if _is_plan_granularity(subject, klass):
        return _arc_brief(count, dur, chapter, standard=True)
    return "\n".join([
        f"STANDARD CANONICAL BRIEF — {count} periods (platform-computed; binding)",
        "",
        f"- This is the chapter's fullest plan: {count} units x {dur} minutes "
        f"(period_schedule: exactly one row {{{dur}, {count}}}).",
        *_serving_block(),
        f"- THE SYNTHESIS MANDATE (this plan alone carries it): unit {count}, the "
        "final unit, is a WHOLE-CHAPTER SYNTHESIS and its section_anchor is exactly "
        "the single word: synthesis (the reserved token — NOT a section name, no "
        "joining). It draws the entire chapter together as a real unit-arc. It may "
        "assume every SECTION'S CONTENT has been taught, and may connect back to "
        "concepts BY NAME — but it must NOT assume any particular earlier activity, "
        "reading, discussion, homework or material actually happened: it will be "
        "served to classes that covered the same sections through DIFFERENT units.",
        f"- COVERAGE COMPLETES BEFORE THE SYNTHESIS: all registry sections "
        f"first-appear across units 1..{count - 1}. No other unit may use the "
        "synthesis token.",
        f"- Save as: ch_{int(chapter):02d}_canonical.json",
    ]) + "\n"


def briefs_for(subject, klass, chapter):
    """{compact_count: brief_text} for the chapter's compact canonicals —
    FREE authoring (v2.0): registry discipline + total coverage, no closing
    mandate, no synthesis token. Raises SystemExit when the standard canonical
    is missing or the row is not annotated."""
    mp = json.load(open(MP))
    combo = mp["combos"][f"{subject}|{klass}"]
    row = next(c for c in combo["chapters"] if c["chapter"] == int(chapter))
    plan = row.get("canonical_plan")
    if not plan or plan.get("provisional"):
        raise SystemExit("Row is provisional — author and certify the standard "
                         "canonical, run this script's annotate pass, then ask again.")
    dur = combo["standard_duration_minutes"]
    if _is_plan_granularity(subject, klass):
        # No registry is read, because there is none to read: this stage's canonicals
        # share no axis, so a compact needs nothing at all from the standard.
        return {k: _arc_brief(k, dur, chapter, standard=False)
                for k in plan["counts"][1:]}, plan
    reg = standard_registry(subject, klass, chapter)
    if reg is None:
        raise SystemExit("No standard canonical on disk — author it first; if the row "
                         "says finalized it is stale: re-run the annotate pass.")
    out = {}
    for k in plan["counts"][1:]:
        lines = [
            f"CANONICAL BRIEF — {k} periods (platform-computed; binding)",
            "",
            f"- This is a COMPLETE, self-sufficient lesson plan for the whole "
            f"chapter at {k} periods x {dur} minutes (period_schedule: exactly "
            f"one row {{{dur}, {k}}}). It is NOT a compression, summary, or "
            f"edit of any other plan of this chapter — author it from the "
            f"chapter summary as if it were the only plan.",
            "- SECTION REGISTRY (verbatim; the chapter's ordered sections):",
        ]
        lines += [f"    {i}. {a}" for i, a in enumerate(reg, 1)]
        lines += [
            "  Every unit's section_anchor MUST be drawn verbatim from this "
            "list (a multi-section unit joins its sections with \" / \" in "
            "list order). Sections must FIRST APPEAR in registry order; a "
            "later unit may revisit earlier sections. The token `synthesis` "
            "is RESERVED to the chapter's standard canonical — never use it here.",
            f"- COVERAGE IS TOTAL: all {len(reg)} registry sections must "
            f"first-appear across this plan's {k} units — merge ADJACENT "
            f"sections into shared units wherever the count demands it (the "
            f"smaller the count, the more condensing this takes; that judgment "
            f"is yours, made at authoring time). NO section may be omitted, and "
            f"section_coverage_note is NOT available to a canonical: a coverage "
            f"gap is an authoring failure, never a budget note.",
            *_serving_block(),
            "- THERE IS NO MANDATED CLOSING SHAPE. End the plan the way this "
            "count teaches best. A final unit that condenses the last adjacent "
            "sections is welcome when the count demands it; a trailing unit that "
            "only revisits sections an earlier unit already taught spends a "
            "period without advancing coverage — at this count that is almost "
            "never affordable.",
            "- The assessment for this plan is generated from THIS plan's "
            "coverage_handoff in the normal way; it references no other "
            "plan of this chapter.",
            f"- Save as: ch_{int(chapter):02d}_canonical_p{k:02d}.json",
        ]
        out[k] = "\n".join(lines) + "\n"
    return out, plan


def print_briefs(subject, klass, chapter):
    """`python3 genon/variant_plans.py brief <subject> <CLASS> <ch>`."""
    briefs, plan = briefs_for(subject, klass, chapter)
    print(f"# Canonical briefs · {subject} {klass} ch {chapter} · "
          f"library {plan['counts']}\n")
    for k, text in briefs.items():
        print("=" * 72)
        print(text)


# ── annotate ─────────────────────────────────────────────────────────────────

def main():
    mp = json.load(open(MP))
    n_real = n_prov = 0
    for key, combo in mp["combos"].items():
        subject, klass = key.split("|")
        for ch in combo["chapters"]:
            a = int(ch["recommended_periods"])
            c = int(ch["floor_periods_at_standard"])
            counts = list(ch.get("canonical_periods") or canonical_counts(a, c))
            reg = standard_registry(subject, klass, ch["chapter"])
            top_path, p_path = library_paths(subject, klass, ch["chapter"])
            authored = ([counts[0]] if os.path.isfile(top_path) else []) + \
                       [k for k in counts[1:] if os.path.isfile(p_path(k))]
            provisional = reg is None
            n_prov += provisional
            n_real += not provisional
            ch.pop("variant_plan", None)            # stale v1.x solver annotation
            ch["canonical_plan"] = {
                "counts": counts,                    # standard first, descending
                "provisional": provisional,
                "basis": "arithmetic" if provisional else "authored_standard",
                "registry_sections": None if reg is None else len(reg),
                "authored": authored,
            }
    mp["_meta"].pop("variant_plans", None)
    mp["_meta"]["canonical_plans"] = (
        "each chapter carries canonical_plan (v2.0 2026-08-03, genon/variant_plans.py): "
        "the canonical counts by equal dispersion over [floor, standard] — no solver, "
        "no sigma, no mandated closing spans (architecture §0). Canonicals are authored "
        "FREE; the standard alone closes with the mandated whole-chapter synthesis "
        "(section_anchor = the reserved token `synthesis`). provisional=true until the "
        "standard canonical is on disk — re-run this script after each authoring pass.")
    json.dump(mp, open(MP, "w"), ensure_ascii=False, indent=2)
    print(f"canonical plans written: {n_real} on authored standards, {n_prov} provisional")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "brief":
        print_briefs(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        main()
