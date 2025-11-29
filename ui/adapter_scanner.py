from pathlib import Path
from rich.progress import Progress

from ui.display import info, warn
from ui.verbose import verbose

from core.log import log
from core.scanner import find_duplicates

progress = Progress()


@verbose(lambda args, groups: f"Unique Files Found: {len(groups or [])}")
def find_duplicates_ui(start_path: str, ignore_path: str, hash_func):
    """
    Handles UI For Scanning Directory Logic.
    Args:
        s
    """
    info(f"Scanning...")
    progress.start()
    try:
        find_dupes_task = progress.add_task(
            "[purple]Searching for Duplicates...", total=None
        )
        log(level="info", message=f"Searching for Duplicates in {start_path}")

        groups = find_duplicates(start_path, ignore_path, hash_func)
        log(level="info", message=f"Unique Files Found: {len(groups)}")
    except RuntimeError as e:
        warn(str(e))
        log(level="error", message=str(e))
    finally:
        progress.stop()
        return groups
