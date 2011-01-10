#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def expand(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Convert tabs in each FILE to spaces"
    p.usage = "%prog [OPTION]... [FILE]..."
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " +\
               "decompressed automatically."
    p.add_option("-t", "--tabs", type="int", default=8, dest="tabs",
            help="have tabs NUMBER characters apart, not 8")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    for line in fileinput.input(args, openhook=fileinput.hook_compressed):
        yield line.expandtabs(opts.tabs)
