"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN } from "./lib/format";
import GenerateTab from "./components/GenerateTab";
import MyPlans from "./components/MyPlans";
import StatePill from "./components/StatePill";

/* ───────── app shell ─────────
 * Two tabs: My Plans (operational home + readiness) and Generate (allocate → generate,
 * folded into one tab). Readiness gates Generate — until it's complete the Generate tab
 * shows a locked/inert state. For now readiness is a front-end flag defaulting to complete;
 * Phase 2 replaces it with real readiness state from the API. */
export default function Home() {
  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");
  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");
  const [tab, setTab] = useState("myplans");
  const [ready, setReady] = useState(false);      // readiness flag — set true on completing setup (Phase 2). Phase 4: from API/DB
  const [readiness, setReadiness] = useState(null); // readiness payload (durations/grids/budget) — feeds G4's weekly ratio

  useEffect(() => { getJSON("/subjects").then((d) => { setSubjects(d.subjects); setSubject(d.subjects.includes("science") ? "science" : d.subjects[0]); }).catch(() => {}); }, []);
  useEffect(() => { if (!subject) return;
    getJSON(`/subjects/${subject}/grades`).then((d) => {
      const gs = [...d.grades].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGrades(gs); setGrade(gs.includes("vii") ? "vii" : gs[0] || "");
    }).catch(() => setGrades([]));
  }, [subject]);

  const TABS = [{ id: "myplans", label: "My Plans" }, { id: "generate", label: "Generate" }];

  return (
    <>
      <header className="hdr">
        <div className="brand">
          <span className="brand-row">Aruvi<em>.</em><small>lesson studio</small></span>
          <span className="brand-ncf">NCF 2023 aligned</span>
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
            onReady={(payload) => { setReadiness(payload); setReady(true); }} onNavigate={setTab} />}
      </main>
    </>
  );
}
