from django.core.urlresolvers import NoReverseMatch

from tmapi.models import Association, Topic

from eats.exceptions import EATSMergedIdentifierException, \
    EATSValidationException

from .base_manager import BaseManager
from .date import Date
from .entity_relationship_property_assertion import EntityRelationshipPropertyAssertion
from .entity_type_property_assertion import EntityTypePropertyAssertion
from .existence_property_assertion import ExistencePropertyAssertion
from .name import Name
from .name_property_assertion import NamePropertyAssertion
from .note_property_assertion import NotePropertyAssertion
from .subject_identifier_property_assertion import SubjectIdentifierPropertyAssertion


class EntityManager (BaseManager):

    def filter_by_duplicate_subject_identifiers (self, entity,
                                                 subject_indicator, authority):
        """Returns entities, excluding `entity`, that have a subject
        identifier property assertion matching `subject_identifier`.

        If `authority` is not None, only those entities that have
        `subject_identifier` asserted by `authority` are returned.

        :param entity: entity to exclude from the results
        :type entity: `Entity`
        :param subject_identifier: the subject identifier to find
        :type subject_identifier: `str`
        :param authority: authority to restrict search
        :type authority: `Authority` or None
        :rtype: `QuerySet` of `Entity`s

        """
        occurrence_type = self.eats_topic_map.subject_identifier_assertion_type
        if authority is None:
            entities = self.filter(occurrences__type=occurrence_type,
                                   occurrences__value=subject_indicator)
        else:
            entities = self.filter(occurrences__type=occurrence_type,
                                   occurrences__value=subject_indicator,
                                   occurrences__scope=authority)
        return entities.exclude(id=entity.id)

    def filter_by_entity_type (self, entity_type):
        assertion_type = self.eats_topic_map.entity_type_assertion_type
        role_type = self.eats_topic_map.property_role_type
        return self.filter(
            roles__association__type=assertion_type,
            roles__association__roles__type=role_type,
            roles__association__roles__player=entity_type)

    def get_by_identifier (self, identifier):
        # This method actually retrieves by Subject Identifier (based
        # on the identifier) and raises an exception if the entity's
        # identifier does not match that used in that derived Subject
        # Identifier. This is to allow for redirecting to the correct
        # URL in the case where an entity has been merged with
        # another, and the identifier supplied is that of the merged
        # entity.
        if identifier is None:
            raise Entity.DoesNotExist
        try:
            entity_si = self.eats_topic_map.get_entity_subject_identifier(
                identifier)
        except NoReverseMatch:
            # If the supplied identifier does not fit the required
            # format as defined in the URL conf.
            raise Entity.DoesNotExist
        topic = self.eats_topic_map.get_topic_by_subject_identifier(entity_si)
        if topic is None:
            raise Entity.DoesNotExist
        # get_topic_by_subject_identifier returns a tmapi.Topic. It
        # needs to be checked whether this is an Entity, and if so to
        # return the corresponding Entity object. Unfortunately,
        # without bypassing the TMAPI API, this requires more database
        # lookups.
        topic_id = topic.get_id()
        entity = super(EntityManager, self).get_by_identifier(topic_id)
        if topic_id != int(identifier):
            # Raise an exception, giving the 'correct' identifier for
            # the entity. This allows for, eg, redirecting to the
            # correct page for viewing/editing a merged entity.
            raise EATSMergedIdentifierException(topic_id)
        return entity

    def get_queryset (self):
        return super(EntityManager, self).get_queryset().filter(
            types=self.eats_topic_map.entity_type)


