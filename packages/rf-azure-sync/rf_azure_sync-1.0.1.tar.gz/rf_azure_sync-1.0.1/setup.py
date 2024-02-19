from setuptools import setup, find_packages

setup(
    name="rf_azure_sync",
    version="1.0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "rf_azure_sync=rf_azure_sync.rf_azure_sync:rf_azure_sync",
        ],
    },
)
