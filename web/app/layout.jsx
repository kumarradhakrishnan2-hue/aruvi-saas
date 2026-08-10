import "./globals.css";

export const metadata = {
  title: "Aruvi",
  description: "NCF-aligned lesson plans & assessments",
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
  /* Lets the page extend under the iPhone notch/status bar so env(safe-area-inset-top)
     resolves to a real value — .topbar pads itself by it and owns that strip with the pine
     fill. Without this the env() is 0 and the padding a no-op. */
  viewportFit: "cover",
  /* Paints the status-bar region ABOVE the page (which CSS cannot reach when the safe-area
     inset is 0, e.g. a home-screen icon added before viewport-fit=cover) in the top bar's
     own pine, so the strip and the bar read as one surface. Values must track --bar-fill in
     globals.css: #164436 light, #14332a dark. THEME_SCRIPT below re-syncs these when the
     in-app theme override differs from the OS setting. */
  themeColor: [
    { media: "(prefers-color-scheme: dark)", color: "#14332a" },
    { color: "#164436" },
  ],
};

/* No-flash theme resolver. Runs before the app paints: reads the saved
   preference (Auto/Light/Dark) + the OS setting, writes the effective theme to
   <html data-theme-effective> (what globals.css keys off), and exposes
   window.__aruviTheme for ThemeToggle.jsx. Default is "system" (follow phone). */
const THEME_SCRIPT = `
(function(){
  /* Always open at the top. A home-screen (standalone) iPhone web app restores the scroll
     position it was left at when it is relaunched, so Aruvi could come up mid-page with the
     brand row already scrolled past — "hidden until I scroll". We own the entry point. */
  try { if ('scrollRestoration' in history) history.scrollRestoration = 'manual'; } catch(e){}
  try {
    var pref = localStorage.getItem('aruvi-theme') || 'system';
    var mql = window.matchMedia('(prefers-color-scheme: dark)');
    function eff(){ return pref === 'system' ? (mql.matches ? 'dark' : 'light') : pref; }
    function apply(){
      var d = document.documentElement;
      d.setAttribute('data-theme', pref);
      d.setAttribute('data-theme-effective', eff());
      /* Status-bar tint must follow the EFFECTIVE theme (the in-app override can differ from
         the OS setting the meta's media attribute tracks). Values = --bar-fill per theme. */
      try {
        var c = eff() === 'dark' ? '#14332a' : '#164436';
        document.querySelectorAll('meta[name="theme-color"]').forEach(function(m){
          m.removeAttribute('media'); m.setAttribute('content', c);
        });
      } catch(e){}
    }
    apply();
    window.__aruviTheme = {
      get: function(){ return pref; },
      set: function(p){ pref = p; try { localStorage.setItem('aruvi-theme', p); } catch(e){} apply(); }
    };
    var onChange = function(){ if (pref === 'system') apply(); };
    if (mql.addEventListener) mql.addEventListener('change', onChange);
    else if (mql.addListener) mql.addListener(onChange);
  } catch(e){}
})();
`;

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>
        <script dangerouslySetInnerHTML={{ __html: THEME_SCRIPT }} />
        {children}
      </body>
    </html>
  );
}
