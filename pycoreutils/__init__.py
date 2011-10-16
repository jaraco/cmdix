#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import base64
import bz2
import fileinput
import glob
import gzip
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
    print("Argparse is included in Python 2.7 and 3.2, or available from PyPi")
    sys.exit(1)


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

_cmds = []  # Commands will be added to this list


### DECORATORS ##############################################################


def addcommand(f):
    '''
    Register a command with pycoreutils
    '''
    _cmds.append(f)
    return f


def onlyunix(f):
    '''
    Decorator that indicates that the command cannot be run on windows
    '''
    f._onlyunix = True
    return f


### HELPER FUNCTIONS ########################################################


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


def compressor(p, comptype='gzip', decompress=False):
    '''
    Handles compression and decompression as bzip2 and gzip
    '''
    p.description = "Compress or uncompress FILEs (by default, compress " + \
                    "FILES in-place)."
    p.set_defaults(func=compressorfunc, comptype=comptype,
                   decompress=decompress)
    p.add_argument('files', nargs='*')
    p.add_argument("-c", "--stdout", "--as-stdout", action="store_true",
            dest="stdout",
            help="write on standard output, keep original files unchanged")
    p.add_argument("-C", "--compresslevel", dest="compresslevel", type=int,
            default=6, help="set file mode (as in chmod), not a=rwx - umask")
    p.add_argument("-d", "--decompress", action="store_true",
            dest="decompress", help="decompress")
    p.add_argument("-1", "--fast", action="store_const", dest="compresslevel",
            const=1, help="Use the fastest type of compression")
    p.add_argument("-2", action="store_const", dest="compresslevel", const=2,
            help="Use compression level 2")
    p.add_argument("-3", action="store_const", dest="compresslevel", const=3,
            help="Use compression level 3")
    p.add_argument("-4", action="store_const", dest="compresslevel", const=4,
            help="Use compression level 4")
    p.add_argument("-5", action="store_const", dest="compresslevel", const=5,
            help="Use compression level 5")
    p.add_argument("-6", action="store_const", dest="compresslevel", const=6,
            help="Use compression level 6")
    p.add_argument("-7", action="store_const", dest="compresslevel", const=7,
            help="Use compression level 7")
    p.add_argument("-8", action="store_const", dest="compresslevel", const=8,
            help="Use compression level 8")
    p.add_argument("-9", "--best", action="store_const", dest="compresslevel",
            const=9, help="Use the best type of compression")


def compressorfunc(args):
    if args.comptype == 'gzip':
        compresstype = gzip.GzipFile
        suffix = '.gz'
    elif args.comptype == 'bzip' or comptype == 'bzip2':
        compresstype = bz2.BZ2File
        suffix = '.bz2'

    infiles = args.files

    # Use stdin for input if no file is specified or file is '-'
    if len(args.files) == 0 or (len(args.files) == 1 and args[0] == '-'):
        infiles = [sys.stdin]

    for infile in infiles:
        print(infile)
        if args.decompress:
            # Decompress
            infile = compresstype(infile, 'rb',
                                  compresslevel=args.compresslevel)
            if len(args) == 0 or args.stdout:
                outfile = sys.stdout
            else:
                unzippath = infile.rstrip(suffix)
                if os.path.exists(unzippath):
                    q = input("{0}: {1} already ".format(p.prog, unzippath) + \
                              "exists; do you wish to overwrite (y or n)? ")
                    if q.upper() != 'Y':
                        StdOutException("not overwritten", 2)

                outfile = open(unzippath, 'wb')
        else:
            # Compress
            zippath = infile + suffix
            infile = open(infile, 'rb')
            if len(args) == 0 or args.stdout:
                outfile = sys.stdout
            else:
                if os.path.exists(zippath):
                    q = input("{0}: {1} already".format(p.prog, zippath) + \
                              " exists; do you wish to overwrite (y or n)? ")
                    if q.upper() != 'Y':
                        StdErrException("not overwritten", 2)

                outfile = compresstype(zippath, 'wb',
                                       compresslevel=args.compresslevel)

        shutil.copyfileobj(infile, outfile)


def coreutils(args):
    if args.license:
        print(__license__)

    if args.runtests:
        try:
            from pycoreutils import test
        except ImportError:
            print("Can't import pycoreutils.test. Please make sure to " +\
                  "include it in your PYTHONPATH", file=sys.stderr)
            sys.exit(1)
        test.runalltests()

    if args.createcommanddirectory:
        createcommandlinks(p.prog, args.createcommanddirectory)


def createcommandlinks(pycorepath, directory):
    '''
    Create a symlink to pycoreutils for every available command

    :param pycorepath:  Path to link to
    :param directory:   Directory where to store the links
    '''
    l = []
    for command in listcommands():
        linkname = os.path.join(directory, command)
        if os.path.exists(linkname):
            raise StdErrException("{0} already exists. Not doing anything.")
        l.append(linkname)

    for linkname in l:
        os.symlink(os.path.abspath(pycorepath), linkname)


def getcommand(commandname):
    '''
    Returns the function of the given commandname.
    Raises a CommandNotFoundException if the command is not found
    '''
    a = [command for command in _cmds if command.__name__ == commandname]
    l = len(a)
    if l == 0:
        raise CommandNotFoundException(commandname)
    if l > 1:
        raise "Command `{0}' has multiple functions ".format(commandname) +\
              "associated with it! This should never happen!"
    return a[0]


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


def listcommands():
    '''
    Returns a list of all available commands
    '''
    l = []
    for command in _cmds:
        l.append(command.__name__.lower())
    return l


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


def run(argv=sys.argv):
    '''
    Parse commandline arguments and run command.
    This is where the magic happens :-)

    :param argv:    List of arguments
    :return:        The exit status of the command. None means 0.
    '''
    p = argparse.ArgumentParser(version=__version__,
                description="Coreutils in Pure Python.",
                epilog="Available Commands: " + ", ".join(listcommands()))

    subparsers = p.add_subparsers(title='subcommands',
                                  description='valid subcommands')

    sp = subparsers.add_parser('pycoreutils')
    sp.set_defaults(func=coreutils)
    sp.description = "Pycoreutils meta-commands"
    sp.add_argument("--createcommandlinks", dest="createcommanddirectory",
                    help="Create a symlink to pycoreutils for every " +\
                         "available command")
    sp.add_argument("--helpall", action="store_true",
                    help="Show help for all commands")
    sp.add_argument("--license", action="store_true",
                    help="show program's license and exit")
    sp.add_argument("--runtests", action="store_true",
                    help="Run all sort of tests")

    # Register commands with subparser
    for command in _cmds:
        s = subparsers.add_parser(command.__name__)
        command(s)

    # Strip sys.argv
    argv[0] = os.path.basename(argv[0])
    if os.path.basename(argv[0]) in ['__init__.py', 'coreutils.py']:
        argv = argv[1:]

    # Run the subcommand
    #print(argv)
    args = p.parse_args(argv)
    args.func(args)


def runcommandline(commandline):
    '''
    Process a commandline

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


# Finally import all commands so addcommand() will register them
try:
    from pycoreutils.command import *
except ImportError:
    print("Can't import pycoreutils.command. Please make sure to " +\
          "include it in your PYTHONPATH", file=sys.stderr)
    sys.exit(1)


if __name__ == '__main__':
    sys.exit(run())
