"""Migrate data/ to the cloud/local physical layout (CLOUD_DATA_MODEL.md §0.5, 2026-08-23).

Moves, never copies. Idempotent and re-runnable: a move whose source is gone and whose
destination exists is silently considered done. Run from anywhere:

    python3 aruvi-scripts/migrate_cloud_layout.py

Target layout:
  data/cloud/content/   allocation_norms, saved_plans, framework, chapters/**/mappings
  data/cloud/state/     accounts, academic_years, readiness, allocations,
                        section_state, prepared_plans, plan_archive, plan_notes
  data/authoring/       constitutions, chapters/**/summaries
  data/testing/         stays where it is
"""
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
CONTENT = DATA / "content"
CLOUD_CONTENT = DATA / "cloud" / "content"
CLOUD_STATE = DATA / "cloud" / "state"
AUTHORING = DATA / "authoring"

STATE_KINDS = ["accounts", "academic_years", "readiness", "allocations",
               "section_state", "prepared_plans", "plan_archive", "plan_notes"]
CONTENT_TO_CLOUD = ["allocation_norms", "saved_plans", "framework"]
CONTENT_TO_AUTHORING = ["constitutions"]


def move(src: Path, dst: Path, log: list) -> None:
    """Move src -> dst. Done already (src gone, dst there) is fine; both present is an error
    (this script never merges — resolve by hand so nothing is silently clobbered)."""
    if not src.exists():
        if dst.exists():
            log.append(f"  = already migrated: {dst.relative_to(ROOT)}")
        return
    if dst.exists():
        sys.exit(f"REFUSING: both {src.relative_to(ROOT)} and {dst.relative_to(ROOT)} exist "
                 f"— merge by hand, then re-run.")
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.move(str(src), str(dst))
    log.append(f"  > moved {src.relative_to(ROOT)} -> {dst.relative_to(ROOT)}")


def main() -> None:
    log: list = []

    # Bucket B state -> data/cloud/state/
    for kind in STATE_KINDS:
        move(DATA / kind, CLOUD_STATE / kind, log)

    # Whole-tree content moves -> data/cloud/content/
    for name in CONTENT_TO_CLOUD:
        move(CONTENT / name, CLOUD_CONTENT / name, log)

    # Authoring content -> data/authoring/
    for name in CONTENT_TO_AUTHORING:
        move(CONTENT / name, AUTHORING / name, log)

    # chapters/{subject}/{grade}/{mappings -> cloud, summaries -> authoring}
    chapters = CONTENT / "chapters"
    if chapters.is_dir():
        for subject in sorted(p for p in chapters.iterdir() if p.is_dir()):
            for grade in sorted(p for p in subject.iterdir() if p.is_dir()):
                rel = Path("chapters") / subject.name / grade.name
                move(grade / "mappings", CLOUD_CONTENT / rel / "mappings", log)
                move(grade / "summaries", AUTHORING / rel / "summaries", log)

    # Sweep junk, then remove the emptied data/content tree; warn on real leftovers.
    if CONTENT.exists():
        for junk in CONTENT.rglob(".DS_Store"):
            try:
                junk.unlink()
            except OSError:
                pass  # sandboxed runs may not be allowed to delete; harmless
        leftovers = [p for p in CONTENT.rglob("*")
                     if p.is_file() and p.name != ".DS_Store"]
        if leftovers:
            print("WARNING — unexpected files left under data/content/ (not moved):")
            for p in leftovers:
                print(f"  ? {p.relative_to(ROOT)}")
        else:
            shutil.rmtree(CONTENT, ignore_errors=True)
            if CONTENT.exists():
                print("NOTE: emptied data/content/ husk could not be deleted here — "
                      "remove it by hand (only .DS_Store remains).")
            else:
                log.append("  - removed emptied data/content/")

    print("\n".join(log) if log else "Nothing to do.")
    print("Done. Layout per CLOUD_DATA_MODEL.md §0.5.")


if __name__ == "__main__":
    main()
