"use client";
import { useEffect, useRef, useState } from "react";
import { getJSON, pad, API, pretty } from "../lib/format";
import PeriodRows, { Stepper, toPeriodRows, periodTypeNames, totalsFinePrint } from "./PeriodRows";
import ViewModelView from "./ViewModelView";

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

/* Derive the weekly period-type ratio from the readiness payload, for this subject·grade.
 * Returns { [minutes]: count } counting how many cells of each duration the teacher set in
 * her weekly grid (summed across this subject's grades). Falls back to null when readiness
 * data isn't available, in which case G4 uses the period-type rows' own counts as the ratio. */
function weeklyRatioFromReadiness(readiness) {
  if (!readiness || !readiness.grids || !readiness.durations) return null;
  const ratio = {};
  readiness.grids.forEach((grid, gi) => {
    const durs = readiness.durations[gi] || [];
    grid.forEach((row) => row.forEach((v) => {
      if (v >= 0 && durs[v] != null) {
        const m = String(durs[v]);
        ratio[m] = (ratio[m] || 0) + 1;
      }
    }));
  });
  return Object.keys(ratio).length ? ratio : null;
}

/* Split a total period count across period types by a ratio map { [minutes]: weight }.
 * Largest-remainder method so the per-type counts always sum back to `total` exactly. */
function splitByRatio(total, ratio) {
  const types = Object.keys(ratio).map((m) => ({ m, w: ratio[m] }));
  const sumW = types.reduce((s, t) => s + t.w, 0) || 1;
  const raw = types.map((t) => ({ m: t.m, exact: (total * t.w) / sumW }));
  const out = {};
  let assigned = 0;
  raw.forEach((r) => { out[r.m] = Math.floor(r.exact); assigned += out[r.m]; });
  // distribute the remainder to the largest fractional parts
  const rem = total - assigned;
  raw.map((r) => ({ m: r.m, frac: r.exact - Math.floor(r.exact) }))
     .sort((a, b) => b.frac - a.frac)
     .slice(0, Math.max(0, rem))
     .forEach((r) => { out[r.m] += 1; });
  return out;
}

