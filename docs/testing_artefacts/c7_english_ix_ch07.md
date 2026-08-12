# C7 — register: audit the gate, judge what it cannot · english · IX · ch 7 *Vitamin-M*

**Date:** 2026-08-12 · **Scanned:** all 10 files — the 3 library canonicals **and the 7 C6
served plans**, including `result.dropped_units` (a teacher reads those on screen) · LP v1.2

---

## (a) The machine gate — 0 ban hits, everywhere

| file | bans | advisories |
|---|---|---|
| `ch_07_canonical.json` (17) | **0** | 0 |
| `ch_07_canonical_p14.json` (14) | **0** | 1 |
| `ch_07_canonical_p10.json` (10) | **0** | 1 |
| served X=9 · 11 · 12 · 13 · 15 · 15-mixed · 16 | **0** each | 0 · 1 · 1 · 1 · 1 · 1 · 0 |

`register_scan` reached the band text in every file (54 / 57 / 26 bands plus titles, notes,
materials and homework), so the zero is a real zero and not a shape it failed to read. This is a
constitution that received its three-ban block the same morning: **the register held on its
first live generation, across 41 authored units and 7 serves.**

## (b) Ruling on every advisory — 2 distinct hits, both correct as advisories

**1 · `calendar` — "today's podcast" · p14 U9 band 1** (propagates into the X=12, 13, 15 and
mixed serves, which all contain that unit)

> *"…Grandpa's calm, deliberate manner and his advice to Ravi's mother suggest a practised inner
> composure — **today's** podcast on meditation explores a discipline that cultivates exactly
> that quality."*

**Ruled: not a breach, leave as advisory.** "Today's podcast" names the lesson's own material,
not a calendar position — it is self-consistent whenever the unit is taught, which is precisely
the test the scanner's header sets for `today`/`yesterday` ("Will it rain today?"). No pattern
change.

**2 · `positional` — "an earlier unit" · p10 U10 `teacher_notes`** (rides into the X=11 serve)

> *"…The photograph slide-show task is set as homework and **does not require any classroom
> artefact from an earlier unit**."*

**Ruled: not a breach — and it is evidence, not noise.** Backward reference is legal since
v1.10; what this sentence actually does is *declare artefact independence*. Recorded at C5 and
worth repeating here because of what §(c) found: **the compact states out loud the rule the
standard breaks.** Same chapter, same run, same constitution.

## (c) What regex could not see — one finding, and it reached the teacher

**The mandated synthesis unit requires an artefact another unit produced, and the served plans
carry it verbatim.**

`ch_07_canonical.json` U17 — the closing synthesis, which is also the unit the engine *lends* —
carries:

- `materials`: `["Textbook pp.97–125", "Students' draft article (notebooks or draft sheets)"]`
- band `[30–50]`: *"Students **complete the draft article** 'Our Inspiring Elderly' (Paragraphs 3
  and 4 …)"*

The draft begins at U15 (*"Students draft Paragraphs 1 and 2 independently"*), twelve sittings
earlier. C3 found this in the library (ARV-D-132, accepted as authored); **C7's job is the served
artefact, and there it is worse**: the borrowed unit appears as the **last sitting** of the
X = 11 and X = 15 serves, where the host prefix comes from a *different* canonical.

| serve | host prefix | its writing unit does | borrowed closer asks for |
|---|---|---|---|
| X = 11 | p10's 10 units | U9 drafts the **whole four-paragraph article** in one sitting | "complete Paragraphs 3 and 4" of a draft that is already finished |
| X = 15 | p14's 14 units | U12 drafts the article | the same — plausible here by luck, not by design |

The X = 11 class is told to finish work it completed five sittings ago; nothing in the plan
reconciles the two. This is the ARV-D-023 family (a borrowed unit assuming a sitting the host
never had) in its artefact form.

**Why no existing pattern saw it.** The `artefact` family had five patterns, from S5's C7 — all
requiring either a time word ("prepared **previously**", "from the **previous** unit") or a
possessive-plus-time ("**their earlier** chart"). English's shape has neither: **a possessive
owner and a produced artefact, with no time word at all.** A class cannot arrive holding
"students' draft article" unless an earlier sitting made it — the dependency is in the
possession, not in a temporal phrase.

---

## The new patterns — added, measured, and one of them thrown away first

Per C7's mandate ("anything found here is a new PATTERN for `register_scan.py`, added with a
dated note"), two patterns land, both **advisory**:

```python
("artefact", False, r"\b(students['’]|pupils['’]|their)\s+(?:\w+\s+){0,2}?"
                    r"(draft|article|essay|poster|chart|model|display|collection|"
                    r"slide[- ]?show|presentation)s?\b(?!\s+(paper|sheets?))"),   # materials only
("artefact", False, r"\b(complete|finish|revise|redraft|continue)\s+(the|their)\s+"
                    r"(draft|article|essay|poster|model|collection)\b"),
```

**The first cut was wrong and the corpus said so immediately.** Applied to *all* fields, the
possessive pattern fired **111 times across the 131 certified and served files on disk** — almost
every one of them *"students make their poster … display their posters"* **inside one unit**,
which the brief expressly licenses ("put BOTH acts inside ONE unit"). That is a gate nobody
would keep, and it is the same mistake S6's C7 records making with six of seven patterns.

Two things separate the real defect from the noise, and both are shape rather than vocabulary:

1. the possessive appears in **`materials` / `visual_aids`** — a shopping list naming an object
   only a previous sitting could have produced;
2. a **completion verb governs a definite artefact** — "complete the draft" presupposes it exists.

So `register_scan` gained **field scoping** (`_FIELD_SCOPED`, keyed by pattern object so the
scope sits beside the pattern it governs and cannot drift onto another). Scoped that way:

| | artefact hits, 131 files |
|---|---|
| before this pass | 36 |
| unscoped first cut | **111** — unusable |
| **shipped (scoped)** | **44** — the 36 unchanged, **+8 all on english ch 7's synthesis unit and its served copies** |

**Zero new hits anywhere outside this chapter**, and the false-positive probe is clean on every
standing classroom item: "Draft paper or notebooks", "Writing paper or notebooks", "Students'
notebooks", "their notebooks", "Exercise books", "Blank graphic organiser" — none fires.

**Advisory, not a ban, on purpose.** The rule it detects lives in the platform *brief*, not in
any constitution; a ban would fail certification against a rule no constitution states. Confirmed
after the change: `--certify-only` re-run reports **register clean (0 ban hits)** on all three
files and DETERMINISTIC CHECKS ALL PASS.

---

## Exit

**Zero live-ban hits across all ten files** — C7's exit condition, met. The advisory findings are
ruled on above; the artefact dependency is already on the register as **ARV-D-132** (accepted as
authored at C3), and it now has a detector so the next stage meets it at build time rather than
by eye.

**What C8 inherits, sharpened:** the transition to read is X = 11 — p10's ten units into the
borrowed U17 — and the specific question is no longer "is the seam smooth" but "what does a class
that already finished its article do with a closing sitting that asks it to finish the article".
