# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import os.path


@pycoreutils.onlyunix
def ln(p):
    p.set_defaults(func=func)
    p.description = "Create symbolic or hard links"
    p.add_argument("TARGET", nargs=1)
    p.add_argument("LINK_NAME", nargs='?')
    p.add_argument("-s", "--symbolic", action="store_true", dest="symbolic",
            help="make symbolic links instead of hard links")
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    return p


def func(args):
    src = args.TARGET
    if args.LINK_NAME:
        dst = args[1]
    else:
        dst = os.path.basename(src)

    if args.symbolic:
        f = os.symlink
        linktype = 'soft'
    else:
        f = os.link
        linktype = 'hard'

    for src in args:
        if args.verbose:
            print("'{0}' -> '{1}'".format(src, dst))
        try:
            f(src, dst)
        except Exception as err:
            print("ln: creating {0} link '{1}' => '{2}': {3}\n".format(
                   linktype, dst, src, err.strerror))
