#!/usr/bin/env python3
"""repair_prose_tables.py — dense enumerable prose visual aids become typed tables (2026-08-19).

FOUNDER DIRECTION (2026-08-19, starting from vi ch 4's 'Shipwreck card content'): the
polish pass left several synthesis-unit visual aids as PROSE whose content is actually a
set of parallel RECORDS — cards, events, scenes, stalls, faults, observations — flattened
into dense text. On screen that reads as a wall of words; in DOCX it is worse (prose
chunks collapse single newlines to spaces, so numbered lists mash into run-on lines).
These become typed TABLE aids ({type: table, title, table}) so all three renderers
(LessonView MaterialPanel, PDF, DOCX) show a real grid.

SCOPE: science·middle only (vi/vii/viii), synthesis units of the top canonicals under
data/content/saved_plans/. 26 aids across 20 chapters convert; genuinely narrative prose
(vi ch5 coverage notes, vi ch11 gap prompts, viii ch11 design questions, scenario/
facilitation paragraphs) stays prose.

DISCIPLINE (per the polish doctrine, CLAUDE.md 2026-08-18: moved, never rewritten):
  * Record labels ('Card 1 –', 'Description:', 'Expected reasoning:', 'STALL 3 —')
    become table STRUCTURE (rows/columns); the content of each field is verbatim, save
    sentence-initial capitalisation and dropped connective boilerplate that the column
    header now states ('Diet is …' under a Diet column).
  * Scene-setting one-liners become the table's leading CAPTION row (parse_table lifts a
    leading narrower row into `caption` — every renderer shows it). Multi-sentence
    format/facilitation text stays as a companion PROSE aid.
  * Titles referenced from teacher_notes/materials pointers ('see visual aid: …') are
    KEPT EXACTLY on the aid that carries the pointed-at content.
  * Each edit asserts the sha1 prefix of the installed prose before replacing — if the
    artefact changed since authoring, the run refuses. Old aid archived under
    genon_canonical.repairs; file backed up; derived plans purged (ARV-D-034).

    python3 genon/repair_prose_tables.py            (dry run: verify + report)
    python3 genon/repair_prose_tables.py --apply
"""
from __future__ import annotations

import hashlib
import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(REPO))
from purge_derived import purge                                    # noqa: E402
from aruvi_core.normalize import parse_table                       # noqa: E402

SAVED = REPO / "data" / "content" / "saved_plans" / "science"
BACKUP = REPO / "backup" / "prose_tables"


def T(title, *lines):
    return {"type": "table", "title": title, "table": "\n".join(lines)}


def P(title, text):
    return {"type": "prose", "title": title, "text": text}


