"""The Ask Aruvi question bank — one official file, one embedded copy (2026-08-30).

Run: python3 tests/test_ask_aruvi_kb.py

★ THE ONE THING THESE TESTS EXIST TO PROTECT.

The question bank is hand-written, and it lives in TWO places on purpose:

    data/cloud/content/ask_aruvi/qa_knowledge_base.json   ← official; the file you edit
    web/app/ask-aruvi/qa_knowledge_base.json              ← embedded; what the app imports

The second copy exists because Ask Aruvi is the HELP screen and must answer when the API is
unreachable or the network is poor — so it is bundled into the web build rather than fetched.
The price of that choice is drift: a founder edits the official file, forgets to sync, and the
app keeps serving last month's answers with nobody the wiser. `test_embedded_copy_is_identical`
is the whole reason that cannot happen quietly — it turns a memory problem into a red test.

`test_index_is_current` covers the second half of the same failure. Keywords are tf-idf derived
and score 3 against a query where the question scores 2 and the answer 1, so they are what make
a teacher's own word reach the right pair. They are corpus-relative: editing ONE pair shifts the
ranking for every other. A hand-edit that skips the re-index leaves the bank looking correct and
searching worse.

Both are fixed the same way: python3 aruvi-scripts/sync_ask_aruvi.py

★ ON test_teacher_words_reach_their_pair.

It mirrors askAruviSearch.js and asserts that a set of realistic teacher phrasings land on the
intended pair. Eight of these failed when the 2026-08-30 batch was first written — "rename"
appeared nowhere in the sections pair, "support" nowhere in its question, "cost" nowhere at all
— and the wording was changed until they landed. If you reword a pair and this test fails, the
finding is real: a teacher's word no longer reaches that answer. **Fix the wording, not the
test** — or, if the question genuinely no longer covers that phrasing, move the expectation to
the pair that now does.
"""
import json
import re
import sys
import unicodedata
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))
sys.path.insert(0, str(REPO_ROOT / "aruvi-scripts"))

import sync_ask_aruvi as sync  # noqa: E402

OFFICIAL = sync.OFFICIAL
EMBEDDED = sync.EMBEDDED

# Teacher phrasing -> the pair it must reach (top 2). See the module docstring.
LANDINGS = [
    ("free trial",                    "d30"),
    ("how much does it cost",         "d31"),
    ("renew",                         "d32"),
    ("add a subject",                 "d33"),
    ("invoice",                       "d34"),
    ("sign in",                       "d35"),
    ("agreement",                     "d36"),
    ("contact support",               "d38"),
    ("download my data",              "d39"),
    ("delete my account",             "d40"),
    ("rename section",                "d41"),
    ("end of year",                   "d42"),
    ("chapter notes",                 "d11"),
    ("who writes the plans",          "a33"),
    ("too few periods",               "c21"),
    ("maximum periods",               "c22"),
    ("edit the plan",                 "e19"),
    ("refund",                        "e22"),
]


def load(path):
    return json.loads(Path(path).read_text())


# ── a compact mirror of askAruviSearch.js (keyword 3 · question 2 · answer 1) ──
def _toks(text):
    out = []
    for w in re.findall(r"[A-Za-z0-9]+", text):
        n = sync.norm(w)
        if len(n) >= 2:
            out.append(n)
    return out


def _hit(bag, tok, weight):
    if tok in bag:
        return weight
    if len(tok) >= 3:
        for t in bag:
            if t.startswith(tok):
                return weight
    return 0


def search(pairs, query):
    scored = []
    for i, p in enumerate(pairs):
        keys = {sync.norm(k) for k in p.get("keywords", [])}
        ques = set(_toks(p["question"]))
        ans = set(_toks(p["answer"]))
        score = matched = 0
        for tok in dict.fromkeys(_toks(query)):
            w = max(_hit(keys, tok, 3), _hit(ques, tok, 2), _hit(ans, tok, 1))
            if w:
                score += w
                matched += 1
        if score:
            scored.append((-matched, -score, i, p))
    scored.sort()
    return [p["id"] for *_, p in scored]


