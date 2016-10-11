from __future__ import absolute_import, unicode_literals

from django.conf import settings as django_settings

from . import global_settings

__all__ = ['settings']


class CustomSettings(object):

    def __getattr__(self, item):
        try:
            return getattr(django_settings, item)
        except AttributeError:
            if item.isupper() and hasattr(global_settings, item):
                return getattr(global_settings, item)
            raise

settings = CustomSettings()

# The CustomSettings class is no more needed, so remove it from the namespace.
del CustomSettings
