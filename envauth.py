from os import environ


def remove_header(headers, name):
    for header in headers:
        if header[0].lower() == name.lower():
            headers.remove(header)
            break

class HTTPBasic(object):
    """This describes a simple pattern for implementing authentication in
    WSGI middleware. This does not propose any new features or environment keys;
    it only describes a baseline recommended practice.
    wsgi.readthedocs.org/en/latest/specifications/simple_authentication.html"""

    def __init__(self, app, user_database, realm='Website'):
        self.app = app
        self.user_database = user_database
        self.realm = realm

    def __call__(self, environ, start_response):
        def repl_start_response(status, headers, exc_info=None):
            if status.startswith('401'):
                remove_header(headers, 'WWW-Authenticate')
                headers.append(('WWW-Authenticate', 'Basic realm="%s"' % self.realm))
            return start_response(status, headers)
        auth = environ.get('HTTP_AUTHORIZATION')
        if auth:
            scheme, data = auth.split(None, 1)
            assert scheme.lower() == 'basic'
            username, password = data.decode('base64').split(':', 1)
            if self.user_database.get(username) != password:
                return self.bad_auth(environ, start_response)
            environ['REMOTE_USER'] = username
            del environ['HTTP_AUTHORIZATION']
        return self.app(environ, repl_start_response)

    def bad_auth(self, environ, start_response):
        body = 'Please authenticate'
        headers = [
            ('content-type', 'text/plain'),
            ('content-length', str(len(body))),
            ('WWW-Authenticate', 'Basic realm="%s"' % self.realm)]
        start_response('401 Unauthorized', headers)
        return [body]

class EnvAuth(HTTPBasic):

    def __init__(self, app, realm='Website'):
        super(EnvAuth, self).__init__(app, environ, realm)
