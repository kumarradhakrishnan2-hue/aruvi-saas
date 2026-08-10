# Testing read-after-write · Area 1 · adding a subject

One action, three outcomes. The point of the doctrine is that **only the middle one speaks**, so
two of these three tests are passed by *seeing nothing happen*.

Throughout: `PROFILE=data/readiness/kumar1/kumar1/profile.json` (swap `kumar1` for whoever you
are signed in as on the phone).

Before you start, note what the profile holds now:

```bash
cd ~/main/kumar/AI/aruvi-saas
python3 -c "
import json,pathlib
d=json.loads(pathlib.Path('data/readiness/kumar1/kumar1/profile.json').read_text())
print([s['name'] for s in d['subjects']])"
```

---

## A · It works → **silence**

The control. If this shows a message, the comparator is too strict and everything else is noise.

1. Phone → **settings gear → teaching profile**.
2. Add a subject you don't have (say **Science**) with one class and one section.
3. **Expect: no message.** The subject appears in the list, and that is all.

Confirm it truly landed:

```bash
python3 -c "
import json,pathlib
d=json.loads(pathlib.Path('data/readiness/kumar1/kumar1/profile.json').read_text())
print([s['name'] for s in d['subjects']])"
```

Science is in the list. **Y′ = Y → ok → nothing said.** Now remove it again so B starts clean.

---

## B · It silently didn't save → **the message fires**

This is the case the whole mechanism exists for: the server accepts the request, the write does
not land, and without the check she would never know.

**Stage it** — make the profile unwritable. The server can still *read* it, which is what makes
this a mismatch rather than an outage:

```bash
chmod 444 data/readiness/kumar1/kumar1/profile.json
```

**Do it** — on the phone, add **Science** again exactly as in A.

**Expect, in this order:**

1. Science appears for a moment (the optimistic update).
2. A line at the top of the profile:
   *"That change didn't save — this is your teaching profile as it stands."*
3. **Science disappears from the list.**

Point 3 is the part worth watching. The view has been re-synced to what the server actually
holds, so the screen and the disk now agree. Telling her it failed while leaving Science on
screen would recreate the exact divergence the check exists to catch.

**Undo it:**

```bash
chmod 644 data/readiness/kumar1/kumar1/profile.json
```

Add Science once more — it should now save silently, as in A.

---

## C · We can't tell → **silence, deliberately**

The doctrine's own limit, and the reason it is honest rather than merely careful.

1. **Stop the API** (Ctrl-C in the uvicorn tab).
2. On the phone, add **Science**.
3. **Expect: no message.** Science stays on screen.

Nothing is claimed because nothing can be checked. Presuming failure here would invent a fact —
the write might have landed and the response been lost.

4. Restart the API, pull down to refresh.
5. Science is **gone** — it never saved.

**This is the residual gap, and you should see it rather than take my word for it.** Between
step 3 and step 5 the screen shows a subject the server does not have. The doctrine forbids
calling that an error, and I think that is right; the alternative is warning her about a
failure that may not have happened. But it is a real window, and if it ever needs closing the
answer is a *pending* state ("not yet confirmed"), which is a third thing — neither success nor
error — and a bigger design decision than this change.

---

## What each outcome proves

| Case | Y′ | outcome | she sees | proves |
|---|---|---|---|---|
| A | = Y | `ok` | nothing | no false alarms |
| B | ≠ Y | `mismatch` | the line + the true state | the only case that speaks |
| C | none | `unverified` | nothing | we never guess |

The comparator behind B is covered by `tests/test_verify_readiness.mjs` (17 checks, `node
tests/test_verify_readiness.mjs`) — most of them asserting what must **not** fire: section
order, subject order, grade case, duration order, `"7"` vs `7`, budget edits.
