import hashlib
from sys import exit
from pathlib import Path
from rich import print as rprint

from utils.log import log


def hash_file(path: Path) -> str:
    """
    Compute SHA-256 Hash of File Contents in 4KB Chunks.
    Args:
        path (Path): Path to the file to hash
    Returns:
        str: SHA-256 Hash of File Contents
    """
    if path.is_dir():
        raise ValueError(f"Cannot hash a directory: {path}")

    try:
        log(level="info", message=f"Chunk Hashing Contents from File {path}.")
        sha256_hash = hashlib.sha256()
        with open(path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
            f.close()
        return sha256_hash.hexdigest()
    except Exception as e:
        rprint(f"❌ [bold underline red]Could Not Hash File {path}: {e}[/]")
        log(
            level="error",
            message=f"✘ Could Not Hash File {path}: {e}",
            exc_info=True,
        )
        exit(1)
