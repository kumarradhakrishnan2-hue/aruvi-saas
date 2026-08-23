import json, re, glob, os, sys
import pathlib
ROOT=str(pathlib.Path(__file__).resolve().parents[1] / 'data/cloud/content/chapters')
DRY='--apply' not in sys.argv
FIX=[(r"\ban (?=passing|genuine|self-contained|distinct|supporting|major|central|part of the chapter|section)", "a "),
     (r"\ba (?=essential|element\b|independent|expression|instantiation|engagement|orientation|item\b)", "an ")]
def strip(o):
    if isinstance(o,dict): return {k:('~' if k=='justification' else strip(v)) for k,v in o.items()}
    if isinstance(o,list): return [strip(v) for v in o]
    return o
n=0
for f in sorted(glob.glob(os.path.join(ROOT,'*/*/mappings/*.json'))):
    raw=open(f,encoding='utf-8').read(); d=json.loads(raw); newraw=raw; t=False
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
                    newraw=newraw.replace(oe,json.dumps(new,ensure_ascii=ea)); t=True; n+=1; break
            if DRY:
                import difflib
                a=old.split(); bb=new.split(); sm=difflib.SequenceMatcher(None,a,bb)
                for tag,i1,i2,j1,j2 in sm.get_opcodes():
                    if tag!='equal': print(' ',f.split('chapters/')[1],'|',' '.join(a[max(0,i1-3):i2+3]),'->',' '.join(bb[max(0,j1-3):j2+3]))
    if t:
        assert strip(json.loads(newraw))==strip(d), f
        if not DRY: open(f,'w',encoding='utf-8').write(newraw)
print('fields:',n,'DRY' if DRY else 'WRITTEN')
