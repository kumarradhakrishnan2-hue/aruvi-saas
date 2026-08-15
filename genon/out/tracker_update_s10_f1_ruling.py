#!/usr/bin/env python3
"""S10 · F1 — append the founder's viii ch 01 ruling and turn the step green.

    python3 genon/out/tracker_update_s10_f1_ruling.py
"""
import json
from pathlib import Path

STATE = Path(__file__).resolve().parents[2] / "data" / "testing" / "campaign_state.json"
NOW = "2026-08-15T17:20:00"

RULING = """<br><br><b>RULING ON THE JUMPY — ACCEPTED AS AUTHORED (founder, 2026-08-15).</b> No \
re-author, no repair, no constitution change. The defect stands on disk and is recorded here \
rather than fixed, on the same principle as the register waiver above: a decision on the record \
beats a silent correction.<br><br>

<b>What is being accepted, stated at full strength so nobody re-derives it as smaller than it \
is.</b> This is NOT a scanner artefact like the 8 waived register hits — those are invisible to a \
teacher. This one is visible in the room: a Class VIII teacher serving <code>viii ch 01</code> at \
<b>X=6</b> gives her class "Narrative Essays and a Limerick of Their Own" as sitting 5, then in \
sitting 6 asks them to draft the same narrative essay from an outline they were never asked to \
make, and introduces the limerick form as though it were new. <b>It is the only accepted defect \
in this stage that a real class can hit.</b> Scope is exactly one serve of one chapter — X=6 on a \
[8, 5] library; X=8 (identity) and X=5 are unaffected, and the other 43 seams are clean.<br><br>

<b>Why accepting is defensible here.</b> The remedy is a re-author (~₹30), and regenerating is a \
lottery (founder, 2026-08-02) — the S11/ARV-D-136 precedent came back clean but nothing \
guarantees a second draw does, and a fresh top would void this chapter's W1 register repair and \
could arrive with new hits of its own. Against that: one serve, of one chapter, in a stage of 46. \
<b>The cost of the ruling is that it must not be forgotten</b>, which is what this entry is for.<br><br>

<b>What this ruling does NOT license.</b> It is scoped to <code>viii ch 01</code>. The underlying \
shape — <b>a TOP canonical whose synthesis unit touches the WRITING spine</b> — is now the second \
sighting (english·IX ch 7 was the first, and was re-authored). Two stages, two chapters, one \
cause. If a third appears at S9 (english·preparatory), the finding is no longer a per-chapter \
defect but a property of how english LP constitutions build the closing unit, and the remedy \
moves upstream to Rule 1's closing-unit exception rather than to another ₹30 re-author. <b>The \
english·preparatory F1 should read its synthesis units for the writing spine FIRST, before \
anything else.</b>"""

s = json.loads(STATE.read_text())
f1 = s["batch"]["english/middle"]["F1"]
f1["comment"] = f1["comment"] + RULING
f1["status"] = "pass"
f1["by"] = "Claude (read) · Kumar (rulings 2026-08-15)"
f1["at"] = NOW
s["updated_at"] = NOW
STATE.write_text(json.dumps(s, ensure_ascii=False, indent=1))
print("F1 -> pass · viii ch 01 accepted-as-authored, scoped, with the S9 trigger recorded")
