# Meyy API — the FastAPI service + aruvi_core engine, as one container (Track A, 2026-09-09).
#
# WHAT GOES IN, BY DESIGN (CLOUD_DATA_MODEL.md §0.5): the runtime code and the
# MIGRATION UNIT'S read-only half — data/cloud/content/ (Bucket A-serve, 81 MB, tracked in
# git so Render's clone already has it). NOTHING ELSE. data/authoring/ (constitutions,
# summaries) is tracked in the same repo and is founder-secure; an image built with
# `COPY . .` would ship it to every host that ever pulls the image. So every COPY below
# names its path, and .dockerignore is the second lock on the same door.
#
# STATE (Bucket B) is NOT in the image. It lives on the persistent disk mounted at
# /var/aruvi (render.yaml) — ARUVI_STATE_DIR points there — so a redeploy keeps every
# teacher's rows. The three seller-side stores that sit outside the tenant shape
# (invoices/_series, support/_series, consents/_ledger) are seeded onto an EMPTY disk by
# deploy/entrypoint.sh so the invoice/support numbering continues rather than restarting.
#
# The served-plan cache under content/saved_plans/ is written at runtime into the
# container's own filesystem and is LOST on redeploy. That is fine: it is a
# reconstructible cache of ~ms deterministic serves (CLOUD_DATA_MODEL §1), warm-from-zero.

FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /app

# Dependencies first so code edits don't invalidate the pip layer.
COPY api/requirements.txt api/requirements.txt
RUN pip install --no-cache-dir -r api/requirements.txt

# Runtime code — the engine and the service, nothing else.
COPY aruvi_core/ aruvi_core/
COPY api/ api/

# Bucket A-serve: the shared read-only content the runtime reads.
COPY data/cloud/content/ data/cloud/content/

# Seed for the seller-side series (copied to the disk only when absent there).
COPY data/cloud/state/invoices/_series/ seed/state/invoices/_series/
COPY data/cloud/state/support/_series/  seed/state/support/_series/
COPY data/cloud/state/consents/_ledger/ seed/state/consents/_ledger/

COPY deploy/entrypoint.sh deploy/entrypoint.sh
RUN chmod +x deploy/entrypoint.sh

# Defaults a bare `docker run` can boot with; render.yaml overrides STATE_DIR onto the disk.
ENV ARUVI_DATA_DIR=/app/data/cloud/content \
    ARUVI_STATE_DIR=/var/aruvi/state \
    PORT=8000

EXPOSE 8000
CMD ["/app/deploy/entrypoint.sh"]
