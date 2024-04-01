from wsgiref import simple_server
import base64
import mimetypes
import os
import ssl
import sys
import io
from urllib.parse import parse_qs, urljoin

import cmdix


class WSGIServer(simple_server.WSGIServer):
    """
    WSGIServer with SSL support
    """

    def __init__(
        self,
        server_address,
        certfile=None,
        keyfile=None,
        ca_certs=None,
        ssl_version=ssl.PROTOCOL_SSLv23,
        handler=simple_server.WSGIRequestHandler,
    ):
        simple_server.WSGIServer.__init__(self, server_address, handler)
        self.allow_reuse_address = True
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.ca_certs = ca_certs

    def get_request(self):
        sock, addr = self.socket.accept()
        if self.certfile:
            sock = ssl.wrap_socket(
                sock,
                server_side=True,
                certfile=self.certfile,
                keyfile=self.keyfile,
                ssl_version=self.ssl_version,
                ca_certs=self.ca_certs,
            )
        return sock, addr


class WSGIAuth:
    """
    WSGI middleware for basic authentication
    """

    def __init__(self, app, userdict, realm='authentication'):
        self.app = app
        self.userdict = userdict
        self.realm = realm

    def __call__(self, environ, start_response):
        if 'HTTP_AUTHORIZATION' in environ:
            authtype, authinfo = environ['HTTP_AUTHORIZATION'].split(None, 1)
            if authtype.upper() != 'BASIC':
                start_response(b'200 ', [(b'Content-Type', b'text/html')])
                return [b"Only basic authentication is supported"]
            encodedinfo = bytes(authinfo.encode())
            decodedinfo = base64.b64decode(encodedinfo).decode()
            username, password = decodedinfo.split(':', 1)
            if username in self.userdict:
                if self.userdict[username] == password:
                    return self.app(environ, start_response)

        return wsgierror(
            start_response,
            401,
            "Authentication required",
            [(b'WWW-Authenticate', b'Basic realm={}'.format(self.realm))],
        )


def wsgierror(start_response, code, text, headers=[]):
    h = [(b'Content-Type', b'text/html')]
    h.extend(headers)
    start_response(b'{} '.format(code), h)
    return [
        b'''<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN"><html><head>
                <title>{code} {text}</title></head><body><h1>{code} {text}</h1>
                </body></html>'''.format(code=code, text=text)
    ]


def wsgiserver(app, args):
    """
    Parse opts and return a WSGIServer running app
    """
    # Set protocol version
    if args.ssl_version:
        if args.ssl_version == 'SSLv23':
            ssl_version = ssl.PROTOCOL_SSLv23
        elif args.ssl_version == 'SSLv3':
            ssl_version = ssl.PROTOCOL_SSLv23
        elif args.ssl_version == 'TLSv1':
            ssl_version = ssl.PROTOCOL_TLSv1

    # Authentication
    if args.userlist:
        userdict = {}
        for x in args.userlist:
            username, password = x.split(':', 1)
            userdict[username] = password
        app = WSGIAuth(app, userdict)

    server = WSGIServer(
        (args.address, args.port),
        certfile=args.certfile,
        keyfile=args.keyfile,
        ca_certs=args.cafile,
        ssl_version=ssl_version,
    )
    server.set_app(app)
    return server


def wsgishell(environ, start_response):
    """
    Web shell
    """
    if environ['REQUEST_METHOD'].upper() != 'GET':
        return wsgierror(start_response, 400, 'Bad Request')

    qs = parse_qs(environ['QUERY_STRING'])
    if 'commandline' in qs:
        commandline = qs['commandline'][0]
        stdoutio = io.StringIO()
        stderrio = io.StringIO()
        sys.stdout = stdoutio
        sys.stderr = stderrio
        cmdix.runcommandline(commandline)
        sys.stdout = sys.__stdout__
        sys.stderr = sys.__stderr__
        stdoutio.seek(0)
        stderrio.seek(0)
        stdoutstr = ''.join(stdoutio.readlines())
        stderrstr = ''.join(stderrio.readlines())
        start_response(b'200 ', [(b'Content-Type', b'text/html')])
        return [
            f"<div class='stdout'>{stdoutstr}</div>",
            f"<div class='stderr'>{stderrstr}</div>",
        ]
    else:
        html = template.format(
            title='Cmdix Console',
            css=css,
            banner=cmdix.showbanner(),
            javascript=javascript,
        )
        start_response(b'200 ', [(b'Content-Type', b'text/html')])
        return [html.encode()]


