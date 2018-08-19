#!/usr/bin/env python3

import logging
import time
from typing import Iterable, Text, Tuple

log = logging.getLogger('run.py')
log.setLevel(logging.DEBUG)

Command = Iterable[Text]

class RunError(Exception):
    pass


class RunTarget(object):
    def __init__(self, pwd: Text) -> None:
        self.pwd = pwd

    def run(self, argv: Command) -> Tuple[int, Text, Text]:
        """
        run executes the given command on the remote target
        """
        return self._run(argv, self.pwd)

    def _run(self, argv: Command, pwd: Text) -> Tuple[int, Text, Text]:
        raise NotImplementedError('_run() must be subclassed')
