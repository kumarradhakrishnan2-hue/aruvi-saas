"""Re-index the Ask Aruvi question bank in place (2026-08-30).

    python3 aruvi-scripts/sync_ask_aruvi.py            # re-index
    python3 aruvi-scripts/sync_ask_aruvi.py --check    # verify only, write nothing (exit 1 if stale)

★ WHAT THIS IS, AND WHAT IT DELIBERATELY IS NOT.

The question bank is **hand-written from now on** (founder, 2026-08-30). Questions and
answers are authored by a person, directly in the official file:

    data/cloud/content/ask_aruvi/qa_knowledge_base.json     ← the one you edit

This script NEVER writes a question, an answer, a category or an id. It does exactly ONE
mechanical thing after you have finished writing: **re-indexes** — recomputes the six search
keywords on every pair, in place.

★ THE COPY STEP IS GONE (2026-08-30). It used to also write the bank into
web/app/ask-aruvi/, which the app imported at build time. That put all 120 answers into a
PUBLIC page chunk, readable before sign-in. The bank is now served by `GET /ask-aruvi`
straight from DATA_DIR and cached on the teacher's device (api/main.py, web/app/ask-aruvi/
bank.js), so there is exactly ONE copy of the file and drift between copies is no longer
possible — which is why tests/test_ask_aruvi_kb.py lost its byte-identity check and gained
a guard that the bank has NOT come back into the bundle.

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

★ SERVED, THEN CACHED — BOTH REQUIREMENTS MET.

Ask Aruvi is the HELP screen: it must answer when the network does not, which on a budget
Android in an Indian school is exactly when a teacher needs it. It is also founder IP that
should not sit on a public url. So the route is signed-in only and the client fetches the
bank ONCE and keeps it in localStorage, re-checking with an ETag on each app load (a 304 and
no body, normally). Do not "simplify" this back into a bundled import — that is what made it
public.

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
BUNDLED = REPO_ROOT / "web" / "app" / "ask-aruvi" / "qa_knowledge_base.json"   # must NOT exist

KEYWORDS_PER_PAIR = 6

# ── normalization — mirror of askAruviSearch.js normalize() ───────────────────
STOP = set('''a an the of to in on for and or but with without as at by from into is are was
were be been being do does did done how what why when which who whom whose this that these
those it its their they them there here he she his her our your you we us i me my mine one two
three four five six all any some more most other another use used uses using make makes made
get gets got give gives given also only just very much many few both same own about over under
between during before after out up down off above below because while where whether can cannot
not no yes if then than so such each per within across need needs want wants work works thing
things help helps helped teacher teachers lesson lessons plan plans aruvi meyy whole full'''.split())
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

    if args.check:
        ok = True
        if stale:
            ok = False
            print("STALE INDEX: %d pair(s) need re-indexing: %s"
                  % (len(stale), ", ".join(stale[:8]) + (" …" if len(stale) > 8 else "")))
        if BUNDLED.exists():
            ok = False
            print("BUNDLED COPY IS BACK: %s\n"
                  "The bank must not ship in the web build — it would be public before "
                  "sign-in. It is served by GET /ask-aruvi." % BUNDLED)
        if ok:
            print("ok · %d pairs · index current · not bundled" % len(pairs))
            return 0
        print("\nRun: python3 aruvi-scripts/sync_ask_aruvi.py")
        return 1

    OFFICIAL.write_text(text)

    print("official : %s" % OFFICIAL)
    print("served   : GET /ask-aruvi (signed-in only; cached on the device)")
    print("pairs    : %d  %s" % (len(pairs), dict(Counter(p['category'] for p in pairs))))
    print("re-indexed: %d pair(s) changed" % len(stale))
    if stale:
        print("            %s" % ", ".join(stale[:12]) + (" …" if len(stale) > 12 else ""))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
