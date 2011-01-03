#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals

import cmd
import os
import platform
import sys

import pycoreutils


class PyCoreutilsShell(cmd.Cmd):

    def _setcommands(self):
        '''
        Copy all the commands to a 'do_foo' function, so it fits in the
        framework
        '''
        for cmd in pycoreutils._cmds:
            x = 'self.do_%s = cmd' % cmd.__name__
            exec(x)

    def _setprompt(self):
        '''
        Update the prompt
        '''
        self.prompt = '%s@%s:%s$ ' % (pycoreutils.getcurrentusername(),
                                      platform.node(),
                                      os.getcwd())

    def default(self, line):
        '''
        Called on an input line when the command prefix is not recognized.
        '''
        print('%s: command not found' % line.split()[0])

    def do_help(self, arg):
        print("\nUse 'COMMAND --help' for help")
        print("Available commands:")
        for cmd in pycoreutils.listcommands():
            print("  " + cmd)

    def emptyline(self):
        '''
        Called when an empty line is entered in response to the prompt.
        '''
        print()

    def postcmd(self, stop, line):
        self._setprompt()
        if stop:
            for l in stop:
                print(l, end='')

    def preloop(self):
        self._setprompt()
        self._setcommands()


if __name__ == '__main__':
    PyCoreutilsShell().cmdloop(pycoreutils.showbanner(width=80))
