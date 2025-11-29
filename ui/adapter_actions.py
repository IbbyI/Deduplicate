from pathlib import Path

from ui.display import ask_yes_no, success, info, warn

from core.log import log
from core.actions import write_to_output, delete_duplicates, move_duplicates


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


def handle_output_file(duplicate_files: list[Path], output_file: Path) -> None:
    """
    Handles UI to Write to Output File.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        output_file (Path): Path of Output File to Write To.
    """
    try:
        write_to_output(duplicate_files, output_file)
        success(f"Sucessfully Wrote to Output File: {output_file}")
    except IOError as e:
        log(
            level="error",
            message=f"❌ Failed To Write to Output File: {output_file}, {e}",
        )
        raise IOError(f"❌ Failed To Write to Output File: {output_file}, {e}") from e


def handle_delete(duplicate_files: list[Path], dry_run_flag: bool) -> None:
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
    result = delete_duplicates(duplicate_files, dry_run_flag)
    log(
        level="info",
        message=f"Deleted: {result["deleted"]}, skipped: {result["skipped"]}, errors: {result["errors"]}",
    )
    success(f"Deleted {len(result["deleted"])} Files.")
    return result


def handle_move(
    duplicate_files: list[Path], move_path: Path, dry_run_flag: bool
) -> dict[list[str | None]]:
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
    result = move_duplicates(duplicate_files, move_path, dry_run_flag)
    log(
        level="info",
        message=f"Moved: {result["moved"]}, skipped: {result["skipped"]}, errors: {result["errors"]}",
    )

    success(f"Moved: {len(result["moved"])} Files.")
    warn(f"Skipped: {len(result["skipped"])} Files.")
    if result["errors"]:
        error(f"Errors: {len(result["errors"])} Files.")
    return result
