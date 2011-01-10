#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest

from pycoreutils.test import BaseTestCase

testdata = '''
foo bar

biz
 '''

class TestCase(BaseTestCase):
    def test_nl(self):
        self.createfile('foo', content=testdata)
        self.assertEqual(
            self.runcommandline('nl foo'),
            '       \n     1\tfoo bar\n       \n     2\tbiz\n     3\t ')

    def test_nl_s(self):
        self.createfile('foo', content=testdata)
        self.assertEqual(
            self.runcommandline('nl -s XYZ foo'),
            '         \n     1XYZfoo bar\n         \n     2XYZbiz\n     3XYZ ')

    def test_nl_w(self):
        self.createfile('foo', content=testdata)
        self.assertEqual(
            self.runcommandline('nl -w 2 foo'),
            '   \n 1\tfoo bar\n   \n 2\tbiz\n 3\t ')


if __name__ == '__main__':
    unittest.main()
