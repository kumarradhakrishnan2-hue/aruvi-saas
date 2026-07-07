import "./globals.css";

export const metadata = {
  title: "Aruvi",
  description: "NCF-aligned lesson plans & assessments",
};

export const viewport = {
  width: "device-width",
  initialScale: 1,
};

/* No-flash theme resolver. Runs before the app paints: reads the saved
   preference (Auto/Light/Dark) + the OS setting, writes the effective theme to
   <html data-theme-effective> (what globals.css keys off), and exposes
   window.__aruviTheme for ThemeToggle.jsx. Default is "system" (follow phone). */
const THEME_SCRIPT = `
(function(){
  try {
    var pref = localStorage.getItem('aruvi-theme') || 'system';
    var mql = window.matchMedia('(prefers-color-scheme: dark)');
    function eff(){ return pref === 'system' ? (mql.matches ? 'dark' : 'light') : pref; }
    function apply(){
      var d = document.documentElement;
      d.setAttribute('data-theme', pref);
      d.setAttribute('data-theme-effective', eff());
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
