import sys


def error(msg: str, rc: int) -> None:
    """Print error message to STDERR and return with given return code."""
    print(msg, file=sys.stderr)

    return rc
