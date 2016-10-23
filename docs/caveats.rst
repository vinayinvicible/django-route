Caveats
=======

Proxy Routing
~~~~~~~~~~~~~

You need to enable ``proxy`` setting by explicitly setting ``ENABLE_PROXY_ROUTING = True``.

**Reason:**

    Since the values passed to wsgi.input and wsgi.errors in request environ are io or socket streams, they cannot be deepcopied.
    So, we endup passing same streams to essentially two different requests.
    Network data cannot be seeked and cannot be read outside of its content length.
    So, we have to pass the same stream to the proxy handler also.
    The issue is that we cannot read multiple times from wsgi.input.
    Either it will raise exception or gives empty data or in the worst case deadlock.

.. note::
    Proper care has been taken to prevent these issues. Still there might an issue which I might have overlooked.

    Hence the proxy feature is disabled by default.

.. warning::

    **YOU HAVE BEEN WARNED!!!**
