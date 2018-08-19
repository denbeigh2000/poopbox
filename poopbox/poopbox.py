#!/usr/bin/env python3

import logging
import sys
from typing import Iterable, List, Optional, Text

from poopbox.dir_utils import format_dir
from poopbox.run.run import RunError, RunTarget
from poopbox.sync.sync import SyncError, SyncTarget

LOG = logging.getLogger('poopbox.py')

class Target():
    def __init__(self, run_target: RunTarget, sync_target: SyncTarget,
                 poopdir: Text, excludes: Optional[Iterable[Text]] = None) -> None:
        self.run_target = run_target
        self.sync_target = sync_target
        self.poopdir = format_dir(poopdir)

        self.excludes = list(excludes) if excludes is not None else []
        self.sync_target.set_excludes(self.excludes)
        self.sync_target.set_poopdir(poopdir)

    def run(self, argv: List[Text]) -> int:
        """
        run executes the given command on the configured RunTarget
        """

        try:
            with self.sync_target.sync():
                return self.run_target.run(argv)

        except SyncError as ex:
            LOG.error('Received error while syncing: %s', ex)
            raise

        except RunError as ex:
            LOG.error('Received error while running command: %s', ex)
            raise

    def push(self, files: Optional[Iterable[Text]] = None) -> None:
        return self.sync_target.push(files)

    def pull(self, files: Optional[Iterable[Text]] = None) -> None:
        return self.sync_target.pull(files)

    def shell(self):
        return self.run_target.shell()
