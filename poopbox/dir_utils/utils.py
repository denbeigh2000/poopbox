#!/usr/bin/env python3

import os.path

from typing import Text

def format_dir(dir_: Text) -> Text:
    return os.path.normpath(dir_) + '/'
