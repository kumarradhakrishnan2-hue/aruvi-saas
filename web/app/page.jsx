"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN, projectReadiness, API, withUser, getUser, setUser, clearUser } from "./lib/format";
import GenerateTab from "./components/GenerateTab";
import MyPlans from "./components/MyPlans";
import StatePill from "./components/StatePill";
import Login from "./components/Login";
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
  const [navCollapsed, setNavCollapsed] = useState(false); // below-logo sidebar collapse state
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
    setReady(false); setReadiness(null);
    getJSON("/readiness").then((d) => {
      if (d && d.ready && d.readiness) {
        setReadiness(projectReadiness(d.readiness));
        setReady(true);
      }
    }).catch(() => {});  // no saved profile / API down → stay in the not-ready setup flow
  }, [user]);

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
    setReady(false); setReadiness(null); setSubjects([]); setSubject(""); setTab("myplans");
  };

  // Still restoring from localStorage — render nothing for a beat (no login flash).
  if (user === null) return null;
  // Not signed in → the portal.
  if (!user) return <Login onEnter={onEnter} />;

  const TABS = [{ id: "myplans", label: "My Plans" }, { id: "generate", label: "Generate" }];

  // The below-logo rail exists only once a profile is set up; open by default, collapsible.
  const navOpen = ready && !navCollapsed;

  return (
    <>
      <header className="hdr">
        <div className="brand">
          <span className="brand-row">Aruvi<em>.</em><small>lesson studio</small></span>
          <span className="brand-ncf">NCF 2023 aligned</span>
        </div>
        {user && (
          <div className="hdr-user">
            <span className="hdr-user-name">{user}</span>
            <button className="hdr-user-logout" onClick={onSignOut}>Log out</button>
          </div>
        )}
      </header>

      <div className={`body ${navOpen ? "nav-open" : ""}`}>
        {navOpen && (
          <aside className="bodyrail">
            <button className="rail-collapse" onClick={() => setNavCollapsed(true)} aria-label="Collapse menu">‹</button>
            {/* Any sidebar view (My Class / Calendar / Lesson Plans) leaves the Generate flow and
                sits under My Plans — reset the tab + clear any pending Generate entry/scope pills. */}
            <SidebarNav onEdit={(mode) => { setEditFlow(mode); setTab("myplans"); setGenerateEntry(null); }}
              onWeek={() => { setEditFlow(null); setTab("myplans"); setGenerateEntry(null); }}
              user={user} onSignOut={onSignOut}
              active={editFlow === "profile" ? "profile" : editFlow === "calendar" ? "calendar" : editFlow === "lessonplans" ? "lessonplans" : "week"} />
          </aside>
        )}

        <div className="bodycontent">
          <div className="tabs">
            {ready && navCollapsed && (
              <button className="hamb" onClick={() => setNavCollapsed(false)} aria-label="Open menu">
                <span /><span /><span />
              </button>
            )}
            {TABS.map((t) => {
              const locked = t.id === "generate" && !ready;
              // Direct Generate-tab click = scope-less entry → run the picker (onEnterGenerate
              // with no opts; it auto-scopes only when there's a single subject AND grade).
              const go = () => { if (t.id === "generate" && ready) onEnterGenerate(); else setTab(t.id); };
              return (
                <button key={t.id}
                  className={`tab ${tab === t.id ? "active" : ""} ${locked ? "locked" : ""}`}
                  onClick={go}>
                  {t.label}{locked ? " 🔒" : ""}
                </button>
              );
            })}
            {/* Subject·grade scope pills belong to the Generate tab only — they have no role
             * in My Plans. Pushed to the right of the tab row by the spacer, same row as tabs. */}
            {tab === "generate" && ready && (
              <>
                <span className="tabs-spacer" />
                <div className="hdr-scope">
                  <StatePill value={subject} options={subjects.map((s) => ({ value: s, label: pretty(s) }))}
                    render={pretty(subject)} onChange={setSubject} />
                  <StatePill value={grade} options={grades.map((g) => ({ value: g, label: gradeUp(g) }))}
                    render={grade ? `Grade ${gradeUp(grade)}` : "—"} onChange={setGrade} />
                </div>
              </>
            )}
          </div>

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
      </div>
    </>
  );
}
