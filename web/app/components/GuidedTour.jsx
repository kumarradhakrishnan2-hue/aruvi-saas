"use client";
import { useEffect, useRef, useState } from "react";

/* ───────── GuidedTour — the one-time first-run walk, 13 steps (revised 2026-07-09) ─────────
 * Launched from the "Show me how" nudge on My Classes after the first lesson is generated but not
 * yet attached. Guide-driven: every step has Back · Skip · Next and an "N of 13" counter; Next
 * itself performs the move (nav, opening the preview, the popup, the attach, the profile), with a
 * TRANSPARENT outline hand (SVG, not the filled emoji) showing where the real tap would land.
 * Steps 9–11 demo the completed state without touching her real progress.
 *
 * Step model (1-based; page.jsx owns shell navigation, MyPlans/MyLessonPlans own view state):
 *    1 My Classes tab         — where your classes sit
 *    2 My Lessons tab         — where your generated lesson plans sit
 *    3 the lesson row + hand  — the plan she just generated
 *    4 the open preview       — hand "clicked" the row; the preview is open
 *    5 section card's "+"     — hand on +; Next opens the picker (the app itself now ALWAYS
 *                               routes + through the window — no direct attach)
 *    6 the track-a-chapter popup, hand on the just-generated lesson row — Next attaches it
 *    7 the attached card      — success; Next opens it
 *    8 the tracking view      — box lifted above the notes/mark-complete tail so both stay visible
 *    9 Mark-complete + hand   — demo only, never really clicked
 *   10 completed card's "+"   — card demoed as Complete; box pinned to the viewport bottom so the
 *                               progress rail AND the second section card stay visible
 *   11 the popup again        — pick the next chapter (bound one excluded)
 *   12 the big "+" grow button — add/amend sections, classes or subjects (My Classes home)
 *   13 the settings gear      — where the teaching profile lives; Done closes the tour
 *
 * Anchor extras per step: `handAnchor` (hand on a different element than the ring, e.g. the row
 * inside the popup), `tipAnchor` (tooltip placed off another element — first match in the array
 * wins, e.g. above the teacher-notes block), `scrollAnchor` (what to scroll into view).
 *
 * The tooltip is the SAME thematic sage-pine "window" as the nudge (.dash-nudge) — one visual
 * voice across the whole first-run journey. Sits ABOVE ap-overlay modals (z 70 > 60). */

const fallback = { tag: "your section", chapter: "your lesson" };

// The circled "+" exactly as it appears on the section card (mini .sc-add look).
const Plus = () => <span className="gt-plus" aria-hidden="true">+</span>;

// Transparent outline hand (white, see-through body — NOT the filled emoji): an index-up pointing
// hand silhouette, stroked in ink with a translucent paper fill so the target shows through.
const Hand = () => (
  <svg viewBox="0 0 24 24" width="36" height="36" aria-hidden="true">
    <path
      d="M12 1.5c-1.4 0-2.5 1.1-2.5 2.5v9.2L7.6 11.3c-1-1-2.6-1-3.5 0-1 1-1 2.5 0 3.5l6 6.2c1.3 1.4 3.2 2.2 5.1 2.2h1.3c3.9 0 7-3.1 7-7v-4.2c0-1.4-1.1-2.5-2.5-2.5-.5 0-.9.1-1.3.4-.4-1-1.3-1.6-2.4-1.6-.5 0-1 .2-1.4.4-.4-.9-1.3-1.6-2.4-1.6-.3 0-.7.1-1 .2V4c0-1.4-1.1-2.5-2.5-2.5z"
      fill="rgba(255,255,255,.42)" stroke="#2b2b26" strokeWidth="1.4" strokeLinejoin="round" />
  </svg>
);

