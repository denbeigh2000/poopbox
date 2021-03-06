#!/usr/bin/env python

from setuptools import setup

setup(
    name='poopbox',
    version='0.1.0',
    packages=['poopbox',
              'poopbox.run',
              'poopbox.sync',
              'poopbox.cli.poopbox',
              'poopbox.cli.pee',
              'poopbox.config',
              'poopbox.utils',
             ],
    entry_points={
        'console_scripts': [
            'p = poopbox.cli.pee.__main__:main',
            'pee = poopbox.cli.pee.__main__:main',
            'poopbox = poopbox.cli.poopbox.__main__:main',
        ]
    },
    install_requires=[
        'pathlib2==2.3.2',
        'pyyaml>=4.2b1,<5.0',
        'subprocess32==3.5.2',
        'typing',
    ]
)
