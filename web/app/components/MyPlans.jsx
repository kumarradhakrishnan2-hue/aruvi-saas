"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty } from "../lib/format";
import Readiness from "./Readiness";
import LessonView from "./LessonView";

const subjectSlug = (name) => (name || "").toLowerCase().replace(/ /g, "_");
const gradeSlug = (g) => (g || "").toLowerCase();

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

  // Home header: time-of-day greeting + the universal "+ Prepare Lesson" action.
  const hour = new Date().getHours();
  const greeting = hour < 12 ? "Good morning" : hour < 17 ? "Good afternoon" : "Good evening";
  const firstName = (user || "").trim();
  const prepareLesson = () => onEnterGenerate && onEnterGenerate();

  // Ready but the teacher has no classes at all (empty profile).
  if (!classes.length) {
    return (
      <div>
        <div className="dash-hd">
          <div>
            <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
          </div>
          <button className="primary dash-prepare" onClick={prepareLesson}>+ Prepare Lesson</button>
        </div>
        <div className="slotcard slot-empty">
          <div className="slotrail dim" />
          <div className="slotbody">
            <div className="slot-title muted">No classes set up yet</div>
            <div className="slot-meta">Prepare a lesson and add it to a class, or set up your teaching profile from the settings gear above.</div>
          </div>
        </div>
      </div>
    );
  }

  // Nothing planned yet? The class cards still show — each as "Pick a chapter to begin" —
  // with a welcome CTA banner ABOVE them. Cards are never hidden.
  const anyBound = classes.some((c) => currentChapterFile(`${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`));

  /* My Classes home (2026-07-02, approved mockup): a FLAT list of section cards — no day
   * buckets, no "today", no pace pills. The card answers exactly one question — "where did I
   * stop with this class?" — via the LU progress rail (done=pine, current=ochre) and the
   * "LU n of N" line. LU-level only for now (phase-level marking is a later step). */
  return (
    <div>
      <div className="dash-hd">
        <div>
          <div className="dash-title">{greeting}{firstName ? `, ${firstName}` : ""}!</div>
          <div className="dash-sub">Here is where you stopped with each class.</div>
        </div>
        <button className="primary dash-prepare" onClick={prepareLesson}>+ Prepare Lesson</button>
      </div>

      {!anyBound && (
        <div className="dash-welcome">
          <div className="dash-welcome-text">
            <div className="dash-welcome-title">Your classes are set up — ready to plan?</div>
            <div className="dash-welcome-sub">Tap a class below to plan its first chapter.</div>
          </div>
        </div>
      )}

      <div className="sc-list">
        {classes.map((c, i) => {
          const sectionKey = `${c.subjectSlug}_${c.gradeSlug}_${c.sectionTag}`;
          const gradePlans = plansByKey[`${c.subjectSlug}/${c.gradeSlug}`];
          const file = currentChapterFile(sectionKey);
          const plan = file && Array.isArray(gradePlans) ? gradePlans.find((p) => p.filename === file) : null;

          // No chapter bound to this class yet → "pick a chapter to begin".
          // Still tappable — an open invitation, not a disabled slot.
          if (!plan) {
            return (
              <div className="sc-card" key={i}
                onClick={() => onEnterGenerate && onEnterGenerate({ subject: c.subjectSlug, grade: c.gradeSlug, single: true })}>
                <div className="sc-tag muted">{c.sectionTag}</div>
                <div className="sc-body">
                  <span className="sc-kicker">{pretty(c.subjectSlug)}</span>
                  <div className="sc-title muted">Pick a chapter to begin</div>
                  <div className="sc-meta">No lesson attached yet</div>
                </div>
              </div>
            );
          }

          const lu = pointerFor(sectionKey);          // current LU, 1-based (null = untouched)
          const total = plan.total_units || null;      // LU count from the plans listing
          const ticks = total ? Array.from({ length: total }) : null;
          return (
            <div className="sc-card" key={i}
              onClick={() => openLesson(c.subjectSlug, c.gradeSlug, plan, sectionKey)}>
              <div className="sc-tag">{c.sectionTag}</div>
              <div className="sc-body">
                <span className="sc-kicker">{pretty(c.subjectSlug)}</span>
                <div className="sc-title">{plan.chapter_number ? `Ch ${plan.chapter_number} — ` : ""}{plan.chapter_title}</div>
                {ticks && (
                  <div className="sc-rail" aria-label={lu ? `Learning Unit ${lu} of ${total}` : `${total} learning units, not started`}>
                    {ticks.map((_, t) => (
                      <span key={t} className={`sc-tick ${lu && t < lu - 1 ? "done" : lu && t === lu - 1 ? "cur" : ""}`} />
                    ))}
                  </div>
                )}
                <div className="sc-meta">{lu ? `LU ${lu}${total ? ` of ${total}` : ""}` : "Ready to start"}</div>
              </div>
            </div>
          );
        })}
      </div>

      <div className="dash-foot">Tap any class to open its lesson. Your place only moves when you tell it to.</div>
    </div>
  );
}
