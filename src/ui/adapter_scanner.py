from pathlib import Path
from rich.progress import Progress
from typing import Callable

from ui.display import info, error
from ui.verbose import verbose

from core.log import log
from core.scanner import find_duplicates

progress = Progress()


@verbose(lambda args, groups: f"Unique Files Found: {len(groups or [])}")
def find_duplicates_ui(
    start_path: Path, ignore_path: Path | None, hash_func: Callable[[Path], str]
) -> list[list[Path]] | None:
    """
    Handles UI For Scanning Directory Logic.
    Args:
        start_path (Path): Path to Search for Duplicate Files.
        ignore_path (Path | None): Path to Ignore Searching (Optional Flag)
        hash_func (Callable[[Path], str]):
            A hashing function that takes a Path and returns a SHA-256 digest string
    Returns:
        list[list[Path]]: Nested List of Path objects of duplicate files found.
        None: If no duplicate files are found, returns None.
    """
    info(f"Scanning Path: {start_path}")
    progress.start()
    try:
        progress.add_task("[purple]Searching for Duplicates...", total=None)
        log(level="info", message=f"Searching for Duplicates in {start_path}")

        groups: list[list[Path]] | None = find_duplicates(
            start_path, ignore_path, hash_func
        )

        number_of_unique = len(groups) if groups is not None else 0
        log(level="info", message=f"Unique Files Found: {number_of_unique}")
        return groups
    except Exception as e:
        error(str(e))
        log(level="error", message=str(e))
    finally:
        progress.stop()
