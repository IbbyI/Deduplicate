import sys
from time import time

from core.log import log
from ui.display import info
from cli.dedupe import main


def entrypoint() -> None:
    """
    Entry Point for the Application.
    Runs the Main Function, Writes Log & Prints Time Taken.
    """
    start_time = time()
    log(level="info", message="Starting Program...")
    log(level="info", message="Parsing Command Line Arguments...")
    main(sys.argv[1:])

    time_taken = time() - start_time
    log(level="info", message=f"Time Taken: {'%.2f' % time_taken}s")
    info(f"Time Taken: {'%.2f' % time_taken}s", style="underline")


if __name__ == "__main__":
    entrypoint()
