"""Grade -> stage derivation. THE single source of this mapping.

Stage is never a separate input — it is always derived from grade here, so the two can
never drift out of sync. Every consumer calls stage_for(grade); nobody re-implements the
`if grade in (...)` test locally (per the prototype's cascade-bug lesson).
"""
from __future__ import annotations

_STAGE = {
    "iii": "preparatory", "iv": "preparatory", "v": "preparatory",
    "vi": "middle", "vii": "middle", "viii": "middle",
    "ix": "secondary", "x": "secondary",
}


class UnknownGradeError(ValueError):
    pass


def stage_for(grade: str) -> str:
    """'vii' -> 'middle', 'ix' -> 'secondary', etc. Tolerates 'Grade VII' / casing."""
    g = str(grade).strip().lower().replace("grade", "").strip()
    if g in _STAGE:
        return _STAGE[g]
    raise UnknownGradeError(f"Cannot derive stage for grade {grade!r}.")
