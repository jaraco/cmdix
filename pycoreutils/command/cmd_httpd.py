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
    from urlparse import parse_qs, urljoin
else:
    from urllib.parse import parse_qs, urljoin


def wsgishell(environ, start_response):
    '''
    Web shell
    '''
    if environ['REQUEST_METHOD'].upper() != 'GET':
        return pycoreutils.wsgierror(start_response, 400, 'Bad Request')

    qs = parse_qs(environ['QUERY_STRING'])
    if 'commandline' in qs:
        commandline = qs['commandline'][0]
        start_response(b'200 ', [(b'Content-Type', b'text/html')])
        s = ''
        for x in pycoreutils.runcommandline(commandline):
            s += x
        return str(s)
    else:
        html = template.format(title='PyCoreutils Console',
                            css=css,
                            banner=pycoreutils.showbanner(),
                            javascript=javascript)
        start_response(b'200 ', [(b'Content-Type', b'text/html')])
        return [html.encode()]        


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
    p.add_option("-s", "--shell", action="store_true", dest="shell",
            help="Start a web shell")
    p.usage = '%prog [OPTION]...'

    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()
    if opts.shell:
        app = wsgishell
    else:
        app = wsgistatic

    server = pycoreutils.wsgiserver(app, opts)

    try:
        server.serve_forever()
    finally:
        server.server_close()



template = '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">

<head>
    <title>{title}</title>
    <meta http-equiv='content-type' content='text/html; charset=utf-8' />
    <style type="text/css">{css}</style>
    <script type="text/javascript">{javascript}</script>
</head>

<body>
    <div id="main">
        <pre><b>{banner}</b></pre>
        <textarea id="output" readOnly=true></textarea>
        <br/>
        <input id="inputtext" type="text">
        <div id="status"><i>Loading...</i></div>
    </div>
</body>
</html>
'''

css = '''
body {
    background: #000;
    color: #CCC;
    font-family: monospace;
    font-size: 14px;
}

a:link, a:visited, a:active, a:hover {
    color: #ccc;
    text-decoration : none;
    font-weight: bold;
}

input, textarea {
    background: #444;
    border : 1px solid #fff;
    font-size : 15px;
    color: #fff;
    margin: 4px;
    width: 95%;
}

#main {
    text-align: center;
}

#output {
    height: 400px;
}

#status {
    font-size: 0.8em;
    font-style: italic;
}
'''

javascript = '''
function getXMLHttpRequest() {
    var xmlhttp = false;
    var arr = [
        function(){return new XMLHttpRequest();},
        function(){return new ActiveXObject("Microsoft.XMLHTTP");},
        function(){return new ActiveXObject("Msxml2.XMLHTTP");}
    ]
    for (var i=0; i!=arr.length; ++i) {
        try {
            xmlhttp = arr[i]()
            break
        } catch (e){}
    }
    return xmlhttp;
}

updateoutput = function() {
    if (xhr.readyState == 4) {
        output.innerHTML += xhr.responseText
        status.innerHTML = ''
    }
}


submitinput = function() {
    commandline = inputtext.value
    inputtext.value = ''
    xhr = getXMLHttpRequest()
    xhr.onreadystatechange = updateoutput
    xhr.open('GET', '/?commandline=' + commandline)
    output.innerHTML += "# " + commandline + "\\n"
    status.innerHTML = "Running command <strong>" + commandline + "</strong>"
    xhr.send()
}


window.onload = function () {
    inputtext = document.getElementById('inputtext')
    inputtext.onchange = submitinput
    inputtext.autofocus = true
    output = document.getElementById('output')
    status = document.getElementById('status')
    status.innerHTML = ""
}
'''
