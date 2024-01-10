"""Network interfaces which are connected via USB."""
import subprocess

from revpi_provisioning.network import NetworkInterface, NetworkEEPROMException
from revpi_provisioning.network.utils import find_usb_ethernet_device_name


class USBNetworkInterface(NetworkInterface):
    """Base class for USB network interfaces."""

    def __init__(
        self, usb_device_path: str, has_eeprom: bool = False, eeprom_tool: str = None
    ) -> None:
        super().__init__(usb_device_path, has_eeprom)

        self.eeprom_tool = eeprom_tool

    def _write_eeprom(self, mac_address: str) -> None:
        interface_name = find_usb_ethernet_device_name(self.path)
        cmd = [self.eeprom_tool, interface_name, str(mac_address)]

        try:
            subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            log = e.stdout.decode()
            raise NetworkEEPROMException(
                f"Failed to write EEPROM for network interface '{interface_name}': {e}\n{log}"
            ) from e


class LAN95XXNetworkInterface(USBNetworkInterface):
    """Microchip LAN95XX network interface class."""

    def __init__(self, usb_device_path: str, has_eeprom: bool = False) -> None:
        super().__init__(usb_device_path, has_eeprom, "/usr/sbin/lan95xx-set-mac")


class LAN78XXNetworkInterface(USBNetworkInterface):
    """Microchip LAN78XX network interface class."""

    def __init__(self, usb_device_path: str, has_eeprom: bool = False) -> None:
        super().__init__(usb_device_path, has_eeprom, "/usr/sbin/lan78xx-set-mac")
