"use client";
import { useEffect, useMemo, useRef, useState } from "react";
import { API, getJSON, pad, pretty, userKey, withUser } from "../lib/format";
import { pullSectionState, readLocalSection } from "../lib/sectionState";
import LessonView from "./LessonView";
import YearPlan from "./YearPlan";
import { RollWheel } from "./wheels";

/* ───────── MyLessonPlans — the lesson library, one class at a time (redesigned 2026-07-03) ─────────
 * A teacher comes here with ONE class in mind ("what's left to prepare for VI Science"), so the
 * tab scopes to a single subject·grade and gives the whole body to that list. It mirrors My
 * Classes structurally: "Your lessons" at the dash-title size, then Subject + Grade as the two
 * first-run RollWheels (only what she teaches), pinned in a frozen header while the lesson list
 * scrolls beneath. Cards reuse the .sc-card sizing so the two tabs read as one family.
 *
 * Card colour = teaching lifecycle, lifted from section to lesson (the basis chosen 2026-07-03):
 *   • sage rail  — no section has taken this chapter yet ("ready to teach", on the shelf)
 *   • green (st-going) — ANY section is mid-chapter on it ("teaching now" wins — it's live)
 *   • clay (st-done)   — every engaged section has finished and none is live
 * The status line is EXHAUSTIVE and single-colour: "Completed 6A, 6C · Teaching now 6B, 6D"
 * (completed first). No per-section drill-down here — that's the section card's job; tapping a
 * card just opens the READ-ONLY lesson plan (PDF attachment later). Per-section state is read
 * from the same server-backed section cache My Classes writes (readLocalSection), so the two
 * tabs always agree.
 *
 * Data: readiness stores subject as DISPLAY NAME ("Science") and grade as UPPERCASE ROMAN ("VI");
 * the plans API uses SLUGS. We convert at the boundary. Section tags are already stored as "6A".
 *
 * Props:
 *   readiness  — page projection carrying .subjects[] (canonical).
 *   onAllocate — (subjectSlug, gradeSlug) => void; opens Generate to prepare a new lesson.
 */

const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const gradeSlug = (g) => (g || "").toLowerCase();
// Display abbreviation for the compact Subject wheel: the full "The World Around Us" is shown as
// "TWAU". Only the visible label is shortened — the subject id/slug used everywhere else is the
// full name, so selection, plans, and API calls are unaffected.
const subjectLabel = (name) => (/world around us/i.test(name || "") ? "TWAU" : name);
// The teacher's word is "Class", shown as a plain number — never "Grade", never Roman numerals.
// Readiness still STORES the grade as Roman ("VI"); we convert to the display number only here.
const CLASS_NUM = { iii: 3, iv: 4, v: 5, vi: 6, vii: 7, viii: 8, ix: 9, x: 10 };
const classNum = (g) => CLASS_NUM[(g || "").toLowerCase()] ?? (g || "");

// Persist the chosen Subject + Class so the tab REMEMBERS where she was when she toggles over to
// My Classes and back (she flips between the two to pick chapters — resetting to the first
// subject/class each time is exactly the annoyance to avoid). localStorage → survives the
// unmount/remount on tab switch AND a full refresh.
// Scoped by user ID (A3, 2026-07-06) so the remembered Subject/Class of one teacher never
// carries into another's session on a shared browser. Resolved inside the component (per
// signed-in user), not as a module constant.
const lsGet = (k) => { if (typeof window === "undefined") return null; try { return window.localStorage.getItem(k); } catch { return null; } };
const lsSet = (k, v) => { if (typeof window === "undefined") return; try { window.localStorage.setItem(k, v); } catch {} };

