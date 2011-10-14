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
def id(p):
    # TODO: List all groups a user belongs to
    p.set_defaults(func=func)
    p.description = "Print user and group information for the specified " + \
                    "USERNAME, or (when USERNAME omitted) for the current " + \
                    "user."
    p.usage = '%(prog)s [OPTION]... [USERNAME]'
    p.add_argument('username', nargs='?')
    p.add_argument("-a", action="store_true", dest="ignoreme",
            help="ignore, for compatibility with other versions")
    p.add_argument("-g", "--group", action="store_true", dest="group",
            help="print only the effective group ID")
    p.add_argument("-n", "--name", action="store_true", dest="name",
            help="print a name instead of a number, for -ug")
    p.add_argument("-u", "--user", action="store_true", dest="user",
            help="print only the effective group ID")


def func(args):
    if args.username:
        u = pwd.getpwnam(args.username)
    else:
        u = pwd.getpwuid(os.getuid())

    uid = u.pw_uid
    gid = u.pw_gid
    username = u.pw_name
    g = grp.getgrgid(gid)
    groupname = g.gr_name

    if args.group and args.name:
        return groupname

    if args.group:
        return gid

    if args.user and args.name:
        return username

    if args.user:
        return uid

    if args.name:
        pycoreutils.StdErrException("id: cannot print only names " +
                                    "or real IDs in default format")

    print("uid={0}({1}) gid={2}({3})".format(uid, username, gid, username))
