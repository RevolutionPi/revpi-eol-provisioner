# EOL utilities for RevPi devices

The main purpose of this repository is the device provisioning during our EOL tests. Among the provisioner tool other tools exists, which aim to ease different tasks in development / debugging.

## Usage

### Run device provisioning

The wrapper script writes the HAT eeprom contents, sets the mac address and probably other stuff in the future.

```
usage: provisioner.py [-h] product-number mac-address eep-image
provisioner.py: error: the following arguments are required: product-number, mac-address, eep-image
```

### Dump HAT eeprom contents

```
usage: dump_hat.py [-h] product-number output-file
dump_hat.py: error: the following arguments are required: product-number, output-file
```

Example:
```
sudo python3 -m revpi_provisioning.cli.dump_hat PR100383R00 hat.eep
```

### Clear HAT eeprom contents

```
usage: clear_hat.py [-h] product-number
clear_hat.py: error: the following arguments are required: product-number
```

Example:
```
sudo python3 -m revpi_provisioning.cli.clear_hat PR100383R00
```