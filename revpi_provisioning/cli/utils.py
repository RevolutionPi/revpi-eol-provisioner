import sys


def error(msg: str, rc: int):
    print(msg, file=sys.stderr)
    sys.exit(rc)
