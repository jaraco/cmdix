#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import fileinput
import platform
import smtplib
import socket
import sys


@pycoreutils.addcommand
def sendmail(argstr):
    # TODO: Authentication
    p = pycoreutils.parseoptions()
    p.description = "A simple sendmail implementation"
    p.usage = '%prog [OPTION]... [RECIPIENT]...'
    p.add_option("-a", "--address", default="localhost", dest="address",
            help="address to send to. default is localhost")
    p.add_option("-c", "--certfile", dest="certfile",
            help="certificate file to use. implies '-s'")
    p.add_option("-f", "-r", "--sender", dest="sender",
            default=pycoreutils.getcurrentusername() + "@" + platform.node(),
            help="set the envelope sender address")
    p.add_option("-k", "--keyfile", dest="keyfile",
            help="key file to use. implies '-s'")
    p.add_option("-m", "--messagefile", default=sys.stdin,
            dest="messagefile",
            help="read message from file. by default, read from stdin.")
    p.add_option("-p", "--port", default=25, dest="port", type="int",
            help="port to send to. defaults is 25")
    p.add_option("-t", "--timeout", default=socket._GLOBAL_DEFAULT_TIMEOUT,
            help="set timeout in seconds", dest="timeout", type="int")
    p.add_option("-s", "--ssl", action="store_true", dest="ssl",
            help="connect using ssl")
    p.add_option("-v", "--verbose", action="store_true", dest="verbose",
            help="show smtp session")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    msg = ""
    for line in fileinput.input(opts.messagefile):
        msg += line

    if opts.ssl or opts.certfile or opts.keyfile:
        smtp = smtplib.SMTP_SSL(opts.address, opts.port,
                                timeout=opts.timeout,
                                keyfile=opts.keyfile,
                                certfile=opts.certfile)
    else:
        smtp = smtplib.SMTP(opts.address, opts.port, timeout=opts.timeout)

    smtp.set_debuglevel(opts.verbose)
    smtp.sendmail(opts.sender, args, msg)
    smtp.quit()
