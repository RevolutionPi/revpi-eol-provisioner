class HatEEPROM:
    def __init__(self,  write_protect_gpio: int) -> None:
        self.write_protect_gpio = write_protect_gpio

    def _write_image(self, eeprom_image: str):
        print(f"write hat eeprom with image '{eeprom_image}'")
        pass

    def _load_dtoverlay(self):
        print("load dtoverlay for eeprom")
        pass

    def _write_protect(self, state: bool):
        print(f"set eeprom write protect: {state}")
        pass

    def _verify_image(self):
        print("verify image")
        pass

    def write(self, eeprom_image: str):
        self._write_protect(False)
        self._load_dtoverlay()
        self._write_image(eeprom_image)
        self._verify_image()
        self._write_protect(True)
