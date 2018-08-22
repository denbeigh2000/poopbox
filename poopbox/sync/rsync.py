#!/usr/bin/env python

from __future__ import print_function

import logging
try:
    from pathlib import PurePath
    import subprocess
except ImportError:
    from pathlib2 import PurePath
    import subprocess32 as subprocess
import sys
from typing import Optional, Iterable, Text

from poopbox.sync import SyncTarget, SyncError

LOG = logging.getLogger('rsync.py')

class RSyncSyncTarget(SyncTarget):
    def _push(self, files=None):
        # type: (Optional[Iterable[Text]]) -> None
        srcs = self._join_srcs(self.poopdir, files)
        sink = '{}:{}'.format(self.remote_host, self.remote_dir)
        return self._exec(srcs, sink, self.excludes)

    def _pull(self, files=None):
        # type: (Optional[Iterable[Text]]) -> None
        srcs = [
            '{}:{}'.format(self.remote_host, src)
            for src in self._join_srcs(self.remote_dir, files)
        ]
        sink = self.poopdir
        return self._exec(srcs, sink, self.excludes)

    @staticmethod
    def _exec(srcs, sink, excl=None):
        # type: (Iterable[Text], Text, Optional[Iterable[Text]]) -> None
        excludes = [
            '--exclude={}'.format(x)
            for x in excl
        ] if excl else []

        argv = ['rsync', '-a', '--delete'] + excludes + list(srcs) + [sink]
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
    def _join_srcs(dir_, files=None):
        # type: (Text, Optional[Iterable[Text]]) -> Iterable[Text]
        if not files:
            return [dir_]

        return [
            Text(PurePath(dir_, f)) for f in files
        ]
