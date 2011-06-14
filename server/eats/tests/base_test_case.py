from django.conf import settings
from django.test import TestCase

from tmapi.models import TopicMapSystemFactory

from eats.constants import AUTHORITY_TYPE_IRI, ENTITY_TYPE_TYPE_IRI, LANGUAGE_TYPE_IRI, NAME_TYPE_TYPE_IRI, SCRIPT_TYPE_IRI
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

    def create_authority (self, authority_name):
        return self.tm.create_typed_topic(AUTHORITY_TYPE_IRI,
                                          {'name': authority_name})

    def create_entity_type (self, entity_type_name):
        return self.tm.create_typed_topic(ENTITY_TYPE_TYPE_IRI,
                                          {'name': entity_type_name})
    
    def create_name_type (self, name_type_name):
        return self.tm.create_typed_topic(NAME_TYPE_TYPE_IRI,
                                          {'name': name_type_name})

    def create_language (self, language_name, language_code):
        return self.tm.create_typed_topic(
            LANGUAGE_TYPE_IRI, {'name': language_name, 'code': language_code})

    def create_script (self, script_name, script_code):
        return self.tm.create_typed_topic(
            SCRIPT_TYPE_IRI, {'name': script_name, 'code': script_code})
