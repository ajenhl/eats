from tmapi.models import Topic

from name_index import NameIndex


class Name (Topic):

    class Meta:
        proxy = True
        app_label = 'eats'

    def _add_name_index (self):
        """Adds the forms of this name to the name index."""
        parts = self.display_form.split()
        for part in parts:
            indexed_form = NameIndex(entity=self.entity, name=self, form=part)
            indexed_form.save()

    def create (self, name_type, language, script, display_form):
        """Creates the data structures holding the name information.

        :param name_type: name type
        :type name_type: `Topic`
        :param language: language of the name
        :type language: `Topic`
        :param script" script of the name
        :type script: `Topic`
        :param display_form: display form of the name
        :type display_form: unicode string

        """
        self.create_name(display_form, name_type)
        # The language of the name is specified via an association
        # with the appropriate language topic.
        language_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_language_type)
        language_association.create_role(self.eats_topic_map.name_role_type,
                                         self)
        language_association.create_role(self.eats_topic_map.language_role_type,
                                         language)
        # The script of the name is specified via an association with
        # the appropriate script topic.
        script_association = self.eats_topic_map.create_association(
            self.eats_topic_map.is_in_script_type)
        script_association.create_role(self.eats_topic_map.name_role_type, self)
        script_association.create_role(self.eats_topic_map.script_role_type,
                                       script)
        self._add_name_index()

    def _delete_name_index_forms (self):
        """Deletes the indexed forms of this name."""
        self.indexed_name_forms.all().delete()
        
    @property
    def display_form (self):
        """Returns the display form of this name.

        :rtype: unicode string

        """
        return self._get_name().get_value()

    @display_form.setter
    def display_form (self, value):
        """Sets the display form of this name.

        Note that changing the value via this method does not update
        the name index.

        :param value: value of the name
        :type value: unicode string

        """
        self._get_name().set_value(value)

    @property
    def eats_topic_map (self):
        value = getattr(self, '_eats_topic_map', None)
        if value is None:
            from eats_topic_map import EATSTopicMap
            topic_map = self.get_parent()
            value = EATSTopicMap.objects.get(pk=topic_map.id)
            setattr(self, '_eats_topic_map', value)
        return value
        
    @property
    def entity (self):
        """Returns the entity to which this name belongs.

        :rtype: `Entity`
        
        """
        return self._entity

    @entity.setter
    def entity (self, entity):
        """Sets the entity to which this name belongs.

        :param entity: the entity
        :type entity: `Entity`

        """
        if hasattr(self, '_entity'):
            # QAZ: raise an EATS-specific exception.
            raise Exception('A name may not be reassigned to another, or the same, entity')
        self._entity = entity

    def _get_name (self):
        """Returns the TMAPI `Name` associated with this name
        entity."""
        # QAZ: convert a possible IndexError into a more
        # useful/descriptive exception.
        return self.get_names()[0]
    
    @property
    def language (self):
        """Returns the language of this name.

        :rtype: `Topic`

        """
        return self._language_role.get_player()

    @language.setter
    def language (self, language):
        """Sets the language of this name.

        Note that changing the language via this method does not
        update the name index.

        :param language: language of the name
        :type language: `Topic`

        """
        self._language_role.set_player(language)

    @property
    def _language_role (self):
        """Returns the language role for this name.

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
    def name_type (self):
        """Returns the name type of this name.

        :rtype: `Topic`

        """
        return self._get_name().get_type()

    @name_type.setter
    def name_type (self, name_type):
        """Sets the name type of this name.

        :param name_type: type of name
        :type name_type: `Topic`

        """
        self._get_name().set_type(name_type)
    
    def remove (self):
        for role in self.get_roles_played():
            association = role.get_parent()
            association.remove()
        super(Name, self).remove()
        
    @property
    def script (self):
        """Returns the script of this name.

        :rtype: `Topic`

        """
        return self._script_role.get_player()

    @script.setter
    def script (self, script):
        """Sets the script of this name.

        Note that changing the script via this method does not update
        the name index.

        :param script: script of the name
        :type script: `Topic`

        """
        self._script_role.set_player(script)

    @property
    def _script_role (self):
        """Returns the script role of this name.

        :rtype: `Role`

        """
        # QAZ: possible index errors.
        name_role = self.get_roles_played(
            self.eats_topic_map.name_role_type,
            self.eats_topic_map.is_in_script_type)[0]
        script_role = name_role.get_parent().get_roles(
            self.eats_topic_map.script_role_type)[0]
        return script_role

    def update (self, name_type, language, script, display_form):
        self.name_type = name_type
        self.language = language
        self.script = script
        self.display_form = display_form
        self.update_name_index()

    def update_name_index (self):
        """Updates the name index forms for this name."""
        self._delete_name_index_forms()
        self._add_name_index()
