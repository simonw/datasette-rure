from setuptools import setup
import os

VERSION = "0.2"


def get_long_description():
    with open(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="datasette-rure",
    description="Datasette plugin that adds a custom SQL function for executing matches using the Rust regular expression engine",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    author="Simon Willison",
    url="https://github.com/simonw/datasette-rure",
    license="Apache License, Version 2.0",
    version=VERSION,
    packages=["datasette_rure"],
    entry_points={"datasette": ["rure = datasette_rure"]},
    install_requires=["datasette", "rure"],
    extras_require={"test": ["pytest"]},
    tests_require=["datasette-rure[test]"],
)
