from .authority import Authority
from .date import Date


class PropertyAssertion (object):

    @property
    def authority (self):
        """Returns the authority of this property assertion.

        :rtype: `Topic`

        """
        topic = self.get_scope().filter(
            types=self.eats_topic_map.authority_type)[0]
        return Authority.objects.get_by_identifier(topic.get_id())

    @property
    def certainty (self):
        """Returns the certainty for this property assertion.

        :rtype: `Topic`

        """
        if getattr(self, '_certainty', None) is None:
            certainty_type = self.eats_topic_map.property_assertion_certainty_type
            for theme in self.scoping_topics:
                if certainty_type in theme.get_types():
                    self._certainty = theme
                    break
            else:
                self._certainty = None
        return self._certainty

    @certainty.setter
    def certainty (self, certainty):
        """Sets the certainty for this property assertion.

        :param certainty: the certainty to be set
        :type certainty: `Topic`

        """
        if self.certainty is not None:
            self.remove_theme(self.certainty)
        self.add_theme(certainty)
        self._certainty = certainty
        self._scoping_topics = None

    def create_date (self, data):
        """Creates a new date associated with this property assertion."""
        date = self.eats_topic_map.create_topic(proxy=Date)
        try:
            date.add_type(self.eats_topic_map.date_type)
            date.create_date_parts()
            self.create_role(self.eats_topic_map.date_role_type, date)
            date.period = data['date_period']
            for prefix in ('start', 'start_taq', 'start_tpq', 'end', 'end_taq',
                           'end_tpq', 'point', 'point_taq', 'point_tpq'):
                if data.get(prefix):
                    part = getattr(date, prefix)
                    part.set_value(data[prefix])
                    part.calendar = data[prefix + '_calendar']
                    part.certainty = data[prefix + '_certainty']
                    part.set_normalised_value(data[prefix + '_normalised'])
                    part.date_type = data[prefix + '_type']
        except:
            date.remove()
            raise
        return date

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from .eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

    @property
    def entity (self):
        """Returns the entity making this property assertion."""
        if not hasattr(self, '_entity'):
            from .entity import Entity
            role = self.get_roles(self.eats_topic_map.entity_role_type)[0]
            self._entity = role.get_player(proxy=Entity)
        return self._entity

    def get_date (self, date_id):
        """Returns the date specified by `date_id`. If there is no
        such date, or the date is not associated with this property
        assertion, returns None.

        :param date_id: id of the requested date
        :type date_id: integer
        :rtype: `Date` or None

        """
        try:
            date = Date.objects.get_by_identifier(date_id)
        except Date.DoesNotExist:
            return None
        if date.property_assertion != self:
            return None
        return date

    def get_dates (self):
        """Returns a list of dates associated with this property assertion.

        :rtype: list of `Date`s

        """
        date_roles = self.get_roles(self.eats_topic_map.date_role_type)
        return [role.get_player(proxy=Date) for role in date_roles]

    @property
    def is_preferred (self):
        """Returns True if this property assertion is marked as
        preferred, False otherwise.

        :rtype: `Boolean`

        """
        return self.eats_topic_map.is_preferred in self.get_scope()

    @is_preferred.setter
    def is_preferred (self, is_preferred):
        """Sets whether this property assertion is preferred."""
        if is_preferred:
            self.add_theme(self.eats_topic_map.is_preferred)
        else:
            self.remove_theme(self.eats_topic_map.is_preferred)

    @property
    def scoping_topics (self):
        if getattr(self, '_scoping_topics', None) is None:
            self._scoping_topics = self.get_scope()
        return self._scoping_topics

    def set_players (self, entity, property):
        raise NotImplementedError

    def update (self, *args):
        """Updates this property assertion with the new data.

        This method should be overridden by subclasses.

        """
        raise NotImplementedError
