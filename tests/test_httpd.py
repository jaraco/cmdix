from cmdix.command import httpd


def test_error_response_uses_native_strings():
    """WSGI requires the status and the headers to be native strings."""
    captured = {}

    def start_response(status, headers):
        captured['status'] = status
        captured['headers'] = headers

    body = httpd.wsgierror(start_response, 404, "not found")

    assert captured['status'] == '404 '
    assert captured['headers'] == [('Content-Type', 'text/html')]
    assert isinstance(body[0], bytes)
    assert b'not found' in body[0]


def test_auth_rejects_unsupported_scheme():
    """A non-basic authorization scheme is answered without calling the app."""
    captured = {}

    def start_response(status, headers):
        captured['status'] = status
        captured['headers'] = headers

    auth = httpd.WSGIAuth(app=lambda environ, start: [], userdict={}, realm='realm')
    body = auth({'HTTP_AUTHORIZATION': 'Bearer token'}, start_response)

    assert captured['status'] == '200 '
    assert captured['headers'] == [('Content-Type', 'text/html')]
    assert body == [b"Only basic authentication is supported"]
