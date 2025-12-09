import hashlib
from pathlib import Path


QUICK_HASH_BYTES_THRESHOLD: int = 2 * 1024 * 1024


def full_hash(file: Path) -> str:
    """
    Compute SHA-256 Hash of Entire Contents of File in 4KB Chunks.
    Args:
        file (Path): Path to the File to Hash
    Returns:
        str: SHA-256 Hash of File Contents
    """
    if file.is_dir():
        raise ValueError(f"❌ Cannot hash a directory: {file}")

    if not file.exists():
        raise FileNotFoundError(f"❌ {file} does not exist.")

    try:
        sha256_hash = hashlib.sha256()
        with open(file, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                sha256_hash.update(chunk)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to hash file '{file}': {e}") from e
    return sha256_hash.hexdigest()


def quick_hash(file: Path) -> str:
    """
    Compute 4KB Chunks from Start and End of file using SHA-256 Hash of File Contents.
    Args:
        file (Path): Path to the File to Hash
    Returns:
        str: SHA-256 Hash of Sampled File Contents
    """
    if file.is_dir():
        raise ValueError(f"❌ Cannot hash a directory: {file}")

    if not file.exists():
        raise FileNotFoundError(f"❌ {file} does not exist.")

    try:
        sha256_hash = hashlib.sha256()
        file_size = file.stat().st_size

        with open(file, "rb") as f:
            sha256_hash.update(f.read(4096))
            if file_size > 4096:
                f.seek(-4096, 2)
                sha256_hash.update(f.read(4096))

        return sha256_hash.hexdigest()

    except Exception as e:
        raise RuntimeError(f"❌ Failed to hash file '{file}': {e}") from e


def auto_hash(file: Path) -> str:
    """
    Compute SHA-256 Hash of File Contents Based on File Size.
    If The File > 2MB, It Fast Hashes the File, Else Slow Hash.
        Args:
        file (Path): Path oF the file to hash
    Returns:
        str: SHA-256 Hash of File Contents or Sample of File.
    """
    try:
        if file.stat().st_size <= QUICK_HASH_BYTES_THRESHOLD:
            return full_hash(file)
        return quick_hash(file)
    except Exception as e:
        raise RuntimeError(f"❌ Failed to hash file '{file}': {e}") from e
