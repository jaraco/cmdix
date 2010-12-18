#!/usr/bin/env python
# -*- coding: utf-8 -*-

# WARNING: This is incomplete software, Not all the flags in the help-section
# are implemented, and some behave different than one might expect!

from __future__ import with_statement
from gzip import GzipFile
from pwd import getpwnam
import hashlib, logging, optparse, os, platform, random, shutil, subprocess, sys, tempfile, time

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
    """ Register a command with pycoreutils """
    _cmds.append(f)


@addcmd
def arch():
    p = _optparse()
    p.description = "Print machine architecture."
    p.usage = '%prog [OPTION]'
    (opts, args) = p.parse_args()

    if len(args) > 0:
        print u"dirname: extra operand `%s'" % (args[0])
        print u"Try arch --help' for more information."
        sys.exit(1)

    print platform.machine(),


@addcmd
def basename():
    p = _optparse()
    p.description = "Print NAME with any leading directory components " + \
                    "removed. If specified, also remove a trailing SUFFIX."
    p.usage = '%prog NAME [SUFFIX]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args()
    
    if len(args) == 0:
        print u"basename: missing operand"
        print u"Try `basename --help' for more information."
        sys.exit(1)

    if len(args) > 2:
        print u"basename: extra operand `%s'" % (args[2])
        print u"Try `basename --help' for more information."
        sys.exit(1)

    b = args[0]

    # Remove trailing slash to make sure /foo/bar/ is the same as /foo/bar
    if len(b) > 1:
        b = b.rstrip('/')
    b = os.path.basename(b)

    if len(args) == 2:
        b = b.rstrip(args[1])

    print b


@addcmd
def cat():
    p = _optparse()
    p.description = "Concatenate FILE(s), or standard input, to standard output."
    p.usage = '%prog [OPTION]... [FILE]...'
    (opts, args) = p.parse_args()

    for arg in args:
        print open(arg).read(),


@addcmd
def chown():
    # TODO: Support for groups and --reference
    p = _optparse()
    p.description = "Change the owner and/or group of each FILE to OWNER " + \
                     "and/or GROUP. With --reference, change the owner and" + \
                     " group of each FILE to those of RFILE."
    p.usage = '%prog [OWNER] FILE'
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"chgrp: missing operand"
        print u"Try chgrp --help' for more information."
        sys.exit(1)

    uid = args.pop(0)
    if not uid.isdigit():
        try:
            user = getpwnam(uid)
        except KeyError:
            print u"chown: invalid user: '%s'" % (uid)
        uid = user.pw_uid

    for arg in args:
        os.chown(arg, int(uid), -1)


@addcmd
def chroot():
    # TODO: Testing!!!
    p = _optparse()
    p.description = "Run COMMAND with root directory set to NEWROOT."
    p.usage = '%prog NEWROOT [COMMAND [ARG]...]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"chroot: missing operand"
        print u"Try chroot --help' for more information."
        sys.exit(1)

    # If no command is given, run ''${SHELL} -i''
    if len(args) == 1:
        args.append(os.environ['SHELL'])
        args.append('-i')

    try:
        os.chroot(args[0])
    except OSError, err:
        print u"chroot: cannot change root directory to %s: %s" % (args[0], err.strerror)

    subprocess.call(args)


@addcmd
def dirname():
    p = _optparse()
    p.description = "Print NAME with its trailing /component removed; if " + \
                    "NAME contains no /'s, output `.' (meaning the current" + \
                    " directory)."
    p.usage = '%prog [NAME]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"dirname: missing operand"
        print u"Try `dirname --help' for more information."
        sys.exit(1)

    if len(args) > 1:
        print u"dirname: extra operand `%s'" % (args[1])
        print u"Try `dirname --help' for more information."
        sys.exit(1)

    d = os.path.dirname(args[0].rstrip('/'))

    if d == '':
        d = '.'

    print d


@addcmd
def env():
    # TODO: --unset
    p = _optparse()
    p.description = "Set each NAME to VALUE in the environment and run COMMAND."
    p.usage = '%prog [OPTION]... [-] [NAME=VALUE]... [COMMAND [ARG]...]'
    p.add_option("-i", "--ignore-environment", action="store_true", dest="ignoreenvironment",
            help="start with an empty environment")
    #p.add_option("-u", "--unset", action="store", dest="unset",
            #help="remove variable from the environment")
    (opts, args) = p.parse_args()

    env = {}
    if not opts.ignoreenvironment:
        env = os.environ

    for arg in args:
        x = arg.split('=')
        if len(x) < 2:
            print u"Invalid argument %s." % (arg)
            print u"Arguments should be in the form of 'foo=bar'"
            sys.exit(127)
    print x[0] + '=' + x[1]

    for k, v in env.iteritems():
        print k + '=' + v


