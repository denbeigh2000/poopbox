#!/usr/bin/env python

import os.path

from typing import Text

def format_dir(dir_):
    # type: (Text) -> Text
    return os.path.normpath(dir_) + '/'
