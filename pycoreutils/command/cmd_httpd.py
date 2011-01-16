#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import base64
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
        return pycoreutils.wsgierror(start_response, 400, 'Bad Request')

    urlpath = environ['PATH_INFO']
    filepath = os.path.join(basedir, urlpath.lstrip('/'))
    if os.path.isfile(filepath):
        mimetype = mimetypes.guess_type(filepath)[0]
        start_response(b'200 ', [(b'Content-Type', mimetype)])
        return open(filepath)
    elif os.path.isdir(filepath):
        start_response(b'200 ', [(b'Content-Type', b'text/html')])
        return [list_directory(urlpath, filepath)]
    else:
        return pycoreutils.wsgierror(start_response, 404, 'File not found')


def list_directory(urlpath, filepath):
    """Helper to produce a directory listing (absent index.html).

    Return value is either a file object, or None (indicating an
    wsgierror).  In either case, the headers are sent, making the
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
