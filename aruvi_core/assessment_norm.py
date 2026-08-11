"""
Assessment item normalization → the uniform NormalizedItem contract.

The registry spec (docs/assessment-question-type-registry.md §1) identifies THREE
incompatible source field-shapes for the same question_type string, by subject family:

  • Constitution family — Science, Social Sciences, TWAU: `question_text`/`task`,
    `expected_elements[]`, `look_for[]`, `scaffold`, `format_of_output[]`, and a
    `guide{TYPE: {what_each_option_reveals, inclusivity, …}}` dict keyed by question type.
  • Maths family — `prompt`, `teacher_guide{expected_answer, method_one_line,
    what_each_option_reveals, inclusivity}`, `exercise{book_ref, description}`.
    SECONDARY maths is a verified hybrid (saved-file inspection 2026-07-10): it carries
    `question_text` + constitution-style `guide{TYPE}` + TOP-LEVEL expected_answer/
    method_one_line/look_for/expected_elements/scaffold — both shapes are read here.
  • English family — `item_stem`, `teacher_guide{suggested_answer, expected_elements[],
    what_each_option_reveals, note}`, `transcript_ref`.

One builder per family (spec §4 master mapping); each subject plugin's normalizer calls
its family builder ONCE per item, after link_resolver.stamp() has filled the meta, and
attaches the result as AssessmentItem.normalized. The 3b renderer reads ONLY that.

Locked rules honoured here:
  • cognitive_demand: absent key OR "" → None (same state; spec Open-items).
  • audio_ref: English transcript_ref ONLY when source_spine is the listening spine —
    its own field, NEVER merged with Maths exercise_ref.
  • EXTRACT_ANALYSIS: the extract routes to `passage`, never a generic stimulus.
  • Legacy English MCQ prose `note` → option_reveals under the "note" key (fallback the
    renderer shows as prose; constitutions were rewritten 2026-07-10, saved plans migrated,
    but un-migrated fallback items must still normalize).
  • English TRUE_FALSE `note` (verdict + justification) → model_answer, not reveals.
  • Tables are pre-split via normalize.parse_table — no renderer re-splits pipe strings.
"""
from __future__ import annotations

import re
from typing import Any, Dict, List, Optional

from .normalize import as_list, classify_stimulus, parse_table
from .view_model import NormalizedItem, RENDER_TEMPLATE, StimulusType

_OT_GUIDE_KEYS = ("format_type", "format_rationale", "what_this_demonstrates",
                  "reading_the_scaffold", "strong_vs_weak_markers",
                  "observation_rubric")  # TWAU performance_task=true variant (Rule 9)


# ── small shared pieces ──────────────────────────────────────────────────────────
def _clean(v: Any) -> Optional[str]:
    """'' / None / whitespace → None; else the stripped string. The empty-string-and-
    absent-are-the-same-state rule (cognitive_demand et al.)."""
    s = str(v).strip() if v is not None else ""
    return s or None


def typed_block(raw: Any) -> Optional[Dict[str, Any]]:
    """Type a raw stimulus exactly like LP visuals (classify_stimulus), with pipe-tables
    pre-split via parse_table so the wire shape is renderer-ready. Accepts both the plain
    string and the structured {type, payload} shape — classify_stimulus handles both — so
    a dict stimulus (SS secondary source_text extracts) is no longer coerced away to ''."""
    vs = classify_stimulus(raw if isinstance(raw, (str, dict)) else "")
    if vs.type == StimulusType.NONE:
        return None
    d: Dict[str, Any] = {"type": vs.type.value, "content": vs.content}
    if vs.type == StimulusType.TABLE:
        d["table"] = parse_table(vs.content)
    return d


def structured_options(raw: Any) -> List[Dict[str, Any]]:
    """Options preserved STRUCTURED ({label, text, is_correct}) — unlike the legacy
    normalize_options flattening, the 3b renderer marks the correct one itself."""
    out: List[Dict[str, Any]] = []
    for o in raw or []:
        if isinstance(o, dict):
            out.append({"label": str(o.get("label") or ""),
                        "text": str(o.get("text") or o.get("option") or ""),
                        "is_correct": bool(o.get("is_correct"))})
        elif str(o).strip():
            out.append({"label": "", "text": str(o), "is_correct": False})
    return out


def _competency(v: Any) -> Optional[Dict[str, str]]:
    if not isinstance(v, dict):
        return None
    code = _clean(v.get("c_code") or v.get("code"))
    text = _clean(v.get("competency_text") or v.get("text"))
    if not code and not text:
        return None
    return {"code": code or "", "text": text or ""}


