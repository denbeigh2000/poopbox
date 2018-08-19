#!/usr/bin/env python3

from contextlib import contextmanager
import logging
import sys
import subprocess
import time
from typing import Text, Tuple

from paramiko import SSHClient  # type: ignore

from poopbox.run.run import Command, RunTarget

LOG = logging.getLogger('ssh.py')

class SSHRunTarget(RunTarget):
    def __init__(self, pwd: Text, hostname: Text) -> None:
        super().__init__(pwd)

        self.hostname = hostname

    @contextmanager
    def _session(self):  # type: ignore
        client = SSHClient()
        client.load_system_host_keys()
        LOG.info('connecting to %s over ssh', self.hostname)
        client.connect(hostname=self.hostname)

        yield client

        LOG.info('closing ssh session with %s', self.hostname)
        client.close()
        LOG.info('disconnected from to %s', self.hostname)


    def _shell(self, pwd: Text) -> None:
        remote_args = ['cd', pwd, '&&', 'exec', '$SHELL', '-l']
        args = ['ssh', '-t', self.hostname, ' '.join(remote_args)]
        proc = subprocess.Popen(args, stdin=sys.stdin, stdout=sys.stdout,
                                stderr=sys.stderr)
        sys.stdin.flush()
        proc.wait()

    def _run(self, argv: Command, pwd: Text) -> int:
        with self._session() as client:

            LOG.info('executing %s on %s over ssh', argv, self.hostname)
            remote_cmd = 'mkdir -p {pwd} && cd {pwd} && {cmd}'.format(
                pwd=pwd, cmd=' '.join(argv))
            cmd = ['sh', '-c', '"{}"'.format(remote_cmd)]
            code = self._run_paramiko_cmd(client, ' '.join(cmd))

        return code

    # https://stackoverflow.com/a/21105626
    @staticmethod
    def _run_paramiko_cmd(client, command):  # type: ignore
        transport = client.get_transport()
        chan = transport.open_session()

        chan.exec_command(command)

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
