#!/usr/bin/env python3

from revpi_provisioning.hat import HatEEPROM
from revpi_provisioning.network import find_interface_class
from revpi_provisioning.network.usb import LAN95XXNetworkInterface
from revpi_provisioning.revpi import RevPi

####################### FROM TEMPLATE - BEGIN################################

# define product
revpi = RevPi(100359, 1)

# define HAT EEPROM
revpi.hat_eeprom = HatEEPROM(22)

# define network interfaces (with attached EEPROMs)
revpi.network_interfaces.append(LAN95XXNetworkInterface("1-5.1.2:1.0", True))
revpi.network_interfaces.append(LAN95XXNetworkInterface("1-5.1.2:1.0", True))

# ... or define network interfaces and determine class from type string (eg. with yaml templates or arparse)
LAN = find_interface_class("lan87xx")
revpi.network_interfaces.append(LAN('0000:00:14.3', True))

####################### FROM TEMPLATE - END #################################

# device specific parts (eg. in a loop)
revpi.write_hat_eeprom("revpi-hat-PR100362R01.bin")
print(revpi.write_mac_addresses('c83ea7001234'))
