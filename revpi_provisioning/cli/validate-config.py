#!/usr/bin/env python3

import argparse
import os

import yaml
from revpi_provisioning.cli.utils import error
from revpi_provisioning.config import config_schema
from schema import SchemaError


parser = argparse.ArgumentParser(
    description="Validate device configuration file")
parser.add_argument("config", metavar="device-configuration-file")

args = parser.parse_args()

device_config_file = args.config
if not os.path.exists(device_config_file):
    error(
        f"Device configuration file '{device_config_file}' does not exist", 1)

with open(device_config_file, "r") as stream:
    try:
        configuration = yaml.safe_load(stream)
    except yaml.YAMLError as ye:
        error(f"Could not parse device configuration file: {ye}", 2)

try:
    config_schema.validate(configuration)
except SchemaError as se:
    error(f"Schema error in device configuration file: {se}", 3)

print("Device configuration file validated succesfully")
