#!/usr/bin/env python

from contextlib import contextmanager
import logging
import sys
import time
from typing import Optional, Dict, List, Text, Tuple

from paramiko import SSHClient  # type: ignore

from poopbox.run.run import Command, RunTarget

LOG = logging.getLogger('ssh.py')

class SSHRunTarget(RunTarget):
    def __init__(self, remote_host, remote_dir, env=None):
        # type: (Text, Text, Optional[Dict[Text, Text]]) -> None
        self.remote_dir = remote_dir
        self.remote_host = remote_host
        self.env = env

    @contextmanager
    def _session(self):  # type: ignore
        client = SSHClient()
        client.load_system_host_keys()
        LOG.info('connecting to %s over ssh', self.remote_host)
        client.connect(hostname=self.remote_host)

        yield client

        LOG.info('closing ssh session with %s', self.remote_host)
        client.close()
        LOG.info('disconnected from %s', self.remote_host)

    def _construct_env_commands(self):
        # type: () -> List[Text]
        if not self.env:
            return []

        args = []

        for k, v in self.env.items():
            args = args + ['export', '{}={}'.format(k, v), '&&']

        return args

    def _run(self, argv):
        # type: (Command) -> int
        with self._session() as client:
            env = self._construct_env_commands
            command = ['mkdir', '-p', self.remote_dir, '&&',
                        'cd', self.remote_dir, '&&'] + env + argv
            cmd_str = ['bash', '-c', '"{}"'.format(' '.join(command))]

            LOG.info('executing %s on %s over ssh', argv, self.remote_host)
            code = self._run_paramiko_cmd(client, ' '.join(cmd_str))

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
