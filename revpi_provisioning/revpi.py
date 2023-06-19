from __future__ import annotations
from typing import Union

import yaml

from revpi_provisioning.hat import HatEEPROM
from revpi_provisioning.network import NetworkInterface
from revpi_provisioning.utils import MacAddress


class RevPi:
    def __init__(self, product_id: int, product_revision: int) -> None:
        self.product_id: int = product_id
        self.product_revision: int = product_revision
        self.hat_eeprom: HatEEPROM = None
        self.network_interfaces: list[NetworkInterface] = []

    def write_hat_eeprom(self, eeprom_image: Union[str, bytes]) -> None:
        if self.hat_eeprom is not None:
            self.hat_eeprom.write(eeprom_image)

    def clear_hat_eeprom(self) -> None:
        if self.hat_eeprom is not None:
            self.hat_eeprom.clear_content()

    def dump_hat_eeprom(self, output_file: str) -> None:
        if self.hat_eeprom is not None:
            self.hat_eeprom.dump(output_file)

    def write_mac_addresses(self, first_mac_address: str = None) -> list[str]:
        mac_address = MacAddress(first_mac_address)
        mac_addresses = []

        for interface in self.network_interfaces:
            interface.set_mac_address(mac_address)
            mac_addresses.append(mac_address)

            mac_address = mac_address + 1

        return mac_addresses

    @staticmethod
    def from_yaml(catalog_file: str) -> RevPi:
        with open(catalog_file, "r") as stream:
            try:
                data = yaml.safe_load(stream)
            except yaml.YAMLError as exc:
                print(exc)

        instance = RevPi(data["product_id"], data["product_revision"])

        for interface_config in data.get("network_interfaces", []):
            network_interface = NetworkInterface.from_config(interface_config)

            instance.network_interfaces.append(network_interface)

        return instance
