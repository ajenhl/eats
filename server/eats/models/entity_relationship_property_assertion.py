from django.db import transaction
from django.db.models import Q

from tmapi.models import Association

from eats.exceptions import EATSValidationException

from .base_manager import BaseManager
from .entity_relationship_cache import EntityRelationshipCache
from .entity_relationship_type import EntityRelationshipType
from .property_assertion import PropertyAssertion


class EntityRelationshipPropertyAssertionManager (BaseManager):

    def filter_by_authority_entity_relationship_type (self, authority,
                                                      entity_relationship_type):
        return self.filter(scope=authority).filter(
            roles__type=self.eats_topic_map.entity_relationship_type_role_type,
            roles__player=entity_relationship_type)

    def filter_by_entity (self, entity):
        return self.filter(Q(cached_relationship__domain_entity=entity) |
                           Q(cached_relationship__range_entity=entity))

    def get_queryset (self):
        assertion_type = self.eats_topic_map.entity_relationship_assertion_type
        qs = super(EntityRelationshipPropertyAssertionManager,
                   self).get_queryset()
        return qs.filter(type=assertion_type)


class EntityRelationshipPropertyAssertion (Association, PropertyAssertion):

    objects = EntityRelationshipPropertyAssertionManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def _add_relationship_cache(self, relationship_type, domain_entity,
                                range_entity):
        """Adds this relationship to the relationships cache."""
        forward_name = relationship_type.get_admin_forward_name()
        reverse_name = relationship_type.get_admin_reverse_name()
        cached_relationship = EntityRelationshipCache(
            entity_relationship=self, authority=self.authority,
            domain_entity=domain_entity,
            range_entity=range_entity,
            relationship_type=relationship_type,
            forward_relationship_name=forward_name,
            reverse_relationship_name=reverse_name)
        cached_relationship.save()
        self._cached_erpa = cached_relationship

    @property
    def authority (self):
        """Returns the authority of this property assertion.

        :rtype: `Topic`

        """
        try:
            authority = self._cached_relationship.authority
        except EntityRelationshipCache.DoesNotExist:
            authority = super(EntityRelationshipPropertyAssertion, self).authority
        return authority

    @property
    def _cached_relationship (self):
        if not hasattr(self, '_cached_erpa'):
            self._cached_erpa = self.cached_relationship
        return self._cached_erpa

    def _delete_relationship_cache(self):
        """Deletes the cache for this relationship."""
        # The cached object may not have been created yet.
        try:
            self._cached_relationship.delete()
        except EntityRelationshipCache.DoesNotExist:
            pass

    @property
    def domain_entity (self):
        """Returns the domain entity in this asserted relationship."""
        try:
            domain_entity = self._cached_relationship.domain_entity
        except EntityRelationshipCache.DoesNotExist:
            from .entity import Entity
            domain_role = self.get_roles(
                self.eats_topic_map.domain_entity_role_type)[0]
            domain_entity = domain_role.get_player(proxy=Entity)
        return domain_entity

    @property
    def entity_relationship_type (self):
        """Returns the entity relationship type for this asserted
        relationship."""
        try:
            entity_relationship_type = self._cached_relationship.relationship_type
        except EntityRelationshipCache.DoesNotExist:
            role = self.get_roles(
                self.eats_topic_map.entity_relationship_type_role_type)[0]
            entity_relationship_type = role.get_player(
                proxy=EntityRelationshipType)
        return entity_relationship_type

    @property
    def range_entity (self):
        """Returns the range entity in this asserted relationship."""
        try:
            range_entity = self._cached_relationship.range_entity
        except EntityRelationshipCache.DoesNotExist:
            from .entity import Entity
            range_role = self.get_roles(
                self.eats_topic_map.range_entity_role_type)[0]
            range_entity = range_role.get_player(proxy=Entity)
        return range_entity

    def get_relationship_type_forward_name(self):
        """Returns the forward name for this asserted relationship."""
        return self._cached_relationship.forward_relationship_name

    def get_relationship_type_reverse_name(self):
        """Returns the reverse name for this asserted relationship."""
        return self._cached_relationship.reverse_relationship_name

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
        self.create_role(self.eats_topic_map.range_entity_role_type,
                         range_entity)
        self.create_role(self.eats_topic_map.entity_relationship_type_role_type,
                         relationship_type)
        self.update_relationship_cache(relationship_type, domain_entity,
                                       range_entity)

    def update_relationship_cache(self, relationship_type, domain_entity,
                                  range_entity):
       """Updates the relationship cache for this relationship."""
       self._delete_relationship_cache()
       self._add_relationship_cache(relationship_type, domain_entity,
                                    range_entity)

    @transaction.atomic
    def update (self, relationship_type, domain_entity,
                range_entity, certainty):
        """Updates this property assertion.

        :param relationship_type: type of the relationship
        :type relationship_type: `EntityRelationshipType`
        :param domain_entity: the domain entity
        :type domain_entity: `Entity`
        :param range_entity: the range entity
        :type range_entity: `Entity`
        :param certainty: the certainty
        :type certainty: `Topic`

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
        if domain_entity != self.domain_entity:
            domain_role = self.get_roles(
                self.eats_topic_map.domain_entity_role_type)[0]
            domain_role.set_player(domain_entity)
        if range_entity != self.range_entity:
            range_role = self.get_roles(
                self.eats_topic_map.range_entity_role_type)[0]
            range_role.set_player(range_entity)
        self.certainty = certainty
        self.update_relationship_cache(relationship_type, domain_entity,
                                       range_entity)
