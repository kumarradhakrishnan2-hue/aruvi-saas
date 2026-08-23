import json, re, glob, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from mapping_deleak_scrub import scrub

import pathlib
ROOT = str(pathlib.Path(__file__).resolve().parents[1] / 'data/cloud/content/chapters')
DRY = '--apply' not in sys.argv

CATS = [
 re.compile(r"\bRules?\s*\d+(\s*\([a-z]\))?|\bunder Rule|\bthe (?:mapping|weighting) constitution\b"),
 re.compile(r"\bWeight\s*[123]\b|\bweighted at\s*[123]\b|\bweight(?:ed)?\s+(?:at|of)\s*[123]\b|\(not\s*[123]\)|\b(?:Central|Substantive|Contributory|Present)\s*\(Weight|\bWeight\s*[123]\s*\(|\bqualif(?:ies|y)\s+for\s+(?:a\s+)?(?:higher\s+)?[Ww]eight|\bhigher weight\b|\bhalf-weight\b"),
 re.compile(r"[Dd]issolution test|[Rr]emov(?:al|ing|e)\s+(?:of\s+)?(?:this|the)\s+competency|would (?:structurally )?dissolve|structurally dissolves|positional test|\bWeight\s*3\s*test\b|\bthe .{0,25}\btest\b(?=[^.]*\b(?:satisf|met|pass|fail|appl))"),
 re.compile(r"architecturally distinct|could stand alone as a learning unit|stand alone as a learning unit|developed substantively and deliberately across multiple named sections|overarching structural framework|named structural element|[Pp]resent rather than [Ss]ubstantive|dedicated,? (?:architecturally distinct|named) section|primary structural activity|organising logic making continuity|governing sub-discipline|sub-discipline governing|sub-discipline|stand as (?:an )?independent learning units?|could stand as independent"),
 re.compile(r"\bco-central\b|\badjunct\b|\bincidental\b|\bsubstantive(?:ly)?\b|\bcore competenc|\bprimary competenc|\bcontributory\b"),
]
def flagged(s): return any(p.search(s) for p in CATS)
def split_sent(t):
    return [p.strip() for p in re.split(r'(?<=[.!?][\'"\u2019\u201d])\s+(?=[A-Z“"\'(])|(?<=[.!?])\s+(?=[A-Z“"\'(])', t) if p.strip()]

def new_just(old):
    sents = split_sent(old.replace('\n', ' '))
    out, changed, deleted = [], 0, 0
    for s in sents:
        if not flagged(s):
            out.append(s); continue
        rw = scrub(s).strip()
        if not rw:
            deleted += 1; continue
        if rw != s: changed += 1
        out.append(rw)
    return ' '.join(out), changed, deleted

