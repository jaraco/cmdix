#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals


# First import version-specific modules
import sys
if sys.version_info[0] == 2:
    if sys.version_info[1] < 6:
        raise Exception("Pycoreutils requires Python version 2.6 or greater")

    input = raw_input

    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from urllib2 import build_opener, HTTPError
else:
    from http.server import HTTPServer, SimpleHTTPRequestHandler
    from urllib.error import HTTPError
    from urllib.request import build_opener


# 'grp' and 'pwd' are Unix only
try:
    import grp as _grp
    import pwd as _pwd
except ImportError:
    pass


# Import rest
import asyncore
import base64 as _base64
import bz2
import fileinput
import gzip as _gzip
import hashlib
import logging
import logging.handlers
import optparse
import os
import platform
import random
import shutil
import signal
import smtpd as _smtpd
import smtplib
import socket
import stat
import subprocess
import tempfile
import textwrap
import time
import zipfile


__version__ = '0.0.5a'
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



### COMMANDS ################################################################


@addcommand
def arch(argstr):
    p = parseoptions()
    p.description = "Print machine architecture."
    p.usage = '%prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) > 0:
        raise ExtraOperandException(prog, args[0])

    return platform.machine() + "\n"


@addcommand
def base64(argstr):
    p = parseoptions()
    p.description = "Base64 encode or decode FILE, or standard input, " + \
                    "to standard output."
    p.usage = '%prog [OPTION]... [FILE]'
    p.add_option("-d", action="store_true", dest="decode",
            help="decode data")
    p.add_option("-w", dest="wrap", default=76, type="int",
            help="wrap encoded lines after COLS character (default 76). " + \
                 "Use 0 to disable line wrapping")
    (opts, args) = p.parse_args(argstr.split())

    s = ''
    for line in fileinput.input(args):
        s += line

    if opts.decode:
        out = _base64.b64decode(s)
        if opts.wrap == 0:
            yield out
        else:
            for line in textwrap.wrap(out, opts.wrap):
                yield line + "\n"
    else:
        out = _base64.b64encode(s)
        if opts.wrap == 0:
            yield out
        else:
            for line in textwrap.wrap(out, opts.wrap):
                yield line + "\n"


@addcommand
def basename(argstr):
    p = parseoptions()
    p.description = "Print NAME with any leading directory components " + \
                    "removed. If specified, also remove a trailing SUFFIX."
    p.usage = '%prog NAME [SUFFIX]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    if len(args) > 2:
        raise ExtraOperandException(prog, args[2])

    b = args[0]

    # Remove trailing slash to make sure /foo/bar/ is the same as /foo/bar
    if len(b) > 1:
        b = b.rstrip('/')
    b = os.path.basename(b)

    if len(args) == 2:
        b = b.rstrip(args[1])

    return b + "\n"


@addcommand
def bunzip2(argstr):
    compressor(argstr, 'bzip2', True)


@addcommand
def bzip2(argstr):
    compressor(argstr, 'bzip2')


@addcommand
def cat(argstr):
    p = parseoptions()
    p.description = "Concatenate FILE(s), or standard input, " + \
                    "to standard output."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    (opts, args) = p.parse_args(argstr.split())

    for line in fileinput.input(args, openhook=fileinput.hook_compressed):
        yield line


@addcommand
def cd(argstr):
    p = parseoptions()
    p.description = "Change the current working directory to HOME or PATH"
    p.usage = '%prog [PATH]'
    (opts, args) = p.parse_args(argstr.split())

    if len(args) == 0:
        pth = getuserhome()
    elif len(args) == 1:
        pth = os.path.expanduser(args[0])
    else:
        raise ExtraOperandException(prog, args[1])

    os.chdir(pth)


@addcommand
@onlyunix
def chown(argstr):
    # TODO: Support for groups and --reference
    p = parseoptions()
    p.description = "Change the owner and/or group of each FILE to OWNER " + \
                     "and/or GROUP. With --reference, change the owner and" + \
                     " group of each FILE to those of RFILE."
    p.usage = '%prog [OWNER] FILE'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    uid = args.pop(0)
    if not uid.isdigit():
        try:
            user = _pwd.getpwnam(uid)
        except KeyError:
            StdErrException("{0}: invalid user: '{1}'".format(prog, uid))
        uid = user.pw_uid

    for arg in args:
        os.chown(arg, int(uid), -1)


@addcommand
def chroot(argstr):
    # TODO: Testing!!!
    p = parseoptions()
    p.description = "Run COMMAND with root directory set to NEWROOT."
    p.usage = '%prog NEWROOT [COMMAND [ARG]...]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    # If no command is given, run ''${SHELL} -i''
    if len(args) == 1:
        args.append(os.environ['SHELL'])
        args.append('-i')

    os.chroot(args[0])
    subprocess.call(args)


@addcommand
def cp(argstr):
    p = parseoptions()
    p.description = "Copy SOURCE to DEST, or multiple SOURCE(s) to DIRECTORY."
    p.usage = "%prog [OPTION]... SOURCE... DIRECTORY"
    p.add_option("-i", "--interactive", action="store_true", 
            dest="interactive", help="prompt before overwrite")
    p.add_option("-p", "--preserve", action="store_true", dest="preserve",
            help="preserve as many attributes as possible")
    p.add_option("-r", "-R", "--recursive", action="store_true",
            dest="recursive", help="copy directories recursively")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    if len(args) == 1:
        raise StdErrException(
                "{0}: missing destination file operand ".format(prog) +\
                "after `{1}'. ".format(args[0]) +\
                "Try {0} --help' for more information.".format(prog)
              )

    # Set the _copy function
    if opts.preserve:
        _copy = shutil.copy2
    else:
        _copy = shutil.copy

    dstbase = args.pop()
    for src in args:
        if opts.recursive:
            # Create the base destination directory if it does not exists
            if not os.path.exists(dstbase):
                os.mkdir(dstbase)

            # Walk the source directory
            for root, dirnames, filenames in os.walk(src):
                if root == dstbase:
                    continue
                dstmid = root.lstrip(src)

                # Create subdirectories in destination directory
                for subdir in dirnames:
                    srcdir = os.path.join(root, subdir)
                    dstdir = os.path.join(dstbase, dstmid, subdir)
                    if not os.path.exists(dstbase):
                        os.mkdir(dstdir)
                    if opts.verbose:
                        yield "`{0}' -> `{1}'\n".format(root, dstdir)

                # Copy file
                for filename in filenames:
                    dstfile = os.path.join(dstbase, dstmid, filename)
                    srcfile = os.path.join(root, filename)
                    if opts.interactive and os.path.exists(dstfile):
                        q = input("{0}: {1} already ".format(prog, dstfile) +\
                                  "exists; do you wish to overwrite (y or n)?")
                        if q.upper() != 'Y':
                            StdOutException("not overwritten", 2)
                            continue
                    _copy(srcfile, dstfile)
                    if opts.verbose:
                        yield "`{0}' -> `{1}'\n".format(srcfile, dstfile)
        else:
            dstfile = dstbase
            if os.path.isdir(dstbase):
                dstfile = os.path.join(dstbase, src)
            _copy(src, dstfile)
            if opts.verbose:
                yield "`{0}' -> `{1}'\n".format(srcfile, dstfile)


