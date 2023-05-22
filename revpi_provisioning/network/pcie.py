from revpi_provisioning.network import NetworkInterface
from revpi_provisioning.network.utils import find_pci_ethernet_device_name


class PCIeNetworkInterface(NetworkInterface):
    def __init__(
        self, pcie_device_path: str, has_eeprom: bool = False, eeprom_tool: str = None
    ) -> None:
        super().__init__(pcie_device_path, has_eeprom)

        self.eeprom_tool = eeprom_tool

    def _write_eeprom(self, mac_address: str):
        interface_name = find_pci_ethernet_device_name(self.path)
        cmd = [self.eeprom_tool, interface_name, mac_address]

        print(cmd)


class LAN87XXNetworkInterface(PCIeNetworkInterface):
    def __init__(self, pcie_device_path: str, has_eeprom: bool = False) -> None:
        super().__init__(pcie_device_path, has_eeprom, "lan87xx-set-mac")
