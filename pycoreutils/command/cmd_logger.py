#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import logging


@pycoreutils.addcommand
def logger(argstr):
    # TODO: -i, -f, t
    p = pycoreutils.parseoptions()
    p.description = "A shell command interface to the syslog system log " +\
                    "module"
    p.usage = '%prog [OPTION] [ MESSAGE ... ]'
    p.add_option("--host", dest="host",
            help="Address of the syslog daemon. The default is `localhost'")
    p.add_option("-p", dest="priority",
            help="Enter the message with the specified priority. The " +\
                 "priority may as a ``facility.level'' pair. For example, " +\
                 "``-p local3.info'' logs the message(s) as informational " +\
                 "level in the local3 facility. " +\
                 "The default is ``user.notice.''")
    p.add_option("--port", dest="port",
            help="Port of the syslog daemon. The default is 514'.'")
    p.add_option("-s", action="store_true", dest="stderr",
            help="Log the message to standard error, as well as the " +\
                 "system log.")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    if opts.priority:
        facility, level = opts.priority.split('.', 2)
    else:
        facility = 'user'
        level = 'notice'

    if opts.host or opts.port:
        host = opts.host or 'localhost'
        port = opts.port or 514
        address = (host, port)
    else:
        address = '/dev/log'

    handler = logging.handlers.SysLogHandler(address, facility)
    if facility not in handler.facility_names:
        err = "Unknown facility {0}. ".format(facility) +\
              "Valid facilities are: "
        facilitylist = list(handler.facility_names.keys())
        facilitylist.sort()
        for f in facilitylist:
            err += f + ", "

        raise pycoreutils.StdErrException(err)

    msg = ' '.join(args)
    levelint = 90 - 10 * handler.priority_names.get(level, 0)

    logger = logging.getLogger('Logger')
    logger.addHandler(handler)
    logger.log(levelint, msg)

    if opts.stderr:
        raise pycoreutils.StdErrException(msg)
