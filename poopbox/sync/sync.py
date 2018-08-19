#!/usr/bin/env python3

from contextlib import contextmanager
import logging
from typing import Iterable, List, Optional, Text

from poopbox.dir_utils import format_dir

LOG = logging.getLogger('sync.py')

class SyncError(Exception):
    pass


class SyncTarget():
    def __init__(self, hostname: Text, remote_dir: Text) -> None:
        self.hostname = hostname
        self.remote_dir = format_dir(remote_dir)

        self.excludes = []  # type: List[Text]

    def set_excludes(self, excludes: Iterable[Text]) -> None:
        LOG.info('extending excludes with %s', excludes)
        if excludes:
            self.excludes.extend(excludes)

    def set_poopdir(self, poopdir: Text):
        self.poopdir = format_dir(poopdir)

    @contextmanager
    def sync(self):  # type: ignore
        self.push()
        yield self
        self.pull()

    def push(self, files: Optional[Iterable[Text]] = None) -> None:
        LOG.info('pushing to %s', self.hostname)
        return self._push(self.hostname, self.poopdir, self.remote_dir, self.excludes, files)

    def pull(self, files: Optional[Iterable[Text]] = None) -> None:
        LOG.info('pulling from %s', self.hostname)
        return self._pull(self.hostname, self.poopdir, self.remote_dir, self.excludes, files)

    def _push(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]],
              files: Optional[Iterable[Text]] = None) -> None:
        raise NotImplementedError('_push() must be subclassed')

    def _pull(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]],
              files: Optional[Iterable[Text]] = None) -> None:
        raise NotImplementedError('_pull() must be subclassed')
