# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils


@pycoreutils.addcommand
def sha384sum(p):
    pycoreutils.hasher('sha384', p)
