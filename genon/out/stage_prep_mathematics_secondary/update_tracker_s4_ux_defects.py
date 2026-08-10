#!/usr/bin/env python3
"""ARV-D-087 / ARV-D-088 — the teacher is told nothing when a prepare fails (2026-08-10)."""
import datetime, json, pathlib, shutil
ROOT = pathlib.Path(__file__).resolve().parents[3]
STATE = ROOT / "data/testing/campaign_state.json"
NOW = datetime.datetime.now().replace(microsecond=0).isoformat()

D087 = {
 "id": "ARV-D-087", "combo": "mathematics/secondary", "step": "C6",
 "severity": "S2", "owner": "founder", "status": "open",
 "opened": NOW, "closed": None, "at": NOW,
 "title": "a failed prepare tells the teacher NOTHING on the ordinary path — the proposed card "
          "flashes and vanishes, and the message is set on a screen she is no longer looking at",
 "evidence": """FOUND 2026-08-10, on the phone, while setting up the C13 mobile demo. The founder
broke ch 4's canonical, asked for 14 periods, and reported: 'something seemed to flash for a
micro sec but nothing readable .. it goes back to my lessons'. That is exactly what the code does.

THE CHAIN, traced end to end:
 1. onPreparing(descriptor) -> page.jsx:279-284 setEditFlow('lessonplans') + setTab('myplans'),
    which UNMOUNTS PrepareLesson and lands her in My Lessons with the proposed card drawn.
 2. the POST fails.
 3. onPrepareError() -> page.jsx:288 is exactly `() => setPreparingCard(null)`. The card is
    pulled. THAT IS THE FLASH.
 4. setError('Couldn't build the lesson plan right now. Try again in a moment.') sets state on
    PrepareLesson, WHICH IS UNMOUNTED. The string is never rendered.
 5. MyLessonPlans has no error surface at all — no error rendering anywhere in the component.
Net: tap -> land in My Lessons -> a card appears and disappears -> nothing. No lesson, no
explanation. She would reasonably conclude she mis-tapped.

THE CODE ANTICIPATED THIS AND STOPPED HALF WAY. The comment on the catch reads: 'She may already
be in My Lessons watching the proposed card — the failure has to reach HER, not this screen, so
it goes back up the same way it went down.' The intent is right; onPrepareError only pulls the
card and never delivers the message.

PATH-DEPENDENT, and the common path is the broken one: on the SECTION-ATTACH path onPreparing
returns false (page.jsx:278, `if (!desc || prepareReturn) return false`), so she stays on the
Prepare screen and does see the generic line. It is the ordinary My Classes / My Lessons route
that is silent.

WHY NO C-STEP CAUGHT IT: C13 tests the API's response bodies and they are correct and readable
(6/6). Nothing in the campaign reads the SCREEN on a failure path. This is the C6/C13 seam —
C6 tests the happy path a teacher takes, C13 tests the API's unhappy path, and neither tests the
teacher's unhappy path.

REMEDY (not applied — founder to rule on the wording): onPrepareError already RECEIVES the
descriptor and throws it away. Keep a failed marker in the shell and render it in My Lessons as a
line she can read — ideally on the card that was about to become her lesson, since that is where
her attention already is.""",
}

D088 = {
 "id": "ARV-D-088", "combo": "mathematics/secondary", "step": "C13",
 "severity": "S3", "owner": "founder", "status": "open",
 "opened": NOW, "closed": None, "at": NOW,
 "title": "postJSON discards the server's `detail`, so every failure collapses to one generic "
          "line — and that line tells her to retry things that can never succeed",
 "evidence": """web/app/lib/format.js:96 — `if (!r.ok) throw new Error(`${r.status}`)`. The
response BODY is never read, so the server's teacher-worded detail is thrown away at the
transport layer, before any component sees it. Only Allocate.jsx reads body.detail, and it uses
its own fetch rather than postJSON.

CONSEQUENCE: the four messages C13 certified never reach her. 'No underlying chapter yet.',
'Period count implausibly large.', and the 500 that names the broken item all render as the same
sentence: 'Couldn't build the lesson plan right now. Try again in a moment.'

AND THAT SENTENCE IS WRONG IN A SPECIFIC WAY: 'Try again in a moment' is true for a transient
failure and FALSE for both cases she can actually reach — an unauthored chapter and an
impossible period count are permanent until someone acts. We send her to retry a thing that
cannot work.

SCOPE NOTE: the 404 is unreachable from the UI anyway. genonAvailable is computed from
/genon/{s}/{g}/chapters (chapters WITH a library) and the picker itself is built from the
SYLLABUS (/subjects/{s}/{g}/chapters, i.e. the mappings folder), so the app never asks the genon
path for a chapter we have not authored. The reachable cases are the 400 (period count) and the
500 (corrupt canonical).

REMEDY (not applied): have postJSON read `detail` off the body and attach it to the thrown Error;
show it when present, keep the generic line as the fallback. Safe by construction — the API
strings are already teacher-worded, which is precisely what C13 check 1 polices ('canonical' is
our word, not hers). Pairs with ARV-D-087: 087 is why she sees nothing, 088 is what she would
see once there is somewhere to say it.""",
}

state = json.loads(STATE.read_text(encoding="utf-8"))
shutil.copy(STATE, STATE.with_suffix(".json.bak_pre_ux_defects"))
have = {d["id"] for d in state["defects"]}
for d in (D087, D088):
    if d["id"] not in have:
        state["defects"].append(d)

note = f"""

[REOPENED FOR RECORD {NOW[:10]} — not the step's verdict, which stands. Mobile testing of the
 C13 cases found the failure path the campaign had never read: the API's messages are correct
 (C13 6/6) but on the ordinary prepare route the teacher is shown NOTHING — ARV-D-087, with
 ARV-D-088 behind it. Recorded here because C6 is the step that owns 'the path a teacher
 actually takes', and this is that path on a bad day. Neither defect affects a served plan;
 both are client-side.]"""
state["combos"]["mathematics/secondary"]["C6"]["comment"] += note
state["combos"]["mathematics/secondary"]["C13"]["comment"] += (
    "\n\n[ADDENDUM " + NOW[:10] + " — the four API responses certified here are correct and were "
    "verified readable. What the TEACHER sees is a separate question and is not: see ARV-D-088 "
    "(the detail is discarded by postJSON) and ARV-D-087 (on the ordinary path nothing is shown "
    "at all). C13's verdict is unchanged; the gap is that no C-step reads the screen on a "
    "failure path.]")
state["updated_at"] = NOW
STATE.write_text(json.dumps(state, indent=1, ensure_ascii=False), encoding="utf-8")
from collections import Counter
ds=[d for d in state["defects"] if d.get("combo")=="mathematics/secondary"]
print("filed ARV-D-087 (S2, silent failure) + ARV-D-088 (S3, detail discarded)")
print("S4 defects:", dict(Counter(d["status"] for d in ds)))
