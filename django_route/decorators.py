from __future__ import absolute_import, unicode_literals

from functools import wraps

from django.utils.decorators import available_attrs

from .utils import route


def enable_routing(view_func):
    """
    Enables routing for the given function.
    """
    @wraps(view_func, assigned=available_attrs(view_func))
    def wrapped_view(request, *args, **kwargs):
        return route(request) or view_func(request, *args, **kwargs)
    return wrapped_view