# ── the declared edits: (grade, chapter, visual_aids index, sha1[:10] of the installed
#    prose text) → replacement list of typed aids ─────────────────────────────────────
EDITS = [

 # ─── VI ch 1 · Case File Cards ───
 dict(grade="vi", ch=1, idx=0, sha="fd4893c7d1", new=[
  P("Case File Cards — preparation note",
    "Prepare five cards per group on separate paper strips or quarter-sheets. Cards 1, 3, "
    "and 5 are correct; Cards 2 and 4 contain deliberate errors for students to find and "
    "fix. Shuffle before handing out."),
  T("Case File Cards — text and error guide",
    "Card | Step | Card text | Error to find",
    "1 (correct) | OBSERVATION | 'Meera noticed that the plant on her windowsill, which "
    "she waters every two days, has drooping leaves and a dull colour. She finds this "
    "puzzling because she has been watering it regularly.' | ",
    "2 (error) | QUESTION | 'Meera asks: Why is everything in the world so difficult to "
    "understand? She decides plants are impossible to figure out.' | The question is too "
    "vague and not connected to the specific observation; it cannot be investigated or "
    "turned into a hypothesis because it is not about an observable, specific thing",
    "3 (correct) | HYPOTHESIS | 'Meera guesses that too much water might be drowning the "
    "roots and stopping them from working properly, causing the drooping.' | ",
    "4 (error) | TEST | 'Meera decides to believe her guess is true because she once heard "
    "that overwatering harms plants. She does not do anything further.' | A hypothesis "
    "must be tested by actual observation or experiment, not accepted on hearsay without "
    "investigation",
    "5 (correct) | ANALYSIS | 'Meera checks the soil and finds it soggy even two days "
    "after watering. She reduces watering to once a week. After several days, the leaves "
    "straighten. Her hypothesis was supported; she also wonders whether the pot's "
    "drainage hole is blocked — a new question for a new inquiry.' | "),
  P("Case Closed paragraph prompt",
    "The paragraph should name curiosity, a specific question, a hypothesis, a test, and "
    "the revision of understanding. If a group omits any of these, prompt: 'What step in "
    "the method does this part of the story show?'"),
 ]),

 # ─── VI ch 2 · Habitat-damage scenarios ───
 dict(grade="vi", ch=2, idx=1, sha="2989665c23", new=[
  T("Habitat-damage scenarios",
    "Distribute one slip per pair, cycling across the four types",
    "Slip | Scenario",
    "1 | 'The freshwater pond has dried up.'",
    "2 | 'The coastal forest was cleared for construction.'",
    "3 | 'The dry grassland was converted to farmland.'",
    "4 | 'The river-plain farm was flooded and abandoned.'"),
  P("Habitat-damage scenarios — facilitation note",
    "Every scenario affects at least one organism on the cards and leaves others "
    "unaffected — this forces discriminating prediction. A strong response names a "
    "specific feature: 'The fish is most affected because its aquatic habitat is gone, "
    "and its fins and streamlined body have no function on land; the goat is unaffected "
    "because its legs and dry-grassland source are untouched.' A weak response says only "
    "'the fish will die because it needs water' — push students to name the feature."),
 ]),

 # ─── VI ch 3 · Patient profile cards / data strips / challenge prompts ───
 dict(grade="vi", ch=3, idx=0, sha="7cc098bb59", new=[
  P("Patient profile cards — format note",
    "Each card is hand-written on an index card or half-sheet. It states the patient's "
    "name, age, location and dominant local crop, current typical daily diet, physical "
    "activity level, and one observable symptom or health need described in plain "
    "language. The card does NOT name the deficiency — students must infer it."),
  T("Patient profile cards",
    "Card | Patient & setting | Diet | Activity | Symptom",
    "1 | Child, recovering patient, jowar-growing district | Predominantly jowar-based "
    "with very little green leafy vegetables or pulses | Low activity (bed rest) | Pale "
    "gums and fatigue, tires easily on minor exertion",
    "2 | Teenager, athlete, coastal fishing village | Rice and fish-based but meals are "
    "often skipped before training | High physical activity | Frequent muscle cramps and "
    "slower recovery after exercise",
    "3 | Elderly person, Himalayan town | Relies on locally grown cereals and dairy; "
    "rarely eats processed or iodised products | Low activity | Visible swelling at the "
    "front of the neck, sluggishness",
    "4 | Young mother, sugarcane-farming belt | Heavy in packaged biscuits, instant "
    "noodles, and sweetened drinks; fresh produce is limited | Moderate activity | "
    "Persistent tiredness, dry skin, frequent minor infections",
    "5 | Construction worker, urban area | Skips breakfast and lunch regularly; eats one "
    "large meal at night, often fried street food | High physical activity | Low stamina "
    "during work hours, slow wound healing"),
 ]),
 dict(grade="vi", ch=3, idx=1, sha="0faa01a1d8", new=[
  T("Canteen food-sample data strips",
    "Both strips are identical — every group receives the same two items. Results are "
    "described by behaviour only; the food is not named",
    "Item | Brown-paper test (pressed, held to light) | Iodine test | Copper sulfate + "
    "caustic soda test",
    "Item X | A translucent patch remains | No blue-black colour appears | A "
    "violet-purple colour develops",
    "Item Y | No translucent patch on paper | The sample turns blue-black | No "
    "violet-purple colour appears"),
  P("Canteen data strips — task note",
    "Groups use these results to determine which nutrients (fat, starch, protein) each "
    "item contains and decide whether each item belongs on their patient's tray or "
    "should be limited."),
 ]),
 dict(grade="vi", ch=3, idx=3, sha="2cb8bb4c74", new=[
  T("Cross-patient challenge prompts",
    "Use these two prompts during the gallery interrogation phase. Do not resolve them "
    "for students — steer toward reasoning tied to the chapter's ideas",
    "Challenge | Prompt (read aloud) | Target insight",
    "1 | 'Two patients both need a mineral — the child in the jowar district and the "
    "elder in the Himalayan town. Their minerals are different and their sources are "
    "very different. Why does the solution look so different for each?' | 'Local and "
    "minimally processed' is not a universal rule; some protective nutrients require "
    "fortified or non-plant sources because local soil lacks them. A good comparison is "
    "iron from green leafy vegetables, regionally available, versus iodine from iodised "
    "salt, processed but necessary",
    "2 | 'One group flagged a food-miles risk in their recommendation. Another group's "
    "recommended food travels even further but they did not flag it — should they "
    "have?' | Food-miles reasoning must be applied consistently and weighed against "
    "nutritional necessity; students must articulate the trade-off rather than apply a "
    "blanket rule"),
  P("Gallery logistics and redirects",
    "If groups are more than five, two groups may share a card and compare "
    "recommendations at the gallery stage. During group work, redirect students who "
    "chose regionally implausible foods by asking 'What grows there?' and redirect "
    "students uncertain about test results by asking 'Which test result tells you fat "
    "is present?'"),
 ]),

 # ─── VI ch 4 · Shipwreck cards (the founder's example) ───
 dict(grade="vi", ch=4, idx=0, sha="fee94834ae", new=[
  P("Shipwreck card format note",
    "Each card is printed double-sided: front shows a simple line illustration of the "
    "object and a one-line description; back poses a single focused question about that "
    "object. All eight cards are identical across groups."),
  T("Shipwreck card content",
    "Card | Question | Expected reasoning",
    "1 – Iron nail: a plain iron nail recovered from the crate | Is this nail a magnet, "
    "a magnetic material, or non-magnetic? How do you know? | Attracts to the known "
    "magnet but does not repel either pole → magnetic material, not a magnet",
    "2 – Glass bottle: a sealed glass bottle, contents unclear | Can the bottle or its "
    "contents be classified using your magnet alone? What result would confirm "
    "non-magnetic? | No response to the known magnet → non-magnetic",
    "3 – Unmarked metal rod A: a smooth metal rod with no markings | Test both ends "
    "against the known North pole. What result would prove this rod is a magnet, and "
    "which end is North? | Attracts AND one end repels the known North pole → confirmed "
    "magnet; the end that repels the known North pole is itself a North pole",
    "4 – Unmarked metal rod B: a second smooth metal rod, slightly shorter | This rod "
    "attracts both poles of the known magnet and never repels. What does that tell "
    "you? | Attracts both poles, never repels → magnetic material, not a magnet",
    "5 – Wooden plank fragment: a small fragment of the ship's hull planking | Predict "
    "the result before testing. What property of wood explains your prediction? | No "
    "response → non-magnetic",
    "6 – Unmarked metal rod C: a third metal rod, slightly corroded | Test both ends. "
    "If the opposite end repels, what can you conclude about that end's pole? | "
    "Attracts AND the opposite end repels → confirmed magnet; the end that repels the "
    "known North pole is North; the other end is South",
    "7 – Copper coin: a large copper coin, date worn away | Copper is a metal. Does "
    "that make it magnetic? What result do you expect? | No response → non-magnetic; "
    "being a metal does not guarantee magnetic behaviour",
    "8 – Iron ring: a thick iron ring, possibly a shackle component | The ring attracts "
    "but never repels. Where on the ring would the magnetic force be strongest, and "
    "what does the absence of repulsion tell you? | Attracts, does not repel → magnetic "
    "material, not a magnet; poles (points of strongest force) exist at two points on "
    "the ring — poles always exist in pairs"),
 ]),

 # ─── VI ch 7 · Debrief verdict board guide ───
 dict(grade="vi", ch=7, idx=2, sha="61490efab8", new=[
  P("Debrief Verdict Column — Board Guide",
    "As groups share findings checkpoint by checkpoint, write a running verdict column "
    "on the board using these four labels:\n\nReliable · Unreliable · Needs conversion · "
    "Instrument mismatch\n\nFor each verdict, ask the group to cite the specific chapter "
    "reasoning behind it, not just the answer."),
  T("Key findings to draw out",
    "Log entry | Reasoning to draw out",
    "The 'felt cool' entry | Sensory judgment is not a measurement and cannot "
    "substitute for one",
    "The Kelvin reading (279 K) | Converts to 5.85 °C, which is within the safe range, "
    "but the reading was taken through refrigerator glass without immersion, "
    "introducing error",
    "The clinical thermometer | Designed for body-temperature range; an instrument "
    "mismatch for a refrigerator context",
    "Division value of the van thermometer | (10 °C − 0 °C) ÷ 20 = 0.5 °C per "
    "division. This means the thermometer cannot distinguish 8.5 °C from 8 °C or 9 °C "
    "— a technically functioning instrument that still fails the task because its "
    "precision is insufficient"),
 ]),

 # ─── VI ch 9 · Neighbour's flawed sequence ───
 dict(grade="vi", ch=9, idx=1, sha="b863c759d5", new=[
  T("Neighbour's flawed sequence — error-analysis card",
    "A neighbouring mill owner attempted the same separation in this order",
    "Step | What the neighbour did",
    "1 | Winnowed the dry portion to remove loose husk (the dry heap was spread out and "
    "air was blown across it)",
    "2 | Added water to the remaining heap to dissolve the salt, creating a wet slurry",
    "3 | Filtered the slurry through a cloth to remove pebbles and wheat grains",
    "4 | Attempted magnetic separation on the wet iron bolt fragments in the residue; "
    "found the process very difficult and concluded that the magnet had 'stopped "
    "working', so abandoned this step",
    "5 | Evaporated the filtrate (the salty water that passed through the cloth) to "
    "recover the salt as a solid residue"),
  P("Error-analysis tasks",
    "Your tasks: (i) Identify which step caused the neighbour to struggle and explain "
    "why, naming the property issue precisely. (ii) Write a corrected version of only "
    "the flawed portion of the sequence. (iii) Name the physical change that occurs at "
    "Step 5 and state what is produced."),
 ]),

 # ─── VI ch 11 · Ramnagar decision cards ───
 dict(grade="vi", ch=11, idx=1, sha="a4af971570", new=[
  T("Ramnagar Decision Cards",
    "Card | Proposal",
    "1 | Install rooftop solar panels on the school",
    "2 | Plant a community forest on the deforested hillside",
    "3 | Build a small stepwell to harvest monsoon rain",
    "4 | Switch the brick kilns from coal to natural gas",
    "5 | Introduce CNG three-wheelers for transport",
    "6 | Create a village compost pit using fallen leaves",
    "7 | Use wind energy to pump water from the existing well",
    "8 | Quarry the local granite ridge for new construction material",
    "9 | Ask residents to fix all household tap leaks",
    "10 | Organise a Van Mahotsav tree-planting drive",
    "11 | Install a solar water heater at the community centre",
    "12 | Restrict the number of trees felled each year"),
  P("Decision Cards — selection rules",
    "Groups must choose at least seven cards and may choose all twelve. Every chosen "
    "card requires a written justification. Each of Ramnagar's six problems must be "
    "matched to at least one chosen card — this prevents groups from avoiding "
    "uncomfortable options."),
 ]),

 # ─── VI ch 12 · Postcards + wall-panel annotations ───
 dict(grade="vi", ch=12, idx=0, sha="7b222431f8", new=[
  T("Postcard message cards",
    "Postcard | Message",
    "1 | 'Just after the Sun went down I saw a brilliant white point of light low in "
    "the west. It was much brighter than any star and disappeared below the horizon "
    "after about an hour. What was it, and why is it so bright?'",
    "2 | 'Late at night the sky was so dark I could see a wide, faint, cloudy band "
    "stretching right across from one side of the sky to the other — not a cloud, it "
    "was made of countless tiny lights blurred together. It made me feel very small.'",
    "3 | 'A slow-moving fuzzy smudge had a long bright streak on the side facing away "
    "from where the Sun had set. It was not a shooting star — it moved over several "
    "nights.'",
    "4 | 'I found a group of seven medium-bright stars shaped like a ladle or a dipper. "
    "Two stars at the end of the ladle bowl seemed to point toward one star that never "
    "moved all night, while everything else rotated around it.'"),
  P("Postcard cards — preparation note",
    "Teacher prepares one master set and photocopies, or writes on card stock. Print or "
    "write one postcard per card; distribute all four face-down before turning them "
    "over together."),
 ]),
 dict(grade="vi", ch=12, idx=2, sha="7bf410ec43", new=[
  T("Wall-panel annotation examples",
    "Each reply postcard on the A3 wall panel should be connected by a line to a brief "
    "annotation naming the chapter concept that made the identification possible",
    "Postcard (identification) | Suggested annotation",
    "1 (Venus) | 'Orbit inside Earth's — Venus visible only near horizon at dawn or "
    "dusk'",
    "2 (Milky Way) | 'Solar System is part of Milky Way disc — band visible because we "
    "are inside it'",
    "3 (Comet) | 'Ice and dust evaporate near Sun — comet tail points away from the "
    "Sun'",
    "4 (Polaris) | 'Pole Star nearly stationary above northern axis — used to find "
    "north'"),
  P("Annotations as formative evidence",
    "These annotations are the formative evidence: they show whether students can name "
    "the principle, not just apply it."),
 ]),

 # ─── VII ch 1 · Village well logbook ───
 dict(grade="vii", ch=1, idx=0, sha="303c062dcf", new=[
  T("Village Well Logbook entries",
    "A sequence of roughly twelve short dated entries spanning several decades. Include "
    "the following",
    "Entry | Content",
    "1 | An observation that the water tastes more sour after heavy rain",
    "2 | A note that the iron bucket rusted faster during the monsoon season",
    "3 | A sketch of ice on the stone rim with an embedded question asking why only the "
    "shaded side froze",
    "4 | A retraction entry reading: 'I was wrong last year — the water did not smell "
    "of metal, I had been handling coins.'",
    "5 | A note that a new observer has begun keeping records",
    "6 | An unanswered question asking whether the water level drop in summer is "
    "connected to less rain or to more people drawing water",
    "7 | A final entry noting that the question is still open and inviting whoever "
    "reads this to continue"),
  P("Logbook entries — filling note",
    "The remaining entries may be filled with additional well observations of varying "
    "sharpness — some careful and specific, some vague or inconclusive. The mix of "
    "precise, muddled, retracted, and unanswered entries is intentional and essential."),
 ]),

 # ─── VII ch 2 · Pickle factory data card ───
 dict(grade="vii", ch=2, idx=0, sha="eec9534d9d", new=[
  T("Pickle Factory Data Card",
    "A factory inspector visited a small pickle factory and tested four liquid samples "
    "using indicator papers. The inspector recorded only the colour changes observed",
    "Observation | Sample | Result recorded",
    "1 | Lemon brine from the pickling vat | Turns blue litmus paper red",
    "2 | Equipment rinse solution | Leaves turmeric paper unchanged; turns red litmus "
    "paper blue",
    "3 | Factory drainage water | Produces no colour change in either litmus paper",
    "4 | Stream water downstream of the factory outlet | Turns red rose extract from "
    "red to green"),
  P("Data card — note", "No other information was recorded."),
 ]),

 # ─── VII ch 5 · Casebook events + concept coverage ───
 dict(grade="vii", ch=5, idx=0, sha="c77a86f551", new=[
  T("Casebook: eight change events",
    "Setting: a steel railway bridge in a coastal region, and a controlled-burn forest "
    "management programme in the same region",
    "Event | What happens",
    "1 | Steel bridge girders developing a reddish-brown crust after years of sea spray "
    "exposure",
    "2 | Bridge painters scraping loose surface scale away, changing the shape of the "
    "metal layer but not its identity",
    "3 | A section of rock cliff beneath the bridge splitting along a crack after "
    "repeated wetting and drying cycles",
    "4 | Minerals in the cliff face reacting with dissolved salts in sea spray, "
    "producing a white powdery residue",
    "5 | Forest undergrowth being deliberately set alight — dry leaves and twigs "
    "burning with flame and producing ash, carbon dioxide, and smoke",
    "6 | Larger living trees at the edge of the burn zone losing outer bark but "
    "surviving — bark chars and peels (shape/mass change), tree remains the same "
    "organism",
    "7 | Ash and charred material being washed by rain into a nearby stream, carried "
    "downstream, and settling as a fine layer on the stream bed",
    "8 | The settled ash layer compacting slowly with sand over centuries into a new "
    "sedimentary layer"),
 ]),
 dict(grade="vii", ch=5, idx=2, sha="5c3fe5e947", new=[
  T("Concept coverage across the eight events",
    "Event | Classification and concept",
    "1 (rusting) | Chemical change",
    "2 (scraping scale) | Physical change",
    "3 (freeze-thaw crack) | Physical change",
    "4 (mineral reaction with salt solution) | Chemical change; new white substance "
    "formed",
    "5 (combustion) | Chemical change; fire triangle implicit in conditions; "
    "deliberately desirable in this land-management context, creating productive "
    "tension with the usual hazard framing",
    "6 (bark charring and peeling) | Physical change; tree identity unchanged",
    "7 (ash transport and deposition) | Physical change, erosion and sedimentation",
    "8 (lithification over centuries) | Physical change, irreversible, slow geological "
    "timescale"),
  P("Concept coverage — spread note",
    "This spread ensures every chapter concept has at least one home: physical/chemical "
    "distinction, observable evidence markers (new substance formation vs shape/mass "
    "change only), reversibility, desirability judgement, and slow natural change "
    "across geological time."),
 ]),

 # ─── VII ch 6 · Health fair stalls ───
 dict(grade="vii", ch=6, idx=1, sha="2309d98cb5", new=[
  T("Health Fair Stall Cards",
    "Stall | Offers | Visitor",
    "1 — Voice Check Corner | A microphone and a simple pitch meter for fun | Arjun, "
    "13, notices his voice crackles when he speaks into the mic and sees a slight bulge "
    "at his throat in the mirror next to the stall",
    "2 — Cycle Calendar Stall | Menstrual tracking charts and information on hygiene "
    "products | Meena, 12, recently started her periods and wants to understand the "
    "cycle length and what products she can use",
    "3 — Iron-Strong Station | A display of iron-rich foods (spinach, kidney beans, "
    "dried fruits) and a quiz | Priya, 14, often feels tired; the stall helper asks "
    "whether her periods have started recently",
    "4 — Move and Mood Zone | Short group dance and sport sessions | Rahul, 13, came "
    "because he has been feeling irritable at home and his friend suggested this stall",
    "5 — Why Is This Happening? Corner | A short talk with an illustrated chart of the "
    "brain-signal chain | Divya, 11, wants to know why so many changes are happening to "
    "her body all at once",
    "6 — Choose Strong Stall | Role-play cards where visitors practise refusing peer "
    "pressure to try tobacco or alcohol | Karan, 15, says some friends have been "
    "pressuring him at school"),
 ]),

 # ─── VII ch 7 · Rooftop scenario cards + facilitation ───
 dict(grade="vii", ch=7, idx=0, sha="5b5f4451ad", new=[
  T("Rooftop scenario cards 1–5",
    "Card | Scenario",
    "1 — Metal pipes | Metal water pipes on the roof are scalding to touch by afternoon",
    "2 — Glass greenhouse | A small glass greenhouse on the roof overheats inside",
    "3 — Concrete vs soil | The surrounding concrete pavement stays warm long after "
    "sunset while the garden soil cools quickly",
    "4 — Rainwater loss | Rainwater runs straight off the concrete roof edges and is "
    "lost",
    "5 — Dark shed | Workers sitting near a dark metal storage shed feel uncomfortably "
    "hot even without touching it"),
  P("Group tasks per card",
    "For each card, groups must: (i) name the mode or modes of heat transfer "
    "responsible, (ii) propose one material or structural change grounded in a "
    "heat-transfer principle, and (iii) write one justification sentence."),
 ]),
 dict(grade="vii", ch=7, idx=2, sha="5b3e50a6d4", new=[
  T("Facilitation notes for scenario cards",
    "Card | Facilitation note",
    "5 (dark shed) | Most productive error: students attribute the worker's discomfort "
    "to convection rather than radiation. The worker is not touching the shed and no "
    "air current is described, so radiation is the primary mode. Press with: 'Is there "
    "any material between the shed and the worker that the heat must travel through?'",
    "2 (greenhouse) | Students may explain overheating without distinguishing that "
    "solar radiation enters through the glass while convection of hot air is trapped "
    "inside. Both modes are at work. The fix involves ventilation (convection) or a "
    "light-coloured surface (radiation reflection)",
    "3 (concrete vs soil) | Students may treat soil cooling as a conduction difference "
    "alone rather than also involving differential heat capacity and radiation loss. "
    "Accept both conduction and radiation as valid contributions and reward reasoning "
    "that names both",
    "4 (rainwater) | This card targets infiltration and groundwater recharge rather "
    "than heat transfer directly. Students who connect it to the water cycle driven by "
    "solar radiation are making the chapter's largest synthesis move"),
  P("Closing move",
    "After the shared table is complete, name each chapter thread as it appears in a "
    "cell: conduction through metal pipes, convection in trapped greenhouse air, "
    "radiation from the dark shed, differential heating of soil versus concrete, "
    "infiltration and groundwater recharge driven by the water cycle. The rooftop "
    "needed all of them — not five separate topics but one framework for understanding "
    "how heat moves, through what, and with what consequence for the materials and "
    "water around us."),
 ]),

 # ─── VII ch 8 · Formula reference ───
 dict(grade="vii", ch=8, idx=3, sha="b758c2bb76", new=[
  T("Formula reference — gap-filling rearrangements",
    "Unknown | Rearrangement",
    "Distance | Distance = Speed × Time",
    "Time | Time = Distance ÷ Speed",
    "Speed | Speed = Distance ÷ Time"),
  P("Motion-type reminder",
    "For uniform linear motion: speed is the same across every equal time interval "
    "within the leg.\n\nFor non-uniform linear motion: speed varies across intervals "
    "within the leg."),
 ]),

 # ─── VII ch 11 · Lighthouse scene cards ───
 dict(grade="vii", ch=11, idx=0, sha="f65f54feb3", new=[
  P("Lighthouse scene cards — preparation note",
    "Print or hand-draw one card per scene on index cards or cut paper. Each card "
    "carries a short illustrated description of the situation."),
  T("Lighthouse scene cards",
    "Scene | Situation",
    "1 — The Hidden Lamp | A fishing boat crew cannot see the lighthouse lamp because "
    "a rocky headland lies directly between them and the lamp",
    "2 — The Changing Shadow | A child walking along the harbour wall notices her "
    "shadow on the wall keeps changing size as she moves closer to or farther from the "
    "lamp post",
    "3 — The Foggy Window | A foggy (frosted) window in the keeper's cottage lets "
    "light into the room but makes the view of the sea outside completely blurry",
    "4 — The Backwards Message | A message scratched backwards into a tide-pool rock "
    "reads correctly only when the keeper looks at its reflection in perfectly still "
    "water",
    "5 — The Inverted Sea | A tiny crack in a shuttered room projects an upside-down "
    "image of the sea and sky onto the floor of the room"),
  P("Principles covered across the five scenes",
    "Rectilinear propagation of light; shadow formation and the effect of source "
    "distance on shadow size; transparency and translucency of materials; the pinhole "
    "effect and image inversion; laws of reflection including lateral inversion."),
 ]),

 # ─── VII ch 12 · Keeper's log design pattern ───
 dict(grade="vii", ch=12, idx=0, sha="b2515e9153", new=[
  P("Lighthouse Keeper's Log — twelve monthly entries",
    "Write or print one entry per month. The entries must collectively satisfy the "
    "following design pattern — no entry should name any phenomenon by its scientific "
    "term; the keeper describes only what they observe in plain language."),
  T("Seasonal shadow and daylight pattern",
    "Entry | Observation recorded",
    "June | Noon shadow is short; daylight hours are long (approximately 15–16 h)",
    "December | Noon shadow is long; daylight hours are short (approximately 8–9 h)",
    "March | Noon shadow is at a middle length; daylight and night are approximately "
    "equal",
    "September | Mirrors March — equal day and night, middle shadow length",
    "Remaining eight entries | A gradual and consistent progression between these four "
    "anchor points"),
  P("Constellation entries",
    "Each entry records the constellation visible on the southern horizon at midnight. "
    "The constellation shifts systematically month by month, completing a full cycle "
    "over twelve entries, so that students must invoke revolution (Earth's changing "
    "night-side direction) rather than rotation to explain the shift."),
  T("Unusual-event entries (three entries only)",
    "Entry | Keeper's words | Teacher key",
    "A | 'At midday the Sun vanished — a dark circle covered it completely, two "
    "minutes of darkness. The sea birds went silent. Then it returned.' | This is a "
    "total solar eclipse. The Moon's apparent size equals the Sun's, allowing complete "
    "coverage",
    "B | 'The full Moon turned a deep copper colour and stayed that way for nearly an "
    "hour before brightening again.' | This is a total lunar eclipse; safe to observe "
    "with naked eye. Earth's shadow falls on the Moon",
    "C | 'A tiny black dot appeared on the face of the Sun and crept slowly across it "
    "over several hours.' | This is NOT an eclipse. Venus is physically larger than "
    "the Moon but is so far away that its apparent size is tiny — it cannot cover the "
    "Sun. This entry tests whether students understand apparent size. The chapter's "
    "Solar Eclipse section addresses transits"),
  P("Distribution of unusual events",
    "Place Entry A and Entry B in two different months; place Entry C in a third "
    "month. No two unusual events should fall in the same month."),
 ]),

 # ─── VIII ch 4 · Fault answer guide ───
 dict(grade="viii", ch=4, idx=2, sha="d1131df769", new=[
  T("Fault answer guide (teacher reference)",
    "Fault | Cause | Fix | Concept",
    "1 | The magnetic field around the coil disappears when current stops flowing; the "
    "electromagnet is on only when the circuit is closed | Restore the loose wire "
    "connection so current flows again | Magnetic effect of current; on/off nature of "
    "electromagnets",
    "2 | The number of turns in the coil is a factor controlling electromagnet "
    "strength; fewer turns produce a weaker field | Restore the original number of "
    "turns | Factors affecting electromagnet strength",
    "3 | Wire length and thickness determine resistance and therefore the amount of "
    "heat produced; a shorter, thinner replacement wire has different resistance, "
    "changing how much heat is generated | Replace with a coil matching the original "
    "length and thickness | Factors affecting heating effect — current, material, "
    "length/thickness of wire",
    "4 | Rechargeable batteries degrade after many charge-discharge cycles and "
    "eventually cannot hold enough charge to drive current for a full day | The old "
    "battery must not be thrown overboard; it must be taken to a proper disposal "
    "facility because it may contain acids and toxic materials | Charge-discharge "
    "cycle life of rechargeable batteries; safe disposal",
    "5 | Reversing the battery terminals reverses the direction of current, which "
    "reverses the poles of the electromagnet, so the compass deflects the opposite "
    "way |  | Current direction determines pole orientation of an electromagnet"),
  P("Extension prompt for early finishers",
    "'Which of these five faults would also apply to a dry cell, and which would not, "
    "and why?' — stretches into the dry-cell versus rechargeable distinction."),
 ]),

 # ─── VIII ch 5 · Harbour data log ───
 dict(grade="viii", ch=5, idx=0, sha="0b84728db0", new=[
  T("Harbour data log — five events",
    "Event | Observation",
    "1 — Laden cargo barge | The barge is sitting lower in the water than its normal "
    "load line indicates it should for the declared cargo weight",
    "2 — Ferry at dock | The ferry's steel hull has become magnetised; during docking, "
    "loose nuts and bolts on the concrete apron are being attracted toward the hull "
    "without anyone touching them",
    "3 — Dockworker's trolley | After being given the same push as usual, the trolley "
    "rolls noticeably farther than normal across the concrete apron, which was wetted "
    "by an earlier rain shower",
    "4 — Buoy adrift | A harbour buoy has broken free from its anchor chain and is "
    "floating on the surface, drifting with the current",
    "5 — Crane hook | A crane hook is hanging motionless from a calibrated spring "
    "scale. The scale reads a measurable number of newtons even though nothing is "
    "being lifted"),
 ]),

 # ─── VIII ch 6 · Weather reporter's notebook ───
 dict(grade="viii", ch=6, idx=0, sha="13d99a184e", new=[
  P("Notebook sheet format",
    "Print or hand-write the following as an A4 sheet. Number each observation, leave "
    "blank annotation space beside each, and include a lined dispatch-paragraph box at "
    "the bottom."),
  T("Weather Reporter's Notebook — six observations",
    "No. | Observation",
    "1 | A sudden afternoon sea breeze strengthens along the coast",
    "2 | Rooftop tiles lift off a beachside building",
    "3 | Dark anvil-shaped clouds build overhead",
    "4 | Lightning flashes followed by distant thunder",
    "5 | Storm surge water rises against the harbour wall",
    "6 | A storm warning is issued citing a deepening low-pressure centre offshore"),
  P("Annotation and dispatch prompts",
    "Annotation prompt beside each observation: (i) Which pressure principle is at "
    "work? (ii) What causes what — state the direction of the effect.\n\n"
    "Dispatch-paragraph box prompt: Write one unbroken account — not six separate "
    "explanations — that uses the word 'pressure' or 'pressure difference' as the "
    "connecting thread across every transition. Your reader does not know the science; "
    "every causal step must be stated, not assumed."),
  T("Acceptable annotation content (teacher reference)",
    "Observation | Acceptable annotation",
    "1 | Differential heating of land and sea creates a pressure gradient; cooler, "
    "denser air over the sea is at higher pressure and moves toward the lower-pressure "
    "warm land surface, generating the sea breeze",
    "2 | High-speed wind over the roof reduces pressure above it (speed-pressure "
    "inverse relationship); the higher pressure inside the building exerts a net "
    "upward force that lifts the tiles",
    "3 | Sustained low-pressure updraft draws moist air upward; rapid cooling at "
    "altitude condenses moisture and builds cumulonimbus (anvil) clouds",
    "4 | Vertical movement of ice crystals and water droplets inside the cloud "
    "separates charge; the resulting potential difference discharges as lightning; "
    "thunder is the pressure wave from rapid air expansion along the lightning channel",
    "5 | Reduced atmospheric pressure over the offshore low allows sea surface to "
    "bulge upward; combined with wind-driven water movement, this raises water level "
    "at the harbour wall as storm surge",
    "6 | Continued surface heating and rising air lower central pressure further; "
    "inflowing air is deflected by Earth's rotation, beginning the self-reinforcing "
    "spiral of a cyclone"),
  P("Strong dispatch paragraph features",
    "Opens with a pressure gradient, traces how it generates wind, shows how "
    "high-speed wind reduces pressure above the roof, describes charge separation and "
    "lightning, and ends by explaining how a self-reinforcing low-pressure centre "
    "signals cyclone formation."),
 ]),

 # ─── VIII ch 8 · River water data card ───
 dict(grade="viii", ch=8, idx=0, sha="211076d339", new=[
  T("River water data card",
    "A river water sample was collected downstream from a town. Record the following "
    "observations",
    "No. | Observation",
    "1 | The water looks slightly cloudy",
    "2 | It smells faintly of rotten eggs",
    "3 | When a small amount is evaporated in a glass dish, a white crust remains",
    "4 | When air is bubbled through the residue from evaporation and tested with lime "
    "water, the lime water turns milky",
    "5 | A small piece of iron left in the water for two days turns reddish-brown",
    "6 | A dissolved-gas reading shows two gases present in unequal proportions"),
 ]),

 # ─── VIII ch 9 · Density answer key ───
 dict(grade="viii", ch=9, idx=3, sha="1ca98e60fa", new=[
  T("Answer Key — Density Calculations and Float/Sink Outcomes",
    "Object | Density calculation | Relative density and outcome",
    "A | density = 48 ÷ 40 = 1.2 g/cm³ | Relative density compared to bottom-layer "
    "water (1.026 g/cm³) is greater than 1 — sinks",
    "B | density = 27 ÷ 36 = 0.75 g/cm³ | Relative density less than 1 — floats",
    "C | density = 55 ÷ 50 = 1.1 g/cm³ | Relative density greater than 1 — sinks"),
  P("Row 8 and facilitation notes",
    "For row 8 (Object B and falling temperature): as water temperature drops, its "
    "density increases; if the water becomes denser than 0.75 g/cm³ by a greater "
    "margin the float outcome is reinforced. Accept any two-sentence answer that names "
    "one concept from each strand — e.g. 'Colder water is denser because its particles "
    "are closer together (density strand); colder water also holds more dissolved gas "
    "such as oxygen because gas solubility increases as temperature falls (solution "
    "strand).' Push groups that skip the density entries for organisms with: 'How "
    "would you measure whether this organism is denser than the water around it?'"),
 ]),

 # ─── VIII ch 10 · Street-intersection site brief ───
 dict(grade="viii", ch=10, idx=0, sha="e4eac293a4", new=[
  T("Street-intersection site brief",
    "A municipal engineer has been asked to install optical devices at four locations "
    "in a busy urban street intersection. No optical vocabulary is used in this brief "
    "— students must supply the device choices themselves",
    "Problem | Situation | Installation requirement",
    "1 — Blind corner | Drivers approaching a sharp blind corner cannot see oncoming "
    "traffic or pedestrians stepping off the pavement | Give drivers the widest "
    "possible view of what is around the corner from a single fixed device",
    "2 — Pedestrian-crossing lighting | A pedestrian crossing is poorly lit at night. "
    "A single lamp is available but its light spreads in all directions | Redirect as "
    "much of that light as possible onto the crossing in a controlled beam",
    "3 — Shopfront display window | A jeweller wants passers-by to see an enlarged "
    "view of small items placed near the window | The image must be upright and "
    "noticeably larger than the actual object",
    "4 — Security monitoring post | A security officer seated at a fixed post must "
    "monitor the widest possible arc of the street in front of the building without "
    "turning or moving | One device, fixed to the wall, must cover the whole arc"),
 ]),

 # ─── VIII ch 12 · Interaction-type legend strip ───
 dict(grade="viii", ch=12, idx=3, sha="5916104f89", new=[
  P("Interaction-type legend strip",
    "Print one per pair as a narrow strip (can be cut from the bottom of the profile "
    "card sheet)."),
  T("Colour code for arrows",
    "Colour | Interaction type",
    "1 | Biotic–biotic interaction",
    "2 | Biotic–abiotic interaction",
    "3 | Abiotic–abiotic interaction"),
  T("Relationship types to label",
    "Relationship | Meaning",
    "Predation / herbivory | One organism eats another",
    "Mutualism | Both organisms benefit",
    "Commensalism | One benefits, one unaffected",
    "Parasitism | One benefits, one harmed",
    "Competition | Both organisms compete for the same resource",
    "Decomposer role | Breaks down dead matter, releases nutrients to abiotic "
    "environment"),
  P("Trophic level reminder",
    "A trophic level is a feeding position in a food chain. Producers are Level 1; "
    "primary consumers (eat producers) are Level 2; secondary consumers (eat primary "
    "consumers) are Level 3; and so on."),
 ]),

 # ─── VIII ch 13 · Verdana data cards ───
 dict(grade="viii", ch=13, idx=0, sha="6de1b76cd8", new=[
  T("Verdana data cards",
    "Copy each card onto a paper slip or index card — one set of five per group",
    "Card | Data",
    "1 — Orbital position | Verdana orbits its star at a distance that allows liquid "
    "water on its surface; average surface temperature 14 °C; water covers 68 % of the "
    "surface",
    "2 — Size and gravity | Verdana's mass is slightly smaller than Earth's; gravity "
    "is strong enough to hold nitrogen, oxygen, and carbon dioxide in its atmosphere, "
    "but only just; atmospheric pressure is 85 % of Earth's",
    "3 — Atmosphere | 21 % oxygen, 0.04 % carbon dioxide, trace ozone layer present; "
    "mild greenhouse effect keeps surface temperatures stable; the ozone layer is thin "
    "but functional",
    "4 — Life forms | Photosynthesising plant-equivalents cover 40 % of land; "
    "animal-equivalents reproduce sexually with external fertilisation in water "
    "bodies; one dominant land species reproduces asexually through vegetative "
    "structures in dry seasons",
    "5 — Reported change event | Over the past century, Verdana's magnetic field has "
    "weakened by 30 %; solar wind particle bombardment reaching the upper atmosphere "
    "has increased; scientists have recorded a 12 % reduction in ozone layer thickness "
    "and a measurable rise in surface UV radiation"),
 ]),
]