class Entity (Topic):

    objects = EntityManager()

    class Meta:
        proxy = True
        app_label = 'eats'

    def create_entity_relationship_property_assertion (
        self, authority, relationship_type, domain_entity, range_entity,
        certainty):
        """Creates a new entity relationship property assertion
        asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Authority`
        :param relationship_type: the type of relationship
        :type relationship_type: `EntityRelationshipType`
        :param domain_entity: entity playing the domain role in the
          relationship
        :type domain_entity: `Entity`
        :param range_entity: entity playing the range role in the
          relationship
        :type range_entity: `Entity`
        :param certainty: the certainty to be set
        :type certainty: `Topic`
        :rtype: `EntityRelationshipPropertyAssertion`

        """
        if domain_entity != self and range_entity != self:
            raise EATSValidationException('An entity relationship property assertion created for an entity must include that entity as one of the related entities')
        authority.validate_components(
            entity_relationship_type=relationship_type)
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.entity_relationship_assertion_type,
            scope=[authority, certainty],
            proxy=EntityRelationshipPropertyAssertion)
        assertion.set_players(domain_entity, range_entity, relationship_type)
        return assertion

    def create_entity_type_property_assertion (self, authority, entity_type):
        """Creates a new entity type property assertion asserted by
        `authority`.

        :param authority: authority asserting the property
        :type authority: `Authority`
        :param entity_type: entity type
        :type entity_type: `EntityType`
        :rtype: `EntityTypePropertyAssertion`

        """
        authority.validate_components(entity_type=entity_type)
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.entity_type_assertion_type, scope=[authority],
            proxy=EntityTypePropertyAssertion)
        assertion.set_players(self, entity_type)
        return assertion

    def create_existence_property_assertion (self, authority):
        """Creates a new existence property assertion asserted by
        `authority`.

        :param authority: authority asserting the property
        :type authority: `Authority`
        :rtype: `ExistencePropertyAssertion`

        """
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.existence_assertion_type, scope=[authority],
            proxy=ExistencePropertyAssertion)
        assertion.set_players(self)
        return assertion

    def create_name_property_assertion (self, authority, name_type, language,
                                        script, display_form,
                                        is_preferred=True):
        """Creates a name property assertion asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Authority`
        :param name_type: name type
        :type name_type: `NameType`
        :param language: language of the name
        :type language: `Language`
        :param script" script of the name
        :type script: `Script`
        :param display_form: display form of the name
        :type display_form: `str`
        :param is_preferred: if the name is a preferred form
        :type is_preferred: `Boolean`
        :rtype: `NamePropertyAssertion`

        """
        authority.validate_components(name_type=name_type, language=language,
                                      script=script)
        name = self.eats_topic_map.create_topic(proxy=Name)
        name.add_type(self.eats_topic_map.name_type)
        scope = [authority]
        if is_preferred:
            scope.append(self.eats_topic_map.is_preferred)
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.name_assertion_type, scope=scope,
            proxy=NamePropertyAssertion)
        assertion.set_players(self, name)
        name.create_name(display_form, name_type)
        # The language of the name is specified via an association
        # with the appropriate language topic.
        language_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_language_type)
        language_association.create_role(self.eats_topic_map.name_role_type,
                                         name)
        language_association.create_role(self.eats_topic_map.language_role_type,
                                         language)
        # The script of the name is specified via an association with
        # the appropriate script topic.
        script_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_script_type)
        script_association.create_role(self.eats_topic_map.name_role_type, name)
        script_association.create_role(self.eats_topic_map.script_role_type,
                                       script)
        name.update_name_cache()
        name.update_name_index()
        return assertion

    def create_note_property_assertion (self, authority, note):
        """Creates a note property assertion asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Authority`
        :param note: text of note
        :type note: `str`
        :rtype: `NotePropertyAssertion`

        """
        assertion = self.create_occurrence(
            self.eats_topic_map.note_assertion_type, note,
            scope=[authority], proxy=NotePropertyAssertion)
        return assertion

    def create_subject_identifier_property_assertion (self, authority,
                                                      subject_identifier):
        """Creates and returns a new subject identifier property
        assertion with URL `subject_identifier`, asserted by
        `authority`.

        :param authority: authority asserting the property
        :type authority: `Authority`
        :param subject_identifier: the subject identifier URL
        :type subject_identifier: `str`
        :rtype: `SubjectIdentifierPropertyAssertion`

        """
        return self.create_occurrence(
            self.eats_topic_map.subject_identifier_assertion_type,
            subject_identifier, scope=[authority],
            proxy=SubjectIdentifierPropertyAssertion)

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from .eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

    def get_assertion (self, assertion_id):
        """Returns the assertion with identifier `assertion_id` and
        associated with this entity, or None.

        :param assertion_id: the assertion's identifier
        :type assertion_id: string
        :rtype: `PropertyAssertion`

        """
        # Note that this is only returning assertions that are
        # implemented as TMAPI Associations.
        topic_map = self.eats_topic_map
        assertion = None
        construct = topic_map.get_construct_by_id(assertion_id)
        if construct is not None and isinstance(construct, Association):
            assertion_type = topic_map.get_assertion_type(construct)
            if assertion_type is not None:
                assertion = assertion_type.objects.get_by_identifier(
                    assertion_id)
                # Check that this assertion is associated with the entity.
                if assertion_type == EntityRelationshipPropertyAssertion:
                    # Entity relationships do not have an entity, but
                    # rather a domain entity and range entity.
                    if assertion.domain_entity != self and \
                            assertion.range_entity != self:
                        assertion = None
                elif assertion.entity != self:
                    assertion = None
        return assertion

    def get_duplicate_subject_identifiers (self, subject_identifier,
                                           authority=None):
        """Returns other entities that have a subject identifier
        property assertion matching `subject_identifier`.

        If `authority` is not None, only those entities that have
        `subject_identifier` asserted by `authority` are returned.

        :param subject_identifier: the subject identifier to find
        :type subject_identifier: `str`
        :param authority: optional authority to restrict search
        :type authority: `Authority`
        :rtype: `QuerySet` of `Entity`s

        """
        return Entity.objects.filter_by_duplicate_subject_identifiers(
            self, subject_identifier, authority)

    def get_eats_names (self, exclude=None):
        """Returns this entity's name property assertions.

        :param exclude: name to exclude from the results
        :type exclude: `NamePropertyAssertion`
        :rtype: `QuerySet` of `NamePropertyAssertion`s

        """
        names = NamePropertyAssertion.objects.filter_by_entity(self)
        if exclude:
            names = names.exclude(id=exclude.id)
        return names

    def get_eats_subject_identifier (self):
        """Returns this entity's subject identifier (not a property assertion,
        but the Topic's SI) that is formed from its id.

        :rtype: `tmapi.SubjectIdentifier`

        """
        locator_url = str(self.eats_topic_map.get_entity_subject_identifier(
            self.get_id()))
        # Check that this SI is actually associated with the entity.
        eats_si = None
        for si in self.get_subject_identifiers():
            if si.get_reference() != locator_url:
                continue
            eats_si = si
            break
        if eats_si is None:
            raise Exception
        return eats_si

    def get_eats_subject_identifiers (self):

        """Returns this entity's subject identifier property assertions.

        :rtype: `QuerySet` of `SubjectIdentifierPropertyAssertion`s

        """
        return SubjectIdentifierPropertyAssertion.objects.filter_by_entity(self)

    def get_entity_relationships (self):
        """Returns this entity's relationships to other entities.

        :rtype: `QuerySet` of `EntityRelationshipPropertyAssertion`s

        """
        return EntityRelationshipPropertyAssertion.objects.filter_by_entity(
            self)

    def get_entity_types (self):
        """Returns this entity's entity type property assertions.

        :rtype: `QuerySet` of `EntityTypePropertyAssertion`s

        """
        return EntityTypePropertyAssertion.objects.filter_by_entity(self)

    def get_existence_dates (self):
        """Return all dates associated with this entity's existence
        property assertions.

        :rtype: `QuerySet` of `Date`s

        """
        return Date.objects.filter_by_entity_existences(self)

    def get_existences (self):
        """Returns this entity's existence property assertions.

        :rtype: `QuerySet` of `ExistencePropertyAssertion`s

        """
        return ExistencePropertyAssertion.objects.filter_by_entity(self)

    def get_notes (self):
        """Returns this entity's note property assertions.

        :rtype: `QuerySet` of `NotePropertyAssertion`s

        """
        return NotePropertyAssertion.objects.filter_by_entity(self)

    def get_preferred_name (self, authority, language, script):
        """Returns the name for this entity that best matches
        `authority`, `language` and `script`.

        The name that best fits first the script (completely
        unreadable names are bad), then the authority, then the
        language, is returned.

        :param authority: preferred authority to assert the name
        :type authority: `Authority`
        :param language: preferred language of the name
        :type language: `Language`
        :param script: preferred script of the name
        :type script: `Script`
        :rtype: `NamePropertyAssertion`

        """
        try:
            return NamePropertyAssertion.objects.get_preferred(
                self, authority, language, script)
        except NamePropertyAssertion.DoesNotExist:
            return None

    def merge_in (self, other):
        # Due to the caching involved in entity relationships, it is
        # unfortunately necessary to move them manually before using
        # the TMAPI merge functionality.
        for er in other.get_entity_relationships():
            domain_entity = er.domain_entity
            if domain_entity == other:
                domain_entity = self
            range_entity = er.range_entity
            if range_entity == other:
                range_entity = self
            er.update(er.entity_relationship_type, domain_entity, range_entity,
                      er.certainty)
        super(Entity, self).merge_in(other)

    def remove (self):
        """Removes this entity from the EATS Topic Map."""
        assertion_getters = [self.get_eats_names, self.get_entity_relationships,
                             self.get_entity_types, self.get_existences,
                             self.get_eats_subject_identifiers, self.get_notes]
        for assertion_getter in assertion_getters:
            for assertion in assertion_getter():
                assertion.remove()
        super(Entity, self).remove()