/* Line-icons, currentColor stroke so they inherit the warm-paper palette. */
const ArchiveIcon = ({ size = 18 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor"
       strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <rect x="3" y="4" width="18" height="4" rx="1" />
    <path d="M5 8v11a1 1 0 0 0 1 1h12a1 1 0 0 0 1-1V8" />
    <path d="M10 12h4" />
  </svg>
);
// The SAME archive box, but OPEN — the lid swung a full 90° UP so it stands vertical, hinged at
// the box's back corner. Shown when you're inside the archive so the icon reads as "the box is
// open, you're in it"; tapping it closes it back to your lessons.
const OpenArchiveIcon = ({ size = 18 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor"
       strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <rect x="6.4" y="12" width="12.2" height="8" rx="1.4" />
    <rect x="3.4" y="2.6" width="3.2" height="9.4" rx="1" />
    <path d="M10.8 16h4" />
  </svg>
);

/* Report line-icon (a document with lines) — the only glyph in the flow; the modal itself is
   icon-free by design. */
const ReportIcon = ({ size = 17 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor"
       strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z" />
    <path d="M14 3v5h5" /><path d="M9 13h6" /><path d="M9 17h6" />
  </svg>
);

/* Year-Plan glyph — varying-length horizontal bars, reading as "periods spread across chapters"
   (an allocation/plan symbol, deliberately NOT a calendar). Sits at the right of the title row. */
const YearPlanIcon = ({ size = 22 }) => (
  <svg viewBox="0 0 24 24" width={size} height={size} fill="none" stroke="currentColor"
       strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M4 6h15" /><path d="M4 12h9" /><path d="M4 18h12" />
  </svg>
);

const REPORT_COMPS = [
  { id: "lesson", title: "Lesson Plan", desc: "Teaching plan, activities, steps and resources" },
  { id: "assessment", title: "Assessment", desc: "Questions and instructions" },
  { id: "integrated", title: "Lesson Plan + Assessment", desc: "Teaching plan together with assessment" },
];

/* Reports modal (2026-07-17) — the LPA/report download surface, per our placement decision:
 * opened from the report icon at the bottom-left of a My Lessons plan card (subject·class·chapter,
 * section-agnostic). Single-select composition (Lesson Plan default · Assessment · Lesson Plan +
 * Assessment); the "include answers" tick appears ONLY for the two that contain assessment and
 * defaults off — the answer layer is a separate server-side render (answers=1), so a clean copy
 * can never carry answers. Format PDF (default) or Word. Preview renders the PDF inline; Download
 * fetches the CHOSEN format. Served by GET /api/plans/{subject}/{grade}/{filename}/export/{kind}. */
function ReportModal({ sSlug, gSlug, filename, onClose }) {
  const [comp, setComp] = useState("lesson");
  const [answers, setAnswers] = useState(false);
  const [fmt, setFmt] = useState("pdf");
  const [busy, setBusy] = useState(false);
  const showAnswers = comp === "assessment" || comp === "integrated";

  const buildUrl = (format) => {
    let url = `${API}/api/plans/${sSlug}/${gSlug}/${filename}/export/${comp}?format=${format}`;
    if (showAnswers && answers) url += "&answers=1";
    return url;
  };

  // Download the report as a file via a blob + `download` attribute. The download attribute means
  // the browser SAVES rather than navigates, so Aruvi stays available (no trap) — including in the
  // Home-Screen PWA. On desktop it lands in Downloads; on iPhone in Files, where you open and share.
  // KNOWN iOS LIMIT: over plain http, iOS references the saved file by a blob: URL, so when you open
  // it and share, it may attach that link instead of the file. Sharing the actual file needs HTTPS
  // (the Web Share file API). There is no http workaround that both avoids the trap AND shares the
  // file — that trade-off is enforced by iOS.
  const download = async () => {
    setBusy(true);
    try {
      const resp = await fetch(buildUrl(fmt), withUser({ method: "GET" }));
      if (!resp.ok) throw new Error(`HTTP ${resp.status}`);
      const blob = await resp.blob();
      const cd = resp.headers.get("content-disposition") || "";
      const m = cd.match(/filename="([^"]+)"/);
      const name = m ? m[1] : `report.${fmt === "pdf" ? "pdf" : "docx"}`;
      const u = URL.createObjectURL(blob);
      const a = document.createElement("a");
      a.href = u; a.download = name;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(() => URL.revokeObjectURL(u), 8000);
      onClose();
    } catch (e) {
      alert(`Couldn't create the report.\n\n${e?.message || "Is the Aruvi engine running on :8000?"}`);
    } finally { setBusy(false); }
  };

  return (
    <div className="rpt-overlay" onClick={(e) => { e.stopPropagation(); onClose(); }}>
      <div className="rpt-modal" onClick={(e) => e.stopPropagation()}>
        <div className="rpt-hd">
          <span className="rpt-title">Reports</span>
          <button className="rpt-x" onClick={onClose} aria-label="Close">✕</button>
        </div>
        <p className="rpt-sub">Create a report of this lesson or its assessment.</p>

        <div className="rpt-opts">
          {REPORT_COMPS.map((c) => {
            const on = comp === c.id;
            const canAns = c.id === "assessment" || c.id === "integrated";
            return (
              <div key={c.id} className={`rpt-opt${on ? " on" : ""}`} role="button" tabIndex={0}
                onClick={() => setComp(c.id)}>
                <div className="rpt-opt-row">
                  <span className="rpt-opt-body">
                    <span className="rpt-opt-t">{c.title}</span>
                    <span className="rpt-opt-d">{c.desc}</span>
                  </span>
                  <span className="rpt-radio" aria-hidden="true" />
                </div>
                {on && canAns ? (
                  // The answers tick lives INSIDE the chosen box (Assessment / LP+A only) —
                  // stops propagation so toggling it never re-fires the card's select.
                  <label className="rpt-ans" onClick={(e) => e.stopPropagation()}>
                    <input type="checkbox" checked={answers}
                      onChange={(e) => setAnswers(e.target.checked)} />
                    <span className="rpt-ans-t">Include answers / model responses</span>
                  </label>
                ) : null}
              </div>
            );
          })}
        </div>

        <div className="rpt-kicker">Format</div>
        <div className="rpt-fmt">
          <button type="button" className={`rpt-fmt-btn${fmt === "pdf" ? " on" : ""}`} onClick={() => setFmt("pdf")}>PDF</button>
          <button type="button" className={`rpt-fmt-btn${fmt === "docx" ? " on" : ""}`} onClick={() => setFmt("docx")}>Word</button>
        </div>

        <div className="rpt-foot">
          <button className="rpt-btn" onClick={onClose} type="button">Cancel</button>
          <button className="rpt-btn rpt-primary" onClick={download} disabled={busy} type="button">
            {busy ? "Preparing…" : `Download ${fmt === "pdf" ? "PDF" : "Word"}`}
          </button>
        </div>
      </div>
    </div>
  );
}

/* The report trigger on a card — a small icon at the bottom-left; opens the Reports modal.
   `dataTour` tags this button as the guided tour's step-4 anchor on the tour's target card. */
function ReportButton({ sSlug, gSlug, filename, dataTour }) {
  const [open, setOpen] = useState(false);
  return (
    <>
      <button className="sc-report" data-tour={dataTour} onClick={(e) => { e.stopPropagation(); setOpen(true); }}
        aria-label="Create a report" title="Reports"><ReportIcon /></button>
      {open ? (
        <ReportModal sSlug={sSlug} gSlug={gSlug} filename={filename} onClose={() => setOpen(false)} />
      ) : null}
    </>
  );
}

export default function MyLessonPlans({ readiness, onAllocate, tourStep }) {
  const LS_SUBJECT = userKey("mylessons_subject");
  const LS_CLASS = userKey("mylessons_class");
  const LS_PANE = userKey("mylessons_pane");
  const subjects = useMemo(() => (readiness && readiness.subjects) || [], [readiness]);

  // Subject in focus (by display name); class in focus (uppercase Roman). RESTORE the last choice
  // from localStorage (see LS_* above); fall back to the first taught subject/class on first ever
  // visit. A stale saved class is harmless — the RollWheel self-corrects if it isn't offered.
  const [activeSubject, setActiveSubject] = useState(() => {
    const saved = lsGet(LS_SUBJECT);
    if (saved && subjects.some((s) => s.name === saved)) return saved;
    return subjects[0] ? subjects[0].name : "";
  });
  const [activeGrade, setActiveGrade] = useState(() => {
    // Default to a class she actually TEACHES for the initial subject. A stale saved class — from
    // another user in this same browser, or left over from before a profile delete/re-run — must
    // NOT strand My Lessons on a class where her prepared lessons don't live (the "lesson not in My
    // Lessons" bug, kumar23 2026-07-06: prepared english/iii was on disk, but My Lessons opened on a
    // stale Class 7 and showed "no lessons prepared"). Derived from the current server profile, not
    // trusted from the persisted value. She can still browse other classes via the wheel afterwards.
    const savedSub = lsGet(LS_SUBJECT);
    const s0 = (savedSub && subjects.find((s) => s.name === savedSub)) || subjects[0] || null;
    const taught = (s0 && s0.grades ? s0.grades : []).map((g) => g.grade);
    const saved = lsGet(LS_CLASS);
    if (saved && taught.includes(saved)) return saved;
    return taught[0] || "";
  });
  // Plans keyed `${subjectSlug}/${gradeSlug}` -> array (or undefined while loading).
  const [plansByKey, setPlansByKey] = useState({});
  const [openPlan, setOpenPlan] = useState(null);   // { view }
  const [opening, setOpening] = useState(false);
  const [, setTick] = useState(0);                  // bumped after a section-state sync → re-read
  // Active vs Archived view over the SAME list. Archive is a per-tenant FLAG the server sets
  // (plan.archived); there is no hard delete. "active" is the default — a teacher lives here.
  const [view, setView] = useState("active");
  // Which pane is showing: the prepared-chapter card list ("lessons") or the whole-year "plan"
  // (YearPlan) — the same Subject·Class scope, two lenses. Persisted per user so a flip survives
  // the unmount/remount on tab switch and a full refresh (mirrors LS_SUBJECT/LS_CLASS above).
  const [pane, setPane] = useState(() => (lsGet(LS_PANE) === "plan" ? "plan" : "lessons"));
  const onPane = (p) => { setPane(p); lsSet(LS_PANE, p); };
  const [toast, setToast] = useState(null);         // { kind:"ok"|"block", text } | null

  const current = subjects.find((s) => s.name === activeSubject) || subjects[0] || null;
  const grades = useMemo(() => (current && current.grades) || [], [current]);   // HER enrolled classes
  // The Class wheel is RESTRICTED to the classes she has enrolled for this subject in her profile
  // (2026-07-06). It never offers a class she hasn't set up — a class shows here only once she adds
  // it (via the "add another class" flow / teaching profile). Every offered class therefore has
  // sections that drive the per-section status.
  const taughtGradeObj = grades.find((g) => g.grade === activeGrade) || null;

  const sSlug = current ? subjectSlug(current.name) : "";
  const gSlug = gradeSlug(activeGrade);
  const key = sSlug && gSlug ? `${sSlug}/${gSlug}` : "";
  const plans = key ? plansByKey[key] : undefined;

  // Keep the active subject AND class valid as the profile changes. The class is now restricted to
  // her enrolled classes, so a stale saved class (from a prior profile, another user in this
  // browser, or the old superset wheel) must be snapped back to one she actually teaches — never
  // left pointing at a class that's no longer in her profile.
  useEffect(() => {
    if (!subjects.length) return;
    const s = subjects.some((x) => x.name === activeSubject)
      ? subjects.find((x) => x.name === activeSubject)
      : subjects[0];
    if (s.name !== activeSubject) {
      const g0 = s.grades && s.grades[0] ? s.grades[0].grade : "";
      setActiveSubject(s.name); lsSet(LS_SUBJECT, s.name);
      setActiveGrade(g0); lsSet(LS_CLASS, g0);
      return;
    }
    const taught = (s.grades || []).map((g) => g.grade);
    if (!taught.includes(activeGrade)) {
      const g0 = taught[0] || "";
      setActiveGrade(g0); lsSet(LS_CLASS, g0);
    }
  }, [subjects, activeSubject, activeGrade]);

  // Fetch the saved plans for the scoped subject·grade (a single small call per combo, cached).
  useEffect(() => {
    if (!key) return;
    setPlansByKey((prev) => (key in prev ? prev : { ...prev, [key]: undefined }));
    getJSON(`/plans/${sSlug}/${gSlug}`)
      .then((d) => setPlansByKey((prev) => ({ ...prev, [key]: d.plans || [] })))
      .catch(() => setPlansByKey((prev) => ({ ...prev, [key]: [] })));
  }, [key, sSlug, gSlug]);

  // Reconcile this grade's section teaching-state from the server into the localStorage cache so
  // the status lines match what the teacher set on My Classes / another device. Re-syncs on load,
  // on tab focus/visibility, and on a light interval — same pattern as My Classes. Skipped while a
  // plan is open so an in-flight read is never interrupted.
  // Refs to publish the frozen header's height (see effect below) so the Year Plan's own head can
  // stick directly beneath it.
  const rootRef = useRef(null);
  const frozenRef = useRef(null);

  const busyRef = useRef(false);
  busyRef.current = !!openPlan;
  useEffect(() => {
    const keys = (taughtGradeObj ? taughtGradeObj.sections || [] : [])
      .map((s) => `${sSlug}_${gSlug}_${s.tag}`).filter(Boolean);
    if (!keys.length) return;
    let live = true;
    const sync = () => {
      if (!live || busyRef.current) return;
      pullSectionState(keys).then(() => { if (live) setTick((t) => t + 1); });
    };
    sync();
    const onVis = () => { if (document.visibilityState === "visible") sync(); };
    document.addEventListener("visibilitychange", onVis);
    window.addEventListener("focus", sync);
    const iv = setInterval(() => { if (document.visibilityState === "visible") sync(); }, 20000);
    return () => {
      live = false;
      document.removeEventListener("visibilitychange", onVis);
      window.removeEventListener("focus", sync);
      clearInterval(iv);
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [sSlug, gSlug]);

  const onSubject = (name) => {
    setActiveSubject(name);
    lsSet(LS_SUBJECT, name);
    const s = subjects.find((x) => x.name === name);
    const g = s && s.grades && s.grades[0] ? s.grades[0].grade : "";
    setActiveGrade(g);
    lsSet(LS_CLASS, g);
  };
  const onGrade = (g) => { setActiveGrade(g); lsSet(LS_CLASS, g); };

  const openLesson = async (p) => {
    setOpening(true);
    try {
      const view = (await getJSON(`/plans/${sSlug}/${gSlug}/${p.filename}/view`)).view;
      setOpenPlan({ view, plan: p });
    } finally { setOpening(false); }
  };

  // Guided-tour orchestration (steps 3–7 live on this view: 3 the lesson row, 4 the report button,
  // 5 the archive button, 6 "open the lesson" — same card as 3, hand on it — and 7 the open
  // preview). The guide DRIVES the preview: on step 7 it opens the first prepared lesson (the hand
  // "clicked" the card at step 6); on any other step — Back to 3/4/5/6, or Back into this view from
  // step 8 — the state converges idempotently. The first prepared, unarchived plan is the same one
  // the list's top row shows (steps 3 and 6's spotlight).
  useEffect(() => {
    if (tourStep == null) return;
    if (tourStep === 7) {
      if (!openPlan && !opening) {
        const p = tourPlanOf();   // the most recently prepared lesson (see below)
        if (p) openLesson(p);
      }
    } else if (openPlan) setOpenPlan(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tourStep, plans, openPlan, opening]);
  // Exhaustive per-section state for one chapter: which sections completed it, which are on it now.
  // A section counts only if it's currently tracking THIS chapter (current_chapter === filename).
  const statusFor = (plan) => {
    const completed = [];
    const live = [];
    (taughtGradeObj ? taughtGradeObj.sections || [] : []).forEach((s) => {
      const st = readLocalSection(`${sSlug}_${gSlug}_${s.tag}`);
      if (st.chapter && st.chapter === plan.filename) (st.done ? completed : live).push(s.tag);
    });
    return { completed, live };
  };

  // A plan is "attached" if any section is currently teaching or has completed it — the same
  // signal that colours the card. Attached plans are BLOCKED from archiving (the teacher would
  // lose the class's pointer/context), so archive is only ever offered on detached plans.
  const isAttached = (plan) => {
    const { completed, live } = statusFor(plan);
    return completed.length > 0 || live.length > 0;
  };

  // The guided tour's plan: her most recently PREPARED lesson — "the lesson you just now
  // generated" — never an arbitrary library entry (/plans returns the whole shared library;
  // gp[0] once made the guide walk a chapter she never generated). Steps 3 and 6 (row/card
  // spotlight) and 7 (auto-open preview) all key off this, so they can never diverge.
  const tourPlanOf = () => {
    const arr = (Array.isArray(plans) ? plans : [])
      .filter((p) => (p.prepared || isAttached(p)) && !p.archived)
      .sort((a, b) => String(b.prepared_at || "").localeCompare(String(a.prepared_at || "")));
    return arr[0] || null;
  };
  const tourPlan = tourStep != null ? tourPlanOf() : null;

  // Flip a plan's archived flag in local state (optimistic) so it moves between the two views
  // instantly, before the server round-trip resolves.
  const setArchivedFlag = (filename, val) => {
    setPlansByKey((prev) => {
      const arr = prev[key];
      if (!Array.isArray(arr)) return prev;
      return {
        ...prev,
        [key]: arr.map((p) =>
          p.filename === filename
            ? { ...p, archived: val, archived_at: val ? new Date().toISOString() : null }
            : p),
      };
    });
  };

  const body = (p) => ({ subject: sSlug, grade: gSlug, filename: p.filename });

  const archivePlan = (p, e) => {
    if (e) e.stopPropagation();
    // Safety only — the archive icon is never rendered for an attached plan, so this can't be
    // reached from the UI. No warning path: attachment simply removes the affordance.
    if (isAttached(p)) return;
    setArchivedFlag(p.filename, true);
    setToast({ kind: "ok", text: "Moved to Archive — find it in the box above." });
    fetch(`${API}/plan-archive`, withUser({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body(p)),
    })).then((r) => { if (!r.ok) throw new Error(); }).catch(() => {
      setArchivedFlag(p.filename, false);   // revert the optimistic move
      setToast({ kind: "block", text: "Couldn't archive just now — please try again." });
    });
  };

  const restorePlan = (p, e) => {
    if (e) e.stopPropagation();
    setArchivedFlag(p.filename, false);
    setToast({ kind: "ok", text: "Restored to your lessons." });
    fetch(`${API}/plan-archive`, withUser({
      method: "DELETE",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body(p)),
    })).then((r) => { if (!r.ok) throw new Error(); }).catch(() => {
      setArchivedFlag(p.filename, true);
      setToast({ kind: "block", text: "Couldn't restore just now — please try again." });
    });
  };

  // Auto-dismiss the toast after a few seconds.
  useEffect(() => {
    if (!toast) return;
    const t = setTimeout(() => setToast(null), 3200);
    return () => clearTimeout(t);
  }, [toast]);

  // Publish the sticky frozen header's live height as --mlp2-frozen-h so the Year Plan's own head
  // (exec + tiles + column line) can stick RIGHT BELOW it — the plan then freezes down to the
  // Chapter/Suggested/Your-plan line while its rows scroll. Re-measures on any header resize.
  useEffect(() => {
    const fz = frozenRef.current, root = rootRef.current;
    if (!fz || !root) return;
    const set = () => root.style.setProperty("--mlp2-frozen-h", `${fz.offsetHeight}px`);
    set();
    if (typeof ResizeObserver === "undefined") return;
    const ro = new ResizeObserver(set);
    ro.observe(fz);
    return () => ro.disconnect();
  });

  if (opening) return <div className="spin">Opening plan…</div>;
  if (openPlan) {
    // READ-ONLY preview. The old "Attach to a class" CTA + section chooser are RETIRED
    // (2026-07-06): attaching happens ONLY via the "+" on a My Classes section card → the
    // track-a-chapter window — one true way, and the tour teaches exactly that.
    return <LessonView view={openPlan.view} onExit={() => setOpenPlan(null)} preview />;
  }

  if (!current) {
    return <div className="mlp-empty">No subjects set up yet. Finish setup in My Classes to see your lessons here.</div>;
  }

  // Subject filter, alphabetical by name (profile order is arbitrary — a stable A–Z list is easier
  // to scan). Copy before sort so the source subjects[] order is untouched.
  const subjectItems = subjects
    .map((s) => ({ id: s.name, label: subjectLabel(s.name) }))
    .sort((a, b) => a.label.localeCompare(b.label));
  // ONLY the classes she has enrolled for this subject, low-to-high — never the content superset.
  const gradeItems = grades
    .map((g) => g.grade)
    .sort((a, b) => classNum(a) - classNum(b))
    .map((g) => ({ id: g, label: `${classNum(g)}` }));

  const prepareCTA = (
    <div className="mlp-allocate">
      <span className="mlp-allocate-q">Need a chapter you don&rsquo;t have yet?</span>
      <button className="mlp-allocate-btn prepare-cta" onClick={() => onAllocate && onAllocate(sSlug, gSlug)}>
        Prepare a new lesson →
      </button>
    </div>
  );

  // My Lessons shows ONLY what this teacher has prepared — never the whole shared sample library
  // (live gen is deferred, so the saved-plan content is identical for every teacher). The server
  // sets `prepared` per tenant; a plan any section is attached to counts as prepared too, so a
  // lesson a class is actively teaching can never vanish from the repository even if its prepared
  // write was lost. Un-prepared sample plans are hidden entirely (the empty-state copy already
  // reads "no lesson plans prepared … yet").
  const preparedPlans = (Array.isArray(plans) ? plans : []).filter((p) => p.prepared || isAttached(p));
  // Split the prepared list into the two views by the server-set archived flag (archive is a
  // flag, not a separate fetch). Chips only appear once something is archived — no clutter before.
  const allPlans = preparedPlans;
  const activePlans = allPlans.filter((p) => !p.archived);
  const archivedPlans = allPlans.filter((p) => p.archived);
  const hasArchived = archivedPlans.length > 0;
  const effView = hasArchived ? view : "active";   // auto-fall-back when nothing's archived
  const shown = effView === "archived" ? archivedPlans : activePlans;

  return (
    <div className="mlp2" ref={rootRef}>
      <div className="mlp2-frozen" ref={frozenRef}>
        <div className="mlp2-titlerow">
          <div className="mlp2-titleleft">
            <h1 className="mlp2-title">{pane === "plan" ? "Year Plan" : effView === "archived" ? "Archive" : "Your lessons"}</h1>
            {/* Year-Plan toggle — sits right beside the title; hidden while the archive is open,
                and back once Your lessons is active. Toggles the whole-year pane. */}
            {!(pane === "lessons" && effView === "archived") && (
              <button className={`mlp2-yearbtn${pane === "plan" ? " on" : ""}`}
                onClick={() => onPane(pane === "plan" ? "lessons" : "plan")}
                aria-label={pane === "plan" ? "Back to your lessons" : "Year plan"}
                title={pane === "plan" ? "Your lessons" : "Year plan"}>
                <YearPlanIcon size={24} />
              </button>
            )}
          </div>
          {/* Archive control stays on the right of the row. */}
          {pane === "plan" ? null : effView === "archived" ? (
            // Open box = you're inside the archive; tapping it closes the box and drops you back
            // to your lessons (the one, symmetric way in and out).
            <button className="mlp2-archfolder open" onClick={() => setView("active")}
              aria-label="Close archive, back to your lessons" title="Back to your lessons">
              <OpenArchiveIcon size={22} />
              <span className="mlp2-archcount">{archivedPlans.length}</span>
            </button>
          ) : hasArchived ? (
            <button className="mlp2-archfolder" onClick={() => setView("archived")}
              aria-label={`Open archive (${archivedPlans.length})`} title="Archived lessons">
              <ArchiveIcon size={22} />
              <span className="mlp2-archcount">{archivedPlans.length}</span>
            </button>
          ) : null}
        </div>
        <div className="mlp2-wheels">
          <div className="mlp2-wcol">
            {subjectItems.length > 1 ? (
              <RollWheel items={subjectItems} value={activeSubject} onChange={onSubject} ariaLabel="Subject" large rowPx={72} fit peek />
            ) : (
              <div className="mlp2-static">{subjectLabel(current.name)}</div>
            )}
          </div>
          <div className="mlp2-wcol">
            {gradeItems.length > 1 ? (
              <RollWheel items={gradeItems} value={activeGrade} onChange={onGrade} ariaLabel="Class" large rowPx={72} peek />
            ) : (
              <div className="mlp2-static">Class {classNum(activeGrade)}</div>
            )}
          </div>
        </div>
      </div>

      {pane === "plan" ? (
        <YearPlan subjectName={current.name} sSlug={sSlug} gSlug={gSlug} readiness={readiness} onAllocate={onAllocate} />
      ) : (
      <>
      {plans === undefined ? (
        <div className="mlp-loading">Loading plans…</div>
      ) : shown.length === 0 ? (
        <div className="mlp2-emptybody">
          {effView === "archived"
            ? "Nothing archived here."
            : hasArchived
              ? `Every prepared lesson for ${pretty(sSlug)} · Class ${classNum(activeGrade)} is archived.`
              : `There are no lesson plans prepared for ${pretty(sSlug)} · Class ${classNum(activeGrade)} yet.`}
        </div>
      ) : (
        <div className="sc-list">
          {shown.map((p, pi) => {
            const { completed, live } = statusFor(p);
            const cls = effView === "archived"
              ? "mlp2-arch"
              : live.length ? "st-going" : completed.length ? "st-done" : "mlp2-shelf";
            // The guided tour's target card (the just-generated lesson). Steps 4/5 ring its
            // report/archive buttons — tagged only on this card and only at the matching step.
            const isTourCard = tourPlan && p.filename === tourPlan.filename;
            return (
              <div className={`sc-card ${cls}`} key={p.filename} onClick={() => openLesson(p)}
                data-tour={(tourStep === 3 || tourStep === 6) && tourPlan && p.filename === tourPlan.filename ? "lesson-first" : undefined}>
                <div className="sc-tag">{pad(p.chapter_number)}</div>
                <div className="sc-body">
                  <div className="sc-title">{p.chapter_title}</div>
                  {effView === "archived" ? (
                    <div className="mlp2-ready">Archived</div>
                  ) : completed.length || live.length ? (
                    <div className="mlp2-status">
                      {completed.length > 0 && <span>Completed {completed.join(", ")}</span>}
                      {completed.length > 0 && live.length > 0 && <span className="sep">·</span>}
                      {live.length > 0 && <span>Teaching now {live.join(", ")}</span>}
                    </div>
                  ) : (
                    <div className="mlp2-ready">Ready to teach</div>
                  )}
                </div>
                {effView === "archived" ? (
                  <button className="mlp2-restore-btn" onClick={(e) => restorePlan(p, e)}
                    aria-label={`Restore ${p.chapter_title}`}>Restore</button>
                ) : (
                  <>
                    {/* Archive in the top-right corner; report trigger in the bottom-right. Attached
                        plans can't be archived, so that control is simply absent for them. */}
                    {!isAttached(p) ? (
                      <button className="mlp2-iconbtn archive" onClick={(e) => archivePlan(p, e)}
                        aria-label={`Archive ${p.chapter_title}`} title="Archive"
                        data-tour={isTourCard && tourStep === 5 ? "lesson-archive" : undefined}>
                        <ArchiveIcon />
                      </button>
                    ) : null}
                    <ReportButton sSlug={sSlug} gSlug={gSlug} filename={p.filename}
                      dataTour={isTourCard && tourStep === 4 ? "lesson-report" : undefined} />
                  </>
                )}
              </div>
            );
          })}
        </div>
      )}

      {prepareCTA}
      </>
      )}

      {toast && (
        <div className={`mlp2-toast ${toast.kind}`} role="status">{toast.text}</div>
      )}
    </div>
  );
}
