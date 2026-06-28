"use client";

/* ───────── SidebarNav — below-logo information rail (2026-06-28 v5, read-only) ─────────
 * Sits below the Aruvi logo. Same warm-paper colour; NO icons, NO row separators.
 *
 * Three direct links:
 *   • "My Week"     — weekly teaching dashboard (via onWeek), i.e. the My Plans "This week" view.
 *   • "My Class"    — the My Class drill-down (via onEdit("profile")): subjects/grades/sections
 *     and their time facts.
 *   • "My Calendar" — the read-only weekly timetable (via onEdit("calendar")): Grade·Section rows
 *     × weekday columns, coloured by subject/grade.
 *
 * Props: user, onSignOut, onEdit(mode), onWeek().
 */

export default function SidebarNav({ user, onSignOut, onEdit, onWeek }) {
  return (
    <div className="sbn">
      <button className="sbn-item" onClick={() => onWeek && onWeek()}>
        My Week
      </button>
      <button className="sbn-item" onClick={() => onEdit && onEdit("profile")}>
        My Class
      </button>
      <button className="sbn-item" onClick={() => onEdit && onEdit("calendar")}>
        My Calendar
      </button>

      <div className="sbn-foot">
        <button className="sbn-foot-item" onClick={() => {}}>Settings</button>
        <button className="sbn-foot-item" onClick={() => {}}>Help &amp; support</button>
        <div className="sbn-foot-user">
          <div className="sbn-foot-name">{user}</div>
          <button className="sbn-foot-logout" onClick={onSignOut}>Log out</button>
        </div>
      </div>
    </div>
  );
}
