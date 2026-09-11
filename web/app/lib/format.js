/* ───────── shared formatting helpers — the web's face of @aruvi/shared/format ─────────
 * Everything here moved to packages/shared/src/format.js on 2026-09-11 (Track D step 1) so
 * the phone runs the same code; components keep importing "../lib/format" unchanged. The one
 * thing that stays on this side is boldMarks, because it builds React elements. */
import "./shared-setup";
import { parseBold } from "@aruvi/shared/format";
export * from "@aruvi/shared/format";

/* Render a string with `**…**` markdown-bold spans as React nodes. Used for homework lines,
 * where the maths normalizer wraps the textbook locator (e.g. "Figure it Out Q11, section 5.2
 * p.115") in `**…**` so the reference alone reads bold. Plain strings (no markers) return as-is.
 * Returns an array of strings / <strong> elements suitable for direct use as React children. */
export function boldMarks(text) {
  const runs = parseBold(text);
  if (runs.length === 1 && !runs[0].bold) return runs[0].text;
  return runs.map((r, i) => (r.bold ? <strong key={i}>{r.text}</strong> : r.text));
}
