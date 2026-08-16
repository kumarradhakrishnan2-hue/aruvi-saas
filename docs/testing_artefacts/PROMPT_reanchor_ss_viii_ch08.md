# TASK — re-anchor social_sciences · VIII · chapter 8 (World Geography: Some Glimpses)

You are repairing SECTION ANCHORS on one authored lesson-plan artefact. You are NOT rewriting
any teaching content. This is a judgement task with a strict output format.

## Background you need

A chapter's STANDARD canonical is the plan of record. Each unit carries a `section_anchor` —
the chapter section(s) that unit teaches. The platform DERIVES the chapter's section registry
from these anchors, in first-visit order, and every shorter version of the chapter ("compact")
is then required to use those exact names. An anchor is not a caption: it is the key the
serving engine uses to reason about what has been taught before what. A wrong anchor is
therefore a wrong answer to "what has this class already been taught?".

## The defect

This standard's anchors are wrong from U6 onward: most units are labelled with the section
BEFORE the one they actually teach (U8 is labelled "Europe" but teaches the Sahara, the
Savannah and the Nile). It is NOT a clean off-by-one — U12 is labelled "The Australian
Continent" but its own band text says it teaches "the chapter's dedicated mountain-roles
passage in the Asia section". The chapter's own compacts are labelled correctly, which is how
this was found. Do not assume any fixed shift; judge each unit on its evidence.

## Your job

For EACH unit below, decide which section(s) it actually teaches, using the title and the
opening band text as evidence, choosing ONLY from the section list below. Then emit repair
declarations.

## Rules — follow exactly

1. Choose section names VERBATIM from the section list. Never invent, abbreviate or reword one.
2. A unit may teach more than one section. Join names with " / " (space-slash-space). Never
   use ";" or ",".
3. Change NOTHING except the `section_anchor` string. No band, title, note, homework or item.
4. A unit that revisits an earlier section must be anchored to that earlier section. A backward
   revisit is legal and normal — do not stretch it forward to keep the sequence tidy.
5. If the evidence does not clearly support any section in the list, do NOT guess: report it
   under UNRESOLVED.
6. Omit a unit entirely if its current anchor is already correct.
7. U13 is the mandated whole-chapter synthesis unit; its anchor is the reserved token
   `synthesis`. Never change it, and never give that token to any other unit.

## Section list (the ONLY permitted anchor names)
  - Introduction
  - The Complexity of Mapping the Earth
  - The Blue of the Blue Planet, the Oceans
  - The oceans
  - Ocean currents
  - Ocean trenches
  - The Great Barrier Reef
  - Smaller water bodies and waterways
  - The Continents: Variety on Land
  - Asia
  - Europe
  - Africa
  - South America
  - North America
  - The Australian Continent
  - Before we move on …

## The units

### U1
- current anchor: `Introduction`
- title: Reading the Language of Physical Maps
- opening band: Display the physical world map. Ask students: 'Why does this map use so many colours — what might blue mean? What about dark brown near mountain ranges?' Take five or six responses without confirming any. Write the colour terms on the board: blue, green, yellow, brown, dark brown, light yellow, white.…
- teacher note: This unit opens with the chapter's framing questions and map-reading vocabulary, which everything else in the chapter depends on. A common confusion is that green on a physical map means forest or veg…

### U2
- current anchor: `The Complexity of Mapping the Earth`
- title: Why Every World Map Lies — Map Projections Compared
- opening band: Hold up an orange and peel it, then try to press the peel flat on the desk without tearing it. Ask: 'What happens when you try to flatten a curved surface? What would happen if the Earth's surface were peeled the same way?' Establish that the Earth is an oblate spheroid — slightly flattened at the poles — and that showing it on flat paper always introduces distortion.…
- teacher note: Having introduced the map colour language, this unit moves to the deeper problem of why the map itself cannot be trusted as a neutral picture. The most persistent confusion is that students treat 'the…

