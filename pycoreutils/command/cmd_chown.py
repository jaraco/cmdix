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
def chown(p):
    # TODO: Support for groups and --reference
    p.set_defaults(func=func)
    p.description = "Change the owner and/or group of each FILE to OWNER " + \
                     "and/or GROUP. With --reference, change the owner and" + \
                     " group of each FILE to those of RFILE."
    p.add_argument('files', nargs='*')
    p.add_argument('owner', nargs='?')


def func(args):
    if not args.owner:
        try:
            user = pwd.getpwnam(args.owner)
        except KeyError:
            raise pycoreutils.StdErrException(
                                  "{0}: invalid user: '{1}'".format(prog, uid))
        uid = user.pw_uid

    for arg in args.files:
        os.chown(arg, int(uid), -1)
