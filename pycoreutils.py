#!/usr/bin/env python

from __future__ import with_statement
from gzip import GzipFile
import hashlib, logging, optparse, os, platform, random, shutil, subprocess, sys, time

__version__ = '0.0.2'
__license__ = '''
Copyright (c) 2009 Hans van Leeuwen

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
    (opts, args) = _optparse().parse_args()

    if len(args) > 0:
        print u"dirname: extra operand `%s'" % (args[0])
        print u"Try arch --help' for more information."
        sys.exit(1)

    print platform.machine(),


@addcmd
def basename():
    (opts, args) = _optparse().parse_args()

    if len(args) == 0:
        print u"basename: missing operand"
        print u"Try `basename --help' for more information."
        sys.exit(1)

    if len(args) > 2:
        print u"basename: extra operand `%s'" % (args[2])
        print u"Try `basename --help' for more information."
        sys.exit(1)

    b = os.path.basename(args[0])

    if len(args) == 2:
        b = b.rstrip(args[1])

    print b


@addcmd
def cat():
    (opts, args) = _optparse().parse_args()

    for arg in args:
        print open(arg).read(),


@addcmd
def chroot():
    # TODO: Testing!!!
    (opts, args) = _optparse().parse_args()

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
    (opts, args) = _optparse().parse_args()

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
def gzip():
    # TODO: Everything :)
    p = _optparse()
    p.add_option("-c", "--stdout", "--as-stdout", action="store_true", dest="stdout",
            help="write on standard output, keep original files unchanged")
    p.add_option("-C", "--compresslevel", action="store", dest="compresslevel", type="int", default=6,
            help="set file mode (as in chmod), not a=rwx - umask")
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

    shutil.copyfileobj(infile, outfile)


@addcmd
def ls():
    # TODO: Everything :)
    (opts, args) = _optparse().parse_args()

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
    # TODO: Implent -v
    p = _optparse()
    p.add_option("-p", "--parents", action="store_true", dest="recursive",
            help="no error if existing, make parent directories as needed")
    p.add_option("-m", "--mode=MODE", action="store", dest="mode", default=0777,
            help="set file mode (as in chmod), not a=rwx - umask")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args()

    if len(args) < 1:
        print "mkdir: missing operand"
        print "Try `mkdir --help' for more information."
        sys.exit(1)

    for arg in args:
        if opts.recursive:
            os.makedirs(arg, int(opts.mode))
            print "mkdir: created directory '%s'" % (arg)
        else:
            try:
                os.mkdir(arg, int(opts.mode))
            except OSError:
                print "mkdir: cannot create directory '%s': No such file or directory" % (arg)
            print "mkdir: created directory '%s'" % (arg)


@addcmd
def mv():
    p = _optparse()
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
def seq():
    p = _optparse()
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
                b = "".join(chr(random.randrange(0,256)))
                fd.write(b)
            fd.close()


@addcmd
def shuf():
    p = _optparse()
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
        outfd = pycoreutils.fopen(opts.output, 'w')

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
            fd = pycoreutils.fopen(args[0])

        lines = fd.readlines()
        random.shuffle(lines)

        if opts.headcount:
            lines = lines[0:int(opts.headcount)]
        for line in lines:
            outfd.write(line)


@addcmd
def tail():
    # TODO: Everything!!!!!!!!
    p = _optparse()
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
def sleep():
    (opts, args) = _optparse().parse_args()

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


@addcmd
def touch():
    # TODO: Implement --date, --time and -t
    p = _optparse()
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
    (opts, args) = _optparse().parse_args()

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

    (opts, args) = _optparse().parse_args()

    if len(args) == 0 or args == ['-']:
        print myhash(sys.stdin) + '  -'
    else:
        for arg in args:
            print myhash(_fopen(arg, 'r')) + '  ' + arg


def _help():
    print "Pycoreutils should be run with a command as first parameter."
    print
    print "Valid commands:"
    for cmd in _cmds:
        print cmd.func_name,
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
        if len(sys.argv) == 1:
            _help()
        sys.argv.pop(0)
        requestcmd = sys.argv[0]
    cmd = _checkcmd(requestcmd)
    if cmd == False:
        print u"Command %s not supported." % (sys.argv[0])
        print u"Use pycoreutils.py --help for a list of valid commands."
    # Run the command
    cmd()
