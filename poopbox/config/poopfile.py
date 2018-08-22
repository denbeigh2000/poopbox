#!/usr/bin/env python3

import os
from pathlib import Path
from typing import Text, Tuple, Type

import yaml

from poopbox.target import Target
from poopbox.target.targets import RSyncSSHTarget

# pylint: disable=pointless-string-statement
"""
Sample poopfile format
target:
    run:
        type: ssh
        opts:
           (kwargs)

    sync:
        type: rsync
        opts:
            (kwargs)
"""
# pylint: enable=pointless-string-statement


DEFAULT_TARGET_CLASS = RSyncSSHTarget  # type: Type[Target]

def subtargets_from_dict(opts):
    target = opts['target']

    run = target['run']
    sync = target['sync']

    assert run['type'] in RUN_TARGETS, 'invalid run target type'
    run_target_cons = RUN_TARGETS[run['type']]
    run_target = run_target_cons(**run['opts'])

    assert sync['type'] in SYNC_TARGETS, 'invalid sync target type'
    sync_target_cons = SYNC_TARGETS[sync['type']]
    sync_target = sync_target_cons(**sync['opts'])

    return (run_target, sync_target)


def find_poopfile() -> Tuple[Text, Text]:
    cand_dir = Path(os.getcwd())
    while True:
        cand = cand_dir.joinpath('.poopfile')
        if cand.exists():
            return (str(cand_dir.resolve()), str(cand.resolve()))

        if str(cand_dir) == cand_dir.root:
            raise RuntimeError('traversed up to root without finding a poopfile, bailing out')

        cand_dir = cand_dir.parent


def find_and_parse_poopfile() -> Target:
    poopdir, poopfile = find_poopfile()

    with open(poopfile, 'r') as file_:
        data = file_.read()

    config = yaml.load(data)
    config_type = config.pop('target', None)

    if not config_type or config_type in ('RSyncSSH', 'RSyncSSHTarget'):
        TargetClass = RSyncSSHTarget
    else:
        raise RuntimeError('Only RSyncSSHTarget supported for now')

    target = TargetClass(poopdir)
    target.configure(config)

    return target
