#!/usr/bin/env python

import argparse
import logging

from poopbox.config.poopfile import find_and_parse_poopfile
from poopbox.target import Target

def setup_logging():
    # type: () -> None
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)

def configure_pushpull(is_push, parser):  # type: ignore
    def go(target, args):
        # type: (Target, argparse.Namespace) -> None
        fn = target.push if is_push else target.pull
        fn(args.files)

    help_text = 'Push any changes from here to the remote workstation' \
        if is_push else 'Pull any changes from the remote workstation to here'

    sparser = parser.add_parser('push' if is_push else 'pull', help=help_text)
    sparser.add_argument('files', nargs='*', default=None, help='files to be transferred')
    sparser.set_defaults(func=go)

def handle_shell(target, args):
    # type: () -> int
    return target.shell()

def handle_sync(target, args):
    # type: () -> None
    target.sync()

def setup_parser():
    # type: () -> argparse.Namespace
    parser = argparse.ArgumentParser(prog='poopbox')
    subparsers = parser.add_subparsers()

    shell_parser = subparsers.add_parser('shell',
            help='Open an interactive shell in your remote build directory')
    shell_parser.set_defaults(func=handle_shell)

    ssh_parser = subparsers.add_parser('ssh', help='alias of "shell"')
    ssh_parser.set_defaults(func=handle_shell)

    shell_parser = subparsers.add_parser('sync', help='Synchronise any changes between your '
                                         'local and remote environments')
    shell_parser.set_defaults(func=handle_sync)

    configure_pushpull(True, subparsers)
    configure_pushpull(False, subparsers)

    return parser.parse_args()

def main():
    # type: () -> int
    target = find_and_parse_poopfile()
    args = setup_parser()

    args.func(target, args)

    return 0

if __name__ == '__main__':
    main()
