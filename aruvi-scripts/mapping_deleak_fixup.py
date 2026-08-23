import json, re, glob, os, sys
import pathlib
ROOT=str(pathlib.Path(__file__).resolve().parents[1] / 'data/cloud/content/chapters')
DRY='--apply' not in sys.argv
FIX=[
 (r"\bIt is treated as a major strand rather than central focus\b","It is a major strand rather than the chapter's central focus"),
 (r"\bIt is major strand rather than central focus\b","It is a major strand rather than the chapter's central focus"),
 (r",\s*giving major strand\b",", so it is a major strand"),
 (r",\s*giving central focus\b",", so it is the chapter's central focus"),
 (r",\s*giving supporting mention\b",", so it is a supporting mention"),
 (r",?\s*meeting the major strand test\b",", which makes it a major strand"),
 (r",?\s*meeting the central focus test\b",", which makes it the chapter's central focus"),
 (r",?\s*satisfying the [a-z-]+(?: [a-z-]+)? test for major strand\b",", which makes it a major strand"),
 (r",?\s*satisfying the [a-z-]+(?: [a-z-]+)? test for central focus\b",", which makes it the chapter's central focus"),
 (r",?\s*hence major strand\b",", so it is a major strand"),
 (r",?\s*hence central focus\b",", so it is the chapter's central focus"),
 (r",?\s*warranting supporting mention\b",", so it is a supporting mention"),
 (r",?\s*warranting major strand\b",", so it is a major strand"),
 (r"\bso central focus is not reached\b","so it is not the chapter's central focus"),
 (r"\bso major strand is not reached\b","so it is not a major strand"),
 (r"\s*[—–]\s*,\s*"," — "),(r"\s{2,}"," "),(r"\s+([,.;])",r"\1"),
]
stats={'files':0,'fields':0}
for f in sorted(glob.glob(os.path.join(ROOT,'*/*/mappings/*.json'))):
    raw=open(f,encoding='utf-8').read(); d=json.loads(raw); newraw=raw; touched=False
    for b in ('competencies','primary','incidental','core_competencies','adjunct_competencies'):
        for c in (d.get(b) or []):
            old=c.get('justification')
            if not old: continue
            new=old
            for p,r in FIX: new=re.sub(p,r,new)
            if new==old: continue
            for ea in (False,True):
                oe=json.dumps(old,ensure_ascii=ea)
                if newraw.count(oe)==1:
                    newraw=newraw.replace(oe,json.dumps(new,ensure_ascii=ea)); touched=True; stats['fields']+=1
                    if DRY: print('OLD:',old[-160:],'\nNEW:',new[-160:],'\n')
                    break
            else: print('UNMATCHED',f)
    if touched:
        stats['files']+=1
        base=json.loads(raw); chk=json.loads(newraw)
        def strip(o):
            if isinstance(o,dict): return {k:('~' if k=='justification' else strip(v)) for k,v in o.items()}
            if isinstance(o,list): return [strip(v) for v in o]
            return o
        assert strip(chk)==strip(base), f
        if not DRY: open(f,'w',encoding='utf-8').write(newraw)
print(stats,'DRY' if DRY else 'WRITTEN')
