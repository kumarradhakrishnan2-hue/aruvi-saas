"use client";

/* ───────── SidebarNav — Phase 2 overlay-drawer contents ("side bar.jpg", 2026-07-02) ─────────
 * Rendered inside page.jsx's <aside className="drawer"> (brand + close button live in the
 * drawer's own header, not here). Same warm-paper colour, icons added so items read as a
 * proper nav list rather than plain links.
 *
 * Direct links, in logical order (this week first — it's Home now — then setup → schedule → resources):
 *   • "My Week"     — weekly teaching dashboard (via onWeek), i.e. the My Plans home view.
 *   • "My Class"    — the My Class drill-down (via onEdit("profile")): subjects/grades/sections
 *     and their time facts.
 *   • "My Calendar" — the read-only weekly timetable (via onEdit("calendar")): Grade·Section rows
 *     × weekday columns, coloured by subject/grade.
 *   • "My Lesson Plans" — the technical resource library (via onEdit("lessonplans")):
 *     subject → grade → chapter, mirroring the lesson viewer hierarchy.
 *
 * Props: user, onSignOut, onEdit(mode), onWeek(), active ("week" | "profile" | "calendar" | "lessonplans").
 *   `active` marks the current view with the same clay rule the old top tabs used.
 */

const ITEMS = [
  { key: "week", label: "My Week", icon: "📅", action: "week" },
  { key: "profile", label: "My Class", icon: "👥", action: "profile" },
  { key: "calendar", label: "My Calendar", icon: "🗓", action: "calendar" },
  { key: "lessonplans", label: "My Lesson Plans", icon: "📖", action: "lessonplans" },
];

function initialsFor(user) {
  const s = (user || "").trim();
  if (!s) return "?";
  return s.slice(0, 2).toUpperCase();
}

export default function SidebarNav({ user, onSignOut, onEdit, onWeek, active }) {
  return (
    <div className="sbn">
      {ITEMS.map((it) => (
        <button
          key={it.key}
          className={`sbn-item ${active === it.key ? "active" : ""}`}
          onClick={() => (it.action === "week" ? onWeek && onWeek() : onEdit && onEdit(it.action))}
        >
          <span className="sbn-item-label">
            <span className="sbn-item-ico" aria-hidden="true">{it.icon}</span>
            {it.label}
          </span>
        </button>
      ))}

      <div className="sbn-foot">
        <button className="sbn-foot-item" onClick={() => {}}>
          <span className="sbn-item-ico" aria-hidden="true">⚙️</span>Settings
        </button>
        <button className="sbn-foot-item" onClick={() => {}}>
          <span className="sbn-item-ico" aria-hidden="true">❓</span>Help &amp; support
        </button>

        {user && (
          <div className="sbn-foot-user">
            <div className="sbn-foot-user-row">
              <span className="sbn-avatar" aria-hidden="true">{initialsFor(user)}</span>
              <span className="sbn-foot-name">{user}</span>
            </div>
            <button className="sbn-foot-logout" onClick={onSignOut}>Log out</button>
          </div>
        )}
      </div>
    </div>
  );
}
