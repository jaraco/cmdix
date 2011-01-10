#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os

try:
    import grp
    import pwd
except ImportError as err:
    pass


@pycoreutils.addcommand
@pycoreutils.onlyunix
def id(argstr):
    # TODO: List all groups a user belongs to
    p = pycoreutils.parseoptions()
    p.description = "Print user and group information for the specified " + \
                    "USERNAME, or (when USERNAME omitted) for the current " + \
                    "user."
    p.usage = '%prog [OPTION]... [USERNAME]'
    p.add_option("-a", action="store_true", dest="ignoreme",
            help="ignore, for compatibility with other versions")
    p.add_option("-g", "--group", action="store_true", dest="group",
            help="print only the effective group ID")
    p.add_option("-n", "--name", action="store_true", dest="name",
            help="print a name instead of a number, for -ug")
    p.add_option("-u", "--user", action="store_true", dest="user",
            help="print only the effective group ID")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    if len(args) > 1:
        raise pycoreutils.ExtraOperandException(prog, args[1])

    if args == []:
        u = pwd.getpwuid(os.getuid())
    else:
        u = pwd.getpwnam(args[0])

    uid = u.pw_uid
    gid = u.pw_gid
    username = u.pw_name
    g = grp.getgrgid(gid)
    groupname = g.gr_name

    if opts.group and opts.name:
        return groupname

    if opts.group:
        return gid

    if opts.user and opts.name:
        return username

    if opts.user:
        return uid

    if opts.name:
        pycoreutils.StdErrException("id: cannot print only names " +
                                    "or real IDs in default format")

    return "uid={0}({1}) gid={2}({3})\n".format(uid, username, gid, username)
