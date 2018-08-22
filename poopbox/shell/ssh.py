from poopbox.shell import ShellTarget

import subprocess
import sys
from typing import Text

class SSHShellTarget(ShellTarget):
    def __init__(self, remote_host: Text, remote_dir: Text):
        self.remote_host = remote_host
        self.remote_dir = remote_dir

    def shell(self):
        remote_args = ['cd', self.remote_dir, '&&', 'exec', '$SHELL', '-l']
        args = ['ssh', '-t', self.remote_host, ' '.join(remote_args)]
        proc = subprocess.Popen(args, stdin=sys.stdin, stdout=sys.stdout,
                                stderr=sys.stderr)
        sys.stdin.flush()
        proc.wait()
