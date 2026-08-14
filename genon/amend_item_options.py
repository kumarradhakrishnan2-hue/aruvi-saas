#!/usr/bin/env python3
"""amend_item_options.py — supply a sub-question's MISSING option set (v1.0, 2026-08-14).

★ THIS TOOL AUTHORS TEXT. Every other genon repair tool is defined by not doing that:
repair_register.py, repair_anchors.py, repair_option_reveals.py and repair_compound_mcq.py
apply stated (old -> new) pairs a human read off the artefact, and refuse anything that
would require a new sentence. The founder ruling behind that line ("regenerating is a
lottery — repair unless the fix is a real teaching change", 2026-08-02) cuts the other way
here: an option set that does not exist cannot be recovered from the file, so writing it is
a real teaching change and must be visible as one. Hence a separate tool, a separate
`kind` in repairs[], and a declaration that carries the SOURCE TEXT the options were
written from so the founder can check every word against it without opening the textbook.

WHAT IT FIXES. english·ix ch 9 `Q-LIS-A-1` asks two sub-questions in its stem and carries
options for only the first:

    "Listen to the World Inclusion Day assembly announcement. Choose the correct answer for
     each question.
     1. The assembly is scheduled for:
     2. Which group will present a staging on inclusion?"

Sub-question 2 is unanswerable as shipped. This is the model's defect, not STEP 6's — the
options were never authored. (STEP 6's compound-item bug is ARV-D-156, a different thing,
repaired by repair_compound_mcq.py.)

WHAT IT DOES NOT DO. It does not invent facts. The distractors below are the OTHER agents
the same transcript names, so each one is a real confusion a listener could make rather
than a manufactured wrong answer, and the correct option is the transcript's own words.
The transcript is quoted in full in `source` and the derivation of every option is stated.

ARRANGEMENT. The item becomes compound, so its labels become GROUPED (`1A`–`1D`, `2A`–`2D`)
— the corpus's one existing convention, from ch 5's listening item. STEP 6 refuses grouped
labels by design, so it will never arrange this item and `unarranged()` will never fail it;
Rule 7's sort is therefore applied HERE, within each sub-question's own set, and asserted.

    python3 genon/amend_item_options.py --list
    python3 genon/amend_item_options.py --apply
"""
from __future__ import annotations

import json
import shutil
import sys
from datetime import datetime
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO))
sys.path.insert(0, str(REPO / "genon"))

TRANSCRIPT = (
    "Good morning everyone. We are excited to announce a special assembly on the occasion "
    "of World Inclusion Day. This assembly will take place on Thursday, 10 October, at "
    "9.00 a.m. in the school auditorium. We have a series of engaging programmes planned "
    "for the day to celebrate and promote inclusion. The assembly will commence with a "
    "welcome speech by our Principal, followed by a staging on inclusion by the Interact "
    "Club. There will also be a special performance by the school's dance team that "
    "highlights themes of diversity and acceptance. After the performances, we will have a "
    "panel discussion featuring guest speakers who are advocates for inclusion in various "
    "fields. We will conclude with a song presented by students to nurture inclusive "
    "practices and collaboration among all members of our school community. Thank you."
)

