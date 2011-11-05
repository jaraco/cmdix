# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals


def yes(p):
    p.set_defaults(func=func)
    p.usage = '%(prog)s [STRING]...\nor:    %(prog)s OPTION'
    p.add_argument('string', nargs='*')
    p.description = "Repeatedly output a line with all specified " + \
                    "STRING(s), or `y'."
    return p


def func(args):
    x = ''
    for arg in args.string:
        x += arg + ' '
    x = x.strip()

    if x == '':
        x = 'y'

    while 1:
        print(x)
