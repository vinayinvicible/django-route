import pytest
from django_route.models import Destination, Router

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
