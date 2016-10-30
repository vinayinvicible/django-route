.. _caveats:

Caveats
=======

Proxy Routing
~~~~~~~~~~~~~

You need to enable ``proxy`` setting by explicitly setting ``ENABLE_PROXY_ROUTING = True``.

**Reason:**

    Since the values passed to wsgi.input and wsgi.errors in request environ are io or socket streams, they cannot be deepcopied.
    So, we end up passing same streams to essentially two different requests.
    Network data cannot be seeked and cannot be read outside of its content length.
    So, we have to pass the same stream to the proxy handler also.
    The issue is that we cannot read multiple times from wsgi.input.
    Either it will raise exception or gives empty data or in the worst case deadlock.

.. note::
    Proper care has been taken to prevent these issues. Still there might an issue which I might have overlooked.

    Hence the proxy feature is disabled by default.

.. warning::

    **YOU HAVE BEEN WARNED!!!**


Randomization
~~~~~~~~~~~~~

Routing does not use any custom cookies to tie the outcome to the user. It rather relies on the session key in deriving the outcome of the destinations.

No matter how many times user visits the source path, destination will always be the same.

.. note::
    Destination for a user might change if

    * Session key changes. (Session key changes during login/logout)

    * New active destination has been added to the router or weightage of the active destinations has been changed. Since the sample space has been changed, outcome might vary.
