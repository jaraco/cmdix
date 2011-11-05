# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import subprocess


def init(p):
    p.set_defaults(func=func)
    p.description = "Process control initialization"
    return p


def func(args):
    # TODO: Create a real init-system
    mount()
    setHostname()
    pycoreutils.runcommandline('login')


def mount():
    subprocess.call(['/bin/mount', '-a'])


def setHostname():
    hostname = open('/etc/hostname').readline()
    open('/proc/sys/kernel/hostname', 'w').write(hostname)
