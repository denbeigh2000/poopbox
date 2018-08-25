#!/usr/bin/env python

import subprocess
import sys
from typing import Text

from poopbox.shell import ShellTarget
from poopbox.shell.tools import (
    construct_env_commands,
    construct_pre_commands,
)

class SSHShellTarget(ShellTarget):
    def __init__(self,
            remote_host,    # type: Text
            remote_dir,     # type: Text
            pre_cmds=None,  # type: Optional[List[List[Text]]]
            env=None,       # type: Optional[Dict[Text, Text]]
            ):
        # type: (...) -> None
        self.remote_host = remote_host
        self.remote_dir = remote_dir

        self.env = env
        self.pre_cmds = pre_cmds

    def shell(self):
        # type: () -> int
        env = []  # type: List[Text]
        pre = []  # type: List[Text]

        if self.env:
            env = construct_env_commands(self.env)
        if self.pre_cmds:
            pre = construct_pre_commands(self.pre_cmds)

        remote_args = ['mkdir', '-p', self.remote_dir, '&&',  'cd',
                self.remote_dir, '&&'] + env + pre + ['exec', '$SHELL', '-l']
        args = ['ssh', '-t', self.remote_host, ' '.join(remote_args)]
        proc = subprocess.Popen(args, stdin=sys.stdin, stdout=sys.stdout,
                                stderr=sys.stderr)
        sys.stdin.flush()
        proc.wait()

        return proc.returncode
