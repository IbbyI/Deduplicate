import shutil
from os import remove
from pathlib import Path

from utils.log import log
from utils.hash import hash_file


def find_duplicates(start_path: str) -> None:
    """
    Find Duplicate Files in Given Path.
    Args:
        start_path (str): Path to Search for Duplicate Files.
    Returns:
        list: List of Duplicate Files Found.
    """
    log(level="info", message=f"Scanning Path '{start_path}' For Duplicate Files...")
    print(f"Scanning Path '{start_path}' For Duplicate Files...")

    hashmap = {}
    for file in start_path.rglob("*"):
        hashed_file = hash_file(file)
        hashmap.setdefault(hashed_file, []).append(file)

    duplicate_results = [value for value in hashmap.values() if len(value) > 1]

    if not duplicate_results:
        print(f"No Duplicates Found in Path: {start_path}\nTerminating Program...")
        log(
            level="info",
            message=f"No Duplicates Found in Path: {start_path}\nTerminating Program...",
        )
        return []
    for duplicates in duplicate_results:
        paths = [str(p) for p in duplicates]
        print(f"{', '.join(paths)} are identical..")
        log(level="info", message=f"{', '.join(paths)} are identical.")
    return duplicate_results


def compare_files(
    duplicate_results: list[list[Path]],
) -> list:  # Optimize Function to Avoid Nested Loops O(n^2)
    """
    Compare Duplicate Files and Select Newer One.
    Args:
        duplicate_results (list): List of nested arrays containing paths of duplicate files.
    Returns:
        list: List of duplicate files, with the oldest file removed from each group.
    """
    print(f"Duplicate Files Found:")
    result = []
    for group in duplicate_results:
        oldest_file = min(group, key=lambda f: f.stat().st_mtime)
        newer_files = [f for f in group if f != oldest_file]
        result.extend(newer_files)

    for f in newer_files:
        print(f" - {f}")
    return result


def move_duplicates(duplicate_files: list, move_path: str) -> None:
    """
    Move Duplicate Files to Given Directory.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
        move_path (str): Path to Move Duplicate Files to.
    """
    try:
        print(f"Moving Duplicate Files to {move_path}...")

        for f in duplicate_files:
            print(f"Moving File: {f} to {move_path}")
            shutil.move(f, move_path)
            log(level="info", message=f"Moved Newer File {f} to {move_path}")
    except OSError:
        log(level="error", message=f"Could Not Move {duplicate_files}.", exc_info=True)
    except shutil.Error:
        log(level="error", message=f"Could Not Move {duplicate_files}.", exc_info=True)
    except Exception as e:
        log(level="error", message=f"Unexpected Error: {e}", exc_info=True)
    finally:
        print("Duplicate Files Successfully Moved.")


def delete_duplicates(duplicate_files: list) -> None:
    """
    Delete Duplicate Files.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
    """
    try:
        for f in duplicate_files:
            remove(f)
    except OSError:
        log(
            level="error", message=f"Could Not Delete {duplicate_files}.", exc_info=True
        )
    except Exception:
        log(level="error", message="Unexpected Error", exc_info=True)
    finally:
        print("Duplicate Files Successfully Deleted.")


def confirm_delete(duplicate_files: list) -> bool:
    """
    Confirm Deletion of Duplicate Files from User.
    Args:
        duplicate_files (list): List of Duplicate Files Found.
    Returns:
        bool: True if User Confirms Deletion, False Otherwise.
    """
    for f in duplicate_files:
        print(f" - {f}")
    confirm = (
        input("Are you sure you want to delete all duplicates? (Y/N): ").strip().lower()
    )
    return confirm in ("y", "yes")
