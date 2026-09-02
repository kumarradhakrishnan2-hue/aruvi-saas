#!/usr/bin/env python3
"""Step 1 of the pilot: keyword scan over every chapter summary to shortlist candidates for a theme.
Usage: python3 scan_theme.py /path/to/data/authoring/chapters water rain monsoon river ... > scan.tsv
"""
import json, re, glob, sys, os
root, kws = sys.argv[1], [k.lower() for k in sys.argv[2:]]
def flat(o, out):
    if isinstance(o, dict): [flat(v, out) for v in o.values()]
    elif isinstance(o, list): [flat(v, out) for v in o]
    elif isinstance(o, str): out.append(o)
for p in sorted(glob.glob(os.path.join(root, '*/*/summaries/ch_*_summary.*'))):
    subj, grade = p.split(os.sep)[-4], p.split(os.sep)[-3]
    ch = int(re.search(r'ch_(\d+)', p).group(1))
    if p.endswith('.json'):
        out = []; flat(json.load(open(p)), out); text = '\n'.join(out)
    else:
        text = open(p, encoding='utf-8', errors='replace').read()
    low = text.lower()
    counts = {k: low.count(k) for k in kws}
    print(f"{subj}\t{grade}\t{ch}\t{counts[kws[0]]}\t{sum(counts.values())}\t{text.splitlines()[0][:80]}")
