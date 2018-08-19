#!/usr/bin/env python3

import argparse
import logging

from poopbox.config.poopfile import find_and_parse_poopfile
from poopbox import Target

def setup_logging() -> None:
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)

def configure_pushpull(is_push: bool, parser: argparse.Action):
    def go(target: Target, args: argparse.Namespace):
        fn = target.push if is_push else target.pull
        return fn(args.files)

    help_text = 'Push any changes from here to the remote workstation' \
        if is_push else 'Pull any changes from the remote workstation to here'

    sparser = parser.add_parser('push' if is_push else 'pull', help=help_text)
    sparser.add_argument('files', nargs='*', default=None, help='files to be transferred')
    sparser.set_defaults(func=go)

def handle_init(target: Target, args: argparse.Namespace):
    return target.init()

def handle_shell(target: Target, args: argparse.Namespace):
    return target.shell()

def handle_sync(target: Target, args: argparse.Namespace):
    return target.sync()

def setup_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='poopbox')
    subparsers = parser.add_subparsers()

    shell_parser = subparsers.add_parser('shell', help='Open an interactive shell in your '
                                                       'remote build directory')
    shell_parser.set_defaults(func=handle_shell)

    shell_parser = subparsers.add_parser('sync', help='Synchronise any changes between your '
                                         'local and remote environments')
    shell_parser.set_defaults(func=handle_sync)

    shell_parser = subparsers.add_parser('init', help='Ensures your remote environment is reachable'
                                                      'and the build directory exists.')
    shell_parser.set_defaults(func=handle_init)

    configure_pushpull(True, subparsers)
    configure_pushpull(False, subparsers)

    return parser.parse_args()

def main() -> int:
    target = find_and_parse_poopfile()
    args = setup_parser()

    args.func(target, args)

    return 0

if __name__ == '__main__':
    main()
