#!/usr/bin/env python3
"""S4 · `source_sections` — the multi-section attribution for end-of-chapter items.

FOLDED INTO LP v1.2, not a new bump: the Rule 12 amendment landed minutes earlier in the same
session and NOTHING has been authored against v1.2 yet, so one version carries both changes.

WHY (founder ruling 2026-08-09, from the maths·IX ch 4 pilot).
`cowork prompts/mathematics/secondary/step_1_chapter_summary.md` gave two rules that cannot
both be satisfied: enumerate the end-of-chapter question set (lines 51-54), AND "every
enumerated item's `source_section` is a `ref` present in `sections`" (line 162). End-of-chapter
questions belong to no numbered section, so the model MUST attribute them falsely. All 8
maths·IX summaries do — 69 items — and ch 4's collapse onto 4.1 is what surfaced it, because
it put three consolidation units under the "Introduction" label on the teacher's screen.

Nor is a single value enough once the false attribution is removed: the end-of-chapter set is
deliberately omnibus. Ch 4's E-13 spans binomial squares, difference of squares AND a binomial
cube; E-14 mixes 17x21 with 147^3; E-15 covers eleven expressions "including sum/difference-of-
cubes and three-term-cube forms". Any single ref is a lie about most of the block.

THE SHAPE, chosen to be backward compatible — no code reads this field today (verified by grep
across aruvi_core/, api/, genon/, web/app/; the english `source_section_id` hits are a different
field), and every existing summary stays valid:
  * `source_section`  — RETAINED and still required. For a single-section item it is the
                        section. For a multi-section item it is the DOMINANT one, so any
                        reader that wants one value still gets a defensible one.
  * `source_sections` — NEW, optional. Present only when an item genuinely exercises more than
                        one section. Lists every section it exercises, in section order, and
                        its first element equals `source_section`.
The LP may then anchor a consolidation unit on the real list (V2 already supports joining
several sections with " / "), instead of inheriting one false ref.

Run from the repo root:
    python3 genon/out/stage_prep_mathematics_secondary/apply_s4_source_sections.py
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
LP = ROOT / "data/content/constitutions/lesson_plan/mathematics/secondary/lesson_plan_constitution.txt"
PROMPT = ROOT / "cowork prompts/mathematics/secondary/step_1_chapter_summary.md"

edits = []


def sub(path_text, old, new, label):
    n = path_text.count(old)
    if n != 1:
        raise SystemExit(f"ABORT [{label}]: anchor found {n} times, expected 1\n---\n{old[:260]}")
    edits.append(label)
    return path_text.replace(old, new, 1)


# ── 1 · the LP schema (A3) learns the field ──────────────────────────────────
lp = LP.read_text()
lp = sub(
    lp,
    '            "source_section": "string — e.g. \'2.5\'",\n',
    '            "source_section": "string — the section this item MAINLY exercises, e.g. \'2.5\'",\n'
    '            "source_sections": "[string] | absent — copied from the summary when the item\n'
    "                                exercises several sections (the end-of-chapter set usually\n"
    "                                does); section order, first element equals source_section.\n"
    '                                A unit built on such items anchors on these sections",\n',
    "A3 textbook_items_in_class · source_sections")
LP.write_text(lp)

# ── 2 · the authoring prompt: resolve the contradiction ──────────────────────
p = PROMPT.read_text()

p = sub(
    p,
    '- **Exercises** → `{ "id": "E-N", "source_section", "book_ref", "description" }`\n'
    "  Every numbered question a student is asked to do: the questions under a\n"
    "  section's practice-exercise banner, and the questions in the\n"
    "  end-of-chapter exercise set. Each numbered question is one `E-N`.\n",

    '- **Exercises** → `{ "id": "E-N", "source_section", "source_sections"?, "book_ref", "description" }`\n'
    "  Every numbered question a student is asked to do: the questions under a\n"
    "  section's practice-exercise banner, and the questions in the\n"
    "  end-of-chapter exercise set. Each numbered question is one `E-N`.\n"
    "\n"
    "  **End-of-chapter questions belong to no single section, and MUST NOT be\n"
    "  parked on one.** They are written to draw on the chapter as a whole. Read\n"
    "  each one and record the sections whose method it actually exercises:\n"
    "  `source_sections` lists them all in section order, and `source_section`\n"
    "  carries the DOMINANT one (its first element). A question that genuinely\n"
    "  tests one section names that section in both, and may omit\n"
    "  `source_sections`. Never choose a section by position — not the first, not\n"
    "  the last — and never because a value is required.\n",
    "prompt · exercises item shape + the EoC rule")

p = sub(
    p,
    '    { "id": "E-1", "source_section": "2.1", "book_ref": "Exercise 2.1 Q1, p.18", "description": "..." }\n',
    '    { "id": "E-1", "source_section": "2.1", "book_ref": "Exercise 2.1 Q1, p.18", "description": "..." },\n'
    '    { "id": "E-9", "source_section": "2.3", "source_sections": ["2.3", "2.5"],\n'
    '      "book_ref": "End of Chapter Q4, p.31", "description": "..." }\n',
    "prompt · JSON example gains an EoC item")

p = sub(
    p,
    "- Every enumerated item's `source_section` is a `ref` present in `sections`.\n",
    "- Every enumerated item's `source_section` is a `ref` present in `sections`, and is the\n"
    "  section the item MAINLY exercises — never a placeholder chosen because the field is\n"
    "  required.\n"
    "- `source_sections`, where present, is a list of `ref`s present in `sections`, in section\n"
    "  order, whose first element equals `source_section`. Required for any end-of-chapter\n"
    "  question that exercises more than one section; omitted for single-section items.\n",
    "prompt · rules")

PROMPT.write_text(p)

print(f"OK — {len(edits)} edits applied:")
for e in edits:
    print(f"  · {e}")
print("\nLP stays at VERSION 1.2 (nothing authored against it yet; one bump carries both changes).")
