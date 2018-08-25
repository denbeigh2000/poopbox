#!/usr/bin/env python

from poopbox.run.run import Command

class SSHExecutor():
    def run_over_ssh(self, argv):
        # type: (Command) -> int
        raise NotImplementedError('run_over_ssh must be implemented')
