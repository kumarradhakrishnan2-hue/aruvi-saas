import json, os, sys, collections
import pathlib
ROOT=str(pathlib.Path(__file__).resolve().parents[1] / 'data/cloud/content/chapters')
DRY='--apply' not in sys.argv
rows={r['id']:r for r in json.load(open('ss_long.json'))}
prop={}
for b in range(4):
    for o in json.load(open(f'out{b}.json')): prop[o['id']]=o['proposed']
assert len(prop)==len(rows)==77
byfile=collections.defaultdict(list)
for i,r in rows.items(): byfile[r['file']].append(i)

def strip(o):
    if isinstance(o,dict): return {k:('~' if k=='justification' else strip(v)) for k,v in o.items()}
    if isinstance(o,list): return [strip(v) for v in o]
    return o

stats={'files':0,'fields':0,'words_before':0,'words_after':0}
for rel,ids in sorted(byfile.items()):
    path=os.path.join(ROOT,rel)
    raw=open(path,encoding='utf-8').read(); d=json.loads(raw); newraw=raw
    for i in ids:
        r=rows[i]
        cur=d[r['bucket']][r['idx']].get('justification')
        # the record must still match what we read when we proposed
        assert cur==r['text'], f"drifted since proposal: {rel} {r['code']}"
        new=prop[i]
        assert len(new.split())<120, (rel,r['code'])
        done=False
        for ea in (False,True):
            oe=json.dumps(cur,ensure_ascii=ea)
            if newraw.count(oe)==1:
                newraw=newraw.replace(oe,json.dumps(new,ensure_ascii=ea)); done=True; break
        assert done, f"no unique match: {rel} {r['code']}"
        stats['fields']+=1; stats['words_before']+=r['words']; stats['words_after']+=len(new.split())
    chk=json.loads(newraw)
    assert strip(chk)==strip(d), rel
    stats['files']+=1
    if not DRY: open(path,'w',encoding='utf-8').write(newraw)
print(json.dumps(stats,indent=1)); print('DRY RUN' if DRY else 'WRITTEN')
