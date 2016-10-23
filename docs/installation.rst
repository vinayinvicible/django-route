Installation
============

Use pip to install from PyPI::

    pip install django-route

Add ``django_route`` to your settings.py file::

    INSTALLED_APPS = (
        ...
        'django_route',
        ...
    )

Run migrations using::

    python manage.py migrate django_route
