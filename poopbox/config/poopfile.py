#!/usr/bin/env python

import importlib
import os
try:
    from pathlib import Path
except ImportError:
    from pathlib2 import Path
from typing import Text, Tuple, Type

import yaml

from poopbox.target import Target
from poopbox.target.targets import RSyncSSHTarget


DEFAULT_TARGET_CLASS = RSyncSSHTarget  # type: Type[Target]

def find_poopfile():
    # type: () -> Tuple[Text, Text]
    cand_dir = Path(os.getcwd())
    while True:
        cand = cand_dir.joinpath('.poopfile')
        if cand.exists():
            return (str(cand_dir.resolve()), str(cand.resolve()))

        if str(cand_dir) == cand_dir.root:
            raise RuntimeError('traversed up to root without finding a poopfile, bailing out')

        cand_dir = cand_dir.parent


def find_and_parse_poopfile():
    # type: () -> Target
    poopdir, poopfile = find_poopfile()

    with open(poopfile, 'r') as file_:
        data = file_.read()

    config = yaml.load(data)
    config_type = config.pop('target', None)

    if not config_type or config_type in ('RSyncSSH', 'RSyncSSHTarget'):
        TargetClass = RSyncSSHTarget
    else:
        TargetClass = importlib.import_module(config_type)

    target = TargetClass(poopdir)
    target.configure(config)

    return target
