# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils.lib


def parseargs(p):
    '''
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    '''
    p.set_defaults(func=func)
    p.description = "Concatenate FILE(s), or standard input, " + \
                    "to standard output."
    p.epilog = "If the FILE ends with '.bz2' or '.gz', the file will be " + \
               "decompressed automatically."
    p.add_argument('FILE', nargs='*')
    return p


def func(args):
    for f in pycoreutils.lib.parsefilelist(args.FILE, True):
        for line in f:
            print(line.decode('utf-8'), end='')
