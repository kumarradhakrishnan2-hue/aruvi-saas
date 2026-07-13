"use client";
import { useEffect, useRef, useState } from "react";
import { getJSON, pretty, pad, classNum } from "../lib/format";
import { pullSectionState, bindSectionChapter, unbindSection } from "../lib/sectionState";
import { readHistory, recordHistory, hasHistory } from "../lib/sectionHistory";
import Readiness from "./Readiness";
import LessonView from "./LessonView";

const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const gradeSlug = (g) => (g || "").toLowerCase();

// Nudge glyph — a transparent, stroke-only ROUTE (start point → dotted path → destination):
// "I'll walk you through it". Deliberately not a filled emoji; inherits the pine of the nudge.
const RouteIcon = (
  <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor"
    strokeWidth="1.6" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <circle cx="6" cy="19" r="2.6" />
    <path d="M9.5 19h8a3.5 3.5 0 0 0 0-7h-11a3.5 3.5 0 0 1 0-7H15" strokeDasharray="3 3.4" />
    <circle cx="18" cy="5" r="2.6" />
  </svg>
);

// The standing "+" portal's glyph (founder, 2026-07-06): a plus RINGED by a circle, with a
// dot on each side outside the ring — "grow in every direction". Inherits pine.
const GrowIcon = (
  <svg viewBox="0 0 24 24" width="26" height="26" fill="none" stroke="currentColor"
    strokeLinecap="round" aria-hidden="true">
    <circle cx="12" cy="12" r="5.9" strokeWidth="1.5" />
    <path d="M12 8.9v6.2M8.9 12h6.2" strokeWidth="2.1" />
    <circle cx="12" cy="3.3" r="1.4" fill="currentColor" stroke="none" />
    <circle cx="12" cy="20.7" r="1.4" fill="currentColor" stroke="none" />
    <circle cx="3.3" cy="12" r="1.4" fill="currentColor" stroke="none" />
    <circle cx="20.7" cy="12" r="1.4" fill="currentColor" stroke="none" />
  </svg>
);

// Small "history" glyph (clock + counter-clockwise arrow) for the section card's history button.
const HistoryIcon = (
  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor"
    strokeWidth="2" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
    <path d="M3 3v5h5" />
    <path d="M3.05 13A9 9 0 1 0 6 5.3L3 8" />
    <path d="M12 7v5l3 2" />
  </svg>
);
// History-status → the label shown on the popup pill.
const HISTORY_LABEL = { ongoing: "Ongoing", completed: "Completed", untracked: "Untracked" };
// Back-compat: an earlier build stored the untracked status as "set_aside". Normalize legacy
// localStorage entries so they still render with a label + slate pill instead of a blank status.
const normStatus = (s) => (s === "set_aside" ? "untracked" : s);

/* ONE CARD PER subject·grade·section the teacher handles — across ALL subjects (walks the
 * canonical readiness.subjects[], not the single active projection). NO day derivation
 * (2026-07-02): My Classes is pointer-organized ("where did I stop?"), never day-organized —
 * the calendar was a category error against the section-pointer model (MEMORY.md). Each entry
 * carries the slugs + section tag so the card can look up that class's plans and pointer. */
function classesFromReadiness(readiness) {
  const subjects = (readiness && readiness.subjects) || [];
  const out = [];
  subjects.forEach((s) => {
    const sSlug = subjectSlug(s.name);
    (s.grades || []).forEach((g) => {
      const gSlug = gradeSlug(g.grade);
      (g.sections || []).forEach((sec) => {
        out.push({
          subjectName: s.name, subjectSlug: sSlug, grade: g.grade, gradeSlug: gSlug,
          sectionTag: sec.tag,
        });
      });
    });
  });
  return out;
}

