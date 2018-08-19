#!/usr/bin/env python3

import os
from pathlib import Path
from typing import Text, Tuple

import yaml

from poopbox import Target
from poopbox.run.targets import SSHRunTarget
from poopbox.sync.targets import RSyncSyncTarget

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



RUN_TARGETS = {
    'ssh': SSHRunTarget,
}

SYNC_TARGETS = {
    'rsync': RSyncSyncTarget,
}

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


    (run_target, sync_target) = subtargets_from_dict(config)
    excludes = config['target']['excludes']

    return Target(run_target, sync_target, poopdir, excludes)