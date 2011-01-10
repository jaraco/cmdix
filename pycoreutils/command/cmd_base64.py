#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import base64 as _base64
import fileinput
import textwrap


@pycoreutils.addcommand
def base64(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Base64 encode or decode FILE, or standard input, " + \
                    "to standard output."
    p.usage = '%prog [OPTION]... [FILE]'
    p.add_option("-d", action="store_true", dest="decode",
            help="decode data")
    p.add_option("-w", dest="wrap", default=76, type="int",
            help="wrap encoded lines after COLS character (default 76). " + \
                 "Use 0 to disable line wrapping")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    s = ''
    for line in fileinput.input(args):
        s += line

    if opts.decode:
        out = _base64.b64decode(s)
        if opts.wrap == 0:
            yield out
        else:
            for line in textwrap.wrap(out, opts.wrap):
                yield line + "\n"
    else:
        out = _base64.b64encode(s)
        if opts.wrap == 0:
            yield out
        else:
            for line in textwrap.wrap(out, opts.wrap):
                yield line + "\n"
