<details>
<summary>We have moved to GitLab! Read this for more information.</summary>

We have recently moved our repositories to GitLab. You can find revpi-eol-provisioner
here: https://gitlab.com/revolutionpi/revpi-eol-provisioner  
All repositories on GitHub will stay up-to-date by being synchronised from
GitLab.

We still maintain a presence on GitHub but our work happens over at GitLab. If
you want to contribute to any of our projects we would prefer this contribution
to happen on GitLab, but we also still accept contributions on GitHub if you
prefer that.
</details>

# EOL utilities for RevPi devices

The main purpose of this repository is the device provisioning during our EOL tests. Among the provisioner tool other tools exists, which aim to ease different tasks in development / debugging.

## Usage

### Run device provisioning

The wrapper script writes the HAT eeprom contents, sets the mac address and probably other stuff in the future.

```
usage: provisioner.py [-h] [-v] product-number mac-address eep-image
provisioner.py: error: the following arguments are required: product-number, mac-address, eep-image
```

> **_NOTE:_** Verbose output with optional information can be enabled with the `-v` switch.

### Dump HAT eeprom contents

```
usage: dump_hat.py [-h] [-v] product-number output-file
dump_hat.py: error: the following arguments are required: product-number, output-file
```

Example:
```
sudo python3 -m revpi_provisioning.cli.dump_hat PR100383R00 hat.eep
```

> **_NOTE:_** Verbose output with optional information can be enabled with the `-v` switch.

### Clear HAT eeprom contents


```
usage: clear_hat.py [-h] [-v] product-number
clear_hat.py: error: the following arguments are required: product-number
```

Example:
```
sudo python3 -m revpi_provisioning.cli.clear_hat PR100383R00
```

> **_NOTE:_** Verbose output with optional information can be enabled with the `-v` switch.