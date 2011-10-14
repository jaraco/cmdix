# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput


@pycoreutils.addcommand
def sort(p):
    p.set_defaults(func=func)
    p.description = "sort lines of text files"
    p.add_argument('files', nargs='*')
    p.add_argument("-r", "--reverse", action="store_true", dest="reverse",
            help="reverse the result of comparisons")


def func(args):
    l = []
    for line in fileinput.input(args.files):
        l.append(line)

    l.sort(reverse=args.reverse or False)
    print(''.join(l), end='')
