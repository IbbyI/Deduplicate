from pathlib import Path
from rich.progress import Progress

from core.log import log
from core.comperator import compare_files

from ui.verbose import verbose
from ui.display import ask_yes_no, print_duplicates, error, info

progress = Progress()


@verbose(lambda args, files: f"Duplicate Files Found: {len(files or [])}")
def compare_files_ui(
    duplicate_files: list[list[Path]], keep_newest_file: bool = False
) -> list[Path]:
    """
    Handles UI Elements for the Comparison Logic.
    Args:
        duplicate_files (list): List of nested arrays containing paths of duplicate files.
    Returns:
        list[Path]: List of duplicate files, with the oldest file removed from each group.
    """
    progress.start()
    try:
        progress.add_task("[purple]Comparing Files            ", total=None)
        log(level="info", message="Comparing Files")
        result = compare_files(duplicate_files, keep_newest_file)
        return result
    except Exception as e:
        error(str(e))
        log(level="error", message=str(e))
        return []
    finally:
        progress.stop()


def print_total_duplicates(result: list[Path]) -> None:
    """
    Handles Printing Duplicates to Console Based on User Input.
    Args:
        list[Path]: List of duplicate files.
    """
    number_of_duplicates = len(result)
    info(f"{number_of_duplicates} Duplicates Found.", style="bold underline")
    log(level="info", message=f"{number_of_duplicates} Duplicates Found.")
    if number_of_duplicates > 30:
        if not ask_yes_no(
            f"Print All {number_of_duplicates} Duplicate File Paths?",
            style="bold underline red",
        ):
            return
    print_duplicates(result)
