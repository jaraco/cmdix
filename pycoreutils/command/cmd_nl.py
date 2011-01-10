#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def nl(argstr):
    p = pycoreutils.parseoptions()
    p.description = "number lines of files"
    p.usage = '%prog [OPTION]... [FILE]'
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_option("-s", "--number-separator", dest="separator", default="\t",
            metavar="STRING",
            help="add STRING after (possible) line number")
    p.add_option("-w", "--number-width", dest="width", default=6, type="int",
            metavar="NUMBER",
            help="use NUMBER columns for line numbers")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    linenr = 0
    for line in fileinput.input(args):
        if line == "\n":
            yield " " * (opts.width + len(opts.separator)) + line
        else:
            linenr += 1
            yield "{0:>{width}}{1}{2}".format(linenr, opts.separator, line,
                                              width=opts.width)
