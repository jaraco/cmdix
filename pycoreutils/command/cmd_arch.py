# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import platform


def arch(p):
    p.set_defaults(func=func)
    p.description = "Print machine architecture."
    return p


def func(args):
    print(platform.machine())
