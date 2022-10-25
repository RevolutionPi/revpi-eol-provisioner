import hashlib
import os
import subprocess
import time

import gpiod


class HatEEPROMWriteException(Exception):
    def __init__(self, message):
        super().__init__(f"RevPi HAT EEPROM: {message}")


class HatEEPROM:
    def __init__(self,  write_protect_gpio: int, gpio_chip: str = "gpiochip0", base_eeprom: str = "/sys/bus/i2c/devices/11-0050/eeprom") -> None:
        self.write_protect_gpio = write_protect_gpio
        self.gpio_chip = gpio_chip
        self.base_eeprom = base_eeprom

        self.__write_protect_gpio_line = None

    def _init_gpio(self) -> None:
        try:
            chip = gpiod.Chip(self.gpio_chip)

            self.__write_protect_gpio_line = chip.get_line(self.write_protect_gpio)
            self.__write_protect_gpio_line.request(consumer="eol-provisioner", type=gpiod.LINE_REQ_DIR_OUT)
        except OSError as e:
            raise HatEEPROMWriteException(f"Failed to set initialize write protection gpio: {e}")

    def _write_image(self, eeprom_image: str) -> None:
        try:
            with open(eeprom_image, 'rb') as file_eeprom_image, open(self.base_eeprom, 'wb') as file_eeprom:
                file_eeprom.write(file_eeprom_image.read())
        except Exception as e:
            raise HatEEPROMWriteException(f"Failed to write image to EEPROM: {e}")

    def _loaded_overlays(self) -> list:
        overlays = []

        try:
            process  = subprocess.run(['dtoverlay','-l'], check=True, capture_output=True)
            lines = process.stdout.decode("utf-8").split('\n')

            # skip first line (headline)
            for line in lines[1:]:
                if ':' not in line:
                    continue

                (_, name) = line.replace(' ', '').split(':')
                overlays.append(name)
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise HatEEPROMWriteException(
                f"Failed to list loaded overlays: {e}")

        return overlays

    def _load_dtoverlay(self, wait_afterwards: int = 0.5, overlay: str = "revpi-hat-eeprom") -> None:
        if overlay in self._loaded_overlays():
            # overlay already loaded, no need to do it again
            return

        try:
            subprocess.check_call(["dtoverlay", overlay])
        except (subprocess.CalledProcessError, FileNotFoundError) as e:
            raise HatEEPROMWriteException(f"Failed to load overlay '{overlay}': {e}")

        time.sleep(wait_afterwards)

    def _write_protect(self, state: bool) -> None:
        if self.__write_protect_gpio_line is None:
            # initialize gpio as output if not done yet
            self._init_gpio()

        try:
            self.__write_protect_gpio_line.set_value(state)
        except OSError as e:
            raise HatEEPROMWriteException(f"Failed to set write protection gpio: {e}")


    def _sha256_checksum(self, file_name: str, file_length: int = None) -> str:
        try:
            with open(file_name, 'rb') as fh:
                if file_length is None:
                    file_content = fh.read()
                else:
                    file_content = fh.read(file_length)
                sha256_checksum = hashlib.sha256(file_content).hexdigest()
        except Exception as e:
            raise HatEEPROMWriteException(f"Failed to get SHA256 checksum of {file_name}: {e}")

        return sha256_checksum

    def _verify_image(self, eeprom_image: str):
        sha256_eeprom_image = self._sha256_checksum(eeprom_image)
        sha256_eeprom = self._sha256_checksum(self.base_eeprom, os.path.getsize(eeprom_image))

        if sha256_eeprom != sha256_eeprom_image:
            raise HatEEPROMWriteException(
                "Failed to verify image: sha256 checksum mismatch: "
                + f"{sha256_eeprom} (eeprom) != {sha256_eeprom_image} (image)")

    def write(self, eeprom_image: str):
        self._write_protect(False)
        self._load_dtoverlay()
        self._write_image(eeprom_image)
        self._verify_image(eeprom_image)
        self._write_protect(True)
