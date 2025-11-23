import shutil
from os import remove
from pathlib import Path
from rich import print as rprint
from rich.prompt import Prompt
from rich.progress import Progress

from utils.log import log
from utils.verbose import verbose

progress = Progress()


@verbose(lambda files: f"Moving {len(files)} duplicates")
def move_duplicates(
    duplicate_files: list[Path], move_path: Path, dry_run_flag: bool
) -> None:
    """
    Move Duplicate Files to Given Directory.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        move_path (Path): Path to Move Duplicate Files to.
        dry_run_flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    """
    try:
        progress.start()
        move_task = progress.add_task("[blue]Moving Files", count=len(duplicate_files))
        rprint(f"[blue]Moving Duplicate Files to {move_path}...[/]")
        if dry_run_flag:
            rprint("[bold green]Dry Run Enabled![/]")
        else:
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


@verbose(lambda files: f"Deleting {len(files)} duplicates")
def delete_duplicates(duplicate_files: list[Path], dry_run_flag: bool) -> None:
    """
    Delete Duplicate Files.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
        dry_run_flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    """
    try:
        progress.start()
        delete_task = progress.add_task(
            "[bold red]Deleting Files...", count=len(duplicate_files)
        )
        rprint("[bold reverse red]⚠️ Deleting Duplicates...[/]")
        if dry_run_flag:
            rprint("[bold green]Dry Run Enabled![/]")
            progress.update(delete_task, advance=len(duplicate_files))
        else:
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


def confirm_delete() -> bool:
    """
    Confirm Deletion of Duplicate Files from User.
    Returns:
        bool: True if User Confirms Deletion, False Otherwise.
    """
    confirm = Prompt.ask(
        "[bold reverse red]⚠️ Are you sure you want to delete all duplicates? (Y/N): [/]",
        case_sensitive=False,
    ).strip()
    return confirm in ("y", "yes")
