"""The Storage seam is HONOURED — the runtime reads content only through the port.

Why this test exists, and why it is a grep rather than a behavioural test: the seam
was declared in ports.py from the beginning and bypassed for months, and nothing
failed. That is the failure mode a normal test cannot catch — going around a port
does not break anything, it just quietly removes the property the port was built to
provide, until the day someone tries to swap the provider and discovers the adapter
was never the only way in.

So this asserts the INVARIANT directly: no filesystem call against the content tree
survives in the runtime outside the local adapter. Add a convenient open() to
api/data.py and this goes red immediately, which is the only moment the cost is
cheap to pay.

Run: python3 tests/test_storage_seam.py
"""
import ast
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from aruvi_core.adapters.storage_file import LocalStorage   # noqa: E402
from aruvi_core.ports import Storage                        # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# The runtime modules that read content. The adapter itself is excluded by definition —
# it is the one place allowed to touch a disk.
RUNTIME_FILES = ["api/data.py", "api/legal.py"]

# api/data.py's append_token_log writes the founder's cost notebook under runtime_data/,
# which is not content, is never read back, and cannot be appended to in an object
# store. Declared here so the exception stays visible instead of being quietly grepped
# around — if the list grows, that is a decision someone must justify.
ALLOWED_FS_FUNCTIONS = {"append_token_log"}

BANNED_CALLS = {"open"}
BANNED_ATTRS = {"listdir", "makedirs", "isdir", "isfile", "getmtime", "exists",
                "scandir", "walk", "remove", "rmdir"}

failures = []


def check(label, cond, detail=""):
    if cond:
        print(f"PASS  {label}")
    else:
        print(f"FAIL  {label}  <- {detail}")
        failures.append(label)


# ── 1. the invariant ──────────────────────────────────────────────────────────
def _enclosing_funcs(tree):
    """Map every node to the name of the function it sits inside."""
    owner = {}

    def walk(node, fname):
        for child in ast.iter_child_nodes(node):
            nm = child.name if isinstance(child, (ast.FunctionDef,
                                                  ast.AsyncFunctionDef)) else fname
            owner[child] = nm
            walk(child, nm)
    walk(tree, None)
    return owner


def test_no_runtime_filesystem_call_against_content():
    """No open()/os.listdir/os.path.* in the content-reading runtime modules."""
    for rel in RUNTIME_FILES:
        path = os.path.join(ROOT, rel)
        tree = ast.parse(open(path, encoding="utf-8").read())
        owner = _enclosing_funcs(tree)
        offenders = []
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call):
                continue
            if owner.get(node) in ALLOWED_FS_FUNCTIONS:
                continue
            f = node.func
            if isinstance(f, ast.Name) and f.id in BANNED_CALLS:
                offenders.append(f"{rel}:{node.lineno} {f.id}()")
            elif isinstance(f, ast.Attribute) and f.attr in BANNED_ATTRS:
                base = f.value
                # os.listdir / os.path.isdir — both read as an `os` lineage
                src = ast.dump(base)
                if "'os'" in src or "'path'" in src:
                    offenders.append(f"{rel}:{node.lineno} os…{f.attr}()")
        check(f"{rel} makes no direct filesystem call",
              not offenders, "; ".join(offenders[:4]))


def test_data_module_holds_no_os_path_joins():
    """A path built with os.path.join in api/data.py means a key became a path again."""
    src = open(os.path.join(ROOT, "api/data.py"), encoding="utf-8").read()
    tree = ast.parse(src)
    owner = _enclosing_funcs(tree)
    bad = [f"line {n.lineno}" for n in ast.walk(tree)
           if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute)
           and n.func.attr == "join" and "'os'" in ast.dump(n.func.value)
           and owner.get(n) not in ALLOWED_FS_FUNCTIONS]
    check("api/data.py builds no os.path.join outside the allowed exception",
          not bad, "; ".join(bad))


# ── 2. the adapter honours the contract ───────────────────────────────────────
def test_adapter_satisfies_the_port():
    s = LocalStorage(tempfile.gettempdir())
    check("LocalStorage satisfies the Storage protocol", isinstance(s, Storage))
    for m in ("get_bytes", "put_bytes", "url_for", "exists",
              "version_token", "list_prefix", "list_subprefixes"):
        check(f"port method {m} is implemented", callable(getattr(s, m, None)))