const STEPS = [
  { anchor: "nav-classes", place: "below",
    title: "This is where your classes sit.",
    body: () => "On the ‘My Classes’ tab you may always access your sections. Each section points to where you are in the lesson plan with it. Soon we will see how." },
  { anchor: "nav-lessons", place: "below",
    title: "This is where your generated lesson plans sit.",
    body: () => "On the ‘My Lessons’ tab you can access all your generated lesson plans as well as generate new ones." },
  { anchor: "lesson-first", place: "below", hand: true,
    title: "See the lesson plan you just now generated.",
    body: () => "You can filter your lesson plans by subject and class to see them all in one place." },
  // Box LIFTED above the sticky "Attach to a class" bar (lift 130) so the bottom stays visible;
  // the hand sits on the "← back to lesson plans" button the copy points at.
  { anchor: "preview-root", handAnchor: "preview-back", place: "over", lift: 130, hand: true,
    scrollTop: true,
    title: "Let us open the plan to have a quick view.",
    body: (i) => `You may review a lesson plan in its entirety here anytime. Let us go back to My Classes by clicking ‘← back to lesson plans’ now and attach this plan to section ${i.tag}.` },
  { anchor: "section-add", place: "below", hand: true,
    title: "Let us attach a lesson plan to a section.",
    body: (i) => `You want to attach “${i.chapter}” to section ${i.tag}. Click the + sign of that section card.` },
  { anchor: "attach-pop", handAnchor: "attach-pop-row", handPos: "center", place: "over", hand: true,
    title: (i) => `Select a lesson plan to track for Section ${i.tag}.`,
    body: () => "Here is where you select the different lessons to attach to your sections. You can also generate new lessons here." },
  { anchor: "section-card-target", handPos: "center", place: "below", hand: true,
    title: "You are now ready to track.",
    body: (i) => `You have successfully attached “${i.chapter}” for section ${i.tag}. Let us click it to see how tracking works.` },
  // Box hangs just BELOW the first phase, view held at the top — the chapter header, progress
  // bar and phase 1 all stay visible above it.
  { anchor: "lesson-root", place: "below", tipAnchor: ["lesson-phase-1"], scrollTop: true,
    title: "You are now ready to use the plan to teach and track progress.",
    body: () => "The time bound plan gives clear steps, materials used, teacher guidance and assessment items." },
  { anchor: "mark-complete", place: "above", hand: true,
    title: "Track progress.",
    body: (i) => `Track chapter progress of “${i.chapter}” with section ${i.tag} unit by unit. Upon completion of a unit, click this button to mark it complete.` },
  // Box lifted off the bottom edge of the phone screen (lift = 10% of the viewport height) —
  // high enough to clear mobile browser bars, low enough to keep the SECOND section card visible.
  { anchor: "section-add", place: "over", lift: 0.1, hand: true,
    title: "You have completed the chapter and are now ready for the next.",
    body: () => <>Once all units of the chapter are marked complete by you, you are ready to teach another chapter. All you need is to click <Plus />.</> },
  { anchor: "attach-pop", place: "over",
    title: "Select a plan.",
    body: () => "You can use the same window shown in step 6 to select an existing chapter or generate a new plan." },
  { anchor: "grow-add", place: "below", handPos: "center", hand: true,
    title: "Add/amend sections, classes and/or subjects.",
    body: () => "Use this button to quickly add sections, classes or subjects to your teaching profile." },
  { anchor: "settings-gear", place: "below",
    title: "Finally, your teaching profile.",
    body: () => "Your teaching profile is built based on interactions. You may pro-actively build and edit your profile here." },
];
const TOTAL = STEPS.length;

const rectOf = (el) => {
  const r = el.getBoundingClientRect();
  return { top: r.top, left: r.left, width: r.width, height: r.height };
};
const q = (name) => (name ? document.querySelector(`[data-tour="${name}"]`) : null);
const qFirst = (names) => {
  for (const n of [].concat(names || [])) { const el = q(n); if (el) return el; }
  return null;
};

