import pytest
from django_route.models import Destination, Router

pytestmark = pytest.mark.django_db


# noinspection PyUnusedLocal
@pytest.fixture
def router(transactional_db):
    return Router.objects.create(
        code='router',
        source='/',
        action='301',
        condition='request.user.is_authenticated',
    )


# noinspection PyUnusedLocal,PyShadowingNames
@pytest.fixture
def destination(router, transactional_db):
    return Destination.objects.create(
        url='/destination/',
        router=router,
    )
