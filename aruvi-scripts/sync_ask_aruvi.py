"""Re-index the Ask Aruvi question bank and copy it into the web app (2026-08-30).

    python3 aruvi-scripts/sync_ask_aruvi.py            # re-index + copy
    python3 aruvi-scripts/sync_ask_aruvi.py --check    # verify only, write nothing (exit 1 if stale)

★ WHAT THIS IS, AND WHAT IT DELIBERATELY IS NOT.

The question bank is **hand-written from now on** (founder, 2026-08-30). Questions and
answers are authored by a person, directly in the official file:

    data/cloud/content/ask_aruvi/qa_knowledge_base.json     ← the one you edit

This script NEVER writes a question, an answer, a category or an id. It does exactly two
mechanical things after you have finished writing:

  1. **Re-indexes** — recomputes the six search keywords on every pair.
  2. **Copies** — writes the result to web/app/ask-aruvi/qa_knowledge_base.json, which the
     app imports at build time.

It replaces `build_kb.py`, which was retired the same day: that script flattened a nested
"V3" master file which no longer exists (and whose path, `data/content/ask_aruvi/`, had been
dead since the 2026-08-23 cloud restructure — the same stale-literal defect found in
purge_derived.py and generate_canonical.py on 2026-08-27).

★ WHY RE-INDEXING CANNOT BE HAND-MAINTAINED, even though the content now is.

askAruviSearch.js scores a query word against three fields — keyword 3 · question 2 ·
answer 1 — so the keywords are what make a teacher's own word reach the right pair. They are
tf-idf derived, six per pair, 744 in all, and **idf is corpus-relative**: adding or rewording
ONE pair shifts the ranking for every other. Hand-maintaining them is not a smaller job than
regenerating them, it is an impossible one. Measured on the 2026-08-30 batch: of 27 realistic
teacher queries, 8 failed to reach the right pair until the wording was adjusted and the index
rebuilt ("rename" appeared nowhere in the sections pair; "support" nowhere in its question;
"cost" nowhere at all).

★ WHY A COPY RATHER THAN A FETCH.

Ask Aruvi is the HELP screen. It must answer when the API is unreachable or the network is
poor — which, on a budget Android in an Indian school, is exactly when a teacher needs it. So
the bank is bundled into the web app (`import kb from "./qa_knowledge_base.json"`) rather than
served over HTTP. The cost of that choice is a second copy, and a second copy can drift; that
is what `--check` and tests/test_ask_aruvi_kb.py exist to prevent. Do not "fix" the drift by
deleting the web copy — the offline guarantee is the point.

★ THE OFFICIAL FILE LIVES IN THE MIGRATION UNIT.

`data/cloud/` is what goes to production byte for byte (CLAUDE.md §7, CLOUD_DATA_MODEL §0.5).
The question bank is shared, read-only, founder-authored content served to every teacher —
Bucket A-serve, exactly like `content/legal/`. It had never been classified into either bucket
and so was living only inside the web bundle; this script's existence is what moved it home.

normalize()/norm() below MUST stay byte-for-byte identical to askAruviSearch.js normalize(),
or the keywords baked into the JSON stop lining up with what a teacher types.
"""
import argparse
import json
import math
import re
import sys
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from api import config  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
OFFICIAL = Path(config.DATA_DIR) / "ask_aruvi" / "qa_knowledge_base.json"
EMBEDDED = REPO_ROOT / "web" / "app" / "ask-aruvi" / "qa_knowledge_base.json"

KEYWORDS_PER_PAIR = 6

# ── normalization — mirror of askAruviSearch.js normalize() ───────────────────
STOP = set('''a an the of to in on for and or but with without as at by from into is are was
were be been being do does did done how what why when which who whom whose this that these
those it its their they them there here he she his her our your you we us i me my mine one two
three four five six all any some more most other another use used uses using make makes made
get gets got give gives given also only just very much many few both same own about over under
between during before after out up down off above below because while where whether can cannot
not no yes if then than so such each per within across need needs want wants work works thing
things help helps helped teacher teachers lesson lessons plan plans aruvi whole full'''.split())
ROMAN = set('i ii iii iv v vi vii viii ix x xi xii'.split())
GRADEWORD = re.compile(r'^(ncf|ncert)$')


def strip_accents(x):
    return ''.join(c for c in unicodedata.normalize('NFD', x)
                   if unicodedata.category(c) != 'Mn')


