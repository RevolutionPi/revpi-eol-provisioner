"""Network interfaces which are located on the SOM itself."""

from revpi_provisioning.network import NetworkInterface


class BoardNetworkInterface(NetworkInterface):
    """Base class for onboard network interfaces."""

    def __init__(self, device_path: str, has_eeprom: bool = False, eeprom_tool: str = None) -> None:
        super().__init__(device_path, has_eeprom)

        self.eeprom_tool = eeprom_tool


class BCM2711NetworkInterface(BoardNetworkInterface):
    """BCM2711 network interface class (eg. Raspberry Pi CM4)."""

    def __init__(self, path: str = "", has_eeprom: bool = False) -> None:
        super().__init__(path, has_eeprom)

    def _write_eeprom(self, mac_address: str) -> None:
        """Do nothing, when mac address is written (no eeprom support for BCM2711)."""
        # Nothing to do here
        pass


class RP1NetworkInterface(BoardNetworkInterface):
    """RP1 network interface class (eg. Raspberry Pi 5)."""

    def __init__(self, path: str = "", has_eeprom: bool = False) -> None:
        super().__init__(path, has_eeprom)

    def _write_eeprom(self, mac_address: str) -> None:
        """Do nothing, when mac address is written (no eeprom support for RP1 based interfaces)."""
        # Nothing to do here
        pass
