#!/usr/bin/python

import functools

def construct_pre_commands(cmds):
    # type: (List[List[Text]]) -> List[Text]
    return functools.reduce(lambda l, cmd: l + cmd + ['&&'], cmds, [])


def construct_env_commands(envs):
    # type: (Dict[Text, Text]) -> List[Text]

    return functools.reduce(
        lambda l, env: l + ['export', '%s=%s' % env, '&&'],  # type: ignore
        envs.items(), [])

