"use client";
import { useEffect, useRef, useState } from "react";

// Shared offscreen canvas for text measurement (auto-fit). One per module — cheap, never in DOM.
let _fitCanvas = null;
function _maxLabelWidth(items, font) {
  if (typeof document === "undefined") return 0;
  _fitCanvas = _fitCanvas || document.createElement("canvas");
  const ctx = _fitCanvas.getContext("2d");
  ctx.font = font;
  let w = 0;
  (items || []).forEach((it) => { w = Math.max(w, ctx.measureText(String(it.label)).width); });
  return w;
}

/* ───────── wheels — the shared selection boxes (extracted from FirstRun.jsx, 2026-07-02) ─────────
 * ONE UI for collecting values everywhere (first run AND the Settings profile redo — the
 * founder's "avoid multiple types of UI" rule):
 *   • RollWheel — single-value pick: one visible row, roll/scroll/arrow to cycle, whatever
 *     settles in the box IS the pick.
 *   • PickWheel — multi-value pick: fixed-height 4-row scroll window, tap any visible row to
 *     toggle it, ▲▼ side arrows for phones.
 * Styling lives in globals.css under .fr-wheel* / .fr-sec-* (unchanged class names, so the
 * extraction is invisible to CSS). */

export const WHEEL_ROW = 64;  // px height of RollWheel's single visible row (shared with CSS)
export const PICK_ROW = 52;   // px height of one PickWheel row (4 visible at once = 208px)

/* Step a scroll box by exactly one row, robustly (B1, 2026-07-06). The ▲▼ arrow buttons used a
 * relative scrollBy({behavior:"smooth"}), which some engines silently no-op when smooth-scroll is
 * throttled — a background/inactive tab, prefers-reduced-motion, or certain mobile browsers — so
 * the arrows appeared dead there (drag always worked). This computes the ABSOLUTE target row from
 * the current position, animates to it when motion is allowed, and GUARANTEES the move: a short
 * fallback snaps scrollTop directly if the smooth scroll didn't take. Also honours reduced-motion
 * (jump instantly rather than animate). */
export function stepScroll(el, dir, rowPx, rowCount) {
  if (!el) return;
  const cur = Math.round(el.scrollTop / rowPx);
  const max = Math.max(0, (rowCount || 0) - 1);
  const target = rowCount ? Math.min(max, Math.max(0, cur + dir)) : cur + dir;
  const top = target * rowPx;
  const reduce = typeof window !== "undefined"
    && typeof window.matchMedia === "function"
    && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  try {
    el.scrollTo({ top, behavior: reduce ? "auto" : "smooth" });
  } catch {
    el.scrollTop = top; // very old engines without the options form
  }
  // If smooth-scroll was suppressed, the box hasn't landed on the target row shortly after —
  // snap it there directly so the arrow is never a no-op.
  setTimeout(() => {
    if (el && Math.round(el.scrollTop / rowPx) !== target) el.scrollTop = top;
  }, 240);
}

// One gesture demo per page load: whichever RollWheel the teacher meets FIRST rocks a few px
// and settles back, so the box demonstrates its own gesture (words get missed).
let wheelDemoDone = false;

/* RollWheel — a single box, the footprint of one option row, showing exactly ONE item at a
 * time. Rolling (drag / scroll / mouse-wheel / arrow keys) cycles the list through it;
 * scroll-snap settles on a row and whichever item landed in the box IS the pick — no separate
 * confirm tap. items: [{ id, chip?, label }] · value: id string · onChange(id)
 * large: one-notch-bigger label for short lists; longer lists (chapter titles) stay smaller. */
