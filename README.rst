ENVAUTH
=======


.. image:: http://www.freepasswordmanager.com/wp-content/uploads/2013/08/strong-passwords.jpg
    :alt: pypi
    :align: center
    :target: https://pypi.python.org/pypi/envauth

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