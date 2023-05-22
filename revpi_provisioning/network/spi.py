from revpi_provisioning.network import NetworkInterface


class KSZ8851NetworkInterface(NetworkInterface):
    def __init__(self, path, has_eeprom: bool = False) -> None:
        super().__init__(path, has_eeprom)