AMENDMENTS = [
 {"file": "data/content/saved_plans/english/ix/ch_09_canonical_p07.json",
  "item_id": "Q-LST-A-1",
  "why": ("The 7-period COMPACT of ch 9 has the SAME defect as its standard, authored "
          "independently in a different wave: two sub-questions in the stem, one option set. "
          "Sub-question 2 ('Which group will stage a presentation on inclusion?') is "
          "unanswerable. That it recurred across two independent generations says the "
          "listening section's shape invites it, not that one run slipped."),
  # sub-question 1 here is the VENUE question — different from the standard's, which asks
  # the date/time — so only its label prefix changes; its four options are untouched.
  "regroup": {"A": "1A", "B": "1B", "C": "1C", "D": "1D"},
  "add": [
      {"label": "2A", "text": "Guest speakers at the panel discussion", "is_correct": False},
      {"label": "2B", "text": "Interact Club", "is_correct": True},
      {"label": "2C", "text": "Principal", "is_correct": False},
      {"label": "2D", "text": "School's dance team", "is_correct": False},
  ],
  "add_reveals": {
      "2A": ("Student has reached past the staging to a later item on the programme — the "
             "guest speakers hold the panel discussion, which comes after the performances."),
      "2C": ("Student has taken the assembly's opening — the Principal gives the welcome "
             "speech that the staging FOLLOWS, not the staging itself."),
      "2D": ("The closest distractor, and the one worth discussing: the dance team does "
             "perform, on diversity and acceptance, but the announcement assigns the "
             "'staging on inclusion' to the Interact Club."),
  },
  "source": TRANSCRIPT,
  "evidence": (
    "IDENTICAL SET TO THE STANDARD'S, and deliberately so: both plans ask the same\n"
    "  sub-question of the same transcript, so authoring a second wording would make two\n"
    "  versions of one chapter disagree about a fact. Correct — verbatim: '…followed by a\n"
    "  staging on inclusion by the Interact Club.'\n"
    "\n"
    "DISTRACTORS — the other agents the SAME transcript names, in programme order:\n"
    "    Principal              'commence with a welcome speech by our Principal'\n"
    "    School's dance team    'a special performance by the school's dance team'\n"
    "    Guest speakers         'a panel discussion featuring guest speakers'\n"
    "\n"
    "ARRANGEMENT (Rule 7, within sub-question 2's own set): first differing word —\n"
    "  guest / interact / principal / school's — sorts g < i < p < s, so 2A/2B/2C/2D as\n"
    "  declared and the answer lands at 2B because the sort put it there.\n"
    "\n"
    "SUB-QUESTION 1 IS THIS COMPACT'S OWN and is untouched: it asks WHERE the assembly is\n"
    "  held (auditorium / canteen / library / sports ground), where the standard asks WHEN.\n"
    "  Its four options keep their text, order and correctness — only the label prefix\n"
    "  changes — and they are already in Rule 7 order (auditorium < canteen < library <\n"
    "  sports ground), which the tool asserts.\n"
    "\n"
    "NOTATION: labels are written 1A…2D, matching the wave-1 tops. The wave-2 compacts of\n"
    "  ch 5 and ch 11 use Q1-A…Q2-D for the same idea. Both render identically — the display\n"
    "  layer matches the shape, not the spelling — but the divergence is itself the finding:\n"
    "  the assessment constitution declares NO notation for a compound item, so each run\n"
    "  invents one. That belongs in the constitution, not in a repair tool."),
 },
 {"file": "data/content/saved_plans/english/ix/ch_09_canonical.json",
  "item_id": "Q-LIS-A-1",
  "why": ("The stem asks two sub-questions and the item carries options for only the first, "
          "so sub-question 2 ('Which group will present a staging on inclusion?') is "
          "unanswerable. The set is authored here from the listening transcript."),
  # sub-question 1's four options, UNCHANGED, matched by text and merely re-prefixed.
  "regroup": {"A": "1A", "B": "1B", "C": "1C", "D": "1D"},
  # sub-question 2's new set, already in Rule 7 arrangement order (see `arrangement`).
  "add": [
      {"label": "2A", "text": "Guest speakers at the panel discussion", "is_correct": False},
      {"label": "2B", "text": "Interact Club", "is_correct": True},
      {"label": "2C", "text": "Principal", "is_correct": False},
      {"label": "2D", "text": "School's dance team", "is_correct": False},
  ],
  "add_reveals": {
      "2A": ("Student has reached past the staging to a later item on the programme — the "
             "guest speakers hold the panel discussion, which comes after the performances."),
      "2C": ("Student has taken the assembly's opening — the Principal gives the welcome "
             "speech that the staging FOLLOWS, not the staging itself."),
      "2D": ("The closest distractor, and the one worth discussing: the dance team does "
             "perform, on diversity and acceptance, but the announcement assigns the "
             "'staging on inclusion' to the Interact Club."),
  },
  "source": TRANSCRIPT,
  "evidence": (
    "CORRECT — the transcript, verbatim: '…followed by a staging on inclusion by the\n"
    "  Interact Club.' The stem's wording ('a staging on inclusion') is the announcement's\n"
    "  own, so the answer is retrieval, which is what the LO asks ('retrieves precise\n"
    "  details'). It also matches the textbook's own fill-in on the same transcript\n"
    "  (p.152 Q2, 'A presentation on inclusion will be made by the ______').\n"
    "\n"
    "DISTRACTORS — each is another agent the SAME transcript names, in programme order,\n"
    "  so every wrong answer is a real mishearing rather than a manufactured one:\n"
    "    Principal              'commence with a welcome speech by our Principal'\n"
    "    School's dance team    'a special performance by the school's dance team'\n"
    "    Guest speakers         'a panel discussion featuring guest speakers'\n"
    "  Nothing outside the transcript is introduced, and no option names an agent the\n"
    "  announcement does not.\n"
    "\n"
    "ARRANGEMENT (Rule 7, applied within sub-question 2's own set because STEP 6 refuses\n"
    "  grouped labels): first differing word — guest / interact / principal / school's —\n"
    "  sorts g < i < p < s, giving 2A/2B/2C/2D as declared. The correct option lands at 2B\n"
    "  because the sort put it there; position is not chosen.\n"
    "\n"
    "SUB-QUESTION 1 is untouched. Its four options keep their text, their order and their\n"
    "  correctness; only the label prefix changes (A->1A …), and its three diagnostics are\n"
    "  re-keyed by the same map. Its own arrangement is already Rule 7 order\n"
    "  (Friday < Thursday 10.00 < Thursday 9.00 < Wednesday) and is asserted unchanged."),
 },
]


