#!/usr/bin/env python3
"""S4 · C8 and C9 (2026-08-09). Both PASS."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

C8 = """PASS — 2026-08-09, founder read. The X=11 Case-1 borrow — p12's ten-unit prefix handing
over to the 15's synthesis unit — SITS FINE. Rated CLEAN; no defect.

WHAT THIS CHAPTER COULD AND COULD NOT EXERCISE, recorded so the thinness is a known property
rather than an unnoticed gap. The choice set produced exactly ONE cross-canonical borrow in an
eleven-wide band, and it is the one read above. Everything else is either an identity, a
surrender, or a SELF fill — the plan's own next unit winning the slot under the v2.1 SELF-FIRST
tie-break (e14), which is that fix working as intended rather than the choice set idling.
Consequence: only fill/single and the Case-1 synthesis borrow are exercised here.
fill/FORWARD and fill/BACKWARD never occur on this library, so C8's per-class coverage is
incomplete at S4 and is owed by a later stage — science·IX is the obvious candidate, whose sweep
carries 'fill/single -2s', '-1s' and a 'rescue/complete (from 10)' mode this chapter never
reaches. The below-floor serve WAS read (X=5) and is recorded under C7.

Structural reason only one synthesis borrow exists, worth keeping: Case 1 can fire at exactly
one X per canonical — its coverage-completion point plus one. The 9 completes at U8 so its
synthesis X is 9, which is cancelled by being the identity; the 12 completes at U10 so X=11
fires and MUST borrow from the 15, because compacts are forbidden the synthesis token; the 15
completes at U13 so X=14 fires and borrows its own. Three candidates, one cancelled, one self."""

C9 = """PASS — 2026-08-09. Anchor table built for all EIGHT served plans (X = 5, 7, 8, 10, 11,
13, 16, and the 4x60+10x50 mixed). All four rules hold.

1. PREFIX REMAP — ZERO mis-anchored items across the eight plans. Every period_ref lands on a
   sitting that exists in THAT plan and whose section_anchor actually contains the item's
   section_ref (synthesis units exempted, as they anchor the reserved token). Checked as a list
   — maths emits period_ref as [n], not n.

2. BORROWED UNIT BRINGS ITS OWN ITEMS — holds where the home variant has an item to bring, and
   the exceptions are correct rather than misses. X=7 and X=8 (filling from the 9): the fill
   sitting carries the 4.8 item, because the 9's handoff routes 4.8 through a single unit. X=10
   and X=13 (filling from the 12 and the 15): the fill sitting carries NO item, because those
   handoffs route 4.8 through TWO teaching units ([10,11] and [13,14]) and the item anchors to
   the LAST — which is not served. Those items are then correctly absent and counted under
   rule 3(b): assessment_items_unserved = 2 and 3 respectively. This is the same mechanism the
   founder observed at C7 (X=10 not showing the second sitting's two items); C9 confirms the
   anchoring is right and the loss is reported in the genon block — what C7 ruled on was the
   absence of a teacher-facing note, not a mis-anchor.

3. UNSERVED ANCHORS (the e13 rewrite, ARV-D-037):
   (a) ZERO items carry an empty or missing period_ref, in any of the eight plans.
   (b) items whose anchor unit was not served are ABSENT and counted —
       assessment_items_unserved reads 2 (X=10), 2 (X=11), 3 (X=13), 2 (X=7), 2 (mixed), 0
       elsewhere.
   (c) BELOW-FLOOR X=5: the three dropped units' items ARE present, flagged unscheduled:true,
       and anchored to 7, 7 and 8 — the dropped units' sitting numbers in THIS plan (dropped
       units are numbered 6,7,8, a contiguous continuation of the served 1-5), never the
       lender's own numbering. The 4.7 pair both anchor at 7 because the 9's handoff routes
       4.7 through [6,7] and the item takes the last.
   (d) EXPORTS OMIT EXACTLY THE UNSCHEDULED ITEMS — exercised through the real export seam
       (carriers.raw_item_list + the api/main.py filter, ARV-D-063's carrier path): 9 items in
       the plan, export keeps 6 (4.1-4.6), omits exactly the 3 unscheduled (4.7, 4.7, 4.8),
       matching the three dropped units the export also omits.

4. NO CROSS-VARIANT REFERENCES of any other kind — every period_ref in every plan resolves
   inside that plan's own sitting numbering, served or dropped.

EXIT MET: zero mis-anchored items; every unserved-anchor item accounted for by count rather
than by an empty ref. No defect filed."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_c8c9"))
c = state["combos"]["mathematics/secondary"]
c["C8"] = {"status": "pass", "by": "Kumar", "at": NOW, "comment": C8}
c["C9"] = {"status": "pass", "by": "Claude", "at": NOW, "comment": C9}
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
print("C8 = pass · C9 = pass")
print("S4 steps:", {k: v.get("status") for k, v in c.items()
                    if isinstance(v, dict) and k.startswith("C")})
