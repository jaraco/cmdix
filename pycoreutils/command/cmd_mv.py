# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import shutil


def mv(p):
    p.set_defaults(func=func)
    p.description = "Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY."
    p.usage = "%(prog)s [OPTION]... [-T] SOURCE DEST\nor:    " + \
              "%(prog)s [OPTION]... SOURCE... DIRECTORY\nor:    " + \
              "%(prog)s [OPTION]... -t DIRECTORY SOURCE..."
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose",
            help="explain what is being done")
    return p


def func(args):
    dest = args.pop()

    for src in args:
        if opts.verbose:
            print("'{0}' -> '{1}'".format(src, dest))

        shutil.move(src, dest)
