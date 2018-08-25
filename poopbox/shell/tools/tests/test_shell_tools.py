#!/usr/bin/python

try:
    from unittest.mock import Mock
except ImportError:
    from mock import Mock

from collections import OrderedDict

from poopbox.shell.tools.shell_tools import (
    create_env_commands,
    chain_commands,
)

from poopbox.test_utils.testcase import TestCase

class TestShellTools(TestCase):
    def test_pre_commands(self):
        commands = [
            ['echo', 'hello', 'world'],
            ['compile', 'my', 'code'],
            ['curl', 'www.google.com', '>', 'google.html']
        ]

        command_list = chain_commands(commands)

        self.assertEqual(command_list, [
            'echo', 'hello', 'world', '&&', 'compile', 'my', 'code', '&&',
            'curl', 'www.google.com', '>', 'google.html', '&&'
        ])

    def test_env_commands(self):
        env = OrderedDict([
            ('HOME', '/home/test',),
            ('PWD', '/home/test',),
            ('SHELL', '/bin/zsh',),
        ])

        self.assertEqual(create_env_commands(env), [
            ['export', 'HOME="/home/test"'],
            ['export', 'PWD="/home/test"'],
            ['export', 'SHELL="/bin/zsh"'],
        ])
