#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import calendar
import time


@pycoreutils.addcommand
def cal(argstr):
    now = time.localtime()
    p = pycoreutils.parseoptions()
    p.description = "Displays a calendar"
    p.usage = '%prog [OPTION]... [FILE]...'
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_option("-M", action="store_const", dest="firstweekday", const=0,
            help="Weeks start on Monday")
    p.add_option("-S", action="store_const", dest="firstweekday", const=6,
            help="Weeks start on Sunday", default=6)
    p.add_option("-y", action="store_true", dest="year",
            help="Display a calendar for the specified year")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    cal = calendar.LocaleTextCalendar(opts.firstweekday)

    if opts.year:
        if args != []:
            for arg in args:
                yield cal.formatyear(int(arg))
        else:
            yield cal.formatyear(now.tm_year)
    else:
        if len(args) > 2:
            raise pycoreutils.ExtraOperandException(prog, args[1])
        elif len(args) == 2:
            yield cal.formatmonth(int(args[1]), int(args[0]))
        elif len(args) == 1:
            yield cal.formatyear(int(args[0]))
        else:
            yield cal.formatmonth(now.tm_year, now.tm_mon)
