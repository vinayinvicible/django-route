Getting Started
===============

You can define your routing configuration from the django admin panel.
For the requests to actually route you need the enable routing.

There are two ways in which you can enable routing.

    * Decorator
    * Middleware

Decorator
---------

If you want to limit routing to specific views, add the ``django_routing.decorators.enable_routing`` decorator to those views.::

    from django_routing.decorators import enable_routing

    @enable_routing
    def view(request, *args, **kwargs):
        ...


Middleware
----------

If you wish to enable routing for all the urls, add ``RoutingRequestMiddleware`` to your middleware settings.::

    MIDDLEWARE_CLASSES = [
        ...
        'django_routing.middlewares.RoutingRequestMiddleware',
        ...
    ]