### U3
- current anchor: `The Blue of the Blue Planet, the Oceans`
- title: The Blue Planet: Oceans as Climate Regulators
- opening band: Ask: 'Early astronauts looking back at Earth called it the blue planet. Why blue, not green or brown?' Take responses, then reveal the data: oceans cover about 71 per cent of the Earth's surface and hold 97 per cent of its water. Ask students to visualise what percentage of the globe's surface they are looking at when they see a full-ocean photograph.…
- teacher note: A common confusion is that rainfall comes directly 'from rivers or clouds' without students connecting moisture to ocean evaporation; the step-by-step mechanism prevents this. The plankton-to-oxygen c…

### U4
- current anchor: `The oceans`
- title: Five Oceans, Currents, and the Deepest Places on Earth
- opening band: Display the five-ocean map. Ask students to locate each ocean and recall one distinguishing feature without prompting. Confirm: Pacific — largest and deepest, home to whales and tuna; Atlantic — busiest waterway for trade and transport, rich fishing ground; Indian Ocean — warm waters, rich biodiversity, historically vital for international trade; Arctic — smallest and shallowest, sea-ice covered, home to polar bears …
- teacher note: Having established the ocean's climate-regulating role through heat absorption and the moisture cycle, this unit applies that logic to moving currents — the Gulf Stream is the clearest case of a named…

### U5
- current anchor: `The Great Barrier Reef`
- title: Reefs, Seas, Gulfs, and Canals — Smaller Marine Formations
- opening band: Define a reef as a ridge at or near the ocean surface, formed by rock or built by tiny animals called corals. Explain that reefs are among the most diverse ecosystems on Earth — often called 'the rainforests of the sea' — providing food and shelter for about a quarter of all ocean species. Introduce the Great Barrier Reef: off Australia's northeastern coast, stretching over 2,000 km, covering about 350,000 square kil…
- teacher note: The Great Barrier Reef's bleaching narrative directly advances the conservation competency first raised in the ocean-pollution plankton discussion. Students often confuse a gulf with a bay; the cleare…

### U6
- current anchor: `The Continents: Variety on Land`
- title: Asia's Roof, Deserts, and Steppes — Landforms of the Largest Continent
- opening band: Open with the chapter's definition: a continent is a large continuous expanse of land, most commonly counted as seven. Introduce the four landform types the tour will encounter — mountains, plateaus, plains, and deserts — defining deserts as large dry expanses with very little precipitation and distinctive flora and fauna. Orient students to the Asia section, noting that the chapter deliberately focuses on parts of t…
- teacher note: The Tibetan Plateau's tectonic origin — Indo-Australian plate colliding with the Eurasian plate — is the same process that raised the Himalayas, and naming that connection helps students build a mecha…

### U7
- current anchor: `Asia`
- title: Urals, the European Plain, and the Alps — Europe's Landform Triangle
- opening band: Introduce the Ural Mountains: an ancient range stretching about 2,500 km from the Arctic Ocean to the Kazakhstan border, forming the natural boundary between Europe and Asia. Rich in iron ore, copper, zinc, platinum, gold, coal, oil, and natural gas. The Urals support coniferous taiga in the west and east, deciduous forest in the south, tundra and swamp in the north, and fertile farmland in the south. Ask: 'Why might…
- teacher note: The Urals section is significant for establishing the Europe–Asia boundary — a frequently confused distinction that students often treat as purely political. The connection between the plain's fertili…

### U8
- current anchor: `Europe`
- title: Africa: Sahara, Savannah, and the Nile
- opening band: Introduce the Sahara as the largest hot desert in the world: temperatures ranging from 30°C to 46°C, rainfall below 25 cm, and scarce vegetation. Describe human and biological adaptation — oases, underground dwellings that stay cool in summer and warm in winter, nomadic clothing and headgear, date palms, water-storing cacti, and the fennec fox's large heat-dissipating ears. Ask: 'What do these adaptations have in com…
- teacher note: The Sahara's adaptation examples are the most vivid illustration in the Africa section of the chapter's broader argument about physical features shaping human life — the fennec fox's ears and undergro…

