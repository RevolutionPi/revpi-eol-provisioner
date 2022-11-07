from schema import And, Optional, Schema

from revpi_provisioning.network import NETWORK_INTERFACE_TYPES

config_schema = Schema({
    Optional("hat_eeprom"): {
        "wp_gpio": int,
        Optional("wp_gpiochip"): str
    },
    "network_interfaces": [
        {
            "type": And(
                str,
                lambda t: t in NETWORK_INTERFACE_TYPES.keys(),
                error="Invalid network interface type"),
            "path": str,
            "eeprom": bool}
    ]
})

def load_config(product: str) -> dict:
    basepath = pathlib.Path(__file__).parent.resolve()
    device_config_file = f"{basepath}/../devices/{product}.yaml"
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
