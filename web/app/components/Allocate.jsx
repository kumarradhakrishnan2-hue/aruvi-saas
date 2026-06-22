"use client";
import { useEffect, useRef, useState } from "react";
import { getJSON, pad } from "../lib/format";
import PeriodRows, { toPeriodRows, periodTypeNames, totalsFinePrint } from "./PeriodRows";
import AllocationReportView from "./AllocationReportView";

/* ── Teacher-adjustment model (explicit Δ per duration, budget-neutral) ──
 * `deltas`: { [chapter_number]: { [duration]: number } }. No auto-rebalancing — the teacher
 * is responsible for both the addition and the matching deduction. We only validate. */

function deltaFor(deltas, cn, m) {
  return Number(deltas?.[cn]?.[m]) || 0;
}

/* Σ Δ for one duration column, across only the given (checked) chapters. */
function balanceFor(deltas, chapters, m) {
  return chapters.reduce((s, c) => s + deltaFor(deltas, c.chapter_number, m), 0);
}

/* Final value for one chapter/duration cell = suggested + Δ. */
function finalCell(byCh, deltas, cn, m) {
  const suggested = Number(byCh[cn]?.periods_by_duration?.[m]) || 0;
  return suggested + deltaFor(deltas, cn, m);
}

/* Chapters (from the given list) whose final value would go negative for any duration.
 * Returns a Set of chapter_number for easy row highlighting. */
function negativeRows(byCh, deltas, chapters, durations) {
  const bad = new Set();
  for (const c of chapters) {
    for (const m of durations) {
      if (finalCell(byCh, deltas, c.chapter_number, m) < 0) { bad.add(c.chapter_number); break; }
    }
  }
  return bad;
}

/* Build the locked-in Final Allocation (suggested + Δ) for the given chapters. Computed once,
 * on Save — not re-derived live — so editing deltas after Save doesn't silently move it. */
function buildFinalAllocation(res, byCh, deltas, chapters) {
  const dur = res.durations;
  const allocations = chapters.map((c) => {
    const a = byCh[c.chapter_number];
    const periods_by_duration = {};
    dur.forEach((m) => { periods_by_duration[m] = finalCell(byCh, deltas, c.chapter_number, m); });
    const total_periods = dur.reduce((s, m) => s + periods_by_duration[m], 0);
    const total_minutes = dur.reduce((s, m) => s + periods_by_duration[m] * Number(m), 0);
    return { chapter_number: c.chapter_number, chapter_title: a?.chapter_title || c.chapter_title,
      weight: a?.weight ?? 0, periods_by_duration, total_periods, total_minutes };
  });
  const totals = {
    periods: allocations.reduce((s, a) => s + a.total_periods, 0),
    minutes: allocations.reduce((s, a) => s + a.total_minutes, 0),
    by_duration: Object.fromEntries(dur.map((m) => [m, allocations.reduce((s, a) => s + a.periods_by_duration[m], 0)])),
  };
  return { durations: dur, allocations, totals };
}

