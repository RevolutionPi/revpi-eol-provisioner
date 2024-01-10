"""Tests regarging the yaml device configuration files."""
import glob

import pytest

from revpi_provisioning.config import EOLConfigException, load_config

revpi_device_configs = sorted(glob.glob("revpi_provisioning/devices/*.yaml"))


@pytest.mark.parametrize("config", revpi_device_configs)
def test_yaml_file(config: str) -> None:
    """Validate YAML configuration file by loading it.

    Parameters
    ----------
    config : str
        yaml configuration file
    """
    try:
        load_config(config, absolute_path=True)
    except EOLConfigException as ce:
        pytest.fail(f"Failed to validate device configuration file: {ce}", 1)
