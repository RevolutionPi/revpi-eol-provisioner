"""Clear HAT eeprom CLI command."""

import argparse
import sys

import revpi_provisioning.cli.utils
from revpi_provisioning.cli.utils import error, verboseprint
from revpi_provisioning.config import EOLConfigException, load_config
from revpi_provisioning.hat import HatEEPROM, HatEEPROMWriteException
from revpi_provisioning.network import (
    InvalidNetworkInterfaceTypeString,
    NetworkEEPROMException,
    find_interface_class,
)
from revpi_provisioning.network.utils import NetworkInterfaceNotFoundException
from revpi_provisioning.revpi import RevPi
from revpi_provisioning.utils import extract_product


def parse_args() -> tuple:
    """Parse CLI args.

    Returns
    -------
    tuple
        CLI args
    """
    parser = argparse.ArgumentParser(description="Provision RevPi hardware")

    parser.add_argument(
        "product_number",
        metavar="product-number",
        help="product number of target device in format PRxxxxxxRxx",
    )
    parser.add_argument(
        "mac_address", metavar="mac-address", help="first MAC address of target device"
    )
    parser.add_argument(
        "eep_image", metavar="eep-image", help="path to eep-image file to be written"
    )
    parser.add_argument("-v", "--verbose", action="store_true", default=False, required=False)

    args = parser.parse_args()

    return args.product_number, args.mac_address, args.eep_image, args.verbose


def main() -> int:
    """Run the actual program logic.

    Returns
    -------
    int
        return code of the program
    """
    product, mac, image_path, verbose = parse_args()
    revpi_provisioning.cli.utils.verbose = verbose

    verboseprint(f"Starting device provisioning for product '{product}'")

    try:
        verboseprint("Loading device configuration ... ", end="")
        configuration = load_config(product)
        verboseprint("OK")

        revpi = RevPi(*extract_product(product))

        # add HAT EEPROM if specified in config file
        if "hat_eeprom" in configuration:
            verboseprint(
                f"Found HAT EEPROM definition in config file. Will write image '{image_path}'"
            )
            revpi.hat_eeprom = HatEEPROM(
                configuration["hat_eeprom"]["wp_gpio"],
                configuration["hat_eeprom"].get("wp_gpio_chipname", "gpiochip0"),
            )

        verboseprint(f"Registering network interfaces. Base mac address will be '{mac}'")

        for index, interface_config in enumerate(configuration.get("network_interfaces", [])):
            interface_path = interface_config["path"]
            interface_type = interface_config["type"]

            # determine current interface class by type lookup
            interface_class = find_interface_class(interface_type)

            line = f"  Ethernet {index}: type={interface_type} "
            if interface_path:
                line += f"path={interface_path} "
            line += "... "

            verboseprint(line, end="")

            interface = interface_class(interface_path, interface_config.get("eeprom", False))

            revpi.network_interfaces.append(interface)

            verboseprint("OK")

        if revpi.hat_eeprom:
            verboseprint("Writing HAT EEPROM ... ", end="")
            revpi.write_hat_eeprom(image_path)
            verboseprint("OK")

        verboseprint("Writing mac addresses ... ", end="")
        mac_addresses = revpi.write_mac_addresses(mac)
        verboseprint("OK")
        verboseprint(f"Successfully wrote {len(mac_addresses)} mac addresses")
    except EOLConfigException as ce:
        print("FAILED")
        error(f"Could not load configuration: {ce}", 1)
    except NetworkInterfaceNotFoundException as nie:
        print("FAILED")
        error(f"Could not found network interface: {nie}", 2)
    except HatEEPROMWriteException as he:
        print("FAILED")
        error(f"Could not write image to HAT EEPROM: {he}", 3)
    except (NetworkEEPROMException, InvalidNetworkInterfaceTypeString) as ne:
        print("FAILED")
        error(f"Could not write mac address: {ne}", 4)


if __name__ == "__main__":
    sys.exit(main())
