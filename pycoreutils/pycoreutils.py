#!/usr/bin/env python

import hashlib, logging, optparse, os, platform, sys

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
