from pathlib import Path


def compare_files(
    duplicate_files: list[list[Path]], keep_newest_file: bool = False
) -> list[Path]:
    """
    Compare Duplicate Files and Select Newer One.
    Args:
        duplicate_files (list): List of nested arrays containing paths of duplicate files.
    Returns:
        list[Path]: List of duplicate files, with the oldest file removed from each group.
    """
    result = []
    for group in duplicate_files:
        if keep_newest_file:
            keep_file = max(group, key=lambda f: f.stat().st_mtime)
        else:
            keep_file = min(group, key=lambda f: f.stat().st_mtime)

        kept_files = [f for f in group if f != keep_file]
        result.extend(kept_files)
    return result
