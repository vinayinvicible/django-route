import django

__version__ = '0.1.0b8'

if django.VERSION < (3, 2):
    default_app_config = 'django_route.apps.DjangoRouteConfig'
