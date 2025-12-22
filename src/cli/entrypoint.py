import sys
import tracemalloc

from time import time

from core.log import log
from cli.dedupe import main
from ui.verbose import verbose
from ui.display import info


@verbose(
    lambda _args, result: (
        f"Current Memory Usage: {result['current']:.3f}MB\n"
        f"Peak Memory Usage: {result['peak']:.3f}MB\n"
        f"Time Taken: {result['time']}s"
    )
)
def run() -> dict[str, float]:
    tracemalloc.start()
    start_time = time()

    log(level="info", message="Starting Program...")
    main(sys.argv[1:])

    time_taken = round(time() - start_time, 2)
    info(message=f"Time Taken: {time_taken}s", style="bold underline")
    
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    log(level="info", message=f"Current Memory Usage: {current:.3f}MB") 
    log(level="info", message=f"Peak Memory Usage: {peak:.3f}MB") 
    log(level="info", message=f"Time Taken: {time_taken}s")

    return {
        "current": current / (1024 * 1024),
        "peak": peak / (1024 * 1024),
        "time": time_taken,
    }


def entrypoint() -> None:
    run()


if __name__ == "__main__":
    entrypoint()
