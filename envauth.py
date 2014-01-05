import os
import json
from functools import wraps

__all__ = ['bottle', 'flask', 'wsgi']

class EnvAuth(object):

    @staticmethod
    def check_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.

        """
        credentials = json.loads(os.environ.get('ENVAUTH'))
        if credentials is None:
            return False
        return credentials.get(username) == password

class HTTPBasic(object):
    """This describes a simple pattern for implementing authentication in
    WSGI middleware. This does not propose any new features or environment
    keys; it only describes a baseline recommended practice.
    wsgi.readthedocs.org/en/latest/specifications/simple_authentication.html

    """

    def __init__(self, app, realm='Website'):
        self.app = app
        self.realm = realm

    def __call__(self, environ, start_response):
        def repl_start_response(status, headers):
            if status.startswith('401'):
                HTTPBasic.remove_header(headers, 'WWW-Authenticate')
                headers.append(('WWW-Authenticate',
                                'Basic realm="%s"' % self.realm))
            return start_response(status, headers)
        auth = environ.get('HTTP_AUTHORIZATION')
        if auth:
            scheme, data = auth.split(None, 1)
            assert scheme.lower() == 'basic'
            username, password = data.decode('base64').split(':', 1)
            if not EnvAuth.check_auth(username, password):
                return self.authenticate(start_response)
            environ['REMOTE_USER'] = username
            del environ['HTTP_AUTHORIZATION']
            return self.app(environ, repl_start_response)
        return self.authenticate(repl_start_response)

    def authenticate(self, start_response):
        body = 'Please authenticate'
        headers = [
            ('content-type', 'text/plain'),
            ('content-length', str(len(body))),
            ('WWW-Authenticate', 'Basic realm="%s"' % self.realm)]
        start_response('401 Unauthorized', headers)
        return [body]

    @staticmethod
    def remove_header(headers, name):
        for header in headers:
            if header[0].lower() == name.lower():
                headers.remove(header)
                break

class EnvAuthWSGI(HTTPBasic):

    def __init__(self, app, realm='Website'):
        super(EnvAuthWSGI, self).__init__(app, realm)

class FlaskEnvAuth(object):

    @staticmethod
    def authenticate(realm):
        """Sends a 401 response that enables basic auth"""
        from flask import Response
        
        return Response(
            'Could not verify your access level for that URL.\n'
            'You have to login with proper credentials', 401,
            {'WWW-Authenticate': 'Basic realm="%s"' % realm}
        )

    @staticmethod
    def requires_auth(realm='Website'):
        """
        Decorator for basic authentication. 

        """
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                from flask import request
                auth = request.authorization
                if not auth or not EnvAuth.check_auth(auth.username,
                                                           auth.password):
                    return FlaskEnvAuth.authenticate(realm)
                return f(*args, **kwargs)
            return wrapper
        return decorator


class BottleEnvAuth(object):

    @staticmethod
    def authenticate(realm):
        """Sends a 401 response that enables basic auth"""
        from bottle import HTTPError
        
        return HTTPError(
            401, 'Could not verify your access level for that URL.\n'
                 'You have to login with proper credentials', 
            header={'WWW-Authenticate': 'Basic realm="%s"' % realm}
        )

    @staticmethod
    def requires_auth(realm='Website'):
        """
        Decorator for basic authentication. 

        """
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                from bottle import request
                try:
                    user, password = request.auth
                except (TypeError, AttributeError):
                    # catch AttributeError because of bug in bottle
                    auth = False
                else:
                    auth = EnvAuth.check_auth(user, password)
                if auth:
                    return f(*args, **kwargs)
                else:
                    return BottleEnvAuth.authenticate(realm)
            return wrapper
        return decorator

# Aliases

wsgi = EnvAuthWSGI
flask = FlaskEnvAuth
bottle = BottleEnvAuth