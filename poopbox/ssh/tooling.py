#!/usr/bin/env python

from typing import Dict, List, Optional, Text, Union

Options = Dict[Text, Union[Text, List[Text]]]

class SSHTooling(object):
    def __init__(self, remote_host, extra_options=None):
        # type: (Text, Optional[Options]) -> None
        self.remote_host = remote_host
        extras = extra_options if extra_options else {}
        self.default_options = dict({
            'LogLevel': 'QUIET',
        }, **extras)

    def form_command(self, command=None, options=None):
        # type: (Text, Optional[Text], Optional[Options]) -> List[Text]
        opts = self._form_options(options)
        cmd = [command] if command else []
        return [ 'ssh', '-t' ] + opts + [ self.remote_host ] + cmd

    def _form_options(self, extra=None):
        # type: (Optional[Options]) -> List[Text]
        """
        Returns a set of options with the -o flag in a flat array, suitable
        for combining into an argv array
        """
        options = dict(self.default_options, **extra) \
                if extra \
                else self.default_options

        items = []
        for k, v in options.items():
            if isinstance(v, list):
                for option in v:
                    items.extend(['-o', '{}={}'.format(k, option)])
            else:
                items.extend(['-o', '{}={}'.format(k, v)])

        return items
