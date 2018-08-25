#!/usr/bin/env python

import sys

from paramiko import SSHClient  # type: ignore

from .ssh_executor import SSHExecutor
from poopbox.run.run import Command

LOG = logging.getLogger(__file__)

class ParamikoSSHExecutor(SSHExecutor):
    def __init__(self, remote_host):
        self.remote_host = remote_host

        self.client = SSHClient()
        self.client.load_system_host_keys()
        LOG.info('created ssh client')

    @contextmanager
    def _session(self):  # type: ignore
        LOG.info('connecting to %s over ssh', self.remote_host)
        self.client.connect(hostname=self.remote_host)

        yield self.client

        LOG.info('closing ssh session with %s', self.remote_host)
        self.client.close()
        LOG.info('disconnected from %s', self.remote_host)

    def run_over_ssh(self, command):
        # type: (Command) -> int
        command_str = ' '.join(command)
        LOG.debug(command_str)
        return self._run_paramiko_cmd(command_str)

    # https://stackoverflow.com/a/21105626
    def _run_paramiko_cmd(self, command):
        # type: (Text) -> int
        with self._session():
            transport = self.client.get_transport()
            chan = transport.open_session()

            chan.exec_command(command)

            while not chan.exit_status_ready():
                time.sleep(.25)
                if chan.recv_ready():
                    self._recv_to_file(chan.recv, sys.stdout)

                if chan.recv_stderr_ready():
                    self._recv_to_file(chan.recv_stderr, sys.stderr)

            exit_status = chan.recv_exit_status()
            # Need to gobble up any remaining output after program terminates...
            while chan.recv_ready():
                self._recv_to_file(chan.recv, sys.stdout)

            while chan.recv_stderr_ready():
                self._recv_to_file(chan.recv_stderr, sys.stderr)

            return exit_status

    @staticmethod
    def _recv_to_file(recv_fn, outfile):
        data = recv_fn(2048).decode('utf-8')
        outfile.write(data)
        outfile.flush()
