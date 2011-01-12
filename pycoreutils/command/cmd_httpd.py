#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) 2009, 2010, 2011 Hans van Leeuwen.
# See LICENSE.txt for details.

from __future__ import print_function, unicode_literals
import pycoreutils
import base64
import ssl
import sys

if sys.version_info[0] == 2:
    from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
    from SimpleHTTPServer import SimpleHTTPRequestHandler
    from SocketServer import TCPServer
else:
    from http.server import BaseHTTPRequestHandler, HTTPServer, \
                            SimpleHTTPRequestHandler
    from socketserver import TCPServer


class AuthHTTPRequestHandler(SimpleHTTPRequestHandler):
    '''
    HTTPRequestHandler with basic authentication.

    You must make sure that 'userdict' contains a dictionary with usernames as
    keys and passwords as value.
    '''
    realm = 'MyRealm'
    server_version = 'PyCoreutilsXMLRPCD/' + pycoreutils.__version__
    userdict = {}  # A dictionary with username as key and password as value

    def parse_request(self):
        BaseHTTPRequestHandler.parse_request(self)

        authheader = self.headers.get('Authorization')
        if authheader:
            authtype, authinfo = authheader.split(None, 1)
            if authtype.lower() == 'basic':
                encodedinfo = bytes(authinfo.encode())
                decodedinfo = base64.b64decode(encodedinfo).decode()
                username, password = decodedinfo.split(':', 1)
                if (username, password) in self.userdict.items():
                    return True  # User is authenticated

        # Request Authentication
        self.send_response(401)
        self.send_header('WWW-Authenticate', 'Basic realm=' + self.realm)
        self.end_headers()
        self.wfile.write('Authentication required')


class HTTPSServer(HTTPServer):
    '''
    HTTPServer with SSL support
    '''
    def __init__(self, server_address, RequestHandlerClass, certfile,
                 keyfile=None, ssl_version=ssl.PROTOCOL_SSLv23, ca_certs=None):
        HTTPServer.__init__(self, server_address, RequestHandlerClass)
        self.allow_reuse_address = True
        self.certfile = certfile
        self.keyfile = keyfile
        self.ssl_version = ssl_version
        self.ca_certs = ca_certs

    def do_GET(self):
        body = "404 Page not Found"
        self.send_response(404)
        self.send_header('Content-type', 'text/html')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)

    def get_request(self):
        # override this to wrap socket with SSL
        sock, addr = self.socket.accept()
        conn = ssl.wrap_socket(sock,
                               server_side=True,
                               certfile=self.certfile,
                               keyfile=self.keyfile,
                               ssl_version=self.ssl_version,
                               ca_certs=self.ca_certs)
        return conn, addr


@pycoreutils.addcommand
def httpd(argstr):
    p = pycoreutils.parseoptions()
    p.description = "Start a web server that serves the current directory"
    p.usage = '%prog [OPTION]...'
    p.epilog = "To enable https, you must supply a certificate file using " +\
               "'-c' and a key using '-k', both PEM-formatted. If both the " +\
               "certificate and the key are in one file, just use '-c'."
    p.add_option("-a", "--address", default="", dest="address",
            help="address to bind to")
    p.add_option("-c", "--certfile", dest="certfile",
            help="Use ssl-certificate for https")
    p.add_option("-p", "--port", default=8000, dest="port", type="int",
            help="port to listen to")
    p.add_option("-k", "--keyfile", dest="keyfile",
            help="Use ssl-certificate for https")
    p.add_option("-u", "--user", action="append", dest="userlist",
            help="Add a user for authentication in the form of " +\
                 "'USER:PASSWORD'. Can be specified multiple times.")
    p.add_option("-V", "--ssl-version", dest="ssl_version", default="SSLv23",
            help="Must be either 'SSLv23' (default), 'SSLv3', or 'TLSv1'")
    p.add_option("--cacertfile", dest="cacertfile",
            help="Authenticate remote certificate using CA certificate " +\
                 "file. Requires -c")

    (opts, args) = p.parse_args(argstr.split())

    if opts.help:
        yield p.format_help()
        exit()

    # Add users to the authentication database
    if opts.userlist:
        if not opts.certfile:
            yield "WARNING: You are using authentication without https!\n" +\
                  "This means your password can be sniffed!\n"
        handler = AuthHTTPRequestHandler
        for x in opts.userlist:
            username, password = x.split(':', 1)
            handler.userdict[username] = password
    else:
        handler = SimpleHTTPRequestHandler

    if opts.certfile:
        # Set protocol version
        if opts.ssl_version:
            if opts.ssl_version == 'SSLv23':
                ssl_version = ssl.PROTOCOL_SSLv23
            elif opts.ssl_version == 'SSLv3':
                ssl_version = ssl.PROTOCOL_SSLv23
            elif opts.ssl_version == 'TLSv1':
                ssl_version = ssl.PROTOCOL_TLSv1
        server = HTTPSServer((opts.address, opts.port), handler,
                            certfile=opts.certfile,
                            keyfile=opts.keyfile,
                            ca_certs=opts.cacertfile,
                            ssl_version=ssl_version)
    else:
        server = HTTPServer((opts.address, opts.port), handler)

    try:
        server.serve_forever()
    finally:
        server.server_close()