// `rowPx` (default WHEEL_ROW=64) sets the single visible row's height AND the scroll-snap step —
// they MUST stay equal or snapping lands between rows. A caller wanting a more compact wheel
// (e.g. My Lessons' Subject/Grade) passes a smaller rowPx; first-run passes nothing and keeps 64.
export function RollWheel({ items, value, onChange, ariaLabel, large, rowPx = WHEEL_ROW, fit = false, peek = false }) {
  const ref = useRef(null);
  const settleTimer = useRef(null);
  const idBase = String(ariaLabel || "wheel").toLowerCase().replace(/\W+/g, "-");
  const rowStyle = rowPx !== WHEEL_ROW ? { height: rowPx } : undefined;
  // Peek mode (My Lessons Subject/Class): a single compact WHITE row showing ONLY the item in use
  // — no dimmed neighbours (founder ask, 2026-07-21). Same one-row footprint as the base wheel;
  // the styling (white box, larger font, single cycling ▼) is all in CSS + the label sizing below.
  const wheelStyle = rowStyle;
  // Continuous wheeling (peek): render the list THREE times and ride the middle copy, recentring
  // after each settle, so dragging/scrolling wraps around forever — matching the ▼ arrow (which
  // already cycles). Only in peek with >1 item; the base wheel (FirstRun) is untouched.
  const N = items.length;
  const loop = peek && N > 1;
  const selIdx = items.findIndex((it) => String(it.id) === String(value));
  const renderItems = loop
    ? Array.from({ length: 3 * N }, (_, i) => ({ ...items[i % N], _i: i }))
    : items.map((it, i) => ({ ...it, _i: i }));
  // Auto-fit (opt-in): shrink the label font just enough that the LONGEST option shows in full,
  // never clipped by the box — for long words on narrow columns (e.g. "Mathematics" on a phone).
  // Measured at the base size (never the already-shrunk inline size, so it can't compound) and at
  // the bold weight (the settled row is bold), so the visible value always fits.
  const [fitPx, setFitPx] = useState(null);

  // whatever settles in the box becomes the pick
  const onScroll = () => {
    if (settleTimer.current) clearTimeout(settleTimer.current);
    settleTimer.current = setTimeout(() => {
      const el = ref.current;
      if (!el || !N) return;
      if (loop) {
        const raw = Math.round(el.scrollTop / rowPx);
        const real = ((raw % N) + N) % N;
        if (items[real]) onChange(String(items[real].id));
        // Silently hop back into the middle copy whenever we've drifted into the first/last one,
        // so there's always another copy to keep scrolling into (seamless — the recentred row
        // shows the identical item).
        if (raw < N || raw >= 2 * N) el.scrollTop = (N + real) * rowPx;
      } else {
        const idx = Math.min(N - 1, Math.max(0, Math.round(el.scrollTop / rowPx)));
        if (items[idx]) onChange(String(items[idx].id));
      }
    }, 120);
  };

  // moves exactly one row; shared by the keyboard handler AND the ▲▼ cue buttons below, so
  // tapping a cue behaves identically to pressing an arrow key
  const step = (dir) => stepScroll(ref.current, dir, rowPx, items.length);

  // Peek mode's single down arrow: advance to the next item and WRAP from the last back to the
  // first (founder ask, 2026-07-21). Index off the CURRENT value (not the live scrollTop, which
  // may be mid-animation) and commit the pick via onChange immediately, so the selection always
  // changes on tap even if the smooth-scroll is throttled; then move the box to match.
  const stepCycle = () => {
    if (!N) return;
    const curIdx = Math.max(0, items.findIndex((it) => String(it.id) === String(value)));
    const next = (curIdx + 1) % N;
    onChange(String(items[next].id));   // commit immediately so a throttled scroll never no-ops
    const el = ref.current;
    if (!el) return;
    const reduce = typeof window !== "undefined" && typeof window.matchMedia === "function"
      && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    if (loop) {
      // Ride one row further DOWN the middle/last copy; onScroll recentres. Always down, so the
      // wrap (last → first) is a smooth continuation rather than a jump back up.
      try { el.scrollBy({ top: rowPx, behavior: reduce ? "auto" : "smooth" }); }
      catch { el.scrollTop = el.scrollTop + rowPx; }
    } else {
      const top = next * rowPx;
      try { el.scrollTo({ top, behavior: reduce ? "auto" : "smooth" }); }
      catch { el.scrollTop = top; }
    }
  };

  const onKeyDown = (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); step(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); step(-1); }
  };

  // keep the value valid whenever the list (re)loads — default to the first item
  useEffect(() => {
    if (!items.length) return;
    if (!items.some((it) => String(it.id) === String(value))) onChange(String(items[0].id));
  }, [items]); // eslint-disable-line react-hooks/exhaustive-deps

  // position the roll on the current pick whenever the wheel (re)mounts or the list changes
  useEffect(() => {
    const el = ref.current;
    const idx = items.findIndex((it) => String(it.id) === String(value));
    if (el && idx >= 0) el.scrollTop = (loop ? N + idx : idx) * rowPx;
  }, [items]); // eslint-disable-line react-hooks/exhaustive-deps

  // one-time gesture demo (see wheelDemoDone above)
  useEffect(() => {
    if (wheelDemoDone || items.length < 2) return;
    const el = ref.current;
    if (!el) return;
    wheelDemoDone = true;
    const idx = Math.max(0, items.findIndex((it) => String(it.id) === String(value)));
    const dir = idx >= items.length - 1 ? -1 : 1; // rock away from the list's edge
    const t1 = setTimeout(() => el.scrollBy({ top: dir * 22, behavior: "smooth" }), 500);
    const t2 = setTimeout(() => el.scrollBy({ top: -dir * 22, behavior: "smooth" }), 1000);
    return () => { clearTimeout(t1); clearTimeout(t2); };
  }, [items]); // eslint-disable-line react-hooks/exhaustive-deps

  // Recompute the fit font whenever the option set, the size class, or the viewport changes.
  useEffect(() => {
    if (!fit || typeof window === "undefined") return;
    let cancelled = false;
    const compute = () => {
      const el = ref.current;
      if (!el || cancelled) return;
      const rowEl = el.querySelector(".fr-wheel-row");
      const labelEl = el.querySelector(".fr-wheel-label");
      if (!rowEl || !labelEl) return;
      const rs = getComputedStyle(rowEl);
      const family = getComputedStyle(labelEl).fontFamily || "serif";
      const base = (large ? 17 : 15) + (peek ? 12 : 0);   // peek Subject reads ~six notches larger; design base (NOT the shrunk inline size)
      const avail = rowEl.clientWidth - parseFloat(rs.paddingLeft || 0) - parseFloat(rs.paddingRight || 0);
      if (!avail || avail <= 0) return;
      const maxW = _maxLabelWidth(items, `600 ${base}px ${family}`);
      const px = maxW > avail ? Math.max(12, Math.floor((base * avail / maxW) * 10) / 10) : base;
      if (!cancelled) setFitPx(px);
    };
    compute();
    window.addEventListener("resize", compute);
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(compute).catch(() => {});
    return () => { cancelled = true; window.removeEventListener("resize", compute); };
  }, [fit, items, large, rowPx, peek]);

  const labelStyle = fit && fitPx ? { fontSize: `${fitPx}px` } : undefined;
  return (
    <div className={`fr-wheel-shell ${large ? "fr-wheel-lg" : ""} ${peek ? "peek" : ""}`}>
      <div className={`fr-wheel ${peek ? "peek" : ""}`} ref={ref} onScroll={onScroll} onKeyDown={onKeyDown}
        role="listbox" tabIndex={0} aria-label={ariaLabel} style={wheelStyle}
        aria-activedescendant={selIdx >= 0 ? `${idBase}-opt-${loop ? N + selIdx : selIdx}` : undefined}>
        {renderItems.map((it) => {
          const sel = String(value) === String(it.id);
          return (
            <div key={it._i} id={`${idBase}-opt-${it._i}`} style={rowStyle}
              className="fr-wheel-row" role="option" aria-selected={sel}>
              {it.chip != null && <span className={`fr-opt-chip ${sel ? "on" : ""}`}>{it.chip}</span>}
              <span className="fr-wheel-label" style={labelStyle}>{it.label}</span>
            </div>
          );
        })}
      </div>
      {/* real step buttons, not decoration — a tap-friendly alternative for anyone who'd
          rather not drag/scroll-wheel the box itself */}
      <span className={`fr-wheel-cue ${peek ? "single" : ""}`}>
        {peek ? (
          // One down arrow: steps forward and wraps last → first, so the whole list is reachable
          // by tapping the same control (no up arrow).
          <button type="button" className="fr-wheel-cue-btn" onClick={stepCycle}
            aria-label={`Next ${ariaLabel || "option"}`}>▼</button>
        ) : (
          <>
            <button type="button" className="fr-wheel-cue-btn" onClick={() => step(-1)} aria-label={`Previous ${ariaLabel || "option"}`}>▲</button>
            <button type="button" className="fr-wheel-cue-btn" onClick={() => step(1)} aria-label={`Next ${ariaLabel || "option"}`}>▼</button>
          </>
        )}
      </span>
    </div>
  );
}

