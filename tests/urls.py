from functools import partial

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse

from django_route.decorators import enable_routing

try:
    from django.urls import re_path
except ImportError:
    from django.conf.urls import url as re_path


@enable_routing
def test_view(request, response):
    return HttpResponse(response)


urlpatterns = [
    re_path(r'^$', partial(test_view, response='home')),
    re_path(r'^destination/$', partial(test_view, response='destination')),
    re_path(r'^admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
