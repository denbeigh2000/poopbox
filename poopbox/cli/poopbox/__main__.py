#!/usr/bin/env python3

import argparse
import logging

from poopbox.config.poopfile import find_and_parse_poopfile

def setup_logging() -> None:
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)

def setup_parser() -> argparse.Namespace:
    parser = argparse.ArgumentParser(prog='poopbox')
    parser.add_argument('command', choices=('push', 'pull', 'sync', 'shell', 'config'))

    return parser.parse_args()

def main() -> int:
    args = setup_parser()
    target = find_and_parse_poopfile()

    if args.command == 'shell':
        target.shell()
        return 0
    else:
        raise NotImplementedError('%s not implemented yet', args.command)

if __name__ == '__main__':
    main()