export default function MyPlans({ subject, grade, ready, readiness, onReady, onNavigate, onEnterGenerate, user, onSignOut, pendingOpen, onConsumePending, pendingAttach, onConsumeAttach, onStartTour, tourActive, tourStep, onTourInfo, onExpandClasses, onProfilePortal }) {
  const [openPlan, setOpenPlan] = useState(null);  // { view, sectionKey } for LessonView
  const [loading, setLoading] = useState(false);
  const [setupStarted, setSetupStarted] = useState(false); // 2a welcome → grid flow gate
  const [growOpen, setGrowOpen] = useState(false); // the standing "+" portal's Subject·Class·Section chooser
  const [attachFor, setAttachFor] = useState(null); // { c, sectionKey } — "+" track-a-chapter picker
  const [untrackFor, setUntrackFor] = useState(null); // { c, sectionKey, plan } — "−" untrack confirm
  const [historyFor, setHistoryFor] = useState(null); // { c, sectionKey } — chapter-history popup
  const [, setSyncTick] = useState(0); // bumped after a server pull so cards re-read the refreshed cache
  // plans for EVERY subject·grade the teacher handles, keyed `${subjectSlug}/${gradeSlug}`.
  const [plansByKey, setPlansByKey] = useState({});

  // "Do you teach {subject} to other classes?" — ONE appearance, EVER (founder, 2026-07-06;
  // supersedes the per-subject 3-appearance budgets). The window shows exactly once: after the
  // first generation, once the guided tour is resolved (completed or skipped), pinned to the
  // first subject that has exactly one class. It stays up for THAT session until she uses it or
  // ✕'s it — either ending hands over to the standing "+" portal, which owns all further growth.
  // It never returns in a later session: an ignored appearance also counts as spent, and the "+"
  // unlocks instead. Reminding beyond this single moment is an irritation, not acquisition.
  // Bumping expandTick re-reads storage after a write (storage isn't reactive).
  const [expandTick, setExpandTick] = useState(0);

  // All classes across all subjects (one card per subject·grade·section).
  const classes = ready ? classesFromReadiness(readiness) : [];

  // Gate: show the invitations once the teacher is past onboarding — she COMPLETED the guided
  // tour, SKIPPED it (at inception or mid-way), or attached a lesson without ever taking it. Held
  // back only while the tour is still on offer OR running, so it never competes with "take the tour".
  //   • tourActive  → the walkthrough overlay is up.
  //   • onStartTour → page.jsx passes this ONLY while the tour is still offered (it becomes
  //     undefined the instant she Skips or finishes — both route through finishTour/tourDismissed).
  //     So `!onStartTour` == "she has resolved the tour this session (skipped or done)".
  //   • anyBoundTop → she attached a lesson (covers the never-offered / manual-attach path).
  const subjectsArr = (readiness && readiness.subjects) || [];
  const anyBoundTop = ready && classes.some((c) => {
    if (typeof window === "undefined") return false;
    try { return !!window.localStorage.getItem(`current_chapter_${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`); }
    catch { return false; }
  });
  const tourResolved = anyBoundTop || !onStartTour; // attached, or skipped/completed the tour
  const expandGateOpen = ready && !tourActive && tourResolved && !!onExpandClasses;

  // Storage: shown + subject are cross-session (localStorage — the single appearance is spent
  // forever, pinned to one subject); session + dismiss are session-scoped (sessionStorage —
  // "shown this session" keeps it up across tab-hops; ✕ hides it now, the plus flag is the
  // permanent part).
  const expKeys = {
    shown: `expand_shown_${user || ""}`,
    subject: `expand_subject_${user || ""}`,
    session: `expand_session_${user || ""}`,
    dismiss: `expand_dismiss_${user || ""}`,
  };
  const lsGet = (k) => { try { return window.localStorage.getItem(k); } catch { return null; } };
  const ssGet = (k) => { try { return window.sessionStorage.getItem(k); } catch { return null; } };

  // The one window to render (or null): never shown before → pin to the first one-class
  // subject; shown THIS session → keep showing the same pinned subject (until ✕/used);
  // shown in a PAST session → never again. `expandTick` is referenced so this recomputes
  // after storage writes.
  const _expandTickRef = expandTick; // eslint-disable-line no-unused-vars
  let expandTarget = null;
  if (typeof window !== "undefined" && expandGateOpen && ssGet(expKeys.dismiss) !== "1") {
    const oneClass = subjectsArr.filter((s) => (s.grades || []).length === 1);
    if (lsGet(expKeys.shown) !== "1") expandTarget = oneClass[0] || null;
    else if (ssGet(expKeys.session) === "1") {
      const slug = lsGet(expKeys.subject);
      expandTarget = oneClass.find((s) => subjectSlug(s.name) === slug) || null;
    }
  }

  // Spend the single appearance the first time the window actually renders.
  const expandTargetName = expandTarget ? expandTarget.name : null;
  useEffect(() => {
    if (typeof window === "undefined" || !expandTargetName) return;
    try {
      if (window.localStorage.getItem(expKeys.shown) !== "1") {
        window.localStorage.setItem(expKeys.shown, "1");
        window.localStorage.setItem(expKeys.subject, subjectSlug(expandTargetName));
        window.sessionStorage.setItem(expKeys.session, "1");
        setExpandTick((t) => t + 1);
      }
    } catch {}
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [expandTargetName, user]);

  const dismissExpand = () => {
    try { window.sessionStorage.setItem(expKeys.dismiss, "1"); } catch {}
    unlockPlus(); // resolving the window (✕) opens the standing "+" portal for good
    setExpandTick((t) => t + 1);
  };

  // The standing "+" profile portal (founder, 2026-07-06) — the gliding path to acquisition.
  // It appears the moment the ONE expand window is resolved, by any of its three endings:
  // (1) she used it — added another class and completed the flow (derived: any subject now has
  // >1 class); (2) she clicked ✕ (dismissExpand above); (3) she ignored it — the appearance was
  // spent in a past session and the window never returns. From then on it is PERMANENT (per-user
  // localStorage flag, sticky even if her profile later shrinks back to one class). After the
  // single window, ALL growth is pull, never push — further reminders are an irritation.
  // Placed BELOW the "Your classes are ready" box but ABOVE the section cards: classes
  // encompass new subjects too, so the portal governs the whole card list, never the welcome.
  const plusKey = `plus_portal_${user || ""}`;
  const plusFlagOn = () => { try { return window.localStorage.getItem(plusKey) === "1"; } catch { return false; } };
  const unlockPlus = () => { try { window.localStorage.setItem(plusKey, "1"); } catch {} };
  const plusUnlocked = (typeof window !== "undefined") && ready && (
    plusFlagOn()
    || subjectsArr.some((s) => (s.grades || []).length > 1)              // path 1: add-class completed
    || (lsGet(expKeys.shown) === "1" && ssGet(expKeys.session) !== "1")  // path 3: spent in a past session, ignored
  );
  // Make the unlock sticky the moment any path first derives true.
  useEffect(() => {
    if (plusUnlocked && !plusFlagOn()) unlockPlus();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [plusUnlocked]);
  // Never compete with the guided tour; needs the portal callback from page.jsx. EXCEPTION: the
  // tour's step 12 deliberately features this "+" (the grow portal), so it's surfaced then even
  // though the tour is active — the guide rings it and the transparent hand lands on it.
  const plusShow = !!onProfilePortal && (
    tourStep === 12 || (plusUnlocked && !tourActive && tourResolved)
  );

  // Fetch saved plans once per distinct subject·grade the teacher handles.
  useEffect(() => { setOpenPlan(null);
    if (!ready) return;
    const seen = new Set();
    classes.forEach((c) => {
      const key = `${c.subjectSlug}/${c.gradeSlug}`;
      if (seen.has(key)) return; seen.add(key);
      setPlansByKey((prev) => (key in prev ? prev : { ...prev, [key]: undefined }));
      getJSON(`/plans/${c.subjectSlug}/${c.gradeSlug}`)
        .then((d) => setPlansByKey((prev) => ({ ...prev, [key]: d.plans || [] })))
        .catch(() => setPlansByKey((prev) => ({ ...prev, [key]: [] })));
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ready, readiness]);

  // Reconcile section teaching-state (tracked chapter + pointer + done) from the SERVER into the
  // localStorage cache, so a device shows the same tracking/progress the teacher set elsewhere
  // (fixes the Chrome-vs-iPhone divergence). localStorage stays the optimistic cache; the server
  // row is authoritative here. Bump syncTick when done so the cards re-read the cache.
  //
  // Re-syncs WITHOUT a manual refresh: on load, whenever the tab regains focus / becomes visible
  // (the "I just switched to my iPhone" moment), and on a light interval while visible. We skip a
  // sync while a modal or the lesson view is open so an in-flight action is never clobbered.
  // Hold the section-state sync while an auto-attach (a lesson just generated from a section card)
  // is pending: the mount pull could otherwise read the server before the fresh binding's push
  // lands and clear it. Set during render so it's true before any effect runs.
  const autoBindHoldRef = useRef(false);
  autoBindHoldRef.current = !!pendingAttach;
  const uiBusyRef = useRef(false);
  uiBusyRef.current = !!(attachFor || untrackFor || openPlan || historyFor);
  useEffect(() => {
    if (!ready) return;
    const keys = classesFromReadiness(readiness)
      .map((c) => `${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`);
    if (!keys.length) return;
    let live = true;
    const sync = () => {
      if (!live || uiBusyRef.current || autoBindHoldRef.current) return;
      pullSectionState(keys).then(() => { if (live) setSyncTick((t) => t + 1); });
    };
    sync(); // initial reconcile
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
  }, [ready, readiness, user]);

  // Deep-link from Track (My Lesson Plans): open a specific SECTION's plan, pointer-enabled.
  // Uses the request's OWN subject/grade (My Week is no longer scoped to one subject·grade).
  useEffect(() => {
    if (!pendingOpen || !ready) return;
    const { subject: pSub, grade: pGrade, sectionTag, filename } = pendingOpen;
    if (!pSub || !pGrade || !filename) { onConsumePending && onConsumePending(); return; }
    const sectionKey = `${pSub}_${pGrade}_${sectionTag}`;
    let live = true;
    setLoading(true);
    getJSON(`/plans/${pSub}/${pGrade}/${filename}/view`)
      .then((d) => { if (live) setOpenPlan({ view: d.view, sectionKey }); })
      .catch(() => {})
      .finally(() => { if (live) { setLoading(false); onConsumePending && onConsumePending(); } });
    return () => { live = false; };
  }, [pendingOpen, ready, onConsumePending]);

  // Return from Prepare-a-lesson launched FROM a section card: the chapter was just prepared, so
  // AUTO-ATTACH it to that section (the card loads it directly — no popup). Refetch this class's
  // plans first so the card can render the chapter title + progress rail. The sync hold above
  // keeps the mount pull from clearing the fresh binding before its push lands.
  useEffect(() => {
    if (!pendingAttach || !ready) return;
    const { subject: pSub, grade: pGrade, sectionTag, filename } = pendingAttach;
    if (!pSub || !pGrade || !sectionTag || !filename) { onConsumeAttach && onConsumeAttach(); return; }
    const key = `${pSub}/${pGrade}`;
    const sectionKey = `${pSub}_${pGrade}_${sectionTag}`;
    let live = true;
    getJSON(`/plans/${pSub}/${pGrade}`)
      .then((d) => { if (live) setPlansByKey((prev) => ({ ...prev, [key]: d.plans || [] })); })
      .catch(() => {})
      .finally(() => {
        if (!live) return;
        bindSectionChapter(sectionKey, filename);   // auto-attach: localStorage + server push
        setSyncTick((t) => t + 1);                  // re-read the cache → card shows the chapter
        onConsumeAttach && onConsumeAttach();
      });
    return () => { live = false; };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [pendingAttach, ready]);

  /* ── Guided-tour orchestration (steps 5–12 live on this view; 13 steps total, 2026-07-09) ──
   * Step 12 features the big "+" grow portal on the My Classes home (no bound/popup change — the
   * card stays attached, the popup closes; plusShow surfaces the "+" for the ring + hand).
   * The tour's TARGET is the first class that already has a prepared plan (the first-run case:
   * exactly one lesson, generated for the section fan-out's subject·grade). All tour moves are
   * IDEMPOTENT and keyed off the numeric tourStep, so Next AND Back both land on a consistent
   * state:  ≤6 unbound (Back from 7 undoes the attach) · 6 the track-a-chapter popup is open
   * (the picker moment — mirrors the app's always-through-the-window attach) · ≥7 bound (the
   * REAL attach — the activation) · 8–9 the tracking lesson view is open · 10–11 the card DEMOS
   * the completed state (render-only — her real pointer/done are never touched) · 11 the popup
   * again (now excluding the bound chapter). Skip mid-flight → prev-ref cleanup closes it all.
   * NOTE: these hooks sit ABOVE the !ready early-return (rules of hooks); helper fns declared
   * further down (openLesson, currentChapterFile) resolve at effect run-time, which is fine. */
  // The tour's plan is the teacher's most recently PREPARED lesson — "the lesson you just now
  // generated" — NEVER a raw library entry. /plans returns the whole shared library with a
  // per-tenant `prepared` flag (api/main.py); picking gp[0] unfiltered made the guide demo an
  // arbitrary library chapter (kumar23 generated ch 2, the guide walked ch 9 — 2026-07-06).
  const latestPrepared = (gp) => {
    if (!Array.isArray(gp)) return null;
    const prepped = gp.filter((p) => p.prepared)
      .sort((a, b) => String(b.prepared_at || "").localeCompare(String(a.prepared_at || "")));
    return prepped[0] || null;
  };
  const tourTarget = (() => {
    if (tourStep == null) return null;
    for (let i = 0; i < classes.length; i++) {
      const c = classes[i];
      const plan = latestPrepared(plansByKey[`${c.subjectSlug}/${c.gradeSlug}`]);
      if (plan) {
        return { idx: i, c, sectionKey: `${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`, plan };
      }
    }
    return null;
  })();
  const tourIdx = tourTarget ? tourTarget.idx : -1;
  const tourDemoDone = tourStep === 10 || tourStep === 11;   // demo-complete rendering only

  // Report the target's name + chapter up so the step copy can say "attach {chapter} to {tag}".
  useEffect(() => {
    if (tourTarget && onTourInfo) {
      onTourInfo({ tag: tourTarget.c.sectionTag, chapter: tourTarget.plan.chapter_title });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tourStep, tourIdx]);

  useEffect(() => {
    if (tourStep == null || !tourTarget) return;
    const { c, sectionKey, plan } = tourTarget;
    const bound = currentChapterFile(sectionKey);
    if (tourStep >= 7 && bound !== plan.filename) {
      bindSectionChapter(sectionKey, plan.filename);   // the real attach (step 6 → 7)
      setSyncTick((t) => t + 1);
    } else if (tourStep <= 6 && bound) {
      unbindSection(sectionKey);                        // Back from 7 → 6 undoes it
      setSyncTick((t) => t + 1);
    }
    // Steps 8–9: the tracking lesson view is open; any other step closes it.
    if (tourStep === 8 || tourStep === 9) {
      if (!openPlan && !loading) openLesson(c.subjectSlug, c.gradeSlug, plan, sectionKey);
    } else if (openPlan) setOpenPlan(null);
    // Steps 6 and 11: the "Track a chapter for this section" popup; any other step closes it.
    // (At 6 nothing is bound, so the just-generated lesson is IN the list — the hand points at
    // it; at 11 the bound chapter is excluded, matching the "pick the NEXT chapter" moment.)
    if (tourStep === 6 || tourStep === 11) {
      if (!attachFor) setAttachFor({ c, sectionKey });
    } else if (attachFor) setAttachFor(null);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [tourStep, tourIdx, plansByKey, openPlan, loading, attachFor]);

  // Tour ended (Done or Skip) → close anything the tour opened, back to the plain cards view.
  const prevTourRef = useRef(null);
  useEffect(() => {
    if (prevTourRef.current != null && tourStep == null) {
      setOpenPlan(null); setAttachFor(null);
    }
    prevTourRef.current = tourStep;
  }, [tourStep]);

  // Readiness incomplete → first the 2a welcome landing, then the readiness grid flow.
  if (!ready) {
    if (!setupStarted) {
      // Screen 2a — welcome / readiness-incomplete empty state.
      return (
        <div className="welcome">
          <div className="kicker kicker-ochre welcome-kicker">Welcome to Aruvi</div>
          <div className="welcome-title">Let&rsquo;s get your week set up</div>
          <div className="welcome-sub">Aruvi needs two quick things before it can plan with you — your weekly grid of classes, and how long your teaching year is.</div>
          <div className="welcome-sub">This only takes a few minutes, and you&rsquo;ll only do it once.</div>
          <button className="welcome-begin" onClick={() => setSetupStarted(true)}>Let&rsquo;s begin →</button>
        </div>
      );
    }
    // Readiness grid flow (ported from readiness-grid-flow.html). Completing it unlocks Generate.
    return (
      <Readiness
        subject={pretty(subject)}
        onComplete={(payload) => { onReady && onReady(payload); /* stay in My Plans → 2b welcome */ }}
      />
    );
  }

  const openLesson = async (sSlug, gSlug, p, sectionKey) => {
    setLoading(true);
    try {
      const view = (await getJSON(`/plans/${sSlug}/${gSlug}/${p.filename}/view`)).view;
      setOpenPlan({ view, sectionKey });
    } finally { setLoading(false); }
  };

  // current-LU pointer (per section) from localStorage, for the "On: Learning Unit N" line
  const pointerFor = (sectionKey) => {
    if (typeof window === "undefined") return null;
    const n = Number(window.localStorage.getItem(`lu_pointer_${sectionKey}`));
    return Number.isFinite(n) && n >= 0 ? n + 1 : null;
  };
  // How many learning units this section has marked complete (= the raw pointer index; 0 when
  // untouched). This is the anti-noise gate for history: a chapter only enters the log if ≥1 unit
  // was completed before it left the current slot (teacher's rule — track/untrack is used casually).
  const unitsDoneFor = (sectionKey) => {
    if (typeof window === "undefined") return 0;
    const n = Number(window.localStorage.getItem(`lu_pointer_${sectionKey}`));
    return Number.isFinite(n) && n > 0 ? n : 0;
  };
  // Which chapter (filename) a section is currently tracking. Written when a chapter is bound to
  // a class; absent = nothing started yet ("pick a chapter to begin tracking").
  const currentChapterFile = (sectionKey) => {
    if (typeof window === "undefined") return null;
    try { return window.localStorage.getItem(`current_chapter_${sectionKey}`) || null; } catch { return null; }
  };
  // Every chapter filename currently bound to ANY section of this subject·grade. This is the API's
  // documented "belt-and-braces": a plan a sibling section is actively teaching counts as prepared
  // even when its `prepared` flag was never written (older bindings, or a lost/absent prepared
  // record) — so a chapter 7A/7B are teaching is still offered when attaching to a newly-added 7C.
  const boundFilesForGrade = (sSlug, gSlug) => {
    const set = new Set();
    classes.forEach((c) => {
      if (c.subjectSlug !== sSlug || c.gradeSlug !== gSlug) return;
      const f = currentChapterFile(`${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`);
      if (f) set.add(f);
    });
    return set;
  };
  // Completion flag written by LessonView when the last learning unit is marked complete.
  const isDone = (sectionKey) => {
    if (typeof window === "undefined") return false;
    try { return window.localStorage.getItem(`lu_done_${sectionKey}`) === "1"; } catch { return false; }
  };
  // Bind an already-prepared chapter to a section and return to the cards view — the originating
  // section card now shows this chapter (closing the modal re-renders it). We deliberately do NOT
  // open the lesson: the teacher lands back on My Classes, where she tapped "+", not inside the plan.
  // The pointer + done flag are PER-SECTION, so switching to a new chapter (e.g. from a completed
  // one) resets them — the new chapter starts fresh at its first learning unit.
  const attachChapter = (c, sectionKey, plan) => {
    bindSectionChapter(sectionKey, plan.filename);   // shared writer (same path the preview uses)
    setAttachFor(null);
    // Force an immediate re-render so the card reflects the new binding at once. On the DIRECT
    // first-run "+" path attachFor is already null, so setAttachFor(null) is a no-op that React
    // skips — without this bump the card only refreshed on the next incidental render (the 20s
    // sync / a tab focus), which read as the "+ works late" lag.
    setSyncTick((t) => t + 1);
  };

  // Clear a section's chapter binding + pointer + done. The chapter itself is untouched (still in
  // My Lessons); the card returns to the unstarted "Pick a chapter" (grey) state.
  const clearBinding = (sectionKey) => unbindSection(sectionKey);
  // Untrack (ongoing/started cards) — the reversal of tracking, via a confirm window. Logs an
  // "untracked" history entry ONLY when ≥1 unit was completed (the anti-noise gate); a casual
  // attach→untrack with no progress leaves no trace. We stamp the progress reached (units done /
  // total) so the history row can say how far the section got before untracking.
  const untrackChapter = (sectionKey, plan) => {
    if (plan && unitsDoneFor(sectionKey) >= 1) {
      recordHistory(sectionKey, {
        file: plan.filename, chapter_number: plan.chapter_number, chapter_title: plan.chapter_title,
        status: "untracked", units_done: unitsDoneFor(sectionKey), total_units: plan.total_units || null,
        ts: Date.now(),
      });
    }
    clearBinding(sectionKey); setUntrackFor(null);
  };
  // Move on from a COMPLETED chapter: one click frees it (card reverts to unstarted grey) and opens
  // the picker to track the next chapter — no confirm, since a finished chapter has no place to lose.
  // A completed chapter always earns its history row (all units done).
  const moveOnFromCompleted = (c, sectionKey, plan) => {
    if (plan) {
      recordHistory(sectionKey, {
        file: plan.filename, chapter_number: plan.chapter_number, chapter_title: plan.chapter_title,
        status: "completed", units_done: plan.total_units || null, total_units: plan.total_units || null,
        ts: Date.now(),
      });
    }
    clearBinding(sectionKey); setAttachFor({ c, sectionKey });
  };

  if (loading) return <div className="spin">Opening plan…</div>;
  if (openPlan) return <LessonView view={openPlan.view} sectionKey={openPlan.sectionKey} onExit={() => setOpenPlan(null)} />;

  // "+" attach-a-lesson picker — a focused MODAL layered over the cards (not a separate screen),
  // scoped to ONE subject·class. Lists chapters already prepared for that subject·grade (tap =
  // attach + open) and offers to prepare a brand-new one. Rendered at the bottom of the main
  // cards view; see attachModal below.
  const attachModal = attachFor ? (() => {
    const { c, sectionKey } = attachFor;
    const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
    // Only chapters SHE PREPARED (never raw library entries — /plans returns the whole shared
    // library; My Lessons applies the same filter), excluding the chapter already bound to this
    // section (e.g. the just-completed one) — she's here to pick a DIFFERENT chapter.
    const boundFile = currentChapterFile(sectionKey);
    const alsoAttachable = boundFilesForGrade(c.subjectSlug, c.gradeSlug); // bound to a sibling section
    const listPlans = Array.isArray(gradePlans)
      ? gradePlans.filter((p) => (p.prepared || alsoAttachable.has(p.filename)) && p.filename !== boundFile)
      : gradePlans;
    return (
      <div className="ap-overlay" onClick={() => setAttachFor(null)}>
        {/* data-tour="attach-pop": the tour's step-6 and step-11 spotlights wrap this popup. */}
        <div className="ap-modal" data-tour="attach-pop" onClick={(e) => e.stopPropagation()}>
          <button className="ap-close" aria-label="Close" onClick={() => setAttachFor(null)}>✕</button>
          <div className="ap-head">
            <div className="ap-kicker">{pretty(c.subjectSlug)} · Class {classNum(c.grade)} · {c.sectionTag}</div>
            <div className="ap-title">Track a chapter for this section</div>
            <div className="ap-sub">Pick a chapter you&rsquo;ve already prepared to track for this section, or build a new one.</div>
          </div>
          <div className="ap-list">
            {listPlans === undefined ? (
              <div className="ap-loading">Loading lessons…</div>
            ) : listPlans.length === 0 ? (
              <div className="ap-none">No other lessons prepared for this section yet.</div>
            ) : (
              listPlans.map((p, pi) => (
                // First row carries data-tour="attach-pop-row" — the tour's step-6 hand sits on
                // it ("select the lesson you just generated").
                <button key={p.filename} className="ap-row" data-tour={pi === 0 ? "attach-pop-row" : undefined}
                  onClick={() => attachChapter(c, sectionKey, p)}>
                  <span className="ch-meta">
                    <span className="ch-meta-tx"><b>Ch {pad(p.chapter_number)}</b></span>
                    <span className="ch-go" aria-hidden="true">›</span>
                  </span>
                  <span className="ch-name" title={p.chapter_title}>{p.chapter_title}</span>
                </button>
              ))
            )}
          </div>
          <div className="mlp-allocate">
            <span className="mlp-allocate-q">Need a chapter you don&rsquo;t have yet?</span>
            <button className="mlp-allocate-btn prepare-cta"
              onClick={() => onEnterGenerate && onEnterGenerate({ subject: c.subjectSlug, grade: c.gradeSlug, single: true, returnSection: c.sectionTag })}>
              Prepare a new lesson →
            </button>
          </div>
        </div>
      </div>
    );
  })() : null;

  // Untrack confirmation — a deliberate window so she's sure. Reversal of tracking; makes the plan
  // available to track again and clears her place in it.
  const untrackModal = untrackFor ? (() => {
    const { c, sectionKey, plan } = untrackFor;
    const chLabel = `${plan.chapter_number ? `Ch ${plan.chapter_number} — ` : ""}${plan.chapter_title}`;
    return (
      <div className="ap-overlay" onClick={() => setUntrackFor(null)}>
        <div className="ap-modal ap-confirm" onClick={(e) => e.stopPropagation()}>
          <button className="ap-close" aria-label="Close" onClick={() => setUntrackFor(null)}>✕</button>
          <div className="ap-head">
            <div className="ap-kicker">{pretty(c.subjectSlug)} · Class {classNum(c.grade)} · {c.sectionTag}</div>
            <div className="ap-title">Stop tracking this chapter?</div>
            <div className="ap-sub">{c.sectionTag} will stop tracking &ldquo;{chLabel}&rdquo;. It will be available to track again for this section.</div>
          </div>
          <div className="ap-confirm-actions">
            <button className="ap-btn-ghost" onClick={() => setUntrackFor(null)}>Keep tracking</button>
            <button className="ap-btn-danger" onClick={() => untrackChapter(sectionKey, plan)}>Stop tracking</button>
          </div>
        </div>
      </div>
    );
  })() : null;

  // Chapter-history popup — an instant in/out list (a function, not a screen). Shows ONE row per
  // chapter (the log is keyed by file → latest action wins), newest first. The still-bound current
  // chapter is overlaid live as "Ongoing"/"Completed" ONLY when it has progress (≥1 unit), so a
  // freshly-attached, untouched chapter never appears (matches the anti-noise gate).
  const historyModal = historyFor ? (() => {
    const { c, sectionKey } = historyFor;
    const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
    const byFile = {};
    readHistory(sectionKey).forEach((h) => { byFile[h.file] = { ...h }; });
    const curFile = currentChapterFile(sectionKey);
    if (curFile) {
      const done = isDone(sectionKey);
      if (done || unitsDoneFor(sectionKey) >= 1) {
        const cp = Array.isArray(gradePlans) ? gradePlans.find((p) => p.filename === curFile) : null;
        const prev = byFile[curFile];
        const total = cp ? (cp.total_units || null) : (prev ? prev.total_units : null);
        byFile[curFile] = {
          file: curFile,
          chapter_number: cp ? cp.chapter_number : (prev ? prev.chapter_number : null),
          chapter_title: cp ? cp.chapter_title : (prev ? prev.chapter_title : ""),
          status: done ? "completed" : "ongoing",
          units_done: done ? total : unitsDoneFor(sectionKey),
          total_units: total,
          ts: Date.now() + 1,   // current action sorts to the top
        };
      }
    }
    const rows = Object.values(byFile).sort((a, b) => (b.ts || 0) - (a.ts || 0));
    return (
      <div className="ap-overlay" onClick={() => setHistoryFor(null)}>
        <div className="ap-modal" onClick={(e) => e.stopPropagation()}>
          <button className="ap-close" aria-label="Close" onClick={() => setHistoryFor(null)}>✕</button>
          <div className="ap-head">
            <div className="ap-kicker">{pretty(c.subjectSlug)} · Class {classNum(c.grade)} · {c.sectionTag}</div>
            <div className="ap-title">Section history</div>
            <div className="ap-sub">Where each chapter stands for this section.</div>
          </div>
          <div className="ap-list">
            {rows.length === 0 ? (
              <div className="ap-none">No chapters taught yet.</div>
            ) : (
              rows.map((r) => {
                const st = normStatus(r.status);
                return (
                <div className="ch-row" key={r.file}>
                  <div className="ch-meta">
                    <span className="ch-meta-tx"><b>Ch {r.chapter_number ? pad(r.chapter_number) : "—"}</b></span>
                    <span className={`ch-pill ch-${st}`}>{HISTORY_LABEL[st] || "Untracked"}</span>
                  </div>
                  <div className="ch-name" title={r.chapter_title}>{r.chapter_title}</div>
                  {r.total_units ? (
                    <div className="sc-rail ch-rail"
                      aria-label={`${r.units_done || 0} of ${r.total_units} units completed`}>
                      {Array.from({ length: r.total_units }).map((_, t) => (
                        <span key={t} className={`sc-tick ${t < (r.units_done || 0) ? "done" : (st === "ongoing" && t === r.units_done ? "cur" : "")}`} />
                      ))}
                    </div>
                  ) : null}
                </div>
                );
              })
            )}
          </div>
        </div>
      </div>
    );
  })() : null;

  // Home header: time-of-day greeting (repeat view only — see below).
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const firstName = (user || "").trim();

  // Ready but the teacher has no classes at all (empty profile).
  if (!classes.length) {
    return (
      <div>
        <div className="dash-hd">
          <div>
            <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
          </div>
        </div>
        <div className="slotcard slot-empty">
          <div className="slotrail dim" />
          <div className="slotbody">
            <div className="slot-title muted">No classes set up yet</div>
            <div className="slot-meta">Set up your teaching profile from the settings gear above to start planning.</div>
          </div>
        </div>
      </div>
    );
  }

  // Nothing planned yet? The class cards still show — each as "Pick a chapter to begin" —
  // with a welcome CTA banner ABOVE them. Cards are never hidden.
  const anyBound = classes.some((c) => currentChapterFile(`${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`));
  // Any lesson SHE PREPARED for one of her classes? After first-gen this is TRUE (the lesson
  // was deposited but left unattached), so the welcome nudge points her at the "+" to attach it.
  // Prepared-only — a raw library entry must never trigger the nudge/welcome copy.
  const anyPlans = Object.values(plansByKey).some((v) => Array.isArray(v) && v.some((p) => p.prepared));

  /* My Classes home: a FLAT list of section cards — no day buckets, no "today", no pace pills.
   * Each card answers one question — "where did I stop with this class?" — via the LU progress
   * rail and a status shade (grey=not started, green=ongoing, gold=completed) carried on a
   * left-edge accent bar. FIRST-TIME view (no chapter bound anywhere) drops the greeting and
   * shows the welcome banner; REPEAT view shows the greeting + "continue where you left off". */
  return (
    <div>
      {/* The standing "+" portal (see the unlock note above) opens the Subject · Class ·
          Section chooser; each option routes into the SAME profile flows the settings gear
          uses (one implementation, two doors). PLACEMENT (founder, 2026-07-06): on the repeat
          view it sits IN the greeting row, right side — no row of its own, no lost real estate
          (and it rides the sticky greeting, so it stays reachable while the cards scroll). On
          the first-time view it keeps its own row BELOW "Your classes are ready" — classes
          encompass new subjects too, so it never sits above the welcome. */}
      {anyBound && (
        <div className="dash-hd">
          <div>
            <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
            <div className="dash-sub">Continue where you left off with every class.</div>
          </div>
          {plusShow && (
            <button className="sc-grow" data-tour="grow-add" aria-label="Add or change subjects, classes, or sections"
              title="Add or change what you teach" onClick={() => setGrowOpen(true)}>{GrowIcon}</button>
          )}
        </div>
      )}

      {!anyBound && (
        <div className="dash-welcome dash-welcome-row">
          <div className="dash-welcome-text">
            <div className="dash-welcome-title">Your classes are ready</div>
            <div className="dash-welcome-sub">{anyPlans
              ? <>Your lesson is waiting in My Lessons — tap <b>+</b> on a class to start teaching it.</>
              : <>Tap <b>+</b> on a class to prepare its first lesson.</>}</div>
          </div>
          {plusShow && (
            <button className="sc-grow" data-tour="grow-add" aria-label="Add or change subjects, classes, or sections"
              title="Add or change what you teach" onClick={() => setGrowOpen(true)}>{GrowIcon}</button>
          )}
        </div>
      )}

      <div className="sc-list">
        {classes.map((c, i) => {
          const sectionKey = `${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`;
          const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
          const file = currentChapterFile(sectionKey);
          const plan = file && Array.isArray(gradePlans) ? gradePlans.find((p) => p.filename === file) : null;
          const hist = hasHistory(sectionKey);   // any PAST chapters logged → show the history glyph

          // No chapter bound to this class yet → "pick a chapter to begin" (grey / not started).
          // The card is NOT tappable-to-generate anymore; the "+" opens the attach picker instead.
          if (!plan) {
            // The card stays EMPTY even after first-run generation (founder's call, 2026-07-09):
            // the freshly generated lesson lands ONLY in My Lessons and is never auto-named onto a
            // section card. The card just reads "Pick a chapter to begin" until she taps "+" and
            // attaches a lesson herself through the track-a-chapter picker.
            return (
              // On the tour's TARGET card, the "+" carries data-tour="section-add" — step 5's
              // spotlight + hand sit on it ("click the + sign of that section card").
              <div className="sc-card st-new" key={i}>
                <div className="sc-tag muted">{c.sectionTag}</div>
                <div className="sc-body">
                  <span className="sc-kicker">{pretty(c.subjectSlug)}</span>
                  <div className="sc-title muted">
                    Pick a chapter to begin
                  </div>
                </div>
                <div className="sc-right">
                  <button className="sc-add" data-tour={i === tourIdx ? "section-add" : undefined}
                    aria-label="Attach a lesson to this section"
                    onClick={() => setAttachFor({ c, sectionKey })}>+</button>
                  {hist && (
                    <button className="sc-hist" aria-label="Section history for this section"
                      onClick={() => setHistoryFor({ c, sectionKey })}>{HistoryIcon}</button>
                  )}
                </div>
              </div>
            );
          }

          const lu = pointerFor(sectionKey);          // current LU, 1-based (null = untouched)
          // Steps 9–10 DEMO the target card as completed (render-only — her real done flag and
          // pointer are untouched; the underlying state stays "attached, not started").
          const done = isDone(sectionKey) || (tourDemoDone && i === tourIdx);
          const total = plan.total_units || null;      // LU count from the plans listing
          const ticks = total ? Array.from({ length: total }) : null;
          const status = done ? "st-done" : lu ? "st-going" : "st-new";
          return (
            <div className={`sc-card ${status}`} key={i}
              data-tour={i === tourIdx ? "section-card-target" : undefined}
              onClick={() => openLesson(c.subjectSlug, c.gradeSlug, plan, sectionKey)}>
              <div className="sc-tag">{c.sectionTag}</div>
              <div className="sc-body">
                <span className="sc-kicker">{pretty(c.subjectSlug)}{plan.chapter_number ? ` · Ch ${plan.chapter_number}` : ""}</span>
                <div className="sc-title" title={plan.chapter_title}>{plan.chapter_title}</div>
                {ticks && (
                  <div className="sc-rail" aria-label={done ? `${total} units, completed` : lu ? `Unit ${lu} of ${total}` : `${total} units, not started`}>
                    {ticks.map((_, t) => (
                      <span key={t} className={`sc-tick ${done || (lu && t < lu - 1) ? "done" : lu && t === lu - 1 ? "cur" : ""}`} />
                    ))}
                  </div>
                )}
              </div>
              {/* Right-slot actions. COMPLETED → a "Complete" label + "+"; clicking "+" frees the
                  finished chapter (card reverts to unstarted) and opens the picker for the next one.
                  STILL TRACKING → "−" untrack, the deliberate reversal via a confirm window.
                  stopPropagation so neither opens the lesson. */}
              {done ? (
                <div className="sc-actions sc-actions-col">
                  <span className="sc-status-done">Complete</span>
                  {/* Step 10's spotlight + hand land on this "+" (the demo-complete target card). */}
                  <button className="sc-add" data-tour={i === tourIdx ? "section-add" : undefined}
                    aria-label="Finish with this chapter and track the next"
                    onClick={(e) => { e.stopPropagation(); moveOnFromCompleted(c, sectionKey, plan); }}>+</button>
                  {hist && (
                    <button className="sc-hist" aria-label="Section history for this section"
                      onClick={(e) => { e.stopPropagation(); setHistoryFor({ c, sectionKey }); }}>{HistoryIcon}</button>
                  )}
                </div>
              ) : (
                <div className="sc-right">
                  <button className="sc-remove" aria-label="Stop tracking this chapter"
                    onClick={(e) => { e.stopPropagation(); setUntrackFor({ c, sectionKey, plan }); }}>−</button>
                  {hist && (
                    <button className="sc-hist" aria-label="Section history for this section"
                      onClick={(e) => { e.stopPropagation(); setHistoryFor({ c, sectionKey }); }}>{HistoryIcon}</button>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* First-run helping hand — a gentle, one-time nudge shown only while nothing is attached
          yet and a lesson is waiting. A distinct-coloured "window" (not the paper background), a
          conversational invitation rather than a hard CTA. "Show me how" launches the guided walk
          (page.jsx owns the tour state). Gone once she's attached her first lesson or skipped. */}
      {!anyBound && anyPlans && !tourActive && onStartTour && (
        <div className="dash-nudge" role="note">
          <div className="dash-nudge-row">
            <span className="dash-nudge-hand" aria-hidden="true">{RouteIcon}</span>
            <div className="dash-nudge-text">
              <div className="dash-nudge-title">Allow me to show you how to track sections and handle Lesson plans</div>
              <div className="dash-nudge-sub">It only takes a few steps — I&rsquo;ll walk you through it.</div>
            </div>
          </div>
          <button className="dash-nudge-cta" onClick={() => onStartTour()}>Show me how&nbsp;&rarr;</button>
        </div>
      )}

      {/* Progressive acquisition — the ONE "grow" invitation, ever (see the expandTarget note
          above): shown once after the first generation + tour, pinned to the first one-class
          subject. Tapping opens the teaching-profile add-a-class flow scoped to that subject;
          ✕ or use hands over to the standing "+" portal. Warm-ochre window, distinct from the
          pine walkthrough nudge above. */}
      {expandTarget && (
        <div className="dash-expand" role="note">
          <button className="dash-expand-x" aria-label="Not now" onClick={dismissExpand}>✕</button>
          <div className="dash-expand-text">
            <div className="dash-expand-title">Do you teach {expandTarget.name} to other classes?</div>
            <div className="dash-expand-sub">Add another class and Aruvi sets it up the same way — its sections, period lengths, and teaching year.</div>
          </div>
          <button className="dash-expand-cta" onClick={() => onExpandClasses(expandTarget.name)}>Add another class&nbsp;&rarr;</button>
        </div>
      )}

      {/* The "+" portal chooser — Subject · Class · Section. Each routes into the teaching-
          profile flows (page.jsx opens the profile view with a one-shot intent; TeachingProfile
          launches the matching screen), where she can ADD or — behind the same scoped warnings
          the profile's dustbins use — REMOVE. Warned, never blocked: mid-year reassignments
          are real. */}
      {growOpen && (
        <div className="ap-overlay" onClick={() => setGrowOpen(false)}>
          <div className="ap-modal ap-grow" onClick={(e) => e.stopPropagation()}>
            <button className="ap-close" aria-label="Close" onClick={() => setGrowOpen(false)}>✕</button>
            <div className="ap-head">
              <div className="ap-kicker">Your teaching</div>
              <div className="ap-title">What would you like to change?</div>
              <div className="ap-sub">Add — or remove — at any level. Your lessons always stay in the library.</div>
            </div>
            <div className="ap-list">
              <button className="ap-row" onClick={() => { setGrowOpen(false); onProfilePortal("subject"); }}>
                <span className="ch-meta"><span className="ch-meta-tx"><b>Subject</b></span><span className="ch-go" aria-hidden="true">›</span></span>
                <span className="ch-name">Teach another subject — or drop one</span>
              </button>
              <button className="ap-row" onClick={() => { setGrowOpen(false); onProfilePortal("class"); }}>
                <span className="ch-meta"><span className="ch-meta-tx"><b>Class</b></span><span className="ch-go" aria-hidden="true">›</span></span>
                <span className="ch-name">Add or remove a class in a subject</span>
              </button>
              <button className="ap-row" onClick={() => { setGrowOpen(false); onProfilePortal("section"); }}>
                <span className="ch-meta"><span className="ch-meta-tx"><b>Section</b></span><span className="ch-go" aria-hidden="true">›</span></span>
                <span className="ch-name">Add or remove a section in a class</span>
              </button>
            </div>
          </div>
        </div>
      )}

      {attachModal}
      {untrackModal}
      {historyModal}
    </div>
  );
}