def _check(edit) -> list[str]:
    """Validate one declared edit against the installed file. Returns problem strings."""
    probs = []
    path = SAVED / edit["grade"] / f"ch_{edit['ch']:02d}_canonical.json"
    doc = json.loads(path.read_text(encoding="utf-8"))
    unit = doc["result"]["lesson_plan"]["periods"][-1]
    if unit.get("synthesis") is not True:
        return [f"{path.name}: final unit is not the synthesis"]
    vas = unit.get("visual_aids") or []
    if edit["idx"] >= len(vas):
        return [f"{path.name}: no visual_aids[{edit['idx']}]"]
    va = vas[edit["idx"]]
    if va.get("type") != "prose":
        return [f"{path.name} VA{edit['idx']}: already type {va.get('type')!r} — skipping?"]
    sha = hashlib.sha1((va.get("text") or "").encode()).hexdigest()[:10]
    if sha != edit["sha"]:
        probs.append(f"{path.name} VA{edit['idx']}: sha {sha} != declared {edit['sha']} "
                     "(artefact changed) — refusing")
    for nva in edit["new"]:
        if nva["type"] == "table":
            t = parse_table(nva["table"])
            if not t["header"] or not t["rows"]:
                probs.append(f"{path.name} VA{edit['idx']} → '{nva['title']}': parse_table "
                             f"header={len(t['header'])} rows={len(t['rows'])}")
            widths = {len(r) for r in t["rows"]}
            if widths and widths != {len(t["header"])}:
                probs.append(f"{path.name} VA{edit['idx']} → '{nva['title']}': ragged "
                             f"widths {widths} vs header {len(t['header'])}")
        elif not nva.get("text"):
            probs.append(f"{path.name} VA{edit['idx']} → '{nva['title']}': empty prose")
    return probs