export default function GuidedTour({ step, info, onNext, onBack, onSkip }) {
  const cfg = step >= 1 && step <= TOTAL ? STEPS[step - 1] : null;
  const [rects, setRects] = useState(null);   // { ring, tip, hand } viewport rects
  // Auto-scroll bookkeeping. INSTANT scrolls with a few retries — smooth scrollIntoView proved
  // unreliable here (silently no-oped on some layouts, and mid-scroll screenshots look broken);
  // retries cover targets whose page grows after mount (fonts, async content).
  const scrollRef = useRef({ step: null, tries: 0, last: 0 });

  // Measure the targets on a light poll so the spotlight tracks navigation, scrolls, resizes and
  // targets that mount after the step transition (previews / modals open asynchronously).
  useEffect(() => {
    if (!cfg) { setRects(null); return; }
    let live = true;
    const measure = () => {
      if (!live) return;
      const el = q(cfg.anchor);
      if (!el) { setRects(null); return; }
      const tipEl = cfg.tipAnchor ? (qFirst(cfg.tipAnchor) || el) : el;
      const handEl = cfg.handAnchor ? (qFirst(cfg.handAnchor) || el) : el;
      const scrollEl = cfg.scrollAnchor ? (q(cfg.scrollAnchor) || el) : el;
      // Bring an off-screen target into view (e.g. Mark complete below the fold) — instant,
      // retried a few times per step in case the layout is still settling. cfg.scrollTop pins
      // the view to the very top instead (step 8: header → phase 1 visible).
      const st = scrollRef.current;
      if (st.step !== step) { st.step = step; st.tries = 0; st.last = 0; }
      const now = Date.now();
      if (cfg.scrollTop) {
        // At most TWO pins to the top — never keep snapping back if the teacher then scrolls
        // to read the plan under the box (the repeated snap read as "garbled" on a phone).
        if (window.scrollY > 0 && st.tries < 2 && now - st.last > 400) {
          st.tries += 1; st.last = now;
          window.scrollTo(0, 0);
        }
      } else {
        const sr = scrollEl.getBoundingClientRect();
        if ((sr.top < 0 || sr.bottom > window.innerHeight) && st.tries < 5 && now - st.last > 400) {
          st.tries += 1; st.last = now;
          scrollEl.scrollIntoView({ block: "center" });
        }
      }
      setRects({ ring: rectOf(el), tip: rectOf(tipEl), hand: rectOf(handEl) });
    };
    measure();
    const iv = setInterval(measure, 200);
    window.addEventListener("resize", measure);
    window.addEventListener("scroll", measure, true);
    return () => {
      live = false;
      clearInterval(iv);
      window.removeEventListener("resize", measure);
      window.removeEventListener("scroll", measure, true);
    };
  }, [cfg, step]);

  if (!cfg) return null;
  const i = { ...fallback, ...(info || {}) };

  const PAD = 8;
  const pad = (r) => ({ top: r.top - PAD, left: r.left - PAD, width: r.width + PAD * 2, height: r.height + PAD * 2 });
  const ring = rects ? pad(rects.ring) : null;
  const tipBox = rects ? pad(rects.tip) : null;
  const handBox = rects ? pad(rects.hand) : null;

  // Tooltip placement. "below"/"above" hang off the tip target (clamped to the viewport); "over"
  // pins the box near the bottom of the screen — used when the target IS the whole view or a
  // modal. cfg.lift raises an "over" box off the bottom: a fraction (<1) of the viewport height,
  // or an absolute px value (e.g. above the sticky attach bar).
  const vw = typeof window !== "undefined" ? window.innerWidth : 390;
  const vh = typeof window !== "undefined" ? window.innerHeight : 800;
  const tw = Math.min(vw * 0.88, 330);
  let tipStyle;
  if (cfg.place === "over" || !tipBox) {
    const lift = cfg.lift ? (cfg.lift < 1 ? Math.round(vh * cfg.lift) : cfg.lift) : 18;
    tipStyle = { bottom: lift, left: "50%", transform: "translateX(-50%)" };
  } else {
    const left = Math.min(Math.max(12, tipBox.left), Math.max(12, vw - tw - 12));
    if (cfg.place === "above") {
      tipStyle = { top: tipBox.top - 12, left, transform: "translateY(-100%)" };
    } else {
      // "below" — but CLAMPED to the viewport: if the target's underside is near/past the fold
      // (long chapter titles push phase 1 down on phones), the box settles onto the lower body
      // of the view instead of dropping off-screen.
      const top = Math.min(tipBox.top + tipBox.height + 12, Math.max(80, vh - 260));
      tipStyle = { top, left };
    }
  }

  // The hand — lower-right corner of its target by default; handPos "center" places it in the
  // middle of the target (e.g. centred on a listed lesson row / section card). Viewport-clamped.
  const handStyle = handBox && cfg.hand
    ? (cfg.handPos === "center"
        ? { top: Math.min(handBox.top + handBox.height / 2 - 18, vh - 52),
            left: Math.min(handBox.left + handBox.width / 2 - 18, vw - 46) }
        : { top: Math.min(handBox.top + handBox.height - 16, vh - 52),
            left: Math.min(handBox.left + handBox.width - 24, vw - 46) })
    : null;

  const title = typeof cfg.title === "function" ? cfg.title(i) : cfg.title;

  return (
    <div className="gt-root gt-block">
      {/* Scrim: hit-blocking everywhere (the guide drives every move); the visual dim comes from
          the ring's box-shadow cutout once a target is measured. */}
      <div className="gt-scrim" style={{ background: ring ? "transparent" : "rgba(31,42,36,.42)" }}
        onClick={(e) => e.stopPropagation()} />

      {ring && (
        <div className="gt-ring" style={{ top: ring.top, left: ring.left, width: ring.width, height: ring.height }} />
      )}
      {handStyle && (
        <div className="gt-hand" style={handStyle} aria-hidden="true"><Hand /></div>
      )}

      <div className="gt-tip" style={{ ...tipStyle, width: tw }} role="dialog" aria-label="Getting started">
        <div className="gt-tip-title">{title}</div>
        <div className="gt-tip-body">{cfg.body(i)}</div>
        <div className="gt-tip-foot">
          <span className="gt-count">{step} of {TOTAL}</span>
          <span className="gt-tip-actions">
            <button type="button" className="gt-back" onClick={onBack}>&larr; Back</button>
            <button type="button" className="gt-skip" onClick={onSkip}>Skip</button>
            <button type="button" className="gt-next" onClick={onNext}>
              {step === TOTAL ? "Done ✓" : "Next →"}
            </button>
          </span>
        </div>
      </div>
    </div>
  );
}
