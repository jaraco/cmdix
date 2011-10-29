# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils


@pycoreutils.addcommand
def init(p):
    p.set_defaults(func=func)
    p.description = "Process control initialization"


def func(args):
    # TODO: Create a real init-system
    pycoreutils.runcommandline('sh')
