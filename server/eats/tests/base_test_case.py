from django.conf import settings
from django.test import TestCase

from tmapi.models import TopicMapSystemFactory

from eats.constants import AUTHORITY_TYPE_IRI, CALENDAR_TYPE_IRI, DATE_PERIOD_TYPE_IRI, DATE_TYPE_TYPE_IRI, ENTITY_RELATIONSHIP_TYPE_TYPE_IRI, ENTITY_TYPE_TYPE_IRI, LANGUAGE_TYPE_IRI, NAME_TYPE_TYPE_IRI, SCRIPT_TYPE_IRI
from eats.models import EATSTopicMap


class BaseTestCase (TestCase):

    def setUp (self):
        # Create a topic map.
        factory = TopicMapSystemFactory.new_instance()
        self.tms = factory.new_topic_map_system()
        self.tms.create_topic_map(settings.EATS_TOPIC_MAP)
        self.tm = EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP)
        # Create an authority.
        self.authority = self.create_authority('Test')

    def create_authority (self, name):
        return self.tm.create_typed_topic(AUTHORITY_TYPE_IRI, {'name': name})

    def create_calendar (self, name):
        return self.tm.create_typed_topic(CALENDAR_TYPE_IRI, {'name': name})

    def create_date_period (self, name):
        return self.tm.create_typed_topic(DATE_PERIOD_TYPE_IRI, {'name': name})
    
    def create_date_type (self, name):
        return self.tm.create_typed_topic(DATE_TYPE_TYPE_IRI, {'name': name})

    def create_entity_relationship_type (self, name, reverse_name):
        return self.tm.create_typed_topic(
            ENTITY_RELATIONSHIP_TYPE_TYPE_IRI,
            {'name': name, 'reverse_name': reverse_name})
    
    def create_entity_type (self, name):
        return self.tm.create_typed_topic(ENTITY_TYPE_TYPE_IRI, {'name': name})
    
    def create_name_type (self, name):
        return self.tm.create_typed_topic(NAME_TYPE_TYPE_IRI, {'name': name})

    def create_language (self, name, code):
        return self.tm.create_typed_topic(LANGUAGE_TYPE_IRI,
                                          {'name': name, 'code': code})

    def create_script (self, name, code):
        return self.tm.create_typed_topic(SCRIPT_TYPE_IRI,
                                          {'name': name, 'code': code})
