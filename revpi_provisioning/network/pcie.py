# SPDX-FileCopyrightText: 2022-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Network interfaces which are connected via PCIe."""

import subprocess

from revpi_provisioning.network import NetworkEEPROMException, NetworkInterface
from revpi_provisioning.network.utils import find_pci_ethernet_device_name


class PCIeNetworkInterface(NetworkInterface):
    """Base class for PCIe network interfaces."""

    def __init__(
        self, pcie_device_path: str, has_eeprom: bool = False, eeprom_tool: str = None
    ) -> None:
        super().__init__(pcie_device_path, has_eeprom)

        self.eeprom_tool = eeprom_tool

    def _write_eeprom(self, mac_address: str) -> None:
        """Write mac address to eeprom.

        Parameters
        ----------
        mac_address : str
            mac address to write
        """
        interface_name = find_pci_ethernet_device_name(self.path)
        cmd = [self.eeprom_tool, interface_name, str(mac_address)]

        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            log = e.stdout.decode()
            raise NetworkEEPROMException(
                f"Failed to write EEPROM for network interface '{interface_name}': {e}\n{log}"
            ) from e


class LAN743XNetworkInterface(PCIeNetworkInterface):
    """Microchip LAN743X network interface class."""

    def __init__(self, pcie_device_path: str, has_eeprom: bool = False) -> None:
        super().__init__(pcie_device_path, has_eeprom, "lan743x-set-mac")
