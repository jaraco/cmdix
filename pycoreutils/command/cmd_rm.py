#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import os.path


@pycoreutils.addcommand
def rm(argstr):
    p = pycoreutils.parseoptions()
    p.description = "print name of current/working directory"
    p.usage = '%prog [OPTION]... FILE...'
    p.add_option("-f", "--force", action="store_true", dest="force",
            help="ignore nonexistent files, never prompt")
    p.add_option("-r", "-R", "--recursive", action="store_true",
            dest="recursive",
            help="remove directories and their contents recursively")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="explain what is being done")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    def _raise(err):
        if not opts.force:
            raise err

    for arg in args:
        if opts.recursive and os.path.isdir(arg):
            # Remove directory recursively
            for root, dirs, files in os.walk(arg, topdown=False,
                                             onerror=_raise):
                for name in files:
                    path = os.path.join(root, name)
                    os.remove(path)
                    if opts.verbose:
                        yield "Removed file `{0}'\n".format(path)
                for name in dirs:
                    path = os.path.join(root, name)
                    os.rmdir(path)
                    if opts.verbose:
                        yield "Removed directory `{0}'\n".format(path)
            os.rmdir(arg)
        else:
            # Remove single file
            try:
                os.remove(arg)
                if opts.verbose:
                    yield "Removed `{0}'\n".format(arg)
            except OSError as err:
                _raise(err)
