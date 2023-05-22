from revpi_provisioning.network import NetworkInterface


class BoardNetworkInterface(NetworkInterface):
    def __init__(
        self, device_path: str, has_eeprom: bool = False, eeprom_tool: str = None
    ) -> None:
        super().__init__(device_path, has_eeprom)

        self.eeprom_tool = eeprom_tool


class BCM2711NetworkInterface(BoardNetworkInterface):
    def __init__(self, path: str = "", has_eeprom: bool = False) -> None:
        super().__init__(path, has_eeprom)

    def _write_eeprom(self, mac_address: str):
        # Nothing to do here
        pass