def main() -> int:
    dry = "--apply" not in sys.argv
    problems = []
    for e in EDITS:
        problems += _check(e)
    n_tables = sum(1 for e in EDITS for v in e["new"] if v["type"] == "table")
    print(f"{len(EDITS)} edits over "
          f"{len({(e['grade'], e['ch']) for e in EDITS})} chapters · {n_tables} new tables")
    for p in problems:
        print(f"  ⚠ {p}")
    if problems:
        return 1
    if dry:
        for e in EDITS:
            print(f"  {e['grade']} ch{e['ch']:02d} VA{e['idx']} → "
                  + " + ".join(f"[{v['type']}] {v['title']}" for v in e["new"]))
        print("dry run — re-run with --apply")
        return 0

    BACKUP.mkdir(parents=True, exist_ok=True)
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    by_file: dict[tuple, list] = {}
    for e in EDITS:
        by_file.setdefault((e["grade"], e["ch"]), []).append(e)
    for (grade, ch), edits in sorted(by_file.items()):
        path = SAVED / grade / f"ch_{ch:02d}_canonical.json"
        shutil.copy2(path, BACKUP / f"science_{grade}_ch{ch:02d}_{ts}.json")
        doc = json.loads(path.read_text(encoding="utf-8"))
        unit = doc["result"]["lesson_plan"]["periods"][-1]
        entries = []
        # splice highest index first so earlier declared indexes stay valid
        for e in sorted(edits, key=lambda x: -x["idx"]):
            old = unit["visual_aids"][e["idx"]]
            unit["visual_aids"][e["idx"]:e["idx"] + 1] = e["new"]
            entries.append({"unit": unit.get("period_number"),
                            "field": f"visual_aids[{e['idx']}]", "removed": old,
                            "replaced_with": [f"[{v['type']}] {v['title']}"
                                              for v in e["new"]]})
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "genon/repair_prose_tables.py v1.0",
            "at": datetime.now().isoformat(timespec="seconds"),
            "reason": ("founder direction 2026-08-19: enumerable card/event/scene "
                       "content flattened into dense prose visual aids becomes typed "
                       "tables (records → rows, field labels → columns, content moved "
                       "verbatim); scene-setting stays as caption or companion prose"),
            "edits": entries,
        })
        path.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
        purge("science", grade, ch, reason="prose visual aids tabulated")
        print(f"applied · {grade} ch{ch:02d}: "
              f"{len(edits)} aid(s) converted, aids now "
              f"{[a['title'] for a in unit['visual_aids']]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
