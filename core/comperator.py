from pathlib import Path


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
    for group in duplicate_results:
        if keep_newest_file:
            keep_file = max(group, key=lambda f: f.stat().st_mtime)
        else:
            keep_file = min(group, key=lambda f: f.stat().st_mtime)

        kept_files = [f for f in group if f != keep_file]
        result.extend(kept_files)
    return result
