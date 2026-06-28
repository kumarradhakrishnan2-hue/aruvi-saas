"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN, projectReadiness, API, withUser, getUser, setUser, clearUser } from "./lib/format";
import GenerateTab from "./components/GenerateTab";
import MyPlans from "./components/MyPlans";
import StatePill from "./components/StatePill";
import Login from "./components/Login";

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

  return (
    <>
      <header className="hdr">
        <div className="brand">
          <span className="brand-row">Aruvi<em>.</em><small>lesson studio</small></span>
          <span className="brand-ncf">NCF 2023 aligned</span>
        </div>
        <span className="tabs-spacer" />
        <div className="user-chip">
          <span className="uid">{user}</span>
          <button className="signout" onClick={onSignOut}>Sign out</button>
        </div>
      </header>
      <div className="tabs">
        {TABS.map((t) => {
          const locked = t.id === "generate" && !ready;
          return (
            <button
              key={t.id}
              className={`tab ${tab === t.id ? "active" : ""} ${locked ? "locked" : ""}`}
              onClick={() => setTab(t.id)}
            >
              {t.label}{locked ? " 🔒" : ""}
            </button>
          );
        })}
        <span className="tabs-spacer" />
        {/* Subject·grade scope pills are hidden during pre-readiness setup (welcome + grid
            flow are cross-scope, not tied to a subject·grade). */}
        {!(tab === "myplans" && !ready) && (
          <>
            <StatePill
              value={subject}
              options={subjects.map((s) => ({ value: s, label: pretty(s) }))}
              render={pretty(subject)}
              onChange={setSubject}
            />
            <StatePill
              value={grade}
              options={grades.map((g) => ({ value: g, label: gradeUp(g) }))}
              render={grade ? `Grade ${gradeUp(grade)}` : "—"}
              onChange={setGrade}
            />
          </>
        )}
      </div>
      <main>
        {!subject ? <div className="empty">Connecting to the Aruvi engine…</div> :
          tab === "generate" ? <GenerateTab subject={subject} grade={grade} ready={ready} readiness={readiness} onNavigate={setTab} /> :
          <MyPlans subject={subject} grade={grade} ready={ready} readiness={readiness}
            onReady={onReadyComplete} onNavigate={setTab} />}
      </main>
    </>
  );
}
