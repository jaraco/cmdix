#!/usr/bin/env python
from __future__ import unicode_literals
from . import BaseTestCase
import unittest


class TestCase(BaseTestCase):

    def test_tail(self):
        self.createfile('foo', size=4096, fill='foo\n')
        self.assertEqual(self.runcommandline('tail foo')[0], 'foo\n' * 10)

    def test_tail_small(self):
        self.createfile('foo', size=4096, fill='foo\n')
        self.assertEqual(self.runcommandline('tail -n2 foo')[0], 'foo\n' * 2)


if __name__ == '__main__':
    unittest.main()
