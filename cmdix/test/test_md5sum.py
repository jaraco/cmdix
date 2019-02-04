#!/usr/bin/env python
from __future__ import unicode_literals

import unittest

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_simple(self):
        self.createfile('foo')
        self.assertEqual(
            self.runcommandline('md5sum foo')[0],
            'cf4b5c51a442990ed7304b535c9468c4  foo\n'
        )


if __name__ == '__main__':
    unittest.main()
