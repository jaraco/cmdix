#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest
from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):
    def test_base64_decode(self):
        self.createfile('foo', content='SGF2ZSBhIGxvdCBvZiBmdW4uLi4K')
        output = self.runcommandline('base64 -d foo')[0]
        self.assertEqual(output, 'Have a lot of fun...\n')

    def test_base64_encode(self):
        self.createfile('foo', size=50)
        output = self.runcommandline('base64 -w 30 foo')[0]
        self.assertEqual(output, 'MDAwMDAwMDAwMDAwMDAwMDAwMDAwMD\n' +\
                                 'AwMDAwMDAwMDAwMDAwMDAwMDAwMDAw\n' +\
                                 'MDAwMDA=\n')


if __name__ == '__main__':
    unittest.main()
