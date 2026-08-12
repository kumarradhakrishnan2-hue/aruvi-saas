#!/usr/bin/env python3
"""S11 · lift `_build_lpa_prompts_english` from the prototype into genon/prompt_assembly.py.

WHY NOW. `prompt_assembly.py` extracted the prototype's prompt wrapper VERBATIM for every
subject except English, and refused English in terms:

    "lift _build_lpa_prompts_english verbatim when the English combo enters step 3/4 —
     its constitution is not yet genon-amended, so extracting it now would freeze a
     prompt that is about to change shape."

S11's P1-P4 (2026-08-12) is that amendment: LP v1.1 -> v1.2 (A1, the register, and P3's
`phases` -> `time_bands`) and assessment v1.3 -> v1.4. The condition the note named is
satisfied, so the lift is due. It fired at STEP 1 of C1 before any API call, so it cost
nothing — the note did exactly what it was written to do.

SOURCE: Project Aruvi `app/aruvi_streamlit/app.py`, lines 584-901 (mtime 2026-07-15),
the same file and the same state the standard path was lifted from. The function text is
read from that file at run time rather than retyped, so there is no transcription risk;
this script asserts what it changes and nothing else.

THE DEVIATIONS, each mechanical and declared (numbering continues the module docstring's):

5. `phases` -> `time_bands` and the band's text key -> `activity`, in the period schema
   sketch and in LENGTH CONSTRAINTS. FORCED, not chosen: english LP v1.2's P3 conversion
   renamed both, and `aruvi_core/genon/compile.py` (v0.5, declared-only) reads exactly
   `time_bands` / `activity`. A verbatim lift here would have instructed the model to emit
   the retired shape and the canonical would have failed to compile AFTER being paid for.
   This is the same class of edit as deviation 4 (role_handoff at LP v1.2): the sketch must
   track the constitution it is generating under.
6. The return annotation `tuple[str, str]` -> `tuple[list, list]`. The prototype's
   annotation was already wrong — the function returns the two BLOCK LISTS, as its own
   last line shows — and deviation 3 made the same correction on the standard path.

NOT CHANGED, deliberately, though both were tempting:

- "Total assessment item count = number of section_contributions ... THAT HAVE AT LEAST ONE
  ANCHORED TASK". That clause is a residue of the drop licence S11 removed from LP Rule 2
  STEP 3. It is not a shape change and it is not wrong under the new mandate (a taught cell
  always has an anchored task), so it stays: editing a prompt string that is merely
  *unnecessary* is how "the same way" guarantee dies. Recorded as a C3 read instead.
- `rubric_bullets = "4-5"` at secondary, where assessment Rule 11 says "3-5 bullets". A
  narrower instruction than the constitution permits, not a contradiction of it. C3 reads it.
- The LP-only surgery block's hardcoded "≤ 12 words" line (it would miss preparatory's 8).
  A latent prototype bug on a stage this run does not touch; lifting it verbatim keeps the
  parity claim honest and leaves the bug where S9 will meet it.
"""
from __future__ import annotations

import pathlib
import shutil

REPO = pathlib.Path(__file__).resolve().parents[3]
OUT = pathlib.Path(__file__).resolve().parent
# The prototype sits beside this repo, on the founder's machine and in the sandbox alike
# (both mount aruvi-saas and "Project Aruvi" as siblings), so resolve it relatively rather
# than hardcoding either machine's absolute path.
PROTO = REPO.parent / "Project Aruvi" / "app/aruvi_streamlit/app.py"
PA = REPO / "genon/prompt_assembly.py"

START = "def _build_lpa_prompts_english(\n"
END = "\ndef generate_lp_only(\n"

DISPATCH_OLD = '''    if subject_to_folder(subject) == "english":
        raise NotImplementedError(
            "English canonical generation: lift _build_lpa_prompts_english "
            "verbatim when the English combo enters step 3/4 — its constitution "
            "is not yet genon-amended, so extracting it now would freeze a "
            "prompt that is about to change shape."
        )
'''

DISPATCH_NEW = '''    if subject_to_folder(subject) == "english":
        return _build_lpa_prompts_english(
            grade, subject, chapter, period_sched, paths,
            include_assessment=include_assessment,
        )
'''