def _reveals(v: Any) -> Dict[str, str]:
    if not isinstance(v, dict):
        return {}
    return {str(k): str(t) for k, t in v.items() if _clean(t)}


def _ot_guide(guide_for_type: Any) -> Optional[Dict[str, str]]:
    if not isinstance(guide_for_type, dict):
        return None
    d = {k: str(guide_for_type[k]) for k in _OT_GUIDE_KEYS if _clean(guide_for_type.get(k))}
    return d or None


_PAREN_MARK = re.compile(r"\((?:[a-z]|[ivxlcdm]+|\d+)\)", re.I)
_PAREN_HEAD = re.compile(r"^\((?:[a-z]|[ivxlcdm]+|\d+)\)", re.I)
_NUM_HEAD = re.compile(r"^\d+\.")


def _assemble(pieces: List[str], head: "re.Pattern") -> "tuple[str, List[Dict[str, str]]]":
    """Fold split pieces into (lead, [{marker, text}]). The first non-marker pieces are the
    lead (an intro / word-box before the list); marker pieces become parts."""
    lead_bits: List[str] = []
    parts: List[Dict[str, str]] = []
    for p in pieces:
        m = head.match(p)
        if m:
            parts.append({"marker": m.group(0), "text": p[m.end():].strip()})
        elif not parts:
            lead_bits.append(p)
        else:                                   # a stray trailing piece → glue to last part
            parts[-1]["text"] = (parts[-1]["text"] + " " + p).strip()
    return " ".join(lead_bits).strip(), parts


def split_parts(text: Any) -> "tuple[str, List[Dict[str, str]]]":
    """Parse a prose blob that packs a numbered/lettered list into ONE string into
    (lead, parts). The ONE place notation knowledge lives — the renderer just renders the
    list. Returns ("", []) / (text, []) when there is no genuine list, so a lone numeric
    answer ("15. It is the LCM…") or scattered figures ("Factors of 8: … 8. … 21.") never
    split. Two authored notations:
      • parenthesized sub-parts  "(a) … (b) …" / "(i) …" / "(1) …"  (≥2, opening paren required)
      • plain numbered list      "1. … 2. … 3. …"                   (≥2, a run starting at 1)
    """
    if not isinstance(text, str) or not text.strip():
        return "", []
    # (1) parenthesized — opening paren required so a closing paren inside maths
    # ("50 – (12 + 9)") is never a marker.
    pieces = [s.strip() for s in re.split(r"(?=(?:^|\s)\((?:[a-z]|[ivxlcdm]+|\d+)\)\s)", text, flags=re.I) if s.strip()]
    if sum(1 for p in pieces if _PAREN_MARK.match(p)) >= 2:
        return _assemble(pieces, _PAREN_HEAD)
    # (2) plain numbered — only when the markers form a run 1, 2, 3, …
    nums = [int(m.group(1)) for m in re.finditer(r"(?:^|\s)(\d+)\.\s", text)]
    if len(nums) >= 2 and all(v == i + 1 for i, v in enumerate(nums)):
        pieces = [s.strip() for s in re.split(r"(?=(?:^|\s)\d+\.\s)", text) if s.strip()]
        return _assemble(pieces, _NUM_HEAD)
    return "", []


_STEP_MARK = re.compile(r"(?:^|\s)Step\s+\d+\b", re.I)
# Any parenthesized sub-marker — number, letter or roman: (1)/(a)/(i). Opening paren
# required so a closing paren inside maths ("50 – (12 + 9)") is never read as a marker.
_PAREN_ANY = re.compile(r"(?<!\w)\((?:[a-z]|[ivxlcdm]+|\d+)\)", re.I)
# A plain single-letter marker "A." / "A)" (the A,B,C / a,b,c list notation).
_LETTER_MARK = re.compile(r"(?:^|\s)([A-Za-z])[.)]\s")


def _is_letter_run(letters: List[str]) -> bool:
    """True when single-letter markers form A,B,C… or a,b,c… — a run starting at A/a. The
    start + sequence check keeps stray capitals ("A. Kumar M. Singh") from splitting."""
    seq = [c.lower() for c in letters]
    return all(ord(c) == ord("a") + i for i, c in enumerate(seq))


