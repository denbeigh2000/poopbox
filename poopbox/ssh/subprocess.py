#!/usr/bin/env python

import logging
import subprocess
import sys

from .ssh_executor import SSHExecutor
from poopbox.types import Command

LOG = logging.getLogger(__file__)

class SubprocessSSHExecutor(SSHExecutor):
    def __init__(self, remote_host):
        self.remote_host = remote_host

    def run_over_ssh(self, command):
        # type: (Command) -> int
        command_str = ' '.join(command)
        LOG.debug(command_str)

        args = ['ssh', '-o', 'LogLevel=QUIET', '-t', self.remote_host, command_str]
        proc = subprocess.Popen(args, stdin=sys.stdin, stdout=sys.stdout,
                                stderr=sys.stderr)
        sys.stdin.flush()
        proc.wait()

        return proc.returncode
