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

def configure_pushpull(is_push: bool, parser: argparse.ArgumentParser):
    def go(target: Target, args: argparse.Namespace):
        fn = target.push if is_push else target.pull
        return fn(args.files)

    parser.add_argument('files', nargs='*', default=None)
    parser.set_defaults(func=go)

def handle_shell(target: Target, args: argparse.Namespace):
    return target.shell()

def setup_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='poopbox')
    subparsers = parser.add_subparsers()

    shell_parser = subparsers.add_parser('shell')
    shell_parser.set_defaults(func=handle_shell)

    configure_pushpull(True, subparsers.add_parser('push'))
    configure_pushpull(False, subparsers.add_parser('pull'))

    return parser.parse_args()

def main() -> int:
    target = find_and_parse_poopfile()
    args = setup_parser()

    args.func(target, args)

    return 0

if __name__ == '__main__':
    main()