def _split_inline_scaffold(line: str) -> List[str]:
    """A single scaffold line that packs a sequential run of ≥2 markers (no newline) → one
    row per marker. Notations handled: 'Step N …'; any parenthesized marker '(1)/(a)/(i) …';
    a plain numbered run 'N. …' (starting at 1); a plain lettered run 'A./A) …' (starting at
    A or a). Otherwise the line is returned whole."""
    if len(_STEP_MARK.findall(line)) >= 2:
        return [s.strip() for s in re.split(r"(?=(?:^|\s)Step\s+\d+\b)", line, flags=re.I) if s.strip()]
    if len(_PAREN_ANY.findall(line)) >= 2:
        return [s.strip() for s in re.split(r"(?=(?<!\w)\((?:[a-z]|[ivxlcdm]+|\d+)\))", line, flags=re.I) if s.strip()]
    nums = [int(m.group(1)) for m in re.finditer(r"(?:^|\s)(\d+)\.\s", line)]
    if len(nums) >= 2 and all(v == i + 1 for i, v in enumerate(nums)):
        return [s.strip() for s in re.split(r"(?=(?:^|\s)\d+\.\s)", line) if s.strip()]
    letters = [m.group(1) for m in _LETTER_MARK.finditer(line)]
    if len(letters) >= 2 and _is_letter_run(letters):
        return [s.strip() for s in re.split(r"(?=(?:^|\s)[A-Za-z][.)]\s)", line) if s.strip()]
    return [line]


def split_scaffold_lines(text: Any) -> List[str]:
    """Break a fill-in scaffold template into display ROWS so numbered/step items never run
    together in one paragraph (founder 2026-07-14: TWAU scaffolds were rendering continuous).
    Authored newlines are always row breaks; a scaffold that packs a sequential
    'Step N' / '(N)' / 'N.' run into ONE line (no newline) is additionally split so each item
    is its own row. A blank authored line is kept as an empty-string spacer (Part A / Part B).
    Returns [] when there is nothing multi-row to show (empty, or a single unnumbered line) —
    the renderer then falls back to plain prose."""
    if not isinstance(text, str) or not text.strip():
        return []
    rows: List[str] = []
    for raw in text.split("\n"):
        ln = raw.strip()
        if not ln:
            rows.append("")
            continue
        rows.extend(_split_inline_scaffold(ln))
    while rows and rows[0] == "":
        rows.pop(0)
    while rows and rows[-1] == "":
        rows.pop()
    if sum(1 for r in rows if r) <= 1:
        return []
    return rows


# Leading "True/False —" (or S/D, Yes/No, Same/Different) verdict word on a justification
# line — stripped because the verdict is already carried structurally (from is_correct). A
# separator (dash/colon) is REQUIRED so a reason that merely starts with such a word
# ("Different birds fly …") is never truncated.
_TF_REASON_HEAD = re.compile(
    r"^\s*(?:true|false|t|f|s|d|yes|no|same|different)\b\s*[—–\-:]\s*", re.I)


def tf_statements(options: List[Dict[str, Any]],
                  model_answer: Optional[str]) -> "tuple[List[Dict[str, Any]], bool]":
    """Collapse a TRUE_FALSE item's DOUBLY-stored content into ONE per-statement key.

    A True/False item packs its statements twice (the numbered list inside `item_stem` AND
    the `options[]`) and its verdicts twice (each option's `is_correct` AND the numbered
    `suggested_answer` prose). Rendering the MCQ/selected-response template over that shows
    the statements and the answer twice each. Here we fold it once: statement text + verdict
    come from the OPTIONS (authoritative), the per-statement justification is matched
    POSITIONALLY from the suggested-answer list (its leading "True/False —" verdict word
    stripped, since the verdict is already carried). Returns (statements, keep_prose):
    keep_prose is True only when the justification list could NOT be aligned 1:1, so the
    standalone prose is preserved rather than silently dropped."""
    if not options:
        return [], True
    _, parts = split_parts(model_answer or "")
    reasons = [p.get("text", "") for p in parts]
    aligned = len(reasons) == len(options)
    out: List[Dict[str, Any]] = []
    for i, o in enumerate(options):
        label = str(o.get("label") or (i + 1)).strip().rstrip(".")
        reason = _TF_REASON_HEAD.sub("", reasons[i]).strip() if aligned else ""
        out.append({"marker": f"{label}.", "text": str(o.get("text") or ""),
                    "verdict": bool(o.get("is_correct")), "reason": reason})
    return out, not aligned


