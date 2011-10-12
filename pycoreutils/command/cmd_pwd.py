#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import sys


@pycoreutils.addcommand
def pwd(p):
    p.set_defaults(func=func)
    p.description = "print name of current/working directory"
    p.add_argument("-L", "--logical", action="store_true", dest="logical",
            help="use PWD from environment, even if it contains symlinks")
    p.add_argument("-P", "--physical", action="store_true", dest="physical",
            help="avoid all symlinks")


def func(args):
    if args.logical:
        print(os.getenv('PWD'))
    elif args.physical:
        print(os.path.realpath(os.getcwd()))
    else:
        print(os.getcwd())
