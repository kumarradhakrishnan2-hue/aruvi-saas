"use client";

import { useEffect, useState } from "react";

/* Header theme control. Cycles Auto → Light → Dark → Auto and drives the saved
   preference through window.__aruviTheme (defined by the no-flash resolver in
   layout.jsx). "Auto" follows the phone's system setting; Light/Dark override it.
   Dark styling itself is mobile-scoped (globals.css), and this button is hidden
   above 600px, so on desktop the app stays on warm paper regardless. */

const ORDER = ["system", "light", "dark"];
const META = {
  system: { glyph: "◐", label: "Theme: Auto (follows your phone)" },
  light: { glyph: "☀", label: "Theme: Light" },
  dark: { glyph: "☾", label: "Theme: Dark" },
};

export default function ThemeToggle() {
  const [pref, setPref] = useState("system");

  useEffect(() => {
    const cur =
      (typeof window !== "undefined" && window.__aruviTheme && window.__aruviTheme.get()) ||
      document.documentElement.getAttribute("data-theme") ||
      "system";
    setPref(cur);
  }, []);

  function cycle() {
    const next = ORDER[(ORDER.indexOf(pref) + 1) % ORDER.length];
    setPref(next);
    if (typeof window !== "undefined" && window.__aruviTheme) window.__aruviTheme.set(next);
  }

  const m = META[pref] || META.system;
  return (
    <button className="hdr-theme" onClick={cycle} aria-label={m.label} title={m.label}>
      <span aria-hidden="true">{m.glyph}</span>
    </button>
  );
}