@addcommand
def dirname(argstr):
    p = parseoptions()
    p.description = "Print NAME with its trailing /component removed; if " + \
                    "NAME contains no /'s, output `.' (meaning the current" + \
                    " directory)."
    p.usage = '%prog [NAME]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    if len(args) > 1:
        raise ExtraOperandException(prog, args[1])

    d = os.path.dirname(args[0].rstrip('/'))

    if d == '':
        d = '.'

    return d + "\n"


@addcommand
def env(argstr):
    # TODO: --unset
    p = parseoptions()
    p.description = "Set each NAME to VALUE in the environment and run " + \
                    "COMMAND."
    p.usage = '%prog [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]'
    p.add_option("-i", "--ignore-environment", action="store_true",
            dest="ignoreenvironment", help="start with an empty environment")
    #p.add_option("-u", "--unset", dest="unset",
            #help="remove variable from the environment")
    (opts, args) = p.parse_args(argstr.split())

    env = {}
    if not opts.ignoreenvironment:
        env = os.environ

    if len(args) == 0:
        for k, v in env.items():
            yield k + '=' + v + "\n"
    else:
        for arg in args:
            x = arg.split('=')
            if len(x) < 2:
                StdErrException("Invalid argument {0}. ".format(arg) +\
                        "Arguments should be in the form of 'foo=bar'", 127)
            else:
                yield x[0] + '=' + x[1] + "\n"


@addcommand
def false(argstr):
    p = parseoptions()
    p.description = "Do nothing, unsuccessfully"
    p.usage = "%prog [OPTION]..."
    (opts, args) = p.parse_args(argstr.split())

    sys.exit(1)


@addcommand
def gunzip(argstr):
    compressor(argstr, 'gzip', True)


@addcommand
def gzip(argstr):
    compressor(argstr, 'gzip')


@addcommand
def httpd(argstr):
    p = parseoptions()
    p.description = "Start a web server that serves the current directory"
    p.usage = '%prog [OPTION]...'
    p.add_option("-a", "--address", default="", dest="address",
            help="address to bind to")
    p.add_option("-p", "--port", default=8000, dest="port", type="int",
            help="port to listen to")
    (opts, args) = p.parse_args(argstr.split())

    handler = SimpleHTTPRequestHandler
    server = HTTPServer((opts.address, opts.port), handler)

    server.serve_forever()


@addcommand
@onlyunix
def id(argstr):
    # TODO: List all groups a user belongs to
    p = parseoptions()
    p.description = "Print user and group information for the specified " + \
                    "USERNAME, or (when USERNAME omitted) for the current " + \
                    "user."
    p.usage = '%prog [OPTION]... [USERNAME]'
    p.add_option("-a", action="store_true", dest="ignoreme",
            help="ignore, for compatibility with other versions")
    p.add_option("-g", "--group", action="store_true", dest="group",
            help="print only the effective group ID")
    p.add_option("-n", "--name", action="store_true", dest="name",
            help="print a name instead of a number, for -ug")
    p.add_option("-u", "--user", action="store_true", dest="user",
            help="print only the effective group ID")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) > 1:
        raise ExtraOperandException(prog, args[1])

    if args == []:
        u = _pwd.getpwuid(os.getuid())
    else:
        u = _pwd.getpwnam(args[0])

    uid = u.pw_uid
    gid = u.pw_gid
    username = u.pw_name
    g = _grp.getgrgid(gid)
    groupname = g.gr_name

    if opts.group and opts.name:
        return groupname

    if opts.group:
        return gid

    if opts.user and opts.name:
        return username

    if opts.user:
        return uid

    if opts.name:
        StdErrException("id: cannot print only names or real IDs in " +
                        "default format")

    return "uid=%i(%s) gid=%i(%s)\n" % (uid, username, gid, username)


@addcommand
def kill(argstr):
    signals = getsignals()

    p = parseoptions()
    p.description = ""
    p.usage = '%prog kill [ -SIGNAL | -s SIGNAL ] PID ...'
    p.add_option("-s", "--signal",  action="store", dest="signal",
            default=signal.SIGTERM,
            help="send signal")

    # Add a string option for each signal
    for name, sigint in list(signals.items()):
        signame = 'SIG' + name.upper()
        p.add_option("--%s" % signame, action="store_const", dest="signal",
            const=sigint,
            help="send signal {0}".format(signame))

    # Add an integer option for each signal
    for sigint in set(signals.values()):
        if sigint < 10:
            p.add_option("-%i" % sigint, action="store_const", dest="signal",
                const=sigint, help="send signal {0}".format(sigint))

    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    try:
        sig = int(opts.signal)
    except ValueError:
        sig = opts.signal.upper()
    
    if list(signals.values()).count(sig):
        sigint = sig
    elif sig in signals:
        sigint = signals[sig]
    elif sig.lstrip('SIG') in signals:
        sigint = signals[sig.lstrip('SIG')]
    else:
        raise StdErrException("kill: {0}: ".format(sig) +\
                              "invalid signal specification")

    for pid in args:
        try:
            pid = int(pid)
        except ValueError:
            raise StdErrException("kill: {0}: ".format(pid) +\
                                  "arguments must be process or job IDs")

        os.kill(pid, sigint)


