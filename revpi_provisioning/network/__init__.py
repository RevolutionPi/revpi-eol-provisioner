"""Network related stuff."""

import importlib

NETWORK_INTERFACE_TYPES = {
    "lan95xx": ("usb", "LAN95XXNetworkInterface"),
    "lan78xx": ("usb", "LAN78XXNetworkInterface"),
    "lan743x": ("pcie", "LAN743XNetworkInterface"),
    "ksz8851": ("spie", "KSZ8851NetworkInterface"),
    "bcm2711": ("board", "BCM2711NetworkInterface"),
    "rp1": ("board", "RP1NetworkInterface"),
}


class NetworkEEPROMException(Exception):
    """Exception which is raised if there are issues regarding the network eeprom."""

    pass


class InvalidNetworkInterfaceTypeString(Exception):
    """Exception which is raised if the network interface type string is invalid."""

    pass


def find_interface_class(interface_type: str) -> "NetworkInterface":
    """Get NetworkInterface implementation by bus type and driver name.

    Parameters
    ----------
    interface_type : str
        interface type (see NETWORK_INTERFACE_TYPES)

    Returns
    -------
    NetworkInterface
        class derived from NetworkInterface with specific implementation

    Raises
    ------
    InvalidNetworkInterfaceTypeString
        an invalid network interface type string was specified
    """
    interface_type = interface_type.lower()

    if interface_type not in NETWORK_INTERFACE_TYPES:
        raise InvalidNetworkInterfaceTypeString(interface_type)

    (module_name, class_name) = NETWORK_INTERFACE_TYPES.get(interface_type)

    module = importlib.import_module(f"{__name__}.{module_name}")
    cls = getattr(module, class_name)

    return cls


class NetworkInterface:
    """Network interface base representation class."""

    def __init__(self, path: str, has_eeprom: bool = False) -> None:
        self.path = path
        self.has_eeprom = has_eeprom

    def set_mac_address(self, mac_address: str) -> None:
        """Set mac address for interface.

        Parameters
        ----------
        mac_address : str
            mac address to set
        """
        if self.has_eeprom:
            self._write_eeprom(mac_address)

    def _write_eeprom(self, mac_address: str) -> None:
        """Abstract method which handles the writing to the eeprom."""
        raise NotImplementedError()
