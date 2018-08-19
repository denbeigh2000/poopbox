#!/usr/bin/env python3

import logging
import subprocess
import sys
from typing import Optional, Iterable, Text

from poopbox.sync import SyncTarget, SyncError

LOG = logging.getLogger('rsync.py')

class RSyncSyncTarget(SyncTarget):
    def _push(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]]) -> None:
        src = local_dir
        sink = '{}:{}'.format(hostname, remote_dir)
        return self._exec(src, sink, exclude_dirs)

    def _pull(self, hostname: Text, local_dir: Text, remote_dir: Text,
              exclude_dirs: Optional[Iterable[Text]]) -> None:
        src = '{}:{}'.format(hostname, remote_dir)
        sink = local_dir
        return self._exec(src, sink, exclude_dirs)

    @staticmethod
    def _exec(src: Text, sink: Text, excl: Optional[Iterable[Text]]) -> None:
        excludes = [
            '--exclude={}'.format(x)
            for x in excl
        ] if excl else []

        argv = ['rsync', '-a'] + excludes + [src, sink]
        LOG.info('executing rsync with %s', argv)
        proc = subprocess.run(argv)
        if proc.stdout is not None:
            print(proc.stdout)
        if proc.stderr is not None:
            print(proc.stderr, file=sys.stderr)

        LOG.info('rsync exited with %d', proc.returncode)

        if proc.returncode != 0:
            raise SyncError('exit status {} ({})'.format(proc.returncode, argv))
