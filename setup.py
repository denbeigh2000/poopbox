#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

print(find_namespace_packages('poopbox'))

setup(
    name='poopbox',
    version='0.0dev',
    # packages=find_namespace_packages('poopbox'),
    packages=['poopbox.run', 'poopbox.sync'],
    install_package_data=True,
)
