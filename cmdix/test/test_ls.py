#!/usr/bin/env python
from __future__ import unicode_literals

import os
import stat
import time
import unittest
import textwrap

from . import BaseTestCase
from . import py27compat


class TestCase(BaseTestCase):
    def test_ls(self):
        self.setup_filesystem()
        self.assertEqual(
            self.runcommandline('ls')[0],
            'dir1\ndir2\nfile1\nfile2.txt\nfile3.empty\n'
        )

    def test_ls_l(self):
        py27compat.mkdir('biz', mode=0o755)
        self.createfile('foo', size=100)
        self.createfile('bar', size=999999)
        os.chmod(
            'bar',
            stat.S_IWUSR +
            stat.S_IRGRP +
            stat.S_IWOTH +
            stat.S_IXOTH
        )
        os.chmod('foo', 0o644)

        dirsize = os.stat('biz').st_size
        uid = os.getuid()
        gid = os.getgid()
        date = time.strftime('%Y-%m-%d %H:%m', time.localtime())
        out = self.runcommandline('ls -l')[0]
        expected = textwrap.dedent("""
            --w-r---wx 1 {uid:<5} {gid:<5} 999999 {date} bar
            drwxr-xr-x 2 {uid:<5} {gid:<5} {dirsize:>6} {date} biz
            -rw-r--r-- 1 {uid:<5} {gid:<5}    100 {date} foo
            """).lstrip().format(**locals())
        assert out == expected


if __name__ == '__main__':
    unittest.main()
