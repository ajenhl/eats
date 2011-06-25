from tmapi.models import Occurrence


class DatePart (Occurrence):

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def calendar (self):
        """Returns the calendar for this date part, or None if no
        calendar is set.

        :rtype: `Topic`

        """
        if getattr(self, '_calendar', None) is None:
            for theme in self.scoping_topics:
                if self.eats_topic_map.calendar_type in theme.get_types():
                    self._calendar = theme
                    break
            else:
                self._calendar = None
        return self._calendar

    @calendar.setter
    def calendar (self, calendar):
        """Sets the calendar for this date part.

        :param calendar: the calendar to be set
        :type calendar: `Calendar`

        """
        if self.calendar is not None:
            self.remove_theme(self.calendar)
        self.add_theme(calendar)
        self._calendar = calendar
        self._scoping_topics = None

    @property
    def certainty (self):
        """Returns the certainty for this date part.

        :rtype: `Topic`
        
        """
        if getattr(self, '_certainty', None) is None:
            for theme in self.scoping_topics:
                if self.eats_topic_map.date_certainty_type in theme.get_types():
                    self._certainty = theme
                    break
            else:
                self._certainty = None
        return self._certainty

    @certainty.setter
    def certainty (self, certainty):
        """Sets the certainty for this date part.

        :param certainty: the certainty to be set
        :type certainty: `Topic`

        """
        if self.certainty is not None:
            self.remove_theme(self.certainty)
        self.add_theme(certainty)
        self._certainty = certainty
        self._scoping_topics = None

    @property
    def date_type (self):
        """Returns the type for this date part.

        :rtype: `Topic`

        """
        if getattr(self, '_date_type', None) is None:
            for theme in self.scoping_topics:
                if self.eats_topic_map.date_type_type in theme.get_types():
                    self._date_type = theme
                    break
            else:
                self._date_type = None
        return self._date_type

    @date_type.setter
    def date_type (self, date_type):
        """Sets the type for this date part.

        :param date_type: the type to be set
        :type date_type: `DateType`

        """
        if self.date_type is not None:
            self.remove_theme(self.date_type)
        self.add_theme(date_type)
        self._date_type = date_type
        self._scoping_topics = None
        
    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map
        
    @property
    def scoping_topics (self):
        if getattr(self, '_scoping_topics', None) is None:
            self._scoping_topics = self.get_scope()
        return self._scoping_topics
