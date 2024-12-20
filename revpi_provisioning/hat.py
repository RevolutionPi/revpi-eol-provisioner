# SPDX-FileCopyrightText: 2022-2024 KUNBUS GmbH
#
# SPDX-License-Identifier: GPL-2.0-or-later

"""HAT eeprom related stuff."""

import hashlib
import os
import subprocess
import time
import glob
from typing import Optional, Union

import gpiod

DEFAULT_GPIO_CHIP = "gpiochip0"
DEFAULT_OVERLAY = "revpi-hat-eeprom"
DEFAULT_EEPROM_PATHS = ["/sys/bus/i2c/devices/?-0050/eeprom", "/sys/bus/i2c/devices/??-0050/eeprom"]


class HatEEPROMWriteException(Exception):
    """Exception which is raised if a there is a problem with writing the HAT eeprom content."""

    def __init__(self, message: str) -> None:
        super().__init__(f"RevPi HAT EEPROM: {message}")


class HatEEPROM:
    """HAT eeprom representation class."""

    def __init__(
        self,
        write_protect_gpio: int,
        gpio_chip: str = DEFAULT_GPIO_CHIP,
        base_eeprom: Optional[str] = None,
        overlay: str = DEFAULT_OVERLAY,
    ) -> None:
        self.write_protect_gpio = write_protect_gpio
        self.gpio_chip = gpio_chip
        self._base_eeprom = base_eeprom
        self._overlay = overlay

        self.__write_protect_gpio_line = None

    @property
    def base_eeprom(self) -> str:
        """Base path of the HAT eeprom in sysfs."""
        if self._base_eeprom is not None:
            paths = [self._base_eeprom]
        else:
            paths = DEFAULT_EEPROM_PATHS

        for path in paths:
            eeprom_path = glob.glob(path)
            if eeprom_path:
                # take first match
                break

        if not eeprom_path:
            raise HatEEPROMWriteException("Unable to determine HAT eeprom i2c path")

        return eeprom_path[0]

    def _init_gpio(self) -> None:
        try:
            chip = gpiod.Chip(self.gpio_chip)

            self.__write_protect_gpio_line = chip.get_line(self.write_protect_gpio)
            self.__write_protect_gpio_line.request(
                consumer="eol-provisioner", type=gpiod.LINE_REQ_DIR_OUT
            )
        except OSError as e:
            raise HatEEPROMWriteException(
                f"Failed to set initialize write protection gpio: {e}"
            ) from e

    def _read_image_file(self, eeprom_image: Union[str, bytes], length: int = None) -> bytes:
        """Read image from file.

        If eeprom image is already of type bytes,
        the data is passed through and no read attempt ins done.

        Parameters
        ----------
        eeprom_image : Union[str, bytes]
            Image file or image content as bytes
        length : int, optional
            Number of bytes to read from image file

        Returns
        -------
        bytes
            image content
        """
        if isinstance(eeprom_image, str):
            with open(eeprom_image, "rb") as fh:
                data = fh.read(length)
        else:
            data = eeprom_image

        return data

    def _write_image(self, eeprom_image: Union[str, bytes], length: int = None) -> None:
        """Write image to HAT eeprom.

        Parameters
        ----------
        eeprom_image : Union[str, bytes]
            Image file or image content as bytes
        length : int, optional
            Number of bytes to read from image file

        Raises
        ------
        HatEEPROMWriteException
            Unable to write HAT eeprom image
        """
        try:
            eeprom_length = os.path.getsize(self.base_eeprom)

            data = self._read_image_file(eeprom_image, length)

            if len(data) > eeprom_length:
                raise Exception("Image file is too big for EEPROM")

            with open(self.base_eeprom, "wb") as file_eeprom:
                file_eeprom.write(data)
        except Exception as exc:
            raise HatEEPROMWriteException(f"Failed to write image to EEPROM: {exc}") from exc

    def _loaded_overlays(self) -> list:
        overlays = []

        try:
            process = subprocess.run(["dtoverlay", "-l"], check=True, capture_output=True)
            lines = process.stdout.decode("utf-8").split("\n")

            # skip first line (headline)
            for line in lines[1:]:
                if ":" not in line:
                    continue

                (_, name) = line.replace(" ", "").split(":")
                overlays.append(name)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise HatEEPROMWriteException(f"Failed to list loaded overlays: {e}") from e

        return overlays

    def _load_dtoverlay(self, wait_afterwards: int = 0.5) -> None:
        if self._overlay in self._loaded_overlays():
            # overlay already loaded, no need to do it again
            return

        try:
            subprocess.check_call(["dtoverlay", self._overlay])
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise HatEEPROMWriteException(f"Failed to load overlay '{self._overlay}': {e}") from e

        time.sleep(wait_afterwards)

    def _write_protect(self, state: bool) -> None:
        if self.__write_protect_gpio_line is None:
            # initialize gpio as output if not done yet
            self._init_gpio()

        try:
            self.__write_protect_gpio_line.set_value(state)
        except OSError as e:
            raise HatEEPROMWriteException(f"Failed to set write protection gpio: {e}") from e

    def _sha256_checksum(self, data: bytes) -> str:
        try:
            sha256_checksum = hashlib.sha256(data).hexdigest()
        except Exception as exc:
            raise HatEEPROMWriteException(
                f"Failed to get SHA256 checksum of HAT eeprom: {exc}"
            ) from exc

        return sha256_checksum

    def _verify_image(self, eeprom_image: Union[str, bytes]) -> None:
        """Verify HAT eeprom against image file or contents.

        Parameters
        ----------
        eeprom_image : Union[str, bytes]
            Image file or image content as bytes

        Raises
        ------
        HatEEPROMWriteException
            Unable to verify image contents
        """
        data_image = self._read_image_file(eeprom_image)
        data_eep = self._read_image_file(self.base_eeprom)

        sha256_eeprom_image = self._sha256_checksum(data_image)
        sha256_eeprom = self._sha256_checksum(data_eep[: len(data_image)])

        if sha256_eeprom != sha256_eeprom_image:
            raise HatEEPROMWriteException(
                "Failed to verify image: sha256 checksum mismatch: "
                + f"{sha256_eeprom} (eeprom) != {sha256_eeprom_image} (image)"
            )

    def write(self, eeprom_image: str) -> None:
        """Write HAT eeprom contents."""
        self._write_protect(False)
        self._load_dtoverlay()
        self._write_image(eeprom_image)
        self._verify_image(eeprom_image)
        self._write_protect(True)

    def clear_content(self) -> None:
        """Clear HAT eeprom contents."""
        self._write_protect(False)
        self._load_dtoverlay()
        self._write_image(b"\xff" * os.path.getsize(self.base_eeprom))
        self._write_protect(True)

    def dump(self, output_file: str) -> None:
        """Dump eeprom contents to file.

        Parameters
        ----------
        output_file : str
            output file where the eeprom content is written to
        """
        self._load_dtoverlay()

        try:
            with open(self.base_eeprom, "rb") as fh, open(output_file, "wb") as fh_output:
                data = fh.read()
                fh_output.write(data)
        except Exception as exc:
            raise HatEEPROMWriteException(
                f"Could not dump EEPROM contents / write to output file: {exc}"
            ) from exc
