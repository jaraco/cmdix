#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils


@pycoreutils.addcommand
def seq(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Print numbers from FIRST to LAST, in steps of " + \
                    "INCREMENT."
    p.usage = "%prog [OPTION]... LAST\nor:    %prog [OPTION]... FIRST " + \
              "LAST\nor:    %prog [OPTION]... FIRST INCREMENT LAST"
    p.add_option("-s", "--seperator", dest="seperator",
            help="use SEPERATOR to separate numbers (default: \\n)")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    if len(args) == 1:
        a = list(range(1, int(args[0]) + 1))
    elif len(args) == 2:
        a = list(range(int(args[0]), int(args[1]) + 1))
    elif len(args) == 3:
        a = list(range(int(args[0]), int(args[2]) + 1, int(args[1])))

    if opts.seperator == None:
        for x in a:
            yield str(x) + "\n"
    else:
        for x in range(len(a) - 1, 0, -1):
            a.insert(x, opts.seperator)
        for x in a:
            yield str(x)
        yield "\n"
