#!/usr/bin/env python3
"""prompt_assembly.py — the prototype's generation prompt wrapper, extracted VERBATIM.

This module IS the "same way" guarantee (HANDOVER, step-4 execution design):
every function below is lifted from Project Aruvi's app/aruvi_streamlit/app.py
(mtime 2026-07-15 state) with ZERO creative edits. Document order, system/user
placement, framing text, caching block structure — all byte-identical to the
prototype's two LP/assessment call sites.

The ONLY deviations, each mechanical and declared:
1. DATA_ROOT: the prototype's `PROJECT_ROOT / "mirror"` becomes this repo's
   `data/content/` (same internal layout; env ARUVI_DATA_DIR overrides) —
   the path-table translation CLAUDE.md §10 prescribes.
2. Streamlit import removed; nothing else in these functions used it.
3. The two prompt-building code paths, which live inline in app.py's
   generate function (non-English) and in _build_lpa_prompts_english, are
   exposed as functions returning (system_prompt_blocks, user_message_blocks).
   The non-English inline block is wrapped as _build_lpa_prompts_standard —
   its body is the verbatim inline code.
4. (2026-07-25, LP v1.2) "role_handoff": <per LP Constitution> added to the
   top-level output sketch in both schema branches — the sketch must track
   Amendment A1's top level or the model drops constitution-mandated siblings.
5. (2026-08-12, S11) `_build_lpa_prompts_english` lifted from the same app.py
   state, with `phases` -> `time_bands` / `description` -> `activity` in its
   period sketch and length constraints. FORCED by english LP v1.2's P3
   conversion: compile.py v0.5 is declared-only and reads exactly `time_bands`
   / `activity`, so the verbatim string would have produced a paid canonical
   that does not compile. Same class as deviation 4.
6. That function's return annotation `tuple[str, str]` -> `tuple[list, list]`,
   which is what it has always returned (deviation 3 made the same correction
   on the standard path).
Nothing else changed. If you edit a prompt string here you are no longer
generating "the same way" — don't.
"""

from __future__ import annotations

import os
from pathlib import Path

# ── Prompt caching toggle ─────────────────────────────────────────────────────
# Set USE_PROMPT_CACHE = True  → cache_control blocks active (1h TTL)
#                                cache_write costs 2× input rate per token
#                                cache_read  costs 0.1× input rate per token
#                                benefit: repeated chapters in same session
#                                hit the cache and save ~90% on static tokens
# Set USE_PROMPT_CACHE = False → no cache_control sent; all tokens billed at
#                                standard input rate (1× — no surcharge)
#                                use during development / single-chapter runs
USE_PROMPT_CACHE = False

def _cache_ctrl() -> dict:
    """Return cache_control block if caching is enabled, else empty dict."""
    return {"cache_control": {"type": "ephemeral", "ttl": "1h"}} if USE_PROMPT_CACHE else {}

# ── Data root (deviation 1: repo data/content instead of prototype mirror) ────

REPO_ROOT = Path(__file__).resolve().parent.parent
DATA_ROOT = Path(os.environ.get("ARUVI_DATA_DIR", REPO_ROOT / "data" / "content"))

# ── Stage derivation ──────────────────────────────────────────────────────────

def get_stage(grade: str) -> str:
    preparatory = {"Grade III", "Grade IV", "Grade V"}
    middle       = {"Grade VI", "Grade VII", "Grade VIII"}
    if grade in preparatory: return "preparatory"
    if grade in middle:      return "middle"
    return "secondary"

def grade_to_folder(grade: str) -> str:
    """Return the folder name for a grade — matches the roman-numeral dirs in mirror/."""
    _mapping = {
        "Grade I":    "i",    "Grade II":   "ii",   "Grade III": "iii",
        "Grade IV":   "iv",   "Grade V":    "v",    "Grade VI":  "vi",
        "Grade VII":  "vii",  "Grade VIII": "viii",
        "Grade IX":   "ix",
    }
    return _mapping.get(grade, grade.lower().replace("grade ", ""))

