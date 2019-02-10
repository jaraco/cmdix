#!/usr/bin/env python
from __future__ import unicode_literals

import gzip
import unittest
from . import BaseTestCase


class TestCase(BaseTestCase):

    def test_cat(self):
        self.createfile('foo', size=66666)
        self.assertEqual(self.runcommandline('cat foo')[0], '0' * 66666)

    def test_cat_gz(self):
        f = gzip.GzipFile('foo.gz', 'wb')
        f.write(b'0' * 12345)
        f.close()
        self.assertEqual(self.runcommandline('cat foo.gz')[0], '0' * 12345)

    def test_cat_stdin(self):
        self.setStdin('foo' * 1000)
        self.assertEqual(self.runcommandline('cat')[0], 'foo' * 1000)


if __name__ == '__main__':
    unittest.main()
