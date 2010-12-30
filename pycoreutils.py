#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2010 Hans van Leeuwen.
# Release under the MIT license.
# See LICENSE for details.


# Use modern print-function
from __future__ import print_function

# Check if Python version >= 2.6
import sys
if sys.version_info[0] != 2 or sys.version_info[1] < 6:
    raise Exception("Pycoreutils requires Python version 2.6 or greater")

import fileinput
import gzip
import hashlib
import logging
import logging.handlers
import optparse
import os
import platform
import random
import shutil
import stat
import subprocess
import tempfile
import textwrap
import time
import urllib2
import zipfile

try:
    # 'grp' and 'pwd' are Unix only
    import grp as _grp
    import pwd as _pwd
except ImportError:
    pass


__version__ = '0.0.3'
__license__ = '''
Copyright (c) 2009, 2010 Hans van Leeuwen

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

_cmds = []


def addcmd(f):
    '''
    Register a command with pycoreutils
    '''
    _cmds.append(f)
    return f


def nowindows(f):
    '''
    Decorator that indicates that the command cannot be run on windows
    '''
    f._nowindows = True
    return f


@addcmd
def arch(argstr):
    p = _optparse()
    p.description = "Print machine architecture."
    p.usage = '%prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) > 0:
        print(u"{0}: extra operand `{1}'".format(prog, args[0]))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    print(platform.machine(), end='')


@addcmd
def basename(argstr):
    p = _optparse()
    p.description = "Print NAME with any leading directory components " + \
                    "removed. If specified, also remove a trailing SUFFIX."
    p.usage = '%prog NAME [SUFFIX]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    if len(args) > 2:
        print(u"{0}: extra operand `{1}'".format(prog, args[0]))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    b = args[0]

    # Remove trailing slash to make sure /foo/bar/ is the same as /foo/bar
    if len(b) > 1:
        b = b.rstrip('/')
    b = os.path.basename(b)

    if len(args) == 2:
        b = b.rstrip(args[1])

    print(b)


@addcmd
def cat(argstr):
    p = _optparse()
    p.description = "Concatenate FILE(s), or standard input, " + \
                    "to standard output."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    (opts, args) = p.parse_args(argstr.split())

    for line in fileinput.input(args, openhook=fileinput.hook_compressed):
        print(line)


@addcmd
def cd(argstr):
    p = _optparse()
    p.description = "Change the current working directory to HOME or PATH"
    p.usage = '%prog [PATH]'
    (opts, args) = p.parse_args(argstr.split())

    if len(args) == 0:
        pth = _getuserhome()
    elif len(args) == 1:
        pth = os.path.expanduser(args[0])
    else:
        print(u"{0}: extra operand `{1}'".format(prog, args[0]))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    os.chdir(pth)


@addcmd
@nowindows
def chown(argstr):
    # TODO: Support for groups and --reference
    p = _optparse()
    p.description = "Change the owner and/or group of each FILE to OWNER " + \
                     "and/or GROUP. With --reference, change the owner and" + \
                     " group of each FILE to those of RFILE."
    p.usage = '%prog [OWNER] FILE'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    uid = args.pop(0)
    if not uid.isdigit():
        try:
            user = _pwd.getpwnam(uid)
        except KeyError:
            print(u"chown: invalid user: '{0}'".format(uid))
        uid = user.pw_uid

    for arg in args:
        os.chown(arg, int(uid), -1)


@addcmd
def chroot(argstr):
    # TODO: Testing!!!
    p = _optparse()
    p.description = "Run COMMAND with root directory set to NEWROOT."
    p.usage = '%prog NEWROOT [COMMAND [ARG]...]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    # If no command is given, run ''${SHELL} -i''
    if len(args) == 1:
        args.append(os.environ['SHELL'])
        args.append('-i')

    try:
        os.chroot(args[0])
    except OSError, err:
        print(u"chroot: cannot change root directory to {0}: {1}".format(
                                                    args[0], err.strerror))

    subprocess.call(args)


@addcmd
def dirname(argstr):
    p = _optparse()
    p.description = "Print NAME with its trailing /component removed; if " + \
                    "NAME contains no /'s, output `.' (meaning the current" + \
                    " directory)."
    p.usage = '%prog [NAME]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    if len(args) > 1:
        print(u"{0}: extra operand `{1}'".format(prog, args[0]))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    d = os.path.dirname(args[0].rstrip('/'))

    if d == '':
        d = '.'

    print(d)


@addcmd
def env(argstr):
    # TODO: --unset
    p = _optparse()
    p.description = "Set each NAME to VALUE in the environment and run COMMAND."
    p.usage = '%prog [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]'
    p.add_option("-i", "--ignore-environment", action="store_true", dest="ignoreenvironment",
            help="start with an empty environment")
    #p.add_option("-u", "--unset", action="store", dest="unset",
            #help="remove variable from the environment")
    (opts, args) = p.parse_args(argstr.split())

    env = {}
    if not opts.ignoreenvironment:
        env = os.environ

    for arg in args:
        x = arg.split('=')
        if len(x) < 2:
            print(u"Invalid argument {0}.".format(arg))
            print(u"Arguments should be in the form of 'foo=bar'")
            sys.exit(127)
    print(x[0] + '=' + x[1])

    for k, v in env.iteritems():
        print(k + '=' + v)


@addcmd
def gzip(argstr):
    # TODO: Decompression
    p = _optparse()
    p.description = "Compress or uncompress FILEs (by default, compress FILES in-place)."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.add_option("-c", "--stdout", "--as-stdout", action="store_true", dest="stdout",
            help="write on standard output, keep original files unchanged")
    p.add_option("-C", "--compresslevel", action="store", dest="compresslevel", type="int", default=6,
            help="set file mode (as in chmod), not a=rwx - umask")
    #p.add_option("-d", "--decompress", action="store_true", dest="decompress",
            #help="force decompression")
    p.add_option("-1", "--fast", action="store_const", dest="compresslevel", const=1,
            help="Use the fastest type of compression")
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
    p.add_option("-9", "--best", action="store_const", dest="compresslevel", const=9,
            help="Use the best type of compression")
    (opts, args) = p.parse_args(argstr.split())

    # Use stdin for input if no file is specified or file is '-'
    if len(args) == 0 or (len(args) == 1 and args[0] == '-'):
        infile = sys.stdin

    # Use stdout for output if no file is specified, or if -c is given
    if len(args) == 0 or opts.stdout:
        outfile = gzip.GzipFile(fileobj=sys.stdout,
                                mode='wb',
                                compresslevel=opts.compresslevel)

    for arg in args:
        infile = open(arg, 'r')
        gzippath = arg + '.gz'
        if os.path.exists(gzippath):
            q = raw_input("gzip: %s already exists; do you wish to overwrite (y or n)? " % (gzippath))
            if q.upper() != 'Y':
                print(u"not overwritten", file=sys.stderr)
                sys.exit(2)
        outfile = GzipFile(filename=gzippath, mode='wb', compresslevel=opts.compresslevel)
        shutil.copyfileobj(infile, outfile)


@addcmd
@nowindows
def id(argstr):
    # TODO: List all groups a user belongs to
    p = _optparse()
    p.description = "Print user and group information for the specified " + \
                   "USERNAME, or (when USERNAME omitted) for the current user."
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
        print(u"{0}: extra operand `{1}'".format(prog, args[0]))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

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
        print(groupname)
        return

    if opts.group:
        print(gid)
        return

    if opts.user and opts.name:
        print(username)
        return

    if opts.user:
        print(uid)
        return

    if opts.name:
        print("id: cannot print only names or real IDs in default format")
        sys.exit(1)

    print("uid=%i(%s) gid=%i(%s)" % (uid, username, gid, username))


@addcmd
def ln(argstr):
    p = _optparse()
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
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)
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
            print(u"`%s' -> `%s'" % (src, dst))
        try:
            f(src, dst)
        except Exception, err:
            print(u"ln: creating %s link `%s' => `%s': %s" % (linktype, dst,
                                                            src, err.strerror))
            sys.exit(1)


@addcmd
def logger(argstr):
    # TODO: -i, -f, t
    p = _optparse()
    p.description = "A shell command interface to the syslog system log module"
    p.usage = '%prog [OPTION] [ MESSAGE ... ]'
    p.add_option("--host", action="store", dest="host",
            help="Address of the syslog daemon. The default is ``localhost'.'")
    p.add_option("-p", action="store", dest="priority",
            help="Enter the message with the specified priority. The " + \
                 "priority may as a ``facility.level'' pair. For example, " + \
                 "``-p local3.info'' logs the message(s) as informational " + \
                 "level in the local3 facility. " + \
                 "The default is ``user.notice.''")
    p.add_option("--port", action="store", dest="port",
            help="Port of the syslog daemon. The default is 514'.'")
    p.add_option("-s", action="store_true", dest="stderr",
            help="Log the message to standard error, as well as the " +\
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
    if not handler.facility_names.has_key(facility):
        sys.stderr.write("Unknown facility %s.\n" % facility)
        sys.stderr.write("Valid facilities are:\n")
        facilitylist = handler.facility_names.keys()
        facilitylist.sort()
        for f in facilitylist:
            sys.stderr.write(" %s\n" % f)
        sys.exit(1)

    msg = ' '.join(args)
    levelint = 90 - 10 * handler.priority_names.get(level, 0)

    logger = logging.getLogger('Logger')
    logger.addHandler(handler)
    logger.log(levelint, msg)

    if opts.stderr:
        sys.stderr.write("%s\n" % msg)


@addcmd
def ls(argstr):
    # TODO: Show user and group names in ls -l
    p = _optparse()
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
                print(f)
            else:
                st = os.lstat(path)
                mode = _mode2string(st.st_mode)
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
            modtime = "{0}-{1}-{2} {3:0>2}:{4:0>2}".format(
                mtime.tm_year,
                mtime.tm_mon,
                mtime.tm_yday,
                mtime.tm_hour,
                mtime.tm_min
                )
            print("{0} {1:>{nlink}} {2:<5} {3:<5} {4:>{size}} {5} {6} ".format(
                mode,
                nlink,
                uid,
                gid,
                size,
                modtime,
                f,
                size=sizelen,
                nlink=nlinklen,
                ))


@addcmd
def md5sum(argstr):
    _hasher('md5', argstr)


@addcmd
def mkdir(argstr):
    p = _optparse()
    p.usage = '%prog [OPTION]... DIRECTORY...'
    p.description = "Create the DIRECTORY(ies), if they do not already exist."
    p.add_option("-p", "--parents", action="store_true", dest="parents",
            help="no error if existing, make parent directories as needed")
    p.add_option("-m", "--mode", action="store", dest="mode", default=0777,
            help="set file mode (as in chmod), not a=rwx - umask")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    for arg in args:
        if opts.parents:
            # Recursively create directories.
            # We can't use os.makedirs because -v won't show all intermediate directories
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
                    print(u"mkdir: created directory '%s'" % (path))
        else:
            os.mkdir(arg, int(opts.mode))
            if opts.verbose:
                print(u"mkdir: created directory '%s'" % (arg))


@addcmd
def mktemp(argstr):
    # TODO: Templates, most of the options
    p = _optparse()
    p.description = "Create a temporary file or directory, safely, and " + \
                    "print its name."
    p.usage = '%prog [OPTION]... [TEMPLATE]'
    p.add_option("-d", "--directory", action="store_true", dest="directory",
            help="create a directory, not a file")
    (opts, args) = p.parse_args(argstr.split())

    if len(args) == 0:
        if opts.directory:
            print(tempfile.mkdtemp(prefix='tmp.'))
        else:
            print(tempfile.mkstemp(prefix='tmp.')[1])
    elif len(args) == 1:
        raise NotImplementedError("Templates are not yet implemented")
    else:
        print(u"mktemp: too many templates")
        print(u"Try `mktemp --help' for more information.")


@addcmd
def mv(argstr):
    p = _optparse()
    p.description = "Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY."
    p.usage = '%prog [OPTION]... [-T] SOURCE DEST\nor:    %prog [OPTION]... SOURCE... DIRECTORY\nor:    %prog [OPTION]... -t DIRECTORY SOURCE...'
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="explain what is being done")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)
    if len(args) == 1:
        print(u"mv: missing destination file operand after '%s'" % (args[0]))
        print(u"Try 'mv --help' for more information.")
        sys.exit(1)

    dest = args.pop()

    for src in args:
        if opts.verbose:
            print(u"'%s' -> '%s'" % (src, dest))
        try:
            shutil.move(src, dest)
        except IOError, err:
            print(u"mv: %s" % (err.strerror))
            sys.exit(1)


@addcmd
def pwd(argstr):
    p = _optparse()
    p.description = "print name of current/working directory"
    p.usage = '%prog [OPTION]...'
    p.add_option("-L", "--logical", action="store_true", dest="logical",
            help="use PWD from environment, even if it contains symlinks")
    p.add_option("-P", "--physical", action="store_true", dest="physical",
            help="avoid all symlinks")
    (opts, args) = p.parse_args(argstr.split())

    if opts.logical:
        print(os.getenv('PWD'))
    elif opts.physical:
        print(os.path.realpath(os.getcwdu()))
    else:
        print(os.getcwdu())


@addcmd
def rmdir(argstr):
    # TODO: Implement -p
    p = _optparse()
    p.description = "Remove the DIRECTORY(ies), if they are empty."
    p.usage = '%prog [OPTION]... DIRECTORY...'
    p.add_option("--ignore-fail-on-non-empty", action="store_true", dest="ignorefail",
            help="ignore each failure that is solely because a directory is non-empty")
    #p.add_option("-p", "--parent", action="store_true", dest="seperator",
            #help="remove DIRECTORY and its ancestors; e.g., `rmdir -p a/b/c' is similar " +
            #"to `rmdir a/b/c a/b a'")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="output a diagnostic for every directory processed")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    for arg in args:
        if opts.verbose:
            print(u"rmdir: removing directory, `%s'" % (arg))
        try:
            os.rmdir(arg)
        except OSError, err:
            if err.errno == 39:
                if opts.ignorefail:
                    break
                print(u"rmdir: failed to remove `%s': Directory not empty" % (arg))
            elif err.errno == 1:
                print(u"rmdir: failed to remove `%s': Operation not permitted" % (arg))
            elif err.errno == 2:
                print(u"rmdir: failed to remove `%s': No such file or directory" % (arg))
            else:
                print(u"Unknown error: %s" % (err))
            sys.exit(1)


@addcmd
def seq(argstr):
    p = _optparse()
    p.description = "Print numbers from FIRST to LAST, in steps of INCREMENT."
    p.usage = '%prog [OPTION]... LAST\nor:    %prog [OPTION]... FIRST LAST\nor:    %prog [OPTION]... FIRST INCREMENT LAST'
    p.add_option("-s", "--seperator", action="store", dest="seperator",
            help="use SEPERATOR to separate numbers (default: \\n)")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    if len(args) == 1:
        a = range(1, int(args[0])+1)
    elif len(args) == 2:
        a = range(int(args[0]), int(args[1])+1)
    elif len(args) == 3:
        a = range(int(args[0]), int(args[2])+1, int(args[1]))

    if opts.seperator == None:
        for x in a:
            print(x)
    else:
        for x in xrange(len(a)-1, 0, -1):
            a.insert(x, opts.seperator)
        for x in a:
            sys.stdout.write(str(x))
        print()


@addcmd
def sha1sum(argstr):
    _hasher('sha1', argstr)


@addcmd
def sha224sum(argstr):
    _hasher('sha224', argstr)


@addcmd
def sha256sum(argstr):
    _hasher('sha256', argstr)


@addcmd
def sha384sum(argstr):
    _hasher('sha384', argstr)


@addcmd
def sha512sum(argstr):
    _hasher('sha512', argstr)


@addcmd
def shred(argstr):
    # TODO: This program acts as 'shred -x', and doesn't round file sizes up to the next full block
    p = _optparse()
    p.description = "Overwrite the specified FILE(s) repeatedly, in order " + \
                    "to make it harder for even very expensive hardware " + \
                    "probing to recover the data."
    p.usage = '%prog [OPTION]... FILE...'
    p.add_option("-n", "--iterations", action="store", dest="iterations", default=3,
            help="overwrite ITERATIONS times instead of the default (3)")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="show progress")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    for arg in args:
        for i in xrange(opts.iterations):
            size = os.stat(arg).st_size
            fd = open(arg, mode='w')
            logging.debug('Size:', size)
            fd.seek(0)
            for i in xrange(size):
                # Get random byte
                b = "".join(chr(random.randrange(0, 256)))
                fd.write(b)
            fd.close()


@addcmd
def shuf(argstr):
    p = _optparse()
    p.description = "Write a random permutation of the input lines to " + \
                    "standard output."
    p.usage = '%prog [OPTION]... [FILE]\nor:    %prog -e [OPTION]... [ARG]...\nor:    %prog -i LO-HI [OPTION]...'
    p.add_option("-e", "--echo", action="store_true", dest="echo",
            help="treat each ARG as an input line")
    p.add_option("-i", "--input-range", action="store", dest="inputrange",
            help="treat each number LO through HI as an input line")
    p.add_option("-n", "--head-count", action="store", dest="headcount",
            help="output at most HEADCOUNT lines")
    p.add_option("-o", "--output", action="store", dest="output",
            help="write result to OUTPUT instead of standard output")
    (opts, args) = p.parse_args(argstr.split())

    lines = ''
    outfd = sys.stdout

    # Write to file if -o is specified
    if opts.output:
        outfd = open(opts.output, 'w')

    if opts.echo:
        if opts.inputrange:
            print(u"shuf: cannot combine -e and -i options")
            sys.exit(1)
        lines = args
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write("%s\n" % line)

    elif len(args) > 1:
        print(u"{0}: extra operand `{1}'".format(prog, args[0]))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    elif opts.inputrange:
        (lo, hi) = opts.inputrange.split('-')
        lines = range(int(lo), int(hi)+1)
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


@addcmd
def sleep(argstr):
    p = _optparse()
    p.description = "Pause for NUMBER seconds. SUFFIX may be `s' for seconds" + \
                    " (the default), `m' for minutes, `h' for hours or `d' " + \
                    "for days. Unlike most implementations that require " + \
                    "NUMBER be an integer, here NUMBER may be an arbitrary " + \
                    "floating point number. Given two or more arguments, " + \
                    "pause for the amount of time"
    p.usage = '%prog NUMBER[SUFFIX]...\nor:    %prog OPTION'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

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
        print(u"sleep: invalid time interval `%s'" % (arg))
        print(u"Try sleep --help' for more information.")
        sys.exit(1)

    time.sleep(sum(a))


def tail(argstr):
    # TODO: Everything!!!!!!!!
    p = _optparse()
    p.description = "Print the last 10 lines of each FILE to standard " + \
                    "output. With more than one FILE, precede each with a " + \
                    "header giving the file name. With no FILE, or when " + \
                    "FILE is -, read standard input."
    p.usage = '%prog [OPTION]... [FILE]...'
    p.add_option("-f", "--follow", action="store_true", dest="follow",
            help="output appended data as the file grows")
    p.add_option("-n", "--lines=N", action="store", dest="lines",
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
            print(line, end='')


@addcmd
def touch(argstr):
    # TODO: Implement --date, --time and -t
    p = _optparse()
    p.description = "Update the access and modification times of each FILE " + \
                    "to the current time. A FILE argument that does not " + \
                    "exist is created empty. A FILE argument string of - is" + \
                    " handled specially and causes touch to"
    p.usage = '%prog [OPTION]... FILE...'
    p.add_option("-a", action="store_true", dest="accessonly",
            help="change only the access time")
    p.add_option("-c", "--no-create", action="store_true", dest="nocreate",
            help="do not create any files")
    p.add_option("-f", action="store_true", dest="thisoptionshouldbeignored",
            help="(ignored)")
    p.add_option("-m", action="store_true", dest="modonly",
            help="change only the modification time")
    p.add_option("-r", "--reference", action="store", dest="reference",
            help="use this file's times instead of current time")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if len(args) == 0:
        print(u"{0}: missing operand".format(prog))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

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


@addcmd
def uname(argstr):
    p = _optparse()
    p.description = "Print certain system information.  With no OPTION, " + \
                    "same as -s."
    p.usage = '%prog [OPTION]...'
    p.add_option("-a", "--all", action="store_true", dest="all",
            help="print all information, in the following order, except omit -p and -i if unknown")
    p.add_option("-s", "--kernel-name", action="store_true", dest="kernelname",
            help="print the kernel name")
    p.add_option("-n", "--nodename", action="store_true", dest="nodename",
            help="print the network node hostname")
    p.add_option("-r", "--kernel-release", action="store_true", dest="kernelrelease",
            help="print the kernel release")
    p.add_option("-v", "--kernel-version", action="store_true", dest="kernelversion",
            help="print the kernel version")
    p.add_option("-m", "--machine", action="store_true", dest="machine",
            help="print the machine hardware name")
    p.add_option("-p", "--processor", action="store_true", dest="processor",
            help="print the processor type or \"unknown\"")
    p.add_option("-i", "--hardware-platform", action="store_true", dest="hardwareplatform",
            help="print the hardware platform or \"unknown\"")
    p.add_option("-o", "--operating-system", action="store_true", dest="operatingsystem",
            help="print the operating system")
    (opts, args) = p.parse_args(argstr.split())

    x = None

    if opts.kernelname or opts.all:
        x = True
        print(platform.system(), end='')
    if opts.nodename or opts.all:
        x = True
        print(platform.node(), end='')
    if opts.kernelrelease or opts.all:
        x = True
        print(platform.release(), end='')
    if opts.kernelversion or opts.all:
        x = True
        print(platform.version(), end='')
    if opts.machine or opts.all:
        x = True
        print(platform.machine(), end='')
    if opts.processor or opts.all:
        x = True
        print(platform.processor(), end='')
    if opts.hardwareplatform or opts.all:
        x = True
        print(platform.architecture()[0], end='')
    if opts.operatingsystem or opts.all:
        x = True
        print(platform.system(), end='')

    if not x:
        print(platform.system(), end='')


@addcmd
def wget(argstr):
    # TODO: recursion, proxy, progress bar, you name it...
    p = _optparse()
    p.description = "Download of files from the Internet"
    p.usage = '%prog [OPTION]... [URL]...'
    p.add_option("-O", "--output-document", action="store", dest="outputdocument",
            help="write documents to FILE.")
    p.add_option("-u", "--user-agent", action="store", dest="useragent",
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

    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', useragent)]

    for url in args:
        try:
            fdin = opener.open(url)
        except urllib2.HTTPError, e:
            sys.stderr.write("Error opening %s: %s\n" % (url, e))
            sys.exit(1)

        length = int(fdin.headers['content-length'])
        print(u"Getting %i bytes from %s" % (length, url))

        for data in fdin.read(4096):
            fdout.write(data)

        print(u'Done')


@addcmd
@nowindows
def whoami(argstr):
    p = _optparse()
    p.description = "Print the user name associated with the current" + \
                    "effective user ID.\nSame as id -un."
    p.usage = '%prog [OPTION]...'
    (opts, args) = p.parse_args(argstr.split())

    if len(args) > 0:
        print(u"{0}: extra operand `{1}'".format(prog, args[0]))
        print(u"Try {0} --help' for more information.".format(prog))
        sys.exit(1)

    print(_pwd.getpwuid(os.getuid())[0])


@addcmd
def yes(argstr):
    p = _optparse()
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

    try:
        while 1:
            print(x)
    except KeyboardInterrupt:
        sys.exit()


@addcmd
def zip(argstr):
    '''
    Overriding a built-in command. Yes, I known :(
    '''
    p = _optparse()
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
            sys.stderr(u"Error on file {0}\n".format(badfile))
            sys.exit(1)
        else:
            print("{0} tested ok".format(args[0]))

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
                    addToZip(zf,
                             os.path.join(path, nm), os.path.join(zippath, nm))
            else:
                sys.stderr.out("Can't store {0}".format(path))

        zf = zipfile.ZipFile(args[0], 'w', allowZip64=True)
        for src in args[1:]:
            addToZip(zf, src, os.path.basename(src))

        zf.close()

    else:
        p.print_usage(sys.stderr)
        sys.exit(1)



############################## PRIVATE FUNCTIONS ##############################


def _banner():
    subtext = '-= PyCoreutils Shell version %s =-' % __version__
    return '''\
 ____  _  _  ___  _____  ____  ____  __  __  ____  ____  __    ___
(  _ \( \/ )/ __)(  _  )(  _ \( ___)(  )(  )(_  _)(_  _)(  )  / __)
 )___/ \  /( (__  )(_)(  )   / )__)  )(__)(   )(   _)(_  )(__ \__ \\
(__)   (__) \___)(_____)(_)\_)(____)(______) (__) (____)(____)(___/

''' + subtext.center(68) + "\n"


def _checkcmd(command):
    ''' Check a command is available '''
    a = [cmd for cmd in _cmds if cmd.func_name == command]
    l = len(a)
    if l == 0:
        return False
    if l > 1:
        raise "Command '%s' has multiple functions associated with it!" % (command)
    return a[0]


def _getuserhome():
    '''
    Returns the home-directory of the current user
    '''
    if os.environ.has_key('HOME'):
        return os.environ['HOME'] # Unix
    if os.environ.has_key('HOMEPATH'):
        return os.environ['HOMEPATH'] # Windows


def _getusername():
    '''
    Returns the username of the current user
    '''
    if os.environ.has_key('USER'):
        return os.environ['USER'] # Unix
    if os.environ.has_key('USERNAME'):
        return os.environ['USERNAME'] # Windows


def _hasher(algorithm, argstr):
    def myhash(fd):
        h = hashlib.new(algorithm)
        with fd as f:
            h.update(f.read())
        return h.hexdigest()
 
    p = _optparse()
    p.description = "Print or check %s checksums.\n" % (algorithm.upper()) + \
                    "With no FILE, or when FILE is -, read standard input."
    p.usage = '%prog [OPTION]... FILE...'
    (opts, args) = p.parse_args(argstr.split())

    if len(args) == 0 or args == ['-']:
        print(myhash(sys.stdin) + '  -')
    else:
        for arg in args:
            print(myhash(open(arg, 'r')) + '  ' + arg)


def _listcommands():
    '''
    Returns a list of all public commands
    '''
    l = []
    for cmd in _cmds:
        l.append(cmd.func_name)
    return l


def _mode2string(mode):
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


def _optparse():
    optparser = optparse.OptionParser(version=__version__)
    optparser.add_option("--license", action="callback", callback=_showlicense,
        help="show program's license and exit")
    return optparser


def _showlicense(option, opt, value, parser):
    print(__license__)
    sys.exit(0)



if __name__ == '__main__':
    # Get the requested command
    requestcmd = os.path.basename(sys.argv[0])
    if requestcmd == 'pycoreutils.py':
        # Print help if pycoreutils.py is directly run without any arguments
        if len(sys.argv) == 1 or sys.argv[1] == "--help":
            print(_banner())
            print("Usage: pycoreutils.py COMMAND [ OPTIONS ... ]\n")
            print("Available commands:")

            cmdstring = ", ".join(_listcommands())
            for line in textwrap.wrap(cmdstring, width=80):
                print(line)

            print("\nUse 'pycoreutils.py COMMAND --help' for help")
            sys.exit(1)

        sys.argv.pop(0)
        requestcmd = sys.argv[0]
    cmd = _checkcmd(requestcmd)
    if cmd == False:
        print(u"Command %s not supported." % (sys.argv[0]))
        print(u"Use pycoreutils.py --help for a list of valid commands.")
        sys.exit(1)

    # Check if the '_nowindows'-flag is set
    if hasattr(cmd, '_nowindows') and platform.system() == 'Windows':
        print(u"Command %s does not work on Windows" % (sys.argv[0]))
        sys.exit(1)

    # Run the command
    argstr = ' '.join(sys.argv[1:])
    try:
        cmd(argstr)
    except IOError, err:
        sys.stderr.write(u"{0}: {1}: {2}\n".format(sys.argv[0], err.filename, err.strerror))
        sys.exit(err.errno)
    except OSError, err:
        sys.stderr.write(u"{0}: {1}: {2}\n".format(sys.argv[0], err.filename, err.strerror))
        sys.exit(err.errno)
