from functools import wraps

VERBOSE = False


def set_verbose(value: bool):
    global VERBOSE
    VERBOSE = value


def verbose(message: str = None):
    """
    Decorator to Print Before and After a Function if Verbose Mode is Enabled.
    Args:
        message (str): Message to Print Before Function is Called.
    """

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if VERBOSE:
                print(f"[VERBOSE] {message or func.__name__} ...")
            result = func(*args, **kwargs)
            if VERBOSE:
                print(f"[VERBOSE] Done: {message or func.__name__}")
            return result

        return wrapper

    return decorator
