#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def sort(argstr):
    p = pycoreutils.parseoptions()
    p.description = "sort lines of text files"
    p.usage = "%prog [OPTION]..."
    p.add_option("-r", "--reverse", action="store_true", dest="reverse",
            help="reverse the result of comparisons")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    l = []
    for line in fileinput.input(args):
        l.append(line)

    l.sort(reverse=opts.reverse or False)
    return ''.join(l)