def items_of(doc):
    from aruvi_core.genon.carriers import raw_item_list        # noqa: E402
    return raw_item_list(doc.get("result", doc))


def reveal_block(item):
    for block in (item.get("teacher_guide"),
                  (item.get("guide") or {}).get(item.get("question_type"))):
        if isinstance(block, dict) and isinstance(block.get("what_each_option_reveals"), dict):
            return block
    return None


def apply_one(doc, spec):
    from normalize_options import skip_reason, sort_options    # noqa: E402

    hit = [i for i in items_of(doc) if isinstance(i, dict) and i.get("id") == spec["item_id"]]
    if len(hit) != 1:
        raise SystemExit(f"ABORT: {spec['item_id']} matched {len(hit)} items, expected 1")
    it = hit[0]
    opts = it.get("options") or []

    # ── the file must be the one the declaration describes ──────────────────────
    if sorted(o["label"] for o in opts) != sorted(spec["regroup"]):
        raise SystemExit(f"ABORT: {spec['item_id']} labels {sorted(o['label'] for o in opts)} "
                         f"!= declared {sorted(spec['regroup'])} — already amended, or a "
                         f"different file")
    if [o["label"] for o in spec["add"]] != sorted(o["label"] for o in spec["add"]):
        raise SystemExit("ABORT: declared new options are not in label order")

    # ── sub-question 1: relabel only; text, order and correctness are asserted ──
    before = [(o["label"], o["text"], bool(o.get("is_correct"))) for o in opts]
    for o in opts:
        o["label"] = spec["regroup"][o["label"]]
    after = [(o["label"], o["text"], bool(o.get("is_correct"))) for o in opts]
    if [(spec["regroup"][l], t, c) for l, t, c in before] != after:
        raise SystemExit("ABORT: sub-question 1 changed by more than its label prefix")
    if [o["text"] for o in opts] != [o["text"] for o in sort_options(list(opts))]:
        raise SystemExit("ABORT: sub-question 1 is not in Rule 7 arrangement order — the "
                         "amendment refuses to freeze an unarranged set behind a grouped label")

    # ── sub-question 2: the authored set, asserted to be in arrangement order ───
    new = [dict(o) for o in spec["add"]]
    if [o["text"] for o in new] != [o["text"] for o in sort_options(list(new))]:
        raise SystemExit("ABORT: declared new options are not in Rule 7 arrangement order")
    if sum(1 for o in new if o["is_correct"]) != 1:
        raise SystemExit("ABORT: the new set must declare exactly one correct option")
    it["options"] = opts + new

    # ── diagnostics: sub-question 1's re-keyed, sub-question 2's added ──────────
    block = reveal_block(it)
    if block is None:
        raise SystemExit(f"ABORT: {spec['item_id']} has no what_each_option_reveals container")
    rev = block["what_each_option_reveals"]
    stale = [k for k in rev if k not in spec["regroup"]]
    if stale:
        raise SystemExit(f"ABORT: diagnostics keyed to unknown labels {stale}")
    merged = {spec["regroup"][k]: v for k, v in rev.items()}
    merged.update(spec["add_reveals"])
    correct = {o["label"] for o in it["options"] if o.get("is_correct")}
    labels = [o["label"] for o in it["options"]]
    block["what_each_option_reveals"] = {l: merged[l] for l in labels if l in merged}
    if set(block["what_each_option_reveals"]) != set(labels) - correct:
        raise SystemExit(f"ABORT: diagnostic key set {sorted(block['what_each_option_reveals'])} "
                         f"!= the non-correct labels {sorted(set(labels) - correct)}")

    # ── and STEP 6 must now refuse the item, or the next run undoes all of this ─
    if skip_reason(it) is None:
        raise SystemExit("ABORT: normalize_options would still arrange this item — the "
                         "grouped-label guard is not in force; do not write this file")

    return {"item_id": spec["item_id"], "regrouped": spec["regroup"],
            "options_added": [o["label"] for o in new],
            "correct_added": [o["label"] for o in new if o["is_correct"]],
            "diagnostics_added": sorted(spec["add_reveals"])}


