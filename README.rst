.. image:: http://www.authenticationtutorial.com/tutorial/basiclogin.gif
    :alt: pypi
    :align: left
    :target: https://pypi.python.org/pypi/envauth

$ENVAUTH
========

.. code:: javascript

    {'username': 'password', 'anotheruser': 'pass1234'}

Examples
--------

Flask
*****

.. code:: python

    from envauth.flask import requires_auth

    @app.route('/secret-page')
    @requires_auth
    def secret_page():
        return render_template('secret_page.html')

Bottle
******

.. code:: python

    from envauth.bottle import requires_auth

    @app.route('/secret-page')
    @requires_auth
    def secret_page():
        return template('secret_page.html')

WSGI
****

.. code:: python

    import envauth

    application = envauth.wsgi(application)

Installation
------------

Install *envauth* with pip:

::

    $ pip install envauth