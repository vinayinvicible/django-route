from __future__ import absolute_import, unicode_literals

import pytest
from django.db import connection
from django.http import QueryDict
from django.test import override_settings
from django.test.utils import CaptureQueriesContext
from django.utils.crypto import constant_time_compare
# noinspection PyUnresolvedReferences
from django.utils.six.moves.urllib.parse import urlparse
from django_route.utils import modify_url

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize(
    ('old_url', 'new_url', 'carry_params', 'new_params', 'url'), [
        ('', '', True, '', ''),
        ('', '', False, '', ''),
        ('/', '', True, '', '/'),
        ('/', '/', True, '', '/'),
        ('', '', True, 'old=param', ''),
        ('', '', False, 'old=param', ''),
        ('/', '', True, 'old=param', '/?old=param'),
        ('/old/path', '/new', True, '', '/new'),
        ('/old/path?asd=asd', '/new', True, '', '/new?asd=asd'),
        ('/old/path?asd=asd', '/new', False, '', '/new'),
        ('/old/path?asd=asd', '/new', True, 'asd=new&new=param', '/new?asd=new&new=param'),
        ('/old/path?asd=asd', '/new', False, 'asd=new&new=param', '/new?asd=new&new=param'),
        ('/old/path?asd=asd', '/new', True, 'new=param', '/new?asd=asd&new=param'),
        ('/old/path?asd=asd', '/new', False, 'new=param', '/new?new=param'),
        ('/old/path', '/new?old=param', True, '', '/new?old=param'),
        ('/old/path?asd=asd', '/new?old=param', True, '', '/new?asd=asd&old=param'),
        ('/old/path?asd=asd', '/new?old=param', False, '', '/new?old=param'),
        ('/old/path?asd=asd', '/new?old=param', True, 'asd=new&new=param', '/new?asd=new&new=param&old=param'),
        ('/old/path?asd=asd', '/new?old=param', False, 'asd=new&new=param', '/new?asd=new&new=param&old=param'),
        ('/old/path?asd=asd', '/new?old=param', True, 'new=param', '/new?asd=asd&new=param&old=param'),
        ('/old/path?asd=asd', '/new?old=param', False, 'new=param', '/new?new=param&old=param'),
    ]
)
def test_modify_url(old_url, new_url, carry_params, new_params, url):
    assert_url_equal(url, modify_url(
        old_path=old_url,
        new_path=new_url,
        carry_params=carry_params,
        new_params=new_params
    ))


def assert_url_equal(url1, url2):
    url1_parts = urlparse(url1)
    url2_parts = urlparse(url2)
    assert url1_parts.scheme == url2_parts.scheme
    assert url1_parts.netloc == url2_parts.netloc
    assert url1_parts.path == url2_parts.path
    assert url1_parts.params == url2_parts.params
    assert QueryDict(url1_parts.query) == QueryDict(url2_parts.query)
    assert url1_parts.fragment == url2_parts.fragment


def assert_string_equal(str1, str2):
    assert constant_time_compare(str1, str2)


def test_empty_router(client, admin_client, router):

    response = client.get(router.source, follow=False)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = client.get(router.source, follow=True)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = admin_client.get(router.source, follow=False)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = admin_client.get(router.source, follow=True)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')


def test_empty_wightage(client, admin_client, router, destination):
    destination.weight = 0
    destination.save()

    response = client.get(router.source, follow=False)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = client.get(router.source, follow=True)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = admin_client.get(router.source, follow=False)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = admin_client.get(router.source, follow=True)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')


def test_redirect_router(client, admin_client, router, destination):
    router.action = '301'
    router.save()

    response = client.get(router.source, follow=False)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = client.get(router.source, follow=True)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = admin_client.get(router.source, follow=False)
    assert response.status_code == 301
    assert_string_equal(response.content, '')

    response = admin_client.get(router.source, follow=True)
    assert response.status_code == 200
    assert_string_equal(response.content, 'destination')


def test_proxy_router_disabled(client, admin_client, router, destination):
    with override_settings(ENABLE_PROXY_ROUTING=False):
        router.action = 'proxy'
        router.save()

        response = client.get(router.source)
        assert response.status_code == 200
        assert_string_equal(response.content, 'home')

        response = admin_client.get(router.source)
        assert response.status_code == 200
        assert_string_equal(response.content, 'home')


def test_proxy_router_enabled(client, admin_client, router, destination):
    with override_settings(ENABLE_PROXY_ROUTING=True):
        router.action = 'proxy'
        router.save()

        response = client.get(router.source)
        assert response.status_code == 200
        assert_string_equal(response.content, 'home')

        response = admin_client.get(router.source)
        assert response.status_code == 200
        assert_string_equal(response.content, 'destination')


def test_unsafe_method(admin_client, router, destination):
    router.action = '301'
    router.save()

    response = admin_client.post(router.source, follow=False)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')


