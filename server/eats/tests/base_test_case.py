from django.apps import apps
from django.conf import settings
from django.contrib.auth.models import User

from tmapi.models import TopicMapSystemFactory

from eats.models import EATSTopicMap, EATSUser


class BaseTestCase (object):

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

    def create_language (self, name, code):
        return self.tm.create_language(name, code)

    def create_name_part_type (self, name):
        return self.tm.create_name_part_type(name)

    def create_name_type (self, name):
        return self.tm.create_name_type(name)

    def create_script (self, name, code, separator):
        return self.tm.create_script(name, code, separator)

    def create_topic_map (self):
        factory = TopicMapSystemFactory.new_instance()
        tms = factory.new_topic_map_system()
        tms.create_topic_map(settings.EATS_TOPIC_MAP)
        return EATSTopicMap.objects.get(iri=settings.EATS_TOPIC_MAP)

    def create_user (self, user):
        eats_user = EATSUser(user=user)
        eats_user.save()
        return eats_user

    def get_managers (self):
        if not hasattr(self, '_managers'):
            self._managers = []
            eats_app = apps.get_app_config('eats')
            for model in list(eats_app.models.values()):
                manager = model.objects
                if hasattr(manager, '_eats_topic_map'):
                    self._managers.append(manager)
        return self._managers

    def reset_managers (self):
        """Resets the managers for the models used in the test.

        This is necesary to avoid massive test failures when using the
        PostgreSQL backend, since the manager caches an EATSTopicMap
        that is then removed and replaced.

        """
        for manager in self.get_managers():
            delattr(manager, '_eats_topic_map')
