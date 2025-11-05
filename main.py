import sys
import time
import argparse
from pathlib import Path

from utils.log import log
from utils.hash import hash_file


def main(argv: list[str]) -> None:
    try:
        parser = argparse.ArgumentParser(
            prog="Deduplicate!",
            description="Recursively check for duplicate files in a given directory.",
            formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        )
        parser.add_argument(
            "-p",
            "--path",
            type=str,
            nargs=1,
            default="./",
            help="Given Path to Run Program",
        )
        parser.add_argument(
            "--delete-duplicates", help="Delete All Duplicate Files Found."
        )
        parser.add_argument(
            "-mv",
            "--move-duplicates",
            nargs=1,
            type=str,
            help="Move Duplicate Files to given directory.",
        )

        args = parser.parse_args()
        start_path = Path(args.path[0])
        duplicate_path = args.move_duplicates

        if not start_path.exists():
            print("✘ Start Path Does Not Exist.")
            log(
                level="error",
                message="✘ Start Path Does Not Exist.",
                exc_info=True,
            )
            sys.exit(2)

        dict = {}
        for file in start_path.iterdir():
            hashed_file = hash_file(file)
            dict.setdefault(hashed_file, []).append(file)

        duplicate_results = [value for value in dict.values() if len(value) > 1]

        if not duplicate_results:
            print(f"No Duplicates Found in {start_path}.\nTerminating Program...")
            log(
                level="info",
                message=f"No Duplicates Found in {start_path}.\nTerminating Program...",
            )
            sys.exit()

        for duplicates in duplicate_results:
            paths = [str(p) for p in duplicates]
            print(f"{', '.join(paths)} are duplicates.")
            log(level="info", message=f"{', '.join(paths)} are duplicates.")

    except argparse.ArgumentError or TypeError as e:
        print(e)
        sys.exit(2)


if __name__ == "__main__":
    start_time = time.time()
    log(level="info", message="Starting Program...")
    main(sys.argv[1:])
    time_taken = time.time() - start_time
    log(level="info", message=f"Time Taken: {"%.2f" % time_taken}s")
