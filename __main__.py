import time
import sys

from src.cli.dedupe import main
from src.ui.display import info
from src.core.log import log

if __name__ == "__main__":
    start_time = time.time()
    log(level="info", message="Starting Program...")
    main(sys.argv[1:])
    time_taken = time.time() - start_time
    log(level="info", message=f"Time Taken: {'%.2f' % time_taken}s")