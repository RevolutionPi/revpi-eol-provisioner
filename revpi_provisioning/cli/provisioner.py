#!/usr/bin/env python3
import argparse

from revpi_provisioning.cli.utils import error
from revpi_provisioning.config import EOLConfigException, load_config
from revpi_provisioning.hat import HatEEPROM
from revpi_provisioning.network import find_interface_class
from revpi_provisioning.revpi import RevPi
from revpi_provisioning.utils import extract_product


def parse_args() -> tuple:
    parser = argparse.ArgumentParser(description="Provision RevPi hardware")

    parser.add_argument(
        'product_number',
        metavar='product-number',
        help='product number of target device in format PRxxxxxxRxx')
    parser.add_argument(
        'mac_address',
        metavar='mac-address',
        help='first MAC address of target device')
    parser.add_argument(
        'eep_image',
        metavar='eep-image',
        help='path to eep-image file to be written')

    args = parser.parse_args()

    return args.product_number, args.mac_address, args.eep_image


if __name__ == "__main__":
    product, mac, image_path = parse_args()

    try:
        configuration = load_config(product)

        revpi = RevPi(*extract_product(product))

        # add HAT EEPROM if specified in config file
        if "hat_eeprom" in configuration:
            revpi.hat_eeprom = HatEEPROM(
                configuration["hat_eeprom"]["wp_gpio"])

        # add network interfaces from config file
        for interface_config in configuration.get("network_interfaces", []):
            # determine current interface class by type lookup
            interface_class = find_interface_class(interface_config["type"])

            interface = interface_class(
                interface_config["path"],
                interface_config.get("eeprom", False)
            )

            revpi.network_interfaces.append(interface)

        # write HAT EEPROM with specified image
        revpi.write_hat_eeprom(image_path)

        # write mac addresses (and other default values) to ethernet EEPROMs
        print(revpi.write_mac_addresses(mac))
    except EOLConfigException as ce:
        error(ce, 1)
