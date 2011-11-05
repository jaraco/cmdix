# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import os
import signal


def kill(p):
    p.set_defaults(func=func)
    p.description = ""
    p.usage = '%(prog)s kill [ -SIGNAL | -s SIGNAL ] PID ...'
    p.add_argument("pid", nargs="+")
    p.add_argument("-s", "--signal",  action="store", dest="signal",
            default=signal.SIGTERM,
            help="send signal")
    return p


def func(args):
    signals = pycoreutils.getsignals()

    # Add a string option for each signal
    for name, sigint in list(signals.items()):
        signame = 'SIG' + name.upper()
        p.add_argument("--" + signame, action="store_const", dest="signal",
            const=sigint,
            help="send signal {0}".format(signame))

    # Add an integer option for each signal
    for sigint in set(signals.values()):
        if sigint < 10:
            p.add_argument("-%i" % sigint, action="store_const", dest="signal",
                const=sigint, help="send signal {0}".format(sigint))

    if len(args) == 0:
        raise pycoreutils.MissingOperandException(prog)

    try:
        sig = int(args.signal)
    except ValueError:
        sig = args.signal.upper()

    if list(signals.values()).count(sig):
        sigint = sig
    elif sig in signals:
        sigint = signals[sig]
    elif sig.lstrip('SIG') in signals:
        sigint = signals[sig.lstrip('SIG')]
    else:
        raise pycoreutils.StdErrException("kill: {0}: ".format(sig) +\
                              "invalid signal specification")

    for pid in args.pid:
        try:
            pid = int(pid)
        except ValueError:
            raise pycoreutils.StdErrException("kill: {0}: ".format(pid) +\
                                  "arguments must be process or job IDs")

        os.kill(pid, sigint)
