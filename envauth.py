from os import environ
from functools import wraps


class HTTPBasic(object):
    """This describes a simple pattern for implementing authentication in
    WSGI middleware. This does not propose any new features or environment
    keys; it only describes a baseline recommended practice.
    wsgi.readthedocs.org/en/latest/specifications/simple_authentication.html

    """

    def __init__(self, app, user_database, realm='Website'):
        self.app = app
        self.user_database = user_database
        self.realm = realm

    def __call__(self, environ, start_response):
        def repl_start_response(status, headers, exc_info=None):
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
            if not self.check_auth(username, password):
                return self.authenticate(environ, start_response)
            environ['REMOTE_USER'] = username
            del environ['HTTP_AUTHORIZATION']
        return self.app(environ, repl_start_response)

    def check_auth(self, username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        return user_database.get(username) == password

    def authenticate(self, environ, start_response):
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
        super(EnvAuth, self).__init__(app, environ, realm)

class FlaskEnvAuth(object):

    @staticmethod
    def check_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.
        """
        return environ.get(username) == password

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
                if not auth or not FlaskEnvAuth.check_auth(auth.username,
                                                           auth.password):
                    return FlaskEnvAuth.authenticate(realm)
                return f(*args, **kwargs)
            return wrapper
        return decorator


class BottleEnvAuth(object):

    @staticmethod
    def check_auth(username, password):
        """This function is called to check if a username /
        password combination is valid.

        """
        return environ.get(username) == password

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
                from bottle import request, HTTPError
                try:
                    user, password = request.auth
                except (TypeError, AttributeError):
                    # catch AttributeError because of bug in bottle
                    auth = False
                else:
                    auth = BottleEnvAuth.check_auth(user, password)
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