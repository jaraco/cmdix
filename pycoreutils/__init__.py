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
import base64
import fileinput
import glob
import hashlib
import os
import platform
import shlex
import shutil
import signal
import stat
import sys

try:
    import argparse
except ImportError:
    print("Failed to import argparse.")
    print("Argparse is included in Python starting 2.7 and 3.2, or " +\
          "available from PyPi")
    sys.exit(1)

import pycoreutils.command

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


def args2fds(args):
    '''

    '''
    fdlist = []
    for arg in args:
        for filename in glob.iglob(arg):
            if filename:
                yield open(filename)
            else:
                print("{0}: cannot access {1}:".format(sys.argv[0], arg) +\
                      "No such file or directory")


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
    f = 'pycoreutils.command.cmd_{0}'.format(commandname)
    try:
        return __import__(f, fromlist=1).parseargs
    except ImportError:
        raise CommandNotFoundException(commandname)


def getcurrentusername():
    '''
    Returns the username of the current user
    '''
    if 'USER' in os.environ:
        return os.environ['USER']      # Unix
    if 'USERNAME' in os.environ:
        return os.environ['USERNAME']  # Windows


def getsignals():
    ''' Return a dict of all available signals '''
    signallist = [
        'ABRT', 'CONT', 'IO', 'PROF', 'SEGV', 'TSTP', 'USR2', '_DFL', 'ALRM',
        'FPE', 'IOT', 'PWR', 'STOP', 'TTIN', 'VTALRM', '_IGN', 'BUS', 'HUP',
        'KILL', 'QUIT', 'SYS', 'TTOU', 'WINCH', 'CHLD', 'ILL', 'PIPE', 'RTMAX',
        'TERM', 'URG', 'XCPU', 'CLD', 'INT', 'POLL', 'RTMIN', 'TRAP', 'USR1',
        'XFSZ',
    ]
    signals = {}
    for signame in signallist:
        if hasattr(signal, 'SIG' + signame):
            signals[signame] = getattr(signal, 'SIG' + signame)
    return signals


def getuserhome():
    '''
    Returns the home-directory of the current user
    '''
    if 'HOME' in os.environ:
        return os.environ['HOME']      # Unix
    if 'HOMEPATH' in os.environ:
        return os.environ['HOMEPATH']  # Windows


def hasher(algorithm, p):
    def myhash(args):
        for fd in args.files:
            h = hashlib.new(algorithm)
            with fd as f:
                h.update(f.read())
            print(h.hexdigest() + '  ' + fd.name)

    p.set_defaults(func=myhash)
    p.description = "Print or check {0} ".format(algorithm.upper()) +\
                    "checksums. With no FILE, or when FILE is -, read " +\
                    "standard input."
    p.add_argument('files', nargs='*', type=argparse.FileType('r'),
                   default='-')
    return p


def listcommands():
    '''
    Returns a list of all available commands
    '''
    for cmd in pycoreutils.command.__all__:
        if cmd.startswith('cmd_'):
            yield cmd[4:]


def mode2string(mode):
    '''
    Convert mode-integer to string
    Example: 33261 becomes "-rwxr-xr-x"
    '''
    if stat.S_ISREG(mode):
        s = '-'
    elif stat.S_ISDIR(mode):
        s = 'd'
    elif stat.S_ISCHR(mode):
        s = 'c'
    elif stat.S_ISBLK(mode):
        s = 'b'
    elif stat.S_ISLNK(mode):
        s = 'l'
    elif stat.S_ISFIFO(mode):
        s = 'p'
    elif stat.S_ISSOCK(mode):
        s = 's'
    else:
        s = '-'

    # User Read
    if bool(mode & stat.S_IRUSR):
        s += 'r'
    else:
        s += '-'

    # User Write
    if bool(mode & stat.S_IWUSR):
        s += 'w'
    else:
        s += '-'

    # User Execute
    if bool(mode & stat.S_IXUSR):
        s += 'x'
    else:
        s += '-'

    # Group Read
    if bool(mode & stat.S_IRGRP):
        s += 'r'
    else:
        s += '-'

    # Group Write
    if bool(mode & stat.S_IWGRP):
        s += 'w'
    else:
        s += '-'

    # Group Execute
    if bool(mode & stat.S_IXGRP):
        s += 'x'
    else:
        s += '-'

    # Other Read
    if bool(mode & stat.S_IROTH):
        s += 'r'
    else:
        s += '-'

    # Other Write
    if bool(mode & stat.S_IWOTH):
        s += 'w'
    else:
        s += '-'

    # Other Execute
    if bool(mode & stat.S_IXOTH):
        s += 'x'
    else:
        s += '-'

    return s


