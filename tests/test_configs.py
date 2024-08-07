"""Test the yaml device configuration files."""

import glob
import os
import re

import pytest
import yamllint.config
import yamllint.linter

from revpi_provisioning.config import EOLConfigException, load_config

revpi_device_configs = sorted(glob.glob("revpi_provisioning/devices/*.yaml"))


def is_integer(value: object) -> bool:
    """Check if provided value is an integer.

    Parameters
    ----------
    value : object
        value to check

    Returns
    -------
    bool
        True if value is an integer, False if not
    """
    try:
        float(value)
    except ValueError:
        return False
    else:
        return float(value).is_integer()


def is_valid_filename(filename: str) -> bool:
    """Check if filename is product number with revision and yaml suffix.

    Parameters
    ----------
    filename : str
        filename

    Returns
    -------
    bool
        True if filename is valid, else False
    """
    return re.match(r"^PR\d{6}R\d{2}.yaml$", filename)


@pytest.mark.parametrize("config", revpi_device_configs)
class TestConfig:
    """Test wrapper which is applied to each yaml configuration."""

    def test_yaml_filename(self, config: str) -> None:
        """Test filename of YAML configuration file..

        Parameters
        ----------
        config : str
            yaml configuration file
        """
        name = os.path.basename(config)

        if not is_valid_filename(name):
            pytest.fail(f"Filename '{name}' does not match product id pattern")

    def test_yaml_lint(self, config: str) -> None:
        """Validate YAML configuration with yamllint.

        Parameters
        ----------
        config : str
            yaml configuration file
        """
        yaml_config = yamllint.config.YamlLintConfig("extends: default")
        with open(config, "r") as fd:
            problems = list(yamllint.linter.run(fd, yaml_config))
            num_problems = len(problems)

            if num_problems:
                message = f"yamllint reports {num_problems} problem"
                message += "s" if num_problems > 1 else ""
                message += "\n"

                for problem in problems:
                    message += f"- line {problem.line}: {problem.desc}"

                pytest.fail(message)

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
                pytest.fail("Write protect gpiochip does not match pattern: " + wp_gpiochip)
        except EOLConfigException as ce:
            pytest.fail(f"Failed to validate device configuration file: {ce}", 1)
