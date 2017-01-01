from __future__ import absolute_import, unicode_literals

from django.utils.lru_cache import lru_cache

from .conf import settings
from .models import Router


@lru_cache()
def _get_routers_from_cache(source):
    return _get_routers(source=source)


def _get_routers(source):
    return Router.objects.filter(source=source, is_active=True)


def get_routers(source):
    if settings.ROUTING_CACHE:
        return _get_routers_from_cache(source=source)
    return _get_routers(source=source)


@lru_cache()
def _get_destinations_from_cache(router):
    return _get_destinations(router=router)


def _get_destinations(router):
    return router.destinations.filter(is_active=True)


def get_destinations(router):
    if settings.ROUTING_CACHE:
        return _get_destinations_from_cache(router=router)
    return _get_destinations(router=router)


def clear_router_cache():
    if settings.ROUTING_CACHE:
        _get_routers_from_cache.cache_clear()


def clear_destination_cache():
    if settings.ROUTING_CACHE:
        _get_destinations_from_cache.cache_clear()
