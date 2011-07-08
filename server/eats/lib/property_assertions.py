from eats.constants import FORWARD_RELATIONSHIP_MARKER, \
    REVERSE_RELATIONSHIP_MARKER
from eats.forms.edit import EntityRelationshipFormSet, EntityTypeFormSet, ExistenceFormSet, NameFormSet, NoteFormSet, create_choice_list
from eats.models import EntityRelationshipType, EntityType, Language, NameType, Script


class PropertyAssertions (object):

    def __init__ (self, topic_map, entity, authorities, authority_choices,
                  data):
        self.topic_map = topic_map
        self.entity = entity
        self.authorities = authorities
        self.authority_choices = authority_choices
        self.data = data
        self._editable, self._non_editable = self.categorise_assertions()

    @property
    def editable (self):
        return self._editable
    
    @property
    def non_editable (self):
        return self._non_editable

    def _create_formset (self, formset_class, formset_data):
        defaults = {'topic_map': self.topic_map, 'entity': self.entity,
                    'data': self.data, 'instances': self.editable,
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
        authority_ids = authorities.values_list('id', flat=True)
        editable = []
        non_editable = []
        for element in scoped:
            authority_id = element.get_scope().values_list('id', flat=True)[0]
            if authority_id not in authority_ids:
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


class ExistencePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        data = {'prefix': 'existences'}
        return self._create_formset(ExistenceFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_existences()
        return self.get_editable(assertions, self.authorities)


class EntityRelationshipPropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        relationship_type_choices = []
        for relationship_type in EntityRelationshipType.objects.all():
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


class EntityTypePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        entity_type_choices = create_choice_list(
            self.topic_map, EntityType.objects.all())
        data = {'entity_type_choices': entity_type_choices,
                'prefix': 'entity_types'}
        return self._create_formset(EntityTypeFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_entity_types()
        return self.get_editable(assertions, self.authorities)


class NamePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        name_type_choices = create_choice_list(self.topic_map,
                                               NameType.objects.all())
        language_choices = create_choice_list(self.topic_map,
                                              Language.objects.all())
        script_choices = create_choice_list(self.topic_map,
                                            Script.objects.all())
        data = {'prefix': 'names', 'name_type_choices': name_type_choices,
                'language_choices': language_choices,
                'script_choices': script_choices}
        return self._create_formset(NameFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_eats_names()
        return self.get_editable(assertions, self.authorities)


class NotePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        data = {'prefix': 'notes'}
        return self._create_formset(NoteFormSet, data)

    def categorise_assertions (self):
        assertions = self.entity.get_notes()
        return self.get_editable(assertions, self.authorities)
