from __future__ import absolute_import, unicode_literals

from django.db import transaction
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from ..cache import clear_destination_cache, clear_router_cache
from ..models import Destination, Router


# noinspection PyUnusedLocal
@receiver(post_save, sender=Destination)
def destination_post_save(instance, **kwargs):
    if hasattr(transaction, 'on_commit'):
        transaction.on_commit(clear_destination_cache)
    else:
        clear_destination_cache()


# noinspection PyUnusedLocal
@receiver(post_delete, sender=Destination)
def destination_post_delete(instance, **kwargs):
    if hasattr(transaction, 'on_commit'):
        transaction.on_commit(clear_destination_cache)
    else:
        clear_destination_cache()


# noinspection PyUnusedLocal
@receiver(post_save, sender=Router)
def router_post_save(instance, **kwargs):
    if hasattr(transaction, 'on_commit'):
        transaction.on_commit(clear_router_cache)
    else:
        clear_router_cache()


# noinspection PyUnusedLocal
@receiver(post_delete, sender=Router)
def router_deleted(instance, **kwargs):
    if hasattr(transaction, 'on_commit'):
        transaction.on_commit(clear_router_cache)
    else:
        clear_router_cache()
