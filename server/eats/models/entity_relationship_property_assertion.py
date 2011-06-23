from tmapi.models import Association

from property_assertion import PropertyAssertion


class EntityRelationshipPropertyAssertion (Association, PropertyAssertion):

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def domain_entity (self):
        """Returns the domain entity in this asserted relationship."""
        if not hasattr(self, '_domain_entity'):
            from entity import Entity
            domain_role = self.get_roles(
                self.eats_topic_map.domain_entity_role_type)[0]
            self._domain_entity = domain_role.get_player(proxy=Entity)
        return self._domain_entity

    @property
    def entity_relationship_type (self):
        """Returns the entity relationship type for this asserted
        relationship."""
        if not hasattr(self, '_entity_relationship_type'):
            role = self.get_roles(
                self.eats_topic_map.entity_relationship_type_role_type)[0]
            self._entity_relationship_type = role.get_player()
        return self._entity_relationship_type
    
    @property
    def range_entity (self):
        """Returns the range entity in this asserted relationship."""
        if not hasattr(self, '_range_entity'):
            from entity import Entity
            range_role = self.get_roles(
                self.eats_topic_map.range_entity_role_type)[0]
            self._range_entity = range_role.get_player(proxy=Entity)
        return self._range_entity
        
    def set_players (self, domain_entity, range_entity, relationship_type):
        """Sets the domain and range entities involved in this relationship.

        :param domain_entity: the domain entity
        :type domain_entity: `Entity`
        :param range_entity: the range entity
        :type range_entity: `Entity`
        :param relationship_type: the type of entity relationship
        :type relationship_type: `Topic`

        """
        self.create_role(self.eats_topic_map.domain_entity_role_type,
                         domain_entity)
        self._domain_entity = domain_entity
        self.create_role(self.eats_topic_map.range_entity_role_type,
                         range_entity)
        self._range_entity = range_entity
        self.create_role(self.eats_topic_map.entity_relationship_type_role_type,
                         relationship_type)

    def update (self, authority, relationship_type, domain_entity,
                range_entity):
        """Updates this property assertion.

        :param authority: authority making the assertion
        :type authority: `Topic`
        :param relationship_type: type of the relationship
        :type relationship_type: `Topic`
        :param domain_entity: the domain entity
        :type domain_entity: `Entity`
        :param range_entity: the range entity
        :type range_entity: `Entity`

        """
        super(EntityRelationshipPropertyAssertion, self).update(authority)
        if domain_entity not in (self.domain_entity, self.range_entity) \
                and range_entity not in (self.domain_entity, self.range_entity):
            # QAZ: use a specific exception
            raise Exception('entity relationship update must keep at least one entity the same')
        if relationship_type != self.entity_relationship_type:
            role = self.get_roles(
                self.eats_topic_map.entity_relationship_type_role_type)[0]
            role.set_player(relationship_type)
            self._entity_relationship_type = relationship_type
        if domain_entity != self.domain_entity:
            domain_role = self.get_roles(
                self.eats_topic_map.domain_entity_role_type)[0]
            domain_role.set_player(domain_entity)
            self._domain_entity = domain_entity
        if range_entity != self.range_entity:
            range_role = self.get_roles(
                self.eats_topic_map.range_entity_role_type)[0]
            range_role.set_player(range_entity)
            self._range_entity = range_entity
        
