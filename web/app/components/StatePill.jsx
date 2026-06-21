"use client";
import { useEffect, useRef, useState } from "react";

/* ───────── state pill (subject / grade selector disguised as a tab) ───────── */
export default function StatePill({ value, options, render, onChange }) {
  const [open, setOpen] = useState(false);
  const ref = useRef(null);

  useEffect(() => {
    if (!open) return;
    const onDoc = (e) => { if (ref.current && !ref.current.contains(e.target)) setOpen(false); };
    const onKey = (e) => { if (e.key === "Escape") setOpen(false); };
    document.addEventListener("mousedown", onDoc);
    document.addEventListener("keydown", onKey);
    return () => { document.removeEventListener("mousedown", onDoc); document.removeEventListener("keydown", onKey); };
  }, [open]);

  const others = options.filter((o) => o.value !== value);

  return (
    <div className="pillwrap" ref={ref}>
      <button className={`tab tab-pill ${open ? "active" : ""}`} onClick={() => setOpen((o) => !o)}>
        {render}<span className="pillcaret">▾</span>
      </button>
      {open ? (
        <div className="pillmenu">
          {others.map((o) => (
            <button
              key={o.value}
              className="pillopt"
              onClick={() => { onChange(o.value); setOpen(false); }}
            >
              {o.label}
            </button>
          ))}
        </div>
      ) : null}
    </div>
  );
}
