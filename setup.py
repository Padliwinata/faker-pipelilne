from setuptools import find_packages, setup

setup(
    name="supply_chain",
    packages=find_packages(exclude=["supply_chain_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud",
        "faker",
        "pandas"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
