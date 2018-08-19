#!/usr/bin/env python3

import logging
from pathlib import PurePath
import subprocess
import sys
from typing import Optional, Iterable, Text

from poopbox.sync import SyncTarget, SyncError

LOG = logging.getLogger('rsync.py')

class RSyncSyncTarget(SyncTarget):
    def _push(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]],
              files: Optional[Iterable[Text]] = None) -> None:
        srcs = self._join_srcs(local_dir, files)
        sink = '{}:{}'.format(hostname, remote_dir)
        return self._exec(srcs, sink, exclude_dirs)

    def _pull(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]],
              files: Optional[Iterable[Text]] = None) -> None:
        srcs = [
            '{}:{}'.format(hostname, src)
            for src in self._join_srcs(remote_dir, files)
        ]
        sink = local_dir
        return self._exec(srcs, sink, exclude_dirs)

    @staticmethod
    def _exec(srcs: Iterable[Text], sink: Text,
              excl: Optional[Iterable[Text]]) -> None:
        excludes = [
            '--exclude={}'.format(x)
            for x in excl
        ] if excl else []

        argv = ['rsync', '-a'] + excludes + srcs + [sink]
        LOG.info('executing rsync with %s', argv)
        proc = subprocess.run(argv)
        if proc.stdout is not None:
            print(proc.stdout)
        if proc.stderr is not None:
            print(proc.stderr, file=sys.stderr)

        LOG.info('rsync exited with %d', proc.returncode)

        if proc.returncode != 0:
            raise SyncError('exit status {} ({})'.format(proc.returncode, argv))

    @staticmethod
    def _join_srcs(dir_: Text, files: Optional[Iterable[Text]]):
        if not files:
            return [dir_]

        return [
            str(PurePath(dir_, f)) for f in files
        ]
