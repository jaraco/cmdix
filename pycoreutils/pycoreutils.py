#!/usr/bin/env python

import hashlib, sys
from optparse import OptionParser


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


def fopen(filename, mode='r', bufsize=-1):
    try:
        f = open(filename, mode, bufsize)
    except IOError:
        print "Error opening %s" % (filename)
        sys.exit(1)
    return f


def hasher(algorithm):
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


def optparse():
    optparser = OptionParser(version=__version__)
    optparser.add_option("--license", action="callback", callback=showlicense,
        help="show program's license and exit")
    return optparser


def showlicense(option, opt, value, parser):
    print __license__
    sys.exit(0)


if __name__ == '__main__':
    print optparse()