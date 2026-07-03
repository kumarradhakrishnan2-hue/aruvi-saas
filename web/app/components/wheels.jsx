"use client";
import { useEffect, useRef } from "react";

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

// One gesture demo per page load: whichever RollWheel the teacher meets FIRST rocks a few px
// and settles back, so the box demonstrates its own gesture (words get missed).
let wheelDemoDone = false;

/* RollWheel — a single box, the footprint of one option row, showing exactly ONE item at a
 * time. Rolling (drag / scroll / mouse-wheel / arrow keys) cycles the list through it;
 * scroll-snap settles on a row and whichever item landed in the box IS the pick — no separate
 * confirm tap. items: [{ id, chip?, label }] · value: id string · onChange(id)
 * large: one-notch-bigger label for short lists; longer lists (chapter titles) stay smaller. */
export function RollWheel({ items, value, onChange, ariaLabel, large }) {
  const ref = useRef(null);
  const settleTimer = useRef(null);
  const idBase = String(ariaLabel || "wheel").toLowerCase().replace(/\W+/g, "-");

  // whatever settles in the box becomes the pick
  const onScroll = () => {
    if (settleTimer.current) clearTimeout(settleTimer.current);
    settleTimer.current = setTimeout(() => {
      const el = ref.current;
      if (!el || !items.length) return;
      const idx = Math.min(items.length - 1, Math.max(0, Math.round(el.scrollTop / WHEEL_ROW)));
      if (items[idx]) onChange(String(items[idx].id));
    }, 120);
  };

  // moves exactly one row; shared by the keyboard handler AND the ▲▼ cue buttons below, so
  // tapping a cue behaves identically to pressing an arrow key
  const step = (dir) => {
    const el = ref.current;
    if (!el) return;
    el.scrollBy({ top: dir * WHEEL_ROW, behavior: "smooth" });
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
    if (el && idx >= 0) el.scrollTop = idx * WHEEL_ROW;
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

  const chosen = items.find((it) => String(it.id) === String(value));
  return (
    <div className={`fr-wheel-shell ${large ? "fr-wheel-lg" : ""}`}>
      <div className="fr-wheel" ref={ref} onScroll={onScroll} onKeyDown={onKeyDown}
        role="listbox" tabIndex={0} aria-label={ariaLabel}
        aria-activedescendant={chosen ? `${idBase}-opt-${chosen.id}` : undefined}>
        {items.map((it) => {
          const sel = String(value) === String(it.id);
          return (
            <div key={it.id} id={`${idBase}-opt-${it.id}`}
              className="fr-wheel-row" role="option" aria-selected={sel}>
              {it.chip != null && <span className={`fr-opt-chip ${sel ? "on" : ""}`}>{it.chip}</span>}
              <span className="fr-wheel-label">{it.label}</span>
            </div>
          );
        })}
      </div>
      {/* real step buttons, not decoration — a tap-friendly alternative for anyone who'd
          rather not drag/scroll-wheel the box itself */}
      <span className="fr-wheel-cue">
        <button type="button" className="fr-wheel-cue-btn" onClick={() => step(-1)} aria-label={`Previous ${ariaLabel || "option"}`}>▲</button>
        <button type="button" className="fr-wheel-cue-btn" onClick={() => step(1)} aria-label={`Next ${ariaLabel || "option"}`}>▼</button>
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
 * `initialScrollTo` positions the wheel on mount without that option being pre-picked. */
export function PickWheel({ options, selected, onToggle, labelFor, initialScrollTo, ariaLabel, children }) {
  const wheelRef = useRef(null);
  const step = (dir) => {
    const el = wheelRef.current;
    if (el) el.scrollBy({ top: dir * PICK_ROW, behavior: "smooth" });
  };
  const onKeyDown = (e) => {
    if (e.key === "ArrowDown") { e.preventDefault(); step(1); }
    else if (e.key === "ArrowUp") { e.preventDefault(); step(-1); }
  };
  const showCue = options.length > 4;

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
