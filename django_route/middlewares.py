from __future__ import absolute_import, unicode_literals

from .utils import route

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # pragma: no cover
    class MiddlewareMixin(object):
        pass


# noinspection PyMethodMayBeStatic
class RoutingRequestMiddleware(MiddlewareMixin):

    def process_request(self, request):
        return route(request=request)