def test_missing_prefix_is_empty_not_an_error():
    """An object store has nothing there to be missing — see the port's contract."""
    with tempfile.TemporaryDirectory() as tmp:
        s = LocalStorage(tmp)
        check("a missing prefix lists empty", s.list_prefix("nowhere") == [])
        check("a missing sub-prefix lists empty", s.list_subprefixes("nowhere") == [])
        check("a missing key does not exist", s.exists("nowhere.json") is False)
        check("a missing key has no version token",
              s.version_token("nowhere.json") is None)
        check("a missing key reads as None", s.get_json("nowhere.json") is None)


def test_listing_is_sorted_and_non_recursive():
    with tempfile.TemporaryDirectory() as tmp:
        s = LocalStorage(tmp)
        for name in ("c.json", "a.json", "b.json", "d.txt"):
            s.put_bytes(f"lib/{name}", b"{}")
        s.put_bytes("lib/deeper/e.json", b"{}")
        keys = s.list_prefix("lib", ".json")
        check("listing is sorted",
              keys == ["lib/a.json", "lib/b.json", "lib/c.json"], str(keys))
        check("listing does not recurse",
              all("deeper" not in k for k in keys), str(keys))
        check("suffix filter excludes other types",
              "lib/d.txt" not in keys)
        check("sub-prefixes are bare segments",
              s.list_subprefixes("lib") == ["deeper"], str(s.list_subprefixes("lib")))


def test_a_directory_is_not_an_object():
    """exists() is never a directory test — an object store has no directories."""
    with tempfile.TemporaryDirectory() as tmp:
        s = LocalStorage(tmp)
        s.put_bytes("lib/a.json", b"{}")
        check("a stored key exists", s.exists("lib/a.json") is True)
        check("a prefix is not an object", s.exists("lib") is False)


def test_version_token_changes_when_the_object_does():
    with tempfile.TemporaryDirectory() as tmp:
        s = LocalStorage(tmp)
        s.put_bytes("a.json", b'{"v":1}')
        t1 = s.version_token("a.json")
        os.utime(s.local_path("a.json"), (0, 0))     # force a distinct mtime
        t2 = s.version_token("a.json")
        check("the version token moves with the object", t1 != t2, f"{t1} == {t2}")
        check("the version token is a string, not a number",
              isinstance(t1, str), type(t1).__name__)


def test_keys_cannot_escape_the_root():
    """A key either resolves INSIDE the root or is refused — never both, never neither.

    Asserting on the resolved location rather than on which exception came back: a
    FileNotFoundError proves nothing on its own (it is also what a perfectly safe
    missing key raises), and an absolute-looking key like "/etc/passwd" is not an
    attack to refuse but a key to normalise — an object store has no root directory
    for a leading slash to mean, so it is stripped and the key lands under the content
    root like any other."""
    with tempfile.TemporaryDirectory() as tmp:
        root = os.path.realpath(tmp)
        s = LocalStorage(tmp)
        for evil in ("../outside.json", "a/../../outside.json", "/etc/passwd",
                     "a/../b.json", "//etc/passwd"):
            try:
                resolved = os.path.realpath(s.local_path(evil))
                inside = resolved == root or resolved.startswith(root + os.sep)
            except ValueError:
                inside = True       # refused outright, which is also correct
            check(f"key {evil!r} stays inside the content root", inside,
                  f"resolved outside {root}")


# ── 3. the swap the port exists to make possible ──────────────────────────────
class DictStorage:
    """A store with no filesystem at all. If the runtime can read a library out of
    this, the seam is real — that is the whole claim the provider sheet makes."""

    def __init__(self, objects):
        self.objects = dict(objects)

    def get_bytes(self, path):
        if path not in self.objects:
            raise FileNotFoundError(path)
        return self.objects[path]

    def put_bytes(self, path, data, content_type="application/octet-stream"):
        self.objects[path] = data
        return path

    def url_for(self, path):
        return f"memory://{path}"

    def exists(self, path):
        return path in self.objects

    def version_token(self, path):
        return str(len(self.objects[path])) if path in self.objects else None

    def list_prefix(self, prefix, suffix=""):
        p = prefix.strip("/") + "/"
        return sorted(k for k in self.objects
                      if k.startswith(p) and "/" not in k[len(p):]
                      and (not suffix or k.endswith(suffix)))

    def list_subprefixes(self, prefix):
        p = prefix.strip("/") + "/"
        return sorted({k[len(p):].split("/")[0] for k in self.objects
                       if k.startswith(p) and "/" in k[len(p):]})

    def get_json(self, path):
        import json
        if path not in self.objects:
            return None
        return json.loads(self.objects[path].decode("utf-8"))

    def get_text(self, path, encoding="utf-8"):
        if path not in self.objects:
            return None
        return self.objects[path].decode(encoding)

    def list_json(self, prefix):
        return [self.get_json(k) for k in self.list_prefix(prefix, ".json")]


