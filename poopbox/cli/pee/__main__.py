#!/usr/bin/env python

import argparse
import logging
import sys

from poopbox.config.poopfile import find_and_parse_poopfile
from poopbox.utils import PoopboxCLI

class P(PoopboxCLI):
    """Executes the given command on the remote machine"""
    def _update_parser(self, parser):
        parser.add_argument('argv', nargs='+',
                            help='Remote command to run')

    def _main(self, args):
        # type: (argparse.Namespace) -> int

        target = find_and_parse_poopfile()
        # forward status code from remote
        return target.run(args.argv)

def main():
    # type: () -> None
    maybe_binary_name = sys.argv[0].split('/')[-1]
    prog = 'p' if '__' in maybe_binary_name else maybe_binary_name
    
    P(prog=prog).main()

if __name__ == '__main__':
    main()
