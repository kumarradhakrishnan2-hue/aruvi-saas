/* ───────── Ask Aruvi · deterministic keyword search ─────────
 * No LLM. A query is tokenised, normalised, and ranked against each pair's
 * index by how many query words it matches — best match first, with a count.
 *
 * normalize() MUST stay identical to build_kb.py's norm() so the keywords
 * baked into qa_knowledge_base.json line up with what a teacher types.
 *
 * Field weights (a query word scores the strongest field it hits):
 *     keyword 3   ·   question 2   ·   answer 1
 * "Additive" = ranking, NOT a strict AND filter: adding a word re-ranks and
 * narrows, but a two-word query never silently collapses to an empty screen —
 * best-match rises, and the caller always shows the live result count.
 */

// strip combining marks (accents) — mirrors Python NFD + Mn removal
function stripAccents(s) {
  return s.normalize("NFD").replace(/[̀-ͯ]/g, "");
}

// canonical match key for a single word (mirror of build_kb.py norm())
export function normalize(word) {
  let t = stripAccents(String(word).toLowerCase()).replace(/[^a-z0-9]/g, "");
  if (t.length > 4 && t.endsWith("ies")) t = t.slice(0, -3) + "y";
  else if (t.length > 4 && /(s|x|z|ch|sh)es$/.test(t)) t = t.slice(0, -2);
  else if (t.length > 3 && t.endsWith("s") && !t.endsWith("ss") && !t.endsWith("us")) t = t.slice(0, -1);
  return t;
}

// text → array of normalised tokens (≥2 chars)
export function tokenize(text) {
  const out = [];
  const raw = String(text).match(/[A-Za-z0-9]+/g) || [];
  for (const w of raw) {
    const n = normalize(w);
    if (n.length >= 2) out.push(n);
  }
  return out;
}

// Precompute a pair's searchable index once (memoised on the pair object).
function indexOf(pair) {
  if (pair.__idx) return pair.__idx;
  const keys = new Set((pair.keywords || []).map(normalize));
  const q = new Set(tokenize(pair.question));
  const a = new Set(tokenize(pair.answer));
  const idx = { keys, q, a, all: new Set([...keys, ...q, ...a]) };
  Object.defineProperty(pair, "__idx", { value: idx, enumerable: false });
  return idx;
}

// best field weight a single query token hits in one pair (0 = miss)
function tokenWeight(idx, tok) {
  const hit = (set, w) => {
    if (set.has(tok)) return w;
    if (tok.length >= 3) { for (const t of set) if (t.startsWith(tok)) return w; } // partial typing
    return 0;
  };
  return Math.max(hit(idx.keys, 3), hit(idx.q, 2), hit(idx.a, 1));
}

/**
 * search(pairs, query)
 *   → null                       when the query is empty (caller shows categories)
 *   → { count, results: [pair] } ranked best-match-first, misses dropped
 */
export function search(pairs, query) {
  const qToks = [...new Set(tokenize(query))];
  if (qToks.length === 0) return null;

  const scored = [];
  pairs.forEach((pair, i) => {
    const idx = indexOf(pair);
    let score = 0, matched = 0;
    for (const tok of qToks) {
      const w = tokenWeight(idx, tok);
      if (w > 0) { score += w; matched += 1; }
    }
    if (score > 0) scored.push({ pair, score, matched, i });
  });

  scored.sort((x, y) =>
    y.matched - x.matched ||  // more query words satisfied wins
    y.score - x.score ||      // then stronger fields
    x.i - y.i                 // then stable original order
  );

  return { count: scored.length, results: scored.map((s) => s.pair) };
}
