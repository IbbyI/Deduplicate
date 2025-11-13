import shutil
from os import remove
from pathlib import Path
from rich import print as rprint
from rich.prompt import Prompt
from rich.progress import Progress

from utils.log import log
from utils.hash import hash_file

progress = Progress()


def find_duplicates(
    start_path: Path, ignore_path: Path | None
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
                hashed_file = hash_file(file)
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


def compare_files(
    duplicate_results: list[list[Path]],
) -> list[Path]:
    """
    Compare Duplicate Files and Select Newer One.
    Args:
        duplicate_results (list): List of nested arrays containing paths of duplicate files.
    Returns:
        list[Path]: List of duplicate files, with the oldest file removed from each group.
    """
    rprint("✅ [bold blue]Duplicate Files Found:[/]")
    result = []
    try:
        for group in duplicate_results:
            keep_file = min(group, key=lambda f: f.stat().st_mtime)
            newer_files = [f for f in group if f != keep_file]
            result.extend(newer_files)
            for f in newer_files:
                rprint(f"[grey54] - {f}[/]")
    finally:
        return result


def move_duplicates(duplicate_files: list[Path], move_path: Path) -> None:
    """
    Move Duplicate Files to Given Directory.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        move_path (Path): Path to Move Duplicate Files to.
    """
    try:
        progress.start()
        move_task = progress.add_task("[blue]Moving Files", count=len(duplicate_files))
        rprint(f"[blue]Moving Duplicate Files to {move_path}...[/]")

        for f in duplicate_files:
            rprint(f"[blue]Moving File: {f} to {move_path}[/]")
            shutil.move(f, move_path)
            log(level="info", message=f"Moved Newer File {f} to {move_path}")
            progress.update(move_task, advance=move_task)
    except (OSError, shutil.Error):
        log(
            level="error", message=f"✘ Could Not Move {duplicate_files}.", exc_info=True
        )
    finally:
        progress.stop()


def delete_duplicates(duplicate_files: list) -> None:
    """
    Delete Duplicate Files.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
    """
    try:
        progress.start()
        delete_task = progress.add_task(
            "[bold red]Deleting Files...", count=len(duplicate_files)
        )
        rprint("[bold reverse red]⚠️ Deleting Duplicates...[/]")
        for f in duplicate_files:
            remove(f)
            progress.update(delete_task, advance=delete_task)
    except OSError:
        log(
            level="error",
            message=f"✘ Could Not Delete {duplicate_files}.",
            exc_info=True,
        )
    except Exception:
        log(level="error", message="✘ Unexpected Error", exc_info=True)
    finally:
        progress.stop()


def confirm_delete(duplicate_files: list) -> bool:
    """
    Confirm Deletion of Duplicate Files from User.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
    Returns:
        bool: True if User Confirms Deletion, False Otherwise.
    """
    confirm = Prompt.ask(
        "[bold reverse red]⚠️ Are you sure you want to delete all duplicates? (Y/N): [/]",
        case_sensitive=False,
    ).strip()
    return confirm in ("y", "yes")
