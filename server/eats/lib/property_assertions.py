from eats.forms.edit import EntityTypeFormSet, ExistenceFormSet, create_choice_list


class PropertyAssertions (object):

    def __init__ (self, topic_map, entity, authorities, authority_choices,
                  data):
        self.topic_map = topic_map
        self.entity = entity
        self.authorities = set(authorities)
        self.authority_choices = authority_choices
        self.data = data
        self.existing = None
        self._editable, self._non_editable = self.categorise_assertions()
        if data is None:
            self.existing_data = self.get_existing_data()

    @property
    def editable (self):
        return self._editable

    @property
    def non_editable (self):
        return self._non_editable

    def get_editable (self, scoped, authorities):
        """Return `scoped` split into two lists, of editable and
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
        raise NotImplementedError

    def get_existing_data (self):
        raise NotImplementedError


class ExistencePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        return ExistenceFormSet(
            data=self.data, prefix='existences', initial=self.existing_data,
            authority_choices=self.authority_choices)

    def categorise_assertions (self):
        existences = self.entity.get_existences()
        return self.get_editable(existences, self.authorities)
    
    def get_existing_data (self):
        existing = []
        for existence in self.editable:
            # QAZ: assuming that there is a single scoping topic, and
            # that it is the authority.
            existing.append({'authority': existence.get_scope()[0].get_id()})
        return existing


class EntityTypePropertyAssertions (PropertyAssertions):

    @property
    def formset (self):
        entity_type_choices = create_choice_list(self.topic_map,
                                                 self.topic_map.entity_types)
        return EntityTypeFormSet(
            data=self.data, prefix='entity_types', initial=self.existing_data,
            authority_choices=self.authority_choices,
            entity_type_choices=entity_type_choices)

    def categorise_assertions (self):
        entity_types = self.entity.get_entity_types()
        return self.get_editable(entity_types, self.authorities)

    def get_existing_data (self):
        existing = []
        for entity_type in self.editable:
            # QAZ: assuming that there is a single scoping topic, and
            # that it is the authority.
            existing.append(
                {'authority': entity_type.get_scope()[0].get_id(),
                 'entity_type': entity_type.get_roles(self.topic_map.property_role_type)[0].get_player().get_id()}
                )
        return existing
