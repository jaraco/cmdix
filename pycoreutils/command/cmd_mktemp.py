#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import tempfile


@pycoreutils.addcommand
def mktemp(argstr):
    # TODO: Templates, most of the options
    p = pycoreutils.parseoptions()
    p.description = "Create a temporary file or directory, safely, and " + \
                    "print its name."
    p.usage = '%prog [OPTION]... [TEMPLATE]'
    p.add_option("-d", "--directory", action="store_true", dest="directory",
            help="create a directory, not a file")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    if len(args) == 0:
        if opts.directory:
            return tempfile.mkdtemp(prefix='tmp.') + "\n"
        else:
            return tempfile.mkstemp(prefix='tmp.')[1] + "\n"
    elif len(args) == 1:
        raise NotImplementedError("Templates are not yet implemented")
    else:
        raise pycoreutils.StdErrException("mktemp: too many templates. " +\
                              "Try `mktemp --help' for more information.")
