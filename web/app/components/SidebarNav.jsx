"use client";

/* ───────── SidebarNav — below-logo information rail (2026-06-28 v5, read-only) ─────────
 * Sits below the Aruvi logo. Same warm-paper colour; NO icons, NO row separators.
 *
 * Direct links, in logical order (setup → schedule → this week → resources):
 *   • "My Class"    — the My Class drill-down (via onEdit("profile")): subjects/grades/sections
 *     and their time facts.
 *   • "My Calendar" — the read-only weekly timetable (via onEdit("calendar")): Grade·Section rows
 *     × weekday columns, coloured by subject/grade.
 *   • "My Week"     — weekly teaching dashboard (via onWeek), i.e. the My Plans "This week" view.
 *   • "My Lesson Plans" — the technical resource library (via onEdit("lessonplans")):
 *     subject → grade → chapter, mirroring the lesson viewer hierarchy.
 *
 * Props: user, onSignOut, onEdit(mode), onWeek(), active ("week" | "profile" | "calendar" | "lessonplans").
 *   `active` marks the current view with the same clay rule the top tabs use.
 */

export default function SidebarNav({ user, onSignOut, onEdit, onWeek, active }) {
  return (
    <div className="sbn">
      <button className={`sbn-item ${active === "profile" ? "active" : ""}`} onClick={() => onEdit && onEdit("profile")}>
        My Class
      </button>
      <button className={`sbn-item ${active === "calendar" ? "active" : ""}`} onClick={() => onEdit && onEdit("calendar")}>
        My Calendar
      </button>
      <button className={`sbn-item ${active === "week" ? "active" : ""}`} onClick={() => onWeek && onWeek()}>
        My Week
      </button>
      <button className={`sbn-item ${active === "lessonplans" ? "active" : ""}`} onClick={() => onEdit && onEdit("lessonplans")}>
        My Lesson Plans
      </button>

      <div className="sbn-foot">
        <button className="sbn-foot-item" onClick={() => {}}>Settings</button>
        <button className="sbn-foot-item" onClick={() => {}}>Help &amp; support</button>
      </div>
    </div>
  );
}
