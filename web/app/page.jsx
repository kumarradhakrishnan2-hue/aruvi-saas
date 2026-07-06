"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN, projectReadiness, API, withUser, getUser, setUser, clearUser } from "./lib/format";
import GenerateTab from "./components/GenerateTab";
import MyPlans from "./components/MyPlans";
import StatePill from "./components/StatePill";
import Login from "./components/Login";
import FirstRun from "./components/FirstRun";
import TeachingProfile from "./components/TeachingProfile";
import MyLessonPlans from "./components/MyLessonPlans";
import GuidedTour from "./components/GuidedTour";

/* ───────── app shell ─────────
 * The app is gated behind a user-ID portal (Login). No password yet: the entered ID is the
 * tenant key — stored in localStorage, sent as X-Aruvi-User on every API call, and used by
 * the server to scope all per-teacher state (tenant_id == user_id). This makes the
 * persistence testable across multiple "teachers" and is the exact seam Phase 4 swaps for
 * Supabase Auth.
 *
 * Nav (2026-07-02 restructure): TWO CENTRE TABS — "My Classes" (home: one card per section,
 * pointer-organized) and "My Lessons" (the plan repository). No sidebar, no hamburger, no
 * Calendar, no My Week — Aruvi organizes by the section pointer ("where did I stop?"), never
 * by days (see MEMORY.md 2026-07-02). The teaching profile is parked behind the header's
 * settings gear. Generate is not a tab — it's reached only through "+ Prepare Lesson".
 * Readiness is PERSISTED server-side per user (GET/POST /readiness): the teaching profile
 * (subjects/grades/sections/durations) is loaded when a user signs in, so it survives a
 * refresh, a server restart, or a fresh browser — never lost on session cut. */
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
  const [editFlow, setEditFlow] = useState(null);  // "profile" (settings gear) | "lessonplans" (My Lessons tab) | null (My Classes home)
  const [profileAutoAdd, setProfileAutoAdd] = useState(null);  // subject NAME to auto-launch the add-a-class flow for (from the My Classes "expand classes" prompt)
  const [profilePortal, setProfilePortal] = useState(null);  // "subject" | "class" | "section" — one-shot intent from My Classes' standing "+" portal
  const [pendingOpen, setPendingOpen] = useState(null);  // {subject,grade,sectionTag,filename} — deep-link from Track into My Week
  // How the Generate tab should open this time:
  //   { mode: "pick" }                     → show the G1.9 subject·grade picker (multi-choice)
  //   { mode: "scoped", subject, grade }   → skip picker, go straight in for that subject·grade
  // Cleared once Generate consumes it. Generate is only ever reached through this handler.
  const [generateEntry, setGenerateEntry] = useState(null);

  /* First-run guided tour (restructured 2026-07-06). `tour` is the current step, 1–11 (or null);
   * the walk is launched from the "Show me how" nudge on My Classes and is GUIDE-DRIVEN: every
   * step advances with Next / reverses with Back, and the transitions here perform whatever the
   * step implies (tab navigation, opening the preview, the real attach — done inside MyPlans —
   * opening the popup, the profile). `tourInfo` carries the target section tag + chapter title
   * (reported up by MyPlans) so the step copy can name them.
   *
   * WHY skip is SESSION-ONLY, not a persisted flag (fixed 2026-07-06, kumar23): the tour offer is
   * gated by SERVER-DERIVED first-run state — MyPlans shows the nudge only while a lesson is
   * prepared but nothing is attached yet (`!anyBound && anyPlans`), which self-closes forever the
   * moment she attaches. A standalone per-user localStorage "tour done" flag is exactly the desync
   * trap the activation-flag note (top of file) warns about: deleting a test user's profile server-
   * side left the stale browser flag behind, so the fresh first run never re-offered the guide.
   * So skipping only hides it for THIS session (in-memory); a fresh login re-derives from the
   * server. Once attached, the server state itself stops the offer — no client flag needed. */
  const [tour, setTour] = useState(null);
  const [tourInfo, setTourInfo] = useState(null);   // { tag, chapter } from MyPlans
  const [tourDismissed, setTourDismissed] = useState(false);   // session-only; never persisted
  const finishTour = () => { setTour(null); setTourDismissed(true); };
  const startTour = () => setTour(1);

  // On mount, restore the signed-in user from localStorage (survives refresh).
  useEffect(() => { setUserState(getUser()); }, []);

  // Freeze the top chrome (sticky header + tabs, then the My Classes greeting) while the card
  // list scrolls beneath. Publish the measured header height and header+tabs height as CSS vars
  // so the sticky offsets stay exact across breakpoints and the two-line brand — no magic numbers.
  useEffect(() => {
    const setVars = () => {
      const root = document.documentElement;
      const h = document.querySelector(".hdr");
      const t = document.querySelector(".main-tabs");
      const hh = h ? Math.round(h.getBoundingClientRect().height) : 0;
      const th = t ? Math.round(t.getBoundingClientRect().height) : 0;
      if (h) root.style.setProperty("--hdr-h", `${hh}px`);
      if (h && t) root.style.setProperty("--nav-h", `${hh + th}px`);
    };
    setVars();
    window.addEventListener("resize", setVars);
    return () => window.removeEventListener("resize", setVars);
  }, [ready, tab, editFlow, user]);

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
    setSubjects([]); setSubject(""); setTab("myplans"); setEditFlow(null);
    setTour(null); setTourDismissed(false);
  };

  // The three destinations: the two centre tabs + the settings gear. Each leaves any
  // in-progress Generate flow and clears its pending entry/scope.
  const goClasses = () => { setEditFlow(null); setTab("myplans"); setGenerateEntry(null); };
  const goLessons = () => { setEditFlow("lessonplans"); setTab("myplans"); setGenerateEntry(null); };

  // Tour Next — the guide performs the move each step implies before advancing. The view-level
  // work (popup at 6/11, attach/unbind at the 6↔7 boundary, lesson at 8–9, demo-complete at
  // 10–11) is orchestrated by MyPlans/MyLessonPlans off the numeric tourStep; here we only
  // handle SHELL navigation: 2→3 open My Lessons · 4→5 back to My Classes · 11→12 open the
  // profile (step 12 rings the settings gear over it) · 12 Done.
  const tourNext = () => {
    if (tour === 2) goLessons();
    else if (tour === 4) goClasses();
    else if (tour === 11) goProfile();
    else if (tour === 12) { finishTour(); goClasses(); return; }
    setTour(tour + 1);
  };
  // Tour Back — mirrors every move so each step reverses cleanly: 3→2 back to My Classes' tab
  // highlight; 5→4 back to My Lessons (the preview re-opens there); 12→11 back to My Classes
  // (the popup re-opens). Back from step 1 backs out to the nudge.
  const tourBack = () => {
    if (tour === 1) { setTour(null); return; }
    if (tour === 3) goClasses();
    else if (tour === 5) goLessons();
    else if (tour === 12) goClasses();
    setTour(tour - 1);
  };
  const goProfile = () => { setProfileAutoAdd(null); setProfilePortal(null); setEditFlow("profile"); setTab("myplans"); setGenerateEntry(null); };
  // From the My Classes "add more classes in this subject" prompt: open the teaching profile and
  // auto-launch its existing add-a-class flow scoped to that subject (sections → durations →
  // periods/week → annual budget per new class). TeachingProfile consumes the directive once.
  const onExpandClasses = (subjectName) => {
    setProfileAutoAdd(subjectName); setProfilePortal(null); setEditFlow("profile"); setTab("myplans"); setGenerateEntry(null);
  };
  // From My Classes' standing "+" portal (founder, 2026-07-06): open the teaching profile with a
  // one-shot intent — "subject" | "class" | "section" — and TeachingProfile launches the matching
  // manage screen (add AND remove, same flows the gear uses). Consumed once, like profileAutoAdd.
  const onProfilePortal = (kind) => {
    setProfileAutoAdd(null); setProfilePortal(kind); setEditFlow("profile"); setTab("myplans"); setGenerateEntry(null);
  };
  // Which centre tab lights up: My Lessons only when the repository is open; the profile
  // (settings) view lights neither; everything else — home cards, Generate — reads as My Classes.
  const activeNav = editFlow === "lessonplans" ? "lessons" : editFlow === "profile" ? "none" : "classes";

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
      {/* Shell header: the brand exactly as the first-run page renders it (Aruvi + red dot,
          LESSON STUDIO tag beneath); settings gear (→ teaching profile) + log out right. No
          hamburger, no drawer — the two tabs below the header are the whole nav. */}
      <header className="hdr">
        <div className="brand">
          <span className="brand-row">Aruvi<em>.</em></span>
          <span className="hdr-brand-tag">lesson studio</span>
        </div>
        <div className="hdr-user">
          <span className="hdr-user-name">{user}</span>
          <button className="hdr-gear" onClick={goProfile} aria-label="Settings" title="Settings"
            data-tour="settings-gear">⚙</button>
          <button className="hdr-user-logout" onClick={onSignOut}>Log out</button>
        </div>
      </header>

      {/* The two tabs — the app's entire nav, at the TOP (under the header), active tab
          marked with the same clay-red underline the original My Plans/Generate tabs used.
          Nouns only: My Classes (where did I stop?) and My Lessons (the plan repository).
          "+ Prepare Lesson" is a verb, so it lives as an action inside both views, never here. */}
      <nav className="tabs main-tabs" aria-label="Primary">
        <button className={`tab ${activeNav === "classes" ? "active" : ""}`} onClick={goClasses}
          data-tour="nav-classes">
          My Classes
        </button>
        <button className={`tab ${activeNav === "lessons" ? "active" : ""}`} onClick={goLessons}
          data-tour="nav-lessons">
          My Lessons
        </button>
      </nav>

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
          {/* Edit-flow views (My Lessons / teaching profile) require a set-up profile. A
           * not-ready user is always routed to the setup flow instead of a dead-end empty
           * view — readiness gates these the same way it gates Generate. */}
          {(editFlow === "lessonplans" && ready) ? (
            /* My Lessons — the plan repository (subject → grade → chapter). */
            <div className="editflow">
              <MyLessonPlans readiness={readiness} onAllocate={onAllocateScoped} onOpenSection={onOpenSection}
                tourStep={tour} />
            </div>
          ) : (editFlow === "profile" && ready) ? (
            /* Teaching profile (via the settings gear) — view + conversational redo (the SAME
             * first-run UI, answers pre-filled) + delete. The MyClasses drill-down is retired.
             * Deleting clears pointers (lessons stay) and drops her STRAIGHT into the redo
             * flow inside this same view — the shell stays open; `ready` is untouched. A
             * signed-out return without rebuilding hits first run naturally (server profile
             * is gone, so GET /readiness comes back empty). */
            <div className="editflow" data-tour="profile-root">
              <TeachingProfile readiness={readiness} onChange={setReadiness} onBack={goClasses}
                autoAddClassSubject={profileAutoAdd} onConsumeAutoAdd={() => setProfileAutoAdd(null)}
                portalIntent={profilePortal} onConsumePortal={() => setProfilePortal(null)} />
            </div>
          ) :
            !subject ? <div className="empty">Connecting to the Aruvi engine…</div> :
            tab === "generate" ? <GenerateTab subject={subject} grade={grade} ready={ready} readiness={readiness}
              onNavigate={setTab} entry={generateEntry} onScope={(s, g) => { setSubject(s); setGrade(g); }}
              onConsumeEntry={() => setGenerateEntry(null)} /> :
            <MyPlans subject={subject} grade={grade} ready={ready} readiness={readiness}
              onReady={onReadyComplete} onNavigate={setTab} onEnterGenerate={onEnterGenerate}
              user={user} onSignOut={onSignOut}
              pendingOpen={pendingOpen} onConsumePending={() => setPendingOpen(null)}
              onStartTour={tourDismissed ? undefined : startTour}
              tourActive={!!tour} tourStep={tour}
              onTourInfo={setTourInfo} onExpandClasses={onExpandClasses} onProfilePortal={onProfilePortal} />}
        </main>
      </div>

      {/* First-run guided tour overlay — 12 guide-driven steps ("N of 12", Back on every one).
          Skip closes it for this session. */}
      {tour && (
        <GuidedTour step={tour} info={tourInfo} onNext={tourNext} onBack={tourBack} onSkip={finishTour} />
      )}

    </>
  );
}
