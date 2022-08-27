from functools import wraps

from .utils import route


def enable_routing(view_func):
    """
    Enables routing for the given function.
    """

    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        return route(request) or view_func(request, *args, **kwargs)

    return wrapped_view
