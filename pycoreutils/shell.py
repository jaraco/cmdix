#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals

import cmd
import os
import platform
import pprint
import sys

import pycoreutils


class PyCoreutilsShell(cmd.Cmd):

    exitstatus = 0

    def default(self, line):
        '''
        Called on an input line when the command prefix is not recognized.
        '''
        self.exitstatus = pycoreutils.run(line.split())

    def do_exit(self, n=None):
        '''
        Exit the shell.

        Exits the shell with a status of N.  If N is omitted, the exit status
        is that of the last command executed.
        '''
        sys.exit(n or self.exitstatus)

    def do_help(self, arg):
        print("\nUse 'COMMAND --help' for help")
        print("Available commands:")
        for cmd in pycoreutils.listcommands():
            print("  " + cmd)

    def do_shell(self, line):
        '''
        Run when them command is '!' or 'shell'.
        Execute the line using the Python interpreter.
        i.e. "!dir()"
        '''
        try:
            exec("pprint.pprint({0})".format(line))
        except Exception as err:
            pprint.pprint(err)

    def emptyline(self):
        '''
        Called when an empty line is entered in response to the prompt.
        '''
        print()

    def postcmd(self, stop, line):
        self.updateprompt()
        if stop:
            for l in stop:
                print(l, end='')

    def preloop(self):
        self.updateprompt()

    def updateprompt(self):
        '''
        Update the prompt
        '''
        self.prompt = '{0}@{1}:{2}$ '.format(pycoreutils.getcurrentusername(),
                                             platform.node(),
                                             os.getcwd())


if __name__ == '__main__':
    PyCoreutilsShell().cmdloop(pycoreutils.showbanner(width=80))
