#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE.txt for details.

import os
import os.path
import subprocess
import tempfile
import unittest

import pycoreutils


class BaseTestCase(unittest.TestCase):

    def setUp(self):
        self.workdir = tempfile.mkdtemp(prefix='pycoreutilstest.')
        with open(os.path.join(self.workdir, 'testfile1'), 'w') as testfile1:
            for i in range(1000000):
                testfile1.write(str(i))

    def tearDown(self):
        # Remove work directory recursively
        for root, dirs, files in os.walk(self.workdir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.workdir)

    def _run(self, cmd):
        subprocess.Popen('ls')

    def test_ls(self):
        self._run('ls /tmp')


if __name__ == '__main__':
    #unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(PyCoreutilsTestCase)
    unittest.TextTestRunner(verbosity=2).run(suite)
