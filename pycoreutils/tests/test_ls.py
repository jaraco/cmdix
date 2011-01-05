#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE.txt for details.

from __future__ import unicode_literals

import os
import stat
import time
import unittest

import pycoreutils
from pycoreutils.tests import BaseTestCase


class TestCase(BaseTestCase):
    def test_simple(self):
        os.mkdir('biz')
        self.createfile('foo', 100)
        self.createfile('bar', 100)
        self.assertEqual(
            self.runcommandline('ls')[0],
            'bar\nbiz\nfoo\n'
        )

    def test_ls_l(self):
        os.mkdir('biz')
        self.createfile('foo', 100)
        self.createfile('bar', 999999)
        os.chmod('bar',
                    stat.S_IWUSR +\
                    stat.S_IRGRP +\
                    stat.S_IWOTH +\
                    stat.S_IXOTH
        )

        uid = 1000
        gid = 1000
        date = time.strftime('%Y-%m-%d %H:%m', time.localtime())
        self.assertEqual(
            self.runcommandline('ls -l')[0],
            '--w-r---wx 1 {0}  {1}  999999 {2} bar\n'.format(uid, gid, date) +\
            'drwxr-xr-x 2 {0}  {1}      40 {2} biz\n'.format(uid, gid, date) +\
            '-rw-r--r-- 1 {0}  {1}     100 {2} foo\n'.format(uid, gid, date)
        )

if __name__ == '__main__':
    unittest.main()