def test_the_runtime_reads_from_a_non_filesystem_store():
    """The claim under test: swapping the provider changes no caller.

    This is the test that would have been impossible to write yesterday. It installs
    a dict-backed store — no disk, no paths, keys only — and asks api/data.py the
    ordinary questions the API asks it. If any read path still reached for the
    filesystem, it would fail here rather than in production.
    """
    import json
    from api import data

    plan = {"chapter_number": 4, "chapter_title": "In Memory",
            "plan_status": "canonical", "saved_at": "2026-01-01T00:00:00",
            "genon": {"academic_year": "2026-27"}}
    store = DictStorage({
        "saved_plans/science/vii/2026-27/ch_04_canonical.json":
            json.dumps(plan).encode(),
        "chapters/science/vii/mappings/ch_04_mapping.json":
            json.dumps({"chapter_number": 4, "title": "In Memory"}).encode(),
        "allocation_norms/ncf_period_norms.json":
            json.dumps({"subjects": {"science": {"middle": 120}}}).encode(),
    })

    real_dir = data.DATA_DIR
    try:
        data.set_storage(store)

        check("list_grades reads from the fake store",
              data.list_grades("science") == ["vii"], str(data.list_grades("science")))
        check("the edition prefix resolves without a filesystem",
              data.lp_library_prefix("science", "vii")
              == "saved_plans/science/vii/2026-27",
              data.lp_library_prefix("science", "vii"))
        check("editions list from the fake store",
              data.lp_library_years("science", "vii") == ["2026-27"])
        check("the canonical loads",
              (data.load_genon_canonical("science", "vii", 4) or {})
              .get("chapter_title") == "In Memory")
        check("chapters enumerate", data.genon_chapters("science", "vii") == [4])
        check("mappings load", len(data.load_mappings("science", "vii")) == 1)
        check("NCF norms load", data.ncf_total_periods("science", "middle") == 120)
        listed = data.list_saved_plans("science", "vii")
        check("saved plans list with their filenames",
              [p["filename"] for p in listed] == ["ch_04_canonical.json"], str(listed))
        check("a named plan loads back",
              (data.load_saved_plan("science", "vii", "ch_04_canonical.json") or {})
              .get("chapter_number") == 4)

        # a WRITE lands in the store, not on any disk
        data.save_generated_plan("science", "vii", {"chapter_number": 9},
                                 filename="ch_09_derived.json")
        check("a generated plan is written through the port",
              "saved_plans/science/vii/2026-27/ch_09_derived.json" in store.objects)
    finally:
        data._storage_explicit = False
        data.DATA_DIR = real_dir
        data.set_storage(LocalStorage(real_dir))
        data._storage_explicit = False


def test_an_explicit_store_is_not_silently_replaced():
    from api import data
    real_dir = data.DATA_DIR
    try:
        store = DictStorage({})
        data.set_storage(store)
        data.DATA_DIR = "/tmp/somewhere-else"
        check("an explicitly-set store survives a DATA_DIR change",
              data.storage() is store)
    finally:
        data._storage_explicit = False
        data.DATA_DIR = real_dir
        data.set_storage(LocalStorage(real_dir))
        data._storage_explicit = False


if __name__ == "__main__":
    test_no_runtime_filesystem_call_against_content()
    test_data_module_holds_no_os_path_joins()
    test_adapter_satisfies_the_port()
    test_missing_prefix_is_empty_not_an_error()
    test_listing_is_sorted_and_non_recursive()
    test_a_directory_is_not_an_object()
    test_version_token_changes_when_the_object_does()
    test_keys_cannot_escape_the_root()
    test_the_runtime_reads_from_a_non_filesystem_store()
    test_an_explicit_store_is_not_silently_replaced()

    print()
    if failures:
        print(f"FAILURES ({len(failures)}): " + "; ".join(failures))
        sys.exit(1)
    print("✓ the Storage seam is honoured — content reads go through the port, "
          "and the runtime works against a store with no filesystem at all")
