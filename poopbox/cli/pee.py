#!/usr/bin/env python3

import sys
from typing import List, Text

from poopbox.config.poopfile import find_and_parse_poopfile

def main(args: List[Text]) -> None:
    assert len(args) > 1, 'must provide commands to run!'

    target = find_and_parse_poopfile()
    target.run(args[1:])


if __name__ == '__main__':
    main(sys.argv)
