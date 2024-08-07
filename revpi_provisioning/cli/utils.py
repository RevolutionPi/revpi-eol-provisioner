"""CLI command utilities."""

import sys


global verbose
verbose = False


def error(msg: str, rc: int) -> None:
    """Print error message to STDERR and return with given return code."""
    print(msg, file=sys.stderr)

    return rc


def verboseprint(*args: str, **kwargs: dict) -> None:
    """Print only if verbose mode is enabled."""
    if verbose:
        print(*args, **kwargs)
