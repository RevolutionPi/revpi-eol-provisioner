from setuptools import setup, find_packages

setup(
    name="revpi-eol-provisioner",
    version="0.1",
    packages=find_packages(),
    package_data={"revpi_provisioning": ["devices/*.yaml"]},
    entry_points={
        "console_scripts": [
            'revpi-eol-provisioner = revpi_provisioning.__main__:main'
        ]
    }
)
