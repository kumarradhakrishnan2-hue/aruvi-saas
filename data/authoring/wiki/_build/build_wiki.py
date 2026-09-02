#!/usr/bin/env python3
"""Build the pilot curriculum wiki (theme: WATER) from the concept extraction.

Input : extract/{subject}.json  (one per subject; see INSTRUCTIONS.md)
Output: an Obsidian-compatible markdown vault + a single-file HTML reader.

    python3 build_wiki.py --extract /tmp/aruvi/extract --summaries /tmp/aruvi/authoring/chapters --out /tmp/aruvi/wiki
"""
import argparse, glob, html, json, os, re, shutil
from collections import defaultdict

VOCAB = [
    ("states-of-water",         "States of water",          "Solid, liquid and gas; melting, freezing, evaporation, condensation, boiling."),
    ("water-cycle",             "The water cycle",          "Evaporation → clouds → precipitation → collection; the Sun as the driver; the cycle as a system."),
    ("rain-and-monsoon",        "Rain and the monsoon",     "Rainfall, monsoon winds, seasons and climate patterns, humidity, weather measurement."),
    ("rivers-and-landforms",    "Rivers and landforms",     "Rivers from source to sea, erosion and deposition, valleys, deltas, floods, glaciers."),
    ("oceans-and-water-bodies", "Oceans and water bodies",  "Oceans, seas, lakes, ponds; how water is distributed on Earth; tides and currents."),
    ("water-as-resource",       "Water as a resource",      "Sources, scarcity, conservation, rainwater harvesting, wells, tanks, dams, irrigation, supply."),
    ("water-and-life",          "Water and life",           "Water in the body, in plants, aquatic habitats, drinking water, health and sanitation."),
    ("water-as-solvent",        "Water as a solvent",       "Dissolving, solutions, mixtures, purification and separation."),
    ("measuring-water",         "Measuring water",          "Capacity and volume in litres, weighing liquids, measuring water temperature."),
    ("water-and-heat",          "Water and heat",           "Heating and cooling water, convection, sea and land breezes, water in heat transfer."),
    ("water-in-society",        "Water in society",         "Civilisations by rivers, water in architecture, urban supply, community disputes, water in stories."),
]
VID = {v[0]: v for v in VOCAB}
SUBJ = {
    "science": "Science", "social_sciences": "Social Sciences", "mathematics": "Mathematics",
    "english": "English", "the_world_around_us": "The World Around Us",
}
SUBJ_SHORT = {"science": "Sci", "social_sciences": "SS", "mathematics": "Maths", "english": "Eng", "the_world_around_us": "TWAU"}
GRADE = {"iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8, "ix": 9}
ROLE_GLYPH = {"introduces": "●", "extends": "◐", "uses": "○"}
ROLE_ORDER = {"introduces": 0, "extends": 1, "uses": 2}

# ----------------------------------------------------------------------------- load

def load_extract(extract_dir):
    chapters = []
    for f in sorted(glob.glob(os.path.join(extract_dir, "*.json"))):
        d = json.load(open(f))
        for c in d["chapters"]:
            c = dict(c)
            c["subject"] = d["subject"]
            c["g"] = GRADE[c["grade"]]
            c["key"] = f"{c['subject']}-{c['grade']}-ch{c['chapter']:02d}"
            c["title"] = re.sub(r"^Chapter\s+0*\d+\s*[:—-]\s*", "", c["title"]).strip()
            chapters.append(c)
    chapters.sort(key=lambda c: (c["g"], c["subject"], c["chapter"]))
    return chapters


def excerpt(summaries_dir, c, n=520):
    """First real paragraph of the source summary, as a taste of the chapter page."""
    rel = c["source"].split("chapters/", 1)[1]
    p = os.path.join(summaries_dir, rel)
    if not os.path.exists(p):
        return ""
    if p.endswith(".txt"):
        paras = [x.strip() for x in open(p, encoding="utf-8", errors="replace").read().split("\n\n") if x.strip()]
        body = next((x for x in paras[1:] if len(x) > 80), paras[0] if paras else "")
    else:
        d = json.load(open(p))
        body = ""
        for sec_key in ("sections", "main_sections"):
            secs = d.get(sec_key) or []
            if secs:
                body = secs[0].get("prose_summary", "") or ""
                break
    body = re.sub(r"\s+", " ", body).strip()
    if len(body) > n:
        body = body[:n].rsplit(" ", 1)[0] + " …"
    return body

# ----------------------------------------------------------------------------- helpers

def cls(g):
    return f"Class {g}"


def chap_link(c, with_subject=True):
    label = f"{SUBJ[c['subject']]} · " if with_subject else ""
    return f"[[{c['key']}|{label}Ch {c['chapter']} {c['title']}]]"


def concept_link(cid):
    return f"[[{cid}|{VID[cid][1]}]]"


def index_nodes(chapters):
    """concept id -> list of (chapter, node) sorted by grade, role, subject."""
    by = defaultdict(list)
    for c in chapters:
        for k in c["concepts"]:
            by[k["id"]].append((c, k))
    for cid in by:
        by[cid].sort(key=lambda t: (t[0]["g"], ROLE_ORDER[t[1]["role"]], t[0]["subject"], t[0]["chapter"]))
    return by


def joint_candidates(by):
    """(grade, concept) cells taught by >=2 subjects."""
    out = []
    for cid, rows in by.items():
        per_grade = defaultdict(list)
        for c, k in rows:
            per_grade[c["g"]].append((c, k))
        for g, lst in per_grade.items():
            subs = {c["subject"] for c, _ in lst}
            if len(subs) >= 2:
                out.append((g, cid, lst))
    out.sort(key=lambda t: (t[0], VOCAB.index(VID[t[1]])))
    return out

# ----------------------------------------------------------------------------- pages (markdown)

def page_hub(chapters, by):
    L = ["# Water — a concept thread through the curriculum", ""]
    L.append("*Pilot wiki built from Aruvi's chapter summaries. One theme, eleven ideas, "
             f"{len([c for c in chapters if c['concepts']])} chapters across five subjects and Classes 3–9.*")
    L.append("")
    L.append("## How to read this")
    L.append("")
    L.append("Every **idea** has a page listing each chapter that touches it, in class order, with one sentence "
             "saying what that chapter adds. Every **chapter** has a page listing the ideas it touches. "
             "Three views read the same links three ways: [[spiral-water|the spiral]] (one idea, class by class), "
             "[[joint-classes|joint classes]] (same class, two subjects, one idea) and "
             "[[cross-subject|cross-subject connections]] (which subjects lean on which).")
    L.append("")
    L.append("Role marks: ● introduces · ◐ extends · ○ uses.")
    L.append("")
    L.append("## The eleven ideas")
    L.append("")
    L.append("| Idea | Classes | Subjects | Chapters |")
    L.append("|---|---|---|---|")
    for cid, name, desc in VOCAB:
        rows = by.get(cid, [])
        grades = sorted({c["g"] for c, _ in rows})
        subs = sorted({SUBJ_SHORT[c["subject"]] for c, _ in rows})
        L.append(f"| {concept_link(cid)} — {desc} | {', '.join(str(g) for g in grades)} | {', '.join(subs)} | {len(rows)} |")
    L.append("")
    L.append("## Coverage at a glance")
    L.append("")
    L.append("Rows are ideas, columns are classes. Each cell names the subject(s) and the role.")
    L.append("")
    L.append("| Idea | " + " | ".join(cls(g) for g in range(3, 10)) + " |")
    L.append("|---|" + "---|" * 7)
    for cid, name, _ in VOCAB:
        cells = []
        for g in range(3, 10):
            items = [(c, k) for c, k in by.get(cid, []) if c["g"] == g]
            cells.append("<br>".join(f"{ROLE_GLYPH[k['role']]} {SUBJ_SHORT[c['subject']]} ch{c['chapter']}" for c, k in items) or " ")
        L.append(f"| {concept_link(cid)} | " + " | ".join(cells) + " |")
    L.append("")
    L.append("## All chapters in this thread")
    L.append("")
    cur = None
    for c in chapters:
        if not c["concepts"]:
            continue
        if c["g"] != cur:
            cur = c["g"]
            L.append(f"**{cls(cur)}**")
            L.append("")
        L.append(f"- {chap_link(c)} — {', '.join(ROLE_GLYPH[k['role']] + ' ' + VID[k['id']][1] for k in c['concepts'])}")
        if c["g"] != (chapters[chapters.index(c) + 1]["g"] if chapters.index(c) + 1 < len(chapters) else None):
            L.append("")
    skipped = [c for c in chapters if not c["concepts"]]
    if skipped:
        L.append("")
        L.append("## Looked at, left out")
        L.append("")
        L.append("The keyword scan flagged these, the reader found only incidental water content:")
        L.append("")
        for c in skipped:
            L.append(f"- {SUBJ[c['subject']]} {cls(c['g'])} ch {c['chapter']} *{c['title']}* — {c.get('skip_reason') or ''}")
    return "\n".join(L) + "\n"


def page_concept(cid, by, chapters, jc):
    _, name, desc = VID[cid]
    rows = by.get(cid, [])
    L = [f"# {name}", "", f"*{desc}*", "", "Part of the [[Water]] thread.", ""]
    intro = [c for c, k in rows if k["role"] == "introduces"]
    if intro:
        first = min(intro, key=lambda c: c["g"])
        L.append(f"**First taught:** {cls(first['g'])}, {chap_link(first)}.")
        L.append("")
    L.append("## The idea, class by class")
    L.append("")
    L.append("| Class | Subject · chapter | Role | What this chapter says |")
    L.append("|---|---|---|---|")
    for c, k in rows:
        L.append(f"| {c['g']} | {chap_link(c)} | {ROLE_GLYPH[k['role']]} {k['role']} | {k['statement']} |")
    L.append("")
    # roles summary
    for role in ("introduces", "extends", "uses"):
        lst = [c for c, k in rows if k["role"] == role]
        if lst:
            L.append(f"**{role.capitalize()}** ({len(lst)}): " + "; ".join(f"{cls(c['g'])} {SUBJ_SHORT[c['subject']]} ch {c['chapter']}" for c in lst))
            L.append("")
    # joint-class candidates for this concept
    mine = [(g, lst) for g, cc, lst in jc if cc == cid]
    if mine:
        L.append("## Joint-class candidates")
        L.append("")
        L.append("Same class, different subjects, this one idea:")
        L.append("")
        for g, lst in mine:
            L.append(f"- **{cls(g)}** — " + " + ".join(chap_link(c) for c, _ in lst))
        L.append("")
    # related concepts (co-occurrence)
    co = defaultdict(int)
    for c, _ in rows:
        for k in c["concepts"]:
            if k["id"] != cid:
                co[k["id"]] += 1
    if co:
        top = sorted(co.items(), key=lambda t: -t[1])[:4]
        L.append("## Related ideas")
        L.append("")
        L.append("Ideas that most often appear in the same chapters: " + ", ".join(f"{concept_link(k)} ({n})" for k, n in top) + ".")
        L.append("")
    return "\n".join(L) + "\n"


def page_chapter(c, ex):
    L = [f"# {c['title']}", ""]
    L.append(f"**{SUBJ[c['subject']]} · {cls(c['g'])} · Chapter {c['chapter']}**")
    L.append("")
    if c.get("one_line"):
        L.append(f"*{c['one_line']}*")
        L.append("")
    if ex:
        L.append("> " + ex)
        L.append("")
    L.append("## Water ideas in this chapter")
    L.append("")
    if c["concepts"]:
        L.append("| Idea | Role | What this chapter says | Where |")
        L.append("|---|---|---|---|")
        for k in sorted(c["concepts"], key=lambda k: ROLE_ORDER[k["role"]]):
            L.append(f"| {concept_link(k['id'])} | {ROLE_GLYPH[k['role']]} {k['role']} | {k['statement']} | {k.get('section_ref','')} |")
    else:
        L.append(f"*None recorded.* {c.get('skip_reason','')}")
    L.append("")
    if c.get("explicit_links"):
        L.append("## The chapter's own pointers")
        L.append("")
        L.append("Phrases in the summary that point at another class or subject, verbatim:")
        L.append("")
        for x in c["explicit_links"]:
            L.append(f"- “{x}”")
        L.append("")
    L.append("---")
    L.append(f"Source summary: `{c['source']}` · Thread: [[Water]]")
    return "\n".join(L) + "\n"


def page_spiral(by):
    L = ["# The spiral — each idea, class by class", "",
         "*Read down any block: that is the idea growing from Class 3 to Class 9. The role mark says whether the class "
         "meets the idea for the first time (●), takes it further (◐), or leans on it (○).*", "", "Part of the [[Water]] thread.", ""]
    for cid, name, _ in VOCAB:
        rows = by.get(cid, [])
        L.append(f"## {concept_link(cid)}")
        L.append("")
        cur = None
        for c, k in rows:
            if c["g"] != cur:
                cur = c["g"]
                L.append(f"**{cls(cur)}**")
                L.append("")
            L.append(f"- {ROLE_GLYPH[k['role']]} {chap_link(c)} — {k['statement']}")
            nxt = rows[rows.index((c, k)) + 1][0]["g"] if rows.index((c, k)) + 1 < len(rows) else None
            if nxt != cur:
                L.append("")
        gaps = [g for g in range(3, 10) if g not in {c["g"] for c, _ in rows}]
        if gaps:
            L.append(f"*Not touched in: {', '.join(cls(g) for g in gaps)}.*")
            L.append("")
    return "\n".join(L) + "\n"


def page_joint(jc):
    L = ["# Joint-class candidates", "",
         "*A cell where the same idea is taught in the same class by two or more subjects. Each is a candidate for a "
         "combined lesson, or at least for the two teachers to know what the other is doing that term.*", "",
         "Part of the [[Water]] thread.", ""]
    cur = None
    for g, cid, lst in jc:
        if g != cur:
            cur = g
            L.append(f"## {cls(g)}")
            L.append("")
        L.append(f"### {concept_link(cid)}")
        L.append("")
        for c, k in lst:
            L.append(f"- {ROLE_GLYPH[k['role']]} {chap_link(c)} — {k['statement']}")
        L.append("")
    return "\n".join(L) + "\n"


def page_cross(chapters, by):
    subs = [s for s in SUBJ if any(c["subject"] == s and c["concepts"] for c in chapters)]
    L = ["# Cross-subject connections", "",
         "*Which subjects share which ideas. The first table counts, for each pair of subjects, the number of ideas "
         "both touch; the second lists them.*", "", "Part of the [[Water]] thread.", ""]
    touched = {s: {k["id"] for c in chapters if c["subject"] == s for k in c["concepts"]} for s in subs}
    L.append("| | " + " | ".join(SUBJ_SHORT[s] for s in subs) + " |")
    L.append("|---|" + "---|" * len(subs))
    for a in subs:
        cells = []
        for b in subs:
            cells.append("–" if a == b else str(len(touched[a] & touched[b])))
        L.append(f"| **{SUBJ_SHORT[a]}** | " + " | ".join(cells) + " |")
    L.append("")
    L.append("## Who teaches, who leans")
    L.append("")
    L.append("For each idea: the subject that first *introduces* it, and the subjects that only *use* it. "
             "A subject that only uses an idea is depending on another subject having taught it.")
    L.append("")
    L.append("| Idea | Introduced by | Extended by | Only used by |")
    L.append("|---|---|---|---|")
    for cid, name, _ in VOCAB:
        rows = by.get(cid, [])
        def fmt(role):
            seen = []
            for c, k in rows:
                if k["role"] == role:
                    t = f"{SUBJ_SHORT[c['subject']]} {c['g']}"
                    if t not in seen:
                        seen.append(t)
            return ", ".join(seen) or " "
        intro_subs = {c["subject"] for c, k in rows if k["role"] in ("introduces", "extends")}
        only_use = []
        for c, k in rows:
            if k["role"] == "uses" and c["subject"] not in intro_subs:
                t = f"{SUBJ_SHORT[c['subject']]} {c['g']}"
                if t not in only_use:
                    only_use.append(t)
        L.append(f"| {concept_link(cid)} | {fmt('introduces')} | {fmt('extends')} | {', '.join(only_use) or ' '} |")
    L.append("")
    L.append("## Subject pairs, idea by idea")
    L.append("")
    for i, a in enumerate(subs):
        for b in subs[i + 1:]:
            shared = [cid for cid, _, _ in VOCAB if cid in touched[a] & touched[b]]
            if not shared:
                continue
            L.append(f"### {SUBJ[a]} ↔ {SUBJ[b]}")
            L.append("")
            for cid in shared:
                ca = [c for c, _ in by[cid] if c["subject"] == a]
                cb = [c for c, _ in by[cid] if c["subject"] == b]
                L.append(f"- {concept_link(cid)}: {SUBJ_SHORT[a]} " + ", ".join(f"{c['g']}·ch{c['chapter']}" for c in ca)
                         + f" — {SUBJ_SHORT[b]} " + ", ".join(f"{c['g']}·ch{c['chapter']}" for c in cb))
            L.append("")
    return "\n".join(L) + "\n"

# ----------------------------------------------------------------------------- markdown -> html (tiny, for the reader)

def md_inline(s, resolve):
    s = html.escape(s, quote=False)
    s = re.sub(r"`([^`]+)`", r"<code>\1</code>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", s)
    def wl(m):
        target, alias = m.group(1), m.group(2) or m.group(1)
        href = resolve(target)
        return f'<a href="#{href}" class="wl">{alias}</a>' if href else f'<span class="wl-dead">{alias}</span>'
    s = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", wl, s)
    s = s.replace("&lt;br&gt;", "<br>")
    return s


def md_to_html(md, resolve):
    out, i, lines = [], 0, md.split("\n")
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*-", lines[i + 1]):
            hdr = [x.strip() for x in ln.strip("|").split("|")]
            i += 2
            body = []
            while i < len(lines) and lines[i].startswith("|"):
                body.append([x.strip() for x in lines[i].strip("|").split("|")])
                i += 1
            out.append("<table><thead><tr>" + "".join(f"<th>{md_inline(h, resolve)}</th>" for h in hdr) + "</tr></thead><tbody>")
            for r in body:
                out.append("<tr>" + "".join(f"<td>{md_inline(x, resolve)}</td>" for x in r) + "</tr>")
            out.append("</tbody></table>")
            continue
        m = re.match(r"^(#{1,3})\s+(.*)", ln)
        if m:
            out.append(f"<h{len(m.group(1))}>{md_inline(m.group(2), resolve)}</h{len(m.group(1))}>")
            i += 1; continue
        if ln.startswith("- "):
            out.append("<ul>")
            while i < len(lines) and lines[i].startswith("- "):
                out.append(f"<li>{md_inline(lines[i][2:], resolve)}</li>")
                i += 1
            out.append("</ul>"); continue
        if ln.startswith("> "):
            out.append(f"<blockquote>{md_inline(ln[2:], resolve)}</blockquote>")
            i += 1; continue
        if ln.strip() == "---":
            out.append("<hr>"); i += 1; continue
        if ln.strip() == "":
            i += 1; continue
        para = [ln]
        i += 1
        while i < len(lines) and lines[i].strip() and not re.match(r"^(#|- |\||> |---)", lines[i]):
            para.append(lines[i]); i += 1
        out.append(f"<p>{md_inline(' '.join(para), resolve)}</p>")
    return "\n".join(out)


READER_CSS = """
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,400;9..144,600&family=Newsreader:opsz,wght@6..72,400;6..72,500&family=IBM+Plex+Mono:wght@400;500&display=swap');
:root{--paper:#f6f1e7;--paper-2:#fbf8f2;--ink:#221f1a;--ink-soft:#5f574c;--line:#d9d0c0;--pine:#2f5d4e;--pine-d:#244a3e;--clay:#b8623f;--ochre:#c9962b;--tint:#e8efe9}
*{box-sizing:border-box}body{margin:0;background:var(--paper);color:var(--ink);font-family:Newsreader,Georgia,serif;font-size:17px;line-height:1.5}
.app{display:grid;grid-template-columns:280px 1fr;min-height:100vh}
nav{border-right:1px solid var(--line);padding:18px 16px;background:var(--paper-2);position:sticky;top:0;height:100vh;overflow:auto}
nav .brand{font-family:Fraunces,Georgia,serif;font-size:22px;color:var(--pine-d);margin:0 0 2px}
nav .tag{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin-bottom:14px}
nav input{width:100%;padding:7px 9px;border:1px solid var(--line);border-radius:6px;background:#fff;font:inherit;font-size:14px;margin-bottom:12px}
nav h4{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--pine-d);margin:16px 0 6px;border-bottom:1px solid var(--line);padding-bottom:4px}
nav a{display:block;color:var(--ink);text-decoration:none;font-size:14.5px;padding:3px 6px;border-radius:4px;line-height:1.3}
nav a:hover{background:var(--tint)}nav a.on{background:var(--pine);color:#fff}
nav a .k{font-family:'IBM Plex Mono',monospace;font-size:11px;color:var(--ink-soft);margin-right:6px}nav a.on .k{color:#dfe9e3}
main{padding:36px 52px 80px;max-width:980px}
h1{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:34px;line-height:1.15;margin:0 0 14px;color:var(--pine-d)}
h2{font-family:Fraunces,Georgia,serif;font-weight:600;font-size:22px;margin:30px 0 10px;border-bottom:1px solid var(--line);padding-bottom:4px}
h3{font-family:'IBM Plex Mono',monospace;font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:var(--pine-d);margin:22px 0 6px}
p{margin:0 0 12px}em{color:var(--ink-soft)}blockquote{margin:0 0 14px;padding:10px 16px;border-left:3px solid var(--ochre);background:var(--paper-2);color:var(--ink-soft);font-size:15.5px}
table{border-collapse:collapse;width:100%;margin:6px 0 18px;font-size:15px}th{text-align:left;font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.06em;text-transform:uppercase;color:var(--ink-soft);border-bottom:2px solid var(--ink);padding:6px 8px;vertical-align:bottom}
td{border-bottom:1px solid var(--line);padding:7px 8px;vertical-align:top}tr:hover td{background:var(--paper-2)}
a.wl{color:var(--pine);text-decoration:none;border-bottom:1px solid #b8ccc2}a.wl:hover{border-bottom-color:var(--pine)}.wl-dead{color:var(--clay);border-bottom:1px dashed var(--clay)}
code{font-family:'IBM Plex Mono',monospace;font-size:13px;background:var(--paper-2);padding:1px 4px;border:1px solid var(--line);border-radius:3px}
ul{padding-left:22px;margin:0 0 12px}li{margin:3px 0}hr{border:0;border-top:1px solid var(--line);margin:24px 0}
.crumb{font-family:'IBM Plex Mono',monospace;font-size:11px;letter-spacing:.08em;text-transform:uppercase;color:var(--ink-soft);margin-bottom:10px}
.wrap{overflow-x:auto}
@media(max-width:820px){.app{grid-template-columns:1fr}nav{position:static;height:auto;border-right:0;border-bottom:1px solid var(--line)}main{padding:22px 18px 60px}h1{font-size:27px}}
"""

READER_JS = """
const PAGES = __PAGES__;
const NAV = __NAV__;
function render(){
  let id = decodeURIComponent(location.hash.slice(1)) || 'Water';
  if(!PAGES[id]) id='Water';
  const p = PAGES[id];
  document.getElementById('crumb').textContent = p.crumb;
  document.getElementById('page').innerHTML = p.html;
  document.title = p.title + ' · Aruvi water wiki';
  document.querySelectorAll('nav a').forEach(a=>a.classList.toggle('on', a.getAttribute('href')==='#'+id));
  window.scrollTo(0,0);
}
function buildNav(){
  const q=(document.getElementById('q').value||'').toLowerCase();
  let h='';
  for(const sec of NAV){
    const items=sec.items.filter(it=>!q||it.label.toLowerCase().includes(q)||(it.k||'').toLowerCase().includes(q));
    if(!items.length) continue;
    h+='<h4>'+sec.title+'</h4>';
    for(const it of items) h+='<a href="#'+it.id+'">'+(it.k?'<span class="k">'+it.k+'</span>':'')+it.label+'</a>';
  }
  document.getElementById('navlist').innerHTML=h;
  render();
}
window.addEventListener('hashchange',render);
document.getElementById('q').addEventListener('input',buildNav);
buildNav();
"""


def build_reader(pages, nav):
    """pages: id -> {title, crumb, md}. nav: list of {title, items:[{id,label,k}]}"""
    ids = set(pages)
    def resolve(target):
        return target if target in ids else None
    P = {pid: {"title": pg["title"], "crumb": pg["crumb"], "html": md_to_html(pg["md"], resolve)} for pid, pg in pages.items()}
    js = READER_JS.replace("__PAGES__", json.dumps(P, ensure_ascii=False)).replace("__NAV__", json.dumps(nav, ensure_ascii=False))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Aruvi · water wiki (pilot)</title><style>{READER_CSS}</style></head><body>
<div class="app"><nav><div class="brand">Aruvi wiki</div><div class="tag">pilot · water thread</div>
<input id="q" type="search" placeholder="filter pages…"><div id="navlist"></div></nav>
<main><div class="crumb" id="crumb"></div><div id="page" class="wrap"></div></main></div>
<script>{js}</script></body></html>"""

# ----------------------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--extract", required=True)
    ap.add_argument("--summaries", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()

    chapters = load_extract(a.extract)
    by = index_nodes(chapters)
    jc = joint_candidates(by)

    out = a.out
    for d in ("concepts", "chapters", "views", "_build"):
        os.makedirs(os.path.join(out, d), exist_ok=True)

    pages = {}  # id -> {title, crumb, md, path}
    def add(pid, path, title, crumb, md):
        pages[pid] = {"title": title, "crumb": crumb, "md": md}
        with open(os.path.join(out, path), "w", encoding="utf-8") as f:
            f.write(md)

    add("Water", "Water.md", "Water", "theme", page_hub(chapters, by))
    for cid, name, _ in VOCAB:
        add(cid, f"concepts/{cid}.md", name, "idea", page_concept(cid, by, chapters, jc))
    for c in chapters:
        add(c["key"], f"chapters/{c['key']}.md", c["title"], f"chapter · {SUBJ[c['subject']]} · {cls(c['g'])}",
            page_chapter(c, excerpt(a.summaries, c)))
    add("spiral-water", "views/spiral-water.md", "The spiral", "view", page_spiral(by))
    add("joint-classes", "views/joint-classes.md", "Joint-class candidates", "view", page_joint(jc))
    add("cross-subject", "views/cross-subject.md", "Cross-subject connections", "view", page_cross(chapters, by))

    # provenance
    merged = {"theme": "water", "vocabulary": [{"id": i, "name": n, "description": d} for i, n, d in VOCAB], "chapters": chapters}
    json.dump(merged, open(os.path.join(out, "_build", "water_concepts.json"), "w"), indent=1, ensure_ascii=False)
    shutil.copy(os.path.abspath(__file__), os.path.join(out, "_build", "build_wiki.py"))
    ins = os.path.join(a.extract, "INSTRUCTIONS.md")
    if os.path.exists(ins):
        shutil.copy(ins, os.path.join(out, "_build", "INSTRUCTIONS.md"))

    # single-file reader
    nav = [
        {"title": "Start", "items": [{"id": "Water", "label": "Water — the thread"}]},
        {"title": "Views", "items": [{"id": "spiral-water", "label": "The spiral"}, {"id": "joint-classes", "label": "Joint-class candidates"}, {"id": "cross-subject", "label": "Cross-subject connections"}]},
        {"title": "Ideas", "items": [{"id": cid, "label": name, "k": str(len(by.get(cid, [])))} for cid, name, _ in VOCAB]},
        {"title": "Chapters", "items": [{"id": c["key"], "label": f"{c['title']}", "k": f"{SUBJ_SHORT[c['subject']]} {c['g']}·{c['chapter']}"} for c in chapters if c["concepts"]]},
    ]
    with open(os.path.join(out, "wiki.html"), "w", encoding="utf-8") as f:
        f.write(build_reader(pages, nav))

    # link check
    ids = set(pages)
    dead = []
    for pid, pg in pages.items():
        for m in re.finditer(r"\[\[([^\]|]+)", pg["md"]):
            if m.group(1) not in ids:
                dead.append((pid, m.group(1)))
    n_nodes = sum(len(c["concepts"]) for c in chapters)
    print(f"pages: {len(pages)}  (concepts {len(VOCAB)}, chapters {len(chapters)}, views 3, hub 1)")
    print(f"nodes: {n_nodes}  joint-class cells: {len(jc)}  dead links: {len(dead)}")
    for d in dead[:20]:
        print("  DEAD", d)


if __name__ == "__main__":
    main()
