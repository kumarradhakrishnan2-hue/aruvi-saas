#!/usr/bin/env python3
"""One-shot tracker write: S2 (social_sciences · middle) C13 + ARV-D-052, and cleanup of the
stray prepared-register mark the mis-designed first C13.3 attempt left on kumar2.

    python3 genon/out/tracker_update_s2_c13.py
"""
import json
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
STATE = REPO / "data" / "testing" / "campaign_state.json"
KUMAR2 = REPO / "data" / "prepared_plans" / "kumar2" / "kumar2" / "prepared.json"
STRAY = "social_sciences/viii/ch_03_canonical.json"
NOW = "2026-08-04T23:05:00"


C13 = """[e14 2026-08-04 - PASS on all four] Kumar broke it in Terminal, Claude read the \
responses. Every path returns a code a client can branch on and a message a teacher can read; \
NOTHING resembling a traceback appears in any body.

1. NO CANONICAL - chapter 7 of social_sciences/viii (no library on disk):
   404  {"detail":"No underlying chapter yet."}
   The 2026-08-04 re-wording is live and correct: "canonical" is our word, not hers, and the \
string names the CHAPTER in her language.

2. IMPLAUSIBLE MATRIX - both arms:
   45x61 (total 61 > 60)  ->  400  {"detail":"Period count implausibly large."}
   rows: []               ->  400  {"detail":"At least one duration row is required."}
   Noted for the record: rows with duration<=0 or count<=0 are FILTERED OUT before the empty \
check, so {"duration":45,"count":0} also yields the empty-rows 400 rather than a 200. Correct, \
but it is a behaviour worth knowing - a client that sends a zeroed row gets the empty message.

3. UNRESOLVABLE ITEM ANCHOR - ch_03_canonical.json copied to scratch chapter 97 with assessment \
item #4's period_ref pointed at unit [99], then requested at 45x12:
   500  {"detail":"Canonical cannot be compiled: canonical plan is not v1.1-declared \
(1 problem): assessment item #4 ECR / C-2.1: no resolvable anchor unit (period_ref/phase_ref) \
- it names [99]"}
   Names the item, its type and its competency, and says what is wrong with it - not a bare \
500. Scratch file removed afterwards; verified absent, and GET /genon/social_sciences/viii/\
chapters lists [3] only, so nothing leaked into the chapter list.

   TEST-DESIGN NOTE, recorded because it cost a run and found a defect: the first attempt asked \
for 45x16, which is the TOP canonical's own count - so the IDENTITY rule fired and returned 200 \
before the compiler was ever reached. The dangling anchor was never exercised. Any future C13.3 \
must use a count that is NOT any canonical's own (here 12). The failed attempt is not wasted: \
it surfaced ARV-D-052 below.

4. QUARANTINED VARIANT ABSENT FROM SERVING - the C10.5 transcript read as a failure path: with \
p13 withheld the library reads [16, 10], serving falls to the next-highest surviving variant \
(X=12 variant_used 13 -> 16; X=13 identity -> fill), nothing 500s, and the string "p13" appears \
in NO response payload.

EXIT: the four codes and readable details recorded; no traceback in any body."""


def main():
    st = json.loads(STATE.read_text())
    mid = st["combos"]["social_sciences/middle"]
    mid["C13"] = {"status": "pass", "by": "Kumar + Claude", "at": NOW, "comment": C13}

    defect = {
        "id": "ARV-D-052", "combo": "campaign", "step": "C13", "severity": "S3",
        "owner": "Kumar", "status": "open",
        "opened": NOW, "closed": None, "at": NOW,
        "title": "The identity response reports the plan's SELF-DECLARED filename, not the "
                 "file it loaded — and that name is what goes into the prepared register",
        "evidence": "api/main.py:918 `filename = canonical[\"filename\"]`. Exposed at C13.3: "
                    "ch_03_canonical.json was copied to ch_97_canonical.json with only "
                    "chapter_number changed, so its internal `filename` field still read "
                    "ch_03_canonical.json. A 45x16 request for CHAPTER 97 returned "
                    "{\"identity\":true,\"filename\":\"ch_03_canonical.json\","
                    "\"chapter_number\":97} with a 200, and prepared_plans_repo.mark wrote "
                    "the key social_sciences/viii/ch_03_canonical.json onto kumar2 — a plan "
                    "she never asked for. NOT cross-chapter leakage: load_genon_library read "
                    "the right file by path; only the reported name is wrong.",
        "notes": "Latent in normal operation, because the generator writes the path and the "
                 "internal field together and they agree. It bites whenever they diverge — a "
                 "hand-copied file, a rename, a restore from backup, or any future tool that "
                 "writes a canonical without resetting the field. The consequence is silent: "
                 "the teacher's register points at a DIFFERENT file, and her listing shows a "
                 "plan she did not prepare. Fix is one line: return the path the library "
                 "actually loaded from rather than the plan's claim about itself, or assert "
                 "the two agree at load time and fail loudly when they do not. The stray "
                 "kumar2 mark this created was removed as part of this write.",
    }
    st["defects"] = [x for x in st["defects"] if x["id"] != defect["id"]]
    st["defects"].append(defect)
    st["updated_at"] = NOW
    STATE.write_text(json.dumps(st, ensure_ascii=False, indent=2))

    print("wrote", STATE)
    print("  social_sciences/middle C13 -> pass (%d chars)" % len(C13))
    print("  defect ARV-D-052 -> open (S3)")
    print("  steps now:", list(mid))

    # ── cleanup: the stray mark the mis-designed 45x16 attempt wrote onto kumar2 ──
    reg = json.loads(KUMAR2.read_text())
    if STRAY in reg:
        removed = reg.pop(STRAY)
        KUMAR2.write_text(json.dumps(reg, ensure_ascii=False, indent=2))
        print("\n  cleaned kumar2 register: removed %s (%s)" % (STRAY, removed))
        print("  -> identities belong to kumar1 by the C6 design; kumar2 runs the "
              "between-variant and below-floor requests. X1's tenancy evidence stays clean.")
    else:
        print("\n  kumar2 register already clean")
    print("  kumar2 viii keys now:",
          len([k for k in reg if "/viii/" in k]))


if __name__ == "__main__":
    raise SystemExit(main())