def match_pairs_from(answer_key: Any) -> List[Dict[str, Any]]:
    """Structured MATCH answer → [{left, right}] rows. The pairing lives ONLY in
    teacher_guide.answer_key (an authored array of {left, right}); unlike TRUE_FALSE's
    is_correct, a MATCH item has NO other machine-readable source for the pairing, and the
    prose suggested_answer is written too many ways to parse reliably — so we read the
    explicit key and nothing else. Empty/absent → [] and the renderer keeps the prose."""
    out: List[Dict[str, Any]] = []
    for p in answer_key or []:
        if isinstance(p, dict):
            left = _clean(p.get("left"))
            right = _clean(p.get("right"))
            if left or right:
                out.append({"left": left or "", "right": right or ""})
    return out


def _dedupe_stem_table(n: NormalizedItem) -> None:
    """Strip an embedded pipe-table out of the stem — the recurring markup-as-prose bug.

    Some saved maths (and English) items pack a table into the stem AS raw pipe-markdown
    (e.g. `| 283 | ___ | 285 | ___ |`) while ALSO carrying it — usually more completely,
    with its header row — in `visual_stimulus`. The renderer shows the stem verbatim, so the
    figures appear TWICE: once as raw pipe text, once as the typed table. A table belongs in
    `visual_stimulus`, never as prose in the stem (mirrors normalize.py's typed-stimulus rule
    and the English FILL_IN anti-duplication constitution rule). So: if the stem's pipe lines
    form a table, drop them from the stem; when no stimulus carries the table yet, promote the
    stem's table into `visual_stimulus` (never overwrite a stimulus that already exists — the
    authored one is authoritative and typically more complete). Structural, at the same
    normalization point maths MCQ / English were stabilized — every saved plan reads clean
    without regeneration."""
    stem = n.stem or ""
    if "|" not in stem:
        return
    lines = stem.splitlines()
    pipe_lines = [ln for ln in lines if "|" in ln]
    block = typed_block("\n".join(pipe_lines))
    if not block or block.get("type") != StimulusType.TABLE.value:
        return  # the pipe lines are not a table — leave the stem untouched
    n.stem = re.sub(r"\n{2,}", "\n", "\n".join(ln for ln in lines if "|" not in ln)).strip()
    if not n.visual_stimulus:
        n.visual_stimulus = block


def _finish(n: NormalizedItem) -> NormalizedItem:
    """Shared tail: table-in-stem dedup + template lookup + EXTRACT_ANALYSIS passage routing +
    structuring any numbered/lettered list packed into the stem or the answer key (once, for
    every family)."""
    _dedupe_stem_table(n)
    n.template = RENDER_TEMPLATE.get(n.question_type, "")
    if n.question_type in ("EXTRACT_ANALYSIS", "SOURCE_INTERPRETATION") and n.visual_stimulus:
        n.passage, n.visual_stimulus = n.visual_stimulus, None
    n.stem_lead, n.stem_parts = split_parts(n.stem)
    n.answer_lead, n.answer_parts = split_parts(n.model_answer)
    n.scaffold_lines = split_scaffold_lines(n.scaffold)
    if n.question_type == "TRUE_FALSE":
        stmts, keep_prose = tf_statements(n.options, n.model_answer)
        if stmts:
            n.tf_statements = stmts
            if not keep_prose:                 # justifications folded into the key
                n.model_answer = None
                n.answer_lead, n.answer_parts = "", []
        else:                                  # degenerate (no options) → legacy MCQ card path
            n.template = "selected_response"
    return n


def _link(n: NormalizedItem, meta: Dict[str, Any]) -> NormalizedItem:
    """Copy the stamped link contract in — call AFTER link_resolver.stamp(meta, …)."""
    n.linked_periods = list(meta.get("linked_periods") or [])
    n.anchor_period = meta.get("anchor_period")
    n.linked_lo = meta.get("linked_lo") or None
    return n


# ── family builders (spec §4 master mapping) ─────────────────────────────────────
_FLAT_GUIDE_KEYS = ("what_each_option_reveals", "inclusivity") + _OT_GUIDE_KEYS


