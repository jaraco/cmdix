#!/usr/bin/env python

import hashlib, logging, optparse, os, platform, shutil, subprocess, sys

__version__ = '0.0.1'
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

def arch():
    p = _optparse()
    (opts, args) = p.parse_args()

    if len(args) > 0:
        print u"dirname: extra operand `%s'" % (args[0])
        print u"Try arch --help' for more information."
        sys.exit(1)

    print platform.machine(),


def basename():
    p = _optparse()
    (opts, args) = p.parse_args()

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


def cat():
    (opts, args) = _optparse().parse_args()

    for arg in args:
        print open(arg).read(),


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


############################## PRIVATE FUNCTIONS ##############################


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

    p = optparse()
    (opts, args) = p.parse_args()

    if len(args) == 0 or args == ['-']:
        print myhash(sys.stdin) + '  -'
    else:
        for arg in args:
            print myhash(fopen(arg, 'r')) + '  ' + arg


def _optparse():
    optparser = optparse.OptionParser(version=__version__)
    optparser.add_option("--license", action="callback", callback=_showlicense,
        help="show program's license and exit")
    return optparser


def _showlicense(option, opt, value, parser):
    print __license__
    sys.exit(0)


if __name__ == '__main__':
    cmd = os.path.basename(sys.argv[0])
    logging.debug("Running command %s" % (cmd))
    try:
        exec(cmd + '()')
    except NameError:
        sys.stderr.write("Command '%s' not part of pycoreutils\n" % (cmd))
        sys.exit(1)
