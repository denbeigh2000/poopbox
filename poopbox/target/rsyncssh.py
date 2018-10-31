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
from poopbox.sync import SyncError
from poopbox.sync.targets import RSyncSyncTarget
from poopbox.target import Target

LOG = logging.getLogger('rsyncssh.py')

class RSyncSSHTarget(Target):
    NO_SYNCFILE_SENTINEL = 'NO_SYNCFILE'

    def _run_on_configure(self, config):
        # type: (Dict[Any, Any]) -> None
        self.remote_host = config['remote_host']
        self.remote_dir = config['remote_dir']

        excludes = config.get('excludes', None)
        pre_cmds = config.get('pre_cmds', None)
        env = config.get('env', None)

        self.remote_cachedir = os.path.join(self.remote_dir, self.cachedir_name)

        self.syncfile = os.path.join(self.cachedir, 'lsyncfile')
        self.remote_syncfile = os.path.join(self.remote_cachedir, 'rsyncfile')

        self._sync = RSyncSyncTarget(self.poopdir,
                self.remote_host, self.remote_dir, excludes)
        self._run = SSHRunTarget(self.remote_host, self.remote_dir, pre_cmds=pre_cmds, env=env)
        self._shell = SSHShellTarget(self.remote_host, self.remote_dir, pre_cmds=pre_cmds, env=env)

        self._ssh_tooling = SSHTooling(self.remote_host)

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
        code = self._sync.push(files)
        self._touch_syncfile()
        self._touch_remote_syncfile()
        return code

    def pull(self, files=None):
        # type: (Optional[Iterable[Text]]) -> int
        if files is None:
            files = self._find_remote_sync_files()
            if files is not None and len(files) == 0:
                LOG.info('Found no files to sync, not syncing.')
                return 0

        code = self._sync.pull(files)
        self._touch_remote_syncfile()
        return code

    def shell(self):
        # type: () -> int
        return self._shell.shell()

    def _touch_syncfile(self):
        # type: () -> None
        if os.path.isfile(self.syncfile):
            os.unlink(self.syncfile)

        try:
            cmd = ['touch', self.syncfile]
            LOG.debug('running %s', cmd)
            proc = subprocess.run(cmd)
            proc.check_returncode()
        except Exception as e:
            LOG.warning('Received error while touching syncfile, continuing', e)

    def _touch_remote_syncfile(self):
        remote_cmd = ['rm', '-f', self.remote_syncfile + ';', 'touch', self.remote_syncfile]
        inner_cmd = ' '.join(remote_cmd)
        cmd = self._ssh_tooling.form_command(' '.join(['sh', '-c', "'" + inner_cmd + "'"]))
        LOG.debug(cmd)
        subprocess.run(cmd, stdout=sys.stdout, stderr=sys.stderr)

    def _find_remote_sync_files_cmd(self):
        # type: () -> List[Text]
        """
        Returns a find command that finds files newer than the syncfile on the
        remote machine.
        """

        file_test = '([[ -f {} ]] || (echo "{}" && exit 1))'.format(
                self.remote_syncfile, self.NO_SYNCFILE_SENTINEL)

        inner_cmd = ' '.join([
            file_test, '&&',
            'find', self.remote_dir,
                '-newer', self.remote_syncfile,
                '-printf', r'%f\\n',
                '!', '-path', self.remote_dir,
        ])

        return self._ssh_tooling.form_command(' '.join(['bash', '-c', "'" + inner_cmd + "'"]))

    def _find_remote_sync_files(self):
        # type: () -> Optional[Iterable[Text]]
        """
        Finds files on the remote newer than the remote syncfile. If there is no
        syncfile, returns None. If there are no other files to sync, returns
        empty list.

        Aside: I did try to come up with a better solution than ssh-ing over,
        finding new files, then running rsync from this side... but even if
        I were to break the abstraction and pass the SSHTarget to the
        RSyncSyncTarget, we would still need to assume this host is running an
        SSH server on 22 with passwordless auth
        """

        find_cmd = self._find_remote_sync_files_cmd()

        proc = subprocess.run(find_cmd, capture_output=True)
        if proc.returncode != 0:
            LOG.warning('find returned nonzero, falling back to native rsync checksumming')
            return None

        if proc.stdout.strip() == self.NO_SYNCFILE_SENTINEL:
            return None

        return [str(line).strip() for line in proc.stdout.decode('utf-8').split('\n') if line]