def parsefilelist(filelist=['-'], decompress=False):
    '''
    Takes a list of files, and generates tuple containing a line and the
    filename.
    Files called '-' will be replaced with stdin.
    If decompress is defined, a file ending with '.gz' or '.bz2' is
    decompressed automatically.
    '''
    if decompress:
        openhook = fileinput.hook_compressed
    else:
        openhook = None

    # Use stdin if filelist is empty
    if filelist == []:
        filelist = ['-']

    for filename in filelist:
        for line in fileinput.input(filename, openhook=openhook):
            yield (line, filename)


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

    if commandname == 'pycoreutils':
        args, argv = parser.parse_known_args(argv)

        if args.license:
            print(__license__)
            return

        elif args.allhelp:
            for line in format_all_help():
                print(line)
            return

        elif args.runtests:
            try:
                from . import test
            except ImportError:
                print("Can't import pycoreutils.test. Please make sure to " +\
                    "include it in your PYTHONPATH", file=sys.stderr)
                sys.exit(1)
            test.runalltests()
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


def showbanner(width=None):
    '''
    Returns pycoreutils banner.
    The banner is centered if width is defined.
    '''
    subtext = "-= PyCoreutils version {0} =-".format(__version__)
    banner = [
        " ____  _  _  ___  _____  ____  ____  __  __  ____  ____  __    ___ ",
        "(  _ \( \/ )/ __)(  _  )(  _ \( ___)(  )(  )(_  _)(_  _)(  )  / __)",
        " )___/ \  /( (__  )(_)(  )   / )__)  )(__)(   )(   _)(_  )(__ \__ \\",
        "(__)   (__) \___)(_____)(_)\_)(____)(______) (__) (____)(____)(___/",
    ]

    if width:
        ret = ""
        for line in banner:
            ret += line.center(width) + "\n"
        ret += "\n" + subtext.center(width) + "\n"
        return ret
    else:
        return "\n".join(banner) + "\n\n" + subtext.center(68) + "\n"


### EXCEPTIONS ##############################################################


class StdOutException(Exception):
    '''
    Raised when data is written to stdout
    '''
    def __init__(self, text, errno=1):
        '''
        :text:  Output text
        ;errno: Exit status of program
        '''
        self.text = text
        self.errno = errno

    def __str__(self):
        return self.text


class StdErrException(Exception):
    '''
    Raised when data is written to stderr
    '''
    def __init__(self, text, errno=2):
        '''
        :text:  Error text
        ;errno: Exit status of program
        '''
        self.text = text
        self.errno = errno

    def __str__(self):
        return self.text


class CommandNotFoundException(Exception):
    '''
    Raised when an unknown command is requested
    '''
    def __init__(self, prog):
        self.prog = prog

    def __str__(self):
        return "Command `{0}' not found.".format(self.prog)


class ExtraOperandException(StdErrException):
    '''
    Raised when an argument is expected but not found
    '''
    def __init__(self, program, operand, errno=1):
        '''
        :program:   Program that caused the error
        :operand:   Value of the extra operand
        ;errno:     Exit status of program
        '''
        self.program = program
        self.operand = operand
        self.errno = errno

    def __str__(self):
        return "{0}: extra operand `{1}'. Try {0} --help' for more ".format(
                self.program, self.operand) + "information."


class MissingOperandException(StdErrException):
    '''
    Raised when an argument is expected but not found
    '''
    def __init__(self, program, errno=1):
        '''
        :program:   Program that caused the error
        ;errno:     Exit status of program
        '''
        self.program = program
        self.errno = errno

    def __str__(self):
        return "{0}: missing operand. Try `{0} --help'".format(self.program) +\
               " for more information."


if __name__ == '__main__':
    sys.exit(run())
