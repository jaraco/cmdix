#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import time
import sys


@pycoreutils.addcommand
def sleep(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Pause for NUMBER seconds. SUFFIX may be `s' for " + \
                    "seconds (the default), `m' for minutes, `h' for " + \
                    "hours or `d' for days. Unlike most implementations " + \
                    "that require NUMBER be an integer, here NUMBER may " + \
                    "be an arbitrary floating point number. Given two or " + \
                    "more arguments, pause for the amount of time"
    p.usage = '%prog NUMBER[SUFFIX]...\nor:    %prog OPTION'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

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
        pycoreutils.StdErrException("sleep: invalid time interval " +\
        "`{0}'. Try sleep --help' for more information.".format(arg))
        sys.exit(1)

    time.sleep(sum(a))
