from functools import wraps
from rich import print as rprint
import ui.verbose as v

from ui.display import print_verbose

VERBOSE = False


def set_verbose(value: bool):
    global VERBOSE
    VERBOSE = value


def verbose(context=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if v.VERBOSE:
                if isinstance(context, str):
                    print_verbose(f"[VERBOSE] {context} ...")

            result = func(*args, **kwargs)

            if v.VERBOSE:
                if callable(context):
                    print_verbose(f"[VERBOSE] {context(result)}")
                print_verbose(f"[VERBOSE] Done: {func.__name__}")

            return result

        return wrapper

    return decorator
