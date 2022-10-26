from schema import And, Optional, Schema

from revpi_provisioning.network import NETWORK_INTERFACE_TYPES

config_schema = Schema({
    "product_id": And(int, lambda n: 100000 <= n < 1000000),
    "product_revision": And(int, lambda n: 0 <= n < 100),
    Optional("hat_eeprom"): {
        "wp_gpio": int,
        Optional("wp_gpiochip"): str
    },
    "network_interfaces": [
        {
            "type": And(str, lambda t: t in NETWORK_INTERFACE_TYPES.keys(), error="Invalid network interface type"),
            "path": str,
            "eeprom": bool}
    ]
})
