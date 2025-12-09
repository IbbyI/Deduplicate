from pathlib import Path
from typing import Callable

from ui.verbose import verbose
from ui.display import success, error

from core.log import log
from core.hasher import quick_hash, full_hash, auto_hash


@verbose(
    lambda args, result: (
        "Could Not Full Hash File."
        if result is None
        else f"Full Hash Computed for File: {str(args[0])}, Hash: {result[:8]}..."
    )
)
def full_hash_ui(file: Path) -> str:
    """
    Handles UI Elements and Function Call for Full Hash.
    Args;
        file (Path): Path of File to Full Hash.
    Returns:
        str: SHA-256 Digest String of Entire File Contents.
    """
    try:
        result = full_hash(file)
        log(
            level="info",
            message=f"Full Hash Computed for File: {str(file)}, Hash: {result[:8]}...",
        )
        return result
    except Exception as e:
        error(f"Failed to hash {file.name}: {e}")
        raise


@verbose(
    lambda args, result: (
        "Could Not Quick Hash File."
        if result is None
        else f"Quick Hash Computed for File: {str(args[0])}, Hash: {result[:8]}..."
    )
)
def quick_hash_ui(file: Path) -> str:
    """
    Handles UI Elements and Function Call for Quick Hash.
    Args:
        file (Path): Path of File to Quick Hash.
    Returns:
        str: SHA-256 Digest String of Sampled File Contents
    """
    try:
        result = quick_hash(file)
        log(
            level="info",
            message=f"Quick Hash Computed for File: {str(file)}, Hash: {result[:8]}...",
        )
        return result
    except Exception as e:
        error(f"Failed to hash {file.name}: {e}")
        raise


@verbose(
    lambda args, result: (
        "Could Not Auto Hash File."
        if result is None
        else f"Auto Hash Computed for File: {str(args[0])}, Hash: {result[:8]}..."
    )
)
def auto_hash_ui(file: Path) -> str:
    """
    Handles UI Elements and Function Call for Auto Hash.
    Args:
        file (Path): Path of File to Auto Hash.
    Returns:
        str: SHA-256 Digest String of File Contents or Sample of File.
    """
    try:
        result = auto_hash(file)
        log(
            level="info",
            message=f"Auto Hash Computed for File: {str(file)}, Hash: {result[:8]}...",
        )
        return result
    except Exception as e:
        error(f"Failed to hash {file.name}: {e}")
        raise


@verbose(
    lambda args, func: (
        "Auto Hash Selected." if func is None else f"{func.__name__} Selected."
    )
)
def choose_hash_func(args: list[bool]) -> Callable:
    if args[0]:
        success("Full Hash Selected!", style="underline")
        return full_hash_ui
    if args[1]:
        success("Quick Hash Selected!", style="underline")
        return quick_hash_ui
    return auto_hash_ui