def from_constitution(it: Dict[str, Any], meta: Dict[str, Any]) -> NormalizedItem:
    """Science (both stages), Social Sciences, TWAU.

    Canonical guide shape: nested under the item's own type key
    (`guide.MCQ.what_each_option_reveals`) — since 2026-07-10 all three constitutions
    specify it (SS v1.7 / TWAU v1.3 amended from their earlier FLAT shape, mirroring the
    English MCQ-reveals fix) and the saved corpus was migrated in place (pure relocation).
    The FLAT read below is kept as a legacy fallback only — corpus-unused, exercised by
    nothing current, tolerated for any stray pre-migration file. SS/TWAU duplicate SCR/ECR
    rubrics into the guide, but the top-level fields carry them too, so the top-level read
    below stays the single source for those."""
    qt = str(it.get("question_type") or "")
    guide = it.get("guide") if isinstance(it.get("guide"), dict) else {}
    gd = guide.get(qt) if isinstance(guide.get(qt), dict) else None
    if gd is None and any(k in guide for k in _FLAT_GUIDE_KEYS):
        gd = guide                      # the SS/TWAU flat shape
    gd = gd or {}
    reveals = _reveals(gd.get("what_each_option_reveals"))
    if not reveals and qt == "MCQ":
        # True last resort for shapes carrying neither guide form: the SS/TWAU `annotation`
        # prose (a per-item marking note) lands under the same "note" fallback key as
        # legacy English MCQs and renders as prose.
        note = _clean(it.get("annotation"))
        if note:
            reveals = {"note": note}
    # SOURCE_INTERPRETATION (SS secondary v2.7) packs its real questions in a structured
    # `sub_questions[]` and its marking surface in `guide.<TYPE>.sub_question_expectations`.
    # Fold the sub-questions into the stem as a "(a) … (b) …" list so the existing split_parts
    # machinery structures them into stem_parts (no new field / renderer path), and surface the
    # per-part expectations as expected_elements — the passage template's marking block.
    stem = str(it.get("question_text") or it.get("task") or "")
    subs = it.get("sub_questions")
    if isinstance(subs, list) and subs:
        parts = [f"({s.get('label') or chr(97 + i)}) {str(s.get('text') or '').strip()}"
                 for i, s in enumerate(subs) if isinstance(s, dict) and s.get("text")]
        if parts:
            stem = (stem + "\n" + "\n".join(parts)).strip() if stem else "\n".join(parts)
    expected = as_list(it.get("expected_elements")) or as_list(gd.get("sub_question_expectations"))
    n = NormalizedItem(
        question_type=qt,
        id=_clean(it.get("id")),
        stem=stem,
        visual_stimulus=typed_block(it.get("visual_stimulus")),
        options=structured_options(it.get("options")),
        expected_elements=expected,
        option_reveals=reveals,
        look_fors=as_list(it.get("look_for")),
        scaffold=_clean(it.get("scaffold")),
        format_of_output=as_list(it.get("format_of_output")),
        open_task_guide=_ot_guide(gd) if qt == "OPEN_TASK" else None,
        # SS edge-model assessments (and TWAU) carry inclusivity as a TOP-LEVEL item field;
        # older/other shapes tuck it in the guide block. Read top level first, guide as fallback.
        inclusivity=_clean(it.get("inclusivity")) or _clean(gd.get("inclusivity")),
        cognitive_demand=_clean(it.get("cognitive_demand")),
        competency=_competency(it.get("competency")),
    )
    return _finish(_link(n, meta))


_NUM_RE = re.compile(r"-?\d+(?:\.\d+)?$")
_PLACEHOLDER_RE = re.compile(r"^[.…_\-\s]+$")   # "...", "…", "___", "-", blank tick


_NL_TAG = re.compile(r"^\s*number[_ ]?line\s*:\s*", re.I)   # constitution Rule 7 form


_MAX_TICK_LABEL = 16      # a tick carries a LABEL; anything longer is a sentence, not a tick


def _nl_block(raw: str, cells: List[str], instruction: str) -> Optional[Dict[str, Any]]:
    """Build a tick-line stimulus from parsed cells; None if the cells are not a tick line.

    THE TEST IS STRUCTURAL, NOT NUMERIC (2026-08-11, founder-directed at S8's C4).
    It used to demand >=2 NUMERIC cells with every cell numeric-or-placeholder. That was a
    leftover from before the `number_line:` tag existed, when typing had to be *guessed* from
    a bare pipe row and the numerals were the only thing distinguishing a number line from a
    table. Since the tag arrived, intent is DECLARED — `_maths_number_line` reads the tag and
    never guesses — so re-deriving intent from cell type is both redundant and wrong: it
    rejected maths III ch 5 Q-C-4, an alternating shape pattern
    (`number_line: line | curve | line | curve | ... `), which then fell through to TABLE and
    printed the literal tag to the teacher (ARV-D-113).

    So what is validated now is only what the RENDERER needs: a single row of at least three
    short cells. Both renderers are already label-agnostic — `ANumberLine` draws `t.label` as
    SVG text, `export_assessment_pdf` joins the labels with " · " — so word labels needed no
    display work at all. Numbers still behave exactly as before; they are simply no longer
    required.

    The `number_line` KEY is deliberately kept though it is now a slight misnomer: it is wired
    through `StimulusType`, both renderers, both exports, both maths constitutions and the
    back-filled ch_06 corpus, and renaming would ripple a long way for no behavioural gain.
    Read it as "tick line".

    A cell that is a PLACEHOLDER ("...", "___") stays an unlabelled tick, as it always did —
    that is what the student fills in.
    """
    if len(cells) < 3:
        return None
    if any(len(c) > _MAX_TICK_LABEL for c in cells):
        return None
    nl: Dict[str, Any] = {
        "ticks": [{"label": "" if _PLACEHOLDER_RE.match(c) else c} for c in cells]}
    if instruction:
        nl["instruction"] = instruction
    return {"type": StimulusType.NUMBER_LINE.value, "content": raw, "number_line": nl}


