#!/usr/bin/env python
from __future__ import unicode_literals

import unittest

from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_basename(self):
        self.assertEqual(
            self.runcommandline('basename foo/bar/biz')[0],
            'biz\n')


if __name__ == '__main__':
    unittest.main()
