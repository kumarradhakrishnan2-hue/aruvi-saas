"use client";
/* ── The legal document's markdown, rendered as React nodes (2026-08-27) ──
 *
 * The user agreement is authored as markdown and served, parsed, by GET /legal/consent
 * (api/legal.py). Two surfaces render it — the subscribe wizard's Agreement step and
 * Settings › Legal — so the renderer lives here rather than in either of them.
 *
 * WHY A HAND-ROLLED ONE. Two reasons, and the second is the real one:
 *   1. No npm dependency is added for ~60 lines of a document whose shape we control.
 *   2. It builds React NODES. A markdown library would hand back an HTML string, and
 *      the only way to show that is dangerouslySetInnerHTML — script injection into the
 *      one screen where a teacher signs something is not a risk worth any convenience.
 *      Nothing here can emit a tag; every branch returns an element we constructed.
 *
 * It handles exactly what the document uses: `##`/`###` headings, `- ` bullets, `---`
 * rules, blank-line-separated paragraphs, and `**bold**` inline (via format.js's
 * boldMarks, the same helper the lesson renderers use). A line it does not recognise
 * renders as a plain paragraph — degrading to readable text, never to nothing.
 *
 * Class names are namespaced `lgl-*` and styled once in globals.css. */
import { boldMarks } from "./format";

/* Inline: **bold** first, then *italic* around what survives. The document's italic runs
 * are whole paragraphs (its intro lines), so a simple pass is enough — and a stray
 * asterisk falls through as the character it is rather than eating the rest of a line. */
function inline(text, keyBase) {
  const bolded = boldMarks(String(text ?? ""));
  const parts = Array.isArray(bolded) ? bolded : [bolded];
  const out = [];
  parts.forEach((p, i) => {
    if (typeof p !== "string") { out.push(p); return; }
    const re = /\*([^*]+)\*/g;
    let last = 0, m, n = 0;
    while ((m = re.exec(p)) !== null) {
      if (m.index > last) out.push(p.slice(last, m.index));
      out.push(<em key={`${keyBase}-i-${i}-${n++}`}>{m[1]}</em>);
      last = re.lastIndex;
    }
    if (last < p.length) out.push(p.slice(last));
  });
  return out;
}

/* Markdown → React nodes. `keyBase` keeps keys unique when a page renders several
 * blocks (the five acknowledgement bodies sit on one screen). */
export function renderMarkdown(md, keyBase = "md") {
  const lines = String(md ?? "").split("\n");
  const nodes = [];
  let para = [];
  let bullets = [];
  let k = 0;

  const flushPara = () => {
    if (!para.length) return;
    const text = para.join(" ").trim();
    para = [];
    if (text) nodes.push(<p className="lgl-p" key={`${keyBase}-p-${k++}`}>{inline(text, `${keyBase}-${k}`)}</p>);
  };
  const flushBullets = () => {
    if (!bullets.length) return;
    const items = bullets;
    bullets = [];
    nodes.push(
      <ul className="lgl-ul" key={`${keyBase}-ul-${k++}`}>
        {items.map((b, i) => <li key={i}>{inline(b, `${keyBase}-${k}-${i}`)}</li>)}
      </ul>);
  };
  const flush = () => { flushPara(); flushBullets(); };

  for (const raw of lines) {
    const s = raw.trim();

    if (!s) { flush(); continue; }
    if (s === "---") { flush(); nodes.push(<hr className="lgl-hr" key={`${keyBase}-hr-${k++}`} />); continue; }

    const h = /^(#{1,4})\s+(.*)$/.exec(s);
    if (h) {
      flush();
      const level = h[1].length;
      // The document's own `#`/`##` become one visual heading and `###` a smaller one —
      // its heading levels describe the DOCUMENT's structure, not a type scale.
      const cls = level <= 2 ? "lgl-h2" : "lgl-h3";
      nodes.push(<p className={cls} key={`${keyBase}-h-${k++}`}>{inline(h[2], `${keyBase}-${k}`)}</p>);
      continue;
    }

    const b = /^[-*]\s+(.*)$/.exec(s);
    if (b) { flushPara(); bullets.push(b[1]); continue; }

    /* The document hard-wraps long bullets: the continuation lines are indented under
     * their `- ` in the source and carry no marker of their own. While a list is open,
     * a plain line therefore BELONGS to the last bullet — pushing it as a paragraph
     * would drop half the bullet outside the list, which is exactly the bug this
     * branch fixes. A blank line is what closes a list (handled above). */
    if (bullets.length) { bullets[bullets.length - 1] += " " + s; continue; }

    para.push(s);
  }
  flush();
  return nodes;
}

/* "2026-08-27T09:12:44+00:00" → "27 August 2026". Empty in, empty out — the callers all
 * have a "not accepted yet" state and none of them wants the string "Invalid Date". */
export function dateWords(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  return d.toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
}
