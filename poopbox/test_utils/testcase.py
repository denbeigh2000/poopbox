#!/usr/bin/env python

import unittest

try:
    from unittest import mock
except ImportError:
    import mock

class TestCase(unittest.TestCase):
    def setUp(self):
        self.patchers = []

    def tearDown(self):
        for patcher in self.patchers:
            patcher.stop()

    def patch(self, *args, **kwargs):
        patcher = mock.patch(*args, **kwargs)
        self.patchers.append(patcher)

        return patcher

    def patch_object(self, *args, **kwargs):
        patcher = mock.patch.object(*args, **kwargs)
        self.patchers.append(patcher)

        return patcher

    def startPatchers(self):
        for patcher in self.patchers:
            patcher.start()
