import json, re, glob, os, sys
import pathlib
ROOT=str(pathlib.Path(__file__).resolve().parents[1] / 'data/cloud/content/chapters')
DRY='--apply' not in sys.argv
FIX=[
 # --- "named structural element" family ---
 (r"(?i)\bNamed structural elements qualifying as present\.", "These are present in the chapter, but not a main focus."),
 (r"(?i)\bNamed structural element qualifying as present\.", "It is present in the chapter, but not a main focus."),
 (r"(?i)\bNamed elements qualifying as present\.", "These are present in the chapter, but not a main focus."),
 (r"(?i)\bNamed structural element demonstrating\b", "This part of the chapter shows"),
 (r"(?i)\bNamed structural elements within the chapter\b", "Parts of the chapter"),
 (r"(?i)\bNamed structural elements are present:", "Several parts of the chapter carry it:"),
 (r"(?i)\bNamed structural elements\b", "Parts of the chapter"),
 (r"(?i)\bNamed structural element\b", "A part of the chapter"),
 (r"(?i)\bacross multiple structural elements\b", "across several parts of the chapter"),
 (r"(?i)\bThis structural element\b", "This element"),
 (r"(?i)\bcontains a structural element\b", "contains an element"),
 (r"(?i)\bstructural elements\b", "parts of the chapter"),
 (r"(?i)\bstructural element\b", "element"),
 # --- "qualifying as ..." verdicts ---
 (r",?\s*qualifying as weight\s*1\.", ", so it is a supporting mention."),
 (r",?\s*qualifying as present but not constituting\b", ", present but without"),
 (r",?\s*qualifying as present but not\b", ", present but not"),
 (r",?\s*qualifying as present\.", "; it is present but not a main focus."),
 # --- dissolution, C-code phrasings ---
 (r"(?i)Remove\s+C-\d+\.\d+\s+and\s+the chapter's[^.;]*?dissolves", "Without it the chapter has no purpose"),
 (r"(?i)(?:Removing|Removal of)\s+C-\d+\.\d+\s+dissolves\s+the chapter's[^.;—]*?purpose", "The chapter would have no purpose without it"),
 # --- the constitution's "architecture" vocabulary ---
 (r"(?i)\bnamed architectural elements\b", "parts of the chapter"),
 (r"\barchitecturally\s+", ""),
 (r"\barchitectural\s+", ""),
 # --- tidy ---
 (r"\s*[—–]\s*,\s*", " — "), (r"\s{2,}", " "), (r"\s+([,.;])", r"\1"), (r",\s*,", ","), (r";\s*;", ";"),
]
def strip(o):
    if isinstance(o,dict): return {k:('~' if k=='justification' else strip(v)) for k,v in o.items()}
    if isinstance(o,list): return [strip(v) for v in o]
    return o
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
            done=False
            for ea in (False,True):
                oe=json.dumps(old,ensure_ascii=ea)
                if newraw.count(oe)==1:
                    newraw=newraw.replace(oe,json.dumps(new,ensure_ascii=ea)); done=True; break
            assert done, f
            touched=True; stats['fields']+=1
            if DRY:
                import difflib
                a=old.split(); bb=new.split()
                sm=difflib.SequenceMatcher(None,a,bb)
                for tag,i1,i2,j1,j2 in sm.get_opcodes():
                    if tag!='equal':
                        print(f"  {f.split('chapters/')[1][:46]:46s} '{' '.join(a[i1:i2])[:70]}' -> '{' '.join(bb[j1:j2])[:70]}'")
    if touched:
        assert strip(json.loads(newraw))==strip(d), f
        stats['files']+=1
        if not DRY: open(f,'w',encoding='utf-8').write(newraw)
print(json.dumps(stats)); print('DRY RUN' if DRY else 'WRITTEN')
