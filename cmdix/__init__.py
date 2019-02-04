#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

'''
PyCoreutils is a pure Python implementation of various standard
UNIX commands, like `ls`, `cp` and `sleep`. It also contains a shell-like
environment which will make Unix-users feel right at home on the Windows
command-prompt.
'''

from __future__ import print_function, unicode_literals
import sys

if sys.version_info[0] < 2 \
or sys.version_info[0] == 2 and sys.version_info[1] < 7 \
or sys.version_info[0] == 3 and sys.version_info[1] < 2:
    print("Minimal required python version is 2.7 or 3.2", file=sys.stderr)
    sys.exit(1)

import argparse
import base64
import fileinput
import glob
import os
import platform
import shlex
import shutil
import signal
import stat

import pycoreutils.command
from pycoreutils.exception import CommandNotFoundException, StdErrException


__version__ = '0.1.0a'
__license__ = '''Copyright (c) 2009, 2010, 2011 Hans van Leeuwen

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included
in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.
'''


def onlyunix(f):
    '''
    Decorator that indicates that the command cannot be run on windows
    '''
    f._onlyunix = True
    return f


def createlinks(directory, pycorepath='/usr/bin/pycoreutils'):
    '''
    Create a symlink to pycoreutils for every available command

    :param directory:   Directory where to store the links
    :param pycorepath:  Path to link to
    '''
    l = []
    for command in listcommands():
        linkname = os.path.join(directory, command)
        if os.path.exists(linkname):
            raise StdErrException("{0} already exists. ".format(linkname) +\
                                  "Not doing anything.")
        l.append(linkname)

    path = os.path.abspath(pycorepath)
    for linkname in l:
        try:
            os.symlink(path, linkname)
        except OSError:
            print("{0} already exists. Skipping.".format(path))
        else:
            print("Linked {0} to {1}".format(linkname, path))


def format_all_help():
    '''
    Yields (commandname, commandhelp) for all available commands.
    '''
    for commandname in listcommands():
        cmd = getcommand(commandname)
        p = cmd(argparse.ArgumentParser(prog=commandname))
        yield (commandname, p.format_help())


def getcommand(commandname):
    '''
    Returns the `parseargs`-function of the given commandname.
    Raises a CommandNotFoundException if the command is not found
    '''
    # Try to import the command module
    importstring = 'pycoreutils.command.cmd_{0}'.format(commandname)
    try:
        parseargs = __import__(importstring, fromlist=1).parseargs
    except ImportError:
        raise CommandNotFoundException(commandname)

    # Check if the command is available on Windows
    if os.name == 'nt':
        try:
            parseargs._onlyunix
        except AttributeError:
            pass
        else:
            raise CommandNotFoundException(commandname)

    return parseargs


def listcommands():
    '''
    Returns a list of all available commands
    '''
    for cmd in pycoreutils.command.__all__:
        if cmd.startswith('cmd_'):
            yield cmd[4:]


def run(argv=None):
    '''
    Parse commandline arguments and run command.
    If argv is None, read from sys.argv.

    For example:

    >>> import pycoreutils
    >>> pycoreutils.run(['seq', '-s', ' to the ', '1', '4'])
    1 to the 2 to the 3 to the 4

    :param argv:    List of arguments
    :return:        The exit status of the command. None means 0.
    '''
    argv = argv or sys.argv
    commandname = os.path.basename(argv.pop(0))
    parser = argparse.ArgumentParser(version=__version__, add_help=False,
                    description="Coreutils in Pure Python.", prog=commandname,
                    epilog="Available Commands: " + ", ".join(listcommands()))
    group = parser.add_mutually_exclusive_group()
    group.add_argument("command", nargs="?")
    group.add_argument("--allhelp", action="store_true",
                help="Show the help pages off all commands")
    group.add_argument("--license", action="store_true",
                help="Show program's license and exit")
    group.add_argument("--runtests", action="store_true",
                help="Run all sort of tests")
    group.add_argument("--createlinks", dest="directory",
                help="For every command, create a symlink to " +\
                     "/usr/bin/pycoreutils in 'directory'")

    if commandname in ('pycoreutils', '__main__.py'):
        args, argv = parser.parse_known_args(argv)

        if args.license:
            print(__license__)
            return

        elif args.allhelp:
            for commandname, commandhelp in format_all_help():
                print("\n" + commandname + "\n\n" + commandhelp)
            return

        elif args.runtests:
            try:
                import pycoreutils.test
            except ImportError:
                print("Can't import pycoreutils.test", file=sys.stderr)
                sys.exit(1)
            pycoreutils.test.runalltests()
            return

        elif args.directory:
            createlinks(args.directory)
            return

        elif not args.command and not argv:
            parser.print_help()
            return

        commandname = args.command

    # Run the subcommand
    try:
        cmd = getcommand(commandname)
    except CommandNotFoundException:
        print("Command `{0}` not found.".format(commandname), file=sys.stderr)
        return
    p = cmd(argparse.ArgumentParser(prog=commandname))
    args = p.parse_args(argv)
    args.func(args)


def runcommandline(commandline):
    '''
    Process a commandline.
    This is main entry-point to PyCoreutils.

    Examples:

    >>> import pycoreutils
    >>> pycoreutils.runcommandline('basename /foo/bar/')
    bar
    >>> pycoreutils.runcommandline('cal 2 2000')
       February 2000
    Su Mo Tu We Th Fr Sa
           1  2  3  4  5
     6  7  8  9 10 11 12
    13 14 15 16 17 18 19
    20 21 22 23 24 25 26
    27 28 29

    :param commandline: String representing the commandline, i.e. "ls -l /tmp"
    '''
    return run(shlex.split(str(commandline)))


if __name__ == '__main__':
    sys.exit(run())
