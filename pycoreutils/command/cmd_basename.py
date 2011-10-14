#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os.path


@pycoreutils.addcommand
def basename(p):
    p.set_defaults(func=func)
    p.description = "Print NAME with any leading directory components " + \
                    "removed. If specified, also remove a trailing SUFFIX."
    p.add_argument('name', nargs='+')


def func(args):
    b = args.name[0]

    # Remove trailing slash to make sure /foo/bar/ is the same as /foo/bar
    if len(b) > 1:
        b = b.rstrip('/')
    b = os.path.basename(b)

    if len(args.name) == 2:
        b = b.rstrip(args.name[1])

    print(b)