@addcmd
def gzip():
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
    (opts, args) = p.parse_args()

    # Use stdin for input if no file is specified or file is '-'
    if len(args) == 0 or (len(args) == 1 and args[0] == '-'):
        infile = sys.stdin

    # Use stdout for output if no file is specified, or if -c is given
    if len(args) == 0 or opts.stdout:
        outfile = GzipFile(fileobj=sys.stdout, mode='wb', compresslevel=opts.compresslevel)

    for arg in args:
        infile = _fopen(arg, 'r')
        gzippath = arg + '.gz'
        if os.path.exists(gzippath):
            q = raw_input("gzip: %s already exists; do you wish to overwrite (y or n)? " % (gzippath))
            if q.upper() != 'Y':
                print u"not overwritten"
                sys.exit(2)
        outfile = GzipFile(filename=gzippath, mode='wb', compresslevel=opts.compresslevel)
        shutil.copyfileobj(infile, outfile)


@addcmd
def ls():
    # TODO: Everything :)
    p = _optparse()
    p.description = "List information about the FILEs (the current " + \
                    "directory by default). Sort entries " + \
                    "alphabetically if none of -cftuvSUX nor --sort."
    p.usage = '%prog [OPTION]... [FILE]...'
    (opts, args) = p.parse_args()

    if len(args) < 1:
        args = '.'

    for arg in args:
        dirlist = os.listdir(arg)
        dirlist.sort()
        for f in dirlist:
            print(f)


@addcmd
def md5sum():
    _hasher('md5')


@addcmd
def mkdir():
    p = _optparse()
    p.usage = '%prog [OPTION]... DIRECTORY...'
    p.description = "Create the DIRECTORY(ies), if they do not already exist."
    p.add_option("-p", "--parents", action="store_true", dest="parents",
            help="no error if existing, make parent directories as needed")
    p.add_option("-m", "--mode", action="store", dest="mode", default=0777,
            help="set file mode (as in chmod), not a=rwx - umask")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args()

    def _mkdir(path, mode, verbose):
        try:
            os.mkdir(path, mode)
        except OSError:
            print "mkdir: cannot create directory '%s': No such file or directory" % (path)
        if verbose:
            print "mkdir: created directory '%s'" % (path)


    if len(args) < 1:
        print "mkdir: missing operand"
        print "Try `mkdir --help' for more information."
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
                _mkdir(path, int(opts.mode), opts.verbose)
        else:
            _mkdir(arg, int(opts.mode), opts.verbose)


@addcmd
def mktemp():
    # TODO: Templates, most of the options
    p = _optparse()
    p.description = "Create a temporary file or directory, safely, and " + \
                    "print its name."
    p.usage = '%prog [OPTION]... [TEMPLATE]'
    p.add_option("-d", "--directory", action="store_true", dest="directory",
            help="create a directory, not a file")
    (opts, args) = p.parse_args()

    if len(args) == 0:
        if opts.directory:
            print tempfile.mkdtemp(prefix='tmp.')
        else:
            print tempfile.mkstemp(prefix='tmp.')[1]
    elif len(args) == 1:
        raise NotImplementedError("Templates are not yet implemented")
    else:
        print u"mktemp: too many templates"
        print u"Try `mktemp --help' for more information."
        


@addcmd
def mv():
    p = _optparse()
    p.description = "Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY."
    p.usage = '%prog [OPTION]... [-T] SOURCE DEST\nor:    %prog [OPTION]... SOURCE... DIRECTORY\nor:    %prog [OPTION]... -t DIRECTORY SOURCE...'
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="explain what is being done")
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"mv: missing file operand"
        print u"Try 'mv --help' for more information."
        sys.exit(1)
    if len(args) == 1:
        print u"mv: missing destination file operand after '%s'" % (args[0])
        print u"Try 'mv --help' for more information."
        sys.exit(1)

    dest = args.pop()

    for src in args:
        if opts.verbose:
            print u"'%s' -> '%s'" % (src, dest)
        try:
            shutil.move(src, dest)
        except IOError, err:
            print u"mv: %s" % (err.strerror)
            sys.exit(1)


