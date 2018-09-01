#!/usr/bin/env python

from poopbox.types import Command

class SSHExecutor():
    def run_over_ssh(self, argv):
        # type: (Command) -> int
        raise NotImplementedError('run_over_ssh must be implemented')
