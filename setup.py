#!/usr/bin/env python
# -*- coding: utf-8 -*-

'''Install the "polevault" package and CLI command.'''


from __future__ import print_function, division

from setuptools import setup, find_packages


VERSION = '0.1.5'

setup(
    name='polevault',
    version=VERSION,
    author='Paulo Lopes',
    author_email='palopes@cisco.com',
    url='https://paulopes.github.io/polevault/',
    description='Encrypts and decrypts credentials',
    long_description='''\
Encrypts and decrypts credentials, stores them
in a .ini, .conf, .json, .yml, or .yaml file,
and can decrypt them into Hashicorp's Vault.
''',
    packages=find_packages(exclude=[
        "*.tests", "*.tests.*", "tests.*", "tests"]),
    install_requires=[
        'click',
        #    It can use the pyyaml package if it is installed, but it does
        # not require it as long as only the JSON or the INI file formats are
        # used.
        #    However, it does need either cryptography or pycryptodome,
        # whichever is available. Neither are explicilty required during set
        # up so that you can choose which one is the most appropriate for
        # your installation.
        #    The cryptography package is better in terms of performance and
        # reliability, but it uses precompiled code, which can make it
        # difficult to install on some platforms.
        #    The pycryptodome package, on the other hand, is slower, but it
        # is written in pure python, and is installable on any platform.
        #    It also will need hvac to be installed if you need to be able to
        # upload data up to a deployment of Hashicorp's Vault.
        #    If pywebview is installed then polevault can be run from the CLI
        # without any arguments and it will open up an app window using the
        # OS's graphical user interface, where all the functions that can be
        # performed through the CLI, can also be perfomed using a graphical
        # point-and-click user interface.
        #    So, neither pywebview nor pyyaml are absolute requirements in
        # order to use polevault, but it requires the click package for the
        # CLI user interface, and it needs either the cryptography package or
        # the pycryptodome package in order to encrypt and decrypt data.
    ],
    test_suite='tests',
    entry_points={
        'console_scripts': [
            'polevault = polevault:main',
        ]
    },
)
