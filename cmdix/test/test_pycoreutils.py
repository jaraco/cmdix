#!/usr/bin/env python
from __future__ import unicode_literals

import unittest

import cmdix

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_getcommand(self):
        for cmd in cmdix.command.__all__:
            cmdix.getcommand(cmd[4:])


if __name__ == '__main__':
    unittest.main()
