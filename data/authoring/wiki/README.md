# Aruvi curriculum wiki — pilot (theme: WATER), 2026-09-02

A concept layer over the chapter summaries in `data/authoring/chapters/`. One theme was traced
end to end to show the mechanism; nothing here is wired into the app or the runtime.
**This folder is founder-secure** (it is derived from the authoring summaries, which `api/` and
`aruvi_core/` may never read — CLAUDE.md §7). If a teacher-facing wiki is ever wanted, that is a
promotion decision recorded in CLOUD_DATA_MODEL.md first.

## Open it

- **`wiki.html`** — double-click. A single file, no server, works offline; left rail lists
  every page, the search box filters it. Fonts load from Google if online, else serif fallbacks.
- **Obsidian** — File › Open vault › choose this folder. Every `[[link]]` resolves; the graph
  view (Ctrl/Cmd-G) draws ideas ↔ chapters.

Start at `Water.md`, then the three views under `views/`.

## What was built, in numbers

| | |
|---|---|
| Chapters scanned | 324 (all subjects, Classes 3–9) |
| Chapters flagged by keyword scan | 52 |
| Chapters that actually teach or use a water idea | 48 (4 read and set aside, listed at the foot of `Water.md`) |
| Fixed vocabulary of ideas | 11 |
| Concept nodes (chapter × idea, with role + one-sentence statement + section ref) | 142 |
| Joint-class candidate cells (same class, ≥ 2 subjects, one idea) | 30 |
| Pages | 67 · dead links 0 |

## How it was made (the pipeline the full build would repeat)

1. **Scan** — keyword count over every summary (`_build/scan_theme.py`; the list of 52 came from
   `water ≥ 7 mentions` plus five hand-adds).
2. **Extract** — five readers (one per subject) read each flagged summary in full against
   `_build/INSTRUCTIONS.md`: a FIXED vocabulary of 11 ids, three roles (introduces / extends /
   uses), one grade-level sentence per node, a section reference, and the summary's own
   verbatim cross-grade pointers. Output `_build/water_concepts.json`.
3. **Generate** — `_build/build_wiki.py` turns that JSON into the vault: one page per idea, one
   per chapter, three views, the hub, and the HTML reader. Re-run it after any edit to the JSON.

The vocabulary being fixed **before** extraction is what made canonicalisation trivial here. At
full scale (all ideas, not one theme) that step becomes a real merge — "map scale" vs "scale" vs
"ratio of distances" — and is where founder review belongs.

## Reviewer's queue — judgement calls the readers flagged

Places where the extraction was uncertain, or where the vocabulary did not fit. Each is a
one-line edit in `_build/water_concepts.json` followed by a re-run.

**Vocabulary gaps (a fuller build would add ids):**
- *Water as a chemical substance / reactant* — no id. Filed under `water-as-solvent` in Sci 7 ch 4
  (rusting), Sci 8 ch 8 (electrolysis, H:O 2:1), Sci 9 ch 9 (H₂O bonding, mass ratio).
- *Water as an energy source* (TWAU 5 ch 7 water-wheels, gharaats) — filed under `water-as-resource`.
- *Liquid pressure* (Sci 8 ch 6: tanks, dam bases) — filed under `water-as-resource`.
- *Cyclones / tsunamis* (SS 6 ch 2) — folded into `rain-and-monsoon` / `water-in-society`.
- *Boats and water transport* (Eng 7 ch 1) — folded into `water-in-society`.
- *Karst / chemical weathering* (SS 9 ch 2) — filed under `water-as-solvent`; a geographic use, not a lab one.

**Nodes that may be too generous:**
- Sci 6 ch 7 `rain-and-monsoon` — air-temperature weather measurement only; no water content.
  Kept because the vocabulary lists "weather measurement" there. Drop if the thread should be water-only.
- Eng 5 ch 5 *The Frog* `water-and-life` — borderline; kept because the poem's stated theme is the
  amphibious life.
- TWAU 3 ch 7 `measuring-water` — household use estimated in "mugs", no standard units.

**Role calls worth a second look:**
- `water-cycle` is marked *introduces* at TWAU 3, TWAU 5 AND Sci 6. Each reader took "introduces"
  as "first properly taught at this level"; the statements make the difference visible (concrete
  journey of rainwater → formal cycle with the Sun → condensation mechanism). If the wiki wants
  ONE first-teaching point per idea, the rule needs deciding.
- Eng 5 ch 6 *What a Tank!* `water-as-resource` is marked *uses* per the "English uses, does not
  teach" guidance, but it is an informational text that genuinely describes harvesting structures —
  the strongest English candidate for *introduces*.

**Set aside as incidental (rule 1):** Sci 8 ch 2, Sci 9 ch 11, Maths 5 ch 5, Eng 6 ch 11 — and
inside kept chapters, snow-melt in SS 7 ch 1, monsoon rāgas in SS 7 ch 3, the carbon-footprint
tick-box in SS 9 ch 3, ice stupas in TWAU 5 ch 4, "Muskaan drinks 3 l a day" in Maths 5 ch 8.

## Things the pilot shows that the filing cabinet could not

- **Who teaches, who leans** (`views/cross-subject.md`): Social Sciences *uses* the water cycle
  in Classes 6, 7, 8 and 9 and never teaches it — it is depending on TWAU 3/5 and Science 6/7
  having done so. Same shape for `states-of-water` (SS 9 leans on Sci 6/8).
- **The spiral is visible** (`concepts/water-cycle.md`): rainwater's journey (3) → the formal
  cycle with the Sun as driver (5) → condensation on dust nuclei (6) → transpiration added (7) →
  runoff, infiltration, minerals and the five spheres (9).
- **Joint classes** (`views/joint-classes.md`): 30 cells, e.g. Class 7 — Science *Heat Transfer in
  Nature* + SS *Understanding the Weather* + SS *Climates of India*, all on the water cycle in
  one year; Class 3 — Maths *Filling and Lifting* (litres) + TWAU *Water–A Precious Gift* (mugs).
- **Gaps** show as empty cells in `Water.md`'s coverage table (e.g. `measuring-water` stops at
  Class 8; `states-of-water` has nothing before Class 5).

## Not done / next

- Only one theme. A full build extracts ALL ideas from every chapter (no theme filter), then
  merges vocabulary — that merge is the real work and needs review.
- No Class 10 anywhere; Science/SS below Class 6 are TWAU (deliberate).
- Statements are the readers' words from the summaries, not the textbook's; the summaries are
  the only source used.
