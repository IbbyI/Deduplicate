import hashlib
from sys import exit
from pathlib import Path
from rich import print as rprint

from utils.log import log
from utils.verbose import verbose


@verbose("Full Hashing File")
def full_hash(path: Path) -> str:
    """
    Compute SHA-256 Hash of Entire Contents of File in 4KB Chunks.
    Args:
        path (Path): Path to the File to Hash
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
        return sha256_hash.hexdigest()
    except Exception as e:
        rprint(f"❌ [bold underline red]Could Not Hash File {path}: {e}[/]")
        log(
            level="error",
            message=f"❌ Could Not Hash File {path}: {e}",
            exc_info=True,
        )


@verbose("Quick Hashing File")
def quick_hash(path: Path) -> str:
    """
    Compute 4KB Chunks from Start and End of file using SHA-256 Hash of File Contents.
    Args:
        path (Path): Path to the File to Hash
    Returns:
        str: SHA-256 Hash of Sampled File Contents
    """
    if path.is_dir():
        raise ValueError(f"Cannot hash a directory: {path}")

    try:
        log(level="info", message=f"Fast Hashing Contents from File {path}.")
        sha256_hash = hashlib.sha256()
        file_size = path.stat().st_size
        with open(path, "rb") as f:
            sha256_hash.update(f.read(4096))
            if file_size > 4096:
                f.seek(-4096, 2)
                sha256_hash.update(f.read(4096))
        return sha256_hash.hexdigest()
    except Exception as e:
        rprint(f"❌ [bold underline red]Could Not Fast Hash File {path}: {e}[/]")
        log(
            level="error",
            message=f"❌ Could Not Fast Hash File {path}: {e}",
            exc_info=True,
        )


@verbose("Auto Hashing File")
def auto_hash(path: Path) -> str:
    """
    Compute SHA-256 Hash of File Contents Based on File Size.
    If The File > 2MB, It Fast Hashes the File, Else Slow Hash.
        Args:
        path (Path): Path o the file to hash
    Returns:
        str: SHA-256 Hash of File Contents or Sample of File.
    """
    if path.stat().st_size <= 2 * 1024 * 1024:
        return full_hash(path)
    return quick_hash(path)
