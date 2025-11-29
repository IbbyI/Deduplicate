import shutil
from os import remove
from pathlib import Path

from ui.verbose import verbose


@verbose(
    lambda args, result: (
        "No Results."
        if result is None
        else f"Moved: {len(result["moved"])}\n"
        f"Skipped: {len(result["skipped"])}\n"
        f"Skipped: {len(result["errors"])}"
    )
)
def move_duplicates(
    duplicate_files: list[Path], move_path: Path, dry_run_flag: bool
) -> dict[list[str | None]]:
    """
    Move Duplicate Files to Given Directory.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        move_path (Path): Path to Move Duplicate Files to.
        dry_run_flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    Returns:
        dict[list[str | None]]: Dictionary of All Files Moved, Skipped, or Failed to Move.
    """
    result = {"moved": [], "skipped": [], "errors": []}
    for f in duplicate_files:
        if dry_run_flag:
            result["skipped"].append(str(f))
            continue

        try:
            shutil.move(f, move_path)
            result["moved"].append(str(f))
        except Exception as e:
            result["errors"].append([str(f), e])
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
def delete_duplicates(
    duplicate_files: list[Path], dry_run_flag: bool
) -> dict[list[str | None]]:
    """
    Delete Duplicate Files.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
        dry_run_flag (bool): Checks if Dry Run Flag is Enabled. False by Default.
    Returns:
        dict[list[str | None]]: Dictionary of All Files Deleted, Skipped, or Failed to Delete.
    """
    result = {"deleted": [], "skipped": [], "errors": []}
    for f in duplicate_files:
        if dry_run_flag:
            result["skipped"].append(str(f))
            continue

        try:
            remove(f)
            result["deleted"].append(str(f))
        except Exception as e:
            result["errors"].append([str(f), e])
    return result


def write_to_output(duplicate_files: list[Path], output_file: Path) -> None:
    """
    Write Results to Output File.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        output_file (Path): Path of Output File to Write To.
    """
    try:
        with open(output_file, "w") as f:
            f.write("✅ Duplicate Files Found:\n")
            for file in duplicate_files:
                f.write(f"  -  {file}\n")
    except Exception as e:
        raise RuntimeError(f"❌ Failed To Write to {output_file}: {e}") from e
