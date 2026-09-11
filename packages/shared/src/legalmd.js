/* ── The legal document's markdown, PARSED (2026-08-27; lifted to shared 2026-09-11) ──
 *
 * The user agreement and the privacy notice are authored as markdown and served, parsed, by
 * GET /legal/consent and GET /legal/privacy (api/legal.py). Three surfaces render them — the
 * subscribe wizard's Agreement step, Settings › Legal, and now the phone — so the PARSER
 * lives here and each app renders the blocks it returns.
 *
 * WHY A HAND-ROLLED ONE. Two reasons, and the second is the real one:
 *   1. No dependency is added for ~80 lines of a document whose shape we control.
 *   2. It never produces markup. A markdown library would hand back an HTML string, and the
 *      only way to show that is dangerouslySetInnerHTML — script injection into the one
 *      screen where a teacher signs something is not a risk worth any convenience. This
 *      returns DATA; the renderers build every element themselves.
 *
 * It handles exactly what the documents use: `#`–`####` headings (the document's `#`/`##`
 * become one visual heading, `###`+ a smaller one — its levels describe the DOCUMENT's
 * structure, not a type scale), `- ` bullets with hard-wrapped continuation lines, `---`
 * rules, pipe tables (the Privacy Notice's §2/§6/§7: DPDP Rule 3 wants an ITEMISED account —
 * data · purpose · basis per row), and `**bold**` / `*italic*` inline. A line it does not
 * recognise becomes a plain paragraph — degrading to readable text, never to nothing.
 *
 * Output — an array of blocks:
 *   { type: "h2" | "h3" | "p", runs }
 *   { type: "ul", items: [runs, …] }
 *   { type: "hr" }
 *   { type: "table", head: [runs, …], headText: [string, …], rows: [[runs, …], …] }
 * where `runs` is [{ text, bold, italic }] from `parseInline`. `headText` is the header cell
 * with its markers stripped — the web prints it as data-th so a four-column table stacks into
 * a card at 360px; the phone will want the same label. */
import { parseBold } from "./format.js";

/* Inline: **bold** first, then *italic* around what survives. The document's italic runs are
 * whole paragraphs (its intro lines), so a simple pass is enough — and a stray asterisk falls
 * through as the character it is rather than eating the rest of a line. */
export function parseInline(text) {
  const out = [];
  for (const run of parseBold(String(text ?? ""))) {
    if (run.bold) { out.push({ text: run.text, bold: true, italic: false }); continue; }
    const p = run.text;
    const re = /\*([^*]+)\*/g;
    let last = 0, m;
    while ((m = re.exec(p)) !== null) {
      if (m.index > last) out.push({ text: p.slice(last, m.index), bold: false, italic: false });
      out.push({ text: m[1], bold: false, italic: true });
      last = re.lastIndex;
    }
    if (last < p.length) out.push({ text: p.slice(last), bold: false, italic: false });
  }
  return out;
}

export function parseMarkdown(md) {
  const lines = String(md ?? "").split("\n");
  const blocks = [];
  let para = [];
  let bullets = [];
  let table = null;   // { head: [], rows: [[]] } while a pipe table is open

  const splitRow = (s) => {
    const cells = s.split("|");
    if (cells.length && !cells[0].trim()) cells.shift();
    if (cells.length && !cells[cells.length - 1].trim()) cells.pop();
    return cells.map((c) => c.trim());
  };
  const isSep = (cells) => cells.length > 0 && cells.every((c) => /^:?-{2,}:?$/.test(c));
  const flushTable = () => {
    if (!table) return;
    const t = table;
    table = null;
    if (!t.head.length) return;
    blocks.push({
      type: "table",
      head: t.head.map(parseInline),
      headText: t.head.map((h) => h.replace(/\*\*/g, "")),
      // every row is squared to the header's width, so a short row never shifts a column
      rows: t.rows.map((r) => t.head.map((_, ci) => parseInline(r[ci] ?? ""))),
    });
  };
  const flushPara = () => {
    if (!para.length) return;
    const text = para.join(" ").trim();
    para = [];
    if (text) blocks.push({ type: "p", runs: parseInline(text) });
  };
  const flushBullets = () => {
    if (!bullets.length) return;
    const items = bullets;
    bullets = [];
    blocks.push({ type: "ul", items: items.map(parseInline) });
  };
  const flush = () => { flushPara(); flushBullets(); flushTable(); };

  for (const raw of lines) {
    const s = raw.trim();
    if (!s) { flush(); continue; }

    if (s.startsWith("|")) {
      flushPara(); flushBullets();
      const cells = splitRow(s);
      if (!table) { table = { head: cells, rows: [] }; continue; }
      if (isSep(cells)) continue;
      table.rows.push(cells);
      continue;
    }
    if (table) flushTable();   // a non-pipe line closes an open table
    if (s === "---") { flush(); blocks.push({ type: "hr" }); continue; }

    const h = /^(#{1,4})\s+(.*)$/.exec(s);
    if (h) {
      flush();
      blocks.push({ type: h[1].length <= 2 ? "h2" : "h3", runs: parseInline(h[2]) });
      continue;
    }

    const b = /^[-*]\s+(.*)$/.exec(s);
    if (b) { flushPara(); bullets.push(b[1]); continue; }

    /* The document hard-wraps long bullets: the continuation lines are indented under their
     * `- ` in the source and carry no marker of their own. While a list is open, a plain line
     * therefore BELONGS to the last bullet — pushing it as a paragraph would drop half the
     * bullet outside the list. A blank line is what closes a list (handled above). */
    if (bullets.length) { bullets[bullets.length - 1] += " " + s; continue; }

    para.push(s);
  }
  flush();
  return blocks;
}

/* "2026-08-27T09:12:44+00:00" → "27 August 2026". Empty in, empty out — the callers all
 * have a "not accepted yet" state and none of them wants the string "Invalid Date". */
export function dateWords(iso) {
  if (!iso) return "";
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return "";
  return d.toLocaleDateString("en-IN", { day: "numeric", month: "long", year: "numeric" });
}
