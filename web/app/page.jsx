"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN } from "./lib/format";
import Allocate from "./components/Allocate";
import Generate from "./components/Generate";
import MyPlans from "./components/MyPlans";
import StatePill from "./components/StatePill";

/* ───────── app shell ───────── */
export default function Home() {
  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");
  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");
  const [tab, setTab] = useState("allocate");

  useEffect(() => { getJSON("/subjects").then((d) => { setSubjects(d.subjects); setSubject(d.subjects.includes("science") ? "science" : d.subjects[0]); }).catch(() => {}); }, []);
  useEffect(() => { if (!subject) return;
    getJSON(`/subjects/${subject}/grades`).then((d) => {
      const gs = [...d.grades].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGrades(gs); setGrade(gs.includes("vii") ? "vii" : gs[0] || "");
    }).catch(() => setGrades([]));
  }, [subject]);

  return (
    <>
      <header className="hdr">
        <div className="brand">
          <span className="brand-row">Aruvi<em>.</em><small>lesson studio</small></span>
          <span className="brand-ncf">NCF 2023 aligned</span>
        </div>
      </header>
      <div className="tabs">
        {["allocate", "generate", "myplans"].map((t) => (
          <button key={t} className={`tab ${tab === t ? "active" : ""}`} onClick={() => setTab(t)}>
            {t === "myplans" ? "My Plans" : t}
          </button>
        ))}
        <span className="tabs-spacer" />
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
      </div>
      <main>
        {!subject ? <div className="empty">Connecting to the Aruvi engine…</div> :
          tab === "allocate" ? <Allocate subject={subject} grade={grade} /> :
          tab === "generate" ? <Generate subject={subject} grade={grade} /> :
          <MyPlans subject={subject} grade={grade} />}
      </main>
    </>
  );
}
