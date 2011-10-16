# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import cmd
import os
import platform
import pprint
import sys


@pycoreutils.addcommand
def sh(p):
    p.set_defaults(func=func)
    p.description = "Start a shell"


def func(args):
    return Sh().cmdloop(pycoreutils.showbanner(width=80))


class Sh(cmd.Cmd):
    '''
    Pycoreutils Shell
    '''
    exitstatus = 0
    prompttemplate = '{username}@{hostname}:{currentpath}$ '

    def __init__(self, *args, **kwargs):
        # Copy all commands from pycoreutils to 'do_foo' functions
        for command in pycoreutils.listcommands():
            x = '''self.do_{0} = lambda l:pycoreutils.runcommandline('{0} '+ l)
                '''.format(command)
            exec(x)
        return cmd.Cmd.__init__(self, *args, **kwargs)

    def default(self, line):
        '''
        Called on an input line when the command prefix is not recognized.
        '''
        self.exitstatus = 127
        return "{0}: Command not found\n".format(line.split(None, 1)[0])

    def do_exit(self, n=None):
        '''
        Exit the shell.

        Exits the shell with a status of N.  If N is omitted, the exit status
        is that of the last command executed.
        '''
        sys.exit(n or self.exitstatus)

    def do_help(self, arg):
        return "Use 'COMMAND --help' for help\n" +\
               "Available commands:\n" +\
               ", ".join(pycoreutils.listcommands()) + "\n"

    def do_shell(self, line):
        '''
        Run when them command is '!' or 'shell'.
        Execute the line using the Python interpreter.
        i.e. "!dir()"
        '''
        try:
            exec("r = {0}".format(line))
        except Exception as err:
            return pprint.pformat(err) + '\n'
        else:
            return pprint.pformat(r) + '\n'

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
        Update the prompt using format() on the template in self.prompttemplate

        You can use the following keywords:
        - currentpath
        - hostname
        - username
        '''
        self.prompt = self.prompttemplate.format(currentpath=os.getcwd(),
           hostname=platform.node(), username=pycoreutils.getcurrentusername())