@addcommand
@onlyunix
def ln(argstr):
    p = parseoptions()
    p.description = ""
    p.usage = '\n%prog [OPTION]... [-T] TARGET LINK_NAME   (1st form)' + \
              '\n%prog [OPTION]... TARGET                  (2nd form)'
    p.add_option("-s", "--symbolic", action="store_true", dest="symbolic",
            help="make symbolic links instead of hard links")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)
    elif len(args) == 1:
        src = args[0]
        dst = os.path.basename(src)
    elif len(args) == 2:
        src = args[0]
        dst = args[1]

    if opts.symbolic:
        f = os.symlink
        linktype = 'soft'
    else:
        f = os.link
        linktype = 'hard'

    for src in args:
        if opts.verbose:
            yield "`{0}' -> `{1}'".format(src, dst)
        try:
            f(src, dst)
        except Exception as err:
            yield "ln: creating {0} link `{1}' => `{2}': {3}\n".format(
                   linktype, dst, src, err.strerror)


@addcommand
def logger(argstr):
    # TODO: -i, -f, t
    p = parseoptions()
    p.description = "A shell command interface to the syslog system log " + \
                    "module"
    p.usage = '%prog [OPTION] [ MESSAGE ... ]'
    p.add_option("--host", dest="host",
            help="Address of the syslog daemon. The default is `localhost'")
    p.add_option("-p", dest="priority",
            help="Enter the message with the specified priority. The " + \
                 "priority may as a ``facility.level'' pair. For example, " + \
                 "``-p local3.info'' logs the message(s) as informational " + \
                 "level in the local3 facility. " + \
                 "The default is ``user.notice.''")
    p.add_option("--port", dest="port",
            help="Port of the syslog daemon. The default is 514'.'")
    p.add_option("-s", action="store_true", dest="stderr",
            help="Log the message to standard error, as well as the "  + \
                 "system log.")
    (opts, args) = p.parse_args(argstr.split())

    if opts.priority:
        facility, level = opts.priority.split('.', 2)
    else:
        facility = 'user'
        level = 'notice'

    if opts.host or opts.port:
        host = opts.host or 'localhost'
        port = opts.port or 514
        address = (host, port)
    else:
        address = '/dev/log'

    handler = logging.handlers.SysLogHandler(address, facility)
    if facility not in handler.facility_names:
        err = "Unknown facility {0}. ".format(facility) +\
              "Valid facilities are: "
        facilitylist = list(handler.facility_names.keys())
        facilitylist.sort()
        for f in facilitylist:
            err += f + ", "

        raise StdErrException(err)

    msg = ' '.join(args)
    levelint = 90 - 10 * handler.priority_names.get(level, 0)

    logger = logging.getLogger('Logger')
    logger.addHandler(handler)
    logger.log(levelint, msg)

    if opts.stderr:
        raise StdErrException(msg)


@addcommand
def ls(argstr):
    # TODO: Show user and group names in ls -l, correctly format dates in ls -l
    p = parseoptions()
    p.description = "List information about the FILEs (the current " + \
                    "directory by default). Sort entries " + \
                    "alphabetically if none of -cftuvSUX nor --sort."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.add_option("-l", action="store_true", dest="longlist",
                 help="use a long listing format")
    (opts, args) = p.parse_args(argstr.split())

    if len(args) < 1:
        args = '.'

    for arg in args:
        dirlist = os.listdir(arg)
        dirlist.sort()
        l = []
        sizelen = 0     # Length of the largest filesize integer
        nlinklen = 0    # Length of the largest nlink integer
        for f in dirlist:
            path = os.path.join(arg, f)
            if not opts.longlist:
                yield f + "\n"
            else:
                st = os.lstat(path)
                mode = mode2string(st.st_mode)
                nlink = st.st_nlink
                uid = st.st_uid
                gid = st.st_gid
                size = st.st_size
                mtime = time.localtime(st.st_mtime)
                if stat.S_ISLNK(st.st_mode):
                    f += " -> {0}".format(os.readlink(path))
                l.append((mode, nlink, uid, gid, size, mtime, f))

                # Update sizelen
                _sizelen = len(str(size))
                if _sizelen > sizelen:
                    sizelen = _sizelen

                # Update nlinklen
                _nlinklen = len(str(nlink))
                if _nlinklen > nlinklen:
                    nlinklen = _nlinklen

        for mode, nlink, uid, gid, size, mtime, f in l:
            modtime = time.strftime('%Y-%m-%d %H:%m', mtime)
            yield "{0} {1:>{nlink}} {2:<5} {3:<5} {4:>{size}} {5} {6}".format(
                                mode,
                                nlink,
                                uid,
                                gid,
                                size,
                                modtime,
                                f,
                                size=sizelen,
                                nlink=nlinklen,
                                ) + "\n"


@addcommand
def md5sum(argstr):
    return hasher('md5', argstr)


@addcommand
def mkdir(argstr):
    p = parseoptions()
    p.usage = '%prog [OPTION]... DIRECTORY...'
    p.description = "Create the DIRECTORY(ies), if they do not already " + \
                    "exist."
    p.add_option("-p", "--parents", action="store_true", dest="parents",
            help="no error if existing, make parent directories as needed")
    p.add_option("-m", "--mode", dest="mode", default=0o777,
            help="set file mode (as in chmod), not a=rwx - umask")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    for arg in args:
        if opts.parents:
            # Recursively create directories. We can't use os.makedirs
            # because -v won't show all intermediate directories
            path = arg
            pathlist = []

            # Create a list of directories to create
            while not os.path.exists(path):
                pathlist.insert(0, path)
                path, tail = os.path.split(path)

            # Create all directories in pathlist
            for path in pathlist:
                os.mkdir(path, int(opts.mode))
                if opts.verbose:
                    yield "mkdir: created directory `%s'\n" % (path)
        else:
            os.mkdir(arg, int(opts.mode))
            if opts.verbose:
                yield "mkdir: created directory `%s'\n" % (arg)


