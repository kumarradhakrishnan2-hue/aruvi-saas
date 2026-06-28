"use client";
import { useState, useMemo } from "react";

/* ───────── MyCalendar — read-only weekly timetable (2026-06-28) ─────────
 * The teacher's whole week at a glance. Rows = Grade·Section (e.g. "6A"), columns = the six
 * weekdays. Each filled cell is the class that section meets that day, showing the subject name
 * and the period duration. View-only: editing the schedule lives in My Class → Section day grids.
 *
 * Built straight off the canonical readiness profile (readiness.subjects[]) — the same shape
 * MyClasses edits:
 *   subjects[] → { name, grades[]→{grade, sections[]→{tag,sec}}, durations[], grids }
 *     grids[gradeIdx][secIdx][dayIdx] = durationIndex | -1
 * Because one teacher teaches each section, at most one subject meets a given Grade·Section on a
 * given day, so every cell holds a single class (no stacking needed).
 *
 * COLOUR: each subject gets a colour FAMILY (auto-assigned in encounter order from a fixed
 * palette); within a family, grades are shaded darkest→lightest by grade order, so e.g. Science
 * Grade 6 and Grade 5 are two greens. Computed inline as CSS custom properties so the stylesheet
 * stays generic.
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

// Flatten readiness into: rows (one per Grade·Section) + a colour map per (subject,grade).
function buildModel(subjects) {
  // 1) assign a colour family per subject (encounter order), and shades per grade within it.
  const colorOf = {};            // `${subject}__${grade}` -> {bg, ink}
  const legend = [];             // [{ subject, grades:[{grade, bg, ink}] }]
  subjects.forEach((s, si) => {
    const fam = FAMILIES[si % FAMILIES.length];
    const gsorted = [...(s.grades || [])].sort((a, b) => gradeNum(a.grade) - gradeNum(b.grade));
    // darkest = HIGHEST grade (e.g. "darker green for 6A, lighter for 5B") → reverse for idx
    const order = [...gsorted].sort((a, b) => gradeNum(b.grade) - gradeNum(a.grade));
    const entry = { subject: s.name, grades: [] };
    order.forEach((g, idx) => {
      const sh = shade(fam, idx, order.length);
      colorOf[`${s.name}__${g.grade}`] = sh;
      entry.grades.push({ grade: g.grade, ...sh });
    });
    legend.push(entry);
  });

  // 2) collect every Grade·Section as a row, keyed by its tag; fill day columns from the grids.
  //    Also tally per-subject totals (periods + minutes) for the footer.
  const rowMap = new Map();      // tag -> { tag, gradeNum, subjSet, days: [cell|null × 6] }
  const totals = {};             // subject -> { periods, mins, swatch }
  subjects.forEach((s) => {
    (s.grades || []).forEach((g, gi) => {
      (g.sections || []).forEach((sec, secIdx) => {
        const tag = sec.tag || `${gradeNum(g.grade)}${sec.sec || ""}`;
        if (!rowMap.has(tag)) rowMap.set(tag, { tag, gradeNum: gradeNum(g.grade), subjSet: new Set(), days: DAYS.map(() => null) });
        const row = rowMap.get(tag);
        const gridRow = ((s.grids || [])[gi] || [])[secIdx] || [];
        DAYS.forEach((_, c) => {
          const di = gridRow[c];
          if (di != null && di >= 0) {
            const mins = (g.durations || [])[di] || 0;
            const sh = colorOf[`${s.name}__${g.grade}`] || {};
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

export default function MyCalendar({ readiness }) {
  const subjects = (readiness && readiness.subjects) || [];
  const { rows, legend } = useMemo(() => buildModel(subjects), [subjects]);

  const [classFilter, setClassFilter] = useState("all");     // a row tag, or "all"
  const [subjectFilter, setSubjectFilter] = useState("all"); // a subject name, or "all"

  const classOptions = rows.map((r) => r.tag);
  const swatchOf = {};
  legend.forEach((l) => { if (l.grades[0]) swatchOf[l.subject] = l.grades[0].bg; });

  // Apply filters: class filter narrows the rows; subject filter blanks non-matching cells.
  const shownRows = rows
    .filter((r) => classFilter === "all" || r.tag === classFilter)
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
              <span className="cal-fgroup-lbl">Classes</span>
              <div className="cal-chips">
                <button className={`cal-chip ${classFilter === "all" ? "on" : ""}`} onClick={() => setClassFilter("all")}>All</button>
                {classOptions.map((t) => (
                  <button key={t} className={`cal-chip ${classFilter === t ? "on" : ""}`} onClick={() => setClassFilter(t)}>{t}</button>
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
            <table className="caltable">
              <thead>
                <tr>
                  <th className="cal-rowhd">Class</th>
                  {DAYS.map((d) => <th key={d} className="cal-dayhd">{d}</th>)}
                </tr>
              </thead>
              <tbody>
                {shownRows.map((row) => (
                  <tr key={row.tag}>
                    <th className="cal-rowhd">
                      <span className="cal-rowhd-tag">{row.tag}</span>
                    </th>
                    {row.days.map((cell, c) => (
                      <td key={c} className="cal-cell">
                        {cell && (
                          <div className="cal-box" style={{ background: cell.bg, color: cell.ink }}>
                            <span className="cal-box-subj">{shortSubj(cell.subject)}</span>
                            {cell.mins != null && <span className="cal-box-min">{cell.mins} min</span>}
                          </div>
                        )}
                      </td>
                    ))}
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
