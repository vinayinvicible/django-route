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
    If you still want to enable proxy routing, atleast make sure that you are not doing any of the following

        * Proxy handler routes through middlewares instead of bypassing directly to the view.
          So, you should not be using body, POST or FILES inside middlewares.
        * Wrapping view inside another view/decorator which plays with the data stream

.. warning::

    **YOU HAVE BEEN WARNED!!!**
