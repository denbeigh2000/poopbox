#!/usr/bin/env python3

from typing import Any, Dict, Iterable, Optional, List, Text

from poopbox.run import RunError
from poopbox.run.targets import SSHRunTarget
from poopbox.shell.targets import SSHShellTarget
from poopbox.sync import SyncError
from poopbox.sync.targets import RSyncSyncTarget
from poopbox.target import Target

class RSyncSSHTarget(Target):
    def _run_on_configure(self, config: Dict[Any, Any]) -> None:
        self.remote_host = config['remote_host']
        self.remote_dir = config['remote_dir']

        excludes = config.get('excludes', None)

        self._sync = RSyncSyncTarget(self.poopdir,
                self.remote_host, self.remote_dir, excludes)
        self._run = SSHRunTarget(self.remote_host, self.remote_dir)
        self._shell = SSHShellTarget(self.remote_host, self.remote_dir)

    def run(self, argv: List[Text]) -> int:
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

    def push(self, files: Optional[Iterable[Text]] = None) -> None:
        return self._sync.push(files)

    def pull(self, files: Optional[Iterable[Text]] = None) -> None:
        return self._sync.pull(files)

    def shell(self):
        return self._shell.shell()
