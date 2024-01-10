"""Network interfaces which are connected via PCIe."""
from revpi_provisioning.network import NetworkInterface
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
        cmd = [self.eeprom_tool, interface_name, mac_address]

        print(cmd)


class LAN87XXNetworkInterface(PCIeNetworkInterface):
    """Microchip LAN87XX network interface class."""

    def __init__(self, pcie_device_path: str, has_eeprom: bool = False) -> None:
        super().__init__(pcie_device_path, has_eeprom, "lan87xx-set-mac")
