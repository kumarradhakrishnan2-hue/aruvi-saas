/* The MEYY wordmark, inline (2026-09-03).
 *
 * Source: web/app/icons/3a-wordmark-{light,dark}.svg — the two files are byte-identical
 * except for the stroke colour (#201e1d ink / #f5ead8 cream), so ONE component with
 * `stroke="currentColor"` replaces both: the mark takes whatever `color` its context sets,
 * and on the pine bar that is `--bar-ink`, in both themes. The square 4a/4b app icons are
 * for the app stores and are deliberately not used here.
 *
 * Inlined rather than <img src> so it (a) inherits colour like text, (b) needs no next/image
 * or static-asset config, and (c) paints on first render with no request. The two dots are
 * classed (`.brand-mark-dot`) so CSS can lift the red on the pine fill — the brand's own
 * #d63a2f measures 2.35:1 on #164436, the same "goes muddy on pine" defect the Aruvi dot was
 * given #e0705f (3.48:1) for. Sizing lives in globals.css (`.brand-mark`).
 *
 * The source viewBox is 0 0 400 110 (letters span y 22–95, the dots sit above the Y's at
 * y 0–18). The viewBox here is TRIMMED to the ink on the x-axis — the M's round cap starts
 * at x = 20 − 7.5 = 12.5 and the last Y's arm ends at 378 + 7.5 = 385.5 — so the mark's
 * left edge IS the M's edge and it sits flush over the L of "lesson studio" beneath it
 * (founder, 2026-09-03; the untrimmed box indented it ~2.5px). Height is left at 110 so the
 * glyph scale for a given CSS height is unchanged. */
export default function MeyyMark({ className = "brand-mark", label = "MEYY" }) {
  return (
    <svg
      className={className}
      viewBox="12.5 0 413 110"
      preserveAspectRatio="xMinYMid meet"
      role="img"
      aria-label={label}
      fill="none"
      stroke="currentColor"
      strokeWidth="15"
      strokeLinecap="round"
      strokeLinejoin="round"
    >
      <title>{label}</title>
      {/* M */}
      <path d="M20 95V22L62 66L104 22V95" />
      {/* E — three bars */}
      <path d="M148 22h64M148 58h64M148 94h64" />
      {/* Y Y */}
      <path d="M268 95V60L240 26M268 60l28-34M350 95V60L322 26M350 60l28-34" />
      {/* the two red dots */}
      <circle className="brand-mark-dot" cx="268" cy="9" r="9" stroke="none" />
      <circle className="brand-mark-dot" cx="350" cy="9" r="9" stroke="none" />
      {/* ™ — circled, at the top-right of the cap height (founder, 2026-09-03; chosen over
          the plain superscript from three placements shown). Ring ≈ 40% of the cap height,
          in the stroke colour; the viewBox grew 373 → 413 units to hold it. */}
      <circle cx="409" cy="30" r="15" strokeWidth="2.5" />
      <text x="409" y="34.7" textAnchor="middle" fontFamily="Helvetica, Arial, sans-serif"
            fontWeight="700" fontSize="13" fill="currentColor" stroke="none">TM</text>
    </svg>
  );
}
