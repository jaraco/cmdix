#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import bz2
import gzip
import unittest
from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):

    def test_cat(self):
        self.createfile('foo', size=66666)
        self.assertEqual(self.runcommandline('cat foo'), '0' * 66666)

    def test_cat_gz(self):
        f = gzip.GzipFile('foo.gz', 'wb')
        f.write(b'0' * 12345)
        f.close()
        self.assertEqual(self.runcommandline('cat foo.gz'), b'0' * 12345)

    def test_cat_stdin(self):
        self.setStdin('foo' * 1000)
        self.assertEqual(self.runcommandline('cat'), 'foo' * 1000)


if __name__ == '__main__':
    unittest.main()
