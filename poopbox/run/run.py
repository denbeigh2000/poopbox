#!/usr/bin/env python3

import logging
from typing import List, Text, Tuple

LOG = logging.getLogger('run.py')
LOG.setLevel(logging.INFO)

Command = List[Text]

class RunError(Exception):
    pass


class RunTarget():
    def __init__(self, pwd: Text) -> None:
        self.pwd = pwd

    def run(self, argv: Command) -> int:
        """
        run executes the given command on the remote target
        """
        return self._run(argv, self.pwd)

    def _run(self, argv: Command, pwd: Text) -> int:
        raise NotImplementedError('_run() must be subclassed')
