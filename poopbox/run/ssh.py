#!/usr/bin/env python

from contextlib import contextmanager
import logging
import subprocess
import time
from typing import Optional, Dict, List, Text, Tuple

from poopbox.run import RunTarget
from poopbox.shell.tools import (
    create_env_commands,
    chain_commands,
)
from poopbox.ssh.executors import SubprocessSSHExecutor
from poopbox.types import Command

LOG = logging.getLogger(__file__)

class SSHRunTarget(RunTarget):
    def __init__(self,
            remote_host,    # type: Text
            remote_dir,     # type: Text
            pre_cmds=None,  # type: Optional[List[Command]]
            env=None,       # type: Optional[Dict[Text, Text]]
            ):
        # type: (...) -> None
        self.remote_dir = remote_dir
        self.remote_host = remote_host
        self.env = env
        self.pre_cmds = pre_cmds

        # self._ssh = ParamikoSSHExecutor(self.remote_host)
        self._ssh = SubprocessSSHExecutor(self.remote_host)

    def _run(self, argv):
        # type: (Command) -> int

        cmd = self._create_cmd(argv)
        LOG.info('executing %s on %s over ssh', argv, self.remote_host)
        return self._ssh.run_over_ssh(cmd)

    def _create_cmd(self, argv):
        # type: (Command) -> Command

        return ['bash', '--rcfile', '/dev/null', '-c',
                   '"' + self._create_inner_cmd_str(argv) + '"']

    def _create_inner_cmd_str(self, argv):
        # type: (Command) -> Text
        leading_cmds = [
            ['mkdir', '-p', self.remote_dir],
            ['cd', self.remote_dir]
        ]

        env_cmds = create_env_commands(self.env or {})
        pre_cmds = self.pre_cmds or []

        inner_cmds = leading_cmds + env_cmds + pre_cmds + [argv]
        return ' '.join(chain_commands(inner_cmds)[:-1])


