#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import signal


@pycoreutils.addcommand
def kill(argstr):
    signals = pycoreutils.getsignals()

    p = pycoreutils.parseoptions()
    p.description = ""
    p.usage = '%prog kill [ -SIGNAL | -s SIGNAL ] PID ...'
    p.add_option("-s", "--signal",  action="store", dest="signal",
            default=signal.SIGTERM,
            help="send signal")
    (opts, args) = p.parse_args(argstr.split())
    prog = p.get_prog_name()

    if opts.help:
        return p.format_help()

    # Add a string option for each signal
    for name, sigint in list(signals.items()):
        signame = 'SIG' + name.upper()
        p.add_option("--" + signame, action="store_const", dest="signal",
            const=sigint,
            help="send signal {0}".format(signame))

    # Add an integer option for each signal
    for sigint in set(signals.values()):
        if sigint < 10:
            p.add_option("-%i" % sigint, action="store_const", dest="signal",
                const=sigint, help="send signal {0}".format(sigint))

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    try:
        sig = int(opts.signal)
    except ValueError:
        sig = opts.signal.upper()

    if list(signals.values()).count(sig):
        sigint = sig
    elif sig in signals:
        sigint = signals[sig]
    elif sig.lstrip('SIG') in signals:
        sigint = signals[sig.lstrip('SIG')]
    else:
        raise pycoreutils.StdErrException("kill: {0}: ".format(sig) +\
                              "invalid signal specification")

    for pid in args:
        try:
            pid = int(pid)
        except ValueError:
            raise pycoreutils.StdErrException("kill: {0}: ".format(pid) +\
                                  "arguments must be process or job IDs")

        os.kill(pid, sigint)
