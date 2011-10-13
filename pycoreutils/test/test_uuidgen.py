#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest
from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):
    def test_uuidgen(self):
        # Make sure uuid1() generates UUIDs that are actually version 1.
        for uuid in [self.runcommandline('uuidgen')[0] for i in range(10)]:
            l = uuid.rstrip().split('-')

            # Check uuid-length
            self.assertEqual(len(uuid), 37)

            # Check if uuid ends with \n
            self.assertTrue(uuid.endswith('\n'))

            # Check split
            self.assertEqual(len(l), 5)

            # Check if every character is hex
            for x in l:
                for c in x:
                    0 <= int(c, 16) <= 15


if __name__ == '__main__':
    unittest.main()
