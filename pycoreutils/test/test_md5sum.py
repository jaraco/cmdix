#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import unittest

from pycoreutils.test import BaseTestCase


class TestCase(BaseTestCase):
    def test_simple(self):
        self.createfile('foo')
        self.assertEqual(
            self.runcommandline('md5sum foo'),
            'cf4b5c51a442990ed7304b535c9468c4  foo\n'
        )


if __name__ == '__main__':
    unittest.main()
