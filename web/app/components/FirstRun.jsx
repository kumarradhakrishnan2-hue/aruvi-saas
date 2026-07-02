"use client";
import { useEffect, useRef, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN } from "../lib/format";

/* ───────── FirstRun — shell-less Guided First Experience (Phase 1, 2026-07-01) ─────────
 * The mobile-first, progressive-acquisition entry point (CLAUDE.md §0). Until the teacher has
 * generated one lesson and attached it to a section, there is NO app shell — no header, no
 * tabs, no sidebar. She just completes one meaningful task. This component owns that whole
 * pre-activation surface and renders full-screen on its own.
 *
 * Principle: benefit first, data second. We ask ONE subject, ONE grade, ONE chapter — the
 * minimum to generate a first lesson — with NCF defaults (40 min / 12 periods) pre-filled and
 * only revealed for editing if the teacher taps "Want to change?". Each answer quietly becomes
 * part of the profile later; she never feels she is "building a profile."
 *
 * Steps: welcome → subject → grade → chapter (+duration) → preview (screen 4, "Lesson plan
 * ready!" — a FACTS TEASER, not the plan itself, PLUS "teach this lesson" + suggested class;
 * screen 5's section picker is a modal over it; generation is a one-way street, no back button)
 * → creatingCards (reward beat) → sectionCards ("My week screen.jpg" — cards + the arrange-week
 * callout together) → arrangeWeek (optional, screen 6's grid) → handoff, at which point page.jsx
 * opens the real workspace shell (sidebar etc. — "side bar.jpg") for the first time. This is the
 * FULL sequence from the mockups (docs/mobile pics/) and the spec
 * (docs/Aruvi_Mobile_First_Progressive_Acquisition_Model_v0.2.md) — "Associate Lesson with
 * Classes" through "Weekly Arrangement". Design: warm-paper system (§4), authored mobile-first.
 *
 * The preview step deliberately does NOT render the full lesson plan (ViewModelView) — a saved
 * plan currently stands in for it, and a REAL generated plan will later live in the exact same
 * saved-plans folder, but either way showing the whole document before she's attached it to a
 * class works against the guided flow. Instead it shows a teaser of common fields (subject,
 * class, chapter title, period count, assessment item count) pulled from that plan's view model.
 *
 * Props:
 *   user        — signed-in id (for the greeting line, optional)
 *   onComplete(payload) — payload = { subjects: [subjectRecord] }, the CANONICAL readiness
 *     shape (same one Readiness.jsx's buildPayload()/onReadyComplete produce) built from
 *     everything the teacher picked: subject, grade, one section-per-fan-out, the weekly grid
 *     (or none, if she skipped arranging). The caller (page.jsx) persists it via POST
 *     /readiness and flips ready+activated — that's the real activation moment, not a flag.
 *   onExit()    — optional: back out to sign-in (from the welcome step)
 */

const DEFAULT_DURATION = 40;   // NCF starting point (minutes per class)
const DEFAULT_PERIODS = 12;    // NCF starting point (teaching periods for the chapter)
// Duration wheel: 20–120 minutes in 5-minute steps. Periods wheel: 1–60 periods, 1 at a time.
const DURATION_CHOICES = Array.from({ length: 21 }, (_, i) => 20 + i * 5); // 20,25,…120
const PERIOD_CHOICES = Array.from({ length: 60 }, (_, i) => i + 1);        // 1,2,…60
const WHEEL_ROW = 64;          // px height of a wheel's single visible row (mobile + desktop, shared with CSS)
// Screens 5/6: same weekday set every other readiness screen uses (Readiness.jsx/MyPlans.jsx
// DAYS). Section letters run the full A–Z range so a school with many parallel sections can
// scroll ("wheel") past the first few and pick any of them — the modal itself scrolls
// (.fr-modal's max-height + overflow:auto), so no separate wheel widget is needed.
const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const SECTION_LETTERS = Array.from({ length: 26 }, (_, i) => String.fromCharCode(65 + i)); // A…Z
// Lesson-card left-edge accent, cycled per card ("My week screen.jpg" uses a different colour
// per section so a multi-section fan-out reads as distinct cards at a glance). Drawn from the
// existing warm-paper palette (§4) rather than introducing new colours.
const SECTION_ACCENTS = ["var(--pine)", "var(--clay)", "var(--ochre)"];

// Teachers say "Class 7", not "Grade VII" — convert the Roman grade slug to its number
// for display (ROMAN starts at "iii" → 3). Falls back to the Roman form if unmapped.
const classNum = (g) => {
  const idx = ROMAN.indexOf(gradeUp(g).toLowerCase());
  return idx >= 0 ? idx + 3 : gradeUp(g);
};

// One gesture demo per page load: whichever wheel the teacher meets FIRST rocks a few px and
// settles back, so the box demonstrates its own gesture (words get missed). Later wheels stay still.
let wheelDemoDone = false;

/* RollWheel — the shared one-row selection box used by the Subject, Grade and Chapter steps.
 * A single box, the footprint of one option row, showing exactly ONE item at a time. Rolling
 * (drag / scroll / mouse-wheel / arrow keys) cycles the list through it; scroll-snap settles
 * on a row and whichever item landed in the box IS the pick — no separate confirm tap.
 * items: [{ id, chip?, label }] · value: id string · onChange(id)
 * large: one-notch-bigger label for short lists (Subject/Class); chapter titles stay smaller. */
