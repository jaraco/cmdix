#!/usr/bin/env python
from __future__ import unicode_literals

import unittest
from . import BaseTestCase


class TestCase(BaseTestCase):
    def test_uuidgen(self):
        # Make sure uuid1() generates UUIDs that are actually version 1.
        for uuid in [self.runcommandline('uuidgen')[0] for i in range(10)]:
            ell = uuid.rstrip().split('-')

            # Check uuid-length
            self.assertEqual(len(uuid), 37)

            # Check if uuid ends with \n
            self.assertTrue(uuid.endswith('\n'))

            # Check split
            self.assertEqual(len(ell), 5)

            # Check if every character is hex
            for x in ell:
                for c in x:
                    self.assertTrue(0 <= int(c, 16) <= 15)


if __name__ == '__main__':
    unittest.main()
