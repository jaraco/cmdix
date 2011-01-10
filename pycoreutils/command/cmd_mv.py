#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import shutil


@pycoreutils.addcommand
def mv(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Rename SOURCE to DEST, or move SOURCE(s) to DIRECTORY."
    p.usage = "%prog [OPTION]... [-T] SOURCE DEST\nor:    " + \
              "%prog [OPTION]... SOURCE... DIRECTORY\nor:    " + \
              "%prog [OPTION]... -t DIRECTORY SOURCE..."
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="explain what is being done")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)
    if len(args) == 1:
        pycoreutils.StdErrException("mv: missing destination file operand " +\
                                    "after '{0}'".format(args[0]) +\
                                    "Try 'mv --help' for more information.")

    dest = args.pop()

    for src in args:
        if opts.verbose:
            yield "'{0}' -> '{1}'\n".format(src, dest)

        shutil.move(src, dest)
