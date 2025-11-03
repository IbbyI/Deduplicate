import sys
import argparse

from utils.log import log
from utils.search_duplicate import *


def main(argv: list[str]) -> None:
    parser = argparse.ArgumentParser(
        prog="Deduplicate!",
        description="Recursively check for duplicate files in a given directory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("-p", type=str, default="./", help="Given Path to Run Program")


if __name__ == "__main__":
    log(level="info", message="Starting Program...")
    main[sys.argv[1:]]
