#!/usr/bin/env python
from __future__ import unicode_literals

import unittest

from . import BaseTestCase

testdata = '''
foo bar

biz
 '''


class TestCase(BaseTestCase):
    def test_nl(self):
        self.createfile('foo', content=testdata)
        self.assertEqual(
            self.runcommandline('nl foo')[0],
            '       \n     1\tfoo bar\n       \n     2\tbiz\n     3\t ')

    def test_nl_s(self):
        self.createfile('foo', content=testdata)
        self.assertEqual(
            self.runcommandline('nl -s XYZ foo')[0],
            '         \n     1XYZfoo bar\n         \n     2XYZbiz\n     3XYZ ')

    def test_nl_w(self):
        self.createfile('foo', content=testdata)
        self.assertEqual(
            self.runcommandline('nl -w 2 foo')[0],
            '   \n 1\tfoo bar\n   \n 2\tbiz\n 3\t ')


if __name__ == '__main__':
    unittest.main()
