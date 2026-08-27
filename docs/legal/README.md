# Legal texts — they live in the content store, not here

The user agreement moved on **2026-08-27**, when it stopped being a draft to review and
became something the app serves:

    data/cloud/content/legal/consent_and_disclaimer_v0.1.md

That is its one and only home. Editing rules:

* **Publishing a new version means adding a new FILE** — `..._v0.2.md` beside the old
  one — never editing text a teacher has already ticked. Her consent record names the
  version she saw, so that file must stay readable to be shown back to her. The runtime
  reads the version out of the filename (`api/legal.py`) and treats the highest as
  current; publishing v0.2 makes every teacher re-tick all six, which is what §J of the
  agreement promises.
* **The parser expects the document's shape** — five `### ☐ N. Title` blocks each ending
  on `**I understand and agree.**`, then the full agreement, then
  `## Final acknowledgement`. Break it and `GET /legal/consent` returns 503 rather than
  serving a consent screen with a tick missing. `tests/test_consent.py` guards this.
* **`> blockquote` front matter is never shown to a teacher** — it is the note to the
  lawyer, and the parser drops it. Put review notes there freely.
* **Three places state the retention of consent records and must agree:** §G of the
  document, `_KEPT` in `aruvi_core/adapters/data_rights_service_file.py`, and the
  placement of the ledger in `aruvi_core/adapters/consent_repository_file.py`.

It sits under `data/cloud/content/` (Bucket A-serve, CLAUDE.md §7) because the runtime
serves it to every teacher before she pays — so it has to travel inside the migration
unit. It is shared, read-only, versioned content, which is exactly what Bucket A is for.
