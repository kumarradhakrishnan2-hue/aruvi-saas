# Water-thread concept extraction — instructions for extractors

You are extracting **concept nodes** from Aruvi chapter summaries for a pilot curriculum wiki
on the theme **WATER**. Read each assigned chapter summary in full, then record which of the
fixed water sub-concepts below the chapter actually teaches or substantively uses.

## Where the files are

Chapter summaries: `/tmp/aruvi/authoring/chapters/{subject}/{grade}/summaries/ch_NN_summary.txt`
(Science, Social Sciences — prose) or `.json` (Mathematics, English, The World Around Us —
structured; read every string field, the prose is in `prose_summary` / `tasks` / `tasks_verbatim`).
Read them with `cat` / `python3` via the bash tool. Do NOT edit them.

## The fixed concept vocabulary (use ONLY these ids)

| id | meaning |
|---|---|
| `states-of-water` | solid/liquid/gas; melting, freezing, evaporation, condensation, boiling; ice/steam/vapour |
| `water-cycle` | evaporation → clouds → precipitation → collection; the sun as driver; the cycle as a system |
| `rain-and-monsoon` | rainfall, monsoon winds, seasons, climate patterns, humidity, weather measurement |
| `rivers-and-landforms` | rivers source-to-sea, erosion/deposition, valleys, deltas, floods, glaciers as water |
| `oceans-and-water-bodies` | oceans, seas, lakes, ponds; how water is distributed on Earth; tides, currents |
| `water-as-resource` | sources of water, scarcity, conservation, rainwater harvesting, wells/tanks/dams, irrigation, supply |
| `water-and-life` | water in the body, plants absorbing/transpiring water, aquatic habitats, drinking water and health, sanitation |
| `water-as-solvent` | dissolving, solutions, mixtures, purification and separation (filtration, distillation, evaporation to recover salt) |
| `measuring-water` | capacity/volume in litres, weighing liquids, measuring water temperature |
| `water-and-heat` | heating/cooling water, convection, sea/land breezes, water's role in heat transfer |
| `water-in-society` | civilisations by rivers, water in architecture (stepwells, tanks), urban water supply, community water disputes, water in stories/poems |

If a chapter's water content does not fit any id, put it under the nearest one and say so
in the statement. Do NOT invent new ids.

## Role — one per (chapter, concept)

- `introduces` — the chapter is where this idea is first properly taught at this level (defines it, builds it).
- `extends` — the chapter assumes the idea and takes it further (adds mechanism, precision, new cases).
- `uses` — the chapter relies on the idea as context or example but does not teach it.

## Rules

1. **Be strict.** Only record a concept if the summary shows the chapter genuinely teaches or
   substantively uses it. An incidental mention ("students bring water bottles") is NOT a node.
   A chapter with no real water content gets `"concepts": []` and a one-line `skip_reason`.
2. **Quote the level.** Each `statement` is ONE sentence, in plain language, saying what THIS
   chapter says about the concept at THIS grade — specific enough that reading the statements
   for one concept across grades shows the idea growing. Good: "Water exists as ice, liquid and
   steam, and heating or cooling moves it between them." Bad: "Discusses states of water."
3. **Cite.** `section_ref` = the section title or task/activity id in the summary the claim rests on.
4. **Cross-links.** If the summary itself points to another grade or subject ("as learnt in
   Grade 6", "links to Geography"), record it verbatim in `explicit_links`.
5. Do not read beyond your assigned list. Do not use outside knowledge of the textbook — only
   what the summary says.

## Output — ONE JSON file

Write `/sessions/inspiring-determined-archimedes/mnt/outputs/wiki_extract/{subject}.json`
(also copy it to `/tmp/aruvi/extract/{subject}.json`, creating the folder). Shape:

```json
{
  "subject": "science",
  "chapters": [
    {
      "grade": "vi",
      "chapter": 8,
      "title": "A Journey through States of Water",
      "source": "authoring/chapters/science/vi/summaries/ch_08_summary.txt",
      "one_line": "What the chapter is about, in one sentence.",
      "concepts": [
        {"id": "states-of-water", "role": "introduces",
         "statement": "…one sentence at this grade's level…",
         "section_ref": "Section: Evaporation and condensation / Activity 8.3"}
      ],
      "explicit_links": ["…verbatim phrase…"],
      "skip_reason": null
    }
  ]
}
```

Validate the JSON parses before finishing. Your final message: the count of chapters with ≥1
concept, the count skipped, and anything that did not fit the vocabulary.
