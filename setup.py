#!/usr/bin/env python3

from setuptools import setup, find_namespace_packages

setup(
    name='poopbox',
    version='0.0dev',
    # packages=find_namespace_packages('poopbox'),
    packages=['poopbox',
              'poopbox.run',
              'poopbox.sync',
              'poopbox.cli.poopbox',
              'poopbox.cli.pee',
              'poopbox.config',
              'poopbox.dir_utils',
             ],
    entry_points={
        'console_scripts': [
            'p = poopbox.cli.pee.__main__:main',
            'pee = poopbox.cli.pee.__main__:main',
            'poopbox = poopbox.cli.poopbox.__main__:main',
        ]
    },
    install_requires=[
        'paramiko==2.4',
        'pyyaml==3.13',
    ]
)
