#!/usr/bin/env python3

from contextlib import contextmanager
import logging
import os.path
import sys
import subprocess
from typing import List, Optional, Sequence, Text

log = logging.getLogger('sync.py')
log.setLevel(logging.DEBUG)

def _format_dir(d: Text) -> Text:
    return os.path.normpath(d) + '/'

class SyncError(Exception):
    pass


class SyncTarget(object):
    def __init__(self, hostname: Text, local_dir: Text, remote_dir: Text,
            excludes: Optional[Sequence[Text]]=None) -> None:
        self.hostname = hostname
        self.local_dir = _format_dir(local_dir)
        self.remote_dir = _format_dir(remote_dir)

        self.excludes = excludes

    def set_excludes(self, excludes: Sequence[Text]) -> None:
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
            exclude_dirs: Optional[Sequence[Text]]) -> None:
        raise NotImplementedError('_push() must be subclassed')

    def _pull(self, hostname: Text, local_dir: Text, remote_dir: Text,
            exclude_dirs: Optional[Sequence[Text]]) -> None:
        raise NotImplementedError('_pull() must be subclassed')

class RSyncSyncTarget(SyncTarget):
    def _push(self, hostname: Text, local_dir: Text, remote_dir: Text,
            exclude_dirs: Optional[Sequence[Text]]) -> None:
        src = local_dir
        sink = '{}:{}'.format(hostname, remote_dir)
        return self._exec(src, sink, exclude_dirs)

    def _pull(self, hostname: Text, local_dir: Text, remote_dir: Text,
            exclude_dirs: Optional[Sequence[Text]]) -> None:
        src = '{}:{}'.format(hostname, remote_dir)
        sink = local_dir
        return self._exec(src, sink, exclude_dirs)

    def _exec(self, src: Text, sink: Text, excl: Optional[Sequence[Text]]) -> None:
        excludes = [
            '--exclude={}'.format(x)
            for x in excl
        ] if excl else []

        argv = ['rsync', '-a'] + excludes + [src, sink]
        p = subprocess.run(argv)
        if p.stdout is not None:
            print(p.stdout)
        if p.stderr is not None:
            print(p.stderr, file=sys.stderr)

        log.info('rsync exited with %d',  p.returncode)

        if p.returncode != 0:
            raise SyncError('exit status {} ({})'.format(p.returncode, argv))
