from functools import wraps

from ui.display import print_verbose

VERBOSE = False


def set_verbose(value: bool):
    """
    Sets Global Verbose Variable.
    Args:
        Value (bool): Verbose Enabled if True, else Disabled.
    """
    global VERBOSE
    VERBOSE = value


def verbose(context=None):
    """
    Verbose Decorator That Prints Detailed Debugging Messages to Console.
    Args:
        context (str | Callable): Determines the message to print.
     Returns:
        (function): Wrapped Function with Verbose Logging.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):

            if VERBOSE:
                if callable(context):
                    print_verbose(context(args, None))
                elif isinstance(context, str):
                    print_verbose(f"[VERBOSE] {context}")

            result = func(*args, **kwargs)

            if VERBOSE:
                if callable(context):
                    print_verbose(context(args, result))

            return result

        return wrapper

    return decorator
