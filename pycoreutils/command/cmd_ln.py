# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import os.path


@pycoreutils.addcommand
@pycoreutils.onlyunix
def ln(p):
    p.set_defaults(func=func)
    p.description = ""
    p.usage = '\n%(prog)s [OPTION]... [-T] TARGET LINK_NAME   (1st form)' + \
              '\n%(prog)s [OPTION]... TARGET                  (2nd form)'
    p.add_argument("-s", "--symbolic", action="store_true", dest="symbolic",
            help="make symbolic links instead of hard links")
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")


def func(args):
    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)
    elif len(args) == 1:
        src = args[0]
        dst = os.path.basename(src)
    elif len(args) == 2:
        src = args[0]
        dst = args[1]

    if opts.symbolic:
        f = os.symlink
        linktype = 'soft'
    else:
        f = os.link
        linktype = 'hard'

    for src in args:
        if opts.verbose:
            print("`{0}' -> `{1}'".format(src, dst))
        try:
            f(src, dst)
        except Exception as err:
            print("ln: creating {0} link `{1}' => `{2}': {3}\n".format(
                   linktype, dst, src, err.strerror))