def subject_to_folder(subject: str) -> str:
    mapping = {
        "Social Science":       "social_sciences",
        "Mathematics":          "mathematics",
        "Science":              "science",
        "English":              "english",
        "The World Around Us":  "the_world_around_us",
    }
    return mapping.get(subject, subject.lower().replace(" ", "_"))

# Subjects whose chapter summaries are JSON (structured for downstream LP/A
# constitutions). All others are plain .txt.
_JSON_SUMMARY_SUBJECTS = {"mathematics", "english", "the_world_around_us"}

# ── Path resolver ─────────────────────────────────────────────────────────────

def resolve_paths(grade: str, subject: str, chapter_number: int) -> dict:
    stage  = get_stage(grade)
    grade_f = grade_to_folder(grade)
    subj_f  = subject_to_folder(subject)
    mirror  = DATA_ROOT  # deviation 1: was PROJECT_ROOT / "mirror"
    nn      = f"{chapter_number:02d}"
    # Prefer stage-routed LP and assessment constitutions
    # (`{subject}/{stage}/...txt`); fall back to the flat path for subjects
    # that haven't been split by stage yet.
    _lp_staged = mirror / f"constitutions/lesson_plan/{subj_f}/{stage}/lesson_plan_constitution.txt"
    _lp_flat   = mirror / f"constitutions/lesson_plan/{subj_f}/lesson_plan_constitution.txt"
    _ac_staged = mirror / f"constitutions/assessment/{subj_f}/{stage}/assessment_constitution.txt"
    _ac_flat   = mirror / f"constitutions/assessment/{subj_f}/assessment_constitution.txt"
    return {
        "lp_constitution":  _lp_staged if _lp_staged.exists() else _lp_flat,
        "assessment_const": _ac_staged if _ac_staged.exists() else _ac_flat,
        "pedagogy":         mirror / f"framework/{subj_f}/{stage}/pedagogy_{stage}_{subj_f}.txt",
        # Mathematics and English summaries are .json (structured for LP/A
        # constitutions); all others are plain .txt.
        "chapter_summary":  (
            mirror / f"chapters/{subj_f}/{grade_f}/summaries/ch_{nn}_summary.json"
            if subj_f in _JSON_SUMMARY_SUBJECTS
            else mirror / f"chapters/{subj_f}/{grade_f}/summaries/ch_{nn}_summary.txt"
        ),
        "chapter_mapping":  mirror / f"chapters/{subj_f}/{grade_f}/mappings/ch_{nn}_mapping.json",
    }

