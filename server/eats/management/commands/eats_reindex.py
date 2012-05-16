"""Django management command to regenerate the name index and cache."""

from django.core.management.base import BaseCommand

from eats.models import Name


class Command (BaseCommand):

    help = 'Regenerates the name index and cache.'

    def handle (self, *args, **options):
        for name in Name.objects.all():
            name.update_name_cache()
            name.update_name_index()
