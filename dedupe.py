import sys
import time
import argparse
from pathlib import Path
from rich import print as rprint

from utils.log import log
from utils.hasher import full_hash, quick_hash, auto_hash
from utils.verbose import set_verbose
from utils.actions import move_duplicates, delete_duplicates, confirm_delete
from utils.comperator import compare_files
from utils.scanner import find_duplicates


def main(argv: list[str]) -> None:
    """
    Main Function to Run Deduplication Program.
    Args:
        argv (list[str]): List of Command Line Arguments.
    """
    parser = argparse.ArgumentParser(
        prog="Deduplicate",
        description="Recursively check for duplicate files in a given directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    try:
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
        args = parser.parse_args()
        start_path = Path(args.path[0])
        duplicate_path = Path(args.move_duplicates[0]) if args.move_duplicates else None
        output_file = Path(args.output_file[0]) if args.output_file else None
        ignore_path = Path(args.ignore_path[0]) if args.ignore_path else None

        keep_newest_file = True if args.keep_newest else False
        delete_duplicates_flag = True if args.delete_duplicates else False

        if args.verbose:
            set_verbose(True)

        if args.full:
            hash_method = full_hash
        elif args.quick:
            hash_method = quick_hash
        else:
            hash_method = auto_hash

        if not start_path.exists():
            rprint("❌ [bold underline red]Start Path Does Not Exist.[/]")
            log(
                level="error",
                message="✘ Start Path Does Not Exist.",
                exc_info=True,
            )
            sys.exit(2)

        duplicate_group = find_duplicates(
            start_path, ignore_path=ignore_path, hash_func=hash_method
        )
        if not duplicate_group:
            return
        duplicate_files = compare_files(duplicate_group, keep_newest_file)

        log(
            level="info",
            message=f"✔ Completed Search! Found {len(duplicate_files)} duplicate files!",
        )

        if duplicate_path:
            if not duplicate_path.exists():
                Path.mkdir(duplicate_path)
                log(level="info", message=f"Directory Created at: {duplicate_path}")
            move_duplicates(duplicate_files, duplicate_path)

        if delete_duplicates_flag:
           if confirm_delete():
                delete_duplicates(duplicate_files)

        if output_file:
            write_to_output(duplicate_files=duplicate_files, output_file=output_file)

    except argparse.ArgumentError:
        log(level="error", message="✘ Invalid Argument Error.", exc_info=True)
        rprint("❌ [bold underline red]Invalid Argument Error.[/]")
        parser.print_help()
        sys.exit(2)
    except FileNotFoundError as e:
        log(level="error", message=f"✘ File Not Found: {e}", exc_info=True)
        rprint(f"❌ [bold underline red]File Not Found: {e}[/]")
        sys.exit(1)


def write_to_output(duplicate_files: list[Path], output_file: Path) -> None:
    try:
        with open(output_file, "w") as f:
            f.write("✔ Duplicate Files Found:\n")
            for file in duplicate_files:
                f.write(f"  -  {file}\n")
        log(
            level="info",
            message=f"✔ Duplicate Results Written to Output File: {output_file}",
        )
        rprint(
            f"✅ [bold underline green]Duplicate Results Written to Output File: {output_file}[/]"
        )
    except (FileNotFoundError, PermissionError, OSError) as e:
        log(
            level="error",
            message=f"✘ Could Not Write to Output File {output_file}: {e}",
            exc_info=True,
        )
        rprint(
            f"❌ [bold underline red]Could Not Write to Output File {output_file}: {e}[/]"
        )


if __name__ == "__main__":
    start_time = time.time()
    log(level="info", message="Starting Program...")
    main(sys.argv[1:])
    time_taken = time.time() - start_time
    log(level="info", message=f"Time Taken: {"%.2f" % time_taken}s")
    rprint(f"[bold underline blue]Time Taken: {'%.2f' % time_taken}s[/]")
