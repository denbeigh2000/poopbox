#!/usr/bin/env python3

import logging
import sys
from typing import Dict, Any, Iterable, List, Optional, Text

from poopbox.dir_utils import format_dir
from poopbox.run.run import RunError, RunTarget
from poopbox.sync.sync import SyncError, SyncTarget

LOG = logging.getLogger('poopbox.py')

class NewTarget():
    def __init__(self, poopdir: Text, excludes: Optional[Iterable[Text]] = None) -> None:
        self.excludes = list(excludes) if excludes is not None else []
        self.poopdir = format_dir(poopdir)

        self.configured = False

    def _run_on_configure(self, config: Dict[Any, Any]) -> None:
        """
        Called once on configuration when the local poopfile is read. Subclasses
        should perform any initial setup and config option parsing here.
        """
        raise NotImplementedError('_run_on_configure() must be implemented')

    def configure(self, config: Dict[Any, Any]) -> None:
        """
        configure initialises the Target from the options in the found poopfile.
        """
        self.configured = True
        self._run_on_configure(config)

    def run(self, argv: List[Text]) -> int:
        """
        run executes the given command on the configured RunTarget, while
        syncing any changes to and from your remote workstation around it.

        Returns the status code from the remote command.
        """
        raise NotImplementedError('run() must be implemented')

    def push(self, files: Optional[Iterable[Text]] = None) -> None:
        """
        push pushes local changes to the remote workstation
        """
        raise NotImplementedError('pull() must be implemented')

    def pull(self, files: Optional[Iterable[Text]] = None) -> None:
        """
        pull pull local changes from the remote workstation
        """
        raise NotImplementedError('pull() must be implemented')

    def shell(self) -> None:
        """
        shell starts an interactive shell on the remote workstation
        """
        raise NotImplementedError('shell() must be implemented')

    def sync(self) -> None:
        """
        sync performs a push then pull with the remote workstration
        """
        raise NotImplementedError('sync() must be implemented')



class Target():
    def __init__(self, run_target: RunTarget, sync_target: SyncTarget,
                 poopdir: Text, excludes: Optional[Iterable[Text]] = None) -> None:
        self.run_target = run_target
        self.sync_target = sync_target
        self.poopdir = format_dir(poopdir)

        self.excludes = list(excludes) if excludes is not None else []
        self.sync_target.set_excludes(self.excludes)
        self.sync_target.set_poopdir(poopdir)

    def init(self) -> int:
        try:
            self.run_target.run(['echo', 'poopbox is ready to rock n\\\' roll!'])

        except RunError as ex:
            LOG.error('poopbox was not able to successfully run on the remote '
                      'workstation: %s', ex)
            raise

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