def main() -> int:
    listing = "--list" in sys.argv
    if not listing and "--apply" not in sys.argv:
        print("usage: amend_item_options.py --list | --apply")
        return 2
    for spec in AMENDMENTS:
        path = REPO / spec["file"]
        print(f"\n=== {spec['file']}  ·  {spec['item_id']}   ★ AUTHORED CONTENT")
        print(f"    why: {spec['why']}")
        print(f"    new options:")
        for o in spec["add"]:
            print(f"      {o['label']}  {'✓' if o['is_correct'] else ' '}  {o['text']}")
        print(f"    source (transcript, verbatim):\n      {spec['source']}")
        for line in spec["evidence"].splitlines():
            print(f"      {line}")
        if listing:
            continue
        if not path.is_file():
            print("    SKIPPED — not on disk")
            continue
        doc = json.loads(path.read_text(encoding="utf-8"))
        if any(r.get("kind") == "authored_option_set"
               for r in (doc.get("genon_canonical") or {}).get("repairs", [])):
            print("    SKIPPED — already amended")
            continue
        shutil.copy2(path, path.with_suffix(".json.bak_pre_amend"))
        done = apply_one(doc, spec)
        doc.setdefault("genon_canonical", {}).setdefault("repairs", []).append({
            "tool": "amend_item_options.py", "kind": "authored_option_set",
            "at": datetime.now().isoformat(timespec="seconds"),
            "why": "A sub-question shipped with no option set. Options AUTHORED from the "
                   "listening transcript (quoted in the tool's declaration); labels regrouped "
                   "1A–1D / 2A–2D. This is a teaching change, not a repair — it needs the "
                   "founder's reading, not just a passing certification.",
            "items": [done],
        })
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False), encoding="utf-8")
        print(f"    APPLIED — {json.dumps(done, ensure_ascii=False)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
