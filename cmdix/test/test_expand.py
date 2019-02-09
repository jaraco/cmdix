#!/usr/bin/env python
from __future__ import unicode_literals

import unittest

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_expand(self):
        self.createfile('foo', fill='\t', size=100)
        self.assertEqual(
            self.runcommandline('expand foo')[0],
            ' ' * 100 * 8
        )

    def test_expand_t(self):
        self.createfile('foo', fill='\t', size=100)
        self.assertEqual(
            self.runcommandline('expand -t 4 foo')[0],
            ' ' * 100 * 4
        )


if __name__ == '__main__':
    unittest.main()
