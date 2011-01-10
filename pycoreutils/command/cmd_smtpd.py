#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import asyncore
import smtpd as _smtpd


@pycoreutils.addcommand
def smtpd(argstr):
    p = pycoreutils.parseoptions()
    p.description = "An RFC 2821 smtp proxy."
    p.usage = '%prog [OPTION]...'
    p.add_option("-a", "--remoteaddress", default="", dest="remoteaddress",
            help="remote address to connect to")
    p.add_option("-p", "--remoteport", default=8025, dest="remoteport",
            type="int", help="remote port to connect to")
    p.add_option("-A", "--localaddress", default="", dest="localaddress",
            help="local address to bind to")
    p.add_option("-P", "--localport", default=8025, dest="localport",
            type="int", help="local port to listen to")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    _smtpd.SMTPServer((opts.localaddress, opts.localport),
                      (opts.remoteaddress, opts.remoteport))

    asyncore.loop()
