#!/usr/bin/env python3

import logging
import sys
import time
from typing import Text, Tuple

from paramiko import SSHClient  # type: ignore

from poopbox.run.run import Command, RunTarget

LOG = logging.getLogger('ssh.py')

class SSHRunTarget(RunTarget):
    def __init__(self, pwd: Text, hostname: Text) -> None:
        super().__init__(pwd)

        self.hostname = hostname

    def _run(self, argv: Command, pwd: Text) -> int:
        try:
            ssh = SSHClient()
            ssh.load_system_host_keys()
            LOG.info('connecting to %s over ssh', self.hostname)
            ssh.connect(hostname=self.hostname)
            LOG.info('executing %s on %s over ssh', argv, self.hostname)
            command = 'bash -c "cd {}; {}"'.format(pwd, ' '.join(argv))
            code = self._run_paramiko_cmd(ssh, command)

        finally:
            ssh.close()
            LOG.info('disconnected from to %s', self.hostname)

        return code

    # https://stackoverflow.com/a/21105626
    @staticmethod
    def _run_paramiko_cmd(ssh, command):  # type: ignore
        transport = ssh.get_transport()
        chan = transport.open_session()

        chan.exec_command(command)

        buff_size = 1024

        while not chan.exit_status_ready():
            time.sleep(.25)
            if chan.recv_ready():
                SSHRunTarget._recv_to_file(chan.recv, sys.stdout)

            if chan.recv_stderr_ready():
                SSHRunTarget._recv_to_file(chan.recv_stderr, sys.stderr)

        exit_status = chan.recv_exit_status()
        # Need to gobble up any remaining output after program terminates...
        while chan.recv_ready():
            SSHRunTarget._recv_to_file(chan.recv, sys.stdout)

        while chan.recv_stderr_ready():
            SSHRunTarget._recv_to_file(chan.recv_stderr, sys.stderr)

        return exit_status

    @staticmethod
    def _recv_to_file(recv_fn, outfile):
        data = recv_fn(2048).decode('utf-8')
        outfile.write(data)
        outfile.flush()