@addcommand
def mktemp(argstr):
    # TODO: Templates, most of the options
    p = parseoptions()
    p.description = "Create a temporary file or directory, safely, and " + \
                    "print its name."
    p.usage = '%prog [OPTION]... [TEMPLATE]'
    p.add_option("-d", "--directory", action="store_true", dest="directory",
            help="create a directory, not a file")
    (opts, args) = p.parse_args(argstr.split())

    if len(args) == 0:
        if opts.directory:
            return tempfile.mkdtemp(prefix='tmp.') + "\n"
        else:
            return tempfile.mkstemp(prefix='tmp.')[1] + "\n"
    elif len(args) == 1:
        raise NotImplementedError("Templates are not yet implemented")
    else:
        raise StdErrException("mktemp: too many templates. " +\
                              "Try `mktemp --help' for more information.")


@addcommand
def mv(argstr):
    p = parseoptions()
    p.description = "Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY."
    p.usage = "%prog [OPTION]... [-T] SOURCE DEST\nor:    " + \
              "%prog [OPTION]... SOURCE... DIRECTORY\nor:    " + \
              "%prog [OPTION]... -t DIRECTORY SOURCE..."
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="explain what is being done")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)
    if len(args) == 1:
        StdErrException("mv: missing destination file operand after " +\
                        "'%s'" % args[0] +\
                        "Try 'mv --help' for more information.")

    dest = args.pop()

    for src in args:
        if opts.verbose:
            yield "'{0}' -> '{1}'\n".format(src, dest)

        shutil.move(src, dest)


@addcommand
def pwd(argstr):
    p = parseoptions()
    p.description = "print name of current/working directory"
    p.usage = '%prog [OPTION]...'
    p.add_option("-L", "--logical", action="store_true", dest="logical",
            help="use PWD from environment, even if it contains symlinks")
    p.add_option("-P", "--physical", action="store_true", dest="physical",
            help="avoid all symlinks")
    (opts, args) = p.parse_args(argstr.split())

    if opts.logical:
        return os.getenv('PWD') + "\n"
    elif opts.physical:
        return os.path.realpath(os.getcwd()) + "\n"
    else:
        return os.getcwd() + "\n"



@addcommand
def rm(argstr):
    p = parseoptions()
    p.description = "print name of current/working directory"
    p.usage = '%prog [OPTION]... FILE...'
    p.add_option("-f", "--force", action="store_true", dest="force",
            help="ignore nonexistent files, never prompt")
    p.add_option("-r", "-R", "--recursive", action="store_true",
            dest="recursive",
            help="remove directories and their contents recursively")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="explain what is being done")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    def _raise(err):
        if not opts.force:
            raise err

    for arg in args:
        if opts.recursive and os.path.isdir(arg):
            # Remove directory recursively
            for root, dirs, files in os.walk(arg, topdown=False,
                                             onerror=_raise):
                for name in files:
                    path = os.path.join(root, name)
                    os.remove(path)
                    if opts.verbose:
                        yield "Removed file `{0}'\n".format(path)
                for name in dirs:
                    path = os.path.join(root, name)
                    os.rmdir(path)
                    if opts.verbose:
                        yield "Removed directory `{0}'\n".format(path)
            os.rmdir(arg)
        else:
            # Remove single file
            try:
                os.remove(arg)
                if opts.verbose:
                    yield "Removed `{0}'\n".format(arg)
            except OSError as err:
                _raise(err)


@addcommand
def rmdir(argstr):
    p = parseoptions()
    p.description = "Remove the DIRECTORY(ies), if they are empty."
    p.usage = '%prog [OPTION]... DIRECTORY...'
    p.add_option("-p", "--parent", action="store_true", dest="parent",
            help="remove DIRECTORY and its ancestors; e.g., " +
                 "`rmdir -p a/b/c' is similar to `rmdir a/b/c a/b a'")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    for arg in args:
        if opts.parent:
            os.removedirs(arg)
        else:
            os.rmdir(arg)


@addcommand
def sendmail(argstr):
    # TODO: Authentication
    p = parseoptions()
    p.description = "A simple sendmail implementation"
    p.usage = '%prog [OPTION]... [RECIPIENT]...'
    p.add_option("-a", "--address", default="localhost", dest="address",
            help="address to send to. default is localhost")
    p.add_option("-c", "--certfile", dest="certfile",
            help="certificate file to use. implies '-s'")
    p.add_option("-f", "-r", "--sender", dest="sender",
            default=getcurrentusername() + "@" + platform.node(),
            help="set the envelope sender address")
    p.add_option("-k", "--keyfile", dest="keyfile",
            help="key file to use. implies '-s'")
    p.add_option("-m", "--messagefile", default=sys.stdin,
            dest="messagefile",
            help="read message from file. by default, read from stdin.")
    p.add_option("-p", "--port", default=25, dest="port", type="int",
            help="port to send to. defaults is 25")
    p.add_option("-t", "--timeout", default=socket._GLOBAL_DEFAULT_TIMEOUT,
            help="set timeout in seconds", dest="timeout", type="int")
    p.add_option("-s", "--ssl", action="store_true", dest="ssl",
            help="connect using ssl")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="show smtp session")
    (opts, args) = p.parse_args(argstr.split())

    msg = ""
    for line in fileinput.input(opts.messagefile):
        msg += line

    if opts.ssl or opts.certfile or opts.keyfile:
        smtp = smtplib.SMTP_SSL(opts.address, opts.port,
                                timeout=opts.timeout,
                                keyfile=opts.keyfile,
                                certfile=opts.certfile)
    else:
        smtp = smtplib.SMTP(opts.address, opts.port, timeout=opts.timeout)

    smtp.set_debuglevel(opts.verbose)
    smtp.sendmail(opts.sender, args, msg)
    smtp.quit()


@addcommand
def seq(argstr):
    p = parseoptions()
    p.description = "Print numbers from FIRST to LAST, in steps of " + \
                    "INCREMENT."
    p.usage = "%prog [OPTION]... LAST\nor:    %prog [OPTION]... FIRST " + \
              "LAST\nor:    %prog [OPTION]... FIRST INCREMENT LAST"
    p.add_option("-s", "--seperator", dest="seperator",
            help="use SEPERATOR to separate numbers (default: \\n)")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    if len(args) == 1:
        a = list(range(1, int(args[0])+1))
    elif len(args) == 2:
        a = list(range(int(args[0]), int(args[1])+1))
    elif len(args) == 3:
        a = list(range(int(args[0]), int(args[2])+1, int(args[1])))

    if opts.seperator == None:
        for x in a:
            yield str(x) + "\n"
    else:
        for x in range(len(a)-1, 0, -1):
            a.insert(x, opts.seperator)
        for x in a:
            yield str(x)
        yield "\n"