export default function Allocate({ subject, grade }) {
  const [chapters, setChapters] = useState([]);
  const [basis, setBasis] = useState(null);
  const [rows, setRows] = useState([{ name: "", count: 45, minutes: 45 }, { name: "", count: 60, minutes: 60 }]);
  const [res, setRes] = useState(null);
  const [busy, setBusy] = useState(false);
  const [showHow, setShowHow] = useState(false);
  const [step, setStep] = useState("periods"); // "periods" | "select" | "adjust" | "final"
  const [selected, setSelected] = useState(null); // Set of chapter_number, null = "all" (not yet touched)
  const [deltas, setDeltas] = useState({}); // { [chapter_number]: { [duration]: number } }
  const [finalAlloc, setFinalAlloc] = useState(null); // locked-in result, set by Save Allocation
  const [allAllocations, setAllAllocations] = useState([]); // accumulate all saved allocations
  // "adjust" step has two sub-states: the AI suggestion is shown first with a binary choice
  // (Accept as-is vs Modify); only choosing Modify reveals the Δ columns / balance / save bar.
  const [modifying, setModifying] = useState(false);
  // Shown when Save Allocation is pressed while deltas are invalid (negative final allocation
  // for some chapter, or a non-zero net adjustment for some period type).
  const [showInvalidWarning, setShowInvalidWarning] = useState(false);
  const [showClearWarning, setShowClearWarning] = useState(false);
  const [allocationReport, setAllocationReport] = useState(null);

  // LocalStorage key for persisting allocations across subject/grade changes
  const allocationStorageKey = `allocations_${subject}_${grade}`;

  // Load persisted allocations from localStorage on mount or subject/grade change
  useEffect(() => {
    setRes(null);
    setStep("periods");
    setSelected(null);
    setDeltas({});
    setFinalAlloc(null);
    setModifying(false);

    // Load persisted allocations for this subject/grade combination
    try {
      const stored = localStorage.getItem(allocationStorageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        // Convert arrays back to proper structures
        const restored = parsed.map((alloc) => ({
          ...alloc,
          durations: alloc.durations || [],
          allocations: alloc.allocations || [],
        }));
        setAllAllocations(restored);
      } else {
        setAllAllocations([]);
      }
    } catch (e) {
      console.warn("Failed to load persisted allocations:", e);
      setAllAllocations([]);
    }

    getJSON(`/subjects/${subject}/${grade}/chapters`).then((d) => { setChapters(d.chapters); setBasis(d.allocation_basis); }).catch(() => { setChapters([]); setBasis(null); });
  }, [subject, grade, allocationStorageKey]);

  // Persist allocations to localStorage whenever they change
  useEffect(() => {
    try {
      localStorage.setItem(allocationStorageKey, JSON.stringify(allAllocations));
    } catch (e) {
      console.warn("Failed to persist allocations:", e);
    }
  }, [allAllocations, allocationStorageKey]);

  /* Build AllocationReport from the current final allocation state.
     This is called when entering the final step, and formats all the data
     needed by AllocationReportView for rendering and exporting. */
  const buildReport = (alloc, subject_) => {
    if (!alloc) return null;

    const stage = {
      "vii": "middle",
      "vi": "middle",
      "viii": "middle",
      "ix": "secondary",
      "x": "secondary",
      "iii": "preparatory",
      "iv": "preparatory",
      "v": "middle",
    }[grade] || "middle";

    const rows = alloc.allocations.map((a, idx) => ({
      chapter_number: a.chapter_number,
      chapter_name: a.chapter_title,
      total_periods: a.total_periods, // allocated for this year
      allocated_periods: a.total_periods,
      effort_index: a.effort_index || null,
      competency_weight: a.weight || null, // from allocations
    }));

    const periodProfileName = rows[0] && alloc.durations
      ? `${alloc.durations.length > 1 ? "Mixed" : "Standard"}`
      : "Custom";
    const periodDuration = alloc.durations && alloc.durations.length > 0
      ? Math.max(...alloc.durations.map(Number))
      : 45;

    return {
      subject: subject_,
      grade: parseInt(grade.replace(/[^\d]/g, "")) || 7,
      stage,
      period_profile_name: periodProfileName,
      period_duration_minutes: periodDuration,
      total_periods: alloc.totals.periods,
      generated_at: new Date().toISOString(),
      rows,
      allocation_basis: basis?.name || "Custom",
      notes: null,
    };
  };

  const isSelected = (cn) => selected === null || selected.has(cn);
  const selectedChapters = chapters.filter((c) => isSelected(c.chapter_number));
  const reqSeq = useRef(0);

  // Run the LRM allocation once, across only the chapters the teacher finalized on the
  // selection screen — not re-run live as checkboxes change (that screen has no numbers yet).
  const run = async (chapterList) => {
    const seq = ++reqSeq.current;
    const list = chapterList ?? selectedChapters;
    if (!list.length) return;
    setRes(null); // never let a stale (e.g. prior all-chapters) result render while a new one is in flight
    setBusy(true);
    try {
      const body = { period_rows: toPeriodRows(rows), chapter_numbers: list.map((c) => c.chapter_number) };
      if (process.env.NODE_ENV !== "production") console.debug("[allocate] request body:", body);
      const data = await getJSON(`/subjects/${subject}/${grade}/allocate`,
        { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify(body) });
      if (seq === reqSeq.current) setRes(data); // drop stale responses from superseded requests
    } finally { if (seq === reqSeq.current) setBusy(false); }
  };

  const goToSelect = () => setStep("select");

  // "Allocate Periods" button on the selection screen: run the LRM once for the chapters
  // checked at that moment, then move to the results/adjust screen.
  const allocatePeriods = async () => {
    await run();
    setStep("adjust");
  };

  const toggleAll = () => setSelected(selected === null || selected.size === chapters.length ? new Set() : null);
  const toggleOne = (cn) => {
    setSelected((cur) => {
      const next = new Set(cur === null ? chapters.map((c) => c.chapter_number) : cur);
      if (next.has(cn)) next.delete(cn); else next.add(cn);
      return next;
    });
  };

  const setDelta = (cn, m, value) => setDeltas((d) => ({ ...d, [cn]: { ...d[cn], [m]: value } }));
  const stepDelta = (cn, m, step_) => setDeltas((d) => ({ ...d, [cn]: { ...d[cn], [m]: deltaFor(d, cn, m) + step_ } }));

  // Durations sorted longest-first (matches the mock: 60 min before 45 min), with each
  // duration labeled using the name the teacher gave that period type on the periods screen.
  const dur = res ? [...res.durations].sort((a, b) => Number(b) - Number(a)) : [];
  const ptNames = periodTypeNames(rows);
  const byCh = res ? Object.fromEntries(res.allocations.map((a) => [a.chapter_number, a])) : {};
  const totalHours = toPeriodRows(rows).reduce((s, r) => s + (r.count * r.minutes) / 60, 0);
  const totalPeriods = toPeriodRows(rows).reduce((s, r) => s + r.count, 0);
  const allChecked = selected === null || selected.size === chapters.length;

  const balances = Object.fromEntries(dur.map((m) => [m, balanceFor(deltas, selectedChapters, m)]));
  const balancesOk = dur.every((m) => balances[m] === 0);
  const badRows = res ? negativeRows(byCh, deltas, selectedChapters, dur) : new Set();
  const canSave = !!res && selectedChapters.length > 0 && balancesOk && badRows.size === 0;

  const saveAllocation = () => {
    if (!canSave) { setShowInvalidWarning(true); return; }
    const newAlloc = buildFinalAllocation(res, byCh, deltas, selectedChapters);
    setFinalAlloc(newAlloc);
    setAllocationReport(buildReport(newAlloc, subject));
    setAllAllocations((prev) => [...prev, newAlloc]); // accumulate
    setStep("final");
  };

  // Accept Allocation: take the AI suggestion as-is (Δ = 0 everywhere) and save immediately —
  // no Δ table is ever shown for this path, matching "Option A" in the spec.
  const acceptAllocation = () => {
    if (!res || !selectedChapters.length) return;
    const newAlloc = buildFinalAllocation(res, byCh, {}, selectedChapters);
    setFinalAlloc(newAlloc);
    setAllocationReport(buildReport(newAlloc, subject));
    setAllAllocations((prev) => [...prev, newAlloc]); // accumulate
    setStep("final");
  };

  /* Export handlers for PDF and DOCX */
  const handleExportPDF = async () => {
    if (!allocationReport) return;
    try {
      const response = await fetch("/api/allocation/export-pdf", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(allocationReport),
      });
      if (!response.ok) throw new Error("Export failed");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `allocation-report-grade-${allocationReport.grade}-${subject}.pdf`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("PDF export error:", err);
      alert("Failed to export PDF. Please try again.");
    }
  };

  const handleExportDOCX = async () => {
    if (!allocationReport) return;
    try {
      const response = await fetch("/api/allocation/export-docx", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(allocationReport),
      });
      if (!response.ok) throw new Error("Export failed");
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `allocation-report-grade-${allocationReport.grade}-${subject}.docx`;
      a.click();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error("DOCX export error:", err);
      alert("Failed to export Word document. Please try again.");
    }
  };

  if (step === "final" && finalAlloc) {
    // Merge overlapping chapters: last allocation for a chapter wins (overwrites earlier)
    const mergedChapters = {};
    allAllocations.forEach((alloc) => {
      alloc.allocations.forEach((a) => {
        mergedChapters[a.chapter_number] = a; // last one wins
      });
    });
    const allChaptersData = Object.values(mergedChapters).sort((a, b) => a.chapter_number - b.chapter_number);
    const allocatedChapterNumbers = new Set(allChaptersData.map((a) => a.chapter_number));

    const combinedTotals = {
      periods: allChaptersData.reduce((s, a) => s + a.total_periods, 0),
      minutes: allChaptersData.reduce((s, a) => s + a.total_minutes, 0),
      by_duration: Object.fromEntries(finalAlloc.durations.map((m) => [
        m,
        allChaptersData.reduce((s, a) => s + (a.periods_by_duration[m] || 0), 0),
      ])),
    };

    const sortedDurations = [...finalAlloc.durations].sort((a, b) => Number(b) - Number(a));
    return (
      <div>
        <button className="back" onClick={() => setStep("adjust")}>← back to allocation</button>
        <p className="h2">Final allocation — {allChaptersData.length} chapters total.</p>
        <div className="atable-scroll">
        <table className="atable atable-combined">
          <thead><tr>
            <th>Chapter</th>
            {sortedDurations.map((m) => (
              <th className="num sub-h" key={m}>
                <span className="sub-h-name">{ptNames[m] || `${m} min period`}</span>
                <span className="sub-h-min">{m} min</span>
              </th>
            ))}
            <th className="num">Periods</th>
          </tr></thead>
          <tbody>{allChaptersData.map((a, idx) => (
            <tr key={`ch-${a.chapter_number}-${idx}`}>
              <td><span className="chn">CH {pad(a.chapter_number)}</span>{a.chapter_title}</td>
              {sortedDurations.map((m) => <td className="num" key={m}>{a.periods_by_duration[m] || 0}</td>)}
              <td className="num total">{a.total_periods}</td>
            </tr>
          ))}</tbody>
          <tfoot><tr>
            <td className="lbl">Total · {combinedTotals.minutes.toLocaleString()} min</td>
            {sortedDurations.map((m) => <td className="num" key={m}>{combinedTotals.by_duration[m]}</td>)}
            <td className="num total">{combinedTotals.periods}</td>
          </tr></tfoot>
        </table>
        </div>

        {/* Allocation Report with PDF/DOCX export */}
        {allocationReport && (
          <div style={{ marginTop: "2rem", marginBottom: "2rem" }}>
            <AllocationReportView
              report={allocationReport}
              onExportPDF={handleExportPDF}
              onExportDOCX={handleExportDOCX}
            />
          </div>
        )}

        <div className="savebar">
          <button className="primary" onClick={() => {
            // Set selected to only the chapters NOT yet allocated (inverse selection)
            const unallocated = new Set(chapters.filter((c) => !allocatedChapterNumbers.has(c.chapter_number)).map((c) => c.chapter_number));
            setSelected(unallocated.size === chapters.length ? null : unallocated); // null = all selected, so invert to unallocated
            setStep("select");
            setRes(null);
            setModifying(false);
            setDeltas({});
            setShowInvalidWarning(false);
          }}>
            Allocate more chapters →
          </button>
          <button className="clear-btn" onClick={() => setShowClearWarning(true)}>
            Clear all
          </button>
        </div>
        {showClearWarning ? (
          <div className="modal-backdrop" onClick={() => setShowClearWarning(false)}>
            <div className="modal-box" onClick={(e) => e.stopPropagation()}>
              <p className="modal-title">Are you sure?</p>
              <p className="modal-body">This will remove all saved chapter allocations for this subject.</p>
              <div className="modal-actions">
                <button className="primary" onClick={() => setShowClearWarning(false)}>Cancel</button>
                <button className="clear-btn" onClick={() => {
                  localStorage.removeItem(allocationStorageKey);
                  setStep("periods"); setRes(null); setSelected(null); setDeltas({}); setFinalAlloc(null); setAllAllocations([]); setModifying(false); setShowInvalidWarning(false); setShowClearWarning(false);
                }}>Clear All</button>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    );
  }

  // Step 2 — chapter selection only. No allocation numbers here: a plain checked/unchecked
  // list, default all selected. "Allocate Periods" runs the LRM once for whatever is checked.
  if (step === "select") {
    // Compute which chapters are already allocated (locked/greyed out)
    const allocatedChapterNumbers = new Set();
    allAllocations.forEach((alloc) => {
      alloc.allocations.forEach((a) => {
        allocatedChapterNumbers.add(a.chapter_number);
      });
    });

    return (
      <div>
        <div className="totalbar totalbar-compact">
          <div className="totalbar-left">
            <div className="totalbar-check">✓</div>
            <div className="totalbar-mid">
              <div className="totalbar-label">Total allocated time</div>
              <div className="totalbar-value">{totalPeriods} <span className="totalbar-unit">periods</span> / {totalHours % 1 === 0 ? totalHours : totalHours.toFixed(1)} <span className="totalbar-unit">hours</span></div>
              <div className="totalbar-fine">{totalsFinePrint(rows)}</div>
            </div>
          </div>
          <button className="back totalbar-edit" onClick={() => setStep("periods")}>← back to period types</button>
        </div>
        <p className="h2">Select the chapters you want to include in this year's plan.</p>

        {!chapters.length ? <div className="empty">No chapter mappings for this subject &amp; grade.</div> : (
          <>
            <div className="atable-card">
              <div className="atable-scroll">
              <table className="atable atable-combined">
                <thead>
                  <tr>
                    <th className="chk">
                      <input type="checkbox" checked={allChecked} onChange={toggleAll}
                        title={allChecked ? "Deselect all" : "Select all"} />
                    </th>
                    <th className="chapter-h">Chapter</th>
                  </tr>
                </thead>
                <tbody>{chapters.map((c) => {
                  const on = isSelected(c.chapter_number);
                  const isAllocated = allocatedChapterNumbers.has(c.chapter_number);
                  return (
                    <tr key={c.chapter_number} className={isAllocated ? "row-allocated" : on ? "" : "row-off"}>
                      <td className="chk"><input type="checkbox" checked={on} onChange={() => toggleOne(c.chapter_number)} disabled={isAllocated} title={isAllocated ? "Already allocated" : ""} /></td>
                      <td><span className="chn">CH {pad(c.chapter_number)}</span><span className="ch-title">{c.chapter_title}</span>{isAllocated ? <span className="ch-badge">allocated</span> : null}</td>
                    </tr>
                  );
                })}</tbody>
              </table>
              </div>
            </div>

            <div className="savebar">
              <button className="primary" onClick={allocatePeriods} disabled={busy || !selectedChapters.length}>
                {busy ? "Allocating…" : "Allocate Periods"}
              </button>
              {!selectedChapters.length ? <span className="savebar-hint">Select at least one chapter.</span> : null}
            </div>
          </>
        )}
      </div>
    );
  }

  // Step 3/4 — AI allocation result, scoped to only the chapters chosen in Step 2.
  // Accept Allocation saves as-is; Modify Allocation reveals the Δ columns.
  if (step === "adjust") {
    return (
      <div>
        <button className="back" onClick={() => { setStep("select"); setRes(null); setModifying(false); setDeltas({}); setShowInvalidWarning(false); }}>← back to chapter selection</button>
        <p className="h2">Suggested allocation</p>

        {basis ? (
          <div className="howbox">
            <button className="howtoggle" onClick={() => setShowHow(!showHow)}>
              <span className="howchevron">{showHow ? "▾" : "▸"}</span> Why did Aruvi allocate periods this way?
            </button>
            {showHow ? (
              <div className="howbody">
                <p>
                  Aruvi estimates the teaching effort required for each chapter and allocates periods proportionally.
                  {" "}The factors considered vary by subject and may include {basis.factors.join(", ").replace(/, ([^,]*)$/, " and $1")}.
                  {" "}Click the &ldquo;How time is allocated across chapters&rdquo; tab of <b className="howlink">Ask Aruvi</b> to know more.
                </p>
              </div>
            ) : null}
          </div>
        ) : null}

        {!res ? <div className="empty">Allocating…</div> : (
          <>
            <div className="atable-card">
              <div className="atable-scroll">
              <table className="atable atable-combined">
                <thead>
                  <tr className="grouprow">
                    <th className="chapter-h" rowSpan={2}>Chapter</th>
                    <th className="group-h" colSpan={dur.length + 1}>Suggested periods</th>
                    {modifying ? <th className="group-h group-h-adjust" colSpan={dur.length}>Change allocation</th> : null}
                  </tr>
                  <tr>
                    {dur.map((m) => (
                      <th className="num sub-h" key={m}>
                        <span className="sub-h-name">{ptNames[m] || `${m} min period`}</span>
                        <span className="sub-h-min">{m} min</span>
                      </th>
                    ))}
                    <th className="num sub-h">Total periods</th>
                    {modifying ? dur.map((m) => (
                      <th className="num sub-h sub-h-adjust" key={m}>
                        <span className="sub-h-name">Δ {ptNames[m] || `${m} min period`}</span>
                        <span className="sub-h-min">{m} min</span>
                      </th>
                    )) : null}
                  </tr>
                </thead>
                <tbody>{selectedChapters.map((c) => {
                  const a = byCh[c.chapter_number];
                  const bad = modifying && badRows.has(c.chapter_number);
                  return (
                    <tr key={c.chapter_number} className={bad ? "row-bad" : ""}>
                      <td><span className="chn">CH {pad(c.chapter_number)}</span><span className="ch-title">{c.chapter_title}</span></td>
                      {dur.map((m) => <td className="num" key={m}>{a ? a.periods_by_duration[m] : ""}</td>)}
                      <td className="num total">{a ? a.total_periods : ""}</td>
                      {modifying ? dur.map((m) => {
                        const dv = deltaFor(deltas, c.chapter_number, m);
                        return (
                        <td className="num adjust-cell" key={m}>
                          <div className="stepper stepper-sm stepper-delta">
                            <button type="button" className="step-btn" onClick={() => stepDelta(c.chapter_number, m, -1)} disabled={busy} aria-label="decrease">−</button>
                            <input className={`step-in${dv < 0 ? " step-in-neg" : ""}`} type="text" inputMode="numeric"
                              value={deltas[c.chapter_number]?.[m] ?? 0}
                              onChange={(e) => { const v = e.target.value; if (/^-?\d*$/.test(v)) setDelta(c.chapter_number, m, v === "" || v === "-" ? v : Number(v)); }}
                              onBlur={(e) => { if (e.target.value === "" || e.target.value === "-") setDelta(c.chapter_number, m, 0); }} />
                            <button type="button" className="step-btn" onClick={() => stepDelta(c.chapter_number, m, 1)} disabled={busy} aria-label="increase">+</button>
                          </div>
                        </td>
                        );
                      }) : null}
                    </tr>
                  );
                })}</tbody>
                <tfoot><tr>
                  <td className="lbl">Total</td>
                  {dur.map((m) => <td className="num" key={m}>{res.totals.by_duration[m]}</td>)}
                  <td className="num total">{res.totals.periods}</td>
                  {modifying ? dur.map((m) => (
                    <td className={`num adjust-cell adjust-total ${balances[m] !== 0 ? "adjust-total-warn" : ""}`} key={m}>
                      {balances[m] > 0 ? `+${balances[m]}` : balances[m]}
                    </td>
                  )) : null}
                </tr></tfoot>
              </table>
              </div>
            </div>

            {!modifying ? (
              <div className="savebar">
                <button className="primary" onClick={acceptAllocation}>Accept Allocation</button>
                <button className="modify-btn" onClick={() => setModifying(true)}>Modify Allocation</button>
              </div>
            ) : (
              <div className="savebar">
                <button className="primary" onClick={saveAllocation}>Save Allocation</button>
                <button className="back" onClick={() => { setDeltas({}); setModifying(false); setShowInvalidWarning(false); }}>← back</button>
              </div>
            )}
          </>
        )}

        {showInvalidWarning ? (
          <div className="modal-backdrop" onClick={() => setShowInvalidWarning(false)}>
            <div className="modal-box" onClick={(e) => e.stopPropagation()}>
              <p className="modal-title">⚠ Allocation can&rsquo;t be saved yet</p>
              <p className="modal-body">
                {badRows.size > 0
                  ? "One or more chapters would have a negative number of periods. Adjust the Δ values so every chapter's final allocation is zero or more."
                  : "Your adjustments don't balance out — the periods you add to some chapters must be matched by periods you remove from others, for every period type."}
              </p>
              <div className="modal-actions">
                <button className="primary" onClick={() => setShowInvalidWarning(false)}>Got it</button>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    );
  }

  return (
    <div>
      <p className="h2">Allocate the available time across chapters</p>
      <p className="h2-sub">To begin, set the total number of periods available and how long each period type lasts below.</p>

      <div className="ptsection-label">Period types <span className="infoq" title="Define the period types that fit your school schedule.">ⓘ</span></div>
      <PeriodRows rows={rows} setRows={setRows} />

      <div className="totalbar">
        <div className="totalbar-left">
          <div className="totalbar-check">✓</div>
          <div className="totalbar-mid">
            <div className="totalbar-label">Total allocated time</div>
            <div className="totalbar-value">{totalPeriods} <span className="totalbar-unit">periods</span> / {totalHours % 1 === 0 ? totalHours : totalHours.toFixed(1)} <span className="totalbar-unit">hours</span></div>
            <div className="totalbar-fine">{totalsFinePrint(rows)}</div>
          </div>
        </div>
        <button className="primary" onClick={goToSelect} disabled={!chapters.length}>
          Continue to chapter selection →
        </button>
      </div>
    </div>
  );
}
