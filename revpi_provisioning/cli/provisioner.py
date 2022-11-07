#!/usr/bin/env python3
import os.path
import pathlib

import yaml
from revpi_provisioning.cli.utils import error
from revpi_provisioning.config import config_schema
from revpi_provisioning.hat import HatEEPROM
from revpi_provisioning.network import find_interface_class
from revpi_provisioning.revpi import RevPi
from revpi_provisioning.utils import extract_product
from schema import SchemaError

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Provision RevPi hardware")
    parser.add_argument('product_number', metavar='product-number',
                        help='product number of target device in format PRxxxxxxRxx')
    parser.add_argument('mac_address', metavar='mac-address',
                        help='first MAC address of target device')
    parser.add_argument('eep_image', metavar='eep-image',
                        help='path to eep-image file to be written')

    args = parser.parse_args()
    product = args.product_number
    mac = args.mac_address
    image_path = args.eep_image

    basepath = pathlib.Path(__file__).parent.resolve()
    device_config_file = f"{basepath}/../devices/{product}.yaml"
    if not os.path.exists(device_config_file):
        error(
            f"Device configuration file '{device_config_file}' does not exist", 1)

    with open(device_config_file, "r") as stream:
        try:
            configuration = yaml.safe_load(stream)
        except yaml.YAMLError as ye:
            error(f"Could not parse device configuration file: {ye}", 2)

    try:
        config_schema.validate(configuration)
    except SchemaError as se:
        error(f"Schema error in device configuration file: {se}", 3)

    revpi = RevPi(*extract_product(product))

    # add HAT EEPROM if specified in config file
    if "hat_eeprom" in configuration:
        revpi.hat_eeprom = HatEEPROM(configuration["hat_eeprom"]["wp_gpio"])

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
