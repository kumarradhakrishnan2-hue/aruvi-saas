"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN, projectReadiness, API, withUser, getUser, setUser, clearUser } from "./lib/format";
import GenerateTab from "./components/GenerateTab";
import MyPlans from "./components/MyPlans";
import StatePill from "./components/StatePill";
import Login from "./components/Login";
import FirstRun from "./components/FirstRun";
import SidebarNav from "./components/SidebarNav";
import MyClasses from "./components/MyClasses";
import MyCalendar from "./components/MyCalendar";
import MyLessonPlans from "./components/MyLessonPlans";

/* ───────── app shell ─────────
 * The app is gated behind a user-ID portal (Login). No password yet: the entered ID is the
 * tenant key — stored in localStorage, sent as X-Aruvi-User on every API call, and used by
 * the server to scope all per-teacher state (tenant_id == user_id). This makes the
 * persistence testable across multiple "teachers" and is the exact seam Phase 4 swaps for
 * Supabase Auth.
 *
 * Two tabs: My Plans (operational home + readiness) and Generate (allocate → generate).
 * Readiness gates Generate, and is PERSISTED server-side per user (GET/POST /readiness): the
 * teaching profile (subjects/grades/sections/durations) is loaded when a user signs in, so it
 * survives a refresh, a server restart, or a fresh browser — never lost on session cut. */
/* Activation gate (Phase 1, §0): the shell stays hidden until the teacher has completed the
 * guided first run. This USED to be tracked as a separate localStorage flag per user — but
 * that flag was purely client-side and could desync from the server: e.g. deleting a test
 * user's profile/allocations server-side left the browser's stale "activated" flag in place,
 * so she'd skip straight to a now-empty shell instead of being sent back through FirstRun
 * (found testing kumar3, 2026-07-02). Fixed by dropping the separate flag entirely — `ready`
 * (rehydrated from the real GET /readiness response) is now the SOLE activation signal, since
 * FirstRun's finishActivation always produces a real subjects[] payload before calling
 * onComplete. One source of truth, server-side, never stale. */

