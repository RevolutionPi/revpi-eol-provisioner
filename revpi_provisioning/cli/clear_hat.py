#!/usr/bin/env python3

import argparse
import sys

from revpi_provisioning.cli.utils import error
from revpi_provisioning.config import EOLConfigException, load_config
from revpi_provisioning.hat import HatEEPROM, HatEEPROMWriteException
from revpi_provisioning.revpi import RevPi
from revpi_provisioning.utils import extract_product


def parse_args() -> tuple:
    parser = argparse.ArgumentParser(description="Clear RevPi HAT EEPROM")

    parser.add_argument(
        "product_number",
        metavar="product-number",
        help="product number of target device in format PRxxxxxxRxx",
    )
    args = parser.parse_args()

    return args.product_number


def main() -> int:
    product = parse_args()

    print(f"Starting device provisioning for product '{product}'")

    try:
        print("Loading device configuration ... ", end="")
        configuration = load_config(product)
        print("OK")

        revpi = RevPi(*extract_product(product))

        # add HAT EEPROM if specified in config file
        if "hat_eeprom" in configuration:
            revpi.hat_eeprom = HatEEPROM(
                configuration["hat_eeprom"]["wp_gpio"],
                configuration["hat_eeprom"].get("wp_gpio_chipname", "gpiochip0"),
            )

        if revpi.hat_eeprom:
            print("Clear HAT EEPROM ... ", end="")
            revpi.clear_hat_eeprom()
            print("OK")

    except EOLConfigException as ce:
        print("FAILED")
        error(f"Could not load configuration: {ce}", 1)
    except HatEEPROMWriteException as he:
        print("FAILED")
        error(f"Could not clear HAT EEPROM: {he}", 3)


if __name__ == "__main__":
    sys.exit(main())
