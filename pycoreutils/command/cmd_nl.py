#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def nl(p):
    p.set_defaults(func=func)
    p.description = "number lines of files"
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_argument('files', nargs='*')
    p.add_argument("-s", "--number-separator", dest="separator", default="\t",
            metavar="STRING", help="add STRING after (possible) line number")
    p.add_argument("-w", "--number-width", dest="width", default=6, type=int,
            metavar="NUMBER", help="use NUMBER columns for line numbers")


def func(args):
    linenr = 0
    for line in fileinput.input(args.files):
        if line == "\n":
            print(" " * (args.width + len(args.separator)) + line, end='')
        else:
            linenr += 1
            print("{0:>{width}}{1}{2}".format(linenr, args.separator, line,
                                              width=args.width), end='')
