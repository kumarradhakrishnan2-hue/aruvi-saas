"use client";
import { useEffect, useMemo, useState } from "react";
import { annualBudgetPeriods, getJSON, pad } from "../lib/format";

/* ───────── YearPlan — the whole teaching year for ONE subject·class, at a glance ─────────
 * This is the restructured "allocation report" (founder decision, 2026-07-21): a LIVING mobile
 * view, never a PDF. It answers the one question My Lessons' per-chapter cards can't — "across
 * all my chapters and my finite annual periods, how does the year shape up, and how much have I
 * committed so far?" It reaches the teacher as the "Year Plan" pane of the My Lessons toggle, so
 * it inherits that tab's Subject·Class scope (this artifact is a class-level thing; it never sits
 * inside a chapter and there's nowhere else it belongs).
 *
 * What it deliberately does NOT show (the whole point of the restructure):
 *   • no competencies / competency weightages — those now live in the LP at chapter level;
 *   • no effort-index VALUES — an internal calibration signal, meaningless to a teacher. The
 *     index's information survives only as its consequence: raw periods (9 for Force vs 7 for
 *     Optics = "Force needs more time"), which is the value she can actually use.
 *
 * Two period figures, side by side:
 *   • Suggested — Aruvi's proposal: her annual budget distributed across chapters by the same
 *     effort/competency weight the allocator uses (largest-remainder, whole periods, sums to
 *     budget). Computed client-side so it always reconciles to the budget with no extra call.
 *   • Your plan — the periods she actually set when she prepared each lesson (prepared_periods
 *     from /plans). A class-level COMMITMENT, not classroom execution — so it stays honest and
 *     needs zero new input from her, and there is deliberately no "actual taught" column (that
 *     lives per-section on My Classes and Aruvi does not supervise it).
 *
 * The budget ledger (budget / committed / left) is the "must return" hook: pure arithmetic of her
 * own choices, updated whenever she prepares a lesson — reflection, never a verdict on her pace.
 *
 * Data: GET /subjects/{s}/{g}/chapters → {chapters:[{chapter_number,chapter_title,weight,
 * ncf_estimated_periods}], allocation_basis}; GET /plans/{s}/{g} → prepared + prepared_periods
 * per chapter; budget from readiness via annualBudgetPeriods().
 *
 * NOTE — duration combos (40m/60m split per chapter) are not shown yet: prepared_periods stores
 * a single total, so a per-chapter by-duration breakdown isn't available on the committed side.
 * Reinstating it is a fast-follow that needs markPrepared to persist periods_by_duration.
 *
 * Props: subjectName (display), sSlug, gSlug (slugs), readiness (page projection), onAllocate.
 */

// Largest-remainder apportionment: split `total` whole periods across `weights`, giving every
// remainder-ranked chapter one extra until the total is exactly used. Same method the backend
// allocator uses, so the client figure matches how periods actually get allocated.
function largestRemainder(total, weights) {
  const sum = weights.reduce((a, b) => a + b, 0);
  if (!total || sum <= 0) return weights.map(() => 0);
  const raw = weights.map((w) => (total * w) / sum);
  const base = raw.map(Math.floor);
  let rem = total - base.reduce((a, b) => a + b, 0);
  const order = raw
    .map((r, i) => ({ i, frac: r - Math.floor(r) }))
    .sort((a, b) => b.frac - a.frac);
  const out = base.slice();
  for (let k = 0; k < rem; k++) out[order[k % order.length].i] += 1;
  return out;
}

