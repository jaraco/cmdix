# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils


@pycoreutils.addcommand
def cat(p):
    p.set_defaults(func=func)
    p.description = "Concatenate FILE(s), or standard input, " + \
                    "to standard output."
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_argument('FILE', nargs='*')


def func(args):
    for line, filename in pycoreutils.parsefilelist(args.FILE, True):
        print(line, end='')
