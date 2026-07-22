"""
build_kb.py — regenerate the app's qa_knowledge_base.json from the AUTHORITATIVE
Ask Aruvi V3 knowledge base.

Source of truth (maintained by the aruvi-kb-refresh pipeline):
    data/content/ask_aruvi/Aruvi_Ask_Aruvi_QA_Knowledge_Base_V3.0_2.json
      { metadata, categories: { cat_a..e: { label, description, pairs:[{id,q,a}] } } }

This script flattens it into the shape the Ask Aruvi screen consumes, and adds a
derived 6-keyword search index per pair (tf-idf). Keywords are NEVER hand-maintained
— they are regenerated from q/a every run, so a KB refresh just means re-running this.

Deferred pairs (empty answer, e.g. d03/d13/d14) are SKIPPED, matching the loader.

normalize() here MUST stay byte-for-byte identical to askAruviSearch.js normalize().

Usage:
    python3 build_kb.py <V3_source.json> [out.json]
"""
import re, json, math, sys, unicodedata
from collections import Counter, defaultdict

SRC = sys.argv[1] if len(sys.argv) > 1 else 'Aruvi_Ask_Aruvi_QA_Knowledge_Base_V3.0_2.json'
OUT = sys.argv[2] if len(sys.argv) > 2 else 'qa_knowledge_base.json'

# short tag (search-result chip) + accent (globals.css section palette), by category id
CAT_TAG    = {'cat_a':'Lessons','cat_b':'Assessments','cat_c':'Time','cat_d':'Platform','cat_e':'Limits'}
CAT_ACCENT = {'cat_a':'var(--sec-a)','cat_b':'var(--sec-b)','cat_c':'var(--sec-c)','cat_d':'var(--sec-d)','cat_e':'var(--ss-plum)'}

src = json.load(open(SRC))
cats = src['categories']

# ---- flatten pairs (skip deferred = empty answer) ----
pairs=[]; deferred=[]
for cid, c in cats.items():
    for p in c.get('pairs', []):
        q=(p.get('q') or '').strip(); a=(p.get('a') or '').strip()
        if not a:
            deferred.append(p.get('id')); continue
        pairs.append({'id':p['id'],'category':cid,'question':q,'answer':a})

# ---- normalization (mirror of askAruviSearch.js) ----
STOP=set('''a an the of to in on for and or but with without as at by from into is are was were be been being do does did done how what why when which who whom whose this that these those it its their they them there here he she his her our your you we us i me my mine one two three four five six all any some more most other another use used uses using make makes made get gets got give gives given also only just very much many few both same own about over under between during before after out up down off above below because while where whether can cannot not no yes if then than so such each per within across need needs want wants work works thing things help helps helped teacher teachers lesson lessons plan plans aruvi whole full'''.split())
ROMAN=set('i ii iii iv v vi vii viii ix x xi xii'.split())
GRADEWORD=re.compile(r'^(ncf|ncert)$')

def strip_accents(x): return ''.join(c for c in unicodedata.normalize('NFD',x) if unicodedata.category(c)!='Mn')
def norm(tok):
    tok=strip_accents(tok.lower()); tok=re.sub(r'[^a-z0-9]','',tok)
    if len(tok)>4 and tok.endswith('ies'): tok=tok[:-3]+'y'
    elif len(tok)>4 and re.search(r'(s|x|z|ch|sh)es$',tok): tok=tok[:-2]
    elif len(tok)>3 and tok.endswith('s') and not tok.endswith('ss') and not tok.endswith('us'): tok=tok[:-1]
    return tok
def words(text):
    for w in re.findall(r"[A-Za-z0-9]+",text):
        n=norm(w)
        if len(n)>=3 and n not in STOP and n not in ROMAN and not GRADEWORD.match(n):
            yield n, strip_accents(w.lower())

# ---- tf-idf keyword pick (readable surface form) ----
df=defaultdict(int); surf=defaultdict(Counter); per=[]
for p in pairs:
    qn=[]; an=[]
    for n,s in words(p['question']): qn.append(n); surf[n][s]+=1
    for n,s in words(p['answer']):   an.append(n); surf[n][s]+=1
    for n in set(qn+an): df[n]+=1
    per.append((qn,an))
Np=len(pairs)
for p,(qn,an) in zip(pairs,per):
    tf=defaultdict(float)
    for n in qn: tf[n]+=3.0
    for n in an: tf[n]+=1.0
    ranked=sorted(tf, key=lambda n: tf[n]*math.log((Np+1)/df[n]), reverse=True)
    keys=ranked[:6]
    while len(keys)<6 and len(keys)<len(ranked): keys.append(ranked[len(keys)])
    p['keywords']=[surf[k].most_common(1)[0][0] for k in keys]

kb={
 'version': src.get('metadata',{}).get('version','V3.0'),
 'generated_from': SRC.split('/')[-1],
 'last_refreshed': src.get('metadata',{}).get('last_refreshed'),
 'categories':[{'id':cid,'title':c['label'],'description':c['description'],
                'tag':CAT_TAG.get(cid,cid),'accent':CAT_ACCENT.get(cid,'var(--ink-soft)')}
               for cid,c in cats.items()],
 'pairs':pairs,
}
json.dump(kb,open(OUT,'w'),ensure_ascii=False,indent=2)
print('pairs:',len(pairs),'| skipped deferred:',deferred)
print('by category:',dict(Counter(p['category'] for p in pairs)))
for p in kb['pairs'][:5]:
    print(' ',p['id'],p['category'],'::',p['keywords'],'|',p['question'][:60])
