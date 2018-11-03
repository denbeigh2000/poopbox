#!/usr/bin/env python

from contextlib import contextmanager
import logging
from typing import Iterable, List, Optional, Text

from poopbox.utils import format_dir

LOG = logging.getLogger('sync.py')

class SyncError(Exception):
    pass


class SyncTarget():
    def __init__(self, poopdir, remote_host, remote_dir, excludes=None):
        # type: (Text, Text, Text, Optional[Iterable[Text]]) -> None
        self.poopdir = poopdir
        self.remote_dir = format_dir(remote_dir)
        self.remote_host = remote_host

        self.excludes = list(excludes) if excludes is not None else []

    def push(self, files=None):
        # type: (Optional[Iterable[Text]]) -> None
        LOG.info('pushing to %s', self.remote_host)
        return self._push(files)

    def pull(self, files=None):
        # type(Optional[Iterable[Text]] -> None
        LOG.info('pulling from %s', self.remote_host)
        return self._pull(files)

    def _push(self, files=None):
        # type(Optional[Iterable[Text]] -> None
        raise NotImplementedError('_push() must be subclassed')

    def _pull(self, files=None):
        # type(Optional[Iterable[Text]] -> None
        raise NotImplementedError('_pull() must be subclassed')