export default function YearPlan({ subjectName, sSlug, gSlug, readiness, onAllocate }) {
  const [chapters, setChapters] = useState(null); // null = loading, [] = none
  const [plans, setPlans] = useState([]);
  const [err, setErr] = useState(false);
  // The "Plan" summary is collapsible (like teacher notes): available to read, but collapsed by
  // default so it doesn't eat the frozen head on every visit.
  const [showPlan, setShowPlan] = useState(false);

  // Scoped fetch: chapters (weights + NCF estimate) and this teacher's prepared plans (for the
  // committed periods). Both are small, single calls per combo. Reset on subject/class change.
  useEffect(() => {
    if (!sSlug || !gSlug) return;
    let live = true;
    setChapters(null); setPlans([]); setErr(false);
    Promise.all([
      getJSON(`/subjects/${sSlug}/${gSlug}/chapters`),
      getJSON(`/plans/${sSlug}/${gSlug}`).catch(() => ({ plans: [] })),
    ])
      .then(([ch, pl]) => {
        if (!live) return;
        setChapters(Array.isArray(ch.chapters) ? ch.chapters : []);
        setPlans(Array.isArray(pl.plans) ? pl.plans : []);
      })
      .catch(() => { if (live) { setErr(true); setChapters([]); } });
    return () => { live = false; };
  }, [sSlug, gSlug]);

  const model = useMemo(() => {
    const chs = (chapters || [])
      .slice()
      .sort((a, b) => (a.chapter_number || 0) - (b.chapter_number || 0));

    // Committed ("Your plan") periods per chapter, from prepared plans. prepared_periods can be
    // null on legacy prepares — such a chapter counts as prepared (a dot) but adds nothing to the
    // committed total, so the ledger only ever reflects periods she actually set.
    const committedByCh = {};
    const preparedSet = new Set();
    (plans || []).forEach((p) => {
      if (!p.prepared) return;
      preparedSet.add(p.chapter_number);
      if (p.prepared_periods != null) committedByCh[p.chapter_number] = p.prepared_periods;
    });

    // Budget: her configured annual budget; fall back to the NCF year total when unset.
    const ncfSum = chs.reduce((s, c) => s + (c.ncf_estimated_periods || 0), 0);
    let budget = annualBudgetPeriods(readiness, sSlug, gSlug);
    if (!budget) budget = ncfSum || null;

    // Suggested per chapter: distribute the budget by weight; fall back to the NCF per-chapter
    // estimate when weights or budget are unavailable.
    const weights = chs.map((c) => (typeof c.weight === "number" && c.weight > 0 ? c.weight : 0));
    const wSum = weights.reduce((a, b) => a + b, 0);
    const sugByCh = {};
    if (budget && wSum > 0) {
      const dist = largestRemainder(budget, weights);
      chs.forEach((c, i) => { sugByCh[c.chapter_number] = dist[i]; });
    } else {
      chs.forEach((c) => { sugByCh[c.chapter_number] = c.ncf_estimated_periods ?? null; });
    }

    const rows = chs.map((c) => {
      const cn = c.chapter_number;
      const prepared = preparedSet.has(cn);
      const plan = committedByCh[cn] ?? null;
      const sug = sugByCh[cn] ?? null;
      return {
        n: cn,
        title: c.chapter_title || "",
        sug,
        plan,
        prepared,
        delta: plan != null && sug != null ? plan - sug : null,
      };
    });

    const committedTotal = Object.values(committedByCh).reduce((a, b) => a + b, 0);
    const sugTotal = rows.reduce((s, r) => s + (r.sug || 0), 0);
    const preparedCount = preparedSet.size;
    const left = budget != null ? budget - committedTotal : null;
    const pct = budget ? Math.max(0, Math.min(100, Math.round((committedTotal / budget) * 100))) : 0;

    return { rows, budget, committedTotal, sugTotal, preparedCount, left, pct, remaining: rows.length - preparedCount };
  }, [chapters, plans, readiness, sSlug, gSlug]);

  if (chapters === null) return <div className="yp-loading">Loading your year…</div>;
  if (err && !model.rows.length) return <div className="yp-empty">Couldn&rsquo;t load the year plan just now. Please try again.</div>;
  if (!model.rows.length) return <div className="yp-empty">No chapters found for {subjectName}.</div>;

  const { rows, budget, committedTotal, sugTotal } = model;
  const dash = <span className="yp-dash">&mdash;</span>;

  return (
    <div className="yp">
      {/* Frozen head — everything down to and including the Chapter/Suggested/Your-plan line stays
          put while the chapter rows scroll beneath it (sticks under My Lessons' own frozen header
          via the measured --mlp2-frozen-h). */}
      <div className="yp-head">
      {/* Executive summary — collapsible like teacher notes: readable on demand, collapsed by
          default (kicker "Plan"; no competency, no effort numbers). */}
      <div className={`yp-exec${showPlan ? " open" : ""}`}>
        <button type="button" className="yp-exec-h" onClick={() => setShowPlan((v) => !v)} aria-expanded={showPlan}>
          <span className="yp-exec-k">Plan</span>
          <span className={`yp-exec-chev${showPlan ? " open" : ""}`} aria-hidden="true">⌄</span>
        </button>
        {showPlan && (
          <p>
            Your teaching year at a glance — how{budget != null ? <> a budget of <b>{budget} periods</b></> : <> your periods</>} spread
            across all {rows.length} chapters. <b>Suggested periods</b> is Aruvi&rsquo;s proposal, giving heavier chapters more
            room. Each time you prepare a lesson you set your own periods for that chapter; those appear
            in <b>Your plan</b>, beside the suggestion, so you can see where you&rsquo;ve adjusted and how much of
            the year you&rsquo;ve committed. To know how Aruvi suggests, refer to Ask Aruvi time allocation section.
          </p>
        )}
      </div>

      {/* Column header — the last frozen line (its bottom border is "the line below the row"). */}
      <div className="yp-colhd">
        <div className="yp-c chap">Chapter</div>
        <div className="yp-c">Suggested periods</div>
        <div className="yp-c">Your plan</div>
      </div>
      </div>{/* /yp-head */}

      {/* Chapter rows (scroll beneath the frozen head) */}
      <div className="yp-rows">
        {rows.map((r) => (
          <div className={`yp-row${r.prepared ? "" : " pend"}`} key={r.n}>
            <div className="yp-cell-ch">
              <span className="yp-cn">{pad(r.n)}</span>
              <span className="yp-cname">{r.title}</span>
            </div>
            <div className="yp-sug">{r.sug != null ? r.sug : dash}</div>
            <div className="yp-planw">
              {r.plan != null ? (
                <span className="yp-plan">{r.plan}</span>
              ) : r.prepared ? (
                <span className="yp-plan yp-set">set</span>
              ) : (
                <><span className="yp-plan">{dash}</span><span className="yp-pend">not yet</span></>
              )}
            </div>
          </div>
        ))}
      </div>

      {/* Totals */}
      <div className="yp-tot">
        <span className="yp-tot-l">Total periods</span>
        <span className="yp-tot-n sug">{sugTotal}</span>
        <span className="yp-tot-n plan">{committedTotal}</span>
      </div>
    </div>
  );
}
