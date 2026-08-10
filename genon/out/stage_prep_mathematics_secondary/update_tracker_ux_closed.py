#!/usr/bin/env python3
"""ARV-D-087 / ARV-D-088 closed, and the read-after-write doctrine recorded (2026-08-10)."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

R087 = """CLOSED 2026-08-10, verified on the phone by the founder. A failed prepare no longer
vanishes: the proposed card STAYS, its bar stops, the dashed 'not yet' border goes solid, and
the last line becomes the reason with a Dismiss she controls. onPrepareError now carries the
message with the descriptor instead of discarding it — which is what the original comment
('the failure has to reach HER, not this screen') asked for and never did.
Card height was wrong on the first pass and is fixed: the failed line is ONE ROW at every
width, because .sc-prep's <=420px column stacking exists to protect the progress BAR and there
is no bar here. The note is clamped to two lines so a long 4xx sentence cannot grow the card
either, with the full text in `title`.
Also fixed in the same pass, found because the founder pressed Prepare on a chapter with no
canonical and got NOTHING: the chapter step had no {error} block at all — the only one sits
inside the 'preview' step, which is why the retired stand-in path used to navigate there just
to be seen. The message now renders beside the button she pressed, with the picker still in
front of her, and clears when she moves the chapter wheel so it cannot accuse the wrong
chapter."""

R088 = """CLOSED 2026-08-10. postJSON now reads the body and attaches `detail` to the thrown
error, so a 4xx reaches her in the API's own words. Scoped to 4xx DELIBERATELY: those strings
are already written for her (C13 check 1 polices exactly that — 'canonical' is our word, not
hers), while a 5xx detail is engine talk ('Canonical cannot be compiled: assessment item #4
NUM / C-3.1 …') and must never be shown. A 5xx therefore keeps the generic sentence.
Verified live: 31 periods on ch 4 now reads 'More than 30 periods is too many for one chapter.'
on the failed card, where it previously read 'try again in a moment' — advice that could never
have worked."""

DOCTRINE = """READ-AFTER-WRITE VERIFICATION — the founder's rule, implemented and proved
(2026-08-10). Recorded here because it is a standing pattern, not a defect fix, and because it
CORRECTS the reasoning that produced ARV-D-087/088.

THE RULE: an error requires a pre-state X, an action A, and an expected post-state Y known
UPFRONT. After A, pull Y' from the server. Error IF AND ONLY IF Y' != Y.
What it rules out, and what I had wrongly been treating as triggers: 'the request threw' is not
a criterion (a 200 can lie; a lost response can hide a write that landed), and 'the server is
unreachable' is NOT an error but a state in which THE CHECK CANNOT RUN — presuming failure
there would invent a fact. Three outcomes, never two: ok (silence) · mismatch (the only case
that speaks) · unverified (silence).

IMPLEMENTED: web/app/lib/verify.js — verifiedWrite({write, read, expect}). The write's own
rejection is swallowed on purpose; the READ is the arbiter. A comparator that throws returns
'unverified' rather than a false alarm.

AREA 1 (the teaching profile) IS LIVE AND TESTED ON THE PHONE. Y = the subjects[] she composed,
Y' = GET /readiness. On mismatch the view is RE-SYNCED to Y' before the message shows —
telling her it failed while leaving her edit on screen would recreate the divergence the check
exists to catch. Founder ran all three cases: A works -> silence; B (profile chmod 444, so the
write fails while the read still succeeds) -> the line fires AND the subject disappears;
C (API stopped) -> silence, correctly.

THE COMPARATOR IS THE WHOLE RISK and is tested as such: tests/test_verify_readiness.mjs, 17
checks, most asserting what must NOT fire (section order, subject order, grade case, duration
order, '7' vs 7, budget edits). A false alarm would teach her to ignore the real one.

KNOWN RESIDUAL, seen deliberately at case C: between an unverified write and her next refresh
the screen shows a state the server may not have. The doctrine forbids calling that an error.
Closing it would need a third state — 'not yet confirmed' — which is a design decision, not a
patch.

OWED, in the founder's numbering: area 2 (LP generation), 3 (archiving), 4 (attaching an LP to
a section card), 5 (mark complete) are the same call with a predicate instead of an equality —
their read endpoints all exist (/plans-prepared, /plan-archive, /section-state). AREA 6
(chapter notes) CANNOT be done: notes live only in localStorage under
chapter_notes_{subject}_{grade}_{chapter_title} and NO endpoint exists, so there is no Y' to
pull. Under the rule that correctly means no error may ever be raised for a note — and also
that her notes are one cache-clear from gone. That is an endpoint decision, not a message."""

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_ux_closed"))
by = {d["id"]: d for d in state["defects"]}
for did, res in (("ARV-D-087", R087), ("ARV-D-088", R088)):
    d = by[did]; d["status"] = "closed"; d["closed"] = NOW; d["at"] = NOW; d["resolution"] = res

state.setdefault("doctrine_notes", []).append(
    {"at": NOW, "title": "read-after-write verification", "note": DOCTRINE})
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
from collections import Counter
ds = [d for d in state["defects"] if d.get("combo") == "mathematics/secondary"]
print("ARV-D-087 + ARV-D-088 closed · doctrine recorded")
print("S4 defects:", dict(Counter(d["status"] for d in ds)))
