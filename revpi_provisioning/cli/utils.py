# SPDX-FileCopyrightText: 2022-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""CLI command utilities."""

import sys


global verbose
verbose = False


def error(msg: str, rc: int) -> None:
    """Print error message to STDERR and return with given return code."""
    print(msg, file=sys.stderr)

    sys.exit(rc)


def verboseprint(*args: str, **kwargs: dict) -> None:
    """Print only if verbose mode is enabled."""
    if verbose:
        print(*args, **kwargs)
