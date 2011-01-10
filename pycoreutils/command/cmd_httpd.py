#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import sys

if sys.version_info[0] == 2:
    from BaseHTTPServer import HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
else:
    from http.server import HTTPServer, SimpleHTTPRequestHandler


@pycoreutils.addcommand
def httpd(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Start a web server that serves the current directory"
    p.usage = '%prog [OPTION]...'
    p.add_option("-a", "--address", default="", dest="address",
            help="address to bind to")
    p.add_option("-p", "--port", default=8000, dest="port", type="int",
            help="port to listen to")
    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        return p.format_help()

    handler = SimpleHTTPRequestHandler
    server = HTTPServer((opts.address, opts.port), handler)

    try:
        server.serve_forever()
    finally:
        server.server_close()
