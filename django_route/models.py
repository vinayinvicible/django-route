from __future__ import absolute_import, unicode_literals

from django.core.validators import MinValueValidator
from django.db import models
from django.utils.translation import ugettext_lazy as _

from .conf import settings
from .validators import validate_url_path


class Destination(models.Model):
    weight = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(limit_value=1)],
        help_text=_(
            "Higher the value higher is it's preference"
        )
    )
    url = models.CharField(max_length=255, validators=[validate_url_path])
    router = models.ForeignKey(
        'Router', on_delete=models.CASCADE, related_name='destinations'
    )
    carry_params = models.BooleanField(
        default=True, help_text=_('Carry forward url params')
    )
    append_params = models.CharField(
        max_length=255, blank=True, help_text=_('Params to be appended')
    )
    is_active = models.BooleanField(
        default=True, help_text=_('Active')
    )

    class Meta(object):
        unique_together = ('router', 'url', 'append_params')

    def __str__(self):
        return '{0.weight} - {0.url}'.format(self)

PERMANENT = '301'
TEMPORARY = '302'
PROXY = 'proxy'


def get_action_choices():  # pragma: no cover
    if settings.ENABLE_PROXY_ROUTING:
        return (
            (PERMANENT, 'Permanent redirect'),
            (TEMPORARY, 'Temporary redirect'),
            (PROXY, 'Proxy to destination'),
        )
    return (
        (PERMANENT, 'Permanent redirect'),
        (TEMPORARY, 'Temporary redirect'),
    )


class Router(models.Model):
    PERMANENT = PERMANENT
    TEMPORARY = TEMPORARY
    PROXY = PROXY
    REDIRECTS = (PERMANENT, TEMPORARY)

    code = models.SlugField(
        max_length=255, unique=True,
        help_text=_(
            'Code name for the router. '
            'Can be used as variable value inside append_params '
            'using {route_code}.'
        )
    )
    source = models.CharField(
        max_length=255, validators=[validate_url_path],
        help_text=_(
            'Source path'
        )
    )
    rank = models.PositiveSmallIntegerField(
        default=1, validators=[MinValueValidator(limit_value=1)],
        help_text=_(
            "Lower the value higher is it's preference"
        )
    )
    action = models.CharField(
        max_length=20,
        choices=get_action_choices(),
        help_text=_(
            'Path to be followed from source to destination'
        )
    )
    condition = models.TextField(
        default='"*"',
        help_text=_(
            'Condition for routing decision'
        )
    )
    is_active = models.BooleanField(
        default=True, help_text=_('Active')
    )

    class Meta(object):
        ordering = ['source', 'rank']
        unique_together = ('source', 'rank')

    def __str__(self):
        return '{0.code} | {0.source} -> {0.action}'.format(self)
