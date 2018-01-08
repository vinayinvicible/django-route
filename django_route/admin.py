from __future__ import absolute_import, unicode_literals

import sys

from django import forms
from django.contrib import admin
from django.http import QueryDict
from django.utils import six

from .models import Destination, Router
from .utils import get_condition_result


class DestinationForm(forms.ModelForm):

    def clean_append_params(self):
        params = self.cleaned_data.get('append_params')
        if params:
            try:
                params = QueryDict(params).urlencode()
            except Exception as e:
                tb = sys.exc_info()[2]
                six.reraise(forms.ValidationError, forms.ValidationError(e), tb)
        return params


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
                six.reraise(forms.ValidationError, forms.ValidationError(e), tb)
        return condition


@admin.register(Router)
class RouterAdmin(admin.ModelAdmin):
    inlines = [DestinationInline]
    form = RouteAdminForm

    def get_form(self, request, obj=None, **kwargs):
        form = super(RouterAdmin, self).get_form(request, obj, **kwargs)
        form.request = request
        return form