def read_file(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as e:
        return f"[FILE NOT FOUND: {path}]"

# ── Period schedule formatting ────────────────────────────────────────────────

def format_period_schedule(period_rows: list, session: dict) -> str:
    lines = []
    total_periods = 0
    total_minutes = 0
    for i, rid in enumerate(period_rows):
        dur = session.get(f"dur_sel_{rid}", 40)
        cnt = session.get(f"cnt_{rid}", 1)
        total_periods += cnt
        total_minutes += dur * cnt
        lines.append(
            f"  Row {i+1}: {dur} minutes × {cnt} period{'s' if cnt != 1 else ''} = {dur*cnt} minutes"
        )
    h, m = divmod(total_minutes, 60)
    time_str = f"{h}h {m}min" if h > 0 else f"{m} minutes"
    return (
        f"Period schedule:\n" + "\n".join(lines) +
        f"\nTotal: {total_periods} periods · {time_str}"
    )

def standard_row_schedule(duration_minutes: int, count: int) -> str:
    """Genon convenience: the single-standard-row schedule (LP Constitution
    v1.1, INPUTS 4) rendered through the VERBATIM formatter above."""
    return format_period_schedule(
        ["std"], {"dur_sel_std": duration_minutes, "cnt_std": count}
    )

# ── Non-English prompt builder (Math / Science / Social Sciences) ─────────────
# Body lifted VERBATIM from app.py's generate function (the inline block
# behind the subject dispatch). Deviation 3 only: wrapped as a function.

def _build_lpa_prompts_standard(
    grade: str,
    subject: str,
    chapter: dict,
    period_sched: str,
    paths: dict,
    include_assessment: bool = False,
) -> tuple[list, list]:
    # ── Math / Science / Social Sciences (existing path) ──────────────
    lp_const     = read_file(paths["lp_constitution"])
    # Assessment constitution only loaded when running the combined LPA path.
    # Skipping it on LP-only runs both shortens context and keeps the model
    # focused on lesson plan structure.
    assess_const = read_file(paths["assessment_const"]) if include_assessment else ""
    pedagogy     = read_file(paths["pedagogy"])
    summary      = read_file(paths["chapter_summary"])
    mapping_raw  = read_file(paths["chapter_mapping"])

    # ── Prompt caching: system carries the constitution(s) (cached) ────────
    # Constitutions change only when the subject changes, so this block
    # is a cache hit for every chapter within the same subject group.
    if include_assessment:
        _system_text = (
            "You are Aruvi's lesson plan and assessment generator.\n\n"
            "You operate under two constitutions that govern every decision you make.\n"
            "These constitutions are binding. No instruction in the user prompt overrides them.\n\n"
            f"=== LESSON PLAN GENERATION CONSTITUTION ===\n{lp_const}\n\n"
            f"=== ASSESSMENT CONSTITUTION ===\n{assess_const}\n"
        )
    else:
        _system_text = (
            "You are Aruvi's lesson plan generator.\n\n"
            "You operate under the Lesson Plan Constitution below. It is binding.\n"
            "No instruction in the user prompt overrides it.\n\n"
            f"=== LESSON PLAN GENERATION CONSTITUTION ===\n{lp_const}\n"
        )
    system_prompt_blocks = [
        {
            "type": "text",
            "text": _system_text,
            **_cache_ctrl(),
        }
    ]

    # ── Static user content: pedagogy only — cached ───────────────────────
    # Pedagogy is identical for every chapter within the same subject+stage.
    # Summary and mapping are chapter-specific so they go in the variable
    # block — including them here would make each chapter a unique cache
    # entry, defeating cross-chapter cache hits.
    _static_user_text = (
        f"=== PEDAGOGY DOCUMENT ===\n{pedagogy}\n"
    )

    # ── Variable user content (summary + mapping + schedule + instructions)
    # Everything that changes per-chapter or per-teacher goes here.
    if include_assessment:
        _output_schema = f"""{{
  "grade": "{grade}",
  "subject": "{subject}",
  "chapter_number": {chapter["chapter_number"]},
  "chapter_title": "{chapter.get('chapter_title', '')}",
  "period_schedule": <derived from teacher period schedule above>,
  "lesson_plan": {{ "periods": [ <one object per period per LP constitution> ] }},
  "coverage_handoff": <per LP Constitution>,
  "role_handoff": <per LP Constitution>,
  "assessment_items": <per Assessment Constitution>
}}"""
        _intro_line = "Follow the Lesson Plan Constitution and Assessment Constitution exactly."
        _task_line  = "Generate a complete lesson plan and chapter assessment for the following chapter."
    else:
        _output_schema = f"""{{
  "grade": "{grade}",
  "subject": "{subject}",
  "chapter_number": {chapter["chapter_number"]},
  "chapter_title": "{chapter.get('chapter_title', '')}",
  "period_schedule": <derived from teacher period schedule above>,
  "lesson_plan": {{ "periods": [ <one object per period per LP constitution> ] }},
  "coverage_handoff": <per LP Constitution>,
  "role_handoff": <per LP Constitution>
}}"""
        _intro_line = "Follow the Lesson Plan Constitution exactly."
        _task_line  = "Generate a complete lesson plan for the following chapter."

    _variable_user_text = f"""{_task_line}

=== CHAPTER SUMMARY ===
{summary}

=== CHAPTER MAPPING JSON ===
{mapping_raw}

=== TEACHER PERIOD SCHEDULE ===
{period_sched}

=== INSTRUCTIONS ===
{_intro_line}
Produce your entire output as a single valid JSON object with this top-level structure:

{_output_schema}

LENGTH CONSTRAINTS (strictly enforced to keep output compact):
- Each phase `description`: 2–3 sentences maximum.
- Each `teacher_notes` field: 2–3 sentences maximum.

Output only the raw JSON object. No markdown. No prose. No section headers. No ```json fences.
"""

    user_message_blocks = [
        {
            "type": "text",
            "text": _static_user_text,
            **_cache_ctrl(),
        },
        {
            "type": "text",
            "text": _variable_user_text,
        },
    ]

    return system_prompt_blocks, user_message_blocks


def _build_lpa_prompts_english(
    grade: str,
    subject: str,
    chapter: dict,
    period_sched: str,
    paths: dict,
    include_assessment: bool = False,
) -> tuple[list, list]:
    """Build (system_prompt, user_prompt) for English LP (and optionally A).

    English uses a two-axis schema (main_section × spine). The chapter
    summary is JSON (produced by the cowork prompt
    `chapter_summary_competency_mapping_english.md`) and is the source
    of truth for the LP and assessment. C-codes do not appear in LP/A
    output; the Allocate page reads `spine_to_cg.json` separately.

    When include_assessment=False the assessment constitution is dropped
    from the system prompt and the output schema instruction omits
    assessment_items — the LP-only run produces lesson_plan plus
    coverage_handoff that a later deferred run will consume.
    """
    stage = get_stage(grade)

    lp_const     = read_file(paths["lp_constitution"])
    assess_const = read_file(paths["assessment_const"]) if include_assessment else ""
    pedagogy     = read_file(paths["pedagogy"])
    summary      = read_file(paths["chapter_summary"])

    # Stage-aware rubric depth (Assessment Constitution Rule 10).
    rubric_bullets = (
        "3"   if stage == "preparatory"
        else "3-4" if stage == "middle"
        else "4-5"
    )

    # Stage-aware prompt template fragments. Prep uses the 5-spine prep-native
    # vocabulary; middle uses the 6-spine model. Prep bans ECR, adds the
    # picture_narrative section type, and folds listening into oracy.
    if stage == "preparatory":
        _section_type_enum = "prose|poem|narrative|dialogue|informational|picture_narrative"
        _coverage_handoff_block = (
            '"coverage_handoff": {\n'
            '    "reading":                      { "section_contributions": [<contribution>] },\n'
            '    "oracy":                        { "section_contributions": [...] },\n'
            '    "writing":                      { "section_contributions": [...] },\n'
            '    "word_work": { "section_contributions": [...] },\n'
            '    "beyond_text":                  { "section_contributions": [...] }\n'
            '  }'
        )
        _spine_code_enum  = "reading|oracy|writing|word_work|beyond_text"
        _spine_title_enum = "Reading|Oracy|Writing|Word Work|Beyond the Text"
        _qtype_enum       = "MCQ|SCR|MATCH|FILL_IN|TRUE_FALSE|ORAL_PROMPT|WRITING_TASK|PROJECT"
        _open_types_list  = "ORAL_PROMPT, WRITING_TASK, PROJECT, reflective SCR"
        _bullet_word_cap  = "8"
        _content_sources_long = (
            "prose_summary (prose/narrative/dialogue/informational sections), "
            "poem_text + poem_appreciation_summary (poem sections), or "
            "picture_story_summary + dialogue_text (picture_narrative sections)"
        )
        _content_sources_short = (
            "prose_summary / poem_text + poem_appreciation_summary / "
            "picture_story_summary + dialogue_text"
        )
        _transcript_constraint = (
            "Listening tasks at preparatory live INSIDE the oracy spine. "
            "Each listening-based oracy item carries transcript_ref \"p.NN\" "
            "lifted from the relevant task object in the summary's oracy cell."
        )
    else:
        _section_type_enum = "prose|poem|narrative|dialogue|informational"
        _coverage_handoff_block = (
            '"coverage_handoff": {\n'
            '    "reading_for_comprehension": { "section_contributions": [<contribution>] },\n'
            '    "listening":                 { "section_contributions": [...] },\n'
            '    "speaking":                  { "section_contributions": [...] },\n'
            '    "writing":                   { "section_contributions": [...] },\n'
            '    "vocabulary_grammar":        { "section_contributions": [...] },\n'
            '    "beyond_text":               { "section_contributions": [...] }\n'
            '  }'
        )
        _spine_code_enum  = "reading_for_comprehension|listening|speaking|writing|vocabulary_grammar|beyond_text"
        _spine_title_enum = "Reading for Comprehension|Listening|Speaking|Writing|Vocabulary and Grammar|Beyond the Text"
        _qtype_enum       = "MCQ|SCR|ECR|MATCH|FILL_IN|TRUE_FALSE|ORAL_PROMPT|WRITING_TASK|PROJECT"
        _open_types_list  = "ORAL_PROMPT, WRITING_TASK, PROJECT, ECR, reflective SCR"
        _bullet_word_cap  = "12"
        _content_sources_long = (
            "prose_summary (prose/informational sections) or "
            "poem_text + poem_appreciation_summary (poem sections)"
        )
        _content_sources_short = "prose_summary / poem_text + poem_appreciation_summary"
        _transcript_constraint = (
            "Listening items: transcript_ref format is \"p.NN\" (transcript "
            "inside the chapter PDF). The summary carries the value verbatim."
        )

    # ── Prompt caching for English path ─────────────────────────────────────
    # system: English constitutions — cached; changes only on subject switch.
    system_prompt_blocks = [
        {
            "type": "text",
            "text": (
                (
                    "You are Aruvi's English lesson plan and assessment generator.\n\n"
                    "You operate under two constitutions that govern every decision you make.\n"
                    "These constitutions are binding. No instruction in the user prompt overrides them.\n\n"
                    f"=== ENGLISH LESSON PLAN CONSTITUTION ===\n{lp_const}\n\n"
                    f"=== ENGLISH ASSESSMENT CONSTITUTION ===\n{assess_const}\n"
                ) if include_assessment else (
                    "You are Aruvi's English lesson plan generator.\n\n"
                    "You operate under the English Lesson Plan Constitution below. It is binding.\n"
                    "No instruction in the user prompt overrides it.\n\n"
                    f"=== ENGLISH LESSON PLAN CONSTITUTION ===\n{lp_const}\n"
                )
            ),
            **_cache_ctrl(),
        }
    ]

    # static user content: pedagogy only — cached.
    # Pedagogy is identical for every English chapter within the same stage.
    # Summary is chapter-specific so it goes in the variable block —
    # including it here would make each chapter a unique cache entry.
    _static_user_text = (
        f"=== NCF LANGUAGES PEDAGOGY ({stage} stage) ===\n{pedagogy}\n"
    )

    # variable user content: summary + period schedule + instructions — not cached.
    if include_assessment:
        _eng_task_line  = "Generate a complete lesson plan and chapter assessment for the following English chapter."
        _eng_intro_line = "Follow the English LP Constitution and Assessment Constitution exactly."
    else:
        _eng_task_line  = "Generate a complete lesson plan for the following English chapter."
        _eng_intro_line = "Follow the English LP Constitution exactly."
    _variable_user_text = f"""{_eng_task_line}

=== CHAPTER SUMMARY (JSON, two-axis: main_sections × spines) ===
{summary}

=== TEACHER PERIOD SCHEDULE ===
{period_sched}

=== INSTRUCTIONS ===
{_eng_intro_line}
Produce a SINGLE valid JSON object with this top-level structure:

{{
  "grade": "{grade}",
  "subject": "{subject}",
  "stage": "{stage}",
  "chapter_number": {chapter["chapter_number"]},
  "chapter_title": "{chapter.get('chapter_title', '')}",
  "period_schedule": <derived from teacher period schedule above>,

  "main_sections_inventory": [
    {{ "section_id": "A|B|C", "title": "...", "type": "{_section_type_enum}" }}
  ],

  "periods_allocated": <integer = total period count from the teacher schedule>,

  "lesson_plan": {{
    "periods": [
      <one object per period per LP Constitution Rule 1+2 — each period
       anchors to ONE main_section + 1-2 spines within it; periods walk
       main_sections in textbook order then spines within each section.
       Required fields: period_number, period_duration_minutes,
       section_id, section_title, spines_taught, activity_title,
       pedagogical_methods (object keyed by each spine in spines_taught;
       each value is one method drawn from that spine's permitted list
       in LP Rule 4 for the stage — keys MUST equal spines_taught
       exactly), tasks_in_class (each {{spine, task_index, task_brief}}),
       homework, time_bands (each {{minutes, activity}}; tile 0..duration
       with no gaps), teacher_notes
       (2-3 sentences max, grounded in main_section's prose_summary or
       poem_appreciation_summary), materials.>
    ]
  }},

  {_coverage_handoff_block},

  "assessment_items": [
    {{
      "spine_code":  "{_spine_code_enum}",
      "spine_title": "{_spine_title_enum}",
      "note":        "",
      "items": [
        <one item per section_contribution in coverage_handoff for this
         spine (Assessment Constitution Rule 2). Each item tests the
         cell's implied_lo.

         STRICT GENERATION RULES — these override everything else:
         - DO NOT read summary.<spine>.tasks_verbatim[] or question_bank[].
           These fields are FORBIDDEN inputs to the assessment generator.
           Reading either field is a constitution violation regardless of
           intent. The implied_lo in coverage_handoff already encodes
           what was taught.
         - Derive every item solely from the section's content sources
           ({_content_sources_long}) plus the implied_lo from
           coverage_handoff.
         - The item MUST be original — it must not reproduce, paraphrase,
           or structurally echo any textbook exercise wording.
         - The item MUST be visibly grounded in the section's actual
           content: name a character, scene, specific line, grammar
           concept, or writing context drawn from prose_summary /
           poem_text. Generic questions that could apply to any chapter
           are prohibited (Assessment Rule 3).

         Required fields per item: id (e.g. "Q-RFC-A-1"),
         source_section_id, source_section_title, source_section_type,
         source_spine, source_lo (implied_lo copied verbatim from
         coverage_handoff), item_stem (original question grounded in
         section content), question_type (from Assessment Rule 4 set:
         {_qtype_enum}), options ([] unless MCQ or TRUE_FALSE),
         visual_stimulus ("" or pipe-table only), transcript_ref
         (Listening items only; "" otherwise), teacher_guide
         {{suggested_answer (CLOSED non-MCQ items; "" otherwise),
         expected_elements (OPEN items: {rubric_bullets} bullets ≤ {_bullet_word_cap}
         words each; [] otherwise), note ("" unless fallback)}},
         verified (true for open items; true for closed only when
         answer is unambiguously supported by the section's content
         sources).>
      ]
    }}
  ]
}}

CRITICAL CONSTRAINTS:
- Total LP period count = the teacher schedule's period_count. Distribute
  across (section × spine) cells in textbook order (LP Rule 1+2), with
  per-section period share roughly proportional to the section's
  page_count (±1 period tolerance).
- Total assessment item count = number of section_contributions across
  all spines in coverage_handoff that have at least one anchored task
  (one item per spine-cell implied_lo, per Assessment Rule 2). Spines
  with no section_contributions are omitted entirely. For each item,
  read ONLY the cell's implied_lo from coverage_handoff and the
  section's content sources ({_content_sources_short}).
  DO NOT read tasks_verbatim[] or question_bank[] for any purpose —
  these fields are forbidden inputs to the assessment generator.
  Generate one original item per cell grounded in the section content.
- C-codes MUST NOT appear anywhere in the LP or assessment JSON.
- `pedagogical_methods` per period MUST be an object whose keys equal
  `spines_taught` exactly. Each value MUST be drawn from that spine's
  permitted method list in LP Constitution Rule 4 for the {stage}
  stage. Do NOT invent methods. Do NOT collapse multiple spines onto
  a single method.
- {_transcript_constraint}
- The answer layer applies per item. A closed item (MCQ, FILL_IN,
  MATCH, TRUE_FALSE, factual SCR) carries
  `teacher_guide.suggested_answer` (verified against the section's
  content sources; omitted for MCQ — correct option is flagged in
  options[].is_correct). An open item ({_open_types_list}) carries
  `teacher_guide.expected_elements` ({rubric_bullets} short bullets,
  each ≤ {_bullet_word_cap} words). No item carries both fields.

LENGTH CONSTRAINTS:
- Each time band `activity`: 2-3 sentences maximum.
- Each `teacher_notes`: 2-3 sentences maximum.
- Each `suggested_answer`: 1-2 sentences plain prose.
- Each `expected_elements` bullet: ≤ {_bullet_word_cap} words.

Output only the raw JSON object. No markdown. No prose. No headers. No ```json fences.
"""

    # LP-only path: strip the assessment_items schema block and the assessment-
    # related critical constraints from the variable user text. The full prompt
    # above stays the source of truth for the LPA path; the surgery below is
    # bounded by unique anchor strings so a constitution edit upstream would
    # surface as a clear failure rather than silent drift.
    if not include_assessment:
        _vt = _variable_user_text
        # Remove the comma after coverage_handoff's closing brace and the entire
        # assessment_items array (from `,\n\n  "assessment_items": [` through
        # the next `]\n}`).
        # Anchors below match the *rendered* f-string output — i.e. each `{{`
        # in source becomes `{` and each `}}` becomes `}`. Do NOT add escapes.
        _start_marker = '  },\n\n  "assessment_items": ['
        _end_marker   = ']\n}\n\nCRITICAL CONSTRAINTS:'
        _si = _vt.find(_start_marker)
        _ei = _vt.find(_end_marker)
        if _si != -1 and _ei != -1:
            _vt = _vt[:_si] + '  }\n}\n\nCRITICAL CONSTRAINTS:' + _vt[_ei + len(_end_marker):]
        # Drop assessment-only critical constraints (the "Total assessment item
        # count …" paragraph through "Generate one original item …").
        _ac_start = '- Total assessment item count'
        _ac_end   = '- C-codes MUST NOT'
        _si2 = _vt.find(_ac_start)
        _ei2 = _vt.find(_ac_end)
        if _si2 != -1 and _ei2 != -1:
            _vt = _vt[:_si2] + _vt[_ei2:]
        # Drop the answer-layer paragraph (closed/open items) — only relevant
        # to assessment items.
        _al_start = '- The answer layer applies per item.'
        _al_end   = '\nLENGTH CONSTRAINTS:'
        _si3 = _vt.find(_al_start)
        _ei3 = _vt.find(_al_end)
        if _si3 != -1 and _ei3 != -1:
            _vt = _vt[:_si3] + _vt[_ei3 + 1:]  # +1 to consume the leading \n of LENGTH
        # Drop assessment-only length constraints (suggested_answer,
        # expected_elements bullets) — they have no effect for LP-only output.
        for _line in (
            "- Each `suggested_answer`: 1-2 sentences plain prose.\n",
            "- Each `expected_elements` bullet: ≤ 12 words.\n",
        ):
            _vt = _vt.replace(_line, "")
        _variable_user_text = _vt

    user_message_blocks = [
        {
            "type": "text",
            "text": _static_user_text,
            **_cache_ctrl(),
        },
        {
            "type": "text",
            "text": _variable_user_text,
        },
    ]

    return system_prompt_blocks, user_message_blocks


def build_lpa_prompts(
    grade: str,
    subject: str,
    chapter: dict,
    period_sched: str,
    paths: dict | None = None,
    include_assessment: bool = False,
) -> tuple[list, list]:
    """Subject dispatch — mirrors app.py's generate function exactly.

    English uses a two-axis (main_section × spine) schema and has no
    per-chapter competency mapping; the prompt is built differently.
    """
    if paths is None:
        paths = resolve_paths(grade, subject, chapter["chapter_number"])
    if subject_to_folder(subject) == "english":
        return _build_lpa_prompts_english(
            grade, subject, chapter, period_sched, paths,
            include_assessment=include_assessment,
        )
    return _build_lpa_prompts_standard(
        grade, subject, chapter, period_sched, paths,
        include_assessment=include_assessment,
    )
