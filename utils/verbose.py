from functools import wraps
from rich import print as rprint
import utils.verbose as v


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
                    rprint(f"[yellow][VERBOSE] {context} ...[/]")
                elif callable(context):
                    rprint(f"[yellow][VERBOSE] {context(None)}[/]")

            result = func(*args, **kwargs)

            if v.VERBOSE:
                if callable(context):
                    rprint(f"[VERBOSE] context(result)[/]")
                elif isinstance(context, str):
                    rprint(f"[yellow][VERBOSE] Done: {context}[/]")
                else:
                    rprint(f"[yellow][VERBOSE] Done: {func.__name__}[/]")

            return result

        return wrapper

    return decorator
