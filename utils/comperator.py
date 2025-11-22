from pathlib import Path
from rich import print as rprint
from rich.prompt import Prompt
from rich.progress import Progress

from utils.log import log
from utils.verbose import verbose

progress = Progress()


@verbose("Comparing Duplicates")
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
        rprint(f"✅ [bold green underline]{number_of_duplicates} Duplicate Files Found:[/]")
        if number_of_duplicates > 30:
            ask_print = Prompt.ask(
                f"[bold blue]Would You Like To Print the Paths of All Duplicates To Console? (Y/N)[/]"
            ).lower()
            if ask_print not in ("yes", "y"):
                return result
        for f in result:
            rprint(f"[grey54] -n {f}[/]")
    finally:
        return result