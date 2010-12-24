#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE for details.

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
            x = 'self.do_%s = cmd' % cmd.func_name
            exec(x)

    def _setprompt(self):
        '''
        Update the prompt
        '''
        self.prompt = '%s@%s:%s$ ' % (pycoreutils._getuserhome(),
                                      platform.node(),
                                      os.getcwdu())

    def default(self, line):
        '''
        Called on an input line when the command prefix is not recognized.
        '''
        self.stdout.write('%s: command not found\n' % line.split()[0])

    def do_help(self, arg):
        self.stdout.write("\nUse 'COMMAND --help' for help\n")
        self.stdout.write("Available commands:\n")
        for cmd in pycoreutils._listcommands():
            self.stdout.write("  " + cmd + "\n")

    def emptyline(self):
        '''
        Called when an empty line is entered in response to the prompt.
        '''
        self.stdout.write('\n')

    def postcmd(self, stop, line):
        self._setprompt()

    def preloop(self):
        self._setprompt()
        self._setcommands()


if __name__ == '__main__':
    PyCoreutilsShell().cmdloop(pycoreutils._banner())
