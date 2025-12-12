import os
import shutil

from pathlib import Path


def move_duplicates(
    duplicate_files: list[Path], move_path: Path, dry_run_flag: bool
) -> dict[str, list[str | list[str | Exception]]]:
    """
    Move Duplicate Files to Given Directory.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        move_path (Path): Path to Move Duplicate Files to.
        dry_run_'flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    Returns:
        dict[list[str | None]]: Dictionary of All Files Moved, Skipped, or Failed to Move.
    """
    result: dict[str, list[str | list[str | Exception]]] = {
        "moved": [],
        "skipped": [],
        "errors": [],
    }
    if dry_run_flag:
        result["skipped"].extend([str(f) for f in duplicate_files])
        return result

    for f in duplicate_files:
        try:
            shutil.move(f, move_path)
            result["moved"].append(str(f))
        except (PermissionError, FileNotFoundError, OSError) as e:
            result["errors"].append([str(f), e])
    return result


def delete_duplicates(
    duplicate_files: list[Path], dry_run_flag: bool
) -> dict[str, list[str | list[str | Exception]]]:
    """
    Delete Duplicate Files.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
        dry_run_flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    Returns:
        dict[list[str | None]]: Dictionary of All Files Deleted, Skipped, or Failed to Delete.
    """
    result: dict[str, list[str | list[str | Exception]]] = {
        "deleted": [],
        "skipped": [],
        "errors": [],
    }
    if dry_run_flag:
        result["skipped"].append([str(f) for f in duplicate_files])
        return result

    for f in duplicate_files:
        try:
            os.remove(f)
            result["deleted"].append(str(f))
        except (PermissionError, FileNotFoundError, OSError) as e:
            result["errors"].append([str(f), e])
    return result
