import os
import csv
import shutil
import datetime

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
        result["skipped"].append([str(f) for f in duplicate_files])
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


def write_to_output(
    output_file_data: list[str], output_file: Path, file_extension: str
) -> None:
    """
    Write Results to Output File.
    Args:
        duplicate_files (list[Path]): List of Duplicate Files Found.
        output_file (Path): Path of Output File to Write To.
    """
    ALLOWED_EXT = [".txt", ".csv"]
    OUTPUT_FILE_HEADER = ["Path", "File Size", "Created Date", "Last Modified Date"]
    try:
        if file_extension not in ALLOWED_EXT:
            raise ValueError(
                f"{file_extension} File Extension is not Supported For Output File."
            )
        if file_extension == ".csv":
            with open(output_file, "w") as f:
                csvwriter = csv.writer(f)

                csvwriter.writerow(OUTPUT_FILE_HEADER)
                csvwriter.writerows([p for p in output_file_data])

        with open(output_file, "w") as f:
            f.write("✅ Duplicate Files Found:\n")
            for file in output_file_data:
                f.write(f"  -  {file}\n")
    except Exception as e:
        raise RuntimeError(f"❌ Failed To Write to {output_file}: {e}") from e


def output_file_format(duplicate_files: list[Path]) -> list[str]:
    """
    Format Duplicate Files for Output File.
    Args:
        duplicate_files (list[Path]):  List of Duplicate Files Found.
    Returns:
        list[str]: Formatted Data to Write to Output File.
    """
    output_file_data = []
    for p in duplicate_files:
        dt_created = datetime.datetime.fromtimestamp(os.path.getctime(p)).strftime(
            "%d/%m/%Y %H:%M:%S"
        )
        dt_modified = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime(
            "%d/%m/%Y %H:%M:%S"
        )

        file_size = f"Size: {os.path.getsize(p)} bytes"
        created = f"Created: {dt_created}"
        last_modified = f"Last Modified: {dt_modified}"

        output_file_data.append([str(p), file_size, created, last_modified])
    return output_file_data
