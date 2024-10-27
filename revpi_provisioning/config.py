# SPDX-FileCopyrightText: 2022-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""Configuration file handling."""

import os
import pathlib

import yaml
from schema import And, Optional, Schema, SchemaError

from revpi_provisioning.network import NETWORK_INTERFACE_TYPES


class EOLConfigException(Exception):
    """Exception which is raised if there is any issue with the config file parsing."""

    pass


config_schema = Schema(
    {
        Optional("hat_eeprom"): {
            "wp_gpio": int,
            Optional("wp_gpiochip"): str,
            Optional("overlay"): And(
                str,
                lambda ovl: ovl in ["revpi-hat-eeprom", "revpi-hat-eeprom-pi5"],
                error="Invalid overlay name for HAT eeprom",
            ),
        },
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
    """Load yaml configuration file from given path.

    Parameters
    ----------
    name : str
        file name
    absolute_path : bool, optional
        if False the file is searched relative to the base path of the python code, by default False

    Returns
    -------
    dict
        configuration object

    Raises
    ------
    EOLConfigException
        Indicates that there where issues during configuration parsing
    """
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
            raise EOLConfigException(f"Could not parse device configuration file: {ye}") from ye

    try:
        config_schema.validate(configuration)
    except SchemaError as se:
        raise EOLConfigException(f"Schema error in device configuration file: {se}") from se

    return configuration