def norm(tok):
    tok = strip_accents(tok.lower())
    tok = re.sub(r'[^a-z0-9]', '', tok)
    if len(tok) > 4 and tok.endswith('ies'):
        tok = tok[:-3] + 'y'
    elif len(tok) > 4 and re.search(r'(s|x|z|ch|sh)es$', tok):
        tok = tok[:-2]
    elif len(tok) > 3 and tok.endswith('s') and not tok.endswith('ss') and not tok.endswith('us'):
        tok = tok[:-1]
    return tok


def words(text):
    for w in re.findall(r"[A-Za-z0-9]+", text):
        n = norm(w)
        if len(n) >= 3 and n not in STOP and n not in ROMAN and not GRADEWORD.match(n):
            yield n, strip_accents(w.lower())


def compute_keywords(pairs):
    """Return {pair_id: [six surface-form keywords]} — tf-idf over the whole bank.

    Pure: takes the pairs, touches nothing. The caller decides whether to write.
    """
    df = defaultdict(int)
    surf = defaultdict(Counter)
    per = []
    for p in pairs:
        qn, an = [], []
        for n, s in words(p['question']):
            qn.append(n); surf[n][s] += 1
        for n, s in words(p['answer']):
            an.append(n); surf[n][s] += 1
        for n in set(qn + an):
            df[n] += 1
        per.append((qn, an))

    out = {}
    n_pairs = len(pairs)
    for p, (qn, an) in zip(pairs, per):
        tf = defaultdict(float)
        for n in qn:
            tf[n] += 3.0
        for n in an:
            tf[n] += 1.0
        ranked = sorted(tf, key=lambda n: tf[n] * math.log((n_pairs + 1) / df[n]), reverse=True)
        keys = ranked[:KEYWORDS_PER_PAIR]
        while len(keys) < KEYWORDS_PER_PAIR and len(keys) < len(ranked):
            keys.append(ranked[len(keys)])
        out[p['id']] = [surf[k].most_common(1)[0][0] for k in keys]
    return out


# ── shape checks — cheap, and they catch a hand-edit typo before it ships ─────
def validate(kb):
    problems = []
    cats = {c['id'] for c in kb.get('categories', [])}
    if not cats:
        problems.append("no categories")
    seen = set()
    for i, p in enumerate(kb.get('pairs', [])):
        where = "pair %d (%s)" % (i, p.get('id', '?'))
        for field in ('id', 'category', 'question', 'answer'):
            if not (p.get(field) or '').strip():
                problems.append("%s: empty %s" % (where, field))
        if p.get('id') in seen:
            problems.append("%s: duplicate id" % where)
        seen.add(p.get('id'))
        if p.get('category') not in cats:
            problems.append("%s: unknown category %r" % (where, p.get('category')))
    return problems


def serialize(kb):
    return json.dumps(kb, ensure_ascii=False, indent=2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true",
                    help="verify the index is current and the copies match; write nothing")
    args = ap.parse_args()

    if not OFFICIAL.exists():
        print("MISSING: %s" % OFFICIAL, file=sys.stderr)
        print("The official question bank is the file you edit. It must exist.", file=sys.stderr)
        return 2

    kb = json.loads(OFFICIAL.read_text())
    pairs = kb.get('pairs', [])

    problems = validate(kb)
    if problems:
        print("The question bank has %d problem(s):" % len(problems), file=sys.stderr)
        for t in problems:
            print("  - %s" % t, file=sys.stderr)
        return 1

    fresh = compute_keywords(pairs)
    stale = [p['id'] for p in pairs if p.get('keywords') != fresh[p['id']]]
    for p in pairs:
        p['keywords'] = fresh[p['id']]
    text = serialize(kb)

    embedded_matches = EMBEDDED.exists() and EMBEDDED.read_text() == text

    if args.check:
        ok = True
        if stale:
            ok = False
            print("STALE INDEX: %d pair(s) need re-indexing: %s"
                  % (len(stale), ", ".join(stale[:8]) + (" …" if len(stale) > 8 else "")))
        if not embedded_matches:
            ok = False
            print("OUT OF SYNC: the web app's copy differs from the official file.")
        if ok:
            print("in sync · %d pairs · index current · web copy identical" % len(pairs))
            return 0
        print("\nRun: python3 aruvi-scripts/sync_ask_aruvi.py")
        return 1

    OFFICIAL.write_text(text)
    EMBEDDED.parent.mkdir(parents=True, exist_ok=True)
    EMBEDDED.write_text(text)

    print("official : %s" % OFFICIAL)
    print("embedded : %s" % EMBEDDED)
    print("pairs    : %d  %s" % (len(pairs), dict(Counter(p['category'] for p in pairs))))
    print("re-indexed: %d pair(s) changed" % len(stale))
    if stale:
        print("            %s" % ", ".join(stale[:12]) + (" …" if len(stale) > 12 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
