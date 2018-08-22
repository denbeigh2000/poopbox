#!/usr/bin/env python3

from contextlib import contextmanager
import logging
from typing import Iterable, List, Optional, Text

from poopbox.dir_utils import format_dir

LOG = logging.getLogger('sync.py')

class SyncError(Exception):
    pass


class SyncTarget():
    def __init__(self, poopdir: Text, remote_host: Text,
                 remote_dir: Text,
                 excludes: Optional[Iterable[Text]] = None) -> None:
        self.poopdir = poopdir
        self.remote_dir = format_dir(remote_dir)
        self.remote_host = remote_host

        self.excludes = list(excludes) if excludes is not None else []

    def push(self, files: Optional[Iterable[Text]] = None) -> None:
        LOG.info('pushing to %s', self.remote_host)
        return self._push(files)

    def pull(self, files: Optional[Iterable[Text]] = None) -> None:
        LOG.info('pulling from %s', self.remote_host)
        return self._pull(files)

    def _push(self, files: Optional[Iterable[Text]] = None) -> None:
        raise NotImplementedError('_push() must be subclassed')

    def _pull(self, files: Optional[Iterable[Text]] = None) -> None:
        raise NotImplementedError('_pull() must be subclassed')
