from eats.tests.base_test_case import BaseTestCase


class DateTest (BaseTestCase):

    def setUp (self):
        super(DateTest, self).setUp()
        self.calendar = self.create_calendar('Gregorian')
        self.date_period = self.create_date_period('lifespan')
        self.date_type = self.create_date_type('exact')
        self.entity = self.tm.create_entity(self.authority)
    
    def test_create_date (self):
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date = assertion.create_date()
        self.assertEqual(len(assertion.get_dates()), 1)
        self.assertEqual(date.assembled_form, '[unspecified date]')
        self.assertEqual(date.start.calendar, None)
        self.assertEqual(date.start.date_type, None)
        self.assertEqual(date.start.certainty, None)
        date.start.calendar = self.calendar
        self.assertEqual(date.start.calendar, self.calendar)
        date.start.date_type = self.date_type
        self.assertEqual(date.start.date_type, self.date_type)
        date_data = {'point': '1 January 1990', 'point_calendar': self.calendar,
                     'point_type': self.date_type,
                     'point_certainty': self.tm.date_full_certainty,
                     'date_period': self.date_period}
        date2 = assertion.create_date(date_data)
        self.assertEqual(len(assertion.get_dates()), 2)
        self.assertEqual(date2.point.calendar, self.calendar)
        self.assertEqual(date2.point.date_type, self.date_type)
        self.assertEqual(date2.point.certainty, self.tm.date_full_certainty)
        self.assertEqual(date2.assembled_form, '1 January 1990')