@addcommand
def sha1sum(argstr):
    return hasher('sha1', argstr)


@addcommand
def sha224sum(argstr):
    return hasher('sha224', argstr)


@addcommand
def sha256sum(argstr):
    return hasher('sha256', argstr)


@addcommand
def sha384sum(argstr):
    return hasher('sha384', argstr)


@addcommand
def sha512sum(argstr):
    return hasher('sha512', argstr)


@addcommand
def shred(argstr):
    p = parseoptions()
    p.description = "Overwrite the specified FILE(s) repeatedly, in order " + \
                    "to make it harder for even very expensive hardware " + \
                    "probing to recover the data."
    p.usage = '%prog [OPTION]... FILE...'
    p.epilog = "This program acts as GNU 'shred -x', and doesn't round " + \
               "sizes up to the next full block"
    p.add_option("-n", "--iterations", dest="iterations", default=3,
            help="overwrite ITERATIONS times instead of the default (3)")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="show progress")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    for arg in args:
        for i in range(opts.iterations):
            size = os.stat(arg).st_size
            fd = open(arg, mode='w')
            logging.debug('Size:', size)
            fd.seek(0)
            for i in range(size):
                # Get random byte
                b = "".join(chr(random.randrange(0, 256)))
                fd.write(b)
            fd.close()


@addcommand
def shuf(argstr):
    p = parseoptions()
    p.description = "Write a random permutation of the input lines to " + \
                    "standard output."
    p.usage = '%prog [OPTION]... [FILE]\nor:    %prog -e [OPTION]... ' + \
              '[ARG]...\nor:    %prog -i LO-HI [OPTION]...'
    p.add_option("-e", "--echo", action="store_true", dest="echo",
            help="treat each ARG as an input line")
    p.add_option("-i", "--input-range", dest="inputrange",
            help="treat each number LO through HI as an input line")
    p.add_option("-n", "--head-count", dest="headcount",
            help="output at most HEADCOUNT lines")
    p.add_option("-o", "--output", dest="output",
            help="write result to OUTPUT instead of standard output")
    (opts, args) = p.parse_args(argstr.split())

    lines = ''
    outfd = sys.stdout

    # Write to file if -o is specified
    if opts.output:
        outfd = open(opts.output, 'w')

    if opts.echo:
        if opts.inputrange:
            StdErrException("shuf: cannot combine -e and -i options")

        lines = args
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write("%s\n" % line)

    elif len(args) > 1:
        raise ExtraOperandException(prog, args[1])

    elif opts.inputrange:
        (lo, hi) = opts.inputrange.split('-')
        lines = list(range(int(lo), int(hi)+1))
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write("%i\n" % line)

    else:
        # Use stdin for input if no file is specified
        if len(args) == 0:
            fd = sys.stdin
        else:
            fd = open(args[0])

        lines = fd.readlines()
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write(line)


@addcommand
def smtpd(argstr):
    p = parseoptions()
    p.description = "An RFC 2821 smtp proxy."
    p.usage = '%prog [OPTION]...'
    p.add_option("-a", "--remoteaddress", default="", dest="remoteaddress",
            help="remote address to connect to")
    p.add_option("-p", "--remoteport", default=8025, dest="remoteport",
            type="int", help="remote port to connect to")
    p.add_option("-A", "--localaddress", default="", dest="localaddress",
            help="local address to bind to")
    p.add_option("-P", "--localport", default=8025, dest="localport",
            type="int", help="local port to listen to")
    (opts, args) = p.parse_args(argstr.split())

    _smtpd.SMTPServer((opts.localaddress, opts.localport),
                      (opts.remoteaddress, opts.remoteport))

    asyncore.loop()


@addcommand
def sleep(argstr):
    p = parseoptions()
    p.description = "Pause for NUMBER seconds. SUFFIX may be `s' for " + \
                    "seconds (the default), `m' for minutes, `h' for " + \
                    "hours or `d' for days. Unlike most implementations " + \
                    "that require NUMBER be an integer, here NUMBER may " + \
                    "be an arbitrary floating point number. Given two or " + \
                    "more arguments, pause for the amount of time"
    p.usage = '%prog NUMBER[SUFFIX]...\nor:    %prog OPTION'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    a = []
    try:
        for arg in args:
            if arg.endswith('s'):
                a.append(float(arg[0:-1]))
            elif arg.endswith('m'):
                a.append(float(arg[0:-1]) * 60)
            elif arg.endswith('h'):
                a.append(float(arg[0:-1]) * 3600)
            elif arg.endswith('d'):
                a.append(float(arg[0:-1]) * 86400)
            else:
                a.append(float(arg))
    except ValueError:
        StdErrException("sleep: invalid time interval `%s'. " % (arg) +\
                        "Try sleep --help' for more information.")
        sys.exit(1)

    time.sleep(sum(a))


@addcommand
def sort(argstr):
    p = parseoptions()
    p.description = "sort lines of text files"
    p.usage = "%prog [OPTION]..."
    p.add_option("-r", "--reverse", action="store_true", dest="reverse",
            help="reverse the result of comparisons")
    (opts, args) = p.parse_args(argstr.split())

    l = []
    for line in fileinput.input(args):
        l.append(line)

    l.sort(reverse=opts.reverse or False)
    return ''.join(l)


def tail(argstr):
    # TODO: Everything!!!!!!!!
    p = parseoptions()
    p.description = "Print the last 10 lines of each FILE to standard " + \
                    "output. With more than one FILE, precede each with a " + \
                    "header giving the file name. With no FILE, or when " + \
                    "FILE is -, read standard input."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.add_option("-f", "--follow", action="store_true", dest="follow",
            help="output appended data as the file grows")
    p.add_option("-n", "--lines=N", dest="lines",
            help="output the last N lines, instead of the last 10")
    (opts, args) = p.parse_args(argstr.split())

    interval = 1.0
    f = open('/var/log/messages')

    while 1:
        where = f.tell()
        line = f.readline()
        if not line:
            time.sleep(interval)
            f.seek(where)
        else:
            yield line


