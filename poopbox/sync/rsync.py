#!/usr/bin/env python

from __future__ import print_function

import logging
try:
    from pathlib import PurePath
    import subprocess
except ImportError:
    from pathlib2 import PurePath
    import subprocess32 as subprocess
import os
import sys
from typing import Optional, Iterable, List, Text

from poopbox.sync import SyncTarget, SyncError

LOG = logging.getLogger('rsync.py')

class RSyncSyncTarget(SyncTarget):
    def _push(self, files=None, syncfile=None):
        # type: (Optional[Iterable[Text]]) -> None
        if files is not None and syncfile is not None:
            LOG.warning('received both a list of files and a syncfile - ignoring syncfile')
            syncfile = None

        sink = '{}:{}'.format(self.remote_host, self.remote_dir)

        if syncfile is not None:
            cmd = RSyncSyncTarget._make_cmd_syncfile(self.poopdir, sink,
                    self.syncfile, self.excludes)
        else:
            srcs = self._join_srcs(self.poopdir, files)

            if srcs is not None and len(srcs) == 0:
                return
            cmd = RSyncSyncTarget._make_cmd([self.poopdir], sink, srcs,
                    self.excludes)

        return self._exec(cmd)

    def _pull(self, files=None, syncfile=None):
        # type: (Optional[Iterable[Text]], Optional[Text]) -> int
        sink = self.poopdir
        if syncfile is not None:
            LOG.debug('making syncfile cmd')
            cmd = RSyncSyncTarget._make_cmd_syncfile(self.remote_dir, sink,
                    self.syncfile, self.excludes)
        else:
            srcs = [
                '{}:{}'.format(self.remote_host, src)
                for src in self._join_srcs(self.remote_dir, files)
            ]
            LOG.debug('making explicit', files)
            cmd = RSyncSyncTarget._make_cmd(self.poopdir, sink, srcs,
                    self.excludes)

        cmd = self._make_cmd(srcs, sink, files, self.excludes)

        return self._exec(cmd)

    @staticmethod
    def _exec(argv):
        # type: (List[Text]) -> int
        LOG.info('executing rsync with %s', argv)
        proc = subprocess.run(argv)
        if proc.stdout is not None:
            print(proc.stdout)
        if proc.stderr is not None:
            print(proc.stderr, file=sys.stderr)

        LOG.info('rsync exited with %d', proc.returncode)

        if proc.returncode != 0:
            raise SyncError('exit status {} ({})'.format(proc.returncode, argv))

        return proc.returncode

    @staticmethod
    def _format_excludes(excludes):
        # type: Optional[Iterable[Text]] -> List[Text]
        return [
            '--exclude={}'.format(x)
            for x in excludes
        ] if excludes else []

    @staticmethod
    def _make_cmd_syncfile(srcdir, sink, syncfile, excl=None):
        # type: (Text, Text, Text) -> List[Text]
        excludes = RSyncSyncTarget._format_excludes(excl)

        return [
            'find', srcdir, '-newer', syncfile, '-printf', r'%P\\0', '|',
            'rsync', '-a', '--delete'] + excludes + ['--files-from=-',
            '--from0', srcdir, sink
        ]

    @staticmethod
    def _make_cmd(srcs, sink, files=None, excl=None):
        # type: (Iterable[Text], Text, Optional[Iterable[Text]]) -> List[Text]
        excludes = RSyncSyncTarget._format_excludes(excl)
        return ['rsync', '--ignore-missing-args', '-a', '--delete'] + excludes + list(srcs) + [sink]

    @staticmethod
    def _join_srcs(dir_, files=None):
        # type: (Text, Optional[Iterable[Text]]) -> Iterable[Text]
        if files is None:
            return [dir_]

        return [
            Text(PurePath(dir_, f)) for f in files
        ]
