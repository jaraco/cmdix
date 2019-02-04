#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest
import pycoreutils

from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):
    def test_getcommand(self):
        for cmd in pycoreutils.command.__all__:
            pycoreutils.getcommand(cmd[4:])


if __name__ == '__main__':
    unittest.main()
