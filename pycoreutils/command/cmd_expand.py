# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def expand(p):
    p.set_defaults(func=func)
    p.description = "Convert tabs in each FILE to spaces"
    p.add_argument('FILE', nargs='*')
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " +\
               "decompressed automatically."
    p.add_argument("-t", "--tabs", type=int, default=8,
                   help="have tabs NUMBER characters apart, not 8")


def func(args):
    for line, filename in pycoreutils.parsefilelist(args.FILE, True):
        print(line.expandtabs(args.tabs), end='')
