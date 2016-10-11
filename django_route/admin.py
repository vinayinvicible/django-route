from __future__ import absolute_import, unicode_literals

import sys

from django import forms
from django.contrib import admin
from django.utils import six

from .models import Destination, Router
from .utils import get_condition_result


class DestinationInline(admin.TabularInline):
    model = Destination
    extra = 0


class RouteAdminForm(forms.ModelForm):

    def clean_condition(self):
        condition = self.cleaned_data.get('condition')
        if condition:
            try:
                get_condition_result(condition=condition, request=self.request)
            except Exception as e:
                tb = sys.exc_info()[2]
                six.reraise(forms.ValidationError,
                            forms.ValidationError(e), tb)
        return condition


class RouterAdmin(admin.ModelAdmin):
    inlines = [DestinationInline]
    form = RouteAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(RouterAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form

admin.site.register(Router, RouterAdmin)
