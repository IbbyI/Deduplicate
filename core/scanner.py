from pathlib import Path
from typing import Callable


def find_duplicates(
    start_path: Path, ignore_path: Path | None, hash_func: Callable[[Path], str]
) -> list[list[Path]] | None:
    """
    Find Duplicate Files in Given Path.
    Args:
        start_path (Path): Path to Search for Duplicate Files.
        ignore_path (Path | None): Path to Ignore Searching (Optional Flag)
        hash_func (Callable[[Path], str]):
            A hashing function that takes a Path and returns a SHA-256 digest string
    Returns:
        list[list[Path]]: Nested List of Path objects of duplicate files found.
        None: If no duplicate files are found, returns None.
    """

    hashmap: dict[str, list[Path]] = {}

    for file in start_path.rglob("*"):
        if not file.is_file():
            continue
        if ignore_path and file.is_relative_to(ignore_path):
            continue

        hashed = hash_func(file)
        hashmap.setdefault(hashed, []).append(file)

    return [group for group in hashmap.values() if len(group) > 1]
