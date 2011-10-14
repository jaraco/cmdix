#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import datetime


@pycoreutils.addcommand
@pycoreutils.onlyunix
def uptime(p):
    # TODO: List number of users
    p.set_defaults(func=func)
    p.description = "Tell how long the system has been running"
    p.epilog = "System load averages is the average number of processes " +\
               "that are either in a runnable or uninterruptable state."


def func(args):
    with open('/proc/uptime') as f:
        uptimeseconds = float(f.readline().split()[0])
        uptime = str(datetime.timedelta(seconds=uptimeseconds))[:-10]

    with open('/proc/loadavg') as f:
        load5, load10, load15, proc, unknown = f.readline().split()[:5]
        totproc, avgproc = proc.split('/')

    print(" {0:%H:%M:%S} up ".format(datetime.datetime.today()) +\
          " {0},  {1} users,  ".format(uptime, 'TODO') +\
          "load average: {0}, {1}, {2}".format(load5, load10, load15))
