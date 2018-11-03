#!/usr/bin/env python

import logging
import os
import sys
from typing import Dict, Any, Iterable, List, Optional, Text

from poopbox.utils import format_dir

LOG = logging.getLogger('poopbox.py')

class Target():
    def __init__(self, poopdir):
        # type: (Text) -> None
        self.poopdir = format_dir(poopdir)
        self.cachedir_name = '.poopbox'
        self.cachedir = os.path.join(self.poopdir, self.cachedir_name)
        self.configured = False

        if not os.path.isdir(self.cachedir):
            os.mkdir(self.cachedir)

    def _run_on_configure(self, config):
        # type: (Dict[Any, Any]) -> None
        """
        Called once on configuration when the local poopfile is read. Subclasses
        should perform any initial setup and config option parsing here.
        """
        raise NotImplementedError('_run_on_configure() must be implemented')

    def configure(self, config):
        # type: (Dict[Any, Any]) -> None
        """
        configure initialises the Target from the options in the found poopfile.
        """
        self.configured = True
        self._run_on_configure(config)

    def run(self, argv):
        # type: (List[Text]) -> int
        """
        run executes the given command on the configured RunTarget, while
        syncing any changes to and from your remote workstation around it.

        Returns the status code from the remote command.
        """
        raise NotImplementedError('run() must be implemented')

    def push(self, files=None):
        # type: (Optional[Iterable[Text]]) -> None
        """
        push pushes local changes to the remote workstation
        """
        raise NotImplementedError('pull() must be implemented')

    def pull(self, files=None):
        # type: (Optional[Iterable[Text]]) -> None
        """
        pull pull local changes from the remote workstation
        """
        raise NotImplementedError('pull() must be implemented')

    def shell(self):
        # type: () -> int
        """
        shell starts an interactive shell on the remote workstation
        """
        raise NotImplementedError('shell() must be implemented')
