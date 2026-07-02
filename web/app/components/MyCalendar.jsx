"use client";
import { useState, useMemo, useEffect } from "react";

/* ───────── MyCalendar — read-only weekly timetable (2026-06-28, transposed 2026-07-02) ─────────
 * The teacher's whole week at a glance — Grade·Section (e.g. "6A") crossed with the six weekdays.
 * Each filled cell is the class that section meets that day, showing the subject name and the
 * period duration. View-only: editing the schedule lives in My Class → Section day grids.
 *
 * ORIENTATION is responsive (matches FirstRun's screen-6 WeekGrid): on a phone, days are ROWS
 * and Grade·Sections are COLUMNS (a short six-row list scrolls better than sideways-scrolling
 * every day at once); on desktop it's the reverse — sections as rows, days as columns.
 *
 * Built straight off the canonical readiness profile (readiness.subjects[]) — the same shape
 * MyClasses edits:
 *   subjects[] → { name, grades[]→{grade, sections[]→{tag,sec}}, durations[], grids }
 *     grids[gradeIdx][secIdx][dayIdx] = durationIndex | -1
 * Because one teacher teaches each section, at most one subject meets a given Grade·Section on a
 * given day, so every cell holds a single class (no stacking needed).
 *
 * COLOUR (rules tightened 2026-07-02): each subject gets a colour FAMILY (auto-assigned in
 * encounter order from a fixed palette). Within a family, grades are normally shaded
 * darkest→lightest by grade order (higher grade = darker), and sections within a grade share
 * its shade. The one exception: with a SINGLE subject and a SINGLE grade, there's nothing left
 * to tell sections apart by, so sections instead each get their own hue from the palette rather
 * than shades of one. Computed inline as CSS custom properties so the stylesheet stays generic.
 *
 * Props: readiness — the projection from page.jsx (carries .subjects[] canonical).
 */

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const ROMANS = { III: 3, IV: 4, V: 5, VI: 6, VII: 7, VIII: 8, IX: 9, X: 10 };
const gradeNum = (g) => ROMANS[g] || (parseInt(g, 10) || 0);

// Colour families (hue anchors). Each subject takes the next one; grades shade within it.
const FAMILIES = [
  { name: "green",  h: 152, s: 42 },
  { name: "blue",   h: 214, s: 38 },
  { name: "ochre",  h: 38,  s: 52 },
  { name: "plum",   h: 286, s: 30 },
  { name: "clay",   h: 14,  s: 48 },
  { name: "teal",   h: 184, s: 38 },
];

// shade a family by position among its grades: 0 = darkest, last = lightest.
// returns { bg, ink } — a fill and a readable text colour for that fill.
function shade(fam, idx, total) {
  const steps = Math.max(1, total - 1);
  const t = total <= 1 ? 0 : idx / steps;          // 0..1 darkest→lightest
  const L = 30 + t * 34;                            // lightness 30%→64%
  const bg = `hsl(${fam.h} ${fam.s}% ${L}%)`;
  const ink = L < 52 ? "#fbf8f1" : "#23201a";       // white ink on dark fills, near-black on light
  return { bg, ink };
}

// A single fixed-lightness fill for a family — used where SECTIONS need to read as genuinely
// different colours (not lighter/darker cousins of one hue), which only happens in the one-
// subject-one-grade case below (there's nothing else left in view to tell sections apart by).
function familyColor(fam) {
  const L = 44;
  const bg = `hsl(${fam.h} ${fam.s}% ${L}%)`;
  const ink = L < 52 ? "#fbf8f1" : "#23201a";
  return { bg, ink };
}

const tagOf = (g, sec) => sec.tag || `${gradeNum(g.grade)}${sec.sec || ""}`;

