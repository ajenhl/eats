from date import Date


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

    def create_date (self, data=None):
        """Creates a new date associated with this property assertion."""
        date = self.eats_topic_map.create_topic(proxy=Date)
        date.create_date_parts()
        self.create_role(self.eats_topic_map.date_role_type, date)
        if data is not None:
            for prefix in ('start', 'start_taq', 'start_tpq', 'end', 'end_taq',
                           'end_tpq', 'point', 'point_taq', 'point_tpq'):
                if data.get(prefix):
                    part = getattr(date, prefix)
                    part.set_value(data[prefix])
                    part.calendar = data[prefix + '_calendar']
                    part.certainty = data[prefix + '_certainty']
                    part.date_type = data[prefix + '_type']
        return date
        
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
        if not hasattr(self, '_entity'):
            from entity import Entity
            role = self.get_roles(self.eats_topic_map.entity_role_type)[0]
            self._entity = role.get_player(proxy=Entity)
        return self._entity

    def get_dates (self):
        """Returns a list of dates associated with this property assertion.

        :rtype: list of `Date`s

        """
        date_roles = self.get_roles(self.eats_topic_map.date_role_type)
        return [role.get_player(proxy=Date) for role in date_roles]
    
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
