"use client";

/* ───────── Ask Aruvi — deterministic Q&A screen ─────────
 * Opened from the "?" on the right of the My Classes / My Lessons row. A full-screen,
 * Settings-style panel over the app. Two modes, one dataset (qa_knowledge_base.json):
 *
 *   • BROWSE (search empty): five collapsible categories. Opening one FREEZES its header
 *     (sticky) so it can be collapsed again from anywhere while its questions scroll.
 *     Tapping a question opens its answer inline.
 *
 *   • SEARCH (search has text): categories disappear entirely — only a ranked, de-duplicated
 *     list of matching Q&A, best match first, with a live result count. No LLM: matching is
 *     keyword + normalised token ranking (see lib/askAruviSearch.js).
 *
 * Same experience on every screen — no context, no pre-expansion. Warm-paper tokens from
 * globals.css, so light/dark follow the app automatically.
 */

import { useState, useMemo, useEffect } from "react";
import kb from "./qa_knowledge_base.json";
import { search } from "./askAruviSearch";

export default function AskAruvi({ onClose }) {
  const [query, setQuery] = useState("");
  const [openCat, setOpenCat] = useState(null);   // the frozen (expanded) category id
  const [openPair, setOpenPair] = useState(null); // the expanded answer id

  const result = useMemo(() => search(kb.pairs, query), [query]);
  const searching = result !== null;

  // category id → {title, description, tag, accent} (all driven by the JSON, no hardcoding)
  const catMap = useMemo(() => Object.fromEntries(kb.categories.map((c) => [c.id, c])), []);

  const byCat = useMemo(() => {
    const m = {};
    kb.pairs.forEach((p) => (m[p.category] = m[p.category] || []).push(p));
    return m;
  }, []);

  // Esc closes; lock body scroll while open.
  useEffect(() => {
    const h = (e) => e.key === "Escape" && onClose();
    window.addEventListener("keydown", h);
    const prev = document.body.style.overflow;
    document.body.style.overflow = "hidden";
    return () => { window.removeEventListener("keydown", h); document.body.style.overflow = prev; };
  }, [onClose]);

  const togglePair = (id) => setOpenPair((cur) => (cur === id ? null : id));

  return (
    <div className="aa-scrim" role="dialog" aria-modal="true" aria-label="Ask Aruvi">
      <div className="aa-panel">

        {/* fixed title bar */}
        <div className="aa-top">
          <div className="aa-title">
            <span className="aa-q" aria-hidden="true">
              <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.9" strokeLinecap="round" strokeLinejoin="round">
                <path d="M7 6.5c6 1 6 5 3.5 7.5S6 18 6 18" />
                <path d="M10.5 14c3.5 0 5.5-1.8 6.5-4" />
                <circle cx="17.3" cy="8.6" r="1.6" fill="#e8b4a0" stroke="none" />
              </svg>
            </span>
            <span>Ask Aruvi</span>
          </div>
          <button className="aa-close" onClick={onClose} aria-label="Close Ask Aruvi">✕</button>
        </div>

        {/* sticky search bar */}
        <div className="aa-search">
          <input
            type="search" value={query} autoFocus
            onChange={(e) => { setQuery(e.target.value); setOpenPair(null); }}
            placeholder="Search Ask Aruvi…"
            aria-label="Search questions"
          />
          {searching && (
            <div className="aa-count">
              {result.count === 0
                ? "No matches — try fewer or different words"
                : `${result.count} ${result.count === 1 ? "result" : "results"}`}
            </div>
          )}
        </div>

        {/* scroll region */}
        <div className="aa-body">
          {searching ? (
            /* ── SEARCH MODE — ranked list only, no categories ── */
            <div className="aa-results">
              {result.results.map((p) => (
                <Answer key={p.id} p={p} open={openPair === p.id} onToggle={() => togglePair(p.id)} tag={catMap[p.category]?.tag} />
              ))}
            </div>
          ) : (
            /* ── BROWSE MODE — five collapsible, freezable categories ── */
            kb.categories.map((c) => {
              const pairs = byCat[c.id] || [];
              const isOpen = openCat === c.id;
              return (
                <section key={c.id} className={`aa-cat ${isOpen ? "open" : ""}`} style={{ "--accent": c.accent }}>
                  <button
                    className="aa-cat-head"
                    aria-expanded={isOpen}
                    onClick={() => { setOpenCat(isOpen ? null : c.id); setOpenPair(null); }}
                  >
                    <span className="aa-cat-bar" aria-hidden="true" />
                    <span className="aa-cat-text">
                      <span className="aa-cat-title">{c.title}</span>
                      <span className="aa-cat-desc">{c.description}</span>
                    </span>
                    <span className="aa-cat-meta">
                      <span className="aa-cat-n">{pairs.length}</span>
                      <span className={`aa-chev ${isOpen ? "up" : ""}`} aria-hidden="true">⌄</span>
                    </span>
                  </button>

                  {isOpen && (
                    <div className="aa-cat-list">
                      {pairs.map((p) => (
                        <Answer key={p.id} p={p} open={openPair === p.id} onToggle={() => togglePair(p.id)} />
                      ))}
                    </div>
                  )}
                </section>
              );
            })
          )}
        </div>
      </div>

      <style jsx>{`
        /* Opens BELOW the frozen header — its grey bottom border (the line under the
           "Aruvi · lesson studio" logo) stays visible and frozen. --hdr-h is the header
           height page.jsx measures live; 72px is the pre-measure fallback. */
        .aa-scrim { position: fixed; top: var(--hdr-h, 72px); left: 0; right: 0; bottom: 0;
          z-index: 40; background: rgba(20,16,10,.34);
          display: flex; justify-content: center; align-items: stretch; }
        .aa-panel { width: 100%; max-width: 720px; height: 100%; background: var(--paper);
          display: flex; flex-direction: column; box-shadow: 0 0 60px rgba(0,0,0,.28); }
        @media (min-width: 721px) { .aa-panel { border-radius: 0 0 16px 16px; overflow: hidden; } }

        .aa-top { display: flex; align-items: center; justify-content: space-between;
          padding: 16px 20px 12px; border-bottom: 1px solid var(--line); background: var(--paper); }
        .aa-title { display: flex; align-items: center; gap: 10px; font-family: var(--f-display);
          font-size: 20px; font-weight: 600; color: var(--ink); }
        .aa-q { display: inline-flex; align-items: center; justify-content: center; width: 26px; height: 26px;
          border-radius: 50%; background: var(--pine); color: #fff; font-family: var(--f-mono); font-size: 15px; }
        .aa-close { background: none; border: none; font-size: 17px; color: var(--ink-soft); cursor: pointer; padding: 6px; }
        .aa-close:hover { color: var(--clay); }

        .aa-search { padding: 12px 20px 10px; border-bottom: 1px solid var(--line-soft);
          background: var(--paper); position: sticky; top: 0; z-index: 3; }
        .aa-search input { width: 100%; font-family: var(--f-body); font-size: 16px; color: var(--ink);
          background: var(--paper-2); border: 1px solid var(--line); border-radius: 10px;
          padding: 11px 14px; outline: none; }
        .aa-search input:focus { border-color: var(--pine); }
        .aa-count { font-family: var(--f-mono); font-size: 11px; letter-spacing: .04em; text-transform: uppercase;
          color: var(--ink-soft); margin: 9px 2px 1px; }

        /* No top padding on the scroll area: it would leave a band above the stuck category
           header where a scrolling question flashes into view before sliding under it. */
        .aa-body { flex: 1; overflow-y: auto; -webkit-overflow-scrolling: touch;
          padding: 0 20px 40px; }
        .aa-results { padding-top: 6px; }

        /* categories */
        .aa-cat { border-bottom: 1px solid var(--line-soft); }
        /* Sticky header sits ABOVE the scrolling rows (raised z-index) on its own paint layer
           (translateZ) with an opaque paper fill, so questions pass cleanly underneath it. */
        .aa-cat-head { position: sticky; top: 0; z-index: 5; width: 100%; display: flex; align-items: center; gap: 12px;
          background: var(--paper); border: none; cursor: pointer; text-align: left; padding: 15px 2px;
          transform: translateZ(0); }
        .aa-cat.open .aa-cat-head { border-bottom: 1px solid var(--line-soft); }
        .aa-cat-bar { flex: none; width: 4px; align-self: stretch; min-height: 30px; border-radius: 3px; background: var(--accent); }
        .aa-cat-text { flex: 1; min-width: 0; }
        .aa-cat-title { display: block; font-family: var(--f-display); font-size: 16.5px; font-weight: 600; color: var(--ink); }
        .aa-cat-desc { display: block; font-family: var(--f-body); font-size: 13px; color: var(--ink-soft); margin-top: 2px; line-height: 1.35; }
        .aa-cat-meta { flex: none; display: flex; align-items: center; gap: 10px; }
        .aa-cat-n { font-family: var(--f-mono); font-size: 12px; color: var(--accent); min-width: 20px; text-align: right; }
        .aa-chev { font-size: 18px; color: var(--ink-soft); transition: transform .18s ease; }
        .aa-chev.up { transform: rotate(180deg); }
        .aa-cat-list { padding: 2px 0 10px; }
      `}</style>

      {/* Answer rows carry their own styles (shared by both modes) */}
      <style jsx global>{`
        .aa-item { border-top: 1px solid var(--line-soft); }
        .aa-results > .aa-item:first-child { border-top: none; }
        .aa-item-q { width: 100%; display: flex; align-items: flex-start; gap: 10px; background: none; border: none;
          cursor: pointer; text-align: left; padding: 13px 2px; font-family: var(--f-body); font-size: 15.5px;
          color: var(--ink); line-height: 1.4; }
        .aa-item-q:hover { color: var(--pine-d); }
        .aa-item-plus { flex: none; font-family: var(--f-mono); font-size: 14px; color: var(--ink-soft); margin-top: 1px; width: 14px; }
        .aa-item.open .aa-item-plus { color: var(--clay); }
        .aa-item-tag { flex: none; font-family: var(--f-mono); font-size: 9px; letter-spacing: .08em; text-transform: uppercase;
          color: var(--ink-soft); border: 1px solid var(--line); border-radius: 20px; padding: 2px 7px; margin-top: 1px; }
        .aa-item-a { font-family: var(--f-body); font-size: 15px; color: var(--ink-soft); line-height: 1.6;
          padding: 0 2px 15px 24px; white-space: pre-wrap; }
      `}</style>
    </div>
  );
}

function Answer({ p, open, onToggle, tag }) {
  return (
    <div className={`aa-item ${open ? "open" : ""}`}>
      <button className="aa-item-q" aria-expanded={open} onClick={onToggle}>
        <span className="aa-item-plus" aria-hidden="true">{open ? "–" : "+"}</span>
        <span className="aa-item-qtext">{p.question}</span>
        {tag && <span className="aa-item-tag">{tag}</span>}
      </button>
      {open && <div className="aa-item-a">{p.answer}</div>}
    </div>
  );
}