def _maths_number_line(raw: Any) -> Optional[Dict[str, Any]]:
    """MATHS-ONLY: re-type a number-line stimulus into an ordered tick line the renderer draws as
    a line, not a grid (the SHARED classifier stays subject-agnostic).

    The stimulus is the constitution Rule 7 form — a line tagged `number_line:` then the ticks
    split by "|" (each a number = labelled tick, or "..." = blank tick). Intent is DECLARED at
    source, so we read the tag and never guess: an untagged pipe row is left to the ordinary table
    typing (a header-less numeric row is non-compliant per Rule 7 and simply shows as a table,
    rather than being silently re-typed)."""
    if not isinstance(raw, str):
        return None
    m = _NL_TAG.match(raw)
    if not m:
        return None
    parts = raw[m.end():].splitlines()
    cells = [c.strip() for c in (parts[0] if parts else "").split("|") if c.strip()]
    instruction = " ".join(ln.strip() for ln in parts[1:] if ln.strip()).strip()
    return _nl_block(raw, cells, instruction)


def _maths_typed_block(raw: Any) -> Optional[Dict[str, Any]]:
    """Stimulus typing for the maths family: try the tick-line override first, else fall back
    to the shared typing (svg / table / prose).

    A TAGGED STIMULUS MUST NEVER DEGRADE SILENTLY (2026-08-11, ARV-D-113). Before this, a
    stimulus that carried `number_line:` but failed the tick test fell straight into the shared
    typing, which saw pipes and returned a TABLE — with the tag still sitting in `content`, so
    the first cell rendered to the teacher as the literal string "number_line: line", on screen
    and in the PDF alike. Two corrections, both here rather than in the renderers, so every
    consumer inherits them:

      * the tag is STRIPPED from the fallback content — an internal token can never reach a
        teacher, whatever the fallback turns out to be;
      * a tagged single row falls to PROSE, not TABLE. A one-row pipe list is not a table, and
        boxing it as one was always the wrong shape; a multi-row payload still types as a table
        because that is what it is.

    The fallback is now also OBSERVABLE rather than silent: `mistyped_tag()` below reports it,
    and `build_library.py` gates on that so a mis-tagged stimulus stops the run instead of
    being found by eye at a C-step.
    """
    nl = _maths_number_line(raw)
    if nl:
        return nl
    if isinstance(raw, str):
        m = _NL_TAG.match(raw)
        if m:
            stripped = raw[m.end():]
            body = [ln for ln in stripped.splitlines() if ln.strip()]
            if len(body) <= 1:
                return {"type": StimulusType.PROSE.value, "content": stripped.strip()}
            return typed_block(stripped)
    return typed_block(raw)


def mistyped_tag(raw: Any) -> Optional[str]:
    """Non-empty reason when a stimulus DECLARES a type it does not satisfy, else None.

    The point of a declared tag is that it removes guessing — which only holds if a tag that
    fails its own contract is loud. This is the reporting half; `genon/build_library.py` turns
    it into a gate. Kept beside the typing it checks so the two cannot drift.
    """
    if not isinstance(raw, str):
        return None
    m = _NL_TAG.match(raw)
    if not m or _maths_number_line(raw):
        return None
    parts = raw[m.end():].splitlines()
    cells = [c.strip() for c in (parts[0] if parts else "").split("|") if c.strip()]
    if len(cells) < 3:
        return f"tagged `number_line:` but has only {len(cells)} tick cell(s); at least 3 are needed"
    long = [c for c in cells if len(c) > _MAX_TICK_LABEL]
    if long:
        return (f"tagged `number_line:` but {len(long)} cell(s) exceed {_MAX_TICK_LABEL} chars "
                f"— a tick carries a label, not a sentence: {long[0][:40]!r}")
    return "tagged `number_line:` but does not parse as a tick line"