// Flatten readiness into: rows (one per Grade·Section) + a colour map. Colour rules (2026-07-02):
//   • one subject, one grade   → each SECTION gets its own hue (nothing else to tell them apart by).
//   • one subject, many grades → grades shade the subject's one hue (higher grade = darker);
//     sections within a grade share their grade's shade.
//   • many subjects            → each subject gets its own hue; grades within it shade that hue
//     (higher grade = darker); sections within a grade share their grade's shade.
function buildModel(subjects) {
  const singleSubject = subjects.length === 1;
  const singleGrade = singleSubject && (subjects[0].grades || []).length === 1;

  // 1) assign colour(s) per subject — keyed by grade normally, or by section in the
  //    single-subject-single-grade special case (see rules above).
  const colorOf = {};            // `${subject}__${grade}` (or `…__${sectionTag}`) -> {bg, ink}
  const legend = [];             // [{ subject, grades:[{grade, bg, ink}] }] — feeds filter chips/totals
  subjects.forEach((s, si) => {
    const fam = FAMILIES[si % FAMILIES.length];
    const entry = { subject: s.name, grades: [] };

    if (singleGrade) {
      const g = s.grades[0];
      const secsSorted = [...(g.sections || [])].sort((a, b) => tagOf(g, a).localeCompare(tagOf(g, b)));
      secsSorted.forEach((sec, idx) => {
        colorOf[`${s.name}__${g.grade}__${tagOf(g, sec)}`] = familyColor(FAMILIES[idx % FAMILIES.length]);
      });
      const rep = secsSorted.length ? colorOf[`${s.name}__${g.grade}__${tagOf(g, secsSorted[0])}`] : familyColor(fam);
      entry.grades.push({ grade: g.grade, ...rep });
    } else {
      const gsorted = [...(s.grades || [])].sort((a, b) => gradeNum(a.grade) - gradeNum(b.grade));
      // darkest = HIGHEST grade (e.g. "darker green for 6A, lighter for 5B") → reverse for idx
      const order = [...gsorted].sort((a, b) => gradeNum(b.grade) - gradeNum(a.grade));
      order.forEach((g, idx) => {
        const sh = shade(fam, idx, order.length);
        colorOf[`${s.name}__${g.grade}`] = sh;
        entry.grades.push({ grade: g.grade, ...sh });
      });
    }
    legend.push(entry);
  });

  // 2) collect every Grade·Section as a row, keyed by its tag; fill day columns from the grids.
  //    Also tally per-subject totals (periods + minutes) for the footer.
  const rowMap = new Map();      // tag -> { tag, gradeNum, subjSet, days: [cell|null × 6] }
  const totals = {};             // subject -> { periods, mins, swatch }
  subjects.forEach((s) => {
    (s.grades || []).forEach((g, gi) => {
      (g.sections || []).forEach((sec, secIdx) => {
        const tag = tagOf(g, sec);
        if (!rowMap.has(tag)) rowMap.set(tag, { tag, gradeNum: gradeNum(g.grade), subjSet: new Set(), days: DAYS.map(() => null) });
        const row = rowMap.get(tag);
        const gridRow = ((s.grids || [])[gi] || [])[secIdx] || [];
        const colorKey = singleGrade ? `${s.name}__${g.grade}__${tag}` : `${s.name}__${g.grade}`;
        DAYS.forEach((_, c) => {
          const di = gridRow[c];
          if (di != null && di >= 0) {
            const mins = (g.durations || [])[di] || 0;
            const sh = colorOf[colorKey] || {};
            row.days[c] = { subject: s.name, mins, ...sh };
            row.subjSet.add(s.name);
            if (!totals[s.name]) totals[s.name] = { subject: s.name, periods: 0, mins: 0 };
            totals[s.name].periods += 1;
            totals[s.name].mins += mins;
          }
        });
      });
    });
  });

  const rows = [...rowMap.values()]
    .map((r) => ({ ...r, subjects: [...r.subjSet] }))
    .sort((a, b) => a.gradeNum - b.gradeNum || a.tag.localeCompare(b.tag));

  // a representative swatch per subject for the footer (darkest grade's fill).
  const subjSwatch = {};
  legend.forEach((l) => { if (l.grades[0]) subjSwatch[l.subject] = { bg: l.grades[0].bg, ink: l.grades[0].ink }; });
  const subjectTotals = Object.values(totals).map((t) => ({ ...t, ...(subjSwatch[t.subject] || {}) }));
  const grandMins = subjectTotals.reduce((a, t) => a + t.mins, 0);

  return { rows, legend, subjectTotals, grandMins };
}

const fmtHrs = (mins) => {
  const h = Math.floor(mins / 60), m = mins % 60;
  return h ? `${h} h${m ? ` ${m} min` : ""}` : `${m} min`;
};

const SUBJ_SHORT = { "Social Sciences": "Soc. Sci.", "The World Around Us": "TWAU", "Mathematics": "Maths" };
const shortSubj = (n) => SUBJ_SHORT[n] || n;

// Same responsive check FirstRun's screen-6 WeekGrid uses (720px, matching the shell's own
// mobile breakpoint) — drives the row/column transpose below. Defaults to mobile (true) before
// the window is known, matching the app's mobile-first stance.
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

