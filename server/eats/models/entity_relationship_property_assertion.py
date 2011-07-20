from django.db import transaction

from tmapi.models import Association

from eats.exceptions import EATSValidationException

from base_manager import BaseManager
from entity_relationship_type import EntityRelationshipType
from property_assertion import PropertyAssertion


class EntityRelationshipPropertyAssertionManager (BaseManager):

    def get_query_set (self):
        assertion_type = self.eats_topic_map.entity_relationship_assertion_type
        qs = super(EntityRelationshipPropertyAssertionManager,
                   self).get_query_set()
        return qs.filter(type=assertion_type)


class EntityRelationshipPropertyAssertion (Association, PropertyAssertion):

    objects = EntityRelationshipPropertyAssertionManager()
    
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
            self._entity_relationship_type = role.get_player(
                proxy=EntityRelationshipType)
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

    @transaction.commit_on_success
    def update (self, relationship_type, domain_entity,
                range_entity):
        """Updates this property assertion.

        :param relationship_type: type of the relationship
        :type relationship_type: `EntityRelationshipType`
        :param domain_entity: the domain entity
        :type domain_entity: `Entity`
        :param range_entity: the range entity
        :type range_entity: `Entity`

        """
        if domain_entity not in (self.domain_entity, self.range_entity) \
                and range_entity not in (self.domain_entity, self.range_entity):
            # QAZ: use a specific exception
            raise EATSValidationException('entity relationship update must keep at least one entity the same')
        if relationship_type != self.entity_relationship_type:
            self.authority.validate_components(
                entity_relationship_type=relationship_type)
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
        
