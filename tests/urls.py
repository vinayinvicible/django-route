from functools import partial

from django.conf.urls import url
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.http import HttpResponse
from django_route.decorators import enable_routing


@enable_routing
def test_view(request, response):
    return HttpResponse(response)

urlpatterns = [
    url(r'^$', partial(test_view, response='home')),
    url(r'^destination/$', partial(test_view, response='destination')),
    url(r'^admin/', admin.site.urls),
]
urlpatterns += staticfiles_urlpatterns()
