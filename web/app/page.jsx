"use client";
import { useEffect, useState } from "react";
import { getJSON, pretty, gradeUp, ROMAN, projectReadiness, API, withUser, getUser, setUser, clearUser } from "./lib/format";
import { verifiedWrite, readinessFingerprint } from "./lib/verify";
import { setSectionMismatchHandler, pullSectionState } from "./lib/sectionState";
import GenerateTab from "./components/GenerateTab";
import MyPlans from "./components/MyPlans";
import Login from "./components/Login";
import FirstRun from "./components/FirstRun";
import TeachingProfile from "./components/TeachingProfile";
import MyLessonPlans from "./components/MyLessonPlans";
import GuidedTour from "./components/GuidedTour";
import ThemeToggle from "./components/ThemeToggle";
import AskAruvi from "./ask-aruvi/AskAruvi";

/* ───────── app shell ─────────
 * The app is gated behind a user-ID portal (Login). No password yet: the entered ID is the
 * tenant key — stored in localStorage, sent as X-Aruvi-User on every API call, and used by
 * the server to scope all per-teacher state (tenant_id == user_id). This makes the
 * persistence testable across multiple "teachers" and is the exact seam Phase 4 swaps for
 * Supabase Auth.
 *
 * Nav (2026-07-02 restructure): TWO CENTRE TABS — "My Classes" (home: one card per section,
 * pointer-organized) and "My Lessons" (the plan repository). No sidebar, no hamburger, no
 * Calendar, no My Week — Aruvi organizes by the section pointer ("where did I stop?"), never
 * by days (see MEMORY.md 2026-07-02). The teaching profile is parked behind the header's
 * settings gear. Generate is not a tab — it's reached only through "+ Prepare Lesson".
 * Readiness is PERSISTED server-side per user (GET/POST /readiness): the teaching profile
 * (subjects/grades/sections/durations) is loaded when a user signs in, so it survives a
 * refresh, a server restart, or a fresh browser — never lost on session cut. */
/* Activation gate (Phase 1, §0): the shell stays hidden until the teacher has completed the
 * guided first run. This USED to be tracked as a separate localStorage flag per user — but
 * that flag was purely client-side and could desync from the server: e.g. deleting a test
 * user's profile/allocations server-side left the browser's stale "activated" flag in place,
 * so she'd skip straight to a now-empty shell instead of being sent back through FirstRun
 * (found testing kumar3, 2026-07-02). Fixed by dropping the separate flag entirely — `ready`
 * (rehydrated from the real GET /readiness response) is now the SOLE activation signal, since
 * FirstRun's finishActivation always produces a real subjects[] payload before calling
 * onComplete. One source of truth, server-side, never stale. */

