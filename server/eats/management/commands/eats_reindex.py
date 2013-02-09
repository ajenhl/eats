"""Django management command to regenerate the name index and cache."""

from django.core.management.base import BaseCommand

from eats.models import EntityRelationshipPropertyAssertion, Name


class Command (BaseCommand):

    help = 'Regenerates the name index and cache, and the entity relationship cache.'

    def handle (self, *args, **options):
        print('Generating name index and cache.')
        for name in Name.objects.all().iterator():
            name.update_name_cache()
            name.update_name_index()

        print('Generating entity relationship cache.')
        for a in EntityRelationshipPropertyAssertion.objects.all().iterator():
            a.update_relationship_cache(
                a.entity_relationship_type, a.domain_entity, a.range_entity,
                a.certainty)
