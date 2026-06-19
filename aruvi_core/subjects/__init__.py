"""Subject registry — the engine asks here by name and gets a plugin; it never
knows what any individual subject is."""
from __future__ import annotations

from typing import Dict, List

from .base import Subject


class UnknownSubjectError(KeyError):
    pass


_REGISTRY: Dict[str, Subject] = {}


def register(subject: Subject) -> None:
    _REGISTRY[subject.name] = subject


def get(name: str) -> Subject:
    try:
        return _REGISTRY[name]
    except KeyError:
        raise UnknownSubjectError(
            f"No subject registered under {name!r}. Available: {available()}"
        )


def available() -> List[str]:
    return sorted(_REGISTRY)


__all__ = ["Subject", "register", "get", "available", "UnknownSubjectError"]
