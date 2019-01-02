#!/usr/bin/env python

import logging
import os
import sys
if sys.version_info[0] == 3:
    import subprocess
else:
    import subprocess32 as subprocess
from typing import Any, Dict, Iterable, Optional, List, Text

from poopbox.run import RunError
from poopbox.run.targets import SSHRunTarget
from poopbox.shell.targets import SSHShellTarget
from poopbox.ssh import SSHTooling
from poopbox.sync import DEFAULT_EXCLUDES, SyncError
from poopbox.sync.targets import RSyncSyncTarget
from poopbox.target import Target

LOG = logging.getLogger('rsyncssh.py')

class RSyncSSHTarget(Target):
    def _run_on_configure(self, config):
        # type: (Dict[Any, Any]) -> None
        self.remote_host = config['remote_host']
        self.remote_dir = config['remote_dir']

        excludes = set(config.get('excludes', []) + DEFAULT_EXCLUDES)
        pre_cmds = config.get('pre_cmds', None)
        env = config.get('env', None)

        self.remote_cachedir = os.path.join(self.remote_dir, self.cachedir_name)

        self.syncfile = os.path.join(self.cachedir, 'lsyncfile')
        self.remote_syncfile = os.path.join(self.remote_cachedir, 'rsyncfile')

        self._sync = RSyncSyncTarget(self.poopdir,
                self.remote_host, self.remote_dir, excludes)
        self._run = SSHRunTarget(self.remote_host, self.remote_dir, pre_cmds=pre_cmds, env=env)
        self._shell = SSHShellTarget(self.remote_host, self.remote_dir, pre_cmds=pre_cmds, env=env)

    def run(self, argv):
        # type: (List[Text]) -> int
        """
        run executes the given command on the configured RunTarget
        """
        try:
            self.push()
            return self._run.run(argv)

        except SyncError as ex:
            LOG.error('Received error while syncing: %s', ex)
            raise

        except RunError as ex:
            LOG.error('Received error while running command: %s', ex)
            raise

        finally:
            self.pull()

    def push(self, files=None):
        # type: (Optional[Iterable[Text]]) -> int
        return self._sync.push(files)

    def pull(self, files=None):
        # type: (Optional[Iterable[Text]]) -> int
        return self._sync.pull(files)

    def shell(self):
        # type: () -> int
        return self._shell.shell()