# ── tests ─────────────────────────────────────────────────────────────────────
def test_official_file_exists_and_parses():
    assert OFFICIAL.exists(), (
        "The official question bank is missing: %s\n"
        "It is Bucket A-serve content and belongs inside data/cloud/ (the migration unit)."
        % OFFICIAL)
    kb = load(OFFICIAL)
    assert kb.get("pairs"), "no pairs"
    assert kb.get("categories"), "no categories"
    print("  ok  official file parses · %d pairs · %d categories"
          % (len(kb["pairs"]), len(kb["categories"])))


def test_shape_is_sound():
    problems = sync.validate(load(OFFICIAL))
    assert not problems, "question bank problems:\n  " + "\n  ".join(problems)
    print("  ok  every pair has an id, a category, a question and an answer; ids unique")


def test_index_is_current():
    kb = load(OFFICIAL)
    fresh = sync.compute_keywords(kb["pairs"])
    stale = [p["id"] for p in kb["pairs"] if p.get("keywords") != fresh[p["id"]]]
    assert not stale, (
        "%d pair(s) have a stale search index: %s\n"
        "Someone edited the bank without re-indexing. Run:\n"
        "  python3 aruvi-scripts/sync_ask_aruvi.py"
        % (len(stale), ", ".join(stale[:10])))
    print("  ok  search index current on all %d pairs" % len(kb["pairs"]))


def test_embedded_copy_is_identical():
    assert EMBEDDED.exists(), (
        "The web app's copy is missing: %s\n"
        "Ask Aruvi is bundled on purpose — it must answer when the network does not."
        % EMBEDDED)
    assert EMBEDDED.read_text() == OFFICIAL.read_text(), (
        "The web app is serving a DIFFERENT question bank from the official file.\n"
        "This is the drift these tests exist to catch. Run:\n"
        "  python3 aruvi-scripts/sync_ask_aruvi.py")
    print("  ok  embedded copy is byte-identical to the official file")


def test_app_imports_the_embedded_copy():
    jsx = (REPO_ROOT / "web" / "app" / "ask-aruvi" / "AskAruvi.jsx").read_text()
    assert 'from "./qa_knowledge_base.json"' in jsx, (
        "AskAruvi.jsx no longer imports ./qa_knowledge_base.json.\n"
        "If the bank moved to an HTTP fetch, this test and sync_ask_aruvi.py both need "
        "revisiting — and keep a bundled fallback, or offline help dies.")
    print("  ok  AskAruvi.jsx imports the embedded copy")


def test_teacher_words_reach_their_pair():
    pairs = load(OFFICIAL)["pairs"]
    misses = []
    for query, want in LANDINGS:
        top = search(pairs, query)[:2]
        if want not in top:
            misses.append("%-28s -> %s   (want %s)" % (query, top or ["nothing"], want))
    assert not misses, (
        "%d teacher phrasing(s) no longer reach their answer:\n  " % len(misses)
        + "\n  ".join(misses)
        + "\nFix the WORDING of the pair, not this test — see the module docstring.")
    print("  ok  all %d teacher phrasings land in the top 2" % len(LANDINGS))


def test_no_retired_feature_names():
    """Period Notes were removed 2026-07-23. The term must not come back in the help.

    It is not a typo guard: leaving the phrase in an answer keeps it a live SEARCH TERM, so a
    teacher typing it is shown a pair about a feature that does not exist.
    """
    blob = OFFICIAL.read_text().lower()
    assert "period note" not in blob, (
        "'period note' is back in the question bank. The per-unit section note was removed on "
        "2026-07-23; there is one note per chapter, per academic year.")
    print("  ok  no reference to the retired Period Notes")


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    print("test_ask_aruvi_kb — %d tests" % len(tests))
    for t in tests:
        t()
    print("all green")
