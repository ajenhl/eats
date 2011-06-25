from tmapi.models import Topic

from entity_relationship_property_assertion import EntityRelationshipPropertyAssertion
from entity_type_property_assertion import EntityTypePropertyAssertion
from existence_property_assertion import ExistencePropertyAssertion
from name import Name
from name_property_assertion import NamePropertyAssertion
from note_property_assertion import NotePropertyAssertion


class Entity (Topic):

    class Meta:
        proxy = True
        app_label = 'eats'

    def create_entity_relationship_property_assertion (
        self, authority, relationship_type, domain_entity, range_entity):
        """Creates a new entity relationship property assertion
        asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :param relationship_type: the type of relationship
        :type relationship_type: `Topic`
        :param domain_entity: entity playing the domain role in the
          relationship
        :type domain_entity: `Entity`
        :param range_entity: entity playing the range role in the
          relationship
        :type range_entity: `Entity`
        :rtype: `EntityRelationshipPropertyAssertion`

        """
        if domain_entity != self and range_entity != self:
            raise Exception('An entity relationship property assertion created for an entity must include that entity as one of the related entities')
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.entity_relationship_assertion_type,
            scope=[authority], proxy=EntityRelationshipPropertyAssertion)
        assertion.set_players(domain_entity, range_entity, relationship_type)
        return assertion
        
    def create_entity_type_property_assertion (self, authority, entity_type):
        """Creates a new entity type property assertion asserted by
        `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :param entity_type: entity type
        :type entity_type: `Topic`
        :rtype: `EntityTypePropertyAssertion`

        """
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.entity_type_assertion_type, scope=[authority],
            proxy=EntityTypePropertyAssertion)
        assertion.set_players(self, entity_type)
        return assertion

    def create_existence_property_assertion (self, authority):
        """Creates a new existence property assertion asserted by
        `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :rtype: `ExistencePropertyAssertion`

        """
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.existence_assertion_type, scope=[authority],
            proxy=ExistencePropertyAssertion)
        assertion.set_players(self)
        return assertion

    def create_name_property_assertion (self, authority, name_type, language,
                                        script, display_form):
        """Creates a name property assertion asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :param name_type: name type
        :type name_type: `Topic`
        :param language: language of the name
        :type language: `Topic`
        :param script" script of the name
        :type script: `Topic`
        :param display_form: display form of the name
        :type display_form: unicode string
        :rtype: `NamePropertyAssertion`

        """
        name = self.eats_topic_map.create_topic(proxy=Name)
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.name_assertion_type, scope=[authority],
            proxy=NamePropertyAssertion)
        assertion.set_players(self, name)
        name.create(name_type, language, script, display_form)
        return assertion

    def create_note_property_assertion (self, authority, note):
        """Creates a note property assertion asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :param note: text of note
        :type note: string
        :rtype: `NotePropertyAssertion`

        """
        assertion = self.create_occurrence(
            self.eats_topic_map.note_occurrence_type, note,
            scope=[authority], proxy=NotePropertyAssertion)
        return assertion

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

    def get_eats_names (self):
        """Returns this entity's name property assertions.

        :rtype: list of `NamePropertyAssertion`s

        """
        # QAZ: This should return a QuerySet.
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.name_assertion_type)
        return [role.get_parent(proxy=NamePropertyAssertion) for role
                in entity_roles]

    def get_entity_relationships (self):
        """Returns this entity's relationships to other entities.

        :rtype: list of `EntityRelationshipPropertyAssertion`s

        """
        domain_entity_roles = self.get_roles_played(
            self.eats_topic_map.domain_entity_role_type)
        range_entity_roles = self.get_roles_played(
            self.eats_topic_map.range_entity_role_type)
        relationships = [role.get_parent(proxy=EntityRelationshipPropertyAssertion) for role in domain_entity_roles] + \
            [role.get_parent(proxy=EntityRelationshipPropertyAssertion) for role in range_entity_roles]
        return relationships

    def get_entity_type (self, assertion):
        """Returns the entity type asserted in `assertion`.

        :param assertion: entity type property assertion
        :type assertion: `Association`
        :rtype: `Topic`

        """
        role = assertion.get_roles(self.eats_topic_map.property_role_type)[0]
        return role.get_player()
    
    def get_entity_types (self):
        """Returns this entity's entity type property assertions.

        :rtype: list of `EntityTypePropertyAssertion`s

        """
        # QAZ: This should return a QuerySet.
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.entity_type_assertion_type)
        entity_types = [role.get_parent(proxy=EntityTypePropertyAssertion)
                        for role in entity_roles]
        return entity_types
    
    def get_existences (self, authority=None):
        """Returns this entity's existence property assertions.

        If `authority` is not None, returns only those existences that
        are asserted by that authority.

        :param authority: the optional authority
        :type authority: `Topic`
        :rtype: list of `Association`s

        """
        # QAZ: This should return a QuerySet.
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.existence_assertion_type)
        existences = [role.get_parent(proxy=ExistencePropertyAssertion)
                      for role in entity_roles]
        if authority is not None:
            existences = [existence for existence in existences if
                          authority in existence.get_scope()]
        return existences

    def get_notes (self):
        """Returns this entity's note property assertions.

        :rtype: `QuerySet` of `Occurrence`s

        """
        return self.get_occurrences(self.eats_topic_map.note_occurrence_type,
                                    proxy=NotePropertyAssertion)