@addcmd
def pwd():
    p = _optparse()
    p.description = "print name of current/working directory"
    p.usage = '%prog [OPTION]...'
    p.add_option("-L", "--logical", action="store_true", dest="logical",
            help="use PWD from environment, even if it contains symlinks")
    p.add_option("-P", "--physical", action="store_true", dest="physical",
            help="avoid all symlinks")
    (opts, args) = p.parse_args()

    if opts.logical:
        print os.getenv('PWD')
    elif opts.physical:
        print os.path.realpath(os.getcwdu())
    else:
        print os.getcwdu()


@addcmd
def rmdir():
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
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"rmdir: missing operand"
        print u"Try 'rmdir --help' for more information."
        sys.exit(1)

    for arg in args:
        if opts.verbose:
            print u"rmdir: removing directory, `%s'" % (arg)
        try:
            os.rmdir(arg)
        except OSError, err:
            if err.errno == 39:
                if opts.ignorefail:
                    break
                print u"rmdir: failed to remove `%s': Directory not empty" % (arg)
            elif err.errno == 1:
                print u"rmdir: failed to remove `%s': Operation not permitted" % (arg)
            elif err.errno == 2:
                print u"rmdir: failed to remove `%s': No such file or directory" % (arg)
            else:
                print u"Unknown error: %s" % (err)
            sys.exit(1)


@addcmd
def seq():
    p = _optparse()
    p.description = "Print numbers from FIRST to LAST, in steps of INCREMENT."
    p.usage = '%prog [OPTION]... LAST\nor:    %prog [OPTION]... FIRST LAST\nor:    %prog [OPTION]... FIRST INCREMENT LAST'
    p.add_option("-s", "--seperator", action="store", dest="seperator",
            help="use SEPERATOR to separate numbers (default: \\n)")
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"seq: missing operand"
        print u"Try 'seq --help' for more information."
        sys.exit(1)

    if len(args) == 1:
        a = range(1, int(args[0])+1)
    elif len(args) == 2:
        a = range(int(args[0]), int(args[1])+1)
    elif len(args) == 3:
        a = range(int(args[0]), int(args[2])+1, int(args[1]))

    if opts.seperator == None:
        for x in a:
            print x
    else:
        for x in xrange(len(a)-1, 0, -1):
            a.insert(x, opts.seperator)
        for x in a:
            sys.stdout.write(str(x))
        print


@addcmd
def sha1sum():
    _hasher('sha1')


@addcmd
def sha224sum():
    _hasher('sha224')


@addcmd
def sha256sum():
    _hasher('sha256')


@addcmd
def sha384sum():
    _hasher('sha384')


@addcmd
def sha512sum():
    _hasher('sha512')


@addcmd
def shred():
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
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"mv: missing file operand"
        print u"Try 'shred --help' for more information."
        sys.exit(1)

    for arg in args:
        for i in xrange(opts.iterations):
            size = os.stat(arg).st_size
            fd = _fopen(arg, mode='w')
            logging.debug('Size:', size)
            fd.seek(0)
            for i in xrange(size):
                # Get random byte
                b = "".join(chr(random.randrange(0, 256)))
                fd.write(b)
            fd.close()


@addcmd
def shuf():
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
    (opts, args) = p.parse_args()

    lines = ''
    outfd = sys.stdout

    # Write to file if -o is specified
    if opts.output:
        outfd = _fopen(opts.output, 'w')

    if opts.echo:
        if opts.inputrange:
            print u"shuf: cannot combine -e and -i options"
            sys.exit(1)
        lines = args
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write("%s\n" % line)

    elif len(args) > 1:
        print u"shuf: extra operand `%s'" % (args[1])
        print u"Try shuf --help' for more information."
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
            fd = _fopen(args[0])

        lines = fd.readlines()
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write(line)


@addcmd
def sleep():
    p = _optparse()
    p.description = "Pause for NUMBER seconds. SUFFIX may be `s' for seconds" + \
                    " (the default), `m' for minutes, `h' for hours or `d' " + \
                    "for days. Unlike most implementations that require " + \
                    "NUMBER be an integer, here NUMBER may be an arbitrary " + \
                    "floating point number. Given two or more arguments, " + \
                    "pause for the amount of time"
    p.usage = '%prog NUMBER[SUFFIX]...\nor:    %prog OPTION'
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"sleep: missing operand"
        print u"Try sleep --help' for more information."
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
        print u"sleep: invalid time interval `%s'" % (arg)
        print u"Try sleep --help' for more information."
        sys.exit(1)

    time.sleep(sum(a))


