#!/usr/bin/env python

import argparse
import logging
import os.path
import sys

from typing import Text

LOG = logging.getLogger(__name__)

def format_dir(dir_):
    # type: (Text) -> Text
    return os.path.normpath(dir_) + '/'


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        # type: (Iterable[Any], Dict[Text, Any]) -> None
        super(ArgumentParser, self).__init__(*args, **kwargs)

        self.add_argument('--log-level', help='Set the global log level',
                          default='warning',
                          choices=('critical', 'error', 'warning', 'info', 'debug'))

    def parse_args(self,
            args=None,  # type: Optional[Iterable[Text]]
            namespace=None,  # type: Optional[argparse.Namespace]
            ):
        # type: (...) -> argparse.Namespace


        args = super(ArgumentParser, self).parse_args(args, namespace)
        level = logging.getLevelName(args.log_level.upper())
        logging.basicConfig(level=level)

        return args


class PoopboxCLI(object):
    def __init__(self, prog=None, exit=True):
        # type: (Optional[Text], bool, ) -> None
        self.exit = exit
        self.prog = prog or self.__class__.__name__

    def main(self):
        # type: () -> int
        parser = self._get_parser()
        self._update_parser(parser)
        args = parser.parse_args()
        code = self._main(args)

        LOG.debug('%s exited with code %d', self.__class__.__name__, code)
        if self.exit:
            LOG.debug('exiting with code %d', code)
            sys.exit(code)

        return code

    def _get_parser(self, **kwargs):
        # type: (Dict[Text, Any]) -> argparse.ArgumentParser
        desc = kwargs.pop('description', self.__doc__)
        formatter_class = kwargs.pop('formatter_class',
                                     argparse.ArgumentDefaultsHelpFormatter)
        parser = ArgumentParser(self.prog, description=desc,
                                formatter_class=formatter_class, **kwargs)

        return parser

    def _update_parser(self, parser):
        # type: (argparse.ArgumentParser) -> None
        raise NotImplementedError('_update_parser must be overridden')

    def _main(self, args):
        # type: (argparse.Namespace) -> int
        raise NotImplementedError('_main must be overridden')
