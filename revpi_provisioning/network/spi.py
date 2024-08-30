# SPDX-FileCopyrightText: 2022-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Network interfaces which are connected via SPI."""

from revpi_provisioning.network import NetworkInterface


class KSZ8851NetworkInterface(NetworkInterface):
    """Microchip KSZ8851 network interface class."""

    def __init__(self, path: str, has_eeprom: bool = False) -> None:
        super().__init__(path, has_eeprom)
