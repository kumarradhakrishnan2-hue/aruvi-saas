"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty } from "../lib/format";
import Readiness from "./Readiness";
import LessonView from "./LessonView";

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
const DAY_FULL = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];
// Same rotating accent palette FirstRun's section cards use — reused here (not imported, since
// FirstRun.jsx doesn't export it) so the "Good morning" home cards read as the same visual family.
const SECTION_ACCENTS = ["var(--pine)", "var(--clay)", "var(--ochre)"];

const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const gradeSlug = (g) => (g || "").toLowerCase();

/* Build the week as ONE CARD PER subject·grade·section the teacher handles — across ALL subjects
 * (walks the canonical readiness.subjects[], not the single active projection). A section that
 * meets on several days is shown once, under its NEXT meeting day (earliest weekday it has a
 * marked cell). Each entry carries the slugs + section tag so My Week can look up that class's
 * plans and its per-section pointer. */
function classesFromReadiness(readiness) {
  const subjects = (readiness && readiness.subjects) || [];
  const out = [];
  subjects.forEach((s) => {
    const sSlug = subjectSlug(s.name);
    (s.grades || []).forEach((g, gi) => {
      const gSlug = gradeSlug(g.grade);
      (g.sections || []).forEach((sec, si) => {
        // earliest weekday this section meets (its "next" / upcoming class)
        const gridRow = ((s.grids || [])[gi] || [])[si] || [];
        let dayIdx = -1;
        for (let c = 0; c < DAYS.length; c++) { if (gridRow[c] != null && gridRow[c] >= 0) { dayIdx = c; break; } }
        out.push({
          subjectName: s.name, subjectSlug: sSlug, grade: g.grade, gradeSlug: gSlug,
          sectionTag: sec.tag, dayIdx, day: dayIdx >= 0 ? DAYS[dayIdx] : null,
        });
      });
    });
  });
  return out;
}

