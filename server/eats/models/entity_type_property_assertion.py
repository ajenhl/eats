from tmapi.models import Association

from .base_manager import BaseManager
from .entity_type import EntityType
from .property_assertion import PropertyAssertion


class EntityTypePropertyAssertionManager (BaseManager):

    def filter_by_authority_entity_type (self, authority, entity_type):
        return self.filter(scope=authority).filter(
            roles__type=self.eats_topic_map.property_role_type,
            roles__player=entity_type)

    def filter_by_entity (self, entity):
        return self.filter(roles__type=self.eats_topic_map.entity_role_type,
                           roles__player=entity)

    def get_queryset (self):
        assertion_type = self.eats_topic_map.entity_type_assertion_type
        qs = super(EntityTypePropertyAssertionManager, self).get_queryset()
        return qs.filter(type=assertion_type)


class EntityTypePropertyAssertion (Association, PropertyAssertion):

    objects = EntityTypePropertyAssertionManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def entity_type (self):
        """Returns the entity type being asserted.

        :rtype: `EntityType`

        """
        if not hasattr(self, '_entity_type'):
            property_role = self.get_roles(
                self.eats_topic_map.property_role_type)[0]
            self._entity_type = property_role.get_player(proxy=EntityType)
        return self._entity_type

    def set_players (self, entity, entity_type):
        """Sets the entity and entity type involved in this property
        assertion.

        :param entity: the entity
        :type entity: `Entity`
        :param entity_type: the entity type
        :type entity_type: `Topic`

        """
        if hasattr(self, '_entity') or hasattr(self, '_entity_type'):
            raise Exception(
                'set_players may be called only once for a property assertion')
        self.create_role(self.eats_topic_map.property_role_type, entity_type)
        self._entity_type = entity_type
        self.create_role(self.eats_topic_map.entity_role_type, entity)
        self._entity = entity

    def update (self, entity_type):
        """Updates this property assertion.

        :param entity_type: entity type
        :type entity_type: `Topic`

        """
        if entity_type != self.entity_type:
            self.authority.validate_components(entity_type=entity_type)
            property_role = self.get_roles(
                self.eats_topic_map.property_role_type)[0]
            property_role.set_player(entity_type)
            self._entity_type = entity_type
