#!/usr/bin/env python3

import setuptools


setuptools.setup(
    name="AutomatedDrinkDispensingSystem",
    version="0.0a3",
    author="Chris Blanks",
    author_email="christopherablanks@gmail.com",
    url="https://github.com/ChrisBlanks/AutomatedDrinkDispensingSystem",
    packages=setuptools.find_packages(),
    include_package_data=True,
    license="LICENSE.txt",
    long_description=open("README.txt").read(),
    install_requires=[
        "setuptools >= 18.5", "cryptography >= 1.7.1",

    ],
)
