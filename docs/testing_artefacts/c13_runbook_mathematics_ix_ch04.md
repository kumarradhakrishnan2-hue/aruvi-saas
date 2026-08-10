# C13 runbook — failure paths · mathematics · IX · ch 4

Four requests. Every expected code and body below was read off the handler in `api/main.py`
or raised for real in-process, so anything different on your machine is a genuine finding.

Base `http://localhost:8000`, identity header `X-Aruvi-User: kumar1`.

---

## 1 · No library for the chapter → **404**

```bash
curl -s -i -X POST http://localhost:8000/genon/mathematics/ix/16/plan \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' \
  -d '{"rows":[{"duration":50,"count":10}]}'
```

Expect `404` and exactly:

```json
{"detail":"No underlying chapter yet."}
```

Chapter 16 is a maths·IX row with no authored library. The wording is the 2026-08-04 founder
change and is the point of the check — *"canonical" is our word, not hers*. If the body says
"canonical" anywhere, that's the defect, even though the sentence would be true.

## 2 · Implausible matrix → **400** (two shapes)

```bash
# a. over the ceiling
curl -s -i -X POST http://localhost:8000/genon/mathematics/ix/4/plan \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' \
  -d '{"rows":[{"duration":50,"count":31}]}'

# b. nothing to serve
curl -s -i -X POST http://localhost:8000/genon/mathematics/ix/4/plan \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' \
  -d '{"rows":[]}'
```

Expect `400` and, respectively:

```json
{"detail":"More than 30 periods is too many for one chapter."}
{"detail":"At least one duration row is required."}
```

The ceiling is `total_periods > 30`, summed across rows — so `40×16 + 60×15` must also fail,
which is worth one extra call if you want the sum path covered rather than the single-row one.

## 3 · Unresolvable item anchor → **500 with the item named**

```bash
cp data/content/saved_plans/mathematics/ix/ch_04_canonical.json \
   data/content/saved_plans/mathematics/ix/ch_99_canonical.json
# point one item's anchor at a unit that does not exist
python3 - <<'PY'
import json,pathlib
p=pathlib.Path('data/content/saved_plans/mathematics/ix/ch_99_canonical.json')
d=json.loads(p.read_text()); d['chapter_number']=99
def items(o):
    if isinstance(o,dict):
        if isinstance(o.get('questions'),list): yield from o['questions']
        for v in o.values(): yield from items(v)
    elif isinstance(o,list):
        for v in o: yield from items(v)
it=list(items(d['result']))[3]; it['period_ref']=[99]; it['section_number']=99
p.write_text(json.dumps(d,indent=1,ensure_ascii=False))
PY

curl -s -i -X POST http://localhost:8000/genon/mathematics/ix/99/plan \
  -H 'Content-Type: application/json' -H 'X-Aruvi-User: kumar1' \
  -d '{"rows":[{"duration":50,"count":10}]}'

rm data/content/saved_plans/mathematics/ix/ch_99_canonical.json   # ← do not skip
```

Expect `500` and a body that **names the item**. Raised for real in-process, this is the
message the handler wraps:

```
Canonical cannot be compiled: canonical plan is not v1.1-declared (1 problem):
assessment item #4 NUM / C-3.1: no resolvable anchor unit (period_ref/phase_ref) — it names [99]
```

That is the check: not a bare 500, and no traceback. Verified: the exception text carries
neither `Traceback` nor a `File "…"` line.

## 4 · Quarantined variant absent from serving

Read the C10.5 transcript as a failure path: move `ch_04_canonical_p09.json` into
`backup/quarantine/mathematics/ix/`, re-request **8 periods** (which p09 had served), and check
that nothing 500s and no response names the quarantined file. Restore afterwards.

Expected, from the proxy run already done in the sandbox: the serve falls to the **12**-unit
canonical, still returns 8 sittings, and the string `p09` appears nowhere in the response.

---

## Two adjacent gaps found while verifying this — not part of C13's four

Both need a **corrupt canonical on disk**, which certification's compile check would have
caught at build time, so the exposure is low. Recorded because C13 is where they'd surface.

| Corruption | Raises | Caught by the handler? |
|---|---|---|
| item anchors a non-existent unit | `GenonDeclarationError` | **yes** → the readable 500 above |
| a period loses `section_anchor` | `KeyError` — *"period 3 has no section_anchor, and Mathematics·Grade IX anchors units to sections"* | **no** |
| a time band's `minutes` is malformed | `ValueError` — *"not enough values to unpack (expected 2, got 1)"* | **no** |

The handler catches `GenonDeclarationError` and `ServeError` only, so the other two escape as
an unhandled 500. C13's exit still holds — FastAPI's default 500 body is
`{"detail":"Internal Server Error"}` with the traceback going to the log, not the response — but
the *first* message is teacher-unreadable and the *second* is a developer message that names
nothing. If it's ever worth closing, the fix is one more `except` clause converting both into
the same "Canonical cannot be compiled: …" shape the declared path already uses.
