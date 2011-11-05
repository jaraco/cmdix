# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals


def seq(p):
    p.set_defaults(func=func)
    p.description = "Print numbers from FIRST to LAST, in steps of " +\
                    "INCREMENT."
    p.usage = "%(prog)s [OPTION]... LAST\nor:    %(prog)s [OPTION]... FIRST" +\
              " LAST\nor:    %(prog)s [OPTION]... FIRST INCREMENT LAST"
    p.add_argument("-s", "--seperator", dest="seperator",
            help="use SEPERATOR to separate numbers (default: \\n)")
    return p


def func(args):
    if len(args) == 1:
        a = list(range(1, int(args[0]) + 1))
    elif len(args) == 2:
        a = list(range(int(args[0]), int(args[1]) + 1))
    elif len(args) == 3:
        a = list(range(int(args[0]), int(args[2]) + 1, int(args[1])))

    if opts.seperator == None:
        for x in a:
            print(str(x))
    else:
        for x in range(len(a) - 1, 0, -1):
            a.insert(x, opts.seperator)
        for x in a:
            print(str(x), end='')
        print()
