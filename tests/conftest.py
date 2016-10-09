import pytest

from django_routing.models import Router, Destination

pytestmark = pytest.mark.django_db


@pytest.fixture
def router():
    return Router.objects.create(
        code='router',
        source='/',
        action='301',
        condition='request.user.is_authenticated',
    )


@pytest.fixture
def destination(router):
    return Destination.objects.create(
        url='/destination/',
        router=router,
    )