@addcommand
@onlyunix
def tee(argstr):
    p = parseoptions()
    p.description = "Copy standard input to each FILE, and also to " + \
                    "standard output."
    p.usage = "%prog [OPTION]... [FILE]..."
    p.add_option("-a", "--append", action="store_true", dest="append",
            help="append to the given FILEs, do not overwrite")
    (opts, args) = p.parse_args(argstr.split())

    fdlist = []
    for filename in args:
        if opts.append:
            fdlist.append(open(filename, 'a'))
        else:
            fdlist.append(open(filename, 'w'))

    for line in sys.stdin.readlines():
        sys.stdout.write(line)
        for fd in fdlist:
            fd.write(line)


@addcommand
def touch(argstr):
    # TODO: Implement --date, --time and -t
    p = parseoptions()
    p.description = "Update the access and modification times of each " + \
                    "FILE to the current time. A FILE argument that does " + \
                    "not exist is created empty. A FILE argument string " + \
                    "of - is handled specially and causes touch to"
    p.usage = '%prog [OPTION]... FILE...'
    p.add_option("-a", action="store_true", dest="accessonly",
            help="change only the access time")
    p.add_option("-c", "--no-create", action="store_true", dest="nocreate",
            help="do not create any files")
    p.add_option("-f", action="store_true", dest="thisoptionshouldbeignored",
            help="(ignored)")
    p.add_option("-m", action="store_true", dest="modonly",
            help="change only the modification time")
    p.add_option("-r", "--reference", dest="reference",
            help="use this file's times instead of current time")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        raise MissingOperandException(prog)

    atime = mtime = time.time()

    for arg in args:
        if not os.path.exists(arg):
            if opts.nocreate:
                # Skip file
                break
            else:
                # Create empty file
                open(arg, 'w').close()

        if opts.reference:
            atime = os.path.getatime(opts.reference)
            mtime = os.path.getmtime(opts.reference)
        if opts.accessonly:
            mtime = os.path.getmtime(arg)
        if opts.modonly:
            atime = os.path.getatime(arg)
        os.utime(arg, (atime, mtime))


@addcommand
def uname(argstr):
    p = parseoptions()
    p.description = "Print certain system information.  With no OPTION, " + \
                    "same as -s."
    p.usage = '%prog [OPTION]...'
    p.add_option("-a", "--all", action="store_true", dest="all",
            help="print all information, in the following order, except " + \
                  "omit -p and -i if unknown")
    p.add_option("-s", "--kernel-name", action="store_true",
            dest="kernelname", help="print the kernel name")
    p.add_option("-n", "--nodename", action="store_true", dest="nodename",
            help="print the network node hostname")
    p.add_option("-r", "--kernel-release", action="store_true",
            dest="kernelrelease", help="print the kernel release")
    p.add_option("-v", "--kernel-version", action="store_true",
            dest="kernelversion", help="print the kernel version")
    p.add_option("-m", "--machine", action="store_true", dest="machine",
            help="print the machine hardware name")
    p.add_option("-p", "--processor", action="store_true", dest="processor",
            help='print the processor type or "unknown"')
    p.add_option("-i", "--hardware-platform", action="store_true",
            dest="hardwareplatform",
            help="print the hardware platform or \"unknown\"")
    p.add_option("-o", "--operating-system", action="store_true",
            dest="operatingsystem", help="print the operating system")
    p.add_option("-A", "--architecture", action="store_true",
            dest="architecture", help="print the systems architecture")
    (opts, args) = p.parse_args(argstr.split())

    output = []

    if opts.kernelname or opts.all:
        output.append(platform.system())

    if opts.nodename or opts.all:
        output.append(platform.node())

    if opts.kernelrelease or opts.all:
        output.append(platform.release())

    if opts.kernelversion or opts.all:
        output.append(platform.version())

    if opts.machine or opts.all:
        output.append(platform.machine())

    if opts.processor:
        output.append(platform.processor())

    if opts.hardwareplatform:
        # Didn't find a way to get this
        output.append('unknown')

    if opts.architecture:
        output.append(" ".join(platform.architecture()))

    if opts.operatingsystem or opts.all or output == []:
        output.append(platform.system())

    return " ".join(output)


@addcommand
def wget(argstr):
    # TODO: Fix for Python3, recursion, proxy, progress bar, you name it...
    p = parseoptions()
    p.description = "Download of files from the Internet"
    p.usage = '%prog [OPTION]... [URL]...'
    p.add_option("-O", "--output-document", dest="outputdocument",
            help="write documents to FILE.")
    p.add_option("-u", "--user-agent", dest="useragent",
            help="identify as AGENT instead of PyCoreutils/VERSION.")
    (opts, args) = p.parse_args(argstr.split())

    if opts.outputdocument:
        fdout = open(opts.outputdocument, 'w')
    else:
        fdout = sys.stdout

    if opts.useragent:
        useragent = opts.useragent
    else:
        useragent = 'PyCoreutils/%s' % __version__

    opener = build_opener()
    opener.addheaders = [('User-agent', useragent)]

    for url in args:
        try:
            fdin = opener.open(url)
        except HTTPError as e:
            StdErrException("HTTP error opening {0}: {1}".format(url, e))

        length = int(fdin.headers['content-length'])
        yield "Getting %i bytes from %s...\n" % (length, url)

        shutil.copyfileobj(fdin, fdout)
        yield "Done\n"


@addcommand
@onlyunix
def whoami(argstr):
    p = parseoptions()
    p.description = "Print the user name associated with the current" + \
                    "effective user ID.\nSame as id -un."
    p.usage = '%prog [OPTION]...'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) > 0:
        raise ExtraOperandException(prog, args[0])

    return _pwd.getpwuid(os.getuid())[0] + "\n"


@addcommand
def yes(argstr):
    p = parseoptions()
    p.description = "Repeatedly output a line with all specified " + \
                    "STRING(s), or `y'."
    p.usage = '%prog [STRING]...\nor:    %prog OPTION'
    (opts, args) = p.parse_args(argstr.split())

    x = ''
    for arg in args:
        x += arg + ' '
    x = x.strip()

    if x == '':
        x = 'y'

    while 1:
        yield x + "\n"


