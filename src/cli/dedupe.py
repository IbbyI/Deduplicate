import argparse
from pathlib import Path

from core.hasher import full_hash, quick_hash, auto_hash

from ui.verbose import set_verbose
from ui.display import error, success
from ui.adapter_scanner import find_duplicates_ui
from ui.adapter_comperator import compare_files_ui, print_total_duplicates
from ui.adapter_actions import (
    confirm_delete,
    handle_output_file,
    handle_delete,
    handle_move,
)


def build_parser() -> argparse.Namespace:
    """
    Creates CLI Arguement Parser
    Returns:
        argparse.Namespace: Returns Parser Object for Argument Specifications.
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
        version="Deduplicate 1.2.3",
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


def main(argv=None) -> int:
    """
    Main Function to Run Deduplication Program.
    Args:
        argv (list[str]): List of Command Line Arguments.
    """
    import sys

    if argv is None:
        argv = sys.argv[1:]

    try:
        args = build_parser()
    except Exception as e:
        error("Could Not Create Command Line Arguments", style="")
        return 2

    try:
        args = build_parser()
        start_path = Path(args.path[0]) if args.path else Path.cwd()
        move_duplicate_path = (
            Path(args.move_duplicates[0]) if args.move_duplicates else None
        )
        output_file = Path(args.output_file[0]) if args.output_file else None
        ignore_path = Path(args.ignore_path[0]) if args.ignore_path else None

        keep_newest_file = True if args.keep_newest else False
        delete_duplicates_flag = True if args.delete_duplicates else False
        dry_run_flag = True if args.dry_run else False

        if dry_run_flag and not (delete_duplicates_flag or move_duplicate_path):
            error("Dry Run Requires Either Moving or Deletion Flag.", style="")
            return 1

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
            error("Start Path Does Not Exist.", style="")
            return 1

        if not start_path:
            error("Start Path Does Not Exist.", style="")
            return 1

        if not start_path.is_dir():
            error("Start Path is Not a Directory.", style="")
            return 1

        duplicate_group = find_duplicates_ui(
            start_path, ignore_path=ignore_path, hash_func=hash_method
        )
        if not duplicate_group:
            success("No Duplicates Found!", style="")
            return 0

        duplicate_files = compare_files_ui(duplicate_group, keep_newest_file)

        print_total_duplicates(duplicate_files)

        if move_duplicate_path:
            if not move_duplicate_path.exists():
                Path.mkdir(move_duplicate_path)
            handle_move(duplicate_files, move_duplicate_path, dry_run_flag)

        if delete_duplicates_flag:
            if confirm_delete():
                handle_delete(duplicate_files, dry_run_flag)

        if output_file:
            handle_output_file(duplicate_files, output_file)
        return 0

    except argparse.ArgumentError:
        error("Invalid Argument Error.", style="")
        return 2
    except FileNotFoundError:
        error("File Not Found.", style="")
        return 2
    except Exception as e:
        error(f"An Unexpected Error Occurred: {e}", style="")
        return 2
