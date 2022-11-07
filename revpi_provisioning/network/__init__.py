
import importlib

NETWORK_INTERFACE_TYPES = {
    "lan95xx": ("usb", "LAN95XXNetworkInterface"),
    "lan78xx": ("usb", "LAN78XXNetworkInterface"),
    "lan87xx": ("pcie", "LAN87XXNetworkInterface"),
    "ksz8851": ("spie", "KSZ8851NetworkInterface"),
}


class NetworkEEPROMException(Exception):
    pass


class InvalidNetworkInterfaceTypeString(Exception):
    pass


def find_interface_class(interface_type: str):
    interface_type = interface_type.lower()

    if interface_type not in NETWORK_INTERFACE_TYPES:
        raise InvalidNetworkInterfaceTypeString(interface_type)

    (module_name, class_name) = NETWORK_INTERFACE_TYPES.get(interface_type)

    module = importlib.import_module(f"{__name__}.{module_name}")
    cls = getattr(module, class_name)

    return cls


class NetworkInterface:
    def __init__(self, path: str, has_eeprom: bool = False) -> None:
        self.path = path
        self.has_eeprom = has_eeprom

    def set_mac_address(self, mac_address: str):
        if self.has_eeprom:
            self._write_eeprom(mac_address)

    def _write_eeprom(self, mac_address: str):
        raise NotImplementedError()
