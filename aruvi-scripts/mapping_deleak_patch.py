from mapping_deleak_common import *
import json, re, glob, sys, os
from mapping_deleak_scrub import scrub
DRY = '--apply' not in sys.argv

stats = dict(files=0, entries=0, changed=0, deleted=0, fallback=0)
report = []
for f in sorted(glob.glob(os.path.join(ROOT, '*/*/mappings/*.json'))):
    raw = open(f, encoding='utf-8').read()
    d = json.loads(raw)
    newraw = raw
    touched = False
    for bucket in ('competencies','primary','incidental','core_competencies','adjunct_competencies'):
        for i, c in enumerate(d.get(bucket) or []):
            old = c.get('justification')
            if not old: continue
            stats['entries'] += 1
            nj, ch, de = new_just(old)
            if nj == old: continue
            stats['changed'] += ch; stats['deleted'] += de
            # byte-safe swap: try both ensure_ascii encodings
            for ea in (False, True):
                oe = json.dumps(old, ensure_ascii=ea)
                if newraw.count(oe) == 1:
                    newraw = newraw.replace(oe, json.dumps(nj, ensure_ascii=ea))
                    touched = True
                    break
            else:
                stats['fallback'] += 1
                report.append(('UNMATCHED', f, bucket, i))
    if touched:
        stats['files'] += 1
        # integrity: parses, and differs from the original only in justification values
        chk = json.loads(newraw)
        base = json.loads(raw)
        def strip(o):
            if isinstance(o, dict): return {k: ('~' if k == 'justification' else strip(v)) for k, v in o.items()}
            if isinstance(o, list): return [strip(v) for v in o]
            return o
        assert strip(chk) == strip(base), f
        if not DRY:
            open(f, 'w', encoding='utf-8').write(newraw)

print(json.dumps(stats, indent=1))
for r in report: print(r)
print('DRY RUN' if DRY else 'WRITTEN')