def wsgistatic(environ, start_response):
    """
    Serves static file from basedir
    """
    basedir = '.'

    # Only support the GET-method
    if environ['REQUEST_METHOD'].upper() != 'GET':
        return wsgierror(start_response, 400, 'Bad Request')

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
        return wsgierror(start_response, 404, 'File not found')


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
    res += f'<html><head><title>{path}</title></head><body>\n'
    res += '<big><strong>Listing %s</strong></big><br>\n' % (path)
    if path != '/':
        item = '..'
        res += f'D <a href={urljoin(path, item)}>{item}</a><br/>\n'
    for item in dirlist:
        res += f'D <a href={urljoin(path, item)}>{item}</a><br/>\n'
    for item in filelist:
        res += f'F <a href={urljoin(path, item)}>{item}</a><br/>\n'
    res += '</body></html>'
    return str(res)


def parseargs(p):
    """
    Add arguments and `func` to `p`.

    :param p: ArgumentParser
    :return:  ArgumentParser
    """
    p.set_defaults(func=func)
    p.description = "Start a web server that serves the current directory"
    p.epilog = (
        "To enable https, you must supply a certificate file using "
        + "'-c' and a key using '-k', both PEM-formatted. If both the "
        + "certificate and the key are in one file, just use '-c'."
    )
    p.add_argument(
        "-a", "--address", default="", dest="address", help="address to bind to"
    )
    p.add_argument(
        "-c", "--certfile", dest="certfile", help="Use ssl-certificate for https"
    )
    p.add_argument(
        "-p", "--port", default=8000, dest="port", type=int, help="port to listen to"
    )
    p.add_argument(
        "-k", "--keyfile", dest="keyfile", help="Use ssl-certificate for https"
    )
    p.add_argument(
        "-u",
        "--user",
        action="append",
        dest="userlist",
        help="Add a user for authentication in the form of "
        + "'USER:PASSWORD'. Can be specified multiple times.",
    )
    p.add_argument(
        "-V",
        "--ssl-version",
        dest="ssl_version",
        default="SSLv23",
        help="Must be either SSLv23 (default), SSLv3, or TLSv1",
    )
    p.add_argument(
        "--cafile",
        dest="cafile",
        help="Authenticate remote certificate using CA "
        + "certificate file. Requires -c",
    )
    p.add_argument(
        "-s", "--shell", action="store_true", dest="shell", help="Start a web shell"
    )
    return p


def func(args):
    if args.shell:
        app = wsgishell
    else:
        app = wsgistatic

    server = wsgiserver(app, args)

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
        <div id="output"></div>
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
    margin: 0px;
    padding: 0px;
}

pre {
    margin: 0px;
}

a:link, a:visited, a:active, a:hover {
    color: #ccc;
    text-decoration : none;
    font-weight: bold;
}

input, #output {
    background: #444;
    border : 1px solid #fff;
    font-size : 15px;
    color: #fff;
    width: 95%;
}

#main {
    text-align: center;
}

#output {
    height: 400px;
    overflow: auto;
}

#status {
    font-size: 0.8em;
    font-style: italic;
}

.prompt {
    color: #ff0;
    text-align: left;
}

.stdout {
    color: #fff;
    text-align: left;
}

.stderr {
    color: #f00;
    text-align: left;
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
        output.innerHTML += "<pre>" + xhr.responseText + "</pre>"
        output.scrollTop = output.scrollHeight - output.clientHeight
        status.innerHTML = ''
    }
}

submitinput = function() {
    commandline = inputtext.value
    inputtext.value = ''
    xhr = getXMLHttpRequest()
    xhr.onreadystatechange = updateoutput
    xhr.open('GET', '/?commandline=' + commandline)
    output.innerHTML += "<pre class=prompt># " + commandline + "</pre>"
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
