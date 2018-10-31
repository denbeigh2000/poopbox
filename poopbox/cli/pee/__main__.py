#!/usr/bin/env python

import logging
import sys

from poopbox.config.poopfile import find_and_parse_poopfile

def setup_logging():
    # type: () -> None
    logger = logging.getLogger()
    handler = logging.StreamHandler()
    logger.setLevel(logging.WARNING)
    logger.addHandler(handler)


def main():
    # type: () -> int
    setup_logging()

    args = list(sys.argv)
    assert len(args) > 1, 'must provide commands to run!'

    target = find_and_parse_poopfile()

    # forward status code from remote
    return target.run(args[1:])


if __name__ == '__main__':
    sys.exit(main())
