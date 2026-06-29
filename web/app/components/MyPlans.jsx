"use client";
import { useEffect, useState } from "react";
import { getJSON, pad, pretty, gradeUp } from "../lib/format";
import Readiness from "./Readiness";
import LessonView from "./LessonView";

const DAYS = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];

/* Build the weekly class list from the readiness payload, scoped to this subject.
 * Each entry: { day, gradeIdx, grade, sectionTag } for every marked cell in the grids. */
function classesFromReadiness(readiness) {
  if (!readiness || !readiness.grids || !readiness.grades) return [];
  const out = [];
  readiness.grids.forEach((grid, gi) => {
    const g = readiness.grades[gi];
    if (!g || !Array.isArray(grid)) return;          // guard sparse/edited projections
    const secs = g.sections || [];
    grid.forEach((row, r) => {
      const sec = secs[r];
      if (!sec) return;                               // grid row without a matching section
      (row || []).forEach((v, c) => { if (v >= 0) out.push({ day: DAYS[c], dayIdx: c, grade: g.grade, sectionTag: sec.tag }); });
    });
  });
  return out;
}

export default function MyPlans({ subject, grade, ready, readiness, onReady, onNavigate, user, onSignOut, pendingOpen, onConsumePending }) {
  const [plans, setPlans] = useState([]);
  const [openPlan, setOpenPlan] = useState(null);  // { view, sectionKey } for LessonView
  const [loading, setLoading] = useState(false);
  const [setupStarted, setSetupStarted] = useState(false); // 2a welcome → grid flow gate

  useEffect(() => { setOpenPlan(null);
    if (!ready) return;
    getJSON(`/plans/${subject}/${grade}`).then((d) => setPlans(d.plans || [])).catch(() => setPlans([]));
  }, [subject, grade, ready]);

  // Deep-link from Track (My Lesson Plans): open a specific SECTION's plan, pointer-enabled.
  // Only act once the active scope matches the request, so we open against the right subject·grade.
  useEffect(() => {
    if (!pendingOpen || !ready) return;
    if (pendingOpen.subject !== subject || pendingOpen.grade !== grade) return;
    const sectionKey = `${subject}_${grade}_${pendingOpen.sectionTag}`;
    let live = true;
    setLoading(true);
    getJSON(`/plans/${subject}/${grade}/${pendingOpen.filename}/view`)
      .then((d) => { if (live) setOpenPlan({ view: d.view, sectionKey }); })
      .catch(() => {})
      .finally(() => { if (live) { setLoading(false); onConsumePending && onConsumePending(); } });
    return () => { live = false; };
  }, [pendingOpen, ready, subject, grade, onConsumePending]);

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
        onComplete={(payload) => { onReady && onReady(payload); onNavigate && onNavigate("generate"); }}
      />
    );
  }

  const openLesson = async (p, sectionKey) => {
    setLoading(true);
    try {
      const view = (await getJSON(`/plans/${subject}/${grade}/${p.filename}/view`)).view;
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

  const classes = classesFromReadiness(readiness)
    // dashboard is scoped to the active grade's sections that match this subject·grade plans
    .filter((c) => gradeUp(grade) === c.grade);
  const byDay = DAYS.map((d) => ({ day: d, items: classes.filter((c) => c.day === d) })).filter((x) => x.items.length);
  const planByChapter = plans; // plans already scoped to subject·grade
  const firstPlan = plans[0];

  // No classes from readiness (sparse data) → fall back to a simple plans list so the screen
  // still resolves to the teacher's content.
  const haveSchedule = byDay.length > 0;

  // 2b — ready but nothing generated yet: forward/panic state, single CTA to Generate.
  if (!plans.length) {
    return (
      <div>
        <div className="dash-hd">
          <div><div className="kicker kicker-ochre">My Plans · This week</div><div className="dash-title">This week&rsquo;s teaching</div></div>
        </div>
        <div className="slotcard empty">
          <div className="slotrail dim" />
          <div className="slotbody">
            <div className="slot-toprow"><span className="slot-sec">{gradeUp(grade)} {pretty(subject).toUpperCase()}</span><span className="slot-ptr none">No plan yet</span></div>
            <div className="slot-title muted">You teach this class — no lesson plan made</div>
            <div className="slot-meta">Plan the chapter in Generate, and it&rsquo;ll appear here, ready to teach.</div>
          </div>
        </div>
        <div className="dash-cta">
          <button className="primary" onClick={() => onNavigate && onNavigate("generate")}>Ready to plan your first few chapters? →</button>
          <div className="dash-cta-note">Opens the Generate tab — choose chapters, set their time, make the plans.</div>
        </div>
      </div>
    );
  }

  // 2c — populated weekly dashboard.
  return (
    <div>
      <div className="dash-hd">
        <div><div className="kicker kicker-ochre">My Plans · This week</div><div className="dash-title">This week&rsquo;s teaching</div></div>
        <div className="dash-count">{classes.length || plans.length} classes<br />{pretty(subject)} · Grade {gradeUp(grade)}</div>
      </div>

      {haveSchedule ? byDay.map(({ day, items }) => (
        <div key={day}>
          <div className="daylabel">{day}</div>
          {items.map((c, i) => {
            const sectionKey = `${subject}_${grade}_${c.sectionTag}`;
            const lu = pointerFor(sectionKey);
            const plan = firstPlan; // one chapter in progress per section (saved-plan model)
            if (!plan) {
              return (
                <div className="slotcard empty" key={i}>
                  <div className="slotrail dim" />
                  <div className="slotbody">
                    <div className="slot-toprow"><span className="slot-sec">{c.sectionTag} {pretty(subject).toUpperCase()}</span><span className="slot-ptr none">No chapter started</span></div>
                    <div className="slot-title muted">Pick a chapter to begin</div>
                    <div className="slot-meta">Schedule only — no content cued yet</div>
                  </div>
                </div>
              );
            }
            return (
              <div className="slotcard" key={i} onClick={() => openLesson(plan, sectionKey)}>
                <div className="slotrail" />
                <div className="slotbody">
                  <div className="slot-toprow"><span className="slot-sec">{c.sectionTag} {pretty(subject).toUpperCase()}</span><span className="slot-ptr">{lu ? `On: Learning Unit ${lu}` : "Ready to start"}</span></div>
                  <div className="slot-title">{plan.chapter_title}</div>
                  <div className="slot-meta">tap to see · resumes where you left {c.sectionTag}</div>
                </div>
              </div>
            );
          })}
        </div>
      )) : (
        // fallback: no readiness schedule — list saved plans as openable cards
        <div>
          <div className="daylabel">Your plans</div>
          {plans.map((p) => {
            const sectionKey = `${subject}_${grade}_ch${p.chapter_number}`;
            const lu = pointerFor(sectionKey);
            return (
              <div className="slotcard" key={p.filename} onClick={() => openLesson(p, sectionKey)}>
                <div className="slotrail" />
                <div className="slotbody">
                  <div className="slot-toprow"><span className="slot-sec">CH {pad(p.chapter_number)}</span><span className="slot-ptr">{lu ? `On: Learning Unit ${lu}` : "Ready to start"}</span></div>
                  <div className="slot-title">{p.chapter_title}</div>
                  <div className="slot-meta">tap to open the lesson</div>
                </div>
              </div>
            );
          })}
        </div>
      )}

      <div className="dash-foot">Tap any class to open its lesson. Your place only moves when you tell it to.</div>
    </div>
  );
}