export default function Allocate({ subject, grade, readiness, onNavigate }) {
  const [chapters, setChapters] = useState([]);
  const [basis, setBasis] = useState(null);
  const [rows, setRows] = useState([{ name: "", count: 45, minutes: 45 }, { name: "", count: 60, minutes: 60 }]);
  const [res, setRes] = useState(null);
  const [busy, setBusy] = useState(false);
  const [showHow, setShowHow] = useState(false);
  const [step, setStep] = useState("periods"); // "periods" | "select" | "adjust" | "final" | "generate"
  const [genPlans, setGenPlans] = useState([]);   // saved plans for this subject·grade (generate spoke)
  const [genView, setGenView] = useState(null);   // currently-opened plan view
  const [genBusy, setGenBusy] = useState(false);
  const [totalPeriodsInput, setTotalPeriodsInput] = useState(48); // G4: single total → split by weekly ratio
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

  // LocalStorage key — now just a same-browser cache for instant paint; the server-side
  // register (app/mirror/allocations/{subject}/{grade}/allocation.json) is the source of
  // truth and is what actually survives an API/web server restart or a fresh browser.
  const allocationStorageKey = `allocations_${subject}_${grade}`;

  // Convert the saved server register ({chapter_num: AllocationRecord}) into the same
  // { durations, allocations, totals } shape buildFinalAllocation() produces, so the
  // "final" step can render it without any special-casing.
  const registerToAlloc = (register) => {
    const entries = Object.entries(register || {});
    if (!entries.length) return null;
    const durSet = new Set();
    entries.forEach(([, rec]) => Object.keys(rec.periods_by_duration || {}).forEach((m) => durSet.add(m)));
    const durations = [...durSet];
    const allocations = entries.map(([cn, rec]) => ({
      chapter_number: Number(cn),
      chapter_title: rec.chapter_title || "",
      weight: rec.weight ?? 0,
      periods_by_duration: rec.periods_by_duration || {},
      total_periods: rec.total_periods ?? 0,
      total_minutes: rec.total_minutes ?? 0,
    }));
    const totals = {
      periods: allocations.reduce((s, a) => s + a.total_periods, 0),
      minutes: allocations.reduce((s, a) => s + a.total_minutes, 0),
      by_duration: Object.fromEntries(durations.map((m) => [m, allocations.reduce((s, a) => s + (a.periods_by_duration[m] || 0), 0)])),
    };
    return { durations, allocations, totals };
  };

  // Load persisted allocations on mount or subject/grade change: paint instantly from
  // localStorage (if present), then reconcile against the server register, which wins.
  useEffect(() => {
    setRes(null);
    setStep("periods");
    setSelected(null);
    setDeltas({});
    setFinalAlloc(null);
    setModifying(false);

    try {
      const stored = localStorage.getItem(allocationStorageKey);
      if (stored) {
        const parsed = JSON.parse(stored);
        const restored = parsed.map((alloc) => ({ ...alloc, durations: alloc.durations || [], allocations: alloc.allocations || [] }));
        setAllAllocations(restored);
      } else {
        setAllAllocations([]);
      }
    } catch (e) {
      console.warn("Failed to load cached allocations:", e);
      setAllAllocations([]);
    }

    getJSON(`/subjects/${subject}/${grade}/chapters`).then((d) => { setChapters(d.chapters); setBasis(d.allocation_basis); }).catch(() => { setChapters([]); setBasis(null); });

    // saved plans power the generate spoke's previews (live gen deferred)
    setGenView(null);
    getJSON(`/plans/${subject}/${grade}`).then((d) => setGenPlans(d.plans || [])).catch(() => setGenPlans([]));

    // Server register is the source of truth — overrides the localStorage paint above
    // once it arrives, so a restarted server / fresh browser still shows saved work.
    getJSON(`/subjects/${subject}/${grade}/allocation`).then((d) => {
      const alloc = registerToAlloc(d.allocation);
      if (alloc && alloc.allocations.length) {
        setAllAllocations([alloc]);
        setFinalAlloc(alloc);
        setStep("final");
      }
    }).catch((e) => console.warn("Failed to load saved allocation register:", e));
  }, [subject, grade, allocationStorageKey]);

  // Cache allocations to localStorage whenever they change (instant repaint on next visit;
  // not relied on for durability — the server register is authoritative).
  useEffect(() => {
    try {
      localStorage.setItem(allocationStorageKey, JSON.stringify(allAllocations));
    } catch (e) {
      console.warn("Failed to cache allocations:", e);
    }
  }, [allAllocations, allocationStorageKey]);

  /* Build the AllocationReport payload from the final allocation state.
     Called on Accept/Save; this is the exact JSON POSTed to the export
     endpoints (no on-page rendering — downloads only). */
  const buildReport = (alloc, subject_) => {
    if (!alloc) return null;

    const durations = alloc.durations || [];

    // Per-chapter allocation. The API enriches each chapter with its competencies
    // (code + description + justification) and effort signals server-side, so the
    // frontend only ships the periods. periods_by_duration is keyed by minutes.
    const reportChapters = alloc.allocations.map((a) => {
      const pbd = {};
      durations.forEach((m) => { pbd[m] = a.periods_by_duration?.[m] || 0; });
      return {
        chapter_number: a.chapter_number,
        chapter_title: a.chapter_title,
        periods_by_duration: pbd,
        total_periods: a.total_periods,
        total_minutes: a.total_minutes ?? durations.reduce((s, m) => s + (pbd[m] || 0) * Number(m), 0),
        weight: a.weight ?? null,
      };
    });

    // Period types used in this allocation: {minutes, count}.
    const periodTypes = durations.map((m) => ({
      minutes: Number(m),
      count: reportChapters.reduce((s, c) => s + (c.periods_by_duration[m] || 0), 0),
    }));

    return {
      subject: subject_,
      grade: String(grade),          // roman string; API derives stage from it
      generated_at: new Date().toISOString(),
      period_types: periodTypes,
      chapters: reportChapters,
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

  // Build the {chapter_num: AllocationRecord} payload the /save_allocation endpoint
  // expects, from the same shape buildFinalAllocation() returns.
  const toRegisterPayload = (alloc) => Object.fromEntries(alloc.allocations.map((a) => [
    String(a.chapter_number),
    {
      chapter_title: a.chapter_title,
      weight: a.weight,
      periods_by_duration: a.periods_by_duration,
      total_periods: a.total_periods,
      total_minutes: a.total_minutes,
    },
  ]));

  // Persist the allocation to the server's file-backed register (the actual source of
  // truth — see registerToAlloc/the GET effect above). Fire-and-forget from the UI's
  // perspective: we've already committed to "final" locally, so a transient network
  // error here shouldn't block the teacher; it just means this save didn't reach disk
  // and a hard refresh would fall back to the last server-confirmed state.
  const persistAllocation = async (alloc) => {
    try {
      await getJSON(`/subjects/${subject}/${grade}/save_allocation`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subject, grade: String(grade), allocation: toRegisterPayload(alloc) }),
      });
    } catch (e) {
      console.warn("Failed to save allocation to server:", e);
    }
  };

  const saveAllocation = () => {
    if (!canSave) { setShowInvalidWarning(true); return; }
    const newAlloc = buildFinalAllocation(res, byCh, deltas, selectedChapters);
    setFinalAlloc(newAlloc);
    setAllocationReport(buildReport(newAlloc, subject));
    setAllAllocations((prev) => [...prev, newAlloc]); // accumulate
    setStep("final");
    persistAllocation(newAlloc);
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
    persistAllocation(newAlloc);
  };

  /* Export handlers for PDF and DOCX. The report itself isn't shown on the page —
     these just stream the file from the API and trigger a browser download.
     NOTE: hit the API base (port 8000), not a relative path (which would hit the
     Next dev server on :3000 and 404). */
  const [exporting, setExporting] = useState({ pdf: false, docx: false });

  const downloadReport = async (fmt) => {
    if (!allocationReport) return;
    setExporting((p) => ({ ...p, [fmt]: true }));
    try {
      const response = await fetch(`${API}/api/allocation/export-${fmt}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(allocationReport),
      });
      if (!response.ok) {
        // FastAPI's `detail` may be a string OR (for 422) an array of error objects.
        let detail = `HTTP ${response.status}`;
        try {
          const body = await response.json();
          if (typeof body?.detail === "string") detail = body.detail;
          else if (Array.isArray(body?.detail)) detail = body.detail.map((e) => e.msg || JSON.stringify(e)).join("; ");
          else if (body?.detail) detail = JSON.stringify(body.detail);
        } catch {}
        throw new Error(detail);
      }
      const blob = await response.blob();
      const url = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = url;
      a.download = `allocation-report-grade-${allocationReport.grade}-${subject}.${fmt}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      console.error(`${fmt.toUpperCase()} export error:`, err);
      const msg = err?.message
        ? err.message
        : "Couldn't reach the Aruvi engine (is the API running on :8000?).";
      alert(`Couldn't generate the ${fmt.toUpperCase()} report.\n\n${msg}`);
    } finally {
      setExporting((p) => ({ ...p, [fmt]: false }));
    }
  };

  const handleExportPDF = () => downloadReport("pdf");
  const handleExportDOCX = () => downloadReport("docx");

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
    const allChaptersAllocated = chapters.length > 0 && chapters.every((c) => allocatedChapterNumbers.has(c.chapter_number));

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
        {/* G2 hub — the allocation table is the resting/landing state for this subject·grade.
            Budget bar shows what's committed; the action bar below carries the three spokes
            (allocate more · generate · reset). annualBudget plumbing from readiness is a
            follow-up; for now the bar reports the committed allocation. */}
        <div className="hubbudget">
          <div className="hubbudget-row">
            <span className="hubbudget-k">Allocated for this subject · grade</span>
            <span className="hubbudget-v">{combinedTotals.periods} periods · {Math.round(combinedTotals.minutes / 60)}h</span>
          </div>
          <div className="hubbudget-note">{allChaptersAllocated ? "All chapters allocated." : `${allChaptersData.length} of ${chapters.length} chapters allocated.`}</div>
        </div>
        <div className="final-head">
          <div>
            <p className="h2 final-h2">Final allocation — {allChaptersData.length} chapters total.</p>
            <p className="final-saved">Allocation has been saved successfully.</p>
          </div>
          {allocationReport && (
            <div className="reports-inline">
              <span className="reports-inline-label">Reports</span>
              <div className="reports-inline-actions">
                <button className="filebtn filebtn-pdf" onClick={handleExportPDF} disabled={exporting.pdf} aria-label="Download PDF report">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 2.5h8.5L19 7v13a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 5 20V4a1.5 1.5 0 0 1 1-1.5Z" fill="#c0392b"/>
                    <path d="M14.5 2.5V7H19l-4.5-4.5Z" fill="#e0735a"/>
                    <text x="12" y="17.2" textAnchor="middle" fontFamily="IBM Plex Mono, monospace" fontSize="6.2" fontWeight="700" fill="#fff">PDF</text>
                  </svg>
                  {exporting.pdf ? "Preparing…" : "PDF"}
                </button>
                <button className="filebtn filebtn-docx" onClick={handleExportDOCX} disabled={exporting.docx} aria-label="Download Word report">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                    <path d="M6 2.5h8.5L19 7v13a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 5 20V4a1.5 1.5 0 0 1 1-1.5Z" fill="#1e5ca8"/>
                    <path d="M14.5 2.5V7H19l-4.5-4.5Z" fill="#5b8fd6"/>
                    <text x="12" y="17.2" textAnchor="middle" fontFamily="IBM Plex Mono, monospace" fontSize="6.2" fontWeight="700" fill="#fff">DOC</text>
                  </svg>
                  {exporting.docx ? "Preparing…" : "Word"}
                </button>
              </div>
            </div>
          )}
        </div>
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
            <td className="lbl">Total</td>
            {sortedDurations.map((m) => <td className="num" key={m}>{combinedTotals.by_duration[m]}</td>)}
            <td className="num total">{combinedTotals.periods}</td>
          </tr></tfoot>
        </table>
        </div>

        <div className="savebar savebar-final">
          {!allChaptersAllocated ? (
            <button className="continue-btn continue-btn-ghost" onClick={() => {
              // Set selected to only the chapters NOT yet allocated (inverse selection)
              const unallocated = new Set(chapters.filter((c) => !allocatedChapterNumbers.has(c.chapter_number)).map((c) => c.chapter_number));
              setSelected(unallocated.size === chapters.length ? null : unallocated); // null = all selected, so invert to unallocated
              setStep("select");
              setRes(null);
              setModifying(false);
              setDeltas({});
              setShowInvalidWarning(false);
            }}>
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <circle cx="12" cy="12" r="9.25" stroke="currentColor" strokeWidth="1.5"/>
                <path d="M10.3 8.3 14 12l-3.7 3.7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
              </svg>
              Continue Allocating
            </button>
          ) : null}
          <button className="continue-btn" onClick={() => setStep("generate")}>
            Continue to Generate
            <svg width="18" height="18" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
              <circle cx="12" cy="12" r="9.25" stroke="currentColor" strokeWidth="1.5"/>
              <path d="M10.3 8.3 14 12l-3.7 3.7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
        {/* Reset is destructive — kept out of the navigation row, in its own danger zone (G2 spec). */}
        <div className="hubdanger">
          <span className="hubdanger-k">Manage allocations</span>
          <button className="clear-btn" onClick={() => setShowClearWarning(true)}>
            Reset allocations…
          </button>
        </div>
        {showClearWarning ? (
          <div className="modal-backdrop" onClick={() => setShowClearWarning(false)}>
            <div className="modal-box" onClick={(e) => e.stopPropagation()}>
              <p className="modal-title">Are you sure?</p>
              <p className="modal-body">This will remove all saved chapter allocations for this subject at this grade level.</p>
              <div className="modal-actions">
                <button className="primary" onClick={() => setShowClearWarning(false)}>Cancel</button>
                <button className="clear-btn" onClick={() => {
                  localStorage.removeItem(allocationStorageKey);
                  getJSON(`/subjects/${subject}/${grade}/allocation`, { method: "DELETE" }).catch((e) => console.warn("Failed to clear server allocation register:", e));
                  setStep("periods"); setRes(null); setSelected(null); setDeltas({}); setFinalAlloc(null); setAllAllocations([]); setModifying(false); setShowInvalidWarning(false); setShowClearWarning(false);
                }}>Reset allocations</button>
              </div>
            </div>
          </div>
        ) : null}
      </div>
    );
  }

  // Generate spoke (G7) — reached from the hub's "Continue to Generate". Pick an allocated
  // chapter and view its plan. Live generation is deferred, so this serves the saved-plan
  // preview for the chapter (same source as the old Generate tab).
  if (step === "generate") {
    const allocatedNums = new Set();
    allAllocations.forEach((alloc) => alloc.allocations.forEach((a) => allocatedNums.add(a.chapter_number)));
    const allocatedList = chapters.filter((c) => allocatedNums.has(c.chapter_number));
    const planFor = (cn) => genPlans.find((p) => String(p.chapter_number) === String(cn));

    const openPlan = async (cn) => {
      const match = planFor(cn);
      if (!match) return;
      setGenBusy(true);
      try { setGenView((await getJSON(`/plans/${subject}/${grade}/${match.filename}/view`)).view); }
      finally { setGenBusy(false); }
    };

    if (genView) {
      return (
        <div>
          <button className="back" onClick={() => setGenView(null)}>← back to chapters</button>
          <ViewModelView view={genView} />
        </div>
      );
    }

    return (
      <div>
        <button className="back" onClick={() => setStep("final")}>← back to allocation</button>
        <p className="h2">Make a lesson plan</p>
        <p className="h2-sub">Pick a chapter you&rsquo;ve allocated. Aruvi builds the lesson plan + its assessment. (Live generation is coming soon — allocated chapters with a saved plan open as a preview.)</p>
        {!allocatedList.length ? (
          <div className="empty">No allocated chapters yet — allocate some first.</div>
        ) : (
          <div className="atable-card">
            {allocatedList.map((c) => {
              const hasPlan = !!planFor(c.chapter_number);
              return (
                <div className="genrow" key={c.chapter_number}>
                  <div><span className="chn">CH {pad(c.chapter_number)}</span><span className="ch-title">{c.chapter_title}</span></div>
                  {hasPlan ? (
                    <button className="primary" onClick={() => openPlan(c.chapter_number)} disabled={genBusy}>
                      {genBusy ? "Opening…" : "Open plan →"}
                    </button>
                  ) : (
                    <span className="gen-soon">plan coming soon</span>
                  )}
                </div>
              );
            })}
          </div>
        )}
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
        <p className="h2-sub">Now choose the chapters you plan to cover in this time. Aruvi holds your plan safely, so you can return and plan the rest of the chapters whenever you're ready.</p>

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
              <span className="howchevron">{showHow ? "▾" : "▸"}</span> How does Aruvi allocate?
            </button>
            {showHow ? (
              <div className="howbody">
                <p className="howbasis">
                  Aruvi splits your periods across chapters by each chapter&rsquo;s <b>{basis.basis || "effort index"}</b> — heavier chapters get more time. For {pretty(subject)}, it weighs:
                </p>
                <ul className="howfactors">
                  {basis.factors.map((f, i) => <li key={i}>{f}</li>)}
                </ul>
                <p className="howmore">
                  Other subjects weigh different things. Want the deeper &ldquo;why&rdquo; for a chapter? Open the &ldquo;How time is allocated across chapters&rdquo; tab of <b className="howlink">Ask Aruvi</b>.
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
                <button className="primary" onClick={saveAllocation}>Save changes</button>
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

  // ── G4 — how many periods in total → split across period types by the weekly ratio ──
  // Ratio source: the readiness weekly grid when available; otherwise the period-type rows'
  // own counts (so the screen still works before readiness data is threaded in).
  const ratio = weeklyRatioFromReadiness(readiness) ||
    Object.fromEntries(toPeriodRows(rows).map((r) => [String(r.minutes), r.count]));
  const ratioTypes = Object.keys(ratio).map(Number).sort((a, b) => b - a); // longest first
  const g4Total = Number(totalPeriodsInput) || 0;
  const g4Split = splitByRatio(g4Total, ratio);
  const g4Minutes = ratioTypes.reduce((s, m) => s + (g4Split[String(m)] || 0) * m, 0);

  // Commit the split into `rows` (the internal contract the rest of the flow consumes),
  // then advance to chapter selection.
  const g4Continue = () => {
    const newRows = ratioTypes.map((m) => ({ name: "", count: g4Split[String(m)] || 0, minutes: m }));
    setRows(newRows.length ? newRows : rows);
    setStep("select");
  };

  return (
    <div>
      <p className="h2">How many periods do these chapters get in total?</p>
      <p className="h2-sub">Your weekly schedule already tells Aruvi how long each period is — just give the total number of periods. Aruvi splits it across your period lengths, then across chapters in the next steps.</p>

      <div className="g4-grid">
        <div className="g4-input-card">
          <div className="g4-input-label">Periods in total</div>
          <Stepper value={totalPeriodsInput} min={0} onChange={setTotalPeriodsInput} />
          <div className="g4-input-fine">
            Split using your weekly mix
            {ratioTypes.length ? ` (${ratioTypes.map((m) => `${ratio[String(m)]}×${m}min`).join(" : ")})` : ""}.
          </div>
        </div>

        <div className="g4-breakdown">
          <div className="g4-breakdown-h">By period length</div>
          {ratioTypes.map((m) => (
            <div className="g4-brow" key={m}>
              <span className="g4-bk">{m} min <small>× {g4Split[String(m)] || 0}</small></span>
              <span className="g4-bv">{(((g4Split[String(m)] || 0) * m) / 60).toFixed(1)}h</span>
            </div>
          ))}
          <div className="g4-bfoot">{g4Total} periods · ~{(g4Minutes / 60).toFixed(1)}h total</div>
        </div>
      </div>

      <div className="savebar">
        <button className="primary" onClick={g4Continue} disabled={!chapters.length || g4Total < 1}>
          Continue to chapter selection →
        </button>
        {!chapters.length ? <span className="savebar-hint">No chapter mappings for this subject &amp; grade.</span> : null}
      </div>
    </div>
  );
}
