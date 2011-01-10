#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os.path


@pycoreutils.addcommand
def dirname(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Print NAME with its trailing /component removed; if " + \
                    "NAME contains no /'s, output `.' (meaning the current" + \
                    " directory)."
    p.usage = '%prog [NAME]\nor:    %prog [OPTION]'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    if len(args) > 1:
        raise pycoreutils.ExtraOperandException(prog, args[1])

    d = os.path.dirname(args[0].rstrip('/'))

    if d == '':
        d = '.'

    return d + "\n"
