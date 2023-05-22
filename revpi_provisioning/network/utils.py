import glob


class NetworkInterfaceNotFoundException(Exception):
    pass


def find_usb_ethernet_device_name(usb_device_path: str):
    return find_ethernet_device_name("usb", usb_device_path)


def find_pci_ethernet_device_name(pci_device_path: str):
    return find_ethernet_device_name("pci", pci_device_path)


def find_ethernet_device_name(bus: str, device_path: str):
    path = f"/sys/bus/{bus}/devices/{device_path}/net/*"
    names = glob.glob(path)

    if len(names) == 0:
        raise NetworkInterfaceNotFoundException(device_path)

    name = names[0].split("/")[-1]

    return name
