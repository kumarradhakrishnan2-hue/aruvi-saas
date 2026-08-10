# C6 runbook — mathematics · IX · ch 4 "Exploring Algebraic Identities"

Phone-first. Three profiles, ten requests. Every expected value below was computed by running
the installed engine against the installed library, so anything that differs on the phone is a
real finding.

**Library:** `[15, 12, 9]` · floor **9** · class-standard duration **50 min** · engine **e17**.
**Split (testing.md §4):** kumar1 = identity · kumar2 = between-variant + below-floor ·
kumar3 = mixed-duration week.

**Setting X on the phone:** the profile fixes the class and its duration(s); the *period count*
for ch 4 comes from Allocate → **Modify Allocation** → set ch 4 to the target number → Save.
Change that one number between requests; the profile itself stays put.

---

## kumar1 — identity · Section A · duration 50 only

Three requests. Each must return **the canonical itself**, not a new file.

| Ask for | Expect | Units | Questions |
|---|---|---|---|
| **15** periods | identity → `ch_04_canonical.json` | 15 | 14 |
| **12** periods | identity → `ch_04_canonical_p12.json` | 12 | 13 |
| **9** periods | identity → `ch_04_canonical_p09.json` | 9 | 9 |

Check on each: `variant_used` equals the number you asked for · `slot_fill` is **null** ·
`surrendered_periods` **0** · **no new plan file is written** (that last one is the point of
this row — an identity request must be a lookup, not a build).

---

## kumar2 — the four interesting cases · Section B · duration 50

| Ask for | Expect | Units | Questions | Watch for |
|---|---|---|---|---|
| **13** | **fill** from the 15 | 13 | **11** | see the ⚠️ below |
| **11** | **synthesis** from the 12 | 11 | 12 | coverage note appears |
| **16** | **surrender** 1 period | **15** | 14 | schedule prints **15**, not 16 |
| **8** | **fill** from the 9 | 8 | 9 | **0 dropped units** — see N/A note |

**Exact strings to expect:**

- At **11**: *"Every section is covered; the closing sitting draws the chapter together in one
  synthesis."*
- At **16**: *"1 period(s) (50 minutes) exceed this chapter's fullest plan and return to your
  budget."* — and the printed schedule must say **15 periods**, with 16 surviving only in the
  request record.

⚠️ **The 13-period request returns FEWER questions than the 12-period one — 11 against 13.**
This is expected and already documented (C3 §D): X=13 switches to the standard canonical, whose
4.8 handoff row anchors late, so a teacher asking for *one more period* gets *two fewer
questions*. Not a bug in any single step — it's the interaction of next-highest selection with
per-section anchoring. **Record it verbatim at C6; it belongs to C9.**

**The below-floor drop case is N/A on this chapter — record the reason, don't chase it.** The
spec expects X = floor−1 to produce non-empty `uncovered_sections` and `dropped_units`. It
won't here: p09's nine units cover all eight sections by unit 8, so its ninth is a multi-section
closer and dropping it loses nothing. **0 drops at every X from 6 to 17.** That's a property of
this chapter, not a failure — but it means C6's dropped-section row goes unexercised at S4 and
is still owed by a later stage.

---

## kumar3 — mixed-duration week · Section C · durations 50 **and 60**

The profile needs the longer duration alongside the standard (P5.4). Identity **never** fires
here — any duration other than the authored 50 forces a whole-canonical serve with proportional
scaling, which is the ordinary teacher case and the thing this row exists to prove.

| Ask for | Expect | Units | Questions | Week order (`duration_sequence`) |
|---|---|---|---|---|
| **10×50 + 3×60** | fill from the 15 | 13 | 11 | `50 50 60 50 50 50 60 50 50 50 60 50 50` |
| **6×50 + 2×60** | fill from the 9 | 8 | 9 | `50 50 60 50 50 50 60 50` |

Check the dispersion rule on both: **the shortest sitting opens the week, the long sittings sit
interior, and no two long sittings are adjacent.** Both sequences above satisfy it — if the
phone shows a 60 first, or two 60s together, that's a defect.

Optional third, if you want a non-standard duration that is *shorter* than authored:
**9×50 + 3×45** → 12 units, 13 questions, sequence `50 50 45 50 50 50 45 50 50 50 45 50`.

---

## What to record

Per request: the mode, `variant_used`, unit count, question count, the served schedule as
printed, any coverage/surrender note **verbatim**, and the filename returned. Then three
cross-cutting checks:

1. **Tenancy** — kumar1/2/3 never see each other's plans (this is the evidence X1 leans on,
   which is why the three sections differ).
2. **Identity writes nothing** — confirm no new file appears for kumar1's three.
3. **The non-monotonicity** at 12 → 13, quoted with both question counts.

**Exit:** every row as expected; responses + filenames recorded; the durations actually run are
recorded. Two rows will close as N/A with a reason rather than a tick — the dropped-section case
and, with it, the `uncovered_sections` note.
