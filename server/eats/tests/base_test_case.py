from django.conf import settings
from django.contrib.auth.models import User
from django.test import TransactionTestCase

from tmapi.models import TopicMapSystemFactory

from eats.models import EATSTopicMap, EATSUser


class BaseTestCase (TransactionTestCase):

    def setUp (self):
        # Create a topic map.
        factory = TopicMapSystemFactory.new_instance()
        self.tms = factory.new_topic_map_system()
        self.tms.create_topic_map(settings.EATS_TOPIC_MAP)
        self.tm = EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP)
        # Create an authority.
        self.authority = self.create_authority('Test')

    def create_authority (self, name):
        return self.tm.create_authority(name)

    def create_calendar (self, name):
        return self.tm.create_calendar(name)

    def create_date_period (self, name):
        return self.tm.create_date_period(name)
    
    def create_date_type (self, name):
        return self.tm.create_date_type(name)

    def create_django_user (self, username, email, password):
        return User.objects.create_user(username, email, password)
    
    def create_entity_relationship_type (self, name, reverse_name):
        return self.tm.create_entity_relationship_type(name, reverse_name)
    
    def create_entity_type (self, name):
        return self.tm.create_entity_type(name)
    
    def create_name_type (self, name):
        return self.tm.create_name_type(name)

    def create_language (self, name, code):
        return self.tm.create_language(name, code)

    def create_script (self, name, code):
        return self.tm.create_script(name, code)

    def create_user (self, user):
        eats_user = EATSUser(user=user)
        eats_user.save()
        return eats_user
