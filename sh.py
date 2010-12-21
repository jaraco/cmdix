#!/usr/bin/env python
# -*- coding: utf-8 -*-

import cmd
import os
import platform
import readline
import sys

import pycoreutils


__version__ = '0.0.1'
__license__ = '''Copyright (c) 2010 Hans van Leeuwen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies
of the Software, and to permit persons to whom the Software is furnished to do
so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
'''

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
    PyCoreutilsShell().cmdloop('PyCoreutils Shell version %s' % __version__)
