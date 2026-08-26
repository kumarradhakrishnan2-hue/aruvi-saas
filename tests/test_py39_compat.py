"""Guard: every runtime module must import cleanly on Python 3.9.

WHY THIS EXISTS (2026-08-26). `erasure_log_file.py` was written with a PEP 604 annotation
(`Dict[str, int] | None`) and shipped green: the dev sandbox runs Python 3.10, where that
is legal, while **the founder's Mac runs 3.9**, where it is a TypeError raised at import —
the server refused to boot. Unit tests could not catch it because they run on the same
3.10 interpreter that accepts it.

The hazard is specific and repeatable: PEP 604 unions in annotations are EVALUATED at
class/function definition time on 3.9. `from __future__ import annotations` makes them
strings and defers evaluation, so a module carrying that import is safe; one without it is
not. This test enforces exactly that rule, statically, on any interpreter.

It also parses every module against the 3.9 grammar, which catches match statements and
other newer syntax.

Run standalone:  python3 tests/test_py39_compat.py     (also pytest-compatible)
"""
from __future__ import annotations

import ast
import os
import re
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Runtime trees only. Authoring/one-off scripts may use whatever the founder's shell runs.
_RUNTIME_DIRS = ("api", "aruvi_core")

# A `|` sitting in an annotation or return position, e.g. `x: int | None` / `-> str | None`.
_PEP604 = re.compile(r"(->\s*[^:=#\n]*\|)|(:\s*[A-Za-z_][A-Za-z0-9_\[\], .\"']*\s*\|)")


def _runtime_files():
    for d in _RUNTIME_DIRS:
        for root, _dirs, files in os.walk(os.path.join(_ROOT, d)):
            if "__pycache__" in root or "_to_delete" in root:
                continue
            for f in sorted(files):
                if f.endswith(".py"):
                    yield os.path.join(root, f)


def _strip_strings_and_comments(src: str) -> str:
    """Blank out docstrings, string literals and comments so prose like
    `{type: table|prose}` in a docstring is never mistaken for an annotation."""
    out = []
    try:
        tree = ast.parse(src)
    except SyntaxError:
        return src
    spans = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            if getattr(node, "end_lineno", None):
                spans.append((node.lineno, node.end_lineno))
    blanked = set()
    for a, b in spans:
        blanked.update(range(a, b + 1))
    for i, line in enumerate(src.splitlines(), start=1):
        if i in blanked:
            out.append("")
        else:
            out.append(line.split("#", 1)[0])
    return "\n".join(out)


def test_no_pep604_without_future_import():
    """PEP 604 unions are fine ONLY in modules that defer annotation evaluation."""
    offenders = []
    for path in _runtime_files():
        with open(path, "r") as f:
            src = f.read()
        if "from __future__ import annotations" in src:
            continue                      # deferred → safe on 3.9
        code = _strip_strings_and_comments(src)
        for lineno, line in enumerate(code.splitlines(), start=1):
            if _PEP604.search(line):
                rel = os.path.relpath(path, _ROOT)
                offenders.append(f"{rel}:{lineno}: {line.strip()}")
    assert not offenders, (
        "PEP 604 union(s) in a module that does not defer annotations — this is a "
        "TypeError at import on Python 3.9 (the founder's Mac):\n  "
        + "\n  ".join(offenders)
        + "\nFix: use Optional[...] / Union[...], or add "
          "`from __future__ import annotations` at the top of the module."
    )
    print("✓ No 3.9-breaking PEP 604 annotations in api/ or aruvi_core/")


def test_everything_parses_under_39_grammar():
    """Catches match statements and any other post-3.9 syntax."""
    bad = []
    for path in _runtime_files():
        with open(path, "r") as f:
            src = f.read()
        try:
            ast.parse(src, feature_version=(3, 9))
        except SyntaxError as e:
            bad.append(f"{os.path.relpath(path, _ROOT)}:{e.lineno}: {e.msg}")
    assert not bad, "post-3.9 syntax in runtime code:\n  " + "\n  ".join(bad)
    print("✓ All runtime modules parse under the Python 3.9 grammar")


if __name__ == "__main__":
    test_no_pep604_without_future_import()
    test_everything_parses_under_39_grammar()
    print("\n✅ All Python 3.9 compatibility checks passed!")