export default function Home() {
  // null = "haven't checked localStorage yet" (avoids a login-screen flash on refresh).
  const [user, setUserState] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");
  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");
  const [tab, setTab] = useState("myplans");
  const [ready, setReady] = useState(false);      // readiness flag — rehydrated per user from GET /readiness
  const [readiness, setReadiness] = useState(null); // readiness projection (durations/grids/budget) — feeds G4's weekly ratio
  const [readinessLoaded, setReadinessLoaded] = useState(false); // has GET /readiness resolved? (gates the first-run decision, avoids a flash)
  const [sidebarOpen, setSidebarOpen] = useState(false); // hamburger-triggered overlay drawer (Phase 2 shell, "side bar.jpg") — closed by default
  const [editFlow, setEditFlow] = useState(null);  // "profile" | "calendar" | "lessonplans" | null — sidebar-launched view
  const [pendingOpen, setPendingOpen] = useState(null);  // {subject,grade,sectionTag,filename} — deep-link from Track into My Week
  // How the Generate tab should open this time:
  //   { mode: "pick" }                     → show the G1.9 subject·grade picker (multi-choice)
  //   { mode: "scoped", subject, grade }   → skip picker, go straight in for that subject·grade
  // Cleared once Generate consumes it. Generate is only ever reached through this handler.
  const [generateEntry, setGenerateEntry] = useState(null);

  // On mount, restore the signed-in user from localStorage (survives refresh).
  useEffect(() => { setUserState(getUser()); }, []);

  // Load this user's readiness profile whenever the signed-in user changes (incl. on the
  // initial restore). The API scopes the read to X-Aruvi-User; we regenerate the active-
  // subject projection the consumers read. Clearing first prevents one user's data flashing
  // for another after a sign-out/sign-in.
  useEffect(() => {
    if (!user) return;
    setReady(false); setReadiness(null); setReadinessLoaded(false);
    getJSON("/readiness").then((d) => {
      if (d && d.ready && d.readiness) {
        setReadiness(projectReadiness(d.readiness));
        setReady(true);
      }
    }).catch(() => {})  // no saved profile / API down → stay in the not-ready setup flow
      .finally(() => setReadinessLoaded(true));
  }, [user]);

  // First-run complete: FirstRun has now walked the FULL sequence (subject → grade → chapter →
  // preview → section fan-out → arrange-week-or-skip) and hands up the canonical readiness
  // payload it built — { subjects: [subjectRecord] }. This is the real activation moment: persist
  // it for real (same POST used by the old upfront wizard, via onReadyComplete's pattern), flip
  // `ready` so the shell opens with her new section card(s) already visible in My Plans, and
  // scope the Generate tab to what she just set up. `ready` is now the ONLY activation signal
  // (see the comment above the component) — no separate local flag to keep in sync.
  const onFirstRunComplete = (payload) => {
    const subs = (payload && payload.subjects) || [];
    if (subs.length) {
      setReadiness(projectReadiness({ subjects: subs }));
      setReady(true);
      const first = subs[0];
      setSubject(subjectSlugify(first.name));
      if (first.grades && first.grades[0]) setGrade((first.grades[0].grade || "").toLowerCase());
      fetch(`${API}/readiness`, withUser({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subjects: subs }),
      })).catch(() => {});
    }
  };

  useEffect(() => { if (!user) return;
    getJSON("/subjects").then((d) => { setSubjects(d.subjects); setSubject(d.subjects.includes("science") ? "science" : d.subjects[0]); }).catch(() => {});
  }, [user]);

  useEffect(() => { if (!subject) return;
    getJSON(`/subjects/${subject}/grades`).then((d) => {
      const gs = [...d.grades].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGrades(gs); setGrade(gs.includes("vii") ? "vii" : gs[0] || "");
    }).catch(() => setGrades([]));
  }, [subject]);

  // Persist the readiness profile (canonical subjects[] only) when setup completes, then
  // flip ready. Fire-and-forget: the UI advances immediately; the write carries the user
  // header so it lands under the right tenant.
  const onReadyComplete = (payload) => {
    setReadiness(payload);
    setReady(true);
    fetch(`${API}/readiness`, withUser({
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ subjects: (payload && payload.subjects) || [] }),
    })).catch(() => {});
  };


  // From My Lesson Plans: "Need a chapter…" pre-scopes Generate to a subject·grade and opens
  // it, so the allocation table lands on that exact combo (slugs match the scope-pill state).
  const onAllocateScoped = (subjectSlug, gradeSlug) => {
    if (subjectSlug) setSubject(subjectSlug);
    if (gradeSlug) setGrade(gradeSlug);
    setEditFlow(null);
    setGenerateEntry({ mode: "scoped", subject: subjectSlug, grade: gradeSlug });
    setTab("generate");
  };

  // THE single route into Generate (the "Ready to plan…" button + My Week empty cards). With one
  // subject AND one grade we skip the picker and scope directly; otherwise the G1.9 picker runs.
  // `opts.subject`/`opts.grade` (slugs) pre-scope and skip the picker (My Week row / My Lesson Plans).
  const subjectSlugify = (n) => (n || "").toLowerCase().replace(/ /g, "_");
  // opts.single === true marks a one-chapter-at-a-time entry (from a My Week card) — Allocate
  // rewords G4 to "this chapter" and shows the budget anchor. Bulk entries (Generate tab, My
  // Lesson Plans "Generate") leave it falsy and keep the multi-chapter framing.
  const onEnterGenerate = (opts = {}) => {
    const subs = (readiness && readiness.subjects) || [];
    const single = !!opts.single;
    if (opts.subject && opts.grade) {
      setSubject(opts.subject); setGrade(opts.grade);
      setGenerateEntry({ mode: "scoped", subject: opts.subject, grade: opts.grade, single });
    } else if (subs.length === 1 && (subs[0].grades || []).length === 1) {
      const sSlug = subjectSlugify(subs[0].name);
      const gSlug = (subs[0].grades[0].grade || "").toLowerCase();
      setSubject(sSlug); setGrade(gSlug);
      setGenerateEntry({ mode: "scoped", subject: sSlug, grade: gSlug, single });
    } else {
      setGenerateEntry({ mode: "pick", single });
    }
    setEditFlow(null);
    setTab("generate");
  };

  // From My Lesson Plans → Track: deep-link into My Week to open a SECTION's pointer-enabled
  // plan (grade-level reads, section-level acts). Scope the tab, leave the library, and stash
  // a pending-open hint that MyPlans consumes on mount.
  const onOpenSection = (subjectSlug, gradeSlug, sectionTag, plan) => {
    if (subjectSlug) setSubject(subjectSlug);
    if (gradeSlug) setGrade(gradeSlug);
    setPendingOpen({ subject: subjectSlug, grade: gradeSlug, sectionTag, filename: plan && plan.filename });
    setEditFlow(null);
    setTab("myplans");
  };

  const onEnter = (id) => { setUser(id); setUserState(id); };
  const onSignOut = () => {
    clearUser(); setUserState("");
    setReady(false); setReadiness(null); setReadinessLoaded(false);
    setSubjects([]); setSubject(""); setTab("myplans"); setSidebarOpen(false);
  };

  // Sidebar item picked (My Class / Calendar / Lesson Plans / My Week) — same handler for both
  // the drawer and the mobile bottom-tab bar, since they route to the exact same places.
  const goEdit = (mode) => { setEditFlow(mode); setTab("myplans"); setGenerateEntry(null); setSidebarOpen(false); };
  const goWeek = () => { setEditFlow(null); setTab("myplans"); setGenerateEntry(null); setSidebarOpen(false); };
  const activeNav = editFlow === "profile" ? "profile" : editFlow === "calendar" ? "calendar" : editFlow === "lessonplans" ? "lessonplans" : "week";

  // Still restoring from localStorage — render nothing for a beat (no login flash).
  if (user === null) return null;
  // Not signed in → the portal.
  if (!user) return <Login onEnter={onEnter} />;
  // Signed in, but wait for GET /readiness to resolve before deciding first-run vs shell
  // (prevents an already-set-up teacher from flashing the guided first run).
  if (!readinessLoaded) return null;
  // Phase 1 gate (§0): no app shell until `ready` — a teacher with an existing (real,
  // server-persisted) readiness profile skips first-run; a brand-new teacher, OR one whose
  // profile was reset, gets the shell-less Guided First Experience until she completes it.
  if (!ready) return <FirstRun user={user} onComplete={onFirstRunComplete} onSignOut={onSignOut} />;

  return (
    <>
      {/* Phase 2 shell header ("side bar.jpg"): hamburger ALWAYS opens the drawer (it's the
          only nav now — the old My Plans/Generate tab row is gone), brand centered, bell right.
          Always rendered regardless of tab/editFlow, so there's always a way back to My Week. */}
      <header className="hdr hdr-shell">
        <button className="hamb" onClick={() => setSidebarOpen(true)} aria-label="Open menu">
          <span /><span /><span />
        </button>
        <span className="brand-row hdr-brand-center">Aruvi<em>.</em><small>lesson studio</small></span>
        <button className="hdr-bell" aria-label="Notifications" disabled>🔔</button>
      </header>

      {sidebarOpen && (
        <div className="drawer-bg" onClick={(e) => { if (e.currentTarget === e.target) setSidebarOpen(false); }}>
          <aside className="drawer">
            <div className="drawer-hd">
              <span className="brand-row">Aruvi<em>.</em><small>lesson studio</small></span>
              <button className="drawer-close" onClick={() => setSidebarOpen(false)} aria-label="Close menu">×</button>
            </div>
            {/* Any sidebar item leaves the Generate flow and sits under My Plans — reset the
                tab + clear any pending Generate entry/scope pills, then close the drawer. */}
            <SidebarNav onEdit={goEdit} onWeek={goWeek} user={user} onSignOut={onSignOut} active={activeNav} />
          </aside>
        </div>
      )}

      <div className="bodycontent">
        {/* Subject·grade scope pills belong to Generate only — no tab row to anchor them to
            anymore, so they sit as a slim strip at the top of Generate's own content. */}
        {tab === "generate" && ready && (
          <div className="hdr-scope hdr-scope-standalone">
            <StatePill value={subject} options={subjects.map((s) => ({ value: s, label: pretty(s) }))}
              render={pretty(subject)} onChange={setSubject} />
            <StatePill value={grade} options={grades.map((g) => ({ value: g, label: gradeUp(g) }))}
              render={grade ? `Grade ${gradeUp(grade)}` : "—"} onChange={setGrade} />
          </div>
        )}

        <main>
          {/* Edit-flow views (My Calendar / My Class) require a set-up profile. A not-ready
           * user is always routed to the My Plans "Let's begin" setup flow instead of a
           * dead-end empty view — readiness gates these the same way it gates Generate. */}
          {(editFlow === "calendar" && ready) ? (
            /* My Calendar — read-only weekly timetable built from the readiness profile. */
            <div className="editflow">
              <MyCalendar readiness={readiness} />
            </div>
          ) : (editFlow === "lessonplans" && ready) ? (
            /* My Lesson Plans — technical resource library (subject → grade → chapter). */
            <div className="editflow">
              <MyLessonPlans readiness={readiness} onAllocate={onAllocateScoped} onOpenSection={onOpenSection} />
            </div>
          ) : (editFlow === "profile" && ready) ? (
            /* My Class — the editable teaching-profile drill-down (subjects/grades/sections +
             * time facts). Persists each edit to /readiness and calls onChange to re-project. */
            <div className="editflow">
              <MyClasses readiness={readiness} onChange={setReadiness} />
            </div>
          ) :
            !subject ? <div className="empty">Connecting to the Aruvi engine…</div> :
            tab === "generate" ? <GenerateTab subject={subject} grade={grade} ready={ready} readiness={readiness}
              onNavigate={setTab} entry={generateEntry} onScope={(s, g) => { setSubject(s); setGrade(g); }}
              onConsumeEntry={() => setGenerateEntry(null)} /> :
            <MyPlans subject={subject} grade={grade} ready={ready} readiness={readiness}
              onReady={onReadyComplete} onNavigate={setTab} onEnterGenerate={onEnterGenerate}
              user={user} onSignOut={onSignOut}
              pendingOpen={pendingOpen} onConsumePending={() => setPendingOpen(null)} />}
        </main>
      </div>

      {/* Mobile bottom-tab bar — the same four destinations as the drawer's main items, always
          reachable without opening the hamburger on a phone. Hidden on desktop widths (CSS). */}
      <nav className="bottom-tabs" aria-label="Primary">
        <button className={`bt-item ${activeNav === "week" ? "on" : ""}`} onClick={goWeek}>
          <span className="bt-ico" aria-hidden="true">📅</span>My Week
        </button>
        <button className={`bt-item ${activeNav === "profile" ? "on" : ""}`} onClick={() => goEdit("profile")}>
          <span className="bt-ico" aria-hidden="true">👥</span>My Class
        </button>
        <button className={`bt-item ${activeNav === "calendar" ? "on" : ""}`} onClick={() => goEdit("calendar")}>
          <span className="bt-ico" aria-hidden="true">🗓</span>Calendar
        </button>
        <button className={`bt-item ${activeNav === "lessonplans" ? "on" : ""}`} onClick={() => goEdit("lessonplans")}>
          <span className="bt-ico" aria-hidden="true">📖</span>Plans
        </button>
      </nav>
    </>
  );
}
