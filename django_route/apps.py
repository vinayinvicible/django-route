from __future__ import absolute_import, unicode_literals

from django.apps import AppConfig


class DjangoRouteConfig(AppConfig):
    name = 'django_route'
    verbose_name = 'Django Route'

    def ready(self):
        from .signals import handlers  # noqa
