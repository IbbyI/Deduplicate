import sys
import argparse
from pathlib import Path
from collections import Counter

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
        print(args)
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
            dict.update({file: hashed_file})

        counts = Counter(dict.values())
        result = {key: value for key, value in dict.items() if counts[value] > 1}
        print(result.keys(), result.values())

    except argparse.ArgumentError and TypeError as e:
        parser.print_help()
        sys.exit(2)


if __name__ == "__main__":
    log(level="info", message="Starting Program...")
    main(sys.argv[1:])
