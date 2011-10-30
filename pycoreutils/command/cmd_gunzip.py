# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
from pycoreutils.compressor import compressor


@pycoreutils.addcommand
def gunzip(p):
    compressor(p, 'gzip', True)
