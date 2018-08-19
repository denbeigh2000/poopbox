#!/usr/bin/env python3

import os
from pathlib import PurePath
from typing import Text

from poopbox import Target
from poopbox.run.ssh import SSHRunTarget
from poopbox.sync.rsync import RSyncSyncTarget

import yaml

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



RUN_TARGETS = {
    'ssh': SSHRunTarget,
}

SYNC_TARGETS = {
    'rsync': RSyncSyncTarget,
}

def target_from_dict(opts):  # type: ignore
    target = opts['target']
    run = target['run']
    sync = target['sync']

    assert run['type'] in RUN_TARGETS, 'invalid run target type'
    run_target_cons = RUN_TARGETS[run['type']]

    assert sync['type'] in SYNC_TARGETS, 'invalid sync target type'
    sync_target_cons = SYNC_TARGETS[sync['type']]

    run_target = run_target_cons(**run['opts'])
    sync_target = sync_target_cons(**sync['opts'])

    return Target(run_target, sync_target)

def find_poopfile() -> Text:
    p = PurePath(os.getcwd())
    while str(p) != '/':
        cand = PurePath(str(p), '.poopfile')
        if cand.exists():
            return str(cand)

    raise RuntimeError('No poopfile found, traversed up to {}'.format(str(p)))

def find_and_parse_poopfile() -> Target:
    poopfile = find_poopfile()
    with open(poopfile, 'r') as f:
        data = f.read()

    config = yaml.loads(f)
    return target_from_dict(config)
