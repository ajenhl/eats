from django.conf import settings
from django.core.urlresolvers import reverse
from django.test import TestCase

from tmapi.models import TopicMapSystemFactory

from eats.constants import AUTHORITY_TYPE_IRI
from eats.models import EATSTopicMap


class EntityChangeViewTestCase (TestCase):

    def setUp (self):
        # Create a topic map.
        factory = TopicMapSystemFactory.new_instance()
        self.tms = factory.new_topic_map_system()
        self.tms.create_topic_map(settings.EATS_TOPIC_MAP)
        self.tm = EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP)
        # Create an authority.
        self.authority = self.create_authority('Test')

    def create_authority (self, authority_name):
        return self.tm.create_typed_topic(AUTHORITY_TYPE_IRI,
                                          {'name': authority_name})

    def test_non_existent_entity (self):
        # Use the authority topic as an example of a non-existent
        # entity. Immediately after setUp it will not be marked as an
        # entity.
        response = self.client.get(reverse(
                'entity-change', kwargs={'entity_id': self.authority.get_id()}))
        self.assertEqual(response.status_code, 404,
                         'Expected a 404 HTTP response code for a non-existent entity')
    
    def test_empty_entity (self):
        entity = self.tm.create_entity(self.authority)
        existence = entity.get_existences()[0]
        response = self.client.get(reverse(
                'entity-change', kwargs={'entity_id': entity.get_id()}))
        self.assertEqual(response.status_code, 200)
        # A newly created entity will have one existence property
        # assertion, and no other property assertions.
        existence_formset = response.context['existence_formset']
        self.assertEqual(existence_formset.initial_form_count(), 1,
                         'Expected one pre-filled existence form')
        existence_data = existence_formset.initial_forms[0].initial
        self.assertEqual(existence_data['assertion'], existence.get_id())
        self.assertEqual(existence_data['authority'],
                         entity.get_authority(existence).get_id())
        for formset in ('entity_type_formset', 'entity_relationship_formset',
                        'name_formset', 'note_formset'):
            self.assertEqual(response.context[formset].initial_form_count(), 0,
                             'Expected no %ss' % formset)