/* PickWheel — a reusable fixed-height (exactly 4 rows visible) scrollable multi-select "wheel":
 * drag/swipe through the full option list, or tap the bare ▲▼ arrows beside it to step one row
 * (phones aren't always obviously drag-scrollable). Any visible row toggles on tap, independent
 * of scroll position — no cap on how many can be picked. Its Done/Continue button is passed in
 * as `children` so it lands in the SAME column as the wheel (its width then always equals the
 * row list's width; the arrows live outside that column entirely, so they never affect it).
 * `initialScrollTo` positions the wheel on mount without that option being pre-picked.
 * Because only 4 rows are visible at a time, a teacher who scrolls to pick from a later batch
 * can't see the earlier ones and may leave a stray tick behind — so a running "chosen so far"
 * line sits UNDER the Continue/Done button, always listing the full current selection (in option
 * order) no matter where the wheel is scrolled. Set `summaryLabel={false}` to suppress it. */
export function PickWheel({ options, selected, onToggle, labelFor, initialScrollTo, ariaLabel, children, summaryLabel = true }) {
  const wheelRef = useRef(null);
  const step = (dir) => stepScroll(wheelRef.current, dir, PICK_ROW, options.length);
  const onKeyDown = (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); step(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); step(-1); }
  };
  const showCue = options.length > 4;

  // Running confirmation of the full current selection, in option order (independent of scroll
  // position), so a stray tick from an earlier, now-scrolled-away batch stays visible.
  const chosen = options.filter((o) => selected.includes(o));
  const summary = chosen.map((o) => (labelFor ? labelFor(o) : String(o))).join(", ");

  useEffect(() => {
    const el = wheelRef.current;
    if (!el || initialScrollTo == null) return;
    const idx = options.indexOf(initialScrollTo);
    if (idx >= 0) el.scrollTop = idx * PICK_ROW;
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="fr-sec-wheel-wrap">
      <div className="fr-sec-wheel-col">
        <div className="fr-sec-list fr-sec-wheel" ref={wheelRef} onKeyDown={onKeyDown} tabIndex={0}
          role="listbox" aria-label={ariaLabel} aria-multiselectable="true">
          {options.map((o) => {
            const on = selected.includes(o);
            return (
              <button type="button" key={o} className={`fr-sec-opt ${on ? "on" : ""}`} onClick={() => onToggle(o)}
                role="option" aria-selected={on}>
                <span className="fr-sec-check">{on ? "✓" : ""}</span>
                <span className="fr-sec-label">{labelFor ? labelFor(o) : o}</span>
              </button>
            );
          })}
        </div>
        {children}
        {summaryLabel && (
          <p className="fr-pick-summary" role="status" aria-live="polite">
            {chosen.length
              ? <>Chosen ({chosen.length}): <b>{summary}</b></>
              : <span className="fr-pick-summary-empty">Nothing chosen yet — tap the rows above</span>}
          </p>
        )}
      </div>
      {showCue && (
        // Bare arrows beside the wheel — no bordered/background box around them, just the two
        // glyphs sitting directly on the body, height-matched to the wheel only.
        <div className="fr-sec-arrows-side">
          <button type="button" className="fr-sec-arrow-btn" onClick={() => step(-1)} aria-label="Scroll up">▲</button>
          <button type="button" className="fr-sec-arrow-btn" onClick={() => step(1)} aria-label="Scroll down">▼</button>
        </div>
      )}
    </div>
  );
}

