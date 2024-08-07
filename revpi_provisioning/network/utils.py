"""Network related utilities."""

import glob


class NetworkInterfaceNotFoundException(Exception):
    """Exception which is raised if the network interface can't be found."""

    pass


def find_usb_ethernet_device_name(usb_device_path: str) -> str:
    """Find USB network interface name (eg. eth0 ...) from device path.

    Parameters
    ----------
    usb_device_path : str
        usb device path

    Returns
    -------
    str
        interface name
    """
    return find_ethernet_device_name("usb", usb_device_path)


def find_pci_ethernet_device_name(pci_device_path: str) -> str:
    """Find PCI(e) network interface name (eg. eth0 ...) from device path.

    Parameters
    ----------
    pci_device_path : str
        pci(e) device path

    Returns
    -------
    str
        interface name
    """
    return find_ethernet_device_name("pci", pci_device_path)


def find_ethernet_device_name(bus: str, device_path: str) -> str:
    """Find network interface name (eg. eth0 ...) by bus and device path.

    Parameters
    ----------
    bus : str
        bus in sysfs
    device_path : str
        device path in sysfs

    Returns
    -------
    str
        interface name

    Raises
    ------
    NetworkInterfaceNotFoundException
        indicates that the network interface cannot be found
    """
    path = f"/sys/bus/{bus}/devices/{device_path}/net/*"
    names = glob.glob(path)

    if len(names) == 0:
        raise NetworkInterfaceNotFoundException(device_path)

    name = names[0].split("/")[-1]

    return name
