from pathlib import Path
from rich import print as rprint
from rich.prompt import Prompt
from rich.progress import Progress

from utils.log import log
from utils.verbose import verbose

progress = Progress()


@verbose("Scanning For Duplicates")
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
    rprint(f"[light_sky_blue1]Scanning Path '{start_path}' For Duplicate Files...[/]")
    if ignore_path:
        log(level="info", message=f"Ignoring Path: {str(ignore_path)}")
        rprint(f"[blue]Ignoring Path: {str(ignore_path)}[/]")
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
            rprint(
                f"✅ [bold underline green]No Duplicates Found in Path: {start_path}[/]\n[blue]Terminating Program...[/]"
            )
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