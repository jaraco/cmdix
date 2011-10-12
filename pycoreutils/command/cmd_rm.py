#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import os.path


@pycoreutils.addcommand
def rm(p):
    p.description = "print name of current/working directory"
    p.add_argument('files', nargs='+')
    p.add_argument("-f", "--force", action="store_true", dest="force",
                   help="ignore nonexistent files, never prompt")
    p.add_argument("-r", "-R", "--recursive", action="store_true",
                   dest="recursive",
                   help="remove directories and their contents recursively")
    p.add_argument("-v", "--verbose", action="store_true", dest="verbose",
                   help="explain what is being done")


def func(args):
    def _raise(err):
        if not args.force:
            raise err

    for arg in args.files:
        if args.recursive and os.path.isdir(arg):
            # Remove directory recursively
            for root, dirs, files in os.walk(arg, topdown=False,
                                             onerror=_raise):
                for name in files:
                    path = os.path.join(root, name)
                    os.remove(path)
                    if args.verbose:
                        print("Removed file `{0}'\n".format(path))
                for name in dirs:
                    path = os.path.join(root, name)
                    os.rmdir(path)
                    if args.verbose:
                        print("Removed directory `{0}'\n".format(path))
            os.rmdir(arg)
        else:
            # Remove single file
            try:
                os.remove(arg)
                if args.verbose:
                    print("Removed `{0}'\n".format(arg))
            except OSError as err:
                _raise(err)
