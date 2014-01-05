.. image:: http://www.authenticationtutorial.com/tutorial/basiclogin.gif
    :alt: pypi
    :align: left
    :target: https://pypi.python.org/pypi/envauth

Super simple authentication middleware for when you quickly need to password
protect something and don't have the time to implement rigorous authentication.

$ENVAUTH
========

``envauth`` looks for a ``JSON`` object in the ``ENVAUTH`` environment variable.
The keys are the usernames and the values contains the passwords.

.. code:: javascript

    {"username": "password", "anotheruser": "pass1234"}

Heroku Example
--------------

    heroku config:add ENVAUTH='{"username": "password", "anotheruser": "pass1234"}'

Examples
========

Flask
-----

.. code:: python

    import envauth

    @app.route('/secret-page')
    @envauth.flask.requires_auth(realm='You shall not pass!')
    def secret_page():
        return render_template('secret_page.html')

Bottle
------

.. code:: python

    import envauth

    @app.route('/secret-page')
    @envauth.bottle.requires_auth(realm='You shall not pass!')
    def secret_page():
        return template('secret_page.html')

WSGI
----

.. code:: python

    import envauth

    application = envauth.wsgi(application, realm='You shall not pass!')

Installation
============

Install *envauth* with pip:

::

    $ pip install envauth