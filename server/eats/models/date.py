from tmapi.models import Topic

from date_part import DatePart


class Date (Topic):

    class Meta:
        proxy = True
        app_label = 'eats'


    @property
    def assembled_form (self):
        """Returns the string form of the date, composed from its parts."""
        parts = []
        form = ''
        if not parts:
            form = '[unspecified date]'
        return form

    def _cache_date_part (self, attr, part_type):
        """Returns the `DatePart` with the type `part_type`, caching the
        result in `attr`.

        :param attr: name of attribute to cache the date part in
        :type attr: string
        :param part_type: the date part type
        :type part_type: `Topic`
        :rtype: `DatePart`

        """
        value = getattr(self, attr, None)
        if value is None:
            value = self.get_occurrences(part_type, proxy=DatePart)[0]
            setattr(self, attr, value)
        return value

    def create_date_parts (self):
        """Creates date parts for this date."""
        self._start_tpq = self.create_name(
            '', self.eats_topic_map.start_tpq_date_type, proxy=DatePart)
        self._start = self.create_name('', self.eats_topic_map.start_date_type,
                                       proxy=DatePart)
        self._start_taq = self.create_name(
            '', self.eats_topic_map.start_taq_date_type, proxy=DatePart)
        self._point_tpq = self.create_name(
            '', self.eats_topic_map.point_tpq_date_type, proxy=DatePart)
        self._point = self.create_name('', self.eats_topic_map.point_date_type,
                                       proxy=DatePart)
        self._point_taq = self.create_name(
            '', self.eats_topic_map.point_taq_date_type, proxy=DatePart)
        self._end_tpq = self.create_name(
            '', self.eats_topic_map.end_tpq_date_type, proxy=DatePart)
        self._end = self.create_name('', self.eats_topic_map.end_date_type,
                                     proxy=DatePart)
        self._end_taq = self.create_name(
            '', self.eats_topic_map.end_taq_date_type, proxy=DatePart)
        date_period_association = self.eats_topic_map.create_association(
            self.eats_topic_map.date_period_association_type)
        date_period_association.create_role(self.eats_topic_map.date_role_type,
                                self)

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map
        
    @property
    def end (self):
        """Returns the end date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_end', self.eats_topic_map.end_date_type)
        
    @property
    def end_taq (self):
        """Returns the terminus ante quem end date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_end_taq', self.eats_topic_map.end_taq_date_type)
        
    @property
    def end_tpq (self):
        """Returns the terminus post quem end date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_end_tpq', self.eats_topic_map.end_tpq_date_type)

    @property
    def period (self):
        """Returns the period (span) of this date.

        :rtype: `Topic`
        
        """
        return self.period_association.get_roles(
            self.eats_topic_map.date_period_role_type)[0].get_player()

    @period.setter
    def period (self, period):
        """Sets the period (span) of this date.

        :param period: date period
        :type period: `Topic`

        """
        try:
            role = self.period_association.get_roles(
                self.eats_topic_map.date_period_role_type)[0]
            role.set_player(period)
        except IndexError:
            role = self.period_association.create_role(
                self.eats_topic_map.date_period_role_type, period)

    @property
    def period_association (self):
        """Returns the date period association for this date.

        :rtype: `Association`

        """
        if not hasattr(self, '_period_association'):
            date_role = self.get_roles_played(
                self.eats_topic_map.date_role_type,
                self.eats_topic_map.date_period_association_type)[0]
            self._period_association = date_role.get_parent()
        return self._period_association
        
    @property
    def point (self):
        """Returns the point date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_point', self.eats_topic_map.point_date_type)
        
    @property
    def point_taq (self):
        """Returns the terminus ante quem point date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_point_taq', self.eats_topic_map.point_taq_date_type)
        
    @property
    def point_tpq (self):
        """Returns the terminus post quem point date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_point_tpq', self.eats_topic_map.point_tpq_date_type)

    @property
    def start (self):
        """Returns the start date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_start', self.eats_topic_map.start_date_type)
        
    @property
    def start_taq (self):
        """Returns the terminus ante quem start date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_start_taq', self.eats_topic_map.start_taq_date_type)
        
    @property
    def start_tpq (self):
        """Returns the terminus post quem start date part.

        :rtype: `DatePart`

        """
        return self._cache_date_part(
            '_start_tpq', self.eats_topic_map.start_tpq_date_type)
