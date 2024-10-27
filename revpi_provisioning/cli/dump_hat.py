# SPDX-FileCopyrightText: 2023-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Dump HAT eeprom contents CLI command."""

import argparse
import sys

import revpi_provisioning.cli.utils
from revpi_provisioning.cli.utils import error, verboseprint
from revpi_provisioning.config import EOLConfigException, load_config
from revpi_provisioning.hat import (
    DEFAULT_GPIO_CHIP,
    DEFAULT_OVERLAY,
    HatEEPROM,
    HatEEPROMWriteException,
)
from revpi_provisioning.revpi import RevPi
from revpi_provisioning.utils import extract_product


def parse_args() -> tuple:
    """Parse CLI args.

    Returns
    -------
    tuple
        CLI args
    """
    parser = argparse.ArgumentParser(description="Clear RevPi HAT EEPROM")

    parser.add_argument(
        "product_number",
        metavar="product-number",
        help="product number of target device in format PRxxxxxxRxx",
    )
    parser.add_argument(
        "output_file",
        metavar="output-file",
        help="output file where the HAT eeprom contents are written to",
    )
    parser.add_argument("-v", "--verbose", action="store_true", default=False, required=False)
    args = parser.parse_args()

    return args.product_number, args.output_file, args.verbose


def main() -> int:
    """Run the actual program logic.

    Returns
    -------
    int
        return code of the program
    """
    product, output_file, verbose = parse_args()
    revpi_provisioning.cli.utils.verbose = verbose

    try:
        verboseprint("Loading device configuration ... ", end="")
        configuration = load_config(product)
        verboseprint("OK")

        revpi = RevPi(*extract_product(product))

        # add HAT EEPROM if specified in config file
        if "hat_eeprom" in configuration:
            revpi.hat_eeprom = HatEEPROM(
                configuration["hat_eeprom"]["wp_gpio"],
                configuration["hat_eeprom"].get("wp_gpio_chipname", DEFAULT_GPIO_CHIP),
                overlay=configuration["hat_eeprom"].get("overlay", DEFAULT_OVERLAY),
            )

        if revpi.hat_eeprom:
            verboseprint("Dump HAT EEPROM ... ", end="")
            revpi.dump_hat_eeprom(output_file)
            verboseprint("OK")

    except EOLConfigException as ce:
        print("FAILED")
        error(f"Could not load configuration: {ce}", 1)
    except HatEEPROMWriteException as he:
        print("FAILED")
        error(f"Could not dump HAT EEPROM: {he}", 3)


if __name__ == "__main__":
    sys.exit(main())
