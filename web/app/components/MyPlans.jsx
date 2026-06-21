"use client";
import { useEffect, useState } from "react";
import { getJSON, pad } from "../lib/format";
import ViewModelView from "./ViewModelView";

export default function MyPlans({ subject, grade }) {
  const [plans, setPlans] = useState([]);
  const [view, setView] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => { setView(null);
    getJSON(`/plans/${subject}/${grade}`).then((d) => setPlans(d.plans)).catch(() => setPlans([]));
  }, [subject, grade]);

  const open = async (fn) => { setLoading(true);
    try { setView((await getJSON(`/plans/${subject}/${grade}/${fn}/view`)).view); } finally { setLoading(false); }
  };

  if (loading) return <div className="spin">Opening plan…</div>;
  if (view) return (<div><button className="back" onClick={() => setView(null)}>← all plans</button><ViewModelView view={view} /></div>);
  return (
    <div>
      <p className="h2">{plans.length} saved plan{plans.length === 1 ? "" : "s"}.</p>
      {plans.map((p) => (
        <div className="plan-row" key={p.filename} onClick={() => open(p.filename)}>
          <span className="plan-num">CH {pad(p.chapter_number)}</span>
          <span className="plan-title">{p.chapter_title}</span>
          <span className="plan-date">{(p.saved_at || "").slice(0, 10)}</span>
        </div>
      ))}
      {!plans.length && <div className="empty">No saved plans for this subject &amp; grade yet.</div>}
    </div>
  );
}
