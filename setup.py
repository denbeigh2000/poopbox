#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

setup(
    name='poopbox',
    version='0.0dev',
    # packages=find_namespace_packages('poopbox'),
    packages=['poopbox', 'poopbox.run', 'poopbox.sync', 'poopbox.cli'],
    entry_points={
        'console_scripts': [
            'p = poopbox.cli.pee.__main__:main',
            'pee = poopbox.cli.pee.__main__:main',
            'poopbox = poopbox.cli.poopbox.__main__:main',
        ]
    },
)