export default function MyPlans({ subject, grade, ready, readiness, onReady, onNavigate, onEnterGenerate, user, onSignOut, pendingOpen, onConsumePending }) {
  const [openPlan, setOpenPlan] = useState(null);  // { view, sectionKey } for LessonView
  const [loading, setLoading] = useState(false);
  const [setupStarted, setSetupStarted] = useState(false); // 2a welcome → grid flow gate
  // plans for EVERY subject·grade the teacher handles, keyed `${subjectSlug}/${gradeSlug}`.
  const [plansByKey, setPlansByKey] = useState({});

  // All classes across all subjects (one card per subject·grade·section).
  const classes = ready ? classesFromReadiness(readiness) : [];

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

  if (loading) return <div className="spin">Opening plan…</div>;
  if (openPlan) return <LessonView view={openPlan.view} sectionKey={openPlan.sectionKey} onExit={() => setOpenPlan(null)} />;

  // current-LU pointer (per section) from localStorage, for the "On: Learning Unit N" line
  const pointerFor = (sectionKey) => {
    if (typeof window === "undefined") return null;
    const n = Number(window.localStorage.getItem(`lu_pointer_${sectionKey}`));
    return Number.isFinite(n) && n >= 0 ? n + 1 : null;
  };
  // Which chapter (filename) a section is currently tracking. Written when a chapter is bound to
  // a class; absent = nothing started yet ("pick a chapter to begin tracking").
  const currentChapterFile = (sectionKey) => {
    if (typeof window === "undefined") return null;
    try { return window.localStorage.getItem(`current_chapter_${sectionKey}`) || null; } catch { return null; }
  };

  // One card per section·subject (cards = Σ subjects-per-section), grouped under its next meeting
  // day in Mon→Sat order. No schedule cell for a class (dayIdx < 0) → an "Unscheduled" bucket last.
  const dayBuckets = [...DAY_FULL.map((d) => ({ day: d, items: [] })), { day: "Unscheduled", items: [] }];
  classes.forEach((c) => {
    const bucket = c.dayIdx >= 0 ? dayBuckets[c.dayIdx] : dayBuckets[dayBuckets.length - 1];
    bucket.items.push(c);
  });
  const byDay = dayBuckets.filter((b) => b.items.length);

  // "My Week is Home" (§0) — a time-of-day greeting replaces the flat "This week's teaching"
  // label, and a universal "+ Prepare Lesson" action replaces the old Generate tab everywhere.
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const firstName = (user || "").trim();
  const prepareLesson = () => onEnterGenerate && onEnterGenerate();

  // 2b — ready but the teacher has no classes at all (empty profile).
  if (!classes.length) {
    return (
      <div>
        <div className="dash-hd">
          <div>
            <div className="kicker kicker-ochre">My Week</div>
            <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
          </div>
          <button className="primary dash-prepare" onClick={prepareLesson}>+ Prepare Lesson</button>
        </div>
        <div className="slotcard slot-empty">
          <div className="slotrail dim" />
          <div className="slotbody">
            <div className="slot-title muted">No classes set up yet</div>
            <div className="slot-meta">Add your classes in My Class, then plan chapters in Generate.</div>
          </div>
        </div>
      </div>
    );
  }

  // Nothing planned yet (fresh after "Let's begin")? The class cards still show — each as "Pick a
  // chapter to begin tracking" — with a welcome CTA banner ABOVE them. Cards are never hidden.
  const anyBound = classes.some((c) => currentChapterFile(`${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`));

  // Today's bucket floats to the top (Mon=0…Sat=5; Sunday has no modelled school day, so the
  // buckets stay in their natural Mon→Sat order that day). "Unscheduled" always sorts last.
  const todayIdx = (new Date().getDay() + 6) % 7;
  const todayName = todayIdx < 6 ? DAY_FULL[todayIdx] : null;
  const orderedBuckets = todayName
    ? [...byDay].sort((a, b) => {
        const rank = (b0) => (b0.day === "Unscheduled" ? 100 : b0.day === todayName ? -1 : DAY_FULL.indexOf(b0.day));
        return rank(a) - rank(b);
      })
    : byDay;

  let cardIdx = 0;

  // Weekly dashboard: every class she handles, today first (+ welcome banner when fresh).
  return (
    <div>
      <div className="dash-hd">
        <div>
          <div className="kicker kicker-ochre">My Week</div>
          <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
          <div className="dash-sub">Here are your lessons for today.</div>
        </div>
        <button className="primary dash-prepare" onClick={prepareLesson}>+ Prepare Lesson</button>
      </div>

      {!anyBound && (
        <div className="dash-welcome">
          <div className="dash-welcome-text">
            <div className="dash-welcome-title">Your week is set up — ready to plan?</div>
            <div className="dash-welcome-sub">Tap a class below to plan its first chapter.</div>
          </div>
        </div>
      )}

      {orderedBuckets.map(({ day, items }) => (
        <div key={day}>
          <div className="daylabel">{day === todayName ? "Today" : day}</div>
          <div className="fr-sc-list">
            {items.map((c, i) => {
              const sectionKey = `${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`;
              const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
              const file = currentChapterFile(sectionKey);
              const plan = file && Array.isArray(gradePlans) ? gradePlans.find((p) => p.filename === file) : null;
              const lu = pointerFor(sectionKey);
              const accent = SECTION_ACCENTS[cardIdx % SECTION_ACCENTS.length];
              cardIdx++;

              // No chapter bound to this class yet → "pick a chapter to begin tracking".
              // Still tappable — an open invitation, not a disabled slot.
              if (!plan) {
                return (
                  <div className="fr-sc-card" key={i} style={{ "--sc-accent": accent }}
                    onClick={() => onEnterGenerate && onEnterGenerate({ subject: c.subjectSlug, grade: c.gradeSlug, single: true })}>
                    <div className="fr-sc-chip">{c.sectionTag}</div>
                    <div className="fr-sc-body">
                      <span className="fr-sc-kicker">{pretty(c.subjectSlug)}</span>
                      <div className="fr-sc-title muted">Pick a chapter to begin tracking</div>
                      <div className="fr-sc-meta">Schedule only — no content cued yet</div>
                    </div>
                  </div>
                );
              }
              return (
                <div className="fr-sc-card" key={i} style={{ "--sc-accent": accent }}
                  onClick={() => openLesson(c.subjectSlug, c.gradeSlug, plan, sectionKey)}>
                  <div className="fr-sc-chip">{c.sectionTag}</div>
                  <div className="fr-sc-body">
                    <span className="fr-sc-kicker">{pretty(c.subjectSlug)}</span>
                    <div className="fr-sc-title">{plan.chapter_title}</div>
                    <div className="fr-sc-meta">tap to see · resumes where you left {c.sectionTag}</div>
                    <span className="fr-sc-ready">{lu ? `On: Learning Unit ${lu}` : "Ready to start"}</span>
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      ))}

      <div className="dash-foot">Tap any class to open its lesson. Your place only moves when you tell it to.</div>
    </div>
  );
}