def test_invalid_action_router(client, admin_client, router, destination):
    router.action = 'invalid'
    router.save()

    response = client.get(router.source)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')

    response = admin_client.get(router.source)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')


def test_invalid_condition_router(client, router, destination):
    router.action = 'invalid'
    router.condition = '{}'
    router.save()

    response = client.get(router.source)
    assert response.status_code == 200
    assert_string_equal(response.content, 'home')


def test_router_params(admin_client, router, destination):
    router.action = '301'
    router.save()

    destination.append_params = 'new=params'
    destination.carry_params = True
    destination.save()
    response = admin_client.get(router.source, follow=True, data={'old': 'params', 'new': 'old_params'})
    assert QueryDict(response.request['QUERY_STRING']) == QueryDict('new=params&old=params')

    destination.append_params = 'new=params'
    destination.carry_params = False
    destination.save()
    response = admin_client.get(router.source, follow=True, data={'old': 'params', 'new': 'old_params'})
    assert QueryDict(response.request['QUERY_STRING']) == QueryDict('new=params')

    destination.append_params = 'new=params&router_code={router_code}'
    destination.carry_params = False
    destination.save()
    router.code = 'code'
    router.save()

    response = admin_client.get(router.source, follow=True, data={'old': 'params', 'new': 'old_params'})
    assert QueryDict(response.request['QUERY_STRING']) == QueryDict('new=params&router_code=code')

    destination.append_params = 'new=params&router_code={router_code}&missing={param}'
    destination.carry_params = False
    destination.save()

    response = admin_client.get(router.source, follow=True, data={'old': 'params', 'new': 'old_params'})
    assert QueryDict(response.request['QUERY_STRING']) == QueryDict('new=params&missing={param}&router_code=code')


# This is just to test for infinite recursion
def test_self_reference(router, destination, admin_client):
    destination.url = '/'
    destination.save()

    admin_client.get('/', follow=True)

    destination.append_params = 'key=value'
    destination.carry_params = True
    destination.save()

    admin_client.get('/?v=1', follow=True)


def test_manual_tampering(router, destination, admin_client):
    destination.url = '/'
    destination.append_params = 'v=1'
    destination.save()

    destination.pk = None
    destination.append_params = 'v=2'
    destination.save()

    query_str_1 = admin_client.get('/', follow=True).request['QUERY_STRING']
    query_str_2 = admin_client.get('/?v=1', follow=True).request['QUERY_STRING']
    query_str_3 = admin_client.get('/?v=2', follow=True).request['QUERY_STRING']
    query_str_4 = admin_client.get('/?v=3', follow=True).request['QUERY_STRING']

    assert QueryDict(query_str_1) == QueryDict(query_str_2) == QueryDict(query_str_3) == QueryDict(query_str_4)


def test_routing_disabled(admin_client, router, destination):
    with override_settings(ROUTING_ENABLED=False):
        response = admin_client.get(router.source, follow=True)
        assert response.status_code == 200
        assert_string_equal(response.content, 'home')


def test_caching_enabled(admin_client, router, destination):
    # Only sqlite3 logs a begin query within transaction
    atomic_queries = 1 if connection.vendor == 'sqlite' else 0

    with override_settings(ROUTING_CACHE=True):
        with CaptureQueriesContext(connection=connection) as c:
            response = admin_client.get(router.source, follow=True)
            assert response.status_code == 200
            assert_string_equal(response.content, 'destination')
            first = len(c)
            assert first - atomic_queries == 5
            response = admin_client.get(router.source, follow=True)
            assert response.status_code == 200
            assert_string_equal(response.content, 'destination')
            # Should only query for user and session because of condition
            assert len(c) - first - atomic_queries == 2

        router.delete()

        with CaptureQueriesContext(connection=connection) as c:
            response = admin_client.get(router.source, follow=True)
            assert response.status_code == 200
            assert_string_equal(response.content, 'home')
            # Only the router query
            assert len(c) == 1


def test_stupidity_in_templates(admin_client, admin_user, router, destination):
    """
    Nobody would willingly set alters_data to False.
    But if the model method is overridden in subclasses
    alters_data needs to be set again.
    """
    router.condition = 'request.user.delete'
    router.save()
    admin_client.get(router.source, follow=True)
    admin_user.refresh_from_db()

    # setting admin_user.delete.alters_data throws errors.
    admin_user.delete.__dict__['alters_data'] = False
    admin_client.get(router.source, follow=True)
    admin_user.refresh_from_db()


def test_self_reference_edge_case(router, destination, admin_client):
    destination.url = '/'
    destination.append_params = 'key=value'
    destination.carry_params = True
    destination.save()

    query_str = admin_client.get('/?random=param', follow=True).request['QUERY_STRING']

    assert QueryDict(query_str) == QueryDict('random=param&key=value')