export default function Home() {
  // null = "haven't checked localStorage yet" (avoids a login-screen flash on refresh).
  const [user, setUserState] = useState(null);
  const [subjects, setSubjects] = useState([]);
  const [subject, setSubject] = useState("");
  const [grades, setGrades] = useState([]);
  const [grade, setGrade] = useState("");
  const [tab, setTab] = useState("myplans");
  const [ready, setReady] = useState(false);      // readiness flag — rehydrated per user from GET /readiness
  const [readiness, setReadiness] = useState(null); // readiness projection (durations/grids/budget) — feeds G4's weekly ratio
  const [readinessLoaded, setReadinessLoaded] = useState(false); // has GET /readiness resolved? (gates the first-run decision, avoids a flash)
  const [editFlow, setEditFlow] = useState(null);  // "profile" (settings gear) | "lessonplans" (My Lessons tab) | null (My Classes home)
  const [profileAutoAdd, setProfileAutoAdd] = useState(null);  // subject NAME to auto-launch the add-a-class flow for. ALWAYS null since 2026-08-21 (its only caller, the "expand classes" prompt)
  const [profilePortal, setProfilePortal] = useState(null);  // "subject" | "class" | "section" — one-shot intent from My Classes' standing "+" portal
  const [pendingOpen, setPendingOpen] = useState(null);  // {subject,grade,sectionTag,filename} — deep-link from Track into My Week
  // Where a Prepare-a-lesson flow should RETURN once the chapter is prepared. Set when Prepare is
  // launched from a section's attach popup; consumed by onPrepared to reopen that popup (now
  // listing the new chapter) instead of dumping the teacher into the lesson plan.
  const [prepareReturn, setPrepareReturn] = useState(null);  // { subject, grade, sectionTag } | null
  const [pendingAttach, setPendingAttach] = useState(null);  // {subject,grade,sectionTag,filename} — reopen the attach popup in My Classes
  // How the Generate tab should open this time:
  //   { mode: "pick" }                     → show the G1.9 subject·grade picker (multi-choice)
  //   { mode: "scoped", subject, grade }   → skip picker, go straight in for that subject·grade
  // Cleared once Generate consumes it. Generate is only ever reached through this handler.
  const [generateEntry, setGenerateEntry] = useState(null);
  const [askOpen, setAskOpen] = useState(false);   // Ask Aruvi Q&A screen (? on the tab row)

  /* First-run guided tour (restructured 2026-07-06; extended to 17 steps 2026-07-23). `tour` is the current step, 1–17 (or null);
   * the walk is launched from the "Show me how" nudge on My Classes and is GUIDE-DRIVEN: every
   * step advances with Next / reverses with Back, and the transitions here perform whatever the
   * step implies (tab navigation, opening the preview, the real attach — done inside MyPlans —
   * opening the popup, the profile). `tourInfo` carries the target section tag + chapter title
   * (reported up by MyPlans) so the step copy can name them.
   *
   * WHY skip is SESSION-ONLY, not a persisted flag (fixed 2026-07-06, kumar23): the tour offer is
   * gated by SERVER-DERIVED first-run state — MyPlans shows the nudge only while a lesson is
   * prepared but nothing is attached yet (`!anyBound && anyPlans`), which self-closes forever the
   * moment she attaches. A standalone per-user localStorage "tour done" flag is exactly the desync
   * trap the activation-flag note (top of file) warns about: deleting a test user's profile server-
   * side left the stale browser flag behind, so the fresh first run never re-offered the guide.
   * So skipping only hides it for THIS session (in-memory); a fresh login re-derives from the
   * server. Once attached, the server state itself stops the offer — no client flag needed. */
  const [tour, setTour] = useState(null);
  const [tourInfo, setTourInfo] = useState(null);   // { tag, chapter } from MyPlans
  const [tourDismissed, setTourDismissed] = useState(false);   // session-only; never persisted
  // Also closes Ask Aruvi: Skip can be pressed on step 18 while the panel is open, and the
  // tour must never leave the shell in a state it opened.
  /* ★ Ending the tour asks her to check her sections (founder, 2026-08-21). First run no longer
     ASKS which sections she teaches — it states a default ("we'll start you with Section 9A")
     because the question was too much to put in front of a brand-new teacher. That default can
     of course be wrong, and by the end of the tour she knows exactly what a section is and has
     watched one being tracked — so this is the first moment the question is cheap to answer.
     It rides finishTour, which is the SINGLE exit for both endings: "Done ✓" on the last step
     and "Skip" from any step. Session-only, like tourDismissed — it is a prompt, not a gate. */
  const [sectionCheck, setSectionCheck] = useState(false);
  /* EVERY ending lands on My Classes (founder, 2026-08-21). Done, Skip and the ✕ all route
     through here, and none of them used to navigate — so skipping from steps 3–7, which run on
     My Lessons, left her there, and the prompt below (which renders inside MyPlans) had no host
     to render in. She reported exactly that: "skip … lands in My Lessons with My Classes
     remaining empty". My Classes is also where the payoff now is, since the first lesson is
     bound to her section. */
  const finishTour = () => {
    setAskOpen(false); setTour(null); setTourDismissed(true);
    goClasses();
    setSectionCheck(true);
  };
  /* The tour opens on My Classes. It always did implicitly, because its only entry point was a
     nudge ON My Classes; now that first run lands on My Lessons and the same nudge renders
     there too, step 1 ("this is where your classes sit") would otherwise ring the My Classes
     tab over the My Lessons view. Navigate first, then start. */
  const startTour = () => { goClasses(); setTour(1); };

  // Areas 4 + 5: a VERIFIED section mismatch — the class is not on the chapter she just
  // attached, or not marked complete. pushSectionState calls this only when the server was read
  // back and disagrees; never on a throw, never when unreachable. Re-pull so the cards show the
  // truth, then say one sentence.
  const [sectionFailed, setSectionFailed] = useState("");
  useEffect(() => {
    setSectionMismatchHandler((sectionKey) => {
      pullSectionState([sectionKey]).finally(() => {
        setSectionFailed("That didn’t save — your classes are as Aruvi has them.");
      });
    });
    return () => setSectionMismatchHandler(null);
  }, []);

  // On mount, restore the signed-in user from localStorage (survives refresh).
  useEffect(() => { setUserState(getUser()); }, []);

  // App-shell scroll ownership (2026-08-09): while the signed-in shell is up, the document
  // never scrolls — html.app-shell (globals.css) locks html/body to the viewport and makes
  // .bodycontent the one scroll container, so the top bar is plain static flow that CANNOT
  // scroll away. This exists because the standalone iPhone webview dropped both sticky AND
  // fixed positioning on the document scroller. Login/first-run keep document scrolling.
  useEffect(() => {
    const on = !!(user && ready);
    document.documentElement.classList.toggle("app-shell", on);
    return () => document.documentElement.classList.remove("app-shell");
  }, [user, ready]);

  // Freeze the top chrome (the fixed .topbar, then the My Classes greeting) while the card
  // list scrolls beneath. Publish two CSS vars so every inner sticky offset stays exact across
  // breakpoints and the two-line brand — no magic numbers:
  //   --nav-h  the FULL height of the frozen bar (what inner stickies sit under)
  //   --hdr-h  the brand row's underside (AskAruvi's scrim hangs off this)
  // Both are measured RELATIVE TO .topbar's top edge, so the safe-area inset a home-screen
  // iPhone adds above the brand row is counted once and only once. ResizeObserver as well as
  // resize: fonts landing late or the status-bar inset changing must not leave stale offsets.
  useEffect(() => {
    const root = document.documentElement;
    const bar = document.querySelector(".topbar");
    const setVars = () => {
      const b = document.querySelector(".topbar");
      const h = document.querySelector(".hdr");
      if (!b) return;
      const bt = b.getBoundingClientRect();
      if (h) root.style.setProperty("--hdr-h", `${Math.round(h.getBoundingClientRect().bottom - bt.top)}px`);
      root.style.setProperty("--nav-h", `${Math.round(bt.height)}px`);
    };
    setVars();
    window.addEventListener("resize", setVars);
    let ro;
    if (bar && typeof ResizeObserver !== "undefined") {
      ro = new ResizeObserver(setVars);
      ro.observe(bar);
    }
    return () => { window.removeEventListener("resize", setVars); if (ro) ro.disconnect(); };
  }, [ready, tab, editFlow, user]);

  // Load this user's readiness profile whenever the signed-in user changes (incl. on the
  // initial restore). The API scopes the read to X-Aruvi-User; we regenerate the active-
  // subject projection the consumers read. Clearing first prevents one user's data flashing
  // for another after a sign-out/sign-in.
  useEffect(() => {
    if (!user) return;
    setReady(false); setReadiness(null); setReadinessLoaded(false);
    getJSON("/readiness").then((d) => {
      if (d && d.ready && d.readiness) {
        setReadiness(projectReadiness(d.readiness));
        setReady(true);
      }
    }).catch(() => {})  // no saved profile / API down → stay in the not-ready setup flow
      .finally(() => setReadinessLoaded(true));
  }, [user]);

  // First-run complete: FirstRun has now walked the FULL sequence (subject → grade → chapter →
  // preview → section fan-out → arrange-week-or-skip) and hands up the canonical readiness
  // payload it built — { subjects: [subjectRecord] }. This is the real activation moment: persist
  // it for real (same POST used by the old upfront wizard, via onReadyComplete's pattern), flip
  // `ready` so the shell opens with her new section card(s) already visible in My Plans, and
  // scope the Generate tab to what she just set up. `ready` is now the ONLY activation signal
  // (see the comment above the component) — no separate local flag to keep in sync.
  // ── READ-AFTER-WRITE for the shell's two readiness writes (founder doctrine, 2026-08-10)
  // X = the profile before setup · A = this save · Y = the subjects[] she just built · Y′ =
  // GET /readiness. Error IFF Y′ ≠ Y. A throw is not a criterion and an unreachable server is
  // not an error — it is a state in which the check cannot run. Same rule, same helper and the
  // same tested fingerprint as TeachingProfile; only the surface differs, because here she is
  // in the shell rather than on the profile screen.
  const [saveFailed, setSaveFailed] = useState(false);
  const verifyReadiness = (subs) => {
    const want = readinessFingerprint(subs);
    verifiedWrite({
      write: () => fetch(`${API}/readiness`, withUser({
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ subjects: subs }),
      })).then((r) => { if (!r.ok) throw new Error(String(r.status)); }),
      read: () => getJSON("/readiness").then((d) => (d && d.readiness) || d || {}),
      expect: (y) => readinessFingerprint(y.subjects) === want,
    }).then(({ status, actual }) => {
      if (status !== "mismatch") return;
      // Y′ is the truth, including whether she is set up at all. Leaving `ready` true over an
      // empty profile would strand her in a shell with no classes and no explanation.
      const real = (actual && actual.subjects) || [];
      setReadiness(projectReadiness({ subjects: real }));
      setReady(real.length > 0);
      setSaveFailed(true);
    });
  };

  const onFirstRunComplete = (payload, preparing) => {
    const subs = (payload && payload.subjects) || [];
    if (subs.length) {
      setReadiness(projectReadiness({ subjects: subs }));
      setReady(true);
      const first = subs[0];
      setSubject(subjectSlugify(first.name));
      if (first.grades && first.grades[0]) setGrade((first.grades[0].grade || "").toLowerCase());
      /* ★ Land on MY LESSONS, not My Classes (founder, 2026-08-21). First run's whole promise is
         a lesson plan, so the first thing she should see when the shell opens is the lesson —
         not a section card that is empty until she attaches something to it. The tour offer
         renders below it there, and the tour itself starts by naming both tabs, so she still
         meets My Classes within seconds — with a reason to care about it.
         `preparing` is the proposed-lesson descriptor: first run fires the serve and hands off
         in the SAME tick, so the plan is still in flight when the shell opens. Setting it here
         puts the ordinary progress card at the head of My Lessons — the identical wait a normal
         run shows — and `onPrepared` replaces it in place when the serve lands. First run has no
         waiting screen of its own any more; there is one wait, in one place. */
      goLessons();
      if (preparing) setPreparingCard(preparing);
      // READ-AFTER-WRITE (lib/verify.js). This is the ACTIVATION write — the one that turns a
      // first-time teacher into a set-up one — and it used to end in an empty catch, so a lost
      // profile looked exactly like a successful setup until her next sign-in.
      verifyReadiness(subs);
    }
  };

  useEffect(() => { if (!user) return;
    getJSON("/subjects").then((d) => { setSubjects(d.subjects); setSubject(d.subjects.includes("science") ? "science" : d.subjects[0]); }).catch(() => {});
  }, [user]);

  useEffect(() => { if (!subject) return;
    getJSON(`/subjects/${subject}/grades`).then((d) => {
      const gs = [...d.grades].sort((a, b) => ROMAN.indexOf(a) - ROMAN.indexOf(b));
      setGrades(gs);
      // Keep the already-selected grade if it's valid for this subject (e.g. a section card
      // scoped us to English·VI just before this fires) — only fall back to a default when the
      // current grade isn't offered for the new subject. Functional update reads the live grade.
      setGrade((prev) => (gs.includes(prev) ? prev : (gs.includes("vii") ? "vii" : gs[0] || "")));
    }).catch(() => setGrades([]));
  }, [subject]);

  // Persist the readiness profile (canonical subjects[] only) when setup completes, then
  // flip ready. Fire-and-forget: the UI advances immediately; the write carries the user
  // header so it lands under the right tenant.
  const onReadyComplete = (payload) => {
    setReadiness(payload);
    setReady(true);
    verifyReadiness((payload && payload.subjects) || []);
  };


  // From My Lesson Plans: "Need a chapter…" pre-scopes Generate to a subject·grade and opens
  // it, so the allocation table lands on that exact combo (slugs match the scope-pill state).
  const onAllocateScoped = (subjectSlug, gradeSlug) => {
    if (subjectSlug) setSubject(subjectSlug);
    if (gradeSlug) setGrade(gradeSlug);
    setEditFlow(null);
    // My Lessons path → deposit only, never auto-attach to a section (no return section).
    setPrepareReturn(null);
    setGenerateEntry({ mode: "scoped", subject: subjectSlug, grade: gradeSlug });
    setTab("generate");
  };

  // THE single route into Generate (the "Ready to plan…" button + My Week empty cards). With one
  // subject AND one grade we skip the picker and scope directly; otherwise the G1.9 picker runs.
  // `opts.subject`/`opts.grade` (slugs) pre-scope and skip the picker (My Week row / My Lesson Plans).
  const subjectSlugify = (n) => (n || "").toLowerCase().replace(/ /g, "_");
  // opts.single === true marks a one-chapter-at-a-time entry (from a My Week card) — Allocate
  // rewords G4 to "this chapter" and shows the budget anchor. Bulk entries (Generate tab, My
  // Lesson Plans "Generate") leave it falsy and keep the multi-chapter framing.
  const onEnterGenerate = (opts = {}) => {
    const subs = (readiness && readiness.subjects) || [];
    const single = !!opts.single;
    if (opts.subject && opts.grade) {
      setSubject(opts.subject); setGrade(opts.grade);
      setGenerateEntry({ mode: "scoped", subject: opts.subject, grade: opts.grade, single });
    } else if (subs.length === 1 && (subs[0].grades || []).length === 1) {
      const sSlug = subjectSlugify(subs[0].name);
      const gSlug = (subs[0].grades[0].grade || "").toLowerCase();
      setSubject(sSlug); setGrade(gSlug);
      setGenerateEntry({ mode: "scoped", subject: sSlug, grade: gSlug, single });
    } else {
      setGenerateEntry({ mode: "pick", single });
    }
    // Launched from a section's attach popup → remember where to return once the chapter is
    // prepared, so onPrepared can reopen that popup instead of opening the lesson plan.
    setPrepareReturn(opts.returnSection && opts.subject && opts.grade
      ? { subject: opts.subject, grade: opts.grade, sectionTag: opts.returnSection } : null);
    setEditFlow(null);
    setTab("generate");
  };

  // A chapter was just prepared in the Generate flow. Don't open the lesson plan.
  //  • Launched FROM a section card → auto-ATTACH the new lesson to that section and land on My
  //    Classes, where the card now shows it (MyPlans consumes pendingAttach and binds it).
  //  • Launched from My Lessons → deposit ONLY: it's already marked prepared, so send her to the
  //    My Lessons repository where it now appears; no section is touched.
  // `filename` is the prepared plan.
  const onPrepared = ({ subject: s, grade: g, filename }) => {
    setGenerateEntry(null);
    setPreparingCard(null);            // the proposed card gives way to the real one
    if (prepareReturn) {
      setPendingAttach({ ...prepareReturn, filename });
      setPrepareReturn(null);
      setEditFlow(null); setTab("myplans");
    } else {
      if (s) setSubject(s); if (g) setGrade(g);
      setEditFlow("lessonplans"); setTab("myplans");
    }
  };

  // ── THE WAIT MOVED TO WHERE THE LESSON LANDS (founder, 2026-08-06) ──────────────
  // Preparing no longer holds her on the Generate screen behind a pale stand-in card.
  // The moment the request goes out, PrepareLesson hands the descriptor up here and we
  // put her in My Lessons, where the proposed lesson is drawn as an ordinary card at the
  // head of the list — real title, real period shape, full strength — with a progress bar
  // where "Ready to teach" will be. When the plan resolves, that card becomes the real one
  // in place; she never changes screens to watch it happen.
  //   `preparingCard` lives HERE, above the tab, because PrepareLesson unmounts the instant
  // we navigate. The request itself keeps running inside that unmounted component's closure
  // and still calls onPrepared / onPrepareError, which is why nothing had to move server-side.
  //   The section-attach path (prepareReturn) is deliberately EXCLUDED: it lands in My
  // Classes, not My Lessons, so there is nowhere to put this card. It keeps the in-place
  // wait, which PrepareLesson still implements as its fallback.
  const [preparingCard, setPreparingCard] = useState(null);
  // Returns TRUE only if the card was actually taken. PrepareLesson falls back to its own
  // in-place wait on false — without that handshake the attach path would show her nothing
  // at all for five seconds, which is worse than either screen.
  const onPreparing = (desc) => {
    if (!desc || prepareReturn) return false;    // attach path keeps the in-place wait
    setGenerateEntry(null);
    setPreparingCard(desc);
    if (desc.subject) setSubject(desc.subject);
    if (desc.grade) setGrade(desc.grade);
    setEditFlow("lessonplans"); setTab("myplans");
    return true;
  };
  // The serve failed. Do NOT simply pull the card: she is watching it, and a card that
  // vanishes silently reads as "I mis-tapped" (ARV-D-087 — the founder met exactly this on the
  // phone: "something seemed to flash for a micro sec but nothing readable"). Keep it, mark it
  // FAILED, and put the message on it — the card is where her attention already is, so it needs
  // no banner and no navigation. A bar that never resolves is still worse than either, which is
  // what the original note was protecting against; `failed` ends the bar.
  const onPrepareError = (desc, message) =>
    setPreparingCard(desc ? { ...desc, failed: true, message } : null);
  const onDismissPrepareError = () => setPreparingCard(null);

  // From My Lesson Plans → Track: deep-link into My Week to open a SECTION's pointer-enabled
  // plan (grade-level reads, section-level acts). Scope the tab, leave the library, and stash
  // a pending-open hint that MyPlans consumes on mount.
  const onOpenSection = (subjectSlug, gradeSlug, sectionTag, plan) => {
    if (subjectSlug) setSubject(subjectSlug);
    if (gradeSlug) setGrade(gradeSlug);
    setPendingOpen({ subject: subjectSlug, grade: gradeSlug, sectionTag, filename: plan && plan.filename });
    setEditFlow(null);
    setTab("myplans");
  };

  const onEnter = (id) => { setUser(id); setUserState(id); };
  const onSignOut = () => {
    clearUser(); setUserState("");
    setReady(false); setReadiness(null); setReadinessLoaded(false);
    setSubjects([]); setSubject(""); setTab("myplans"); setEditFlow(null);
    setTour(null); setTourDismissed(false);
  };

  // The three destinations: the two centre tabs + the settings gear. Each leaves any
  // in-progress Generate flow and clears its pending entry/scope.
  const goClasses = () => { setEditFlow(null); setTab("myplans"); setGenerateEntry(null); };
  const goLessons = () => { setEditFlow("lessonplans"); setTab("myplans"); setGenerateEntry(null); };

  // Tour Next — the guide performs the move each step implies before advancing. The view-level
  // work (report/archive buttons at 4/5 on My Lessons, "open the lesson" card at 6 + preview at 7,
  // popup at 9/14, attach/unbind at the 9↔10 boundary, lesson at 11–12, demo-complete at 13–14, the
  // big "+" grow button surfaced at 15) is orchestrated by MyPlans/MyLessonPlans off the numeric
  // tourStep; here we only handle SHELL navigation: 2→3 open My Lessons · 7→8 back to My Classes ·
  // 14→15 close the popup back to My Classes home (the "+" step) · 15→16 open the profile (step 16
  // rings the settings gear over it) · 16→17 back to My Classes (the Ask Aruvi mark) · 17→18 OPEN
  // Ask Aruvi so step 18 rings the real panel · 18→19 close it again for the centred "Welcome to
  // Aruvi" sign-off · 19 Done → My Classes.
  const tourNext = () => {
    if (tour === 2) goLessons();
    else if (tour === 7) goClasses();
    else if (tour === 14) goClasses();
    else if (tour === 15) goProfile();
    else if (tour === 16) goClasses();          // leave the profile → show the Ask Aruvi mark on My Classes
    else if (tour === 17) setAskOpen(true);     // show her the panel itself, not just its mark
    else if (tour === 18) setAskOpen(false);    // clear the screen for the sign-off
    else if (tour === 19) { setAskOpen(false); finishTour(); goClasses(); return; }
    setTour(tour + 1);
  };
  // Tour Back — mirrors every move so each step reverses cleanly: 3→2 back to My Classes' tab
  // highlight; 8→7 back to My Lessons (the preview re-opens there); 16→15 back to My Classes
  // (the grow "+" step; 15→14 re-opens the popup, handled by MyPlans). Steps 4/5/6/7 stay within My
  // Lessons so need no shell move. Back from step 1 backs out to the nudge.
  const tourBack = () => {
    if (tour === 1) { setTour(null); return; }
    if (tour === 3) goClasses();
    else if (tour === 8) goLessons();
    else if (tour === 16) goClasses();
    else if (tour === 17) goProfile();   // back to the settings-gear step (profile open)
    else if (tour === 18) setAskOpen(false);  // 18→17: the mark on the tab row, panel closed
    else if (tour === 19) setAskOpen(true);   // 19→18: re-open the panel the step rings
    setTour(tour - 1);
  };
  const goProfile = () => { setProfileAutoAdd(null); setProfilePortal(null); setEditFlow("profile"); setTab("myplans"); setGenerateEntry(null); };
  // (The "add more classes in this subject" prompt that used to call in here was removed on
  // 2026-08-21 along with its one-time window — see the plusShow note in MyPlans.jsx. Nothing
  // sets `profileAutoAdd` to a subject any more, so TeachingProfile's `autoAddClassSubject`
  // is permanently null: its idle state, and the same value goProfile/onProfilePortal pass.
  // The state is kept because the auto-add flow it drives is still wired and may be re-used.)
  // From My Classes' standing "+" portal (founder, 2026-07-06): open the teaching profile with a
  // one-shot intent — "subject" | "class" | "section" — and TeachingProfile launches the matching
  // manage screen (add AND remove, same flows the gear uses). Consumed once, like profileAutoAdd.
  const onProfilePortal = (kind) => {
    setProfileAutoAdd(null); setProfilePortal(kind); setEditFlow("profile"); setTab("myplans"); setGenerateEntry(null);
  };
  // Which centre tab lights up: My Lessons only when the repository is open; the profile
  // (settings) view lights neither; everything else — home cards, Generate — reads as My Classes.
  const activeNav = editFlow === "lessonplans" ? "lessons" : editFlow === "profile" ? "none" : "classes";

  // Still restoring from localStorage — render nothing for a beat (no login flash).
  if (user === null) return null;
  // Not signed in → the portal.
  if (!user) return <Login onEnter={onEnter} />;
  // Signed in, but wait for GET /readiness to resolve before deciding first-run vs shell
  // (prevents an already-set-up teacher from flashing the guided first run).
  if (!readinessLoaded) return null;
  // Phase 1 gate (§0): no app shell until `ready` — a teacher with an existing (real,
  // server-persisted) readiness profile skips first-run; a brand-new teacher, OR one whose
  // profile was reset, gets the shell-less Guided First Experience until she completes it.
  // onPrepared / onPrepareError are page.jsx's OWN handlers, the same ones PrepareLesson uses:
  // first run fires the serve and hands off in the same tick, so the request resolves after
  // FirstRun has unmounted and must land on the shell's preparing card, not on a dead screen.
  if (!ready) return <FirstRun user={user} onComplete={onFirstRunComplete}
                       onPrepared={onPrepared} onPrepareError={onPrepareError} onSignOut={onSignOut} />;

  return (
    <>
      {/* ONE FIXED top bar (2026-08-08). Two histories are baked into this element:
          (a) the brand row and the tab row used to be two INDEPENDENT sticky siblings — .hdr at
              top:0 and .main-tabs at top:var(--hdr-h) — so nothing tied them together and the
              tab row could stay frozen while the Aruvi row scrolled away behind it. Both rows
              are now STATIC inside this one wrapper; they can only move as a unit.
          (b) the wrapper was then `position: sticky`, and on an iPhone home-screen (standalone)
              web app it still scrolled away — the brand row simply left with the content and
              came back on returning to the top, i.e. sticky was not taking effect at all for a
              direct child of <body> in that webview. It was made `position: fixed` + spacer —
              and the webview scrolled THAT away too.
          (c) so scroll ownership moved off the document entirely (2026-08-09): when the shell
              is up, html.app-shell (globals.css) locks html/body and .bodycontent is the one
              scroll container — this bar is plain static flow and cannot move. The fixed rule
              in .topbar still applies pre-lock and is harmless; the spacer is display:none in
              shell mode. Do not "simplify" any of this back to sticky or fixed-on-document.
          (--hdr-h/--nav-h are still published — inner views use them for their own offsets.) */}
      <div className="topbar">
      {/* Shell header: the brand exactly as the first-run page renders it (Aruvi + red dot,
          LESSON STUDIO tag beneath); settings gear (→ teaching profile) + log out right. No
          hamburger, no drawer — the two tabs below the header are the whole nav. */}
      <header className="hdr">
        <div className="brand">
          <span className="brand-row">Aruvi<em>.</em></span>
          <span className="hdr-brand-tag">lesson studio</span>
        </div>
        <div className="hdr-user">
          <ThemeToggle />
          <button className="hdr-gear" onClick={goProfile} aria-label="Settings" title="Settings"
            data-tour="settings-gear">⚙</button>
          {/* rightmost: profile name stacked over its own log out */}
          <div className="hdr-user-id">
            <span className="hdr-user-name">{user}</span>
            <button className="hdr-user-logout" onClick={onSignOut}>Log out</button>
          </div>
        </div>
      </header>

      {/* The two tabs — the app's entire nav, at the TOP (under the header), active tab
          marked with the same clay-red underline the original My Plans/Generate tabs used.
          Nouns only: My Classes (where did I stop?) and My Lessons (the plan repository).
          "+ Prepare Lesson" is a verb, so it lives as an action inside both views, never here. */}
      <nav className="tabs main-tabs" aria-label="Primary">
        <button className={`tab ${activeNav === "classes" ? "active" : ""}`} onClick={goClasses}
          data-tour="nav-classes">
          My Classes
        </button>
        <button className={`tab ${activeNav === "lessons" ? "active" : ""}`} onClick={goLessons}
          data-tour="nav-lessons">
          My Lessons
        </button>
        {/* Ask Aruvi — permanent "?" at the right of the tab row; opens the deterministic Q&A screen. */}
        <button className="ask-q" onClick={() => setAskOpen(true)} aria-label="Ask Aruvi" title="Ask Aruvi" data-tour="ask-aruvi">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round" aria-hidden="true">
            <path d="M7 6.5c6 1 6 5 3.5 7.5S6 18 6 18" />
            <path d="M10.5 14c3.5 0 5.5-1.8 6.5-4" />
            <circle cx="17.3" cy="8.6" r="1.6" fill="#c0392b" stroke="none" />
          </svg>
        </button>
      </nav>
      </div>
      {/* reserves the fixed bar's height in the flow — see the .topbar comment above */}
      <div className="topbar-spacer" aria-hidden="true" />

      <div className="bodycontent">

        <main>
          {/* Shown only on a VERIFIED mismatch — the server was read back and disagrees with
              what she just set up. Never on a throw, never when the server could not be
              reached. `ready` and the profile above have already been re-synced to what is
              actually stored, so this is a caption for the screen she is now looking at. */}
          {saveFailed && (
            <div className="tp-savefail" role="alert">
              <span>Your teaching set-up didn’t save — this is what Aruvi has for you.</span>
              <button type="button" onClick={() => setSaveFailed(false)}>Dismiss</button>
            </div>
          )}
          {sectionFailed && (
            <div className="tp-savefail" role="alert">
              <span>{sectionFailed}</span>
              <button type="button" onClick={() => setSectionFailed("")}>Dismiss</button>
            </div>
          )}
          {/* Edit-flow views (My Lessons / teaching profile) require a set-up profile. A
           * not-ready user is always routed to the setup flow instead of a dead-end empty
           * view — readiness gates these the same way it gates Generate. */}
          {(editFlow === "lessonplans" && ready) ? (
            /* My Lessons — the plan repository (subject → grade → chapter). */
            <div className="editflow">
              <MyLessonPlans readiness={readiness} onAllocate={onAllocateScoped} onOpenSection={onOpenSection}
                tourStep={tour} preparing={preparingCard}
                onStartTour={tourDismissed ? undefined : startTour} tourActive={!!tour}
                onDismissPrepareError={onDismissPrepareError} />
            </div>
          ) : (editFlow === "profile" && ready) ? (
            /* Teaching profile (via the settings gear) — view + conversational redo (the SAME
             * first-run UI, answers pre-filled) + delete. The MyClasses drill-down is retired.
             * Deleting clears pointers (lessons stay) and drops her STRAIGHT into the redo
             * flow inside this same view — the shell stays open; `ready` is untouched. A
             * signed-out return without rebuilding hits first run naturally (server profile
             * is gone, so GET /readiness comes back empty). */
            <div className="editflow" data-tour="profile-root">
              <TeachingProfile readiness={readiness} onChange={setReadiness} onBack={goClasses}
                autoAddClassSubject={profileAutoAdd} onConsumeAutoAdd={() => setProfileAutoAdd(null)}
                portalIntent={profilePortal} onConsumePortal={() => setProfilePortal(null)} />
            </div>
          ) :
            !subject ? <div className="empty">Connecting to the Aruvi engine…</div> :
            tab === "generate" ? <GenerateTab subject={subject} grade={grade} ready={ready} readiness={readiness}
              onNavigate={setTab} entry={generateEntry} onScope={(s, g) => { setSubject(s); setGrade(g); }}
              onConsumeEntry={() => setGenerateEntry(null)} onPrepared={onPrepared}
              onPreparing={onPreparing} onPrepareError={onPrepareError} /> :
            <MyPlans subject={subject} grade={grade} ready={ready} readiness={readiness}
              onReady={onReadyComplete} onNavigate={setTab} onEnterGenerate={onEnterGenerate}
              user={user} onSignOut={onSignOut}
              pendingOpen={pendingOpen} onConsumePending={() => setPendingOpen(null)}
              pendingAttach={pendingAttach} onConsumeAttach={() => setPendingAttach(null)}
              onStartTour={tourDismissed ? undefined : startTour}
              tourActive={!!tour} tourStep={tour}
              onTourInfo={setTourInfo} onProfilePortal={onProfilePortal} onOpenProfile={goProfile}
              sectionCheck={sectionCheck} onSectionCheckDone={() => setSectionCheck(false)} />}
        </main>
      </div>

      {/* First-run guided tour overlay — 17 guide-driven steps ("N of 17", Back on every one).
          Skip closes it for this session. */}
      {tour && (
        <GuidedTour step={tour} info={tourInfo} onNext={tourNext} onBack={tourBack} onSkip={finishTour} />
      )}

      {/* Ask Aruvi Q&A — full-screen deterministic helpline (browse + keyword search). */}
      {askOpen && <AskAruvi onClose={() => setAskOpen(false)} />}

    </>
  );
}
