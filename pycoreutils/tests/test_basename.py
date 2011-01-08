#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest

from pycoreutils.tests import BaseTestCase


class TestCase(BaseTestCase):
    def test_basename(self):
        self.assertEqual(
            self.runcommandline('basename foo/bar/biz'),
            'biz\n'
        )


if __name__ == '__main__':
    unittest.main()
