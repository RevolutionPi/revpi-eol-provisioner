import re


class InvalidMacAddressFormat(Exception):
    pass


class InvalidProductNumberException(Exception):
    def __init__(self, product_number: str):
        self.product_number = product_number

        super().__init__(f"Could not parse product number: {product_number}")


class MacAddress:
    """MAC address representation class with some helper methods"""

    def __init__(self, mac: str) -> None:
        mac = mac.lower()
        mac = mac.replace(':', '')
        mac = mac.replace('-', '')

        if not re.match(r'[a-f0-9]{12}', mac):
            raise InvalidMacAddressFormat(mac)

        self.__mac = int(mac, 16)

    def __str__(self) -> str:
        return self.__format_hexstring(self.__mac)

    def __repr__(self) -> str:
        return str(self)

    def __add__(self, other: int) -> "MacAddress":
        new_mac = self.__mac + other

        return __class__(self.__format_hexstring(new_mac))

    def __sub__(self, other: int) -> "MacAddress":
        new_mac = self.__mac - other

        return __class__(self.__format_hexstring(new_mac))

    def __format_hexstring(self, value: int):
        return f"{value:x}"

    def __format_with_delimiter(self, delimiter: chr, group_length: int) -> str:
        return delimiter.join(map(''.join, zip(*[iter(str(self))]*group_length)))

    @property
    def format_colon(self) -> str:
        return self.__format_with_delimiter(':', 2)

    @property
    def format_dash(self) -> str:
        return self.__format_with_delimiter('-', 4)

    @property
    def oui(self) -> str:
        return str(self)[:6]

    @property
    def nic(self) -> str:
        return str(self)[6:]


def extract_product(product_number: str) -> tuple:
    product_match = re.match(r'^PR([0-9]{6})R([0-9]{2})$', product_number, re.IGNORECASE)

    if product_match:
        return product_match.groups()

    raise InvalidProductNumberException(product_number)
