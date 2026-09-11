#!/usr/bin/env python3
"""Regenerate theme/tokens.js from web/app/globals.css. Run from mobile/: python3 theme/gen-tokens.py
The web is the source of every colour; this keeps the phone's palette byte-equal to it."""
import json, re, pathlib
here = pathlib.Path(__file__).resolve().parent
css = (here.parent.parent / "web/app/globals.css").read_text()
tok = re.compile(r"(?<![\w-])(--[\w-]+):\s*((?:#[0-9a-fA-F]{3,8}|rgba?\([^)]*\)|var\(--[\w-]+\)))\s*;")
parse = lambda seg: {m.group(1): m.group(2) for m in tok.finditer(seg)}
root = css[css.index(":root {"): css.index("\n}", css.index(":root {"))]
di = css.index('[data-theme-effective="dark"] {'); dark_blk = css[di: css.index("\n  }", di)]
L, D = parse(root), parse(dark_blk)
bi = css.index("--bar-fill: var(--pine-d)"); L.update(parse(css[bi - 50: bi + 400]))
D.update(parse(css[css.index('[data-theme-effective="dark"] .topbar'):][:800]))
L.update(parse(css[css.index(".aa-panel {"):][:400]))
D.update(parse(css[css.index('[data-theme-effective="dark"] .aa-panel'):][:900]))
def resolve(d):
    out = {}
    for k, v in d.items():
        m = re.fullmatch(r"var\((--[\w-]+)\)", v)
        if m: v = d[m.group(1)]
        out[k[2:].replace("-", "_")] = v
    return out
light, dark = resolve(L), resolve({**L, **D})
names = sorted(light); assert set(dark) == set(light)
js = lambda d: "{\n" + "\n".join(f"  {n}: {json.dumps(d[n])}," for n in names) + "\n}"
out = f'''/* ───────── Meyy design tokens, GENERATED from web/app/globals.css (Track D step 2, 2026-09-11) ─────────
 * One value per token per theme — the same {len(names)} colours the web paints with (`:root` + the
 * `[data-theme-effective="dark"]` block + the pine bar's --bar-* + the Ask Meyy section palette),
 * with the CSS aliases (--card-doc → --paper-2, --bar-fill → --pine-d) resolved per theme and the
 * kebab names snake-cased (--ink-soft → ink_soft). A token the dark block does not flip keeps its
 * light value, exactly as the cascade does on the web. Regenerate with
 * `python3 theme/gen-tokens.py` from mobile/ after a globals.css palette change; never hand-edit a
 * colour here — the web is the source. --shell-w / --shell-pad are web layout and not carried. */
export const light = {js(light)};

export const dark = {js(dark)};

export const TOKEN_NAMES = {json.dumps(names)};
'''
(here / "tokens.js").write_text(out)
print(len(names), "tokens → theme/tokens.js")
