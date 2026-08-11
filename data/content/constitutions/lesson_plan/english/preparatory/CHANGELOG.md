# CHANGELOG — Lesson Plan Constitution · English · Preparatory Stage

The `VERSION` line lives in the constitution; the history lives here (testing.md §3, P4).

---

## v1.1 — 2026-08-11 · the narration format loses its JSON quote hazard (cross-stage)

Cross-stage amendment made after S8's C1 lost a paid compact to it. Landed ahead of this stage's own P-prep (S9). **One extra correction here:** the Example under this Format line never demonstrated the format — it showed a bare section name with no quoted brief — so a model copying the example would have produced the one shape the rule does not ask for. Made self-consistent.

**The hazard.** This rule mandated a narration format that puts a double-quoted phrase
inside a value the model emits as JSON — `Format: `<spine_section_name> ("brief ≤ 10 words")``. JSON strings are
delimited by `"`, so the inner pair has to be written `\"`, and nothing enforces that.
It is a habit the model keeps for a whole run or drops for a whole run: mathematics III
ch 5 proved both halves on consecutive calls, the standard escaping all 45 of its pairs
and parsing clean, the 11-period compact escaping none of its 42, blowing past the
pipeline's repair bound and costing ₹40.72 for a file that had to be recovered by hand.

**The fix removes the hazard rather than repairing it.** The repair bound was raised the
same day (10 → 500, `genon/generate_canonical.py::parse_with_repair`), but that catches
the mistake after the fact with a heuristic carrying its own magic numbers. Curly
quotation marks (U+201C/U+201D) have no meaning in JSON, need no escaping, and cannot
truncate a file — the mistake stops being possible. Straight *single* quotes would be
equally safe but collide with apostrophes, which this content is full of:
`('Make Amma's rangoli')` reads worse than `(“Make Amma's rangoli”)`. The teacher-facing
text is unchanged in substance and reads better in print.

**§9 — RELAXATION-ONLY, and the wording is what makes it so.** A bare substitution of one
mandated format for another would be a constitution change in the full sense, and would
re-open every stage already authored under the old text. So this amendment *licenses*
rather than switches: the curly form is what the Format and Example lines now show, and
one sentence records that the straight-quoted form **remains valid and is not a defect**.
Nothing is tightened, no new obligation is created (`MUST NOT` count asserted unchanged),
and every existing artefact satisfies the new text by construction. **No library
re-opens.**

**Scope is the narration format only.** The same `("…")` shape appears elsewhere in this
document as prose — register illustrations, prohibition examples — where it is the
document quoting a string to its reader rather than an instruction to emit quotes inside
a value. Those carry no hazard and are untouched.

Artefacts: `genon/out/stage_prep_mathematics_preparatory/` — `lp_english_preparatory_v1.0_pre.txt` ·
`curlyquote_english_preparatory.diff` · `apply_curly_quote_narration.py` (one script, all five
constitutions, exactly-one-occurrence asserts plus a guard that the obligation count is
unchanged in every file).

---

## v1.0 and earlier

No sidecar was kept before this file existed, and the constitution carried no in-document version-history block to lift out. Earlier history is in git.
