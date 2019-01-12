#!/usr/bin/env python3

import setuptools

setuptools.setup(
    name="AutomatedDrinkDispensingSystem",
    version="0.0a1",
    author="Chris B.",
    author_email="christopherablanks@gmail.com",
    packages=setuptools.find_packages(),
    license="LICENSE.txt",
    long_description=open("README.txt").read(),
    install_requires=[
        "cryptography >= 1.7.1",
    ],
)
