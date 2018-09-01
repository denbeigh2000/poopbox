#!/usr/bin/env python

import logging
from typing import List, Text, Tuple

from poopbox.types import Command

LOG = logging.getLogger('run.py')
LOG.setLevel(logging.INFO)

class RunError(Exception):
    pass


class RunTarget():
    def run(self, argv):
        # type: (Command) -> int
        """
        run executes the given command on the remote target
        """
        return self._run(argv)

    def _run(self, argv):
        # type: (Command) -> int
        raise NotImplementedError('_run() must be subclassed')
