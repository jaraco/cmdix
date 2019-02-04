#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals
from pycoreutils.test import BaseTestCase
import os
import pycoreutils
import unittest


class TestCase(BaseTestCase):
    def test_onlyunix(self):
        for command in ['chmod', 'chown', 'id', 'ln', 'login', 'mount', 'tee',
                        'uptime', 'whoami']:
            os.name = 'nt'
            self.assertRaises(pycoreutils.CommandNotFoundException,
                              pycoreutils.getcommand, command)


if __name__ == '__main__':
    unittest.main()
