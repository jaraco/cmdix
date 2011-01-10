#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os


@pycoreutils.addcommand
def rmdir(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Remove the DIRECTORY(ies), if they are empty."
    p.usage = '%prog [OPTION]... DIRECTORY...'
    p.add_option("-p", "--parent", action="store_true", dest="parent",
            help="remove DIRECTORY and its ancestors; e.g., " +
                 "`rmdir -p a/b/c' is similar to `rmdir a/b/c a/b a'")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    for arg in args:
        if opts.parent:
            os.removedirs(arg)
        else:
            os.rmdir(arg)
