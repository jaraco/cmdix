#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os

try:
    import pwd
except ImportError:
    pass


@pycoreutils.addcommand
@pycoreutils.onlyunix
def chown(argstr):
    # TODO: Support for groups and --reference
    p = pycoreutils.parseoptions()
    p.description = "Change the owner and/or group of each FILE to OWNER " + \
                     "and/or GROUP. With --reference, change the owner and" + \
                     " group of each FILE to those of RFILE."
    p.usage = '%prog [OWNER] FILE'
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    uid = args.pop(0)
    if not uid.isdigit():
        try:
            user = pwd.getpwnam(uid)
        except KeyError:
            raise pycoreutils.StdErrException(
                                  "{0}: invalid user: '{1}'".format(prog, uid))
        uid = user.pw_uid

    for arg in args:
        os.chown(arg, int(uid), -1)
