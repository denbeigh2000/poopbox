#!/usr/bin/env python

from contextlib import contextmanager
import logging
import subprocess
import sys
import time
from typing import Optional, Dict, List, Text, Tuple

from paramiko import SSHClient  # type: ignore

from poopbox.shell.tools import (
    create_env_commands,
    chain_commands,
)
from poopbox.run.run import Command, RunTarget

LOG = logging.getLogger('ssh.py')
LOG.setLevel(logging.DEBUG)

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


class SSHExecutor():
    def run_over_ssh(self, argv):
        # type: (Command) -> int
        raise NotImplementedError('run_over_ssh must be implemented')

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

class SubprocessSSHExecutor(SSHExecutor):
    def __init__(self, remote_host):
        self.remote_host = remote_host

    def run_over_ssh(self, command):
        # type: (Command) -> int
        command_str = ' '.join(command)
        LOG.debug(command_str)

        args = ['ssh', '-t', self.remote_host, command_str]
        proc = subprocess.Popen(args, stdin=sys.stdin, stdout=sys.stdout,
                                stderr=sys.stderr)
        sys.stdin.flush()
        proc.wait()

        return proc.returncode