def sub(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    assert n == 1, f"{label}: expected exactly 1 occurrence, found {n}"
    return text.replace(old, new)


def main() -> None:
    src = PROTO.read_text(encoding="utf-8")
    i = src.index(START)
    j = src.index(END, i)
    fn = src[i:j].rstrip("\n") + "\n"
    (OUT / "_lifted_english_prototype.txt").write_text(fn, encoding="utf-8")
    print(f"extracted {len(fn.splitlines())} lines from the prototype")

    # ── deviation 6 · the annotation matches what the function actually returns ──
    fn = sub(fn, ") -> tuple[str, str]:", ") -> tuple[list, list]:", "return annotation")

    # ── deviation 5 · the schema sketch tracks LP v1.2's P3 conversion ───────────
    fn = sub(fn,
             "       homework, phases (tile 0..duration with no gaps), teacher_notes",
             # NOTE the doubled braces: this sketch lives inside an f-string, so a literal
             # `{` must be written `{{` or Python evaluates it as an expression. Caught by
             # `NameError: name 'minutes' is not defined` on the first dry run — the same
             # family of hazard as the JSON quote escape MEMORY records for 2026-08-11, and
             # the reason the dry run exists.
             "       homework, time_bands (each {{minutes, activity}}; tile 0..duration\n"
             "       with no gaps), teacher_notes",
             "period schema · time_bands")
    fn = sub(fn,
             "- Each phase `description`: 2-3 sentences maximum.",
             "- Each time band `activity`: 2-3 sentences maximum.",
             "length constraints · band activity")
    assert "phases" not in fn, "the retired band shape survived the conversion"
    assert fn.count("time_bands") == 1 and fn.count("`activity`") == 1

    # ── splice into prompt_assembly.py, before build_lpa_prompts ────────────────
    pa = PA.read_text(encoding="utf-8")
    shutil.copyfile(PA, OUT / "prompt_assembly_pre_english_lift.py")
    marker = "def build_lpa_prompts(\n"
    pa = sub(pa, marker, fn + "\n\n" + marker, "splice point")
    pa = sub(pa, DISPATCH_OLD, DISPATCH_NEW, "dispatch")

    # the module docstring's deviation list gains the two this lift declares
    pa = sub(pa,
             "4. (2026-07-25, LP v1.2) \"role_handoff\": <per LP Constitution> added to the\n"
             "   top-level output sketch in both schema branches — the sketch must track\n"
             "   Amendment A1's top level or the model drops constitution-mandated siblings.\n",
             "4. (2026-07-25, LP v1.2) \"role_handoff\": <per LP Constitution> added to the\n"
             "   top-level output sketch in both schema branches — the sketch must track\n"
             "   Amendment A1's top level or the model drops constitution-mandated siblings.\n"
             "5. (2026-08-12, S11) `_build_lpa_prompts_english` lifted from the same app.py\n"
             "   state, with `phases` -> `time_bands` / `description` -> `activity` in its\n"
             "   period sketch and length constraints. FORCED by english LP v1.2's P3\n"
             "   conversion: compile.py v0.5 is declared-only and reads exactly `time_bands`\n"
             "   / `activity`, so the verbatim string would have produced a paid canonical\n"
             "   that does not compile. Same class as deviation 4.\n"
             "6. That function's return annotation `tuple[str, str]` -> `tuple[list, list]`,\n"
             "   which is what it has always returned (deviation 3 made the same correction\n"
             "   on the standard path).\n",
             "docstring deviations")
    PA.write_text(pa, encoding="utf-8")

    # ── guards ──────────────────────────────────────────────────────────────────
    now = PA.read_text(encoding="utf-8")
    assert now.count("def _build_lpa_prompts_english(") == 1
    assert "NotImplementedError" not in now, "the refusal must be gone, not shadowed"
    assert now.count("tasks_verbatim") >= 2, (
        "the prohibition prose must survive the lift — english sends the FULL summary "
        "(the LP needs tasks_verbatim; Rule 3 draws tasks from it) and holds the "
        "assessment off it in words, which is why stripping it here would be wrong")
    compile(now, str(PA), "exec")
    print("spliced into prompt_assembly.py · dispatch rewired · parse clean")


if __name__ == "__main__":
    main()
