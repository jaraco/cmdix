# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import os


def rmdir(p):
    p.set_defaults(func=func)
    p.description = "Remove the DIRECTORY(ies), if they are empty."
    p.usage = '%(prog)s [OPTION]... DIRECTORY...'
    p.add_argument('directory', nargs='+')
    p.add_argument("-p", "--parent", action="store_true", dest="parent",
            help="remove DIRECTORY and its ancestors; e.g., " +
                 "'rmdir -p a/b/c' is similar to 'rmdir a/b/c a/b a'")
    return p


def func(args):
    for arg in args.directory:
        if args.parent:
            os.removedirs(arg)
        else:
            os.rmdir(arg)
