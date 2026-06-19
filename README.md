# Aruvi SaaS

Greenfield rebuild of Aruvi as a cloud-hosted, multi-tenant SaaS. The prototype
(`../Project Aruvi`, frozen at git tag `prototype-final`) is the proven specification and
data source; this repo lifts its durable IP into a clean architecture.

## Design rules (from the architecture plan)

1. **Lift, don't drag** — reuse the proven generation logic; discard the Streamlit monolith.
2. **Subjects are plugins, not conditionals** — each subject is a self-contained package
   implementing one `Subject` interface; the engine never branches on subject.
3. **One renderer, many subjects** — subjects normalize to a single, structure-PRESERVING
   `ViewModel`; one shared renderer produces HTML / PDF / DOCX / mobile. Curriculum changes
   touch one subject; styling changes touch one renderer.
4. **No vendor lock-in — ports & adapters** — core logic depends only on the Protocols in
   `aruvi_core/ports.py`; each vendor is a thin adapter at the edge.
5. **Validation-first** — `aruvi_core → API → Auth → DB → Web` is the spine; pgvector, heavy
   orchestration, and mobile are deferred until paying traction.

## Layout (Phase 0 — the bones)

```
aruvi_core/
  view_model.py        # canonical, structure-preserving contract (Group/Period/Assessment*)
  subjects/
    base.py            # the Subject Protocol (build prompts, validate, to_view)
    __init__.py        # registry: register / get / available
  ports.py             # LLMClient, OutputCache, Storage, Repository, JobQueue, Auth, Billing
  engine.py            # tiny subject-agnostic orchestrator: prompt -> LLM -> validate -> view
tests/
  test_view_model.py   # proves all 5 prototype structures are preserved + JSON-serializable
```

## Run the smoke test

```bash
python3 tests/test_view_model.py
```

## Status / next

- **Done (Phase 0 bones):** view model, Subject interface + registry, adapter ports, engine,
  structure-preservation test.
- **Next:** port **one real subject end-to-end** (lift its prompt assembly + `to_view_model`
  from the prototype), with the prototype's output as the parity fixture; then the Anthropic
  `LLMClient` adapter; then FastAPI + async generation (Phase 1).