@addcommand
def zip(argstr):
    '''
    Overriding a built-in command. Yes, I known :(
    '''
    p = parseoptions()
    p.description = "package and compress (archive) files"
    p.usage = '%prog -l [OPTION]... ZIPFILE...\n' + \
       '       %prog -t [OPTION]... ZIPFILE...\n' + \
       '       %prog -e [OPTION]... ZIPFILE TARGET\n' + \
       '       %prog -c [OPTION]... ZIPFILE SOURCE...\n'
    p.add_option("-c", "--create", action="store_true", dest="create",
            help="create zipfile from source.")
    p.add_option("-e", "--extract", action="store_true", dest="extract",
            help="extract zipfile into target directory.")
    p.add_option("-l", "--list", action="store_true", dest="list",
            help="list files in zipfile.")
    p.add_option("-t", "--test", action="store_true", dest="test",
            help="test if a zipfile is valid.")
    (opts, args) = p.parse_args(argstr.split())

    if opts.list:
        if len(args) != 1:
            p.print_usage(sys.stderr)
            sys.exit(1)
        zf = zipfile.ZipFile(args[0], 'r')
        zf.printdir()
        zf.close()

    elif opts.test:
        if len(args) != 1:
            p.print_usage(sys.stderr)
            sys.exit(1)
        zf = zipfile.ZipFile(args[0], 'r')
        badfile = zf.testzip()
        if badfile:
            sys.stderr("Error on file {0}\n".format(badfile))
            sys.exit(1)
        else:
            return "{0} tested ok".format(args[0]) + "\n"

    elif opts.extract:
        if len(args) != 2:
            p.print_usage(sys.stderr)
            sys.exit(1)

        zf = zipfile.ZipFile(args[0], 'r')
        out = args[1]
        for path in zf.namelist():
            if path.startswith('./'):
                tgt = os.path.join(out, path[2:])
            else:
                tgt = os.path.join(out, path)

            tgtdir = os.path.dirname(tgt)
            if not os.path.exists(tgtdir):
                os.makedirs(tgtdir)
            fp = open(tgt, 'wb')
            fp.write(zf.read(path))
            fp.close()
        zf.close()

    elif opts.create:
        if len(args) < 2:
            p.print_usage(sys.stderr)
            sys.exit(1)

        def addToZip(zf, path, zippath):
            if os.path.isfile(path):
                zf.write(path, zippath, zipfile.ZIP_DEFLATED)
            elif os.path.isdir(path):
                for nm in os.listdir(path):
                    addToZip(zf, os.path.join(path, nm),
                             os.path.join(zippath, nm))
            else:
                StdErrException("Can't store {0}".format(path))

        zf = zipfile.ZipFile(args[0], 'w', allowZip64=True)
        for src in args[1:]:
            addToZip(zf, src, os.path.basename(src))

        zf.close()

    else:
        p.print_usage(sys.stderr)
        sys.exit(1)




### HELPER FUNCTIONS ########################################################


def compressor(argstr, comptype='gzip', decompress=False):
    '''
    Handles compression and decompression as bzip2 and gzip
    '''
    p = parseoptions()
    p.description = "Compress or uncompress FILEs (by default, compress " + \
                    "FILES in-place)."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.add_option("-c", "--stdout", "--as-stdout", action="store_true",
            dest="stdout",
            help="write on standard output, keep original files unchanged")
    p.add_option("-C", "--compresslevel", dest="compresslevel", type="int",
            default=6, help="set file mode (as in chmod), not a=rwx - umask")
    p.add_option("-d", "--decompress", action="store_true", dest="decompress",
            help="decompress")
    p.add_option("-1", "--fast", action="store_const", dest="compresslevel",
            const=1, help="Use the fastest type of compression")
    p.add_option("-2", action="store_const", dest="compresslevel", const=2,
            help="Use compression level 2")
    p.add_option("-3", action="store_const", dest="compresslevel", const=3,
            help="Use compression level 3")
    p.add_option("-4", action="store_const", dest="compresslevel", const=4,
            help="Use compression level 4")
    p.add_option("-5", action="store_const", dest="compresslevel", const=5,
            help="Use compression level 5")
    p.add_option("-6", action="store_const", dest="compresslevel", const=6,
            help="Use compression level 6")
    p.add_option("-7", action="store_const", dest="compresslevel", const=7,
            help="Use compression level 7")
    p.add_option("-8", action="store_const", dest="compresslevel", const=8,
            help="Use compression level 8")
    p.add_option("-9", "--best", action="store_const", dest="compresslevel",
            const=9, help="Use the best type of compression")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if comptype == 'gzip':
        compresstype = _gzip.GzipFile
        suffix = '.gz'
    elif comptype == 'bzip' or comptype == 'bzip2':
        compresstype = bz2.BZ2File
        suffix = '.bz2'

    infiles = args
    stdin = False

    # Use stdin for input if no file is specified or file is '-'
    if len(args) == 0 or (len(args) == 1 and args[0] == '-'):
        infiles = [sys.stdin]
        stdin = True

    for infile in infiles:
        if opts.decompress or decompress:
            # Decompress
            infile = compresstype(infile, 'rb',
                                  compresslevel=opts.compresslevel)
            if len(args) == 0 or opts.stdout:
                outfile = sys.stdout
            else:
                unzippath = infile.rstrip(suffix)
                if os.path.exists(unzippath):
                    q = input("{0}: {1} already ".format(prog, unzippath) + \
                              "exists; do you wish to overwrite (y or n)? ")
                    if q.upper() != 'Y':
                        StdOutException("not overwritten", 2)

                outfile = open(unzippath, 'wb')
        else:
            # Compress
            zippath = infile + suffix
            infile = open(infile, 'rb')
            if len(args) == 0 or opts.stdout:
                outfile = sys.stdout
            else:
                if os.path.exists(zippath):
                    q = input("{0}: {1} already".format(prog, zippath) + \
                              " exists; do you wish to overwrite (y or n)? ")
                    if q.upper() != 'Y':
                        StdErrException("not overwritten", 2)

                outfile = compresstype(zippath, 'wb',
                                       compresslevel=opts.compresslevel)

        shutil.copyfileobj(infile, outfile)


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
    a = [cmd for cmd in _cmds if cmd.__name__ == commandname]
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
        return os.environ['USER'] # Unix
    if 'USERNAME' in os.environ:
        return os.environ['USERNAME'] # Windows


