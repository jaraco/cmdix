#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

import filecmp
import os
import os.path
import subprocess
import tempfile
import unittest

import pycoreutils


class BaseTestCase(unittest.TestCase):

    def assertSamefile(self, file1, file2):
        self.assertTrue(filecmp.cmp(file1, file2))

    def createfile(self, filename, content=None, size=64*1024, fill='0'):
        '''
        Create a temporary file of 'size' filled with 'fill'
        '''
        with open(os.path.join(self.workdir, filename), 'w') as fd:
            if content:
                fd.write(content)
            else:
                fd.write(fill * size)

    def runcommandline(self, commandline, stdin=None):
        '''
        Run commandline as a subprocess.

        :param commandline: A string containing the commandline, i.e. 'ls -l X'
        :return:            A tuple containing the unicoded stdout and stderr
        '''
        r = ''
        for line in pycoreutils.runcommandline(commandline):
            r += line
        return r

    def setUp(self):
        '''
        Create temporary work directory
        '''
        self.workdir = tempfile.mkdtemp(prefix='pycoreutilstest.')
        os.chdir(self.workdir)

    def setup_filesystem(self):
        '''
        Create the following filesystem:

        /dir1
        /dir1/dir1-1
        /dir1/dir1-1/dir1-1-1
        /dir1/dir1-1/dir1-1-1/file1-1-1-1
        /dir1/dir1-1/dir1-1-2
        /dir1/dir1-2
        /dir1/dir1-2/dir1-2-1
        /dir1/dir1-2/file1-2-1
        /dir1/dir1-2/file1-2-2
        /dir1/dir1-3
        /dir1/file1-1
        /dir1/file1-2
        /dir2
        /dir2/dir2-1
        /dir2/dir2-2
        /dir2/dir2-2/file2-2-1
        /file1
        /file2.txt
        /file3
        '''
        os.makedirs('dir1/dir1-1/dir1-1-1')
        os.makedirs('dir1/dir1-1/dir1-1-2')
        os.makedirs('dir1/dir1-2/dir1-2-1')
        os.makedirs('dir1/dir1-3')
        os.makedirs('dir2/dir2-1')
        os.makedirs('dir2/dir2-2')
        self.createfile('file1', size=111)
        self.createfile('file2.txt', size=2222)
        self.createfile('file3.empty', size=0)
        self.createfile('dir1/file1-1', size=33333)
        self.createfile('dir1/file1-2', size=44444)
        self.createfile('dir1/dir1-1/dir1-1-1/file1-1-1-1', size=55555)
        self.createfile('dir1/dir1-2/file1-2-1', size=66666)
        self.createfile('dir1/dir1-2/file1-2-2', size=77777)
        self.createfile('dir2/dir2-2/file2-2-1', size=88888)

    def tearDown(self):
        '''
        Recursively remove work directory
        '''
        for root, dirs, filenames in os.walk(self.workdir, topdown=False):
            for name in filenames:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.workdir)


def getalltests():
    '''
    Returns a testsuite containing all tests in test_*.py
    '''
    testcaselist = []
    for filename in os.listdir(os.path.abspath(os.path.dirname(__file__))):
        if filename.startswith('test_') and filename.endswith('.py'):
            testcaselist.append("pycoreutils.test." + filename.rstrip('.py'))
    return unittest.TestLoader().loadTestsFromNames(testcaselist)


def runalltests(verbosity=2):
    '''
    Run all test found by getalltests()
    '''
    unittest.TextTestRunner(verbosity=verbosity).run(getalltests())


if __name__ == '__main__':
    runalltests()