/* ───────── periods/week capture — shared by FirstRun's profile acquisition AND (a copy of) the
 * Settings profile editor. periods/week is stored PER DURATION TYPE (ppw_by_duration:
 * { [minutes]: count }); the weekly total is their SUM, never asked directly. See MEMORY.md
 * 2026-07-05. NOTE: TeachingProfile.jsx still carries its OWN identical copy of normPpw/ppwMapSum/
 * PpwCapture + these constants — migrating it to import from here is a deferred cleanup. ───────── */
export const DEFAULT_DURATION = 40;
export const DEFAULT_PPW = 6;
export const DURATION_CHOICES = Array.from({ length: 21 }, (_, i) => 20 + i * 5); // 20,25,…120 min
export const PPW_CHOICES = Array.from({ length: 14 }, (_, i) => i + 1);           // 1…14 periods/week

export const ppwMapSum = (m) => Object.keys(m || {}).reduce((a, k) => a + (Number(m[k]) || 0), 0);
// Reconcile a per-duration weekly-count map to the CURRENT durations: keep each surviving count;
// a duration with no count yet defaults to the whole total when there's a single type, else to 1.
export const normPpw = (durations, map, fallbackPpw) => {
  const durs = (durations && durations.length) ? durations : [DEFAULT_DURATION];
  const out = {};
  durs.forEach((d) => {
    const v = Number((map || {})[d] ?? (map || {})[String(d)]);
    out[d] = v > 0 ? v : (durs.length === 1 ? (Number(fallbackPpw) || DEFAULT_PPW) : 1);
  });
  return out;
};

