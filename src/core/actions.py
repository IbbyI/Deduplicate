import shutil
from os import remove
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


def write_to_output(
    duplicate_files: list[Path], output_file: Path, file_extension: str
) -> None:
    """
    Write Results to Output File.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        output_file (Path): Path of Output File to Write To.
    """
    allowed_ext = [".txt", ".csv"]
    try:
        if file_extension not in allowed_ext:
            raise ValueError(
                f"{file_extension} File Extension is not Supported For Output File."
            )
        if file_extension == ".csv":
            import csv

            with open(output_file, "w") as f:
                csvwriter = csv.writer(f)

                csvwriter.writerow(["Path"])
                csvwriter.writerows([[str(p)] for p in duplicate_files])
            return

        with open(output_file, "w") as f:
            f.write("✅ Duplicate Files Found:\n")
            for file in duplicate_files:
                f.write(f"  -  {file}\n")
    except Exception as e:
        raise RuntimeError(f"❌ Failed To Write to {output_file}: {e}") from e
