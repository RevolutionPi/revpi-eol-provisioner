import os
import pathlib

import yaml
from schema import And, Optional, Schema, SchemaError

from revpi_provisioning.network import NETWORK_INTERFACE_TYPES


class EOLConfigException(Exception):
    pass


config_schema = Schema(
    {
        Optional("hat_eeprom"): {"wp_gpio": int, Optional("wp_gpiochip"): str},
        "network_interfaces": [
            {
                "type": And(
                    str,
                    lambda t: t in NETWORK_INTERFACE_TYPES.keys(),
                    error="Invalid network interface type",
                ),
                "path": str,
                "eeprom": bool,
            }
        ],
    }
)


def load_config(name: str, absolute_path: bool = False) -> dict:
    if absolute_path:
        device_config_file = name
    else:
        basepath = pathlib.Path(__file__).parent.resolve()
        device_config_file = f"{basepath}/devices/{name}.yaml"

    if not os.path.exists(device_config_file):
        raise EOLConfigException(
            f"Device configuration file '{device_config_file}' " "does not exist"
        )

    with open(device_config_file, "r") as stream:
        try:
            configuration = yaml.safe_load(stream)
        except yaml.YAMLError as ye:
            raise EOLConfigException(f"Could not parse device configuration file: {ye}")

    try:
        config_schema.validate(configuration)
    except SchemaError as se:
        raise EOLConfigException(f"Schema error in device configuration file: {se}")

    return configuration