def getsignals():
    ''' Return a dict of all available signals '''
    signallist = [
        'ABRT', 'CONT', 'IO', 'PROF', 'SEGV', 'TSTP', 'USR2', '_DFL', 'ALRM',
        'FPE', 'IOT', 'PWR', 'STOP', 'TTIN', 'VTALRM', '_IGN', 'BUS', 'HUP',
        'KILL', 'QUIT', 'SYS', 'TTOU', 'WINCH', 'CHLD', 'ILL', 'PIPE', 'RTMAX',
        'TERM', 'URG', 'XCPU', 'CLD', 'INT', 'POLL', 'RTMIN', 'TRAP', 'USR1',
        'XFSZ'
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
        return os.environ['HOME'] # Unix
    if 'HOMEPATH' in os.environ:
        return os.environ['HOMEPATH'] # Windows


def hasher(algorithm, argstr):
    def myhash(fd):
        h = hashlib.new(algorithm)
        with fd as f:
            h.update(f.read())
        return h.hexdigest()
 
    p = parseoptions()
    p.description = "Print or check %s checksums.\n" % (algorithm.upper()) + \
                    "With no FILE, or when FILE is -, read standard input."
    p.usage = '%prog [OPTION]... FILE...'
    (opts, args) = p.parse_args(argstr.split())

    if len(args) == 0 or args == ['-']:
        yield myhash(sys.stdin) + '  -' + "\n"
    else:
        for arg in args:
            yield myhash(open(arg, 'r')) + '  ' + arg + "\n"


def listcommands():
    '''
    Returns a list of all public commands
    '''
    l = []
    for cmd in _cmds:
        l.append(cmd.__name__)
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


def parseoptions():
    def showhelp(option, opt, value, parser):
        raise StdOutException(parser.format_help())

    def showlicense(option, opt, value, parser):
        raise StdOutException(__license__)

    p = optparse.OptionParser(version=__version__, add_help_option=False)
    p.add_option("-h", "-?", "--help", action="callback", callback=showhelp,
                 help="show program's help message and exit")
    p.add_option("--license", action="callback", callback=showlicense,
                 help="show program's license and exit")
    return p


def run(argv=sys.argv, stdout=sys.stdout, stderr=sys.stderr, stdin=sys.stdin):
    '''
    Parse commandline arguments and run command.
    This is where the magic happens :-)

    :param argv:    List of arguments
    :param stdout:  A file-like object to use as stdout
    :param stderr:  A file-like object to use as stderr
    :param stdin:   A file-like object to use as stdin
    :return:        The exit status of the command. None means 0.
    '''
    if os.path.basename(argv[0]) in ['__init__.py', 'coreutils.py']:
        argv = argv[1:]

    p = optparse.OptionParser(version=__version__)
    p.disable_interspersed_args()  # Important!
    p.description = "Coreutils in Pure Python."
    p.usage = "%prog [OPTION]... [COMMAND]..."
    p.epilog = "Available Commands: " + ", ".join(listcommands())
    p.add_option("--createcommandlinks", dest="createcommanddirectory",
            help="Create a symlink to pycoreutils for every available command")
    p.add_option("--runtests", action="store_true", dest="runtests",
            help="Run all sort of tests")
    (opts, args) = p.parse_args(argv)
    prog = p.get_prog_name()

    if argv == []:
        return p.print_help()

    if opts.runtests:
        try:
            from pycoreutils import tests
        except ImportError:
            print("Can't import pycoreutils.tests. Please make sure to " +\
                  "include it in your PYTHONPATH", file=stderr)
            sys.exit(1)
        return tests.runalltests()

    if opts.createcommanddirectory:
        return createcommandlinks(prog, opts.createcommanddirectory)

    # Run the command
    errno = 0
    try:
        commandline = " ".join(args)
        for out in runcommandline(commandline,
                                  stdout=stdout,
                                  stderr=stderr,
                                  stdin=stdin):
            print(out, end='', file=stdout)
    except CommandNotFoundException as err:
        print(err, file=stderr)
        print("Use {0} --help for a list of valid commands.".format(prog))
        errno = 2
    except StdOutException as err:
        print(err, file=stdout)
        errno = err.errno
    except StdErrException as err:
        print(err, file=stderr)
        errno = err.errno
    except IOError as err:
        print("{0}: {1}: {2}".format(
              prog, err.filename, err.strerror), file=stderr)
        errno = err.errno
    except OSError as err:
        print("{0}: {1}: {2}".format(
              prog, err.filename, err.strerror), file=stderr)
        errno = err.errno
    except KeyboardInterrupt:
        errno = 0

    return errno


def runcommandline(commandline, stdout=sys.stdout,
                   stderr=sys.stderr, stdin=sys.stdin):
    '''
    Process a commandline

    :param commandline:   String representing the commandline, i.e. "ls -l /tmp"
    :param stdout:        A file-like object to use as stdout
    :param stderr:        A file-like object to use as stderr
    :param stdin:         A file-like object to use as stdin
    '''
    # Replace std's
    sys.stdout = stdout
    sys.stderr = stderr
    sys.stdin = stdin

    argv = commandline.split(' ')

    prog = os.path.basename(argv[0])
    argstr = ' '.join(argv[1:])
    command = getcommand(prog)
    error = None

    try:
        return command(argstr)
    except Exception as err:
        error = err  # Will be raised later

    # Restore std's
    sys.stdout = sys.__stdout__
    sys.stderr = sys.__stderr__
    sys.stdin = sys.__stdin__

    # Raise previously caught error
    if error:
        raise err


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
        ;errno: Exit status of program
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
        ;errno: Exit status of program
        '''
        self.program = program
        self.errno = errno

    def __str__(self):
        return "{0}: missing operand. Try `{0} --help'".format(self.program) +\
               " for more information."


if __name__ == '__main__':
    sys.exit(run())
