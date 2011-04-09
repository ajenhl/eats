from tmapi.models import Topic


class Entity (Topic):

    class Meta:
        proxy = True

    def create_existence_property_assertion (self, authority):
        """Creates a new existence property assertion asserted by
        `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`

        """
        assertion = self.eats_topic_map.topic_map.create_association(
            self.eats_topic_map.existence_assertion_type, scope=[authority])
        assertion.create_role(self.property_role_type, self.existence)

    @property
    def eats_topic_map (self):
        return self._eats_topic_map

    @eats_topic_map.setter
    def eats_topic_map (self, value):
        self._eats_topic_map = value
        
    def get_entity_types (self):
        """Returns this entity's entity type property assertions.

        :rtype: list of `Association`s

        """
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.entity_type_assertion_type)
        entity_types = [role.get_parent() for role in entity_roles]
        return entity_types
    
    def get_existences (self, authority=None):
        """Returns this entity's existence property assertions.

        If `authority` is not None, returns only those existences that
        are asserted by that authority.

        :param authority: the optional authority
        :type authority: `Topic`
        :rtype: list of `Association`s

        """
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.existence_assertion_type)
        existences = [role.get_parent() for role in entity_roles]
        if authority is not None:
            existences = [existence for existence in existences if
                          authority in existence.get_scope()]
        return existences
