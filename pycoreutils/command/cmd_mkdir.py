#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os


@pycoreutils.addcommand
def mkdir(argstr):
    p = pycoreutils.parseoptions()
    p.usage = '%prog [OPTION]... DIRECTORY...'
    p.description = "Create the DIRECTORY(ies), if they do not already " + \
                    "exist."
    p.add_option("-p", "--parents", action="store_true", dest="parents",
            help="no error if existing, make parent directories as needed")
    p.add_option("-m", "--mode", dest="mode", default=0o777,
            help="set file mode (as in chmod), not a=rwx - umask")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    for arg in args:
        if opts.parents:
            # Recursively create directories. We can't use os.makedirs
            # because -v won't show all intermediate directories
            path = arg
            pathlist = []

            # Create a list of directories to create
            while not os.path.exists(path):
                pathlist.insert(0, path)
                path, tail = os.path.split(path)

            # Create all directories in pathlist
            for path in pathlist:
                os.mkdir(path, int(opts.mode))
                if opts.verbose:
                    yield "mkdir: created directory `{0}'\n".format(path)
        else:
            os.mkdir(arg, int(opts.mode))
            if opts.verbose:
                yield "mkdir: created directory `{0}'\n".format(arg)
