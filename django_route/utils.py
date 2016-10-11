from __future__ import absolute_import, unicode_literals

import copy
import logging
import random
import string
from functools import reduce

from django.core.wsgi import get_wsgi_application
from django.http import HttpResponseRedirect, QueryDict
from django.template import RequestContext, Template
# noinspection PyUnresolvedReferences
from django.utils.six.moves.urllib.parse import urlparse, urlunparse

from .conf import settings
from .models import Router

try:
    from math import gcd
except ImportError:  # pragma: no cover
    from fractions import gcd

CONDITION_TEMPLATE = "{{% if {} %}}True{{% endif %}}"

logger = logging.getLogger('django_route')
logger.setLevel(logging.DEBUG)


def route(request):
    if getattr(request, 'routing_processed', False):
        return

    # Avoid checking the request twice by adding a custom attribute to
    # request. This will be relevant when both decorator and middleware
    # are used.
    request.routing_processed = True

    # Routing only the 'safe' methods.
    if request.method not in ('GET', 'HEAD', 'OPTIONS', 'TRACE'):
        return

    url_path = request.path_info
    for router in Router.objects.filter(source=url_path).iterator():
        if not router.destinations.exists():
            continue
        if should_route(condition=router.condition, request=request):
            break
    else:
        # Can be one of the following
        # 1. No router is found
        # 2. No destination for the router
        # 3. Routing condition is not satisfied
        return

    # seed will make sure that outcome will not change for a given session
    random.seed(request.session.session_key)
    destination = weighted_choice(
        router.destinations.iterator(),
        weight_func=lambda dest: dest.weight
    )
    if not destination:
        return

    destination_url = modify_url(
        old_path=request.get_full_path(),
        new_path=destination.url,
        carry_params=destination.carry_params,
        new_params=safe_format(
            destination.append_params, router_code=router.code
        ),
    )
    if router.action in router.REDIRECTS:
        return HttpResponseRedirect(
            redirect_to=destination_url, status=int(router.action)
        )

    parse = urlparse(destination_url)
    if settings.ENABLE_PROXY_ROUTING and router.action == router.PROXY:
        handler = get_wsgi_application()
        # noinspection PyProtectedMember
        # django < 1.10
        if handler._request_middleware is None:  # pragma: no cover
            handler.load_middleware()

        # FIXME: deepcopy with stream mock?
        environ = copy.copy(request.environ)
        environ['PATH_INFO'] = destination.url
        environ['QUERY_STRING'] = parse.query
        proxy_request = handler.request_class(environ=environ)
        response = handler.get_response(proxy_request)
        return response


class SafeFormatter(string.Formatter):
    def get_value(self, key, args, kwargs):
        try:
            return super(SafeFormatter, self).get_value(key, args, kwargs)
        except KeyError:
            return super(SafeFormatter, self).format('{{{0}}}', key)

safe_format = SafeFormatter().format


# noinspection PyBroadException
def should_route(condition, request):
    try:
        return bool(get_condition_result(condition=condition, request=request))
    except:
        if settings.DEBUG:  # pragma: no cover
            raise
        logger.debug('Error while rendering condition', exc_info=True)


def get_condition_result(condition, request=None):
    template = Template(CONDITION_TEMPLATE.format(condition))
    return template.render(context=RequestContext(request=request))


def modify_url(old_path, new_path='', carry_params=True, new_params=None):
    """
    Returns a new path based on the following conditions
        if new_path is not given
        old path is returned modified as per the given arguments

        if new_path if given
        new path is returned modified as per the given arguments

    :param old_path: default values are taken from this path
    :param new_path: path to be modified
    :param carry_params: Carry forwards the query params from old path
    :param new_params: Appends the given query params
    :return: url path
    """
    if not(old_path or new_path):
        return old_path

    old_url_parts = list(urlparse(old_path))
    new_url_parts = list(urlparse(new_path))
    query_params = old_url_parts[-2] if carry_params else None
    query_dict = QueryDict(query_params, mutable=True)

    # XXX QueryDict.update does not replace the key but appends the value
    for key, list_ in QueryDict(new_url_parts[-2]).lists():
        query_dict.setlist(key, list_)

    if new_params:
        # assumed to be urlencoded string
        for key, list_ in QueryDict(new_params).lists():
            query_dict.setlist(key, list_)

    new_url_parts[-2] = query_dict.urlencode()
    new_url_parts[2] = new_url_parts[2] or old_url_parts[2]
    return urlunparse(new_url_parts)


def weighted_choice(choices, weight_func):
    if not callable(weight_func):  # pragma: no cover
        raise ValueError('weight_func should be a callable')

    dictionary = {choice: weight_func(choice) for choice in choices}
    return get_random_key(dictionary=dictionary)


def get_random_key(dictionary):
    dictionary = normalize_dict_values(dictionary)
    if not dictionary:
        return None

    choices = [key for key, value in dictionary.items() for _ in range(value)]
    random.shuffle(choices)
    return random.choice(choices)


def normalize_dict_values(dictionary):
    if not dictionary:  # pragma: no cover
        return dictionary

    l_gcd = gcd_of_list(list(dictionary.values()))
    if l_gcd:
        return {key: int(value / l_gcd) for key, value in dictionary.items()}
    return {}


def gcd_of_list(l):
    if not l:  # pragma: no cover
        return

    return reduce(gcd, l)
