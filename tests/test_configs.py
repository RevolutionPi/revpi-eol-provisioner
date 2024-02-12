"""Test the yaml device configuration files."""
import glob

import pytest
import re

from revpi_provisioning.config import EOLConfigException, load_config

revpi_device_configs = sorted(glob.glob("revpi_provisioning/devices/*.yaml"))


def is_integer(value: object) -> bool:
    try:
        float(value)
    except ValueError:
        return False
    else:
        return float(value).is_integer()


@pytest.mark.parametrize("config", revpi_device_configs)
class TestConfig:
    def test_yaml_file(self, config: str) -> None:
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

    def test_network_interfaces(self, config: str) -> None:
        """Validate YAML configuration file by loading it.

        Parameters
        ----------
        config : str
            yaml configuration file
        """
        try:
            config = load_config(config, absolute_path=True)

            if "network_interfaces" not in config:
                pytest.fail("No network interfaces defined")

            if not len(config["network_interfaces"]):
                pytest.fail("A RevPi must have at least one network interface")
        except EOLConfigException as ce:
            pytest.fail(f"Failed to validate device configuration file: {ce}", 1)

    def test_eeprom(self, config: str) -> None:
        """Validate YAML configuration file by loading it.

        Parameters
        ----------
        config : str
            yaml configuration file
        """
        try:
            config = load_config(config, absolute_path=True)

            if "hat_eeprom" not in config:
                return

            wp_gpio = config["hat_eeprom"].get("wp_gpio", None)
            if wp_gpio is None:
                pytest.fail("Missing write protect gpio in hat_eeprom section")
            elif not is_integer(wp_gpio):
                pytest.fail("Write protect gpio must be an integer")

            wp_gpiochip = config["hat_eeprom"].get("wp_gpiochip", None)
            if wp_gpiochip is None:
                pytest.fail("Missing write protect gpiochip in hat_eeprom section")
            elif not re.match(r"^gpiochip\d+$", wp_gpiochip):
                pytest.fail(
                    "Write protect gpiochip does not match pattern: " + wp_gpiochip
                )
        except EOLConfigException as ce:
            pytest.fail(f"Failed to validate device configuration file: {ce}", 1)
