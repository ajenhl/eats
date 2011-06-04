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

        """
        name = self.eats_topic_map.convert_topic_to_entity(
            self.eats_topic_map.create_topic())
        name.create_name(display_form, name_type)
        language_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_language_type)
        language_association.create_role(self.eats_topic_map.name_role_type,
                                         name)
        language_association.create_role(self.eats_topic_map.language_role_type,
                                         language)
        script_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_script_type)
        script_association.create_role(self.eats_topic_map.name_role_type, name)
        script_association.create_role(self.eats_topic_map.script_role_type,
                                       script)
        assertion = self.eats_topic_map.create_association(
            self.eats_topic_map.name_assertion_type, scope=[authority])
        assertion.create_role(self.eats_topic_map.property_role_type, name)
        assertion.create_role(self.eats_topic_map.entity_role_type, self)

    def create_note_property_assertion (self, authority, note):
        """Creates a note property assertion asserted by `authority`.

        :param authority: authority asserting the property
        :type authority: `Topic`
        :param note: text of note
        :type note: string

        """
        self.create_occurrence(self.eats_topic_map.note_occurrence_type, note,
                               scope=[authority])
        
    @property
    def eats_topic_map (self):
        return self._eats_topic_map

    @eats_topic_map.setter
    def eats_topic_map (self, value):
        self._eats_topic_map = value

    def get_eats_names (self):
        """Returns this entity's name property assertions.

        :rtype: list of `Association`s

        """
        entity_roles = self.get_roles_played(
            self.eats_topic_map.entity_role_type,
            self.eats_topic_map.name_assertion_type)
        return [role.get_parent() for role in entity_roles]
        
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

    def get_notes (self):
        """Returns this entity's note property assertions.

        :rtype: list of `Occurrence`s

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
        return self.name_language_role.get_player()

    @name_language.setter
    def name_language (self, language):
        """Sets the language of the name this entity represents.

        :param language: language of the name
        :type language: `Topic`

        """
        self.name_language_role.set_player(language)

    @property
    def name_language_role (self):
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
        return self.name_script_role.get_player()

    @name_script.setter
    def name_script (self, script):
        """Sets the script of the name this entity represents.

        :param script: script of the name
        :type script: `Topic`

        """
        self.name_script_role.set_player(script)

    @property
    def name_script_role (self):
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
    
    def update_name_property_assertion (self, assertion, name_type, language,
                                        script, display_form):
        role = assertion.get_roles(self.eats_topic_map.property_role_type)[0]
        name_topic = self.eats_topic_map.convert_topic_to_entity(
            role.get_player())
        name_topic.name_language = language
        name_topic.name_script = script
        # QAZ: is there only one name?
        name = name_topic.get_names()[0]
        name.set_type(name_type)
        name.set_value(display_form)
