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

    def createfile(self, filename, size=1048576, fill='0'):
        '''
        Create a temporary file of 'size' filled with 'fill'
        '''
        with open(os.path.join(self.workdir, filename), 'w') as fd:
                fd.write(fill * size)

    def runcommandline(self, commandline, stdin=None):
        '''
        Run commandline as a subprocess.

        :param commandline: A string containing the commandline, i.e. 'ls -l X'
        :return:            A tuple containing the unicoded stdout and stderr
        '''
        stdout, stderr = subprocess.Popen(commandline.split(),
                                          stdout=subprocess.PIPE,
                                          stderr=subprocess.PIPE
                                         ).communicate(stdin)
        return stdout.decode('utf8'), stderr.decode('utf8')

    def setUp(self):
        '''
        Create temporary work directory
        '''
        self.workdir = tempfile.mkdtemp(prefix='pycoreutilstest.')
        os.chdir(self.workdir)

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
            testcaselist.append("pycoreutils.tests." + filename.rstrip('.py'))
    return unittest.TestLoader().loadTestsFromNames(testcaselist)


def runalltests(verbosity=2):
    '''
    Run all test found by getalltests()
    '''
    unittest.TextTestRunner(verbosity=verbosity).run(getalltests())


if __name__ == '__main__':
    runalltests()
