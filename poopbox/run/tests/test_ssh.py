#!/usr/bin/env python

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from poopbox.run.ssh import SSHRunTarget
from poopbox.test_utils.testcase import TestCase

class TestSSHRunTarget(TestCase):
    def setUp(self):
        super(TestSSHRunTarget, self).setUp()

        self.build_dir = 'build/test'
        self.build_host = 'abc-123-test.example.org'
        self.target = SSHRunTarget(self.build_host, self.build_dir)

        self.client = Mock()
        self.target._get_client = Mock(return_value=self.client)

        # self.patch_object(self.target, '_run_paramiko_cmd', return_value=0)
        self.target._run_paramiko_cmd = Mock()
        self.target._run_paramiko_cmd.return_value = 0

        self.startPatchers()

    # def test_basic_run(self):
    #     assert self.target.run(['echo', 'hello', 'world']) == 0

    #     self.client.close.assert_called_once_with()
    #     self.assertTrue(self.target._run_paramiko_cmd.called)
    #     expected_cmd = ('ssh {host} mkdir -p {dir} && cd {dir} && '
    #         'bash --rcfile /dev/null -c "echo hello world'
    #     ).format(host=self.build_host, dir=self.build_dir)

    #     self.assertIn(expected_cmd, self.target._run_paramiko_cmd.call_args)

    def set_inner_cmd_str(self):
        self.assertEqual(
            self.target._create_inner_cmd_str(['echo', 'hello', 'world']),
            'mkdir -p {} && cd {} && echo hello world'
        )
