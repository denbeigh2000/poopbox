#!/usr/bin/env python3

import sys

from poopbox.config.poopfile import find_and_parse_poopfile

def main() -> int:
    args = list(sys.argv)
    assert len(args) > 1, 'must provide commands to run!'

    target = find_and_parse_poopfile()

    # forward status code from remote
    return target.run(args[1:])


if __name__ == '__main__':
    main()
