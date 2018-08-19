#!/usr/bin/env python3

import time
from typing import Text, Tuple

from paramiko import SSHClient  # type: ignore

from poopbox.run.run import Command, RunTarget


class SSHRunTarget(RunTarget):
    def __init__(self, pwd: Text, hostname: Text) -> None:
        super().__init__(pwd)

        self.hostname = hostname

    def _run(self, argv: Command, pwd: Text) -> Tuple[int, Text, Text]:
        try:
            ssh = SSHClient()
            ssh.load_system_host_keys()
            ssh.connect(hostname=self.hostname)
            command = 'sh -c "cd {}; {}"'.format(pwd, ''.join(argv))
            code, out, err = self._run_paramiko_cmd(ssh, command, get_pty=True)

        finally:
            ssh.close()

        return code, out, err

    # https://stackoverflow.com/a/21105626
    @staticmethod
    def _run_paramiko_cmd(ssh, command, *args, **kwargs):  # type: ignore
        transport = ssh.get_transport()
        chan = transport.open_session()

        chan.exec_command(command, *args, **kwargs)

        buff_size = 1024
        stdout = ""
        stderr = ""

        while not chan.exit_status_ready():
            time.sleep(.25)
            if chan.recv_ready():
                stdout += chan.recv(buff_size).decode('utf-8')

            if chan.recv_stderr_ready():
                stderr += chan.recv_stderr(buff_size).decode('utf-8')

        exit_status = chan.recv_exit_status()
        # Need to gobble up any remaining output after program terminates...
        while chan.recv_ready():
            stdout += chan.recv(buff_size)

        while chan.recv_stderr_ready():
            stderr += chan.recv_stderr(buff_size)

        return exit_status, stdout or None, stderr or None
