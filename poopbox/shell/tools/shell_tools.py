#!/usr/bin/python

import functools

from poopbox.types import Command

def chain_commands(cmds):
    # type: (List[Command]) -> Command

    return functools.reduce(lambda l, cmd: l + cmd + ['&&'], cmds, [])


def create_env_commands(envs):
    # type: (Dict[Text, Text]) -> List[Command]

    return [
        ['export', '%s="%s"' % (k, v)]
        for k, v in envs.items()
    ]
