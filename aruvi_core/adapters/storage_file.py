"""File-based implementation of the Storage port — the content tree on local disk.

This is the adapter that HONOURS the seam declared in ports.py. Until 2026-08-29 the
Storage port was declared and bypassed: api/data.py read the certified lesson library
straight off the filesystem with open()/os.listdir/os.path.isdir, about twenty call
sites, so "swap the provider by writing one adapter" was true of every port except
this one. Nothing about that was broken — it is one machine, and a filesystem is a
perfectly good content store — but it meant the object-store migration was a refactor
wearing the costume of a config change.

WHAT THIS ADAPTER IS FOR: it is the LOCAL implementation, and deliberately the only
one. No vendor is named here or anywhere above it. An S3 / GCS / Supabase Storage
adapter is a second class implementing the same five methods, chosen in the same one
block of api/main.py, with no caller changing.

★ THE DESIGN RULE THIS ADAPTER EXISTS TO PROVE: a path is a KEY. Every method takes a
'/'-joined key relative to the content root, and this class is the only code in the
product allowed to turn one into an os.path. That is why `list_prefix` does not raise
on a missing prefix and why `exists` never tests for a directory — an object store has
no directories to find and nothing there to be missing, so a port that reported those
conditions would be encoding a filesystem assumption its successor cannot honour.

The three read helpers (get_json, list_json, get_text) are conveniences on top of
get_bytes, not extra port surface: every runtime read in api/data.py is "fetch this
key and JSON-parse it" or "fetch every .json under this prefix and parse each", and
writing that twice per call site is how a decoding inconsistency gets in.
"""
from __future__ import annotations

import json
import os
from typing import Any, Dict, List, Optional

from aruvi_core.ports import Storage


class LocalStorage(Storage):
    """Content store backed by a directory tree on the local filesystem."""

    def __init__(self, root: str):
        """
        Args:
            root: Base directory of the content tree (i.e. ARUVI_DATA_DIR /
                  config.DATA_DIR). Every key is resolved beneath it.
        """
        self.root = str(root)

    # ── key handling ──────────────────────────────────────────────────────────
    def _abs(self, path: str) -> str:
        """Resolve a '/'-joined key to an absolute filesystem path beneath the root.

        Refuses to escape the root. The content tree is not user-writable and today's
        keys are all built from validated subject/grade values, so this is defence in
        depth rather than a live threat — but a Storage port whose keys could walk
        upwards would hand that same weakness to every future adapter, and an object
        store's flat keyspace has no natural '..' to inherit the protection from.
        """
        rel = str(path).strip().strip("/")
        full = os.path.normpath(os.path.join(self.root, *rel.split("/"))) if rel \
            else os.path.normpath(self.root)
        root = os.path.normpath(self.root)
        if full != root and not full.startswith(root + os.sep):
            raise ValueError(f"path escapes the content root: {path!r}")
        return full

    # ── the port ──────────────────────────────────────────────────────────────
    def get_bytes(self, path: str) -> bytes:
        with open(self._abs(path), "rb") as f:
            return f.read()

    def put_bytes(self, path: str, data: bytes,
                  content_type: str = "application/octet-stream") -> str:
        full = self._abs(path)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "wb") as f:
            f.write(data)
        return path

    def url_for(self, path: str) -> str:
        """Local files have no URL; the absolute path is the honest answer. An object
        store returns a real (possibly signed) URL here. Nothing in the runtime calls
        this yet — it is the export/download path's seam, not the library's."""
        return "file://" + self._abs(path)

    def exists(self, path: str) -> bool:
        """True if an OBJECT is stored at this key. A directory is not an object, so
        a folder path answers False — matching what an object store would say."""
        return os.path.isfile(self._abs(path))

    def version_token(self, path: str) -> Optional[str]:
        """The object's modification time as a string, or None if absent.

        Returned as a STRING, not the float os.path.getmtime gives, so no caller can
        start doing arithmetic on it — an S3 adapter returns an ETag here and the
        comparison must stay an equality test. See the port's contract."""
        try:
            return str(os.path.getmtime(self._abs(path)))
        except (OSError, ValueError):
            return None

    def list_prefix(self, prefix: str, suffix: str = "") -> List[str]:
        """Sorted keys directly under `prefix`, as root-relative paths.

        Missing prefix -> empty list, never an exception (see the class docstring).
        Sorting is contractual: the library is read in name order and served in the
        order read, so an unsorted listing would quietly reorder a teacher's plan."""
        base = self._abs(prefix)
        if not os.path.isdir(base):
            return []
        pre = str(prefix).strip().strip("/")
        out = []
        for name in os.listdir(base):
            if suffix and not name.endswith(suffix):
                continue
            if os.path.isfile(os.path.join(base, name)):
                out.append(f"{pre}/{name}" if pre else name)
        return sorted(out)

    def list_subprefixes(self, prefix: str) -> List[str]:
        """Sorted next-segment names under `prefix` (S3's CommonPrefixes). Bare
        segments, not full paths — see the port's contract."""
        base = self._abs(prefix)
        if not os.path.isdir(base):
            return []
        return sorted(name for name in os.listdir(base)
                      if os.path.isdir(os.path.join(base, name)))

    # ── local-only escape hatch ───────────────────────────────────────────────
    def local_path(self, path: str) -> str:
        """The absolute filesystem path for a key — LOCAL ADAPTER ONLY.

        Not on the Storage port, and deliberately not: an object store has no such
        thing to return. It exists for tooling that genuinely needs a real file (the
        authoring pipeline, migration scripts, a test asserting where a library
        landed), and calling it is a declaration that the caller cannot be swapped.

        If a RUNTIME read path ever calls this, the seam is bypassed again — that is
        precisely the regression tests/test_storage_seam.py greps for."""
        return self._abs(path)

    # ── read conveniences (composed from get_bytes; not port surface) ─────────
    def get_json(self, path: str) -> Optional[Any]:
        """Parse the object at `path` as JSON, or None if there is nothing there.

        None-on-missing matches what every call site in api/data.py already did with
        its `if os.path.isfile(p)` guard, so routing through the port changed no
        behaviour. A key that exists but holds malformed JSON still raises — that is a
        corrupt library, which should be loud."""
        try:
            raw = self.get_bytes(path)
        except (FileNotFoundError, NotADirectoryError, IsADirectoryError, ValueError):
            return None
        return json.loads(raw.decode("utf-8"))

    def get_text(self, path: str, encoding: str = "utf-8") -> Optional[str]:
        """The object at `path` decoded as text, or None if absent."""
        try:
            return self.get_bytes(path).decode(encoding)
        except (FileNotFoundError, NotADirectoryError, IsADirectoryError, ValueError):
            return None

    def list_json(self, prefix: str) -> List[Dict[str, Any]]:
        """Every .json object directly under `prefix`, parsed, in sorted key order.

        Unreadable or malformed members are SKIPPED rather than raising, because this
        backs the library listings (a chapter's canonicals, a grade's mappings) where
        one bad file must not blank the whole shelf — the behaviour the try/except
        around each json.load in api/data.py already had."""
        out: List[Dict[str, Any]] = []
        for key in self.list_prefix(prefix, ".json"):
            try:
                doc = self.get_json(key)
            except Exception:
                continue
            if doc is not None:
                out.append(doc)
        return out