function RollWheel({ items, value, onChange, ariaLabel, large }) {
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
  // tapping a cue behaves identically to pressing an arrow key (settle → onChange fires the same way)
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

// Row height for PickWheel's scroll window — 4 rows visible at once (208px / 52px). Independent
// of RollWheel's WHEEL_ROW since this is a free-scrolling multi-select list, not a snap-to-
// center single value.
const PICK_ROW = 52;

/* PickWheel — a reusable fixed-height (exactly 4 rows visible) scrollable multi-select "wheel":
 * drag/swipe through the full option list, or tap the bare ▲▼ arrows beside it to step one row
 * (phones aren't always obviously drag-scrollable). Any visible row toggles on tap, independent
 * of scroll position — no cap on how many can be picked. Shared by SectionPicker (screen 5,
 * letters A–Z) and DurationEditor (screen 6, period lengths) so both look and behave identically
 * — including their Done button, passed in as `children` so it lands in the SAME column as the
 * wheel (its width then always equals the row list's width; the arrows live outside that column
 * entirely, so they never affect it). `initialScrollTo` positions the wheel on mount without
 * that option being pre-picked (e.g. DurationEditor opens scrolled to 40 min either way). */
function PickWheel({ options, selected, onToggle, labelFor, initialScrollTo, ariaLabel, children }) {
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
        // glyphs sitting directly on the modal body, one notch bigger than the wheel cue buttons
        // used elsewhere. Height-matched to the wheel only, not the Done button below it.
        <div className="fr-sec-arrows-side">
          <button type="button" className="fr-sec-arrow-btn" onClick={() => step(-1)} aria-label="Scroll up">▲</button>
          <button type="button" className="fr-sec-arrow-btn" onClick={() => step(1)} aria-label="Scroll down">▼</button>
        </div>
      )}
    </div>
  );
}

/* SectionPicker — the multi-select overlay behind "Change section" (screen 5, picking from the
 * full A–Z letter list, opened from the suggested-class Add/Edit button). `allowEmpty` is kept
 * for callers that don't require a minimum of one. */
function SectionPicker({ letters, selected, tagFor, title, allowEmpty, onDone, onClose }) {
  // Every time this picker opens it starts fully unticked — no section pre-checked, even if
  // some were picked last time — so she always makes a fresh, deliberate choice.
  const [picked, setPicked] = useState([]);
  const toggle = (s) => setPicked((a) => (a.includes(s) ? a.filter((x) => x !== s) : [...a, s].sort()));

  return (
    <div className="fr-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}>
      <div className="fr-modal">
        <h2 className="fr-q">{title || "Select sections"}</h2>
        <p className="fr-hint">
          Choose all the sections you will teach this lesson to.
          {letters.length > 4 ? " Wheel up or down, or use the arrows, for more." : ""}
        </p>
        <PickWheel options={letters} selected={picked} onToggle={toggle} ariaLabel={title || "Select sections"}
          labelFor={(s) => (tagFor ? `Section ${tagFor(s)}` : s)}>
          <button type="button" className="primary fr-cta" disabled={!allowEmpty && picked.length === 0}
            onClick={() => onDone(picked)}>
            Done
          </button>
        </PickWheel>
      </div>
    </div>
  );
}

// Is the viewport at/under the same breakpoint the rest of the shell treats as "mobile"
// (globals.css's .bottom-tabs media query) — drives WeekGrid's row/column transpose below.
// Defaults to mobile (true) before the window is known, matching the app's mobile-first stance.
function useIsMobile(bp) {
  const [isMobile, setIsMobile] = useState(() => (typeof window !== "undefined" ? window.innerWidth <= bp : true));
  useEffect(() => {
    if (typeof window === "undefined") return;
    const mq = window.matchMedia(`(max-width: ${bp}px)`);
    const update = () => setIsMobile(mq.matches);
    update();
    if (mq.addEventListener) mq.addEventListener("change", update); else mq.addListener(update);
    return () => {
      if (mq.removeEventListener) mq.removeEventListener("change", update); else mq.removeListener(update);
    };
  }, [bp]);
  return isMobile;
}

/* DurationEditor — the list of period lengths the weekly grid cycles through (screen 6's
 * "Class duration(s)" Add/Edit). Deliberately the EXACT same window as SectionPicker (same
 * PickWheel, same layout) — just picking minutes instead of letters: tap a row to add/remove
 * it, no separate "add" step. Opens scrolled to the 40-minute default (DURATION_CHOICES runs
 * 20–120 in 5-minute steps either side of it), not to whatever was last picked. At least one
 * duration must stay selected — a grid with zero durations has nothing to cycle through. */
function DurationEditor({ durations, onDone, onClose }) {
  const [list, setList] = useState(durations);
  const toggle = (d) => setList((a) => {
    if (a.includes(d)) return a.length > 1 ? a.filter((x) => x !== d) : a;
    return [...a, d].sort((x, y) => x - y);
  });
  return (
    <div className="fr-modal-bg" onClick={(e) => { if (e.currentTarget === e.target) onClose(); }}>
      <div className="fr-modal">
        <h2 className="fr-q">Class duration{list.length > 1 ? "s" : ""}</h2>
        <PickWheel options={DURATION_CHOICES} selected={list} onToggle={toggle} ariaLabel="Select class durations"
          labelFor={(d) => `${d} min`} initialScrollTo={DEFAULT_DURATION}>
          <button type="button" className="primary fr-cta" onClick={() => onDone(list)}>Done</button>
        </PickWheel>
      </div>
    </div>
  );
}

