from __future__ import absolute_import, unicode_literals

import re

from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from .conf import settings

url_path_re = re.compile(
    r'^/(?:[-a-zA-Z0-9_]+/{})*$'.format(r'' if settings.APPEND_SLASH else r'?')
)

validate_url_path = RegexValidator(
    url_path_re,
    _("Enter a valid 'url path'. Path should start {}with '/'.".format(
        'and end ' if settings.APPEND_SLASH else ''
    )),
    'invalid'
)
