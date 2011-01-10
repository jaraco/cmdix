#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os


@pycoreutils.addcommand
def pwd(argstr):
    p = pycoreutils.parseoptions()
    p.description = "print name of current/working directory"
    p.usage = '%prog [OPTION]...'
    p.add_option("-L", "--logical", action="store_true", dest="logical",
            help="use PWD from environment, even if it contains symlinks")
    p.add_option("-P", "--physical", action="store_true", dest="physical",
            help="avoid all symlinks")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    if opts.logical:
        return os.getenv('PWD') + "\n"
    elif opts.physical:
        return os.path.realpath(os.getcwd()) + "\n"
    else:
        return os.getcwd() + "\n"