### U9
- current anchor: `Africa`
- title: Andes, Amazon, and Atacama — South America's Extremes
- opening band: Introduce the Andes as the continent's largest mountain range on the west coast, home to Mount Aconcagua — the highest peak in the Western Hemisphere — and to Bolivia's Uyuni Salt Flats, the largest salt flat on Earth. The Andes hold reserves of copper, zinc, silver, and lithium, and are a vital freshwater source feeding major rivers including the Amazon. Ask: 'Why would a mountain range be both a water source and a …
- teacher note: The Sahara-to-Amazon phosphorus fact is one of the chapter's most striking interdependence examples — use it to illustrate that physical geography operates across vast distances, not just locally. A c…

### U10
- current anchor: `South America`
- title: Colorado Plateau, Rockies, Appalachians, and Great Lakes — North America
- opening band: Introduce the Colorado Plateau: a large highland in the southwestern United States covering over 330,000 square km, composed mostly of sedimentary rock layers slowly uplifted by tectonic forces and shaped by erosion over millions of years, creating dramatic red rock formations and deep canyons including the Grand Canyon. It is rich in coal, oil, natural gas, uranium, and copper, and the Grand Canyon draws about 5 mil…
- teacher note: The Yellowstone wolf-reintroduction story is the chapter's clearest example of deliberate ecosystem restoration producing a cascade of positive effects — students can trace the causal chain (wolves → …

### U11
- current anchor: `North America`
- title: Australia's Deserts, the Spinifex People, and Antarctica
- opening band: Establish the chapter's corrective point before diving into detail: not all deserts are hot. Use Antarctica as the opening case — the largest and coldest desert on Earth, covering over 14 million square kilometres, more than four times the area of India, and colder than the Arctic. Ask: 'Given what we have established about what makes something a desert — less than 25 cm of precipitation a year — why does Antarctica …
- teacher note: The Antarctica-as-desert point is the chapter's most counter-intuitive definition, and students almost invariably resist it — holding firm to the precipitation criterion (less than 25 cm per year) rat…

### U12
- current anchor: `The Australian Continent`
- title: Mountains as Water Towers, Boundaries, and Biodiversity Hotspots
- opening band: This unit focuses on the chapter's dedicated mountain-roles passage in the Asia section: mountains are formed by tectonic forces, volcanic activity, and erosion; they shape climates, act as 'water towers', form biodiversity hotspots, and often serve as natural boundaries. Present these four roles explicitly on the board. Ask students to propose one mountain range from anywhere in the chapter that they think illustrat…
- teacher note: The chapter's four mountain-roles framework is the closest the Asia section comes to an explicit analytical task — the Himalayas assessment is the chapter's own prescribed activity and should be compl…

### U13
- current anchor: `synthesis`
- title: Earth's Features, Human Futures — Whole-Chapter Synthesis
- opening band: Open by displaying the physical world map and posing three questions from the chapter's own frame: 'What are the unique physical features of the continents? Why does world geography need to be understood? How do human actions trigger environmental issues?' Ask students to call out — without notes — one physical feature and one human-geography link from any part of the world. Record responses on the board as a rapid k…
- teacher note: This synthesis draws on the full range of landforms, water bodies, and human-geography connections developed across the chapter — the Tibetan Plateau's tectonic formation and glacier melt, the Europea…

## Output format — exactly this, nothing before or after

For each unit you are changing, one Python tuple, in unit order:

```python
    (UNIT_NUMBER,
     "CURRENT ANCHOR STRING, VERBATIM",
     "CORRECTED ANCHOR STRING",
     "V2/mis-anchored",
     "one sentence: what the unit actually teaches, and the words in the band or title that "
     "prove it"),
```

Then two short sections after the code block:

**UNRESOLVED** — any unit you could not decide, and what you would need in order to decide it.

**SEQUENCE CHECK** — list your corrected anchors in unit order and state whether each section's
FIRST appearance follows the section list's own order. If one appears out of order, say so
plainly rather than adjusting an anchor to hide it.