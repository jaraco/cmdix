#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest

from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):
    def test_simple(self):
        self.createfile('foo')
        self.assertEqual(
            self.runcommandline('md5sum foo'),
            'd8d4c2d1c8e4b04d96bca23175d071c5  foo\n'
        )


if __name__ == '__main__':
    unittest.main()
