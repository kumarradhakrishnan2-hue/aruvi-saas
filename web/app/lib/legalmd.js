"use client";
/* ── The legal document's markdown, rendered as React nodes (2026-08-27) ──
 * The PARSER moved to packages/shared/src/legalmd.js on 2026-09-11 (its header has the
 * reasoning: hand-rolled, never emits markup). This file turns its blocks into the same
 * `lgl-*` elements as before — Agreement, PrivacyNotice and Settings › Legal are unchanged.
 * Each td carries its column heading as `data-th` — at phone widths the CSS stacks a row
 * into a card and prints that heading before each cell, so a four-column table stays
 * readable at 360px without a sideways scroll. */
import "./shared-setup";
import { parseMarkdown } from "@aruvi/shared/legalmd";
export { dateWords, parseMarkdown, parseInline } from "@aruvi/shared/legalmd";

const inline = (runs, keyBase) =>
  runs.map((r, i) =>
    r.bold ? <strong key={`${keyBase}-b-${i}`}>{r.text}</strong>
    : r.italic ? <em key={`${keyBase}-i-${i}`}>{r.text}</em>
    : r.text);

/* Markdown → React nodes. `keyBase` keeps keys unique when a page renders several
 * blocks (the five acknowledgement bodies sit on one screen). */
export function renderMarkdown(md, keyBase = "md") {
  return parseMarkdown(md).map((b, k) => {
    const key = `${keyBase}-${b.type}-${k}`;
    switch (b.type) {
      case "h2": return <p className="lgl-h2" key={key}>{inline(b.runs, key)}</p>;
      case "h3": return <p className="lgl-h3" key={key}>{inline(b.runs, key)}</p>;
      case "p": return <p className="lgl-p" key={key}>{inline(b.runs, key)}</p>;
      case "hr": return <hr className="lgl-hr" key={key} />;
      case "ul":
        return (
          <ul className="lgl-ul" key={key}>
            {b.items.map((runs, i) => <li key={i}>{inline(runs, `${key}-${i}`)}</li>)}
          </ul>);
      case "table":
        return (
          <div className="lgl-tablewrap" key={key}>
            <table className="lgl-table">
              <thead>
                <tr>{b.head.map((runs, i) => <th key={i}>{inline(runs, `${key}-th-${i}`)}</th>)}</tr>
              </thead>
              <tbody>
                {b.rows.map((row, ri) => (
                  <tr key={ri}>
                    {row.map((runs, ci) => (
                      <td key={ci} data-th={b.headText[ci]}>{inline(runs, `${key}-td-${ri}-${ci}`)}</td>
                    ))}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>);
      default: return null;
    }
  });
}
