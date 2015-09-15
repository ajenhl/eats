from tmapi.models import Association

from .base_manager import BaseManager
from .property_assertion import PropertyAssertion


class ExistencePropertyAssertionManager (BaseManager):

    def filter_by_entity (self, entity):
        entity_role_type = self.eats_topic_map.entity_role_type
        return self.filter(roles__type=entity_role_type,
                           roles__player=entity)

    def get_queryset (self):
        assertion_type = self.eats_topic_map.existence_assertion_type
        qs = super(ExistencePropertyAssertionManager, self).get_queryset()
        return qs.filter(type=assertion_type)


class ExistencePropertyAssertion (Association, PropertyAssertion):

    objects = ExistencePropertyAssertionManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def set_players (self, entity):
        """Sets the entity involved in this property assertion.

        :param entity: the entity
        :type entity: `Entity`

        """
        if hasattr(self, '_entity'):
            raise Exception(
                'set_players may be called only once for a property assertion')
        self.create_role(self.eats_topic_map.property_role_type,
                         self.eats_topic_map.existence)
        self.create_role(self.eats_topic_map.entity_role_type, entity)
        self._entity = entity
