# SPDX-FileCopyrightText: 2022-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Validate yaml config file CLI command."""

import argparse
import sys

from revpi_provisioning.cli.utils import error
from revpi_provisioning.config import EOLConfigException, load_config


def main() -> None:
    """Run the actual program logic.

    Returns
    -------
    int
        return code of the program
    """
    parser = argparse.ArgumentParser(description="Validate device configuration file")
    parser.add_argument("config", metavar="device-configuration-file")

    args = parser.parse_args()

    device_config_file = args.config

    try:
        load_config(device_config_file, absolute_path=True)
    except EOLConfigException as ce:
        error(f"Failed to validate device configuration file: {ce}", 1)

    print(f"Device configuration file '{device_config_file}' has been validated successfully")

    return 0


if __name__ == "__main__":
    sys.exit(main())