def tail():
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
    (opts, args) = p.parse_args()

    interval = 1.0
    f = open('/var/log/messages')

    while 1:
        where = f.tell()
        line = f.readline()
        if not line:
            time.sleep(interval)
            f.seek(where)
        else:
            print line,


@addcmd
def touch():
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
    (opts, args) = p.parse_args()

    if len(args) == 0:
        print u"touch: missing operand"
        print u"Try 'touch --help' for more information."
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
def uname():
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
    (opts, args) = p.parse_args()

    x = None

    if opts.kernelname or opts.all:
        x = True
        print platform.system(),
    if opts.nodename or opts.all:
        x = True
        print platform.node(),
    if opts.kernelrelease or opts.all:
        x = True
        print platform.release(),
    if opts.kernelversion or opts.all:
        x = True
        print platform.version(),
    if opts.machine or opts.all:
        x = True
        print platform.machine(),
    if opts.processor or opts.all:
        x = True
        print platform.processor(),
    if opts.hardwareplatform or opts.all:
        x = True
        print platform.architecture()[0],
    if opts.operatingsystem or opts.all:
        x = True
        print platform.system(),

    if not x:
        print platform.system(),


@addcmd
def yes():
    p = _optparse()
    p.description = "Repeatedly output a line with all specified " + \
                    "STRING(s), or `y'."
    p.usage = '%prog [STRING]...\nor:    %prog OPTION'
    (opts, args) = p.parse_args()

    x = ''
    for arg in args:
        x += arg + ' '
    x = x.strip()

    if x == '':
        x = 'y'

    try:
        while 1:
            print x
    except KeyboardInterrupt:
        sys.exit()



############################## PRIVATE FUNCTIONS ##############################


def _checkcmd(command):
    ''' Check a command is available '''
    a = [cmd for cmd in _cmds if cmd.func_name == command]
    l = len(a)
    if l == 0:
        return False
    if l > 1:
        raise "Command '%s' has multiple functions associated with it!" % (command)
    return a[0]


def _fopen(filename, mode='r', bufsize=-1):
    try:
        f = open(filename, mode, bufsize)
    except IOError:
        print "Error opening %s" % (filename)
        sys.exit(1)
    return f


def _hasher(algorithm):
    def myhash(fd):
        h = hashlib.new(algorithm)
        with fd as f:
            h.update(f.read())
        return h.hexdigest()
 
    p = _optparse()
    p.description = "Print or check %s checksums.\n" % (algorithm.upper()) + \
                    "With no FILE, or when FILE is -, read standard input."
    p.usage = '%prog [OPTION]... FILE...'
    (opts, args) = p.parse_args()

    if len(args) == 0 or args == ['-']:
        print myhash(sys.stdin) + '  -'
    else:
        for arg in args:
            print myhash(_fopen(arg, 'r')) + '  ' + arg


def _help():
    print u"Pycoreutils should be run with a command as first parameter."
    print u"Use 'pycoreutils.py <command> --help' for detailed help"
    print
    print u"Valid commands:"
    for cmd in _cmds:
        print '  ' + cmd.func_name
    sys.exit(1)


def _optparse():
    optparser = optparse.OptionParser(version=__version__)
    optparser.add_option("--license", action="callback", callback=_showlicense,
        help="show program's license and exit")
    return optparser


def _showlicense(option, opt, value, parser):
    print __license__
    sys.exit(0)



if __name__ == '__main__':
    # Get the requested command
    requestcmd = os.path.basename(sys.argv[0])
    if requestcmd == 'pycoreutils.py':
        # Print help if pycoreutils.py is directly run without any arguments
        if len(sys.argv) == 1 or sys.argv[1] == "--help":
            _help()
        sys.argv.pop(0)
        requestcmd = sys.argv[0]
    cmd = _checkcmd(requestcmd)
    if cmd == False:
        print u"Command %s not supported." % (sys.argv[0])
        print u"Use pycoreutils.py --help for a list of valid commands."
        sys.exit(1)
    # Run the command
    cmd()
