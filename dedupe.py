import sys
import time
import argparse
from pathlib import Path

from core.log import log
from core.hasher import full_hash, quick_hash, auto_hash
from ui.verbose import set_verbose
from core.actions import (
    move_duplicates,
    delete_duplicates,
    confirm_delete,
    write_to_output,
)
from core.comperator import compare_files
from core.scanner import find_duplicates
from ui.display import info, error


def build_parser() -> argparse.ArgumentParser:
    """
    Creates CLI Arguement Parser
    Returns:
        argparse.ArgumentParser: Returns Parser Object for Argument Specification
    """
    parser = argparse.ArgumentParser(
        prog="Deduplicate",
        description="Recursively check for duplicate files in a given directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "-ver",
        "-VER",
        "--version",
        action="version",
        version="Deduplicate 1.1.9",
        help="Show Program Version.",
    )
    parser.add_argument(
        "-vv",
        "-VV",
        "--verbose",
        action="store_true",
        help="Print Detailed Output For Debugging",
    )
    parser.add_argument(
        "-p",
        "-P",
        "--path",
        type=str,
        nargs=1,
        default="./",
        help="Given Path to Run Program",
    )
    parser.add_argument(
        "-del",
        "--delete-duplicates",
        action="store_true",
        help="Delete All Duplicate Files Found.",
    )
    parser.add_argument(
        "-mv",
        "--move-duplicates",
        nargs=1,
        type=str,
        help="Move Duplicate Files to given directory.",
    )
    parser.add_argument(
        "-o",
        "-O",
        "--output-file",
        nargs=1,
        type=str,
        help="Output File to Save Duplicate Results.",
    )
    parser.add_argument(
        "-i",
        "-I",
        "--ignore-path",
        nargs=1,
        type=str,
        help="Ignore a Specific Path from Search & Comparison.",
    )
    parser.add_argument(
        "-kn",
        "--keep-newest",
        action="store_true",
        help="Keeps the Newest Copy & Marks Older Files as Duplicates",
    )
    parser.add_argument(
        "-f",
        "-F",
        "--full",
        action="store_true",
        help="Longer but More Accurate Check for Duplicates",
    )
    parser.add_argument(
        "-q",
        "-Q",
        "--quick",
        action="store_true",
        help="Quick but Less Accurate Check for Duplicates",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry Run for Testing Moving & Deletion",
    )
    return parser.parse_args()


def main(argv: list[str]) -> None:
    """
    Main Function to Run Deduplication Program.
    Args:
        argv (list[str]): List of Command Line Arguments.
    """
    try:
        args = build_parser()
        start_path = Path(args.path[0])
        move_duplicate_path = (
            Path(args.move_duplicates[0]) if args.move_duplicates else None
        )
        output_file = Path(args.output_file[0]) if args.output_file else None
        ignore_path = Path(args.ignore_path[0]) if args.ignore_path else None

        keep_newest_file = True if args.keep_newest else False
        delete_duplicates_flag = True if args.delete_duplicates else False
        dry_run_flag = True if args.dry_run else False

        if dry_run_flag and not (delete_duplicates_flag or move_duplicate_path):
            return error("Dry Run Requires Either Moving or Deletion Flag.")
            sys.exit(1)

        if args.verbose:
            set_verbose(True)
        else:
            set_verbose(False)

        if args.full:
            hash_method = full_hash
        elif args.quick:
            hash_method = quick_hash
        else:
            hash_method = auto_hash

        if not start_path.exists():
            return error("Start Path Does Not Exist.")

        duplicate_group = find_duplicates(
            start_path, ignore_path=ignore_path, hash_func=hash_method
        )
        if not duplicate_group:
            return
        duplicate_files = compare_files(duplicate_group, keep_newest_file)

        if move_duplicate_path:
            if not move_duplicate_path.exists():
                Path.mkdir(move_duplicate_path)
            move_duplicates(duplicate_files, move_duplicate_path, dry_run_flag)

        if delete_duplicates_flag:
            if confirm_delete():
                delete_duplicates(duplicate_files, dry_run_flag)

        if output_file:
            write_to_output(duplicate_files=duplicate_files, output_file=output_file)

    except argparse.ArgumentError:
        return error("Invalid Argument Error.")
        parser.print_help()
    except FileNotFoundError:
        raise error("File Not Found.")
        sys.exit(1)


if __name__ == "__main__":
    start_time = time.time()
    log(level="info", message="Starting Program...")
    main(sys.argv[1:])
    time_taken = time.time() - start_time
    info(f"Time Taken: {'%.2f' % time_taken}s")