def _inclusivity(v: Any) -> Optional[str]:
    """Maths middle/prep author inclusivity as an OBJECT — `{support, challenge}` (middle's
    Rule 6: "an OBJECT with two keys, each ONE short clause"). Every other stage authors a
    sentence.

    `_clean` calls `str()`, so the object arrived at the screen as its Python repr —
    `{'support': 'Let the student…', 'challenge': 'Name one more property…'}`, braces, keys
    and single quotes and all (2026-08-10, S7). Flattened here to the SAME colon-labelled
    form maths·secondary already emits, so `InclusivityText` bolds the two labels and rows
    them without learning a new shape. Empty halves are dropped rather than labelled blank.
    Shape-based: any mapping carrying either key, never a branch on subject."""
    if isinstance(v, dict):
        parts = []
        for key, label in (("support", "Support"), ("challenge", "Challenge"),
                           ("stretch", "Stretch")):
            s = _clean(v.get(key))
            if s:
                parts.append(f"{label}: {s}")
        return "  ".join(parts) or None
    return _clean(v)


_GOAL_DEMAND = {
    # MIDDLE — assessment Rule 3's `goal`
    "recall": "Recall", "reason": "Reason", "apply": "Apply",
    # PREPARATORY — the same axis under its own name, `intent`, on its own four-way
    # A/B/C/D scale (Explore · Reason · Practise · Solve). Verified on the saved plan
    # `mathematics/iii/ch_06`, whose items carry `intent` and no `goal` at all — which is
    # also how the prototype told the two stages apart at render time
    # (`assessment_pdf_generator.py:117-192`: middle has `goal` and no `intent`).
    "explore": "Explore", "practise": "Practise", "practice": "Practise", "solve": "Solve",
}


def _goal_demand(*values: Any) -> Optional[str]:
    """Maths middle's `goal` / preparatory's `intent` as the Overview's cognitive-demand
    value — the first of them the item actually carries.

    Title-cased only. The word itself is the constitution's own (middle's assessment Rule 3
    names `goal` the item's cognitive level), so nothing is translated into secondary's
    Bloom-ish vocabulary and no scale is claimed to be another. An unrecognised value is
    carried as authored rather than dropped, since a new stage's word is more useful on
    screen than a blank row."""
    for v in values:
        g = _clean(v)
        if g:
            return _GOAL_DEMAND.get(g.strip().lower(), g)
    return None


def _section_label(meta: Dict[str, Any]) -> Optional[str]:
    """The section under test — "section 7.5 — Types of Triangles" — but ONLY where the
    group heading does not already say it.

    Read off `meta`, not the item, and set by the PORT. Both maths stages carry
    `section_ref`/`section_title` on the item, so deriving it here put the row on secondary
    too — where the group heading already IS the section, making it a duplicate, and where
    the closing item rendered "Section: synthesis", leaking the reserved token into
    teacher-facing text. Middle groups by A/B/C cluster instead, so there the section is
    genuinely invisible without this row. Which of the two a stage is, is exactly the kind
    of fact the plugin owns and this module must not infer (CLAUDE.md §3)."""
    return _clean(meta.get("section_label"))


