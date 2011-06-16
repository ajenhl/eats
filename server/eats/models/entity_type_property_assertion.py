from tmapi.models import Association

from property_assertion import PropertyAssertion


class EntityTypePropertyAssertion (Association, PropertyAssertion):

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def entity_type (self):
        """Returns the entity type being asserted."""
        if not hasattr(self, '_entity_type'):
            property_role = self.get_roles(
                self.eats_topic_map.property_role_type)[0]
            self._entity_type = property_role.get_player()
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

    def update (self, authority, entity_type):
        """Update this property assertion.

        :param authority: authority making the assertion
        :type authority: `Topic`
        :param entity_type: entity type
        :type entity_type: `Topic`

        """
        super(EntityTypePropertyAssertion, self).update(authority)
        if entity_type != self.entity_type:
            property_role = self.get_roles(
                self.eats_topic_map.property_role_type)[0]
            property_role.set_player(entity_type)
            self._entity_type = entity_type