"use client";

/* ───────── shared period-schedule input widgets (used by Allocate + Generate) ───────── */
export function Stepper({ value, onChange, min = 0, step = 1 }) {
  const dec = () => onChange(Math.max(min, Number(value || 0) - step));
  const inc = () => onChange(Number(value || 0) + step);
  const onInput = (e) => {
    const raw = e.target.value;
    if (raw === "") { onChange(""); return; }
    if (!/^\d*$/.test(raw)) return; // digits only, but let it be typed freely
    onChange(Number(raw));
  };
  const onBlur = () => { if (value === "" || value == null) onChange(min); };
  return (
    <div className="stepper">
      <button type="button" className="step-btn" onClick={dec} aria-label="decrease">−</button>
      <input
        className="step-in"
        type="text"
        inputMode="numeric"
        pattern="[0-9]*"
        value={value}
        onChange={onInput}
        onBlur={onBlur}
      />
      <button type="button" className="step-btn" onClick={inc} aria-label="increase">+</button>
    </div>
  );
}

function PeriodTypeCard({ row, index, onChange, onRemove, removable }) {
  const upd = (k, v) => onChange({ ...row, [k]: v });
  return (
    <div className="ptcard">
      <div className="ptnum">{index + 1}</div>
      <div className="ptbody">
        <div className="ptmain-row">
          <div className="ptlabel-col">
            <div className="ptlabel">{`Period type ${index + 1}`}</div>
          </div>
          <Stepper value={row.count} min={0} onChange={(v) => upd("count", v)} />
          <span className="ptunit">Periods</span>
          <Stepper value={row.minutes} min={5} step={5} onChange={(v) => upd("minutes", v)} />
          <span className="ptunit">min</span>
          {removable ? (
            <button className="ptdel" title="remove period type" onClick={onRemove}>
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                <polyline points="3 6 5 6 21 6" />
                <path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6" />
                <path d="M10 11v6" />
                <path d="M14 11v6" />
                <path d="M9 6V4a2 2 0 0 1 2-2h2a2 2 0 0 1 2 2v2" />
              </svg>
            </button>
          ) : null}
        </div>
      </div>
    </div>
  );
}

export default function PeriodRows({ rows, setRows }) {
  const upd = (i, next) => setRows(rows.map((r, j) => (j === i ? next : r)));
  const addRow = () => setRows([...rows, { name: "", count: 20, minutes: 60 }]);
  return (
    <div className="ptcards">
      {rows.map((r, i) => (
        <PeriodTypeCard
          key={i}
          row={r}
          index={i}
          onChange={(next) => upd(i, next)}
          removable={rows.length > 1}
          onRemove={() => setRows(rows.filter((_, j) => j !== i))}
        />
      ))}
      <button className="padd" onClick={addRow}>+ Add another period type</button>
    </div>
  );
}

export const toPeriodRows = (rows) => rows.map((r) => ({ minutes: Number(r.minutes), count: Number(r.count) })).filter((r) => r.count > 0 && r.minutes > 0);

/* Map duration (minutes, as used in the allocate-API response, e.g. "60") to the label shown
 * in table column headers. "Period type N" is only a creation-time label on the periods
 * screen — in every downstream table the column is just "Period", with its minutes shown
 * underneath, so this returns a flat generic name for every duration. */
export function periodTypeNames(rows) {
  const out = {};
  rows.forEach((r) => {
    const m = String(Number(r.minutes));
    if (m && m !== "0" && !out[m]) out[m] = "Period";
  });
  return out;
}

export function totalsFinePrint(rows) {
  const valid = toPeriodRows(rows);
  if (!valid.length) return "";
  return valid.map((r) => `${r.minutes} mins × ${r.count}`).join(", ");
}