def from_maths(it: Dict[str, Any], meta: Dict[str, Any]) -> NormalizedItem:
    """Mathematics, all stages. Middle/prep carry the teacher_guide dict; SECONDARY is the
    hybrid (top-level expected_answer/method_one_line + constitution-style guide{TYPE} +
    look_for/expected_elements/scaffold) — both shapes read tolerantly, spec §4 column 2."""
    qt = str(it.get("question_type") or "")
    tg = it.get("teacher_guide") if isinstance(it.get("teacher_guide"), dict) else {}
    gd = (it.get("guide") or {}).get(qt) or {}
    ex = it.get("exercise") if isinstance(it.get("exercise"), dict) else {}
    ref = _clean(ex.get("book_ref"))
    desc = _clean(ex.get("description"))
    n = NormalizedItem(
        question_type=qt,
        id=_clean(it.get("id")),
        stem=str(it.get("prompt") or it.get("question_text") or it.get("task") or ""),
        visual_stimulus=_maths_typed_block(it.get("visual_stimulus")),
        options=structured_options(it.get("options")),
        # MCQ answer = the ✓ option + what-each-choice-reveals (as English/constitution do).
        # Maths generation ALSO emits `expected_answer` ("Option A — …") for MCQ, which just
        # restates the ticked option and triplicates the Answer tab (CORRECT ANSWER · ANSWER ·
        # reveals). Drop it for MCQ — structural, at the same normalization point English was
        # stabilized — so every saved maths MCQ reads clean without regeneration. Kept for
        # every other type (NUM worked answer, SCR/ECR suggested answer, TRUE_FALSE verdict).
        model_answer=(None if qt == "MCQ"
                      else _clean(tg.get("expected_answer")) or _clean(it.get("expected_answer"))),
        expected_elements=as_list(it.get("expected_elements")),
        option_reveals=_reveals(tg.get("what_each_option_reveals")) or _reveals(gd.get("what_each_option_reveals")),
        look_fors=as_list(it.get("look_for")),
        scaffold=_clean(it.get("scaffold")),
        method_one_line=_clean(tg.get("method_one_line")) or _clean(it.get("method_one_line")),
        format_of_output=as_list(it.get("format_of_output")),
        open_task_guide=_ot_guide(gd) if qt == "OPEN_TASK" else None,
        # book_ref (the BOOK ITEM) and description carried SEPARATELY, not pre-joined: the ref
        # itself can contain " — " (e.g. "Let us Play — Flag game, p.69"), so a joined string is
        # unsplittable downstream. The renderer bolds the ref and shows the description after.
        exercise_ref=ref,
        exercise_desc=desc,
        inclusivity=_inclusivity(tg.get("inclusivity")) or _inclusivity(gd.get("inclusivity")),
        # SECONDARY emits `cognitive_demand` ("Analysis"). MIDDLE and PREPARATORY emit
        # `goal` — recall | reason | apply — and their own constitution calls it the
        # cognitive level in terms: assessment Rule 3, "The prompt's cognitive level MUST
        # match `goal`: recall → retrieve a fact, definition or directly-stated property;
        # reason → construct an argument, justify a claim, or derive a relationship; apply
        # → use a chapter procedure in a fresh numerical, geometric, or word context."
        #
        # So this is ONE field under two names, not two ideas (2026-08-10, S7 — the same
        # normalize-at-the-seam move `unit_approaches` makes for the five spellings of the
        # LP's approach line). Before it, a maths·middle item's Overview panel rendered a
        # single row — "Question type" — because Competency is forbidden at this stage by
        # LP Rule 8, `linked_lo` is null by 8-rule row 4, and `cognitive_demand` is a
        # secondary-only key. Three of its four rows were structurally empty and the panel
        # read as bare. Nothing here is invented: `goal` is authored, per item, and already
        # governs the prompt.
        cognitive_demand=(_clean(it.get("cognitive_demand"))
                          or _goal_demand(it.get("goal"), it.get("intent"))),
        competency=_competency(it.get("competency")),
        # The section under test, where the item names one. Middle/prep carry both halves
        # verbatim from the LP handoff; the handoff-bridged stages carry neither and this
        # stays None, so their panel is unchanged.
        section=_section_label(meta),
    )
    return _finish(_link(n, meta))


def from_english(it: Dict[str, Any], meta: Dict[str, Any]) -> NormalizedItem:
    """English, all stages."""
    qt = str(it.get("question_type") or "")
    tg = it.get("teacher_guide") if isinstance(it.get("teacher_guide"), dict) else {}
    note = _clean(tg.get("note"))
    reveals = _reveals(tg.get("what_each_option_reveals"))
    if not reveals and qt == "MCQ" and note:
        reveals = {"note": note}          # legacy prose fallback, rendered as prose
    model = _clean(tg.get("suggested_answer"))
    if not model and qt == "TRUE_FALSE" and note:
        model = note                      # TRUE_FALSE verdict+justification → model_answer
    spine = str(it.get("source_spine") or "").lower()
    n = NormalizedItem(
        question_type=qt,
        id=_clean(it.get("id")),
        stem=str(it.get("item_stem") or it.get("question_text") or ""),
        visual_stimulus=typed_block(it.get("visual_stimulus")),
        options=structured_options(it.get("options")),
        audio_ref=_clean(it.get("transcript_ref")) if "listening" in spine else None,
        model_answer=model,
        expected_elements=as_list(tg.get("expected_elements")),
        option_reveals=reveals,
        cognitive_demand=_clean(it.get("cognitive_demand")),   # ""/absent → None (all English)
    )
    if qt == "MATCH":
        n.match_pairs = match_pairs_from(tg.get("answer_key"))
    return _finish(_link(n, meta))
