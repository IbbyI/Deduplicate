from pathlib import Path

from os.path import splitext
from ui.verbose import verbose
from ui.display import ask_yes_no, success, warn, error

from core.log import log
from core.actions import write_to_output, delete_duplicates, move_duplicates


@verbose(
    lambda args, result: (
        "No Results."
        if result is None
        else f"Moved: {len(result["moved"])}\n"
        f"Skipped: {len(result["skipped"])}\n"
        f"Skipped: {len(result["errors"])}"
    )
)
def handle_move(
    duplicate_files: list[Path], move_path: Path, dry_run_flag: bool
) -> dict[str, list[str | list[str | Exception]]]:
    """
    Calls Move Logic and Handles UI.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        move_path (Path): Path to Move Duplicate Files to.
        dry_run_flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    Returns:
        dict[str, list[Path | str]]: Dictionary of All Files Moved, Skipped, or Failed to Move.
    """
    if dry_run_flag:
        success("Dry Run Flag Enabled!")
    result: dict[str, list[str | list[str | Exception]]] = move_duplicates(
        duplicate_files, move_path, dry_run_flag
    )
    log(
        level="info",
        message=f"Moved: {result["moved"]}, skipped: {result["skipped"]}, errors: {result["errors"]}",
    )

    success(f"Moved: {len(result["moved"])} Files.")
    warn(f"Skipped: {len(result["skipped"])} Files.")
    if result["errors"]:
        error(f"Errors: {len(result["errors"])} Files.")
    return result


@verbose(
    lambda args, result: (
        "No Results."
        if result is None
        else f"Deleted: {len(result["deleted"])}\n"
        f"Skipped: {len(result["skipped"])}\n"
        f"Skipped: {len(result["errors"])}"
    )
)
def handle_delete(
    duplicate_files: list[Path], dry_run_flag: bool
) -> dict[str, list[str | list[str | Exception]]]:
    """
    Calls Delete Logic and Handles UI.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
        dry_run_flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    Returns:
        dict[list[str | None]]: Dictionary of All Files Deleted, Skipped, or Failed to Delete.
    """
    if dry_run_flag:
        success("Dry Run Flag Enabled!")
    result: dict[str, list[str | list[str | Exception]]] = delete_duplicates(
        duplicate_files, dry_run_flag
    )
    log(
        level="info",
        message=f"Deleted: {result["deleted"]}, skipped: {result["skipped"]}, errors: {result["errors"]}",
    )
    success(f"Deleted {len(result["deleted"])} Files.")
    warn(f"Skipped: {len(result["skipped"])} Files.")
    if result["errors"]:
        error(f"Errors: {len(result["errors"])} Files.")
    return result


def handle_output_file(duplicate_files: list[Path], output_file: Path) -> None:
    """
    Handles UI to Write to Output File.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        output_file (Path): Path of Output File to Write To.
    """
    try:
        file_extension = splitext(output_file)[1]
        write_to_output(duplicate_files, output_file, file_extension)
        success(f"Sucessfully Wrote to Output File: {output_file}")
    except IOError as e:
        log(
            level="error",
            message=f"❌ Failed To Write to Output File: {output_file}, {e}",
        )
        raise IOError(f"❌ Failed To Write to Output File: {output_file}, {e}") from e


def confirm_delete() -> bool:
    """
    Confirm Deletion of Duplicate Files from User.
    Returns:
        bool: True if User Confirms Deletion, False Otherwise.
    """
    confirm = ask_yes_no(
        "Are you sure you want to delete all duplicates?", style="red bold reverse"
    )
    return confirm
