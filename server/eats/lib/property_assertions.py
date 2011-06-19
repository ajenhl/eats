from eats.constants import FORWARD_RELATIONSHIP_MARKER, \
    REVERSE_RELATIONSHIP_MARKER
from eats.forms.edit import EntityRelationshipFormSet, EntityTypeFormSet, ExistenceFormSet, NameFormSet, NoteFormSet, create_choice_list


class PropertyAssertions (object):

    def __init__ (self, topic_map, entity, authorities, authority_choices,
                  data):
        self.topic_map = topic_map
        self.entity = entity
        self.authorities = set(authorities)
        self.authority_choices = authority_choices
        self.data = data
        self.existing_data = self._editable = self._non_editable = None
        if data is None:
            self._editable, self._non_editable = self.categorise_assertions()
            self.existing_data = self.get_existing_data()

    @property
    def editable (self):
        return self._editable
    
    @property
    def non_editable (self):
        return self._non_editable

    def _create_formset (self, formset_class, formset_data):
        defaults = {'topic_map': self.topic_map, 'entity': self.entity,
                    'data': self.data, 'initial': self.existing_data,
                    'authority_choices': self.authority_choices}
        defaults.update(formset_data)
        return formset_class(**defaults)
    
    def get_editable (self, scoped, authorities):
        """Returns `scoped` split into two lists, of editable and
        non-editable elements.

        Editable elements are those that are scoped by an authority in
        `authorities`.

        :param scoped: list of elements to be categorised
        :type scoped: list of `Scoped`
        :param authorities: authorities that are editable
        :type authorities: set of `Topic`s
        :rtype: two-tuple of lists
        
        """
        editable = []
        non_editable = []
        for element in scoped:
            if set(element.get_scope()).isdisjoint(authorities):
                non_editable.append(element)
            else:
                editable.append(element)
        return editable, non_editable

    def categorise_assertions (self):
        """Returns the entity's property assertions as a tuple of
        editable and non-editable objects.

        :rtype: tuple of lists

        """
        raise NotImplementedError

    def get_existing_data (self):
        """Returns the data for each editable property assertion,
        suitable for feeding into a Form.

        :rtype: list of dictionaries

        """
        raise NotImplementedError


class ExistencePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        data = {'prefix': 'existences'}
        return self._create_formset(ExistenceFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_existences()
        return self.get_editable(assertions, self.authorities)
    
    def get_existing_data (self):
        existing = []
        for assertion in self.editable:
            # QAZ: assuming that there is a single scoping topic, and
            # that it is the authority.
            existing.append(
                {'authority': assertion.authority.get_id(),
                 'assertion': assertion.get_id()})
        return existing


class EntityRelationshipPropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        relationship_type_choices = []
        for relationship_type in self.topic_map.entity_relationship_types:
            id = unicode(relationship_type.get_id())
            name = relationship_type.get_names(
                self.topic_map.relationship_name_type)[0].get_value()
            reverse_name = relationship_type.get_names(
                self.topic_map.reverse_relationship_name_type)[0].get_value()
            relationship_type_choices.append((id + FORWARD_RELATIONSHIP_MARKER,
                                              name ))
            relationship_type_choices.append((id + REVERSE_RELATIONSHIP_MARKER,
                                              reverse_name))
        relationship_type_choices = [('', '----------')] + \
            relationship_type_choices
        data = {'relationship_type_choices': relationship_type_choices,
                'prefix': 'entity_relationships'}
        return self._create_formset(EntityRelationshipFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_entity_relationships()
        return self.get_editable(assertions, self.authorities)

    def get_existing_data (self):
        existing = []
        for assertion in self.editable:
            # QAZ: assuming that there is a single scoping topic, and
            # that it is the authority.
            relationship_id = str(assertion.entity_relationship_type.get_id())
            direction_marker = FORWARD_RELATIONSHIP_MARKER
            related_entity = assertion.range_entity
            if self.entity == assertion.range_entity:
                direction_marker = REVERSE_RELATIONSHIP_MARKER
                related_entity = assertion.domain_entity
            existing.append(
                {'authority': assertion.authority.get_id(),
                 'assertion': assertion.get_id(),
                 'relationship_type': relationship_id + direction_marker,
                 'related_entity': related_entity.get_id()})
        return existing


class EntityTypePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        entity_type_choices = create_choice_list(self.topic_map,
                                                 self.topic_map.entity_types)
        data = {'entity_type_choices': entity_type_choices,
                'prefix': 'entity_types'}
        return self._create_formset(EntityTypeFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_entity_types()
        return self.get_editable(assertions, self.authorities)

    def get_existing_data (self):
        existing = []
        for assertion in self.editable:
            # QAZ: assuming that there is a single scoping topic, and
            # that it is the authority.
            existing.append(
                {'authority': assertion.authority.get_id(),
                 'entity_type': assertion.entity_type.get_id(),
                 'assertion': assertion.get_id()})
        return existing


class NamePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        name_type_choices = create_choice_list(self.topic_map,
                                               self.topic_map.name_types)
        language_choices = create_choice_list(self.topic_map,
                                              self.topic_map.languages)
        script_choices = create_choice_list(self.topic_map,
                                            self.topic_map.scripts)
        data = {'prefix': 'names', 'name_type_choices': name_type_choices,
                'language_choices': language_choices,
                'script_choices': script_choices}
        return self._create_formset(NameFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_eats_names()
        return self.get_editable(assertions, self.authorities)

    def get_existing_data (self):
        existing = []
        for assertion in self.editable:
            name = assertion.name
            existing.append(
                {'authority': assertion.authority.get_id(),
                 'assertion': assertion.get_id(),
                 'display_form': name.display_form,
                 'name_type': name.name_type.get_id(),
                 'language': name.language.get_id(),
                 'script': name.script.get_id(),
                 })
        return existing


class NotePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        data = {'prefix': 'notes'}
        return self._create_formset(NoteFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_notes()
        return self.get_editable(assertions, self.authorities)

    def get_existing_data (self):
        existing = []
        for assertion in self.editable:
            existing.append(
                {'authority': assertion.authority.get_id(),
                 'assertion': assertion.get_id(),
                 'note': assertion.note})
        return existing
