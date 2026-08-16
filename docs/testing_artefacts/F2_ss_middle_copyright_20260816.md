# F2 — C14 copyright across the batch · social_sciences · middle

**Deterministic floor: `genon/copyright_scan.py --book-only`, 8-gram shingles, runs ≥12 words.**
Scanned **all 41 chapters × 3 canonicals** against their own textbook PDF — the whole stage, not a
sample. The SAMPLING is of the READING, by evidence: longest runs first.

- teacher-facing words scanned: **790,321**
- words inside a run ≥12: **2,426** — **0.31%** reach
- longest run in the stage: **28 words** · runs ≥20 words: **11** · runs 12–19: **159**
- 14 of 41 chapters produce no run ≥12 at all
- by class: vi 19 · vii 25 · **viii 126** — class VIII carries 74% of all runs

**Sampling plan, recorded before reading (runbook §5):** 100% of runs ≥20 words (11), plus 15
drawn from the 12–19 band, seed `social_sciences|middle|F2|2026-08-16`, `random.Random(seed).sample(sorted(pool), 15)`.
Total **26 runs** read in full.

> The scanner cannot see paraphrase, and does not decide anything. "How much is short" and
> "is this too close" are the calls C14 sends here by design.

---

## MANDATORY — every run ≥20 words

### VIII ch 11 · 28 words
- `ch_11_canonical.json` · field `served u8 band3`
- > appointed by the president of india in consultation with the chief justice of india the governor of the state and the chief justice of the concerned high court

### VIII ch 11 · 25 words
- `ch_11_canonical.json` · field `served u14 band2`
- > citizens have a role in helping the judicial system by bringing to its notice social concerns that affect the rights of people animals and nature

### VIII ch 11 · 25 words
- `ch_11_canonical.json` · field `item11 question_text`
- > citizens have a role in helping the judicial system by bringing to its notice social concerns that affect the rights of people animals and nature

### VIII ch 11 · 25 words
- `ch_11_canonical_p09.json` · field `served u6 band1`
- > president of india in consultation with the chief justice of india the governor of the state and the chief justice of the concerned high court

### VIII ch 15 · 24 words
- `ch_15_canonical.json` · field `served u12 band1`
- > persian with the help of learned scholars in varanasi these translations later reached europe and influenced leading philosophers and thinkers in the 19th century

### VIII ch 15 · 23 words
- `ch_15_canonical.json` · field `served u15 band2`
- > the angrakha a robe like upper garment worn by both men and women is believed to have evolved from persian court fashion and

### VIII ch 15 · 23 words
- `ch_15_canonical_p14.json` · field `served u12 band3`
- > the angrakha a robe like upper garment worn by both men and women is believed to have evolved from persian court fashion and

### VIII ch 4 · 22 words
- `ch_04_canonical_p11.json` · field `item13 question_text`
- > was designed primarily to move raw materials from the interior to ports for export and to distribute british manufactured goods throughout india

### VIII ch 15 · 22 words
- `ch_15_canonical.json` · field `served u15 band2`
- > court with variations for women fine muslin sari inspired dupattas added to the style the sari with its rich regional variations continued

### VII ch 9 · 21 words
- `ch_09_canonical.json` · field `served u9 band1`
- > a republic is a form of government in which the head of state is elected and is not a hereditary monarch

### VII ch 10 · 20 words
- `ch_10_canonical_p15.json` · field `served u12 band4`
- > nandalal bose and his team illustrated its pages with scenes from indian history from mohenjo daro to the freedom movement

---

## SAMPLED — 15 of 159 runs in the 12–19 band

**VI ch 8 · 13 words** · `ch_08_canonical.json` · `served u9 band1`
> these two epics created a dense web of cultural interactions across india and

**VI ch 12 · 12 words** · `ch_12_canonical_p11.json` · `served u2 band2`
> a mechanism for citizens living in an area to come together and

**VIII ch 4 · 12 words** · `ch_04_canonical_p11.json` · `served u7 band2`
> the colonial administration at a fraction of the cost of british personnel

**VIII ch 4 · 13 words** · `ch_04_canonical_p15.json` · `served u4 band4`
> a rare instance of an asian power successfully repelling a european colonial force

**VIII ch 4 · 12 words** · `ch_04_canonical.json` · `item19 question_text`
> the bones of the cotton weavers are bleaching the plains of india

**VIII ch 9 · 12 words** · `ch_09_canonical.json` · `served u9 band2`
> tilak s statement swaraj is my birthright and i shall have it

**VIII ch 10 · 13 words** · `ch_10_canonical.json` · `item13 question_text`
> strategically located near important land or sea routes and often atop a hill

**VIII ch 10 · 14 words** · `ch_10_canonical.json` · `served u3 band1`
> footprints the wheel of dharma or the stupa itself rather than in human form

**VIII ch 11 · 15 words** · `ch_11_canonical.json` · `served u8 band1`
> in some cases two or more states or union territories share a common high court

**VIII ch 11 · 14 words** · `ch_11_canonical.json` · `served u7 band1`
> the centre and a state on one side and another state on the other

**VIII ch 12 · 12 words** · `ch_12_canonical.json` · `served u11 band2`
> caste religion ethnicity disability race physical appearance gender sexuality or economic background

**VIII ch 12 · 16 words** · `ch_12_canonical_p11.json` · `item1 question_text`
> in india all citizens are equal under the constitution despite differences of language religion or culture

**VIII ch 12 · 13 words** · `ch_12_canonical_p08.json` · `served u1 band2`
> legally belongs to a country and is a member of its political community

**VIII ch 14 · 13 words** · `ch_14_canonical_p09.json` · `served u5 band3`
> inscribed on unesco s list of intangible cultural heritage of humanity in 2021

**VIII ch 15 · 17 words** · `ch_15_canonical.json` · `served u16 band1`
> 17th centuries indian art and architecture reached remarkable heights blending tradition with innovation across regions and dynasties
