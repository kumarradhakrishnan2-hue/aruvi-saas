"""API config. For now the data source is the prototype's mirror on local disk
(saved plans + mappings); env-overridable. This is the seam the cloud content store
replaces later — nothing else in the API hardcodes a path."""
import os

# Default to the prototype's runtime data dir; override with ARUVI_DATA_DIR.
_DEFAULT = "/Users/kumar_radhakrishnan/main/kumar/AI/Project Aruvi/app/mirror"
DATA_DIR = os.environ.get("ARUVI_DATA_DIR", _DEFAULT)
