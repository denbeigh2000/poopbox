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

    def _run(self, argv: Command) -> int:
        raise NotImplementedError('_run() must be subclassed')
