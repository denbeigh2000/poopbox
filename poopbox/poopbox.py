#!/usr/bin/env python3

import sys
from typing import List, Optional, Sequence, Text, Tuple

from poopbox.run import RunError, RunTarget
from poopbox.sync import SyncError, SyncTarget

class Target(object):
    def __init__(self, run_target: RunTarget, sync_target: SyncTarget) -> None:
        self.run_target = run_target
        self.sync_target = sync_target

        self.excludes = self.sync_target.excludes
        self.pwd = self.run_target.pwd

    def run(self, argv: Sequence[Text]) -> int:
        """
        run executes the given command on the configured RunTarget
        """

        try:
            with self.sync_target.sync():
                code, out, err = self.run_target.run(argv)
                if out is not None:
                    print(out)
                if err is not None:
                    print(err, file=sys.stderr)

                return code

        except SyncError:
            raise

        except RunError:
            raise
