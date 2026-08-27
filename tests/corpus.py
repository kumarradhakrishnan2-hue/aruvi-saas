"""One way for tests to reach the real plan library — edition-aware (§2.2, 2026-08-27).

Ten test files used to carry their own `glob(saved_plans/*/*/*.json)`. When the library
was foldered by edition year (saved_plans/{subject}/{grade}/{year}/…) every one of them
silently found ZERO plans — and a corpus test that finds nothing does not fail loudly,
it passes vacuously unless someone remembered to assert a non-empty corpus. Several had;
several had not.

So the depth of the library now lives in ONE place. The next edition bump — a second
year folder, or whatever replaces it — is a change here, not a sweep through the suite.

Both layouts are matched deliberately: a partner's checkout, an un-migrated clone or a
half-run migration should still exercise the corpus rather than quietly testing nothing.

    from corpus import plan_paths, grade_dir

    for fp in plan_paths():                       every plan, every subject, edition
    for fp in plan_paths("english", "ix"):        one subject·grade
    for fp in plan_paths(pattern="ch_*_canonical*.json"):   canonicals only
"""
import os
import re
from typing import List, Optional

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SAVED = os.path.join(os.environ.get("ARUVI_DATA_DIR",
                                    os.path.join(ROOT, "data", "cloud", "content")),
                     "saved_plans")

_YEAR_RE = re.compile(r"^\d{4}-\d{2}$")


def is_year_dir(name: str) -> bool:
    """"2026-27" — an edition folder, not a grade."""
    return bool(_YEAR_RE.match(str(name)))


def _ls(d: str) -> List[str]:
    try:
        return sorted(os.listdir(d))
    except OSError:
        return []


def editions(subject: str, grade: str) -> List[str]:
    """Edition years present for one subject·grade, newest first. Empty for a flat tree."""
    return sorted((e for e in _ls(os.path.join(SAVED, subject, grade))
                   if is_year_dir(e) and os.path.isdir(os.path.join(SAVED, subject, grade, e))),
                  reverse=True)


def grade_dir(subject: str, grade: str, year: Optional[str] = None) -> str:
    """The folder holding one subject·grade's plans.

    `year` picks an edition; without it the NEWEST is used, because a test asking for
    "the library" means the one a teacher would be served today. Falls back to the flat
    path when no edition folder exists.
    """
    base = os.path.join(SAVED, subject, grade)
    if year:
        return os.path.join(base, year)
    yrs = editions(subject, grade)
    return os.path.join(base, yrs[0]) if yrs else base


def plan_paths(subject: str = "*", grade: str = "*",
               pattern: str = "*.json", year: Optional[str] = None) -> List[str]:
    """Every plan file matching `pattern`, across both layouts. Sorted, deduplicated.

    `subject`/`grade` accept "*" (all). `year` restricts to one edition; without it
    EVERY edition is walked — a corpus check should see the whole library, including
    editions carried forward from previous years.
    """
    import glob as _glob
    out = []
    for depth in (
            os.path.join(SAVED, subject, grade, pattern),              # flat (legacy)
            os.path.join(SAVED, subject, grade, year or "*", pattern),  # editioned
    ):
        out.extend(_glob.glob(depth))
    # The flat pattern cannot match a directory, so nothing needs filtering out — but a
    # file could be reached by both globs when year == "*" and the tree is half-migrated.
    return sorted(set(out))


def split_path(fp: str) -> tuple:
    """(subject, grade, filename) for a plan path in EITHER layout.

    Tests group results by subject·grade and used to do this with a fixed negative
    index, which the extra folder level silently shifted by one — english/ix plans
    started reporting their subject as "ix". Read the shape instead of counting back.
    """
    parts = os.path.abspath(fp).split(os.sep)
    fn = parts[-1]
    rest = parts[:-1]
    if rest and is_year_dir(rest[-1]):
        rest = rest[:-1]
    return (rest[-2] if len(rest) >= 2 else "",
            rest[-1] if rest else "", fn)


def require_corpus(paths, what: str = "saved plans") -> None:
    """Fail loudly when the corpus is empty.

    A corpus test that finds nothing proves nothing, and the failure mode is silence.
    Call this rather than letting a zero-iteration loop report success.
    """
    assert paths, (
        f"no {what} found under {SAVED} — the library is missing or its layout "
        f"changed. If it was just foldered by edition year, fix tests/corpus.py, "
        f"not this test.")
