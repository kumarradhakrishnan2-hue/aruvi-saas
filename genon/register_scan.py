#!/usr/bin/env python3
"""register_scan.py — the deterministic gate for THE SELF-CONTAINED REGISTER (v1.0, 2026-08-02).

WHY THIS EXISTS. The register is stated in every LP constitution as a prohibition, and the
SS·IX ch 3 pilot proved a prohibition is not enforcement: the top canonical, authored under
v1.10 which bans it in terms, carried NINE forward-reference/completion breaches (docs/testing.md
C3, defects ARV-D-011..013). This is the failure family the MCQ probe already documented
(rollout brief A9): asking the model to MAINTAIN a constraint across 25k tokens is not the same
as asking it to recognise one sentence. So the constraint moves where it can be enforced — into
code that runs at build time, before a plan can certify.

WHAT IT CHECKS — the v1.10 register's three bans, plus internal-ID leakage:
  forward     · points at a unit that follows, or promises what it will do
  completion  · claims the chapter (or all its sections) has been covered
  calendar    · names a SCHEDULE in days/weeks (tomorrow, next class, this week) — Aruvi keeps
                no calendar and sittings do not map to days. NOTE "today"/"yesterday" are
                ADVISORY, not bans: in a weather chapter "Will it rain today?" and "today's
                newspaper" are content, self-consistent whenever the unit is taught. A gate that
                fails on those would be switched off within a week, so a human judges them.
  clock       · states a quantity of minutes; proportional scaling falsifies it silently
  ids         · competency codes (C-4.2) in teacher-facing text (Rule 10 P bans them in notes;
                Rule 13 makes bands the core teacher-facing product, so a leak there is worse)
  positional  · ADVISORY, not a ban: v1.10 legalised backward references. Flagged only because
                Rule 13 P3 keeps unit-to-unit linking in teacher_notes, and "the previous unit"
                is positional where content-naming was available.

WHAT IT DOES NOT CATCH, stated plainly: paraphrase. "Later in this chapter we shall meet…"
sails through. The scanner carries the floor; a sampled LLM audit at batch level is what finds
new phrasings, and every one it finds should be added to PATTERNS here with a dated note.

Scanned fields are exactly the teacher-facing ones, ACROSS ALL ELEVEN SUBJECT-STAGE SHAPES
(checked 2026-08-02 against every LP constitution): activity_title · teacher_notes, or
`teacher_facilitation_note` where TWAU-preparatory names it that · the band array, which is
`time_bands[]` in the five converted constitutions and still `phases[]` in the six awaiting P3,
with its text under `activity` or `description` · homework[]. section_context and LO rows are
internal and not scanned.

Reading only one shape would be worse than useless — a Group B plan would scan clean because
nothing was read. Every shape is tried, and `scanned_fields()` reports what was actually found.

Vocabulary note: all eleven constitutions name the atomic chunk a "unit" in teacher-facing prose
and reserve "period" for schema/scheduling, so the families below are subject-neutral. Several
give "the previous unit" as a LEGITIMATE cross-reference, which is why backward-positional
phrasing is advisory here rather than a ban.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from aruvi_core.genon.carriers import is_synthesis as _is_synth   # noqa: E402

# (family, is_ban, compiled pattern). Order is report order.
PATTERNS = [
    # ── COMPLETION-BY-PARAPHRASE — added 2026-08-10 (S7 · C7, ARV-D-100).
    # The forward family is literal-phrase based, so it caught nothing in ch 7 while a real
    # ban-2 breach sat in the top: U11's "connecting the geometric intuition BUILT THROUGHOUT
    # THE CHAPTER". U11 is not the synthesis unit, and any unit may be a teacher's last
    # sitting or a borrowed Xth unit, so a class meeting it as first exposure has built no
    # such intuition. Second occurrence of the scanner-gap class after ARV-D-026.
    #
    # EXEMPT ON THE SYNTHESIS UNIT (see the ban calculation in scan_plan). The closing
    # whole-chapter synthesis is licensed by the platform brief to assume the chapter's
    # CONTENT has been taught, so "warming up all five sections' ideas" is correct there and
    # a gate that failed it would be switched off within a week. Deliberately NOT added:
    # references pointing OUTSIDE the chapter ("explored further in a later chapter") — true
    # wherever the plan ends, and therefore not a ban-2 breach at all.
    ("completion", True, re.compile(
        r"\b(built|developed|established|learned|covered)\s+(up\s+)?(throughout|across)\s+(the|this)\s+chapter\b"
        r"|\bso far in (the|this) chapter\b"
        r"|\bnow that (you|we|students|they) have (covered|met|seen|learned|built)\b"
        r"|\ball (five|six|seven|eight|nine|ten|of the) sections\b", re.I)),
    ("forward", True, re.compile(r"\bthe (next|following) (unit|lesson|class|session)\b", re.I)),
    ("forward", True, re.compile(r"\bnext unit\b", re.I)),
    ("forward", True, re.compile(r"\blater (unit|units|lessons)\b", re.I)),
    ("forward", True, re.compile(r"\bas we (will|shall) see\b", re.I)),
    ("forward", True, re.compile(r"\bwhat is to come\b", re.I)),
    ("forward", True, re.compile(r"\b(connecting|pointing|looking) (forward|ahead)\b", re.I)),
    ("forward", True, re.compile(r"\bunit (will|would) (show|develop|examine|cover|introduce)\b", re.I)),
    ("forward", True, re.compile(r"\b(develops|develop) (further|mechanistically)\b", re.I)),
    ("forward", True, re.compile(r"\bthread (to pick up|that .{0,40} develops)\b", re.I)),
    ("forward", True, re.compile(r"\bpreviewing\b|\bforeshadow\w*\b", re.I)),
    ("forward", True, re.compile(r"\bfrom the next\b|\bthis unit from the next\b", re.I)),
    # ── added 2026-08-07 (S6·C7), AFTER a false start worth recording ──────────────────
    # The C7(c) subjective sweep turned up seven paraphrases the word list could not see, and
    # I first added all seven as BANS. Six were wrong, and the certified corpus said so
    # immediately: 26 ban hits appeared on SS·IX and science·IX, libraries that had certified
    # clean. The bulk of them were "having established …" — which is not a breach at all but
    # the phrasing the science·secondary register block ENDORSES by name as the model
    # continuity link. v1.10 LEGALISED backward reference; ban 2 is FORWARD reference and
    # COMPLETION claims only, and I had treated every backward paraphrase as a breach.
    #   Two survive, for reasons that are about direction, not phrasing:
    ("forward", True, re.compile(r"\b(you|students|they) will have (built|made|drawn|created|seen|covered)\b", re.I)),
    # ARTEFACT DEPENDENCE — ADVISORY, a different rule from the register. The variant brief
    # requires per-unit independence ("no unit may require that another unit was taught, or
    # that its homework was set, in order to run"), and a unit that reaches for "their earlier
    # chart" cannot be run without one — the sharpest form of the dependency, because it is
    # not a reference but a prerequisite. Advisory rather than ban: within a plan that is
    # always served whole (a plan-granularity stage) it is perfectly legal, so a human decides.
    ("artefact", False, re.compile(r"\btheir (earlier|previous) (chart|table|diagram|map|list|notes|model)\b", re.I)),
    ("artefact", False, re.compile(r"\b(the|that) \w+ (they|students) already (made|built|drew|created)\b", re.I)),
    # ── ARTEFACT DEPENDENCE, second pass — added 2026-08-12 (S5 · C7, ARV-D-119) ───────
    # The two patterns above look for a POSSESSIVE reference in prose ("their earlier chart").
    # TWAU V ch 5's breach used neither shape: it wrote the dependency as a MATERIALS ENTRY,
    # in the passive, with no owner and no unit named —
    #     materials:    ["Group posters and charts PREPARED PREVIOUSLY"]
    #     visual_aids:  "Group-created posters and charts from all states represented"
    #     band 0-5:     "Groups SET UP THEIR POSTERS or displays around the classroom."
    # A materials list is a shopping list, and a shopping list that includes an item only a
    # previous sitting could have produced is the sharpest form of the dependency: not a
    # reference to another unit but a PREREQUISITE on one. `_fields` now reads `materials[]`
    # and `visual_aids` (see the dated note there) so these patterns have somewhere to fire.
    #
    # Kept ADVISORY, like the two above and for the same reason: on a plan-granularity stage
    # every unit is served with every other, so the dependency is legal there and a human
    # decides. The place it is now FORBIDDEN outright is the platform brief
    # (`variant_plans.top_brief_for` / `briefs_for`, 2026-08-12), which is where a rule about
    # serving belongs; this is the detector, not the rule.
    ("artefact", False, re.compile(
        r"\b(prepared|made|built|drawn|created|collected|written)\s+"
        r"(previously|earlier|beforehand|in advance|last time)\b", re.I)),
    ("artefact", False, re.compile(
        r"\b(set up|bring out|hand back|redistribute|display)\s+their\s+"
        r"(posters?|charts?|models?|displays?|drafts?|collections?)\b", re.I)),
    ("artefact", False, re.compile(
        r"\bfrom the (earlier|previous|last) (sitting|unit|session|lesson)\b", re.I)),
    # ── ARTEFACT DEPENDENCE, third pass — added 2026-08-12 (S11 · C7, from ARV-D-132) ─────
    # english·IX ch 7's mandated SYNTHESIS unit — the one the engine lends to other plans —
    # carried the dependency in a shape none of the five patterns above can see:
    #     materials: ["Textbook pp.97–125", "STUDENTS' DRAFT ARTICLE (notebooks or draft sheets)"]
    #     band 30-50: "Students COMPLETE THE DRAFT ARTICLE 'Our Inspiring Elderly' (Paragraphs
    #                  3 and 4 …)"          [the draft is begun in U15, twelve sittings earlier]
    # There is no time word ("previously", "earlier"), no named unit, and no "their … chart".
    # The dependency is carried by a POSSESSIVE OWNER plus a PRODUCED artefact: a class cannot
    # arrive holding "students' draft article" unless an earlier sitting produced it. That is
    # the same prerequisite shape as S5's "posters prepared previously", stated in the one way
    # the earlier patterns do not cover.
    #
    # SCOPED AWAY FROM STANDING CLASSROOM ITEMS on purpose. "their notebooks", "students'
    # exercise books", "draft paper" and "writing paper" are things every class already has and
    # must never fire — so the artefact noun list is PRODUCED objects only, and the possessive
    # is required. Measured on the whole certified corpus when added: 2 hits, both the english
    # synthesis unit and its served copies; zero elsewhere.
    #
    # ADVISORY, like every other pattern in this family and for one more reason of its own: the
    # rule it detects lives in the platform BRIEF, not in any constitution, and a ban here would
    # fail certification against a rule no constitution states. C7 and the human gate rule on it.
    # MEASURED BEFORE IT WAS TRUSTED, and the first cut was thrown away. A possessive +
    # produced-artefact pattern applied to ALL fields fires 111 times across the 131 certified
    # and served files on disk — almost all of them "students make their poster … display their
    # posters" INSIDE ONE unit, which the brief expressly licenses ("put BOTH acts inside ONE
    # unit"). That is a gate nobody would keep. Two things separate the real defect from the
    # noise, and both are in the shape rather than the words:
    #   1. the possessive appears in MATERIALS or VISUAL_AIDS — a shopping list naming an object
    #      only a previous sitting could have produced (field-scoped below, `_FIELD_SCOPED`);
    #   2. a COMPLETION verb governs a definite artefact — "complete the draft", "revise their
    #      article" — which presupposes the thing already exists.
    # Scoped that way the two patterns catch english ch 7's synthesis unit and its served copies
    # and NOTHING else in the corpus.
    ("artefact", False, re.compile(
        r"\b(students['’]|pupils['’]|their)\s+(?:\w+\s+){0,2}?"
        r"(draft|article|essay|poster|chart|model|display|collection|slide[- ]?show|"
        r"presentation)s?\b(?!\s+(paper|sheets?))", re.I)),
    ("artefact", False, re.compile(
        r"\b(complete|finish|revise|redraft|continue)\s+(the|their)\s+"
        r"(draft|article|essay|poster|model|collection)\b", re.I)),
    # ── added 2026-08-03 (ARV-D-026) — three forward phrasings that sailed through a clean run:
    # "the monsoon regime that will follow", "the interlinkage that the Monsoon unit will extend",
    # "explored in upcoming units". The second is the general shape: a NAMED unit plus a future
    # verb, which no earlier pattern covered because it never says "next".
    ("forward", True, re.compile(r"\bthat (will|would) follow\b|\bthat follows? later\b", re.I)),
    ("forward", True, re.compile(r"\bthe [\w'’-]+ (unit|lesson) will\b", re.I)),
    ("forward", True, re.compile(r"\bin upcoming (units|lessons|sections)\b|\bupcoming (unit|lesson)\b", re.I)),
    ("forward", True, re.compile(r"\bwill (extend|pick up|take up|carry (this|it) forward)\b", re.I)),
    # ── added 2026-08-03 (ARV-D-038, found at C8 by reading a served plan's LAST sitting) ──
    # "This bridges toward the climate change and Punjab floods sections that follow" is TRUE
    # in the canonical, where those sections do follow, and FALSE the moment a serve ends on
    # that unit. Every unit is a potential last sitting, so a closing band that points at what
    # comes next is a landmine for whichever request lands there.
    ("forward", True, re.compile(r"\bsections?\s+that\s+follows?\b", re.I)),
    ("forward", True, re.compile(r"\bbridges?\s+(toward|towards|to)\s+the\b", re.I)),
    ("completion", True, re.compile(r"\bhaving (worked through|covered|completed) (every|all|the whole)\b", re.I)),
    ("completion", True, re.compile(r"\bnow that (we|students|they) have (covered|completed)\b", re.I)),
    ("completion", True, re.compile(r"\bthe chapter is (now )?complete\b", re.I)),
    ("calendar", True, re.compile(r"\btomorrow\b", re.I)),
    ("calendar", True, re.compile(r"\b(this|next|last) (week|month)\b", re.I)),
    # "term" split out to ADVISORY, 2026-08-09. It was a ban, and it fired on maths·IX ch 4's
    # "identify the square root of the first term, the square root of the LAST TERM" — the term
    # of a polynomial, not the school calendar. Across mathematics that reading is the common
    # one by a wide margin, and a gate that fails a correct algebra band gets switched off, the
    # same argument the header already makes for today/yesterday. Still surfaced, so a genuine
    # "last term" in the academic sense is ruled on at C7 rather than ignored.
    ("calendar", False, re.compile(r"\b(this|next|last) term\b", re.I)),
    ("calendar", True, re.compile(r"\b(next|last) class\b", re.I)),
    ("calendar", False, re.compile(r"\b(today|yesterday)\b", re.I)),      # advisory — see header
    ("clock", True, re.compile(r"\bfor (two|three|four|five|six|seven|eight|nine|ten|fifteen|twenty|thirty|\d+) minutes\b", re.I)),
    # ── added 2026-08-03 (ARV-D-026, found by hand at C3 — four breaches passed a clean run) ──
    # The header promises that every new phrasing lands here with a dated note. These are those.
    # Ranged and hedged clock quantities: "for two to three minutes", "for about ten minutes".
    # The {0,20} window keeps it to the same clause, so "asks for the map … minutes later" in a
    # different sentence is not swept in.
    ("clock", True, re.compile(r"\bfor\b[^.;]{0,20}\bminutes\b", re.I)),
    ("clock", True, re.compile(r"\bthe remaining time\b|\bhalf the (session|period)\b", re.I)),
    # "half the class" is AMBIGUOUS and, in practice, almost never a clock quantity: it is how
    # every teacher describes a grouping ("half the class will be plants and animals, the other
    # half will be forest visitors" — TWAU iv ch03 role-play, 2026-08-12). Banning it would have
    # had a repair strike correct pedagogy to satisfy a pattern written for "half the session".
    # Advisory, so a genuine time use is still visible to a reader. Same treatment as "last
    # term" at S4 (v1.5): when a phrase is a homonym, the scanner reports and the human rules.
    ("clock", False, re.compile(r"\bhalf the class\b", re.I)),
    ("clock", True, re.compile(r"\bin the (first|last) \w+ minutes\b", re.I)),
    ("ids", True, re.compile(r"\(C-\d+\.\d+\)")),
    ("positional", False, re.compile(r"\b(previous|earlier|first|last) unit\b", re.I)),
]


NOTE_KEYS = ("teacher_notes", "teacher_facilitation_note")   # TWAU-prep names it the long way
BAND_KEYS = ("time_bands", "phases")                        # phases[] until P3 converts a stage
BAND_TEXT = ("activity", "description")                     # description[] is the phases-era key


def _fields(unit):
    """The teacher-facing strings of one unit, as (label, text) pairs — shape-agnostic."""
    yield "activity_title", str(unit.get("activity_title") or "")
    # ── MATERIALS AND VISUAL AIDS — added 2026-08-12 (S5 · C7, ARV-D-119) ──────────────
    # These were not scanned, and that is where the breach was. TWAU V ch 5's closing unit
    # named no other unit anywhere in its prose — it listed
    # `materials: ["Group posters and charts prepared previously"]` and
    # `visual_aids: "Group-created posters and charts from all states represented"`.
    # The dependency arrived through the PROPS, so a scanner reading only titles, notes and
    # bands reported 0 hits on a plan that could not be run as served.
    #
    # They are teacher-facing by definition — a materials list is the first thing a teacher
    # reads when deciding whether she can run the sitting — so they belong here on the same
    # ground as `homework[]`, which has always been scanned. Verified against every certified
    # library before landing: adding them introduces ZERO new BAN hits corpus-wide (the
    # discipline S6's note records, after six of its seven new patterns turned out wrong).
    mats = unit.get("materials")
    for i, m in enumerate(mats if isinstance(mats, list) else ([mats] if mats else [])):
        yield f"materials[{i}]", m if isinstance(m, str) else json.dumps(m, ensure_ascii=False)
    if unit.get("visual_aids"):
        yield "visual_aids", str(unit["visual_aids"])
    for k in NOTE_KEYS:
        if unit.get(k):
            yield k, str(unit[k])
    for bk in BAND_KEYS:
        for i, b in enumerate(unit.get(bk) or []):
            text = next((str(b[t]) for t in BAND_TEXT if b.get(t)), "")
            yield f"{bk}[{i}] {b.get('minutes','?')}", text
    for i, h in enumerate(unit.get("homework") or []):
        yield f"homework[{i}]", h if isinstance(h, str) else json.dumps(h, ensure_ascii=False)


def scanned_fields(plan: dict):
    """Which teacher-facing keys were actually found — so a silent miss is visible.
    A plan reporting 0 bans AND 0 band fields has not been scanned, it has been skipped."""
    periods = ((plan.get("result") or plan).get("lesson_plan") or {}).get("periods") or []
    seen = {}
    for u in periods:
        for label, text in _fields(u):
            key = label.split("[")[0]
            seen[key] = seen.get(key, 0) + (1 if text else 0)
    return seen


_QUOTED = re.compile(r"[\u2018\u2019\u201c\u201d\'\"]([^\u2018\u2019\u201c\u201d\'\"]{0,300}?)[\u2018\u2019\u201c\u201d\'\"]")


def _quoted_spans(text):
    """Character ranges inside quotation marks — specimen sentences, textbook prompts and
    the questions Rule 13 requires bands to state. A calendar word inside one is the
    chapter speaking, not the plan scheduling itself."""
    return [(m.start(1), m.end(1)) for m in _QUOTED.finditer(text)]


# FIELD-SCOPED PATTERNS (2026-08-12, S11 · C7). One pattern in the list above is precise in a
# materials list and noise everywhere else: a possessive + produced artefact is a PREREQUISITE
# when it appears in `materials` / `visual_aids` (a class cannot arrive holding it) and ordinary
# teaching prose when it appears in a band ("students display their posters" in the unit that
# made them). Rather than weaken the pattern until it catches nothing, it is scoped to the
# fields where the shape means what it says. Keyed by pattern object so the entry sits beside
# the pattern it governs and cannot drift onto another one.
_FIELD_SCOPED = {
    # the possessive + produced-artefact pattern (S11 · C7): materials-shaped fields only
    next(pat for fam, ban, pat in PATTERNS
         if fam == 'artefact' and "students['\u2019]" in pat.pattern):
        ('materials', 'visual_aids'),
}


def _scope_ok(pat, field: str) -> bool:
    allowed = _FIELD_SCOPED.get(pat)
    return True if allowed is None else any(field.startswith(f) for f in allowed)


def scan_plan(plan: dict):
    """-> list of hits {unit, field, family, ban, match, excerpt}. Empty ban list = clean.

    Two deliberate suppressions, both to keep the gate credible:
      * overlapping matches on one field collapse to the first (several patterns describe the
        same breach; reporting it three times trains people to skim);
      * a CALENDAR hit inside quotation marks drops to advisory (quoted chapter content)."""
    # WHICH BANS THIS STAGE ACTUALLY CARRIES (2026-08-07, S6). The register is not the
    # same three bans everywhere: science·middle's constitution (LP v2.2) carries a TWO-ban
    # cut, because its units are never served apart, so forward reference and completion
    # claims are true there. A scanner that enforces a rule the constitution does not have
    # fails good plans — it flagged 4 hits across ch 6's compacts, every one of them legal.
    # Asked of the subject plugin through the same seam compile.py and serve.py use.
    _r = plan.get("result") or plan
    try:
        from aruvi_core.genon.carriers import forward_reference_legal
        _fwd_ok = forward_reference_legal(plan.get("subject") or _r.get("subject"),
                                          plan.get("grade") or _r.get("grade"))
    except Exception:                                    # noqa: BLE001
        _fwd_ok = False                                  # unknown subject -> strict default
    periods = (_r.get("lesson_plan") or {}).get("periods") or []
    hits = []
    for u in periods:
        for field, text in _fields(u):
            quoted = _quoted_spans(text)
            taken = []
            for family, ban, pat in PATTERNS:
                if not _scope_ok(pat, field):
                    continue
                for m in pat.finditer(text):
                    if any(m.start() < e and s_ < m.end() for s_, e in taken):
                        continue                       # already reported as another pattern
                    taken.append((m.start(), m.end()))
                    in_quote = any(s_ <= m.start() and m.end() <= e for s_, e in quoted)
                    a, b = max(0, m.start() - 60), min(len(text), m.end() + 60)
                    hits.append({
                        "unit": u.get("period_number"), "field": field, "family": family,
                        # A forward hit on a stage whose register drops ban 2 is reported
                        # as ADVISORY, never suppressed: it stays visible to the human
                        # reader, it just does not fail a library that is obeying its own
                        # constitution.
                        # `completion` is exempt on the synthesis unit, which the brief
                        # licenses to assume the chapter's content has been taught.
                        "ban": ban and not (family == "calendar" and in_quote)
                                   and not (family in ("forward", "completion") and _fwd_ok)
                                   # `completion` IS ban 2, so it takes the SAME stage
                                   # exemption as `forward`. science·middle drops ban 2
                                   # entirely (its units are served only as a whole arc,
                                   # so a completion claim is true there) — without this
                                   # the new pattern failed CERTIFIED science·VIII ch 6
                                   # p08 on "built across the chapter". Found by running
                                   # the pattern corpus-wide before trusting it.
                                   and not (family == "completion" and _is_synth(u)),
                        "quoted": in_quote, "match": m.group(0),
                        "excerpt": ("…" if a else "") + text[a:b].strip() + ("…" if b < len(text) else ""),
                    })
    return hits


def scan_file(path):
    return scan_plan(json.loads(Path(path).read_text(encoding="utf-8")))


def report(hits, name=""):
    """Human-readable block; returns (n_bans, n_advisory)."""
    bans = [h for h in hits if h["ban"]]
    adv = [h for h in hits if not h["ban"]]
    if name:
        print(f"\n--- {name}: {len(bans)} ban hit(s), {len(adv)} advisory")
    for h in bans + adv:
        tag = h["family"].upper() if h["ban"] else h["family"] + " (advisory)"
        print(f"  U{h['unit']:<3} {h['field']:<22} [{tag}] {h['excerpt']}")
    return len(bans), len(adv)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit("usage: python3 genon/register_scan.py <plan.json> [more.json ...]")
    total = 0
    for p in sys.argv[1:]:
        n, _ = report(scan_file(p), Path(p).name)
        total += n
    print(f"\nTOTAL ban hits: {total}")
    sys.exit(1 if total else 0)
