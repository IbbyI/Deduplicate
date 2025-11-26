from pathlib import Path
from rich.progress import Progress

from core.log import log
from ui.verbose import verbose
from ui.display import *

progress = Progress()


@verbose(lambda groups: f"Unique Files: {len(groups or [])}")
def find_duplicates(
    start_path: Path,
    ignore_path: Path | None,
    hash_func: any,
) -> list[list[Path]] | None:
    """
    Find Duplicate Files in Given Path.
    Args:
        start_path (Path): Path to Search for Duplicate Files.
    Returns:
        list[list[Path]]: Nested List of Path objects of duplicate files found.
        None: If no duplicate files are found, returns None.
    """
    log(level="info", message=f"Scanning Path '{start_path}' For Duplicate Files...")
    info(f"Scanning Path '{start_path}' For Duplicate Files...")
    if ignore_path:
        log(level="info", message=f"Ignoring Path: {str(ignore_path)}")
        info(f"Ignoring Path: {str(ignore_path)}")
    try:
        progress.start()
        hashmap = {}
        hash_task = progress.add_task("[light_sky_blue1]Hashing Files...", total=None)
        for file in Path(start_path).rglob("*"):
            if file.is_file():
                if ignore_path and file.is_relative_to(ignore_path):
                    progress.update(hash_task)
                    continue
                hashed_file = hash_func(file)
                hashmap.setdefault(hashed_file, []).append(file)
        duplicate_results = [value for value in hashmap.values() if len(value) > 1]
        if not duplicate_results:
            success(f"No Duplicates Found in Path: {start_path}")
            info("Terminating Program...")
            log(
                level="info",
                message=f"✔ No Duplicates Found in Path: {start_path}\nTerminating Program...",
            )
            return
        for duplicates in duplicate_results:
            paths = [str(p) for p in duplicates]
            log(level="info", message=f"{' , '.join(paths)} are identical.")
        return duplicate_results
    finally:
        progress.stop()
