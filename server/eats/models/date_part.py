from tmapi.models import Name

from .calendar import Calendar
from .date_type import DateType


class DatePart (Name):

    class Meta:
        proxy = True
        app_label = 'eats'

    @property
    def assembled_form (self):
        form = self.get_value()
        if form:
            if self.certainty == self.eats_topic_map.date_no_certainty:
                form = form + '?'
            if self.get_type() in (self.eats_topic_map.point_tpq_date_type,
                                   self.eats_topic_map.start_tpq_date_type,
                                   self.eats_topic_map.end_tpq_date_type):
                form = 'at or after ' + form
            elif self.get_type() in (self.eats_topic_map.point_taq_date_type,
                                     self.eats_topic_map.start_taq_date_type,
                                     self.eats_topic_map.end_taq_date_type):
                form = 'at or before ' + form
        return form

    @property
    def calendar (self):
        """Returns the calendar for this date part, or None if no
        calendar is set.

        :rtype: `Calendar`

        """
        if getattr(self, '_calendar', None) is None:
            calendar_type = self.eats_topic_map.calendar_type
            for theme in self.scoping_topics:
                if calendar_type in theme.get_types():
                    self._calendar = Calendar.objects.get_by_identifier(
                        theme.get_id())
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
        self.date.property_assertion.authority.validate_components(
            calendar=calendar)
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
            certainty_type = self.eats_topic_map.date_certainty_type
            for theme in self.scoping_topics:
                if certainty_type in theme.get_types():
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
    def date (self):
        """Returns the date of which this is a part.

        :rtype: `Date`

        """
        from .date import Date
        return self.get_parent(proxy=Date)

    @property
    def date_type (self):
        """Returns the type for this date part.

        :rtype: `DateType`

        """
        if getattr(self, '_date_type', None) is None:
            date_type_type = self.eats_topic_map.date_type_type
            for theme in self.scoping_topics:
                if date_type_type in theme.get_types():
                    self._date_type = DateType.objects.get_by_identifier(
                        theme.get_id())
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
        self.date.property_assertion.authority.validate_components(
            date_type=date_type)
        if self.date_type is not None:
            self.remove_theme(self.date_type)
        self.add_theme(date_type)
        self._date_type = date_type
        self._scoping_topics = None

    @property
    def eats_topic_map (self):
        if not hasattr(self, '_eats_topic_map'):
            from .eats_topic_map import EATSTopicMap
            self._eats_topic_map = self.get_topic_map(proxy=EATSTopicMap)
        return self._eats_topic_map

    def get_form_data (self, prefix):
        """Returns the data for this date part in a format suitable
        for a `DateForm`.

        :param prefix: prefix for dictionary keys
        :type prefix: string
        :rtype: dict

        """
        data = {}
        value = self.get_value()
        if value:
            certainty = False
            if self.certainty == self.eats_topic_map.date_full_certainty:
                certainty = True
            data[prefix] = value
            data[prefix+'_normalised'] = self.get_normalised_value()
            data[prefix+'_type'] = self.date_type.get_id()
            data[prefix+'_calendar'] = self.calendar.get_id()
            data[prefix+'_certainty'] = certainty
        return data

    def get_normalised_value (self):
        """Returns the value of the normalised form of this date part.

        :rtype: Unicode string

        """
        return self.normalised.get_value()

    @property
    def normalised (self):
        """Returns the variant name that represents the normalised
        form of this date part.

        :rtype: `Variant`

        """
        if not hasattr(self, '_normalised'):
            variants = self.get_variants()
            if len(variants) == 0:
                self._normalised = self.create_variant(
                    '', self.eats_topic_map.normalised_date_form_type)
            else:
                self._normalised = variants[0]
        return self._normalised

    @property
    def scoping_topics (self):
        if getattr(self, '_scoping_topics', None) is None:
            self._scoping_topics = self.get_scope()
        return self._scoping_topics

    def set_normalised_value (self, value):
        """Sets the value of the normalised form of this date part.

        :param value: value of the normalised form
        :type value: Unicode string

        """
        self.normalised.set_value(value)
