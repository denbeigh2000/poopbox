#!/usr/bin/env python3

from contextlib import contextmanager
import logging
import os.path
from typing import Optional, Iterable, Text

LOG = logging.getLogger('sync.py')
LOG.setLevel(logging.DEBUG)

def _format_dir(dir_: Text) -> Text:
    return os.path.normpath(dir_) + '/'

class SyncError(Exception):
    pass


class SyncTarget():
    def __init__(self, hostname: Text, local_dir: Text, remote_dir: Text,
                 excludes: Optional[Iterable[Text]] = None) -> None:
        self.hostname = hostname
        self.local_dir = _format_dir(local_dir)
        self.remote_dir = _format_dir(remote_dir)

        self.excludes = list(excludes) if excludes is not None else []

    def set_excludes(self, excludes: Iterable[Text]) -> None:
        if self.excludes:
            self.excludes.extend(excludes)
        else:
            self.excludes = list(excludes)

    @contextmanager
    def sync(self):  # type: ignore
        self.push()
        yield self
        self.pull()

    def push(self) -> None:
        return self._push(self.hostname, self.local_dir, self.remote_dir, self.excludes)

    def pull(self) -> None:
        return self._pull(self.hostname, self.local_dir, self.remote_dir, self.excludes)

    def _push(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]]) -> None:
        raise NotImplementedError('_push() must be subclassed')

    def _pull(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]]) -> None:
        raise NotImplementedError('_pull() must be subclassed')
