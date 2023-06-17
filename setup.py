from setuptools import setup, find_packages

setup(
    name="revpi-eol-provisioner",
    version="1.0.0",
    packages=find_packages(),
    package_data={"revpi_provisioning": ["devices/*.yaml"]},
    install_requires=[
        "schema"
    ],
    entry_points={
        "console_scripts": [
            'revpi-eol-provisioner = revpi_provisioning.cli.provisioner:main',
            'revpi-eol-clear-hat = revpi_provisioning.cli.clear_hat:main',
            'revpi-eol-validate-config = revpi_provisioning.cli.validator:main'
        ]
    }
)
