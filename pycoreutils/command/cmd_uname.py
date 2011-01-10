#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import platform


@pycoreutils.addcommand
def uname(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Print certain system information.  With no OPTION, " + \
                    "same as -s."
    p.usage = '%prog [OPTION]...'
    p.add_option("-a", "--all", action="store_true", dest="all",
            help="print all information, in the following order, except " + \
                  "omit -p and -i if unknown")
    p.add_option("-s", "--kernel-name", action="store_true",
            dest="kernelname", help="print the kernel name")
    p.add_option("-n", "--nodename", action="store_true", dest="nodename",
            help="print the network node hostname")
    p.add_option("-r", "--kernel-release", action="store_true",
            dest="kernelrelease", help="print the kernel release")
    p.add_option("-v", "--kernel-version", action="store_true",
            dest="kernelversion", help="print the kernel version")
    p.add_option("-m", "--machine", action="store_true", dest="machine",
            help="print the machine hardware name")
    p.add_option("-p", "--processor", action="store_true", dest="processor",
            help='print the processor type or "unknown"')
    p.add_option("-i", "--hardware-platform", action="store_true",
            dest="hardwareplatform",
            help="print the hardware platform or \"unknown\"")
    p.add_option("-o", "--operating-system", action="store_true",
            dest="operatingsystem", help="print the operating system")
    p.add_option("-A", "--architecture", action="store_true",
            dest="architecture", help="print the systems architecture")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    output = []

    if opts.kernelname or opts.all:
        output.append(platform.system())

    if opts.nodename or opts.all:
        output.append(platform.node())

    if opts.kernelrelease or opts.all:
        output.append(platform.release())

    if opts.kernelversion or opts.all:
        output.append(platform.version())

    if opts.machine or opts.all:
        output.append(platform.machine())

    if opts.processor:
        output.append(platform.processor())

    if opts.hardwareplatform:
        # Didn't find a way to get this
        output.append('unknown')

    if opts.architecture:
        output.append(" ".join(platform.architecture()))

    if opts.operatingsystem or opts.all or output == []:
        output.append(platform.system())

    return " ".join(output) + "\n"
