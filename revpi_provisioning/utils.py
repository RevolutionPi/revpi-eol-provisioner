# SPDX-FileCopyrightText: 2022-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Utilities for device provisioning."""

import re


class InvalidMacAddressFormat(Exception):
    """Exception which is raised on an invalid mac address format."""

    pass


class InvalidProductNumberException(Exception):
    """Exception which is raised on an invalid product number format."""

    def __init__(self, product_number: str) -> None:
        """Create InvalidProductNumberException instance.

        Parameters
        ----------
        product_number : str
            product number with invalid format
        """
        self.product_number = product_number

        super().__init__(f"Could not parse product number: {product_number}")


class MacAddress:
    """MAC address representation class with some helper methods."""

    def __init__(self, mac: str) -> None:
        """Create MacAddress instance.

        Parameters
        ----------
        mac : str
            mac address

        Raises
        ------
        InvalidMacAddressFormat
            Exception if mac address format is invalid
        """
        mac = mac.lower()
        mac = mac.replace(":", "")
        mac = mac.replace("-", "")

        if not re.match(r"[a-f0-9]{12}", mac):
            raise InvalidMacAddressFormat(mac)

        self.__mac = int(mac, 16)

    def __str__(self) -> str:
        """Return a string representation of the mac address."""
        return self.__format_hexstring(self.__mac)

    def __repr__(self) -> str:
        """Return the representation of this instance."""
        return str(self)

    def __add__(self, other: int) -> "MacAddress":
        """Increment mac address with + operator."""
        new_mac = self.__mac + other

        return __class__(self.__format_hexstring(new_mac))

    def __sub__(self, other: int) -> "MacAddress":
        """Decrement mac address with - operator."""
        new_mac = self.__mac - other

        return __class__(self.__format_hexstring(new_mac))

    def __format_hexstring(self, value: int) -> str:
        """Format value as hexstring."""
        return f"{value:x}"

    def __format_with_delimiter(self, delimiter: chr, group_length: int) -> str:
        """Format mac address with delimiter.

        Parameters
        ----------
        delimiter : chr
            delimiter character
        group_length : int
            length of each group

        Returns
        -------
        str
            mac address formated with delimiters
        """
        return delimiter.join(map("".join, zip(*[iter(str(self))] * group_length, strict=True)))

    @property
    def format_colon(self) -> str:
        """Return mac address with colon format (eg. aa:bb:cc:dd:ee:ff).

        Returns
        -------
        str
            formated mac address
        """
        return self.__format_with_delimiter(":", 2)

    @property
    def format_dash(self) -> str:
        """Return mac address with dash format (eg. aa-bb-cc-dd-ee-ff).

        Returns
        -------
        str
            formated mac address
        """
        return self.__format_with_delimiter("-", 4)

    @property
    def oui(self) -> str:
        """Return oui part of mac address."""
        return str(self)[:6]

    @property
    def nic(self) -> str:
        """Return nic part of mac address."""
        return str(self)[6:]


def extract_product(product_number: str) -> tuple:
    """Extract product id and revision from string (format: PR123456R00).

    Parameters
    ----------
    product_number : str
        product number with revision

    Returns
    -------
    tuple
        product_id, product_revision

    Raises
    ------
    InvalidProductNumberException
        _description_
    """
    product_match = re.match(
        r"^(?:PR(?P<pr>\d{6})|FE(?P<fe>\d{4}))R(?P<rev>\d{2})$", product_number, re.IGNORECASE
    )

    if product_match:
        groups = product_match.groupdict()
        product_id = groups["pr"] or groups["fe"]
        product_revision = groups["rev"]
        return (product_id, product_revision)

    raise InvalidProductNumberException(product_number)
