Super simple authentication middleware for when you quickly need to password
protect something and don't have the time to implement rigorous authentication.
Supports ``Flask``, ``bottle``, ``Django`` and generic ``WSGI`` servers out of the box.

$ENVAUTH
========

``envauth`` looks for a ``JSON`` object in the ``ENVAUTH`` environment variable.
The keys are the usernames and the value contains the password for the user.

.. code:: javascript

    {"username": "password", "anotheruser": "pass1234"}

Heroku Example
--------------

``envauth`` is especially useful if you happen to be running your application on a PAAS!

::

    $ heroku config:set ENVAUTH='{"username": "password", "anotheruser": "pass1234"}'
    Setting config vars and restarting application... done, v2

Examples
========

.. image:: http://www.authenticationtutorial.com/tutorial/basiclogin.gif
    :alt: pypi
    :align: left
    :target: https://pypi.python.org/pypi/envauth

----

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

Django
------

.. code:: python

    MIDDLEWARE_CLASSES += ('envauth.django',)

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
