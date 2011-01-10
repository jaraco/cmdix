#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import os.path


@pycoreutils.addcommand
@pycoreutils.onlyunix
def ln(argstr):
    p = pycoreutils.parseoptions()
    p.description = ""
    p.usage = '\n%prog [OPTION]... [-T] TARGET LINK_NAME   (1st form)' + \
              '\n%prog [OPTION]... TARGET                  (2nd form)'
    p.add_option("-s", "--symbolic", action="store_true", dest="symbolic",
            help="make symbolic links instead of hard links")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="print a message for each created directory")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        yield p.format_help()
        exit()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)
    elif len(args) == 1:
        src = args[0]
        dst = os.path.basename(src)
    elif len(args) == 2:
        src = args[0]
        dst = args[1]

    if opts.symbolic:
        f = os.symlink
        linktype = 'soft'
    else:
        f = os.link
        linktype = 'hard'

    for src in args:
        if opts.verbose:
            yield "`{0}' -> `{1}'".format(src, dst)
        try:
            f(src, dst)
        except Exception as err:
            yield "ln: creating {0} link `{1}' => `{2}': {3}\n".format(
                   linktype, dst, src, err.strerror)
