class PropertyAssertion (object):

    @property
    def authority (self):
        """Returns the authority of this property assertion.

        :rtype: `Topic`

        """
        # QAZ: convert a possible IndexError into a more
        # useful/descriptive exception. Also raise an exception if
        # there is more than one theme.
        return self.get_scope()[0]

    @authority.setter
    def authority (self, authority):
        """Sets the authority of this property assertion.

        :param authority: authority
        :type authority: `Topic`

        """
        for theme in self.get_scope():
            self.remove_theme(theme)
        self.add_theme(authority)

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
        """Returns the entity making this property assertion."""
        return self._entity

    def set_players (self, entity, property):
        raise NotImplementedError
        
    def update (self, authority, *args):
        """Updates this property assertion with the new data.

        This method should be overridden by subclasses, but called via
        super.

        :param authority: authority making the property assertion
        :type authority: `Topic`

        """
        if authority != self.authority:
            self.authority = authority
