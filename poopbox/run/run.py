#!/usr/bin/env python3

import logging
from typing import List, Text, Tuple

LOG = logging.getLogger('run.py')
LOG.setLevel(logging.INFO)

Command = List[Text]

class RunError(Exception):
    pass


class RunTarget():
    def run(self, argv: Command) -> int:
        """
        run executes the given command on the remote target
        """
        return self._run(argv)

    def shell(self) -> None:
        """
        shell initiates an interactive shell session on the remote machine.
        This may not be applicable in some use cases.
        """
        return self._shell()

    def _shell(self) -> int:
        raise NotImplementedError('_run() must be subclassed')

    def _run(self, argv: Command) -> int:
        raise NotImplementedError('_run() must be subclassed')