export default function MyCalendar({ readiness }) {
  const subjects = (readiness && readiness.subjects) || [];
  const { rows, legend } = useMemo(() => buildModel(subjects), [subjects]);
  const isMobile = useIsMobile(720);

  const [gradeFilter, setGradeFilter] = useState("all");     // a grade number, or "all"
  const [subjectFilter, setSubjectFilter] = useState("all"); // a subject name, or "all"

  // Grade options in ascending order (one entry per grade, regardless of section count).
  const gradeOptions = [...new Set(rows.map((r) => r.gradeNum))].sort((a, b) => a - b);
  const swatchOf = {};
  legend.forEach((l) => { if (l.grades[0]) swatchOf[l.subject] = l.grades[0].bg; });

  // Apply filters: grade filter narrows the rows; subject filter blanks non-matching cells.
  const shownRows = rows
    .filter((r) => gradeFilter === "all" || r.gradeNum === gradeFilter)
    .map((r) => ({
      ...r,
      days: r.days.map((cell) =>
        cell && (subjectFilter === "all" || cell.subject === subjectFilter) ? cell : null),
    }));

  // Totals reflect the CURRENT filter — tally only the cells actually shown.
  const totalsMap = {};
  shownRows.forEach((r) => r.days.forEach((cell) => {
    if (!cell) return;
    if (!totalsMap[cell.subject]) totalsMap[cell.subject] = { subject: cell.subject, periods: 0, mins: 0, bg: swatchOf[cell.subject] };
    totalsMap[cell.subject].periods += 1;
    totalsMap[cell.subject].mins += cell.mins || 0;
  }));
  const subjectTotals = Object.values(totalsMap);
  const grandMins = subjectTotals.reduce((a, t) => a + t.mins, 0);

  return (
    <div className="mycal">
      <div className="lvl-head">
        <div>
          <h1 className="lvl-title">My Calendar</h1>
          <p className="lvl-sub">Your teaching week — each section's classes by day. To change a schedule, open My Class.</p>
        </div>
      </div>

      {rows.length === 0 ? (
        <div className="cal-empty">No classes scheduled yet. Set weekly days in My Class → a grade → a section.</div>
      ) : (
        <>
          <div className="cal-filterbar">
            <div className="cal-fgroup">
              <span className="cal-fgroup-lbl">Grade</span>
              <div className="cal-chips">
                <button className={`cal-chip ${gradeFilter === "all" ? "on" : ""}`} onClick={() => setGradeFilter("all")}>All</button>
                {gradeOptions.map((g) => (
                  <button key={g} className={`cal-chip ${gradeFilter === g ? "on" : ""}`} onClick={() => setGradeFilter(g)}>{g}</button>
                ))}
              </div>
            </div>
            <div className="cal-fgroup">
              <span className="cal-fgroup-lbl">Subject filter</span>
              <div className="cal-chips">
                <button className={`cal-chip ${subjectFilter === "all" ? "on" : ""}`} onClick={() => setSubjectFilter("all")}>All</button>
                {legend.map((l) => (
                  <button key={l.subject} className={`cal-chip ${subjectFilter === l.subject ? "on" : ""}`} onClick={() => setSubjectFilter(l.subject)}>
                    <span className="cal-chip-dot" style={{ background: (l.grades[0] || {}).bg }} />{shortSubj(l.subject)}
                  </button>
                ))}
              </div>
            </div>
          </div>

          <div className="cal-scroll">
            {/* Transposed by viewport: phone = days as rows / sections as columns (a short
                six-row list, scrolled once per day); desktop = sections as rows / days as
                columns (the original layout). .cal-rowhd's existing sticky-left CSS keeps
                whichever label column is showing pinned in view either way. */}
            <table className="caltable">
              <thead>
                <tr>
                  <th className="cal-rowhd">{isMobile ? "Day" : "Class"}</th>
                  {(isMobile ? shownRows.map((r) => r.tag) : DAYS).map((c) => (
                    <th key={c} className="cal-dayhd">{c}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(isMobile ? DAYS : shownRows.map((r) => r.tag)).map((r, ri) => (
                  <tr key={r}>
                    <th className="cal-rowhd">
                      <span className="cal-rowhd-tag">{r}</span>
                    </th>
                    {(isMobile ? shownRows : DAYS).map((_, ci) => {
                      const rowIdx = isMobile ? ci : ri;
                      const dayIdx = isMobile ? ri : ci;
                      const cell = shownRows[rowIdx] ? shownRows[rowIdx].days[dayIdx] : null;
                      return (
                        <td key={ci} className="cal-cell">
                          {cell && (
                            <div className="cal-box" style={{ background: cell.bg, color: cell.ink }}>
                              <span className="cal-box-subj">{shortSubj(cell.subject)}</span>
                              {cell.mins != null && <span className="cal-box-min">{cell.mins} min</span>}
                            </div>
                          )}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div className="cal-totals">
            <div className="cal-total-grand">
              <span className="cal-total-clock">◷</span>
              <div>
                <div className="cal-total-cap">Total this week</div>
                <div className="cal-total-big">{grandMins} min</div>
                <div className="cal-total-sub">{fmtHrs(grandMins)}</div>
              </div>
            </div>
            {subjectTotals.map((t) => (
              <div key={t.subject} className="cal-total-subj">
                <span className="cal-total-swatch" style={{ background: t.bg }} />
                <div>
                  <div className="cal-total-name">{shortSubj(t.subject)}</div>
                  <div className="cal-total-detail">{t.periods} period{t.periods !== 1 ? "s" : ""} ({t.mins} min)</div>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  );
}
