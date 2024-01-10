"""Run provisioner command as default CLI command."""

import sys

# If we are running from a wheel, add the wheel to sys.path
if __package__ == "":
    from os.path import dirname
    from sys import path

    # __file__ is package-*.whl/package/__main__.py
    # Resulting path is the name of the wheel itself
    package_path = dirname(dirname(__file__))
    path.insert(0, package_path)

if __name__ == "__main__":
    from revpi_provisioning.cli.provisioner import main

    sys.exit(main())
