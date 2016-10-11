# -*- coding: utf-8 -*-
# Generated by Django 1.10.2 on 2016-10-09 03:18
from __future__ import unicode_literals

import re

import django.core.validators
import django.db.models.deletion
import django_route.conf
from django.db import migrations, models


def get_action_choices():
    if django_route.conf.settings.ENABLE_PROXY_ROUTING:
        return (
            ('301', 'Permanent redirect'),
            ('302', 'Temporary redirect'),
            ('proxy', 'Proxy to destination'),
        )
    return (
        ('301', 'Permanent redirect'),
        ('302', 'Temporary redirect'),
    )


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Destination',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.PositiveSmallIntegerField(default=1, help_text="Higher the value higher is it's preference", validators=[django.core.validators.MinValueValidator(limit_value=1)])),
                ('url', models.CharField(max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^/(?:[-a-zA-Z0-9_]+/)*$', 32), "Enter a valid 'url path'. Path should start and end with '/'.", 'invalid')])),
                ('carry_params', models.BooleanField(default=True, help_text='Carry forward url params')),
                ('append_params', models.CharField(blank=True, help_text='Params to be appended', max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Router',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.SlugField(help_text='Code name for the router. Can be used as variable value inside append_params using {route_code}.', max_length=255, unique=True)),
                ('source', models.CharField(help_text='Source path', max_length=255, validators=[django.core.validators.RegexValidator(re.compile('^/(?:[-a-zA-Z0-9_]+/)*$', 32), "Enter a valid 'url path'. Path should start and end with '/'.", 'invalid')])),
                ('rank', models.PositiveSmallIntegerField(default=1, help_text="Lower the value higher is it's preference", validators=[django.core.validators.MinValueValidator(limit_value=1)])),
                ('action', models.CharField(choices=get_action_choices(), help_text='Path to be followed from source to destination', max_length=20)),
                ('condition', models.TextField(help_text='Condition for routing decision')),
            ],
            options={
                'ordering': ['source', 'rank'],
            },
        ),
        migrations.AlterUniqueTogether(
            name='router',
            unique_together=set([('source', 'rank')]),
        ),
        migrations.AddField(
            model_name='destination',
            name='router',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='destinations', to='django_route.Router'),
        ),
        migrations.AlterUniqueTogether(
            name='destination',
            unique_together=set([('url', 'append_params')]),
        ),
    ]
