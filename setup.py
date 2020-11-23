#!/usr/bin/env python3

from setuptools import setup

setup(
    name='bolt11',
    version='0.1',
    author='nievk',
    packages=['bolt11'],
    install_requires=['ecdsa', 'bech32', 'bitstring']
)
