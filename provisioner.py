#!/usr/bin/env python3

from revpi_provisioning.hat import HatEEPROM
from revpi_provisioning.network import find_interface_class
from revpi_provisioning.network.usb import LAN95XXNetworkInterface
from revpi_provisioning.revpi import RevPi


def _extract_product(product_number: str) -> tuple:
    product_id = int(product_number[2:8])
    revision = int(product_number[9:11])
    return (product_id, revision)


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

    _extract_product(product)
    ####################### FROM TEMPLATE - BEGIN #############################
    # define product
    revpi = RevPi(*_extract_product(product))

    # define HAT EEPROM
    revpi.hat_eeprom = HatEEPROM(22)

    # define network interfaces (with attached EEPROMs)
    revpi.network_interfaces.append(LAN95XXNetworkInterface("1-5.1.2:1.0", True))
    revpi.network_interfaces.append(LAN95XXNetworkInterface("1-5.1.2:1.0", True))

    # ... or define network interfaces and determine class from type string
    # (eg. with yaml templates or arparse)
    LAN = find_interface_class("lan87xx")
    revpi.network_interfaces.append(LAN('0000:00:14.3', True))
    ####################### FROM TEMPLATE - END ###############################

    # device specific parts (eg. in a loop)
    revpi.write_hat_eeprom(image_path)
    print(revpi.write_mac_addresses(mac))