/* WeekGrid — the weekly scheduling table (screen 6), same tap-to-cycle-durations mechanics as
 * Readiness.jsx's own grid (.wk/.cell), but transposed by viewport: on a phone, days are ROWS
 * and sections are COLUMNS (a short six-row list she scrolls vertically, one glance per day);
 * on desktop it flips to match Readiness's own layout — sections as rows, days as columns. The
 * label column is pinned (position:sticky, see globals.css .fr-wk-scroll) so it stays in view
 * however many section columns scroll past on a narrow phone. */
function WeekGrid({ sections, tagFor, days, grid, durations, isMobile, onTap }) {
  const secLabels = sections.map((s) => tagFor(s));
  const rowLabels = isMobile ? days : secLabels;
  const colLabels = isMobile ? secLabels : days;
  const cornerLabel = isMobile ? "Day" : "Section";

  // Scroll-edge arrows — appear only while there's actually more grid off to that side (e.g.
  // more sections than fit on a phone's width), and hide themselves once she's scrolled all
  // the way to that edge. A tap steps the scroll by roughly one column, same distance either way.
  const scrollRef = useRef(null);
  const [canScrollLeft, setCanScrollLeft] = useState(false);
  const [canScrollRight, setCanScrollRight] = useState(false);
  const checkScroll = () => {
    const el = scrollRef.current;
    if (!el) return;
    setCanScrollLeft(el.scrollLeft > 4);
    setCanScrollRight(el.scrollLeft + el.clientWidth < el.scrollWidth - 4);
  };
  useEffect(() => {
    checkScroll();
    const el = scrollRef.current;
    if (!el) return;
    el.addEventListener("scroll", checkScroll, { passive: true });
    window.addEventListener("resize", checkScroll);
    return () => {
      el.removeEventListener("scroll", checkScroll);
      window.removeEventListener("resize", checkScroll);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sections.length, isMobile]);
  const scrollStep = (dir) => {
    const el = scrollRef.current;
    if (el) el.scrollBy({ left: dir * 130, behavior: "smooth" });
  };

  return (
    <div className="fr-wk-wrap">
      <div className="fr-wk-scroll" ref={scrollRef}>
        <table className="wk fr-wk">
          <thead>
            <tr>
              <th className="rowhd">{cornerLabel}</th>
              {colLabels.map((c) => <th key={c}>{c}</th>)}
            </tr>
          </thead>
          <tbody>
            {rowLabels.map((r, ri) => (
              <tr key={r}>
                <th className="rowhd"><span className="rowtag">{r}</span></th>
                {colLabels.map((c, ci) => {
                  const secIdx = isMobile ? ci : ri;
                  const dayIdx = isMobile ? ri : ci;
                  const v = grid[secIdx] ? grid[secIdx][dayIdx] : -1;
                  return (
                    <td key={c}>
                      <div className={`cell ${v >= 0 ? "on" : ""}`} data-sec={v >= 0 ? secIdx % 4 : undefined}
                        onClick={() => onTap(secIdx, dayIdx)}>
                        {v >= 0 ? durations[v] : ""}
                      </div>
                    </td>
                  );
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
      {canScrollLeft && (
        <button type="button" className="fr-wk-arrow fr-wk-arrow-l" onClick={() => scrollStep(-1)} aria-label="Scroll to earlier sections">‹</button>
      )}
      {canScrollRight && (
        <button type="button" className="fr-wk-arrow fr-wk-arrow-r" onClick={() => scrollStep(1)} aria-label="Scroll to more sections">›</button>
      )}
    </div>
  );
}

/* DateBadge — a small torn-calendar-page icon (ring holes + month + day) showing TODAY'S real
 * date, computed live rather than relying on an emoji glyph (some platforms' 📅 emoji happens
 * to render the current date, most don't — this is the reliable version). Used on the
 * arrange-week callout below. */
function DateBadge() {
  const now = new Date();
  const month = now.toLocaleDateString("en-US", { month: "short" }).toUpperCase();
  const day = now.getDate();
  return (
    <div className="fr-datebadge" aria-hidden="true">
      <span className="fr-datebadge-rings"><span /><span /><span /></span>
      <span className="fr-datebadge-month">{month}</span>
      <span className="fr-datebadge-day">{day}</span>
    </div>
  );
}

/* BenefitIcon — hand-drawn single-stroke line glyphs (not stock emoji) for the arrange-week
 * callout's benefit row, so the pitch reads in the same "scholarly planner" register as the
 * rest of the app rather than clashing with default colourful emoji. Each sits in a small
 * outlined circle cycling through the app's three accents (pine/clay/ochre), mirroring the
 * .fr-sc-chip badge language used on the lesson cards above. */
const BENEFIT_PATHS = {
  // funnel — narrowing down to what matters (less clutter)
  clutter: <path d="M4.5 5h15l-5.5 6.2v5.3l-4 1.8v-7.1L4.5 5z" />,
  // simple clock face — save time
  time: <><circle cx="12" cy="12" r="7.7" /><path d="M12 7.8V12l3 2.1" /></>,
  // per-row checkmarks — track each section individually
  track: <><path d="M9.3 6.5h9.2M9.3 12h9.2M9.3 17.5h9.2" /><path d="M4.3 6.5l1.1 1.1 2-2.2M4.3 12l1.1 1.1 2-2.2M4.3 17.5l1.1 1.1 2-2.2" /></>,
};

function BenefitIcon({ kind, accent }) {
  return (
    <span className="fr-benefit-badge" style={{ "--sc-accent": accent }} aria-hidden="true">
      <svg viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round">
        {BENEFIT_PATHS[kind]}
      </svg>
    </span>
  );
}

/* LessonCard — one independent card per fan-out section ("My week screen.jpg"): coloured
 * left stripe, section-tag chip, subject kicker, chapter title, "Chapter N · Learning Unit 1"
 * meta line, "Ready to teach" pill. This is the reward payoff shown right after the
 * creatingCards beat — same visual language My Plans will eventually use for the real cards. */
function LessonCard({ tag, subjectName, chapterTitle, chapterNumber, accent }) {
  return (
    <div className="fr-sc-card" style={{ "--sc-accent": accent }}>
      <div className="fr-sc-chip">{tag}</div>
      <div className="fr-sc-body">
        <span className="fr-sc-kicker">{subjectName}</span>
        <div className="fr-sc-title">{chapterTitle || "—"}</div>
        <div className="fr-sc-meta">{chapterNumber ? `Chapter ${chapterNumber} · Learning Unit 1` : "Learning Unit 1"}</div>
        <span className="fr-sc-ready">Ready to teach</span>
      </div>
    </div>
  );
}

export default function FirstRun({ user, onComplete, onExit, onSignOut }) {
  const [step, setStep] = useState("welcome");
  // welcome | subject | grade | chapter | preview | creatingCards | sectionCards | arrangeWeek

  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");   // slug

  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");       // slug

  const [chapters, setChapters] = useState([]);
  const [chapterNo, setChapterNo] = useState(""); // chapter_number as string

  const [durationMin, setDurationMin] = useState(DEFAULT_DURATION);
  const [periods, setPeriods] = useState(DEFAULT_PERIODS);
  // Estimated periods' recommendation is chapter-specific (NCF period-norms × effort index),
  // so it's tracked separately from the live `periods` value — the "NCF recommended" tag
  // compares the CURRENT value against this, live, on every wheel move: land back on the
  // recommended number and the tag reappears, move off it and the tag drops. Duration's
  // recommendation is the flat DEFAULT_DURATION constant, so no extra state is needed there.
  const [defaultPeriods, setDefaultPeriods] = useState(DEFAULT_PERIODS);
  // Both fields sit grey/read-only showing their default until "Change" is pressed, which
  // opens that field's wheel picker (the other field's wheel, if open, closes — only one
  // edit box open at a time).
  const [editingField, setEditingField] = useState(null); // null | "duration" | "periods"

  // Screens 4-6: section fan-out + weekly arrangement. `sections` is the letters she's teaching
  // this lesson to (default one, "A", matching the mockup's default "VI A" before she changes
  // it).
  const [sections, setSections] = useState(["A"]);
  const [sectionPickerOpen, setSectionPickerOpen] = useState(false);
  // weekGrid[secIdx][dayIdx] = index into durationOptions, or -1 for "no class". Same shape
  // Readiness.jsx's own weekly grid uses, so the canonical payload built below needs no
  // reshaping. Kept in sync with `sections` by the effect right below.
  const [weekGrid, setWeekGrid] = useState(() => sections.map(() => DAYS.map(() => -1)));
  useEffect(() => {
    setWeekGrid((prev) => sections.map((_, i) => (prev && prev[i]) || DAYS.map(() => -1)));
  }, [sections]);
  // Most teachers have one period length; this stays null until she opens the duration editor
  // on screen 6, at which point it becomes the real list a grid tap cycles through. Until then
  // the grid just uses her single already-chosen `durationMin` (from the chapter step).
  const [durationOptions, setDurationOptions] = useState(null);
  const [durationEditorOpen, setDurationEditorOpen] = useState(false);
  const [activating, setActivating] = useState(false);      // busy state for the final handoff

  // Preview step — live generation is deferred, so "Generate Lesson Plan" pulls the closest
  // matching SAVED plan for this subject·grade·chapter and reads its view model for the teaser
  // facts (periods, assessment items) — see the "preview" step below, not the full document.
  const [previewBusy, setPreviewBusy] = useState(false);
  const [previewView, setPreviewView] = useState(null);
  const [previewNote, setPreviewNote] = useState("");
  const [previewError, setPreviewError] = useState("");

  // Load the subject catalogue once (used on the subject step).
  useEffect(() => {
    getJSON("/subjects").then((d) => setSubjects(d.subjects || [])).catch(() => setSubjects([]));
  }, []);

  // Stepping away from the chapter step and back (← Change class, ← Back to chapter, etc.)
  // should never re-open a duration/periods wheel the teacher left open — every fresh arrival
  // on the chapter step starts with both boxes closed.
  useEffect(() => {
    if (step === "chapter") setEditingField(null);
  }, [step]);

  // Grades for the chosen subject.
  useEffect(() => {
    if (!subject) { setGrades([]); return; }
    getJSON(`/subjects/${subject}/grades`).then((d) => {
      const gs = [...(d.grades || [])].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGrades(gs);
    }).catch(() => setGrades([]));
  }, [subject]);

  // Chapters for the chosen subject·grade.
  useEffect(() => {
    if (!subject || !grade) { setChapters([]); return; }
    getJSON(`/subjects/${subject}/${grade}/chapters`).then((d) => {
      setChapters(d.chapters || []);
    }).catch(() => setChapters([]));
  }, [subject, grade]);

  // Estimated teaching periods for the chosen chapter — sourced from the NCF period-norms
  // table (data/content/allocation_norms/ncf_period_norms.json), distributed across this
  // grade's chapters by effort index (api's /chapters endpoint does the maths, same allocator
  // Allocate.jsx uses). Falls back to the flat NCF_DEFAULT_PERIODS placeholder only when the
  // norm table has no figure for this subject·stage (e.g. Science·preparatory).
  useEffect(() => {
    const c = chapters.find((x) => String(x.chapter_number) === String(chapterNo));
    if (!c) return;
    const rec = c.ncf_estimated_periods != null ? Math.round(c.ncf_estimated_periods) : DEFAULT_PERIODS;
    setDefaultPeriods(rec);
    setPeriods(rec);
    setEditingField((f) => (f === "periods" ? null : f)); // close a stale edit box, if open
  }, [chapterNo, chapters]);

  const chosenChapter = chapters.find((c) => String(c.chapter_number) === String(chapterNo));

  // Section tag matches the app-wide convention (MyClasses.jsx / Readiness.jsx): arabic grade
  // number + letter, e.g. "6A" — displayed everywhere else as "Section 6A".
  const tagFor = (letter) => `${classNum(grade)}${letter}`;

  // The grid's active duration list — her single chapter-step duration until she opens the
  // screen-6 editor and turns it into a real (possibly multi-value) list.
  const durOptions = durationOptions && durationOptions.length ? durationOptions : [durationMin];
  const isMobile = useIsMobile(720); // WeekGrid's row/column transpose (screen 6)

  // Tap a weekly-grid cell: cycles empty → duration[0] → duration[1] → … → empty, exactly like
  // Readiness.jsx's own grid (`tapCell`) — a single duration just toggles on/off.
  const tapWeekCell = (secIdx, dayIdx) => {
    setWeekGrid((prev) => {
      const next = prev.map((row) => [...row]);
      if (!next[secIdx]) return prev;
      const v = next[secIdx][dayIdx];
      const n = durOptions.length;
      next[secIdx][dayIdx] = v < 0 ? 0 : (v + 1 >= n ? -1 : v + 1);
      return next;
    });
  };

  // Screen 4→6 handoff: build the CANONICAL readiness payload from everything picked across
  // the whole flow. One subject record, one grade, one section per fan-out choice, a weekly
  // grid if she arranged one (all -1 / "no schedule" if she didn't — My Plans already has a
  // graceful fallback for that, per its own doc comment).
  const buildActivationPayload = () => {
    const secObjs = sections.map((s) => ({ tag: tagFor(s), sec: s }));
    const grid = sections.map((_, secIdx) =>
      DAYS.map((_, dayIdx) => (weekGrid[secIdx] ? weekGrid[secIdx][dayIdx] : -1))
    );
    const subjectRecord = {
      name: pretty(subject),
      grades: [{
        grade: gradeUp(grade),
        sections: secObjs,
        durations: durOptions,
      }],
      grids: [grid],
      budget: {},
    };
    return { subjects: [subjectRecord] };
  };

  // "Add to Class" (screen 4) fires this: hold on a short "Section Cards are being created…"
  // beat (screen "creatingCards") so the moment reads as something being built for her, THEN
  // land on "sectionCards" — her actual reward payoff ("My week screen.jpg": the lesson cards
  // + the arrange-week callout together). The delay belongs HERE, right when the cards are
  // created — not at the very end of the flow, so it lands as immediate gratification rather
  // than a hold-up before she's allowed to finish.
  const goCreateCards = () => {
    setStep("creatingCards");
    setTimeout(() => setStep("sectionCards"), 1800);
  };

  // Fires from "Maybe later" (on sectionCards or arrangeWeek) or "Set up my week" — the reward
  // beat already happened at goCreateCards, so this just finalizes: hand the canonical
  // readiness payload to onComplete. Persistence itself (POST /readiness) is page.jsx's job,
  // same as the old upfront Readiness wizard did.
  const finishActivation = () => {
    setActivating(true);
    onComplete && onComplete(buildActivationPayload());
  };

  // "Generate Lesson Plan" — live generation is deferred (see api/main.py's /generate stub),
  // so we pull a SAVED plan's real facts (periods, assessment item count) for the teaser
  // summary, same pattern Allocate.jsx's G7 spoke uses to serve saved-plan previews. We no
  // longer render the plan itself here — see screen 4a "preview" below: showing the full
  // document before she's attached it to a class got in the way of the guided flow, and a
  // REAL generated plan will live in this same saved-plans folder later, so this fetch already
  // works unchanged once live generation lands. Try the exact chosen chapter first; if this
  // subject·grade has no saved plan for it yet, fall back to whichever saved plan IS available
  // so testing isn't blocked (the disclosure note below stays honest about that substitution).
  const generate = async () => {
    if (!chosenChapter) return;
    setStep("preview");
    setPreviewBusy(true);
    setPreviewError("");
    setPreviewNote("");
    setPreviewView(null);
    try {
      const plansRes = await getJSON(`/plans/${subject}/${grade}`);
      const plans = plansRes.plans || [];
      let match = plans.find((p) => String(p.chapter_number) === String(chapterNo));
      if (!match && plans.length) {
        match = plans[0];
        setPreviewNote(
          `No saved test plan for Chapter ${chapterNo} yet — showing Chapter ${match.chapter_number} (${match.chapter_title}) as a stand-in preview.`
        );
      }
      if (!match) {
        setPreviewError(`No saved test plans available yet for ${pretty(subject)} · Class ${classNum(grade)}.`);
        return;
      }
      const viewRes = await getJSON(`/plans/${subject}/${grade}/${match.filename}/view`);
      setPreviewView(viewRes.view);
    } catch (e) {
      setPreviewError("Couldn't load a saved plan right now. Try again in a moment.");
    } finally {
      setPreviewBusy(false);
    }
  };

  /* ── shared: three-step progress rail (Subject · Grade · Chapter) ── */
  const Progress = ({ active }) => {
    const steps = ["Subject", "Class", "Chapter"];
    const idx = steps.indexOf(active);
    return (
      <ol className="fr-prog" aria-label="Setup progress">
        {steps.map((label, i) => (
          <li key={label} className={`fr-prog-step ${i < idx ? "done" : ""} ${i === idx ? "current" : ""}`}>
            <span className="fr-prog-dot">{i < idx ? "✓" : i + 1}</span>
            <span className="fr-prog-label">{label}</span>
          </li>
        ))}
      </ol>
    );
  };

  const Brand = () => (
    <div className="fr-brand">
      {user && (
        <div className="fr-user">
          <span className="fr-user-name">{user}</span>
          {onSignOut && <button className="fr-user-logout" onClick={onSignOut}>Log out</button>}
        </div>
      )}
      <span className="brand-row">Aruvi<em>.</em></span>
      <span className="fr-brand-tag">lesson studio</span>
    </div>
  );

  /* ── WELCOME ── */
  if (step === "welcome") {
    return (
      <div className="fr-wrap fr-welcome">
        <Brand />
        <div className="fr-welcome-body">
          <h1 className="fr-welcome-title">Welcome to Aruvi</h1>
          <p className="fr-welcome-sub">
            We help you teach engaging, NCF-aligned lessons while saving you time.
          </p>
          <ul className="fr-pain-list">
            <li><span className="fr-pain-tick">✓</span><span>Lesson plan in minutes, not hours</span></li>
            <li><span className="fr-pain-tick">✓</span><span>NCF / NCERT aligned</span></li>
            <li><span className="fr-pain-tick">✓</span><span>Assessment built in</span></li>
            <li><span className="fr-pain-tick">✓</span><span>Every section's status at one glance</span></li>
          </ul>
          <h2 className="fr-welcome-h2">Let’s get started</h2>
          <p className="fr-welcome-sub">
            Answer three quick questions and Aruvi will create your first lesson plan.
          </p>
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" onClick={() => setStep("subject")}>Prepare my first lesson →</button>
          <p className="fr-secure">🛡 Your data is private and secure</p>
        </div>
      </div>
    );
  }

  /* ── STEP 1 · SUBJECT ── */
  if (step === "subject") {
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress active="Subject" />
        <div className="fr-step-body">
          <h1 className="fr-q">What would you like to teach?</h1>
          <p className="fr-hint">Let’s start with one subject. Roll the box or use the arrows — the subject shown is your pick.</p>
          {subjects.length === 0 && <div className="fr-loading">Loading subjects…</div>}
          {subjects.length > 0 && (
            <RollWheel ariaLabel="Subject" value={subject} onChange={setSubject} large
              items={subjects.map((s) => ({ id: s, chip: pretty(s).charAt(0), label: pretty(s) }))} />
          )}
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={!subject} onClick={() => setStep("grade")}>Continue</button>
          <button className="fr-link" onClick={() => setStep("welcome")}>← Back</button>
        </div>
      </div>
    );
  }

  /* ── STEP 2 · GRADE ── */
  if (step === "grade") {
    return (
      <div className="fr-wrap">
        <Brand />
        <Progress active="Class" />
        <div className="fr-step-body">
          <h1 className="fr-q">Which class do you want to teach {pretty(subject)} to?</h1>
          <p className="fr-hint">You can add more classes later. Roll the box or use the arrows — the class shown is your pick.</p>
          {grades.length === 0 && <div className="fr-loading">Loading classes…</div>}
          {grades.length > 0 && (
            <RollWheel ariaLabel="Class" value={grade} onChange={setGrade} large
              items={grades.map((g) => ({ id: g, chip: classNum(g), label: `Class ${classNum(g)}` }))} />
          )}
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={!grade} onClick={() => setStep("chapter")}>Continue</button>
          <button className="fr-link" onClick={() => setStep("subject")}>← Change subject</button>
        </div>
      </div>
    );
  }

  /* ── STEP 4 · LESSON PLAN READY — facts teaser + "teach this lesson" + suggested class, all
   * one screen (mockup: "Lesson generated" screen 1). Generation is a one-way street from here
   * — no back-to-chapter escape hatch; the only way forward is "Create teaching cards". Screen
   * 5's section picker is the modal at the bottom, opened from the suggested-class Add/Edit. ── */
  if (step === "preview") {
    const assessmentCount = previewView
      ? (previewView.assessment?.groups || []).reduce((sum, g) => sum + (g.items ? g.items.length : 0), 0)
      : null;
    return (
      <div className="fr-wrap">
        <Brand />
        <div className="fr-step-body">
          {previewBusy && <div className="fr-loading">Building your lesson plan…</div>}
          {!previewBusy && previewError && <div className="empty">{previewError}</div>}
          {!previewBusy && !previewError && previewView && (
            <>
              <div className="fr-plan-ready">
                <span className="fr-plan-ready-check" aria-hidden="true">✓</span>
                <h1 className="fr-plan-ready-title">Lesson plan ready!</h1>
                <p className="fr-plan-ready-sub">Your lesson has been generated successfully.</p>
              </div>

              <div className="fr-teaser-card">
                <h2 className="fr-teaser-title">{chosenChapter ? chosenChapter.chapter_title : previewView.lesson_plan.chapter_title}</h2>
                <p className="fr-teaser-sub">{pretty(subject)} · Class {classNum(grade)}</p>
                <div className="fr-teaser-stats">
                  <div className="fr-teaser-stat">
                    <span className="fr-teaser-stat-num">{previewView.lesson_plan.total_periods}</span>
                    <span className="fr-teaser-stat-label">periods</span>
                  </div>
                  <div className="fr-teaser-stat">
                    <span className="fr-teaser-stat-num">{assessmentCount}</span>
                    <span className="fr-teaser-stat-label">assessment items</span>
                  </div>
                </div>
              </div>

              <h2 className="fr-teach-heading">Teach this lesson to your class</h2>
              <p className="fr-hint">We'll create one teaching card for each class so each can progress independently.</p>

              <span className="fr-default-kicker">{sections.length > 1 ? "Classes" : "Class"}</span>
              <div className="fr-suggested-class fr-suggested-class-tap" onClick={() => setSectionPickerOpen(true)}>
                <span className={`fr-default-val ${sections.length > 2 ? "fr-default-val-compact" : ""}`}>
                  {sections.length ? sections.map((s) => tagFor(s)).join(", ") : "—"}
                </span>
                <button type="button" className="fr-change-btn fr-change-btn-primary"
                  onClick={(e) => { e.stopPropagation(); setSectionPickerOpen(true); }}>
                  Add/Edit
                </button>
              </div>
            </>
          )}
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={previewBusy || !sections.length} onClick={goCreateCards}>
            Create teaching cards →
          </button>
          <p className="fr-secure">You can change this anytime.</p>
        </div>
        {sectionPickerOpen && (
          <SectionPicker letters={SECTION_LETTERS} selected={sections} tagFor={tagFor}
            onDone={(picked) => { setSections(picked); setSectionPickerOpen(false); }}
            onClose={() => setSectionPickerOpen(false)} />
        )}
      </div>
    );
  }

  /* ── STEP · CREATING CARDS (the reward beat — a few seconds, then sectionCards) ── */
  if (step === "creatingCards") {
    return (
      <div className="fr-wrap fr-celebrate">
        <Brand />
        <div className="fr-celebrate-body">
          <span className="fr-celebrate-spin" aria-hidden="true" />
          <h1 className="fr-celebrate-title">Section Cards are being created…</h1>
          <p className="fr-hint">Just a moment while Aruvi sets up your class.</p>
        </div>
      </div>
    );
  }

  /* ── STEP · SECTION CARDS + arrange-week callout together ("My week screen.jpg") ── */
  if (step === "sectionCards") {
    return (
      <div className="fr-wrap">
        <Brand />
        <div className="fr-step-body">
          <div className="fr-ready-note">
            <span className="fr-ready-check">✓</span>
            <div className="fr-ready-text">
              <strong>Lesson added to {sections.length} section{sections.length === 1 ? "" : "s"}.</strong>
              <span>Independent lesson cards created.</span>
            </div>
          </div>

          <h2 className="fr-sc-heading">Your lesson cards</h2>
          <p className="fr-hint">Each section has its own lesson plan.</p>
          <div className="fr-sc-list">
            {sections.map((s, i) => (
              <LessonCard key={s} tag={tagFor(s)} subjectName={pretty(subject)}
                chapterTitle={chosenChapter ? chosenChapter.chapter_title : ""}
                chapterNumber={chosenChapter ? chosenChapter.chapter_number : ""}
                accent={SECTION_ACCENTS[i % SECTION_ACCENTS.length]} />
            ))}
          </div>

          <div className="fr-arrange-callout">
            <div className="fr-arrange-top">
              <DateBadge />
              <div className="fr-arrange-text">
                <strong>Open Aruvi each morning and see <span className="fr-arrange-accent">only today's classes</span>.</strong>
                <p>Tell Aruvi which days you teach each class, and we'll keep your home screen focused on what's relevant today.</p>
              </div>
            </div>
            <div className="fr-benefit-row">
              <div className="fr-benefit"><BenefitIcon kind="clutter" accent="var(--pine)" />Less clutter</div>
              <div className="fr-benefit"><BenefitIcon kind="time" accent="var(--clay)" />Save time</div>
              <div className="fr-benefit"><BenefitIcon kind="track" accent="var(--ochre)" />Track section</div>
            </div>
          </div>
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={activating} onClick={() => setStep("arrangeWeek")}>
            Set up my week →
          </button>
          <button className="fr-link fr-center" disabled={activating} onClick={finishActivation}>Maybe later</button>
        </div>
      </div>
    );
  }

  /* ── STEP 6 · ARRANGE-WEEK GRID (mockup screen 6) — same tap-to-cycle grid as the Readiness
   * setup wizard, transposed by viewport (days=rows/sections=columns on mobile; sections=rows/
   * days=columns on desktop, matching Readiness.jsx). A duration Add/Edit box sits above it —
   * most teachers leave it at the one chapter-step duration; adding a second (or third) one
   * makes each grid tap cycle through them instead of a plain on/off. ── */
  if (step === "arrangeWeek") {
    const durLabel = durOptions.map((d) => `${d} min`).join(", ");
    return (
      <div className="fr-wrap">
        <Brand />
        <div className="fr-step-body">
          <h1 className="fr-q">Arrange your week</h1>
          <p className="fr-hint">
            {durOptions.length > 1
              ? "Tap a cell to mark a class. Tap again to cycle through your durations, and once more to clear it."
              : "Tap a cell to mark a class. Tap again to clear it."}
          </p>

          <span className="fr-default-kicker">Class duration{durOptions.length > 1 ? "s" : ""}</span>
          <p className="fr-hint">
            Tell us how long your {pretty(subject)} periods are for Class {classNum(grade)}. This
            helps Aruvi generate lesson plans that match your classroom.
          </p>
          <div className="fr-suggested-class fr-suggested-class-tap" onClick={() => setDurationEditorOpen(true)}>
            <span className="fr-default-val">{durLabel}</span>
            <button type="button" className="fr-change-btn fr-change-btn-primary"
              onClick={(e) => { e.stopPropagation(); setDurationEditorOpen(true); }}>
              Add/Edit
            </button>
          </div>

          <WeekGrid sections={sections} tagFor={tagFor} days={DAYS} grid={weekGrid}
            durations={durOptions} isMobile={isMobile} onTap={tapWeekCell} />
        </div>
        <div className="fr-foot">
          <button className="primary fr-cta" disabled={activating} onClick={finishActivation}>
            {activating ? "Setting up…" : "Set up my week"}
          </button>
          <button className="fr-link" disabled={activating} onClick={finishActivation}>Maybe later</button>
        </div>
        {durationEditorOpen && (
          <DurationEditor durations={durOptions}
            onDone={(list) => { setDurationOptions(list); setDurationEditorOpen(false); }}
            onClose={() => setDurationEditorOpen(false)} />
        )}
      </div>
    );
  }

  /* ── STEP 3 · CHAPTER (+ NCF default duration/periods) ── */
  return (
    <div className="fr-wrap">
      <Brand />
      <Progress active="Chapter" />
      <div className="fr-step-body">
        <h1 className="fr-q">Choose the chapter to teach</h1>
        <p className="fr-hint">Roll the box or use arrows to pick one chapter.</p>

        {chapters.length === 0 && <div className="fr-loading">Loading chapters…</div>}
        {chapters.length > 0 && (
          <RollWheel ariaLabel="Chapter" value={chapterNo} onChange={setChapterNo}
            items={chapters.map((c) => ({ id: String(c.chapter_number), chip: c.chapter_number, label: c.chapter_title }))} />
        )}

        <div className="fr-defaults">
          <div className={`fr-default ${editingField === "duration" ? "fr-default-editing" : ""}`}>
            <span className="fr-default-kicker-row">
              <span className="fr-default-kicker">Class duration</span>
              {durationMin === DEFAULT_DURATION && <span className="fr-tag-recommended">NCF recommended</span>}
            </span>
            {editingField !== "duration" ? (
              <div className="fr-default-row">
                <span className="fr-default-val fr-default-val-muted">{durationMin}-minute classes</span>
                <button type="button" className="fr-change-btn" onClick={() => setEditingField("duration")}>
                  Change
                </button>
              </div>
            ) : (
              <div className="fr-default-wheel-wrap">
                <RollWheel ariaLabel="Class duration" value={String(durationMin)}
                  onChange={(v) => setDurationMin(Number(v))}
                  items={DURATION_CHOICES.map((m) => ({ id: String(m), chip: m, label: "minute classes" }))} />
                <button type="button" className="fr-done-btn" onClick={() => setEditingField(null)}>Done</button>
              </div>
            )}
          </div>
          <div className={`fr-default ${editingField === "periods" ? "fr-default-editing" : ""}`}>
            <span className="fr-default-kicker-row">
              <span className="fr-default-kicker">Estimated periods</span>
              {periods === defaultPeriods && <span className="fr-tag-recommended">NCF recommended</span>}
            </span>
            {editingField !== "periods" ? (
              <div className="fr-default-row">
                <span className="fr-default-val fr-default-val-muted">{periods} periods</span>
                <button type="button" className="fr-change-btn" onClick={() => setEditingField("periods")}>
                  Change
                </button>
              </div>
            ) : (
              <div className="fr-default-wheel-wrap">
                <RollWheel ariaLabel="Estimated periods" value={String(periods)}
                  onChange={(v) => setPeriods(Number(v))}
                  items={PERIOD_CHOICES.map((p) => ({ id: String(p), chip: p, label: p === 1 ? "period" : "periods" }))} />
                <button type="button" className="fr-done-btn" onClick={() => setEditingField(null)}>Done</button>
              </div>
            )}
          </div>
        </div>
      </div>
      <div className="fr-foot">
        <button className="primary fr-cta" disabled={!chosenChapter} onClick={generate}>Generate Lesson Plan</button>
        <button className="fr-link" onClick={() => setStep("grade")}>← Change class</button>
      </div>
    </div>
  );
}
