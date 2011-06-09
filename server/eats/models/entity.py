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
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.existence_assertion_type, scope=[authority])
        assertion.create_role(self.eats_topic_map.property_role_type,
                              self.eats_topic_map.existence)
        assertion.create_role(self.eats_topic_map.entity_role_type, self)

    def create_entity_type_property_assertion (self, authority, entity_type):
        """Creates a new entity type property assertion asserted by
        `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :param entity_type: entity type
        :type entity_type: `Topic`

        """
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.entity_type_assertion_type, scope=[authority])
        assertion.create_role(self.eats_topic_map.property_role_type,
                              entity_type)
        assertion.create_role(self.eats_topic_map.entity_role_type, self)
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
        :rtype: `Association`

        """
        name = self.eats_topic_map.convert_topic_to_entity(
            self.eats_topic_map.create_topic())
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
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.name_assertion_type, scope=[authority])
        assertion.create_role(self.eats_topic_map.property_role_type, name)
        assertion.create_role(self.eats_topic_map.entity_role_type, self)
        return assertion

    def create_note_property_assertion (self, authority, note):
        """Creates a note property assertion asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :param note: text of note
        :type note: string

        """
        self.create_occurrence(self.eats_topic_map.note_occurrence_type, note,
                               scope=[authority])

    def delete_entity_type_property_assertion (self, assertion):
        """Deletes the entity type property assertion `assertion`.

        :param assertion: entity type property assertion
        :type assertion: `Association`

        """
        assertion.remove()
        
    def delete_name_property_assertion (self, assertion):
        """Deletes the name property assertion `assertion`.

        :param assertion: name property assertion
        :type assertion: `Association`

        """
        name_topic = self.get_entity_name(assertion)
        for role in name_topic.get_roles_played():
            association = role.get_parent()
            association.remove()
        name_topic.remove()

    @property
    def eats_topic_map (self):
        return self._eats_topic_map

    @eats_topic_map.setter
    def eats_topic_map (self, value):
        self._eats_topic_map = value

    def get_authority (self, assertion):
        """Returns the authority asserting the property `assertion`.

        :param assertion: property assertion
        :type assertion: `Construct`
        :rtype: `Topic`

        """
        # QAZ: convert a possible IndexError into a more
        # useful/descriptive exception.
        return assertion.get_scope()[0]
    
    def get_eats_names (self):
        """Returns this entity's name property assertions.

        :rtype: list of `Association`s

        """
        # QAZ: This should return a QuerySet.
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.name_assertion_type)
        return [role.get_parent() for role in entity_roles]

    def get_entity_name (self, assertion):
        """Returns the name entity asserted in `assertion`.

        :param assertion: name property assertion
        :type assertion: `Association`
        :rtype: `Entity`

        """
        role = assertion.get_roles(self.eats_topic_map.property_role_type)[0]
        return self.eats_topic_map.convert_topic_to_entity(role.get_player())

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

        :rtype: list of `Association`s

        """
        # QAZ: This should return a QuerySet.
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
        # QAZ: This should return a QuerySet.
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.existence_assertion_type)
        existences = [role.get_parent() for role in entity_roles]
        if authority is not None:
            existences = [existence for existence in existences if
                          authority in existence.get_scope()]
        return existences

    def _get_name (self):
        """Returns the `Name` associated with this name entity."""
        # QAZ: convert a possible IndexError into a more
        # useful/descriptive exception.
        return self.get_names()[0]
    
    def get_notes (self):
        """Returns this entity's note property assertions.

        :rtype: `QuerySet` of `Occurrence`s

        """
        return self.get_occurrences(self.eats_topic_map.note_occurrence_type)

    def get_relationships (self):
        """Returns this entity's relationships to other entities.

        :rtype: list of `Association`s

        """
        domain_entity_roles = self.get_roles_played(
            self.eats_topic_map.domain_entity_role_type)
        range_entity_roles = self.get_roles_played(
            self.eats_topic_map.range_entity_role_type)
        relationships = [role.get_parent() for role in domain_entity_roles] + \
            [role.get_parent() for role in range_entity_roles]
        return relationships

    @property
    def name_language (self):
        """Returns the language of the name this entity represents.

        :rtype: `Topic`

        """
        return self._name_language_role.get_player()

    @name_language.setter
    def name_language (self, language):
        """Sets the language of the name this entity represents.

        :param language: language of the name
        :type language: `Topic`

        """
        self._name_language_role.set_player(language)

    @property
    def _name_language_role (self):
        """Returns the language role for the name this entity represents.

        :rtype: `Role`

        """
        # QAZ: possible index errors.
        name_role = self.get_roles_played(
            self.eats_topic_map.name_role_type,
            self.eats_topic_map.is_in_language_type)[0]
        language_role = name_role.get_parent().get_roles(
            self.eats_topic_map.language_role_type)[0]
        return language_role
        
    @property
    def name_script (self):
        """Returns the script of the name this entity represents.

        :rtype: `Topic`

        """
        return self._name_script_role.get_player()

    @name_script.setter
    def name_script (self, script):
        """Sets the script of the name this entity represents.

        :param script: script of the name
        :type script: `Topic`

        """
        self._name_script_role.set_player(script)

    @property
    def _name_script_role (self):
        """Returns the script role for the name this entity represents.

        :rtype: `Role`

        """
        # QAZ: possible index errors.
        name_role = self.get_roles_played(
            self.eats_topic_map.name_role_type,
            self.eats_topic_map.is_in_script_type)[0]
        script_role = name_role.get_parent().get_roles(
            self.eats_topic_map.script_role_type)[0]
        return script_role

    @property
    def name_type (self):
        """Returns the type of name this entity represents.

        :rtype: `Topic`

        """
        return self._get_name().get_type()

    @name_type.setter
    def name_type (self, name_type):
        """Sets the name type for the name this entity represents.

        :param name_type: type of name
        :type name_type: `Topic`

        """
        self._get_name().set_type(name_type)
    
    @property
    def name_value (self):
        """Returns the value of the name this entity represents.

        :rtype: unicode string

        """
        return self._get_name().get_value()

    @name_value.setter
    def name_value (self, value):
        """Sets the value of the name this entity represents.

        :param value: value of the name
        :type value: unicode string

        """
        self._get_name().set_value(value)

    def update_entity_type_property_assertion (self, authority, assertion,
                                               entity_type):
        assertion.get_roles(self.eats_topic_map.property_role_type)[0].remove()
        assertion.create_role(self.eats_topic_map.property_role_type,
                              entity_type)
        self._update_property_assertion_authority(assertion, authority)
        
    def update_existence_property_assertion (self, authority, assertion):
        self._update_property_assertion_authority(assertion, authority)
        
    def update_name_property_assertion (self, authority, assertion, name_type,
                                        language, script, display_form):
        name = self.get_entity_name(assertion)
        name.name_language = language
        name.name_script = script
        name.name_type = name_type
        name.name_value = display_form
        self._update_property_assertion_authority(assertion, authority)

    def update_note_property_assertion (self, authority, assertion, note):
        assertion.set_value(note)
        self._update_property_assertion_authority(assertion, authority)

    def _update_property_assertion_authority (self, assertion, authority):
        """Replaces the authority of `assertion` with `authority`.

        :param assertion: property assertion
        :type assertion: `Scoped` `Construct`
        :param authority: authority
        :type authority: `Topic`

        """
        for theme in assertion.get_scope():
            assertion.remove_theme(theme)
        assertion.add_theme(authority)
        