// Single duration → the same large periods/week wheel; >1 duration → a two-column table
// (Duration · a −/number/+ stepper per row, up to three) with a live weekly total.
export function PpwCapture({ durations, map, onSet }) {
  const durs = (durations && durations.length) ? durations : [DEFAULT_DURATION];
  if (durs.length === 1) {
    const d = durs[0];
    const val = Number(map[d] ?? map[String(d)]) || DEFAULT_PPW;
    return (
      <RollWheel ariaLabel="Periods per week" large value={String(val)}
        onChange={(v) => onSet(d, Number(v))}
        items={PPW_CHOICES.map((p) => ({ id: String(p), chip: p, label: p === 1 ? "period a week" : "periods a week" }))} />
    );
  }
  const total = durs.reduce((a, d) => a + (Number(map[d] ?? map[String(d)]) || 0), 0);
  return (
    <div className="tp-ppw-table">
      <div className="tp-ppw-row tp-ppw-head">
        <span className="tp-ppw-dur">Duration</span>
        <span className="tp-ppw-ct">Periods / week</span>
      </div>
      {durs.map((d) => {
        const val = Number(map[d] ?? map[String(d)]) || 1;
        return (
          <div className="tp-ppw-row" key={d}>
            <span className="tp-ppw-dur">{d} min</span>
            <span className="tp-ppw-stepper">
              <button type="button" className="tp-val-btn" aria-label={`Fewer ${d}-minute periods`} onClick={() => onSet(d, Math.max(1, val - 1))}>−</button>
              <input type="number" className="tp-val-input tp-ppw-input" min="1" value={val}
                onChange={(e) => onSet(d, Math.max(1, parseInt(e.target.value, 10) || 1))}
                aria-label={`Periods per week for ${d}-minute classes`} />
              <button type="button" className="tp-val-btn" aria-label={`More ${d}-minute periods`} onClick={() => onSet(d, val + 1)}>+</button>
            </span>
          </div>
        );
      })}
      <p className="tp-ppw-total">= {total} periods a week</p>
    </div>
  );
}
