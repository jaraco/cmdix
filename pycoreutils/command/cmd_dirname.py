#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os.path
import sys


@pycoreutils.addcommand
def dirname(p):
    p.set_defaults(func=func)
    p.description = "Print NAME with its trailing /component removed; if " + \
                    "NAME contains no /'s, output `.' (meaning the current" + \
                    " directory)."
    p.add_argument('path')


def func(args):
    d = os.path.dirname(args.path.rstrip('/'))
    if d == '':
        d = '.'
    return d + "\n"
