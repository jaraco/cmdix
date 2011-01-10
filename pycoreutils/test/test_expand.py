#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest

from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):
    def test_expand(self):
        self.createfile('foo', fill='\t', size=100)
        self.assertEqual(
            self.runcommandline('expand foo'),
            ' ' * 100 * 8
        )

    def test_expand_t(self):
        self.createfile('foo', fill='\t', size=100)
        self.assertEqual(
            self.runcommandline('expand -t 4 foo'),
            ' ' * 100 * 4
        )

if __name__ == '__main__':
    unittest.main()
