#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import mimetypes
import os
import posixpath
import sys

if sys.version_info[0] == 2:
    from urlparse import urljoin
else:
    from urllib.parse import urljoin


def wsgistatic(environ, start_response):
    """
    Serves static file from basedir
    """
    basedir = '.'

    # Only support the GET-method
    if environ['REQUEST_METHOD'].upper() != 'GET':
        start_response('400 ', [('Content-Type', 'text/html')])
        return ['''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
        <HTML><HEAD><TITLE>400 Bad Request</TITLE></HEAD><BODY>
        <H1>400 Bad Request</H1>Expected POST-request</BODY></HTML>''']

    urlpath = environ['PATH_INFO']
    filepath = os.path.join(basedir, urlpath.lstrip('/'))
    if os.path.isfile(filepath):
        t = mimetypes.guess_type(filepath)
        f = open(filepath)
        start_response(b'200 ', [(b'Content-Type', t)])
        return f
    elif os.path.isdir(filepath):
        start_response(b'200 ', [(b'Content-Type', b'text/html')])
        return [list_directory(urlpath, filepath)]
    else:
        start_response(b'404 ', [(b'Content-Type', b'text/html')])
        return ['''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
        <HTML><HEAD><TITLE>404 File not found</TITLE></HEAD><BODY>
        <H1>404 File not found</H1>Nothing matches the given URI</BODY></HTML>''']


def list_directory(urlpath, filepath):
    """Helper to produce a directory listing (absent index.html).

    Return value is either a file object, or None (indicating an
    error).  In either case, the headers are sent, making the
    interface the same as for send_head().
    """
    path = urlpath.rstrip('/') + '/'
    listdir = os.listdir(filepath)
    dirlist = []
    filelist = []

    for file in listdir:
        if os.path.isdir(os.path.join(path, file)):
            dirlist.append(file)
        else:
            filelist.append(file)

    dirlist.sort()
    filelist.sort()

    res = '<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.0 Transitional//EN">\n'
    res += '<html><head><title>{0}</title></head><body>\n'.format(path)
    res += '<big><strong>Listing %s</strong></big><br>\n' % (path)
    if path != '/':
        item = '..'
        res += 'D <a href=%s>%s</a><br/>\n' % (urljoin(path, item), item)
    for item in dirlist:
        res += 'D <a href=%s>%s</a><br/>\n' % (urljoin(path, item), item)
    for item in filelist:
        res += 'F <a href=%s>%s</a><br/>\n' % (urljoin(path, item), item)
    res += '</body></html>'
    return str(res)


@pycoreutils.addcommand
def httpd(argstr):
    p = pycoreutils.wsgiserver_getoptions()
    p.description = "Start a web server that serves the current directory"
    p.usage = '%prog [OPTION]...'

    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    server = pycoreutils.wsgiserver(wsgistatic, opts)

    try:
        server.serve_forever()
    finally:
        server.server_close()
