from pathlib import Path

from core.log import log
from ui.verbose import verbose
from ui.display import success, ask_yes_no, print_duplicates


@verbose(lambda result: f"Found {len(result or [])} duplicate files")
def compare_files(
    duplicate_results: list[list[Path]], keep_newest_file: bool = False
) -> list[Path]:
    """
    Compare Duplicate Files and Select Newer One.
    Args:
        duplicate_results (list): List of nested arrays containing paths of duplicate files.
    Returns:
        list[Path]: List of duplicate files, with the oldest file removed from each group.
    """
    result = []
    try:
        for group in duplicate_results:
            if keep_newest_file:
                keep_file = max(group, key=lambda f: f.stat().st_mtime)
            else:
                keep_file = min(group, key=lambda f: f.stat().st_mtime)
            log(level="info", message=f"Setting file {keep_file} as original.")

            newer_files = [f for f in group if f != keep_file]
            result.extend(newer_files)
        number_of_duplicates = len(result)
        success(f"{number_of_duplicates} Duplicate Files Found:")
        if number_of_duplicates > 30:
            ask_print = ask_yes_no(
                "Would You Like To Print the Paths of All Duplicates To Console? ",
                style="cyan",
            )
            if ask_print:
                print_duplicates(result)
    finally:
        return result
