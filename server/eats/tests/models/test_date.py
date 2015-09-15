from eats.exceptions import EATSValidationException
from eats.tests.models.model_test_case import ModelTransactionTestCase


class DateTestCase (ModelTransactionTestCase):

    def setUp (self):
        super(DateTestCase, self).setUp()
        self.calendar = self.create_calendar('Gregorian')
        self.date_period = self.create_date_period('lifespan')
        self.date_type = self.create_date_type('exact')
        self.entity = self.tm.create_entity()
        self.authority.set_calendars([self.calendar])
        self.authority.set_date_periods([self.date_period])
        self.authority.set_date_types([self.date_type])

    def test_create_date_authority_components (self):
        # Test that create_date fails when one or more date components
        # are not associated with the authority.
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        self.assertEqual(len(assertion.get_dates()), 0)
        calendar = self.create_calendar('Julian')
        date_period = self.create_date_period('floruit')
        date_type = self.create_date_type('circa')
        date_data = {'date_period': date_period}
        self.assertRaises(EATSValidationException, assertion.create_date,
                          date_data)
        self.assertEqual(len(assertion.get_dates()), 0,
                         'A date should not be created with invalid data')
        date_data = {'date_period': self.date_period, 'point': '1 June 1900',
                     'point_normalised': '1900-06-01',
                     'point_type': self.date_type,
                     'point_certainty': self.tm.date_full_certainty,
                     'point_calendar': calendar}
        self.assertRaises(EATSValidationException, assertion.create_date,
                          date_data)
        self.assertEqual(len(assertion.get_dates()), 0,
                         'A date should not be created with invalid data')
        date_data['point_calendar'] = self.calendar
        date_data['point_type'] = date_type
        self.assertRaises(EATSValidationException, assertion.create_date,
                          date_data)
        self.assertEqual(len(assertion.get_dates()), 0,
                         'A date should not be created with invalid data')

    def test_create_date (self):
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date = assertion.create_date({'date_period': self.date_period})
        self.assertEqual(len(assertion.get_dates()), 1)
        self.assertEqual(date.period, self.date_period)
        self.assertEqual(date.start.calendar, None)
        self.assertEqual(date.start.date_type, None)
        self.assertEqual(date.start.certainty, None)
        self.assertEqual(date.start.get_value(), '')
        self.assertEqual(date.start.get_normalised_value(), '')
        self.assertEqual(date.assembled_form, '[unspecified date]')
        date_data = {'point': '1 January 1990', 'point_calendar': self.calendar,
                     'point_type': self.date_type,
                     'point_normalised': '1990-01-01',
                     'point_certainty': self.tm.date_full_certainty,
                     'date_period': self.date_period}
        date2 = assertion.create_date(date_data)
        self.assertEqual(len(assertion.get_dates()), 2)
        self.assertEqual(date2.period, self.date_period)
        self.assertEqual(date2.point.calendar, self.calendar)
        self.assertEqual(date2.point.date_type, self.date_type)
        self.assertEqual(date2.point.certainty, self.tm.date_full_certainty)
        self.assertEqual(date2.point.get_value(), '1 January 1990')
        self.assertEqual(date2.point.get_normalised_value(), '1990-01-01')
        self.assertEqual(date2.assembled_form, '1 January 1990')

    def test_update_date_authority_components (self):
        # Test that update fails when one or more date components
        # are not associated with the authority.
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date = assertion.create_date(
            {'point': '1 January 1990', 'point_calendar': self.calendar,
             'point_type': self.date_type, 'point_normalised': '1990-01-01',
             'point_certainty': self.tm.date_full_certainty,
             'date_period': self.date_period})
        calendar = self.create_calendar('Julian')
        date_period = self.create_date_period('floruit')
        date_type = self.create_date_type('circa')
        try:
            date.point.calendar = calendar
            self.fail('Updating a date part\'s calendar to one not associated with the authority should raise an exception')
        except EATSValidationException:
            pass
        try:
            date.period = date_period
            self.fail('Updating a date\'s period to one not associated with the authority should raise an exception')
        except EATSValidationException:
            pass
        try:
            date.point.date_type = date_type
            self.fail('Updating a date part\'s type to one not associated with the authority should raise an exception')
        except EATSValidationException:
            pass

    def test_update_date (self):
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date = assertion.create_date(
            {'point': '1 January 1990', 'point_calendar': self.calendar,
             'point_type': self.date_type, 'point_normalised': '1990-01-01',
             'point_certainty': self.tm.date_full_certainty,
             'date_period': self.date_period})
        date.point.set_value('29 November 2000')
        self.assertEqual(date.point.get_value(), '29 November 2000')
        date.point.set_normalised_value('2000-11-29')
        self.assertEqual(date.point.get_normalised_value(), '2000-11-29')
        calendar2 = self.create_calendar('Julian')
        self.authority.set_calendars([self.calendar, calendar2])
        date.point.calendar = calendar2
        self.assertEqual(date.point.calendar, calendar2)
        date.point.certainty = self.tm.date_no_certainty
        self.assertEqual(date.point.certainty, self.tm.date_no_certainty)
        date_period2 = self.create_date_period('floruit')
        self.authority.set_date_periods([self.date_period, date_period2])
        date.period = date_period2
        self.assertEqual(date.period, date_period2)
        date_type2 = self.create_date_type('circa')
        self.authority.set_date_types([self.date_type, date_type2])
        date.point.date_type = date_type2
        self.assertEqual(date.point.date_type, date_type2)

    def test_assembled_form (self):
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date = assertion.create_date(
            {'date_period': self.date_period, 'start_tpq': '1 January 1900',
             'start_tpq_certainty': self.tm.date_full_certainty,
             'start_tpq_calendar': self.calendar,
             'start_tpq_normalised': '1900-01-01',
             'start_tpq_type': self.date_type})
        self.assertEqual(date.start_tpq.assembled_form,
                         'at or after 1 January 1900')
        self.assertEqual(date.assembled_form,
                         'at or after 1 January 1900 \N{EN DASH}')
        date.start_taq.set_value('21 February 1900')
        date.start_taq.set_normalised_value('1900-02-21')
        date.start_taq.calendar = self.calendar
        date.start_taq.certainty = self.tm.date_full_certainty
        date.start_taq.date_type = self.date_type
        self.assertEqual(date.start_taq.assembled_form,
                         'at or before 21 February 1900')
        self.assertEqual(date.assembled_form, 'at or after 1 January 1900 and at or before 21 February 1900 \N{EN DASH}')
        date.start_taq.certainty = self.tm.date_no_certainty
        self.assertEqual(date.start_taq.assembled_form,
                         'at or before 21 February 1900?')
        self.assertEqual(date.assembled_form, 'at or after 1 January 1900 and at or before 21 February 1900? \N{EN DASH}')
        date.end_tpq.set_value('12 June 1975')
        date.end_tpq.set_normalised_value('1975-06-12')
        date.end_tpq.calendar = self.calendar
        date.end_tpq.certainty = self.tm.date_full_certainty
        date.end_tpq.date_type = self.date_type
        self.assertEqual(date.end_tpq.assembled_form,
                         'at or after 12 June 1975')
        self.assertEqual(date.assembled_form, 'at or after 1 January 1900 and at or before 21 February 1900? \N{EN DASH} at or after 12 June 1975')
        date.end_taq.set_value('16 June 1975')
        date.end_taq.set_normalised_value('1975-06-16')
        date.end_taq.calendar = self.calendar
        date.end_taq.certainty = self.tm.date_no_certainty
        date.end_taq.date_type = self.date_type
        self.assertEqual(date.end_taq.assembled_form,
                         'at or before 16 June 1975?')
        self.assertEqual(date.assembled_form, 'at or after 1 January 1900 and at or before 21 February 1900? \N{EN DASH} at or after 12 June 1975 and at or before 16 June 1975?')
        date.end.set_value('14 June 1975')
        date.end.set_normalised_value('1975-06-14')
        date.end.calendar = self.calendar
        date.end.certainty = self.tm.date_no_certainty
        date.end.date_type = self.date_type
        self.assertEqual(date.end.assembled_form, '14 June 1975?')
        self.assertEqual(date.assembled_form, 'at or after 1 January 1900 and at or before 21 February 1900? \N{EN DASH} 14 June 1975?')
        date.point_taq.set_value('2 November 2009')
        date.point_taq.set_normalised_value('2009-11-02')
        date.point_taq.calendar = self.calendar
        date.point_taq.certainty = self.tm.date_full_certainty
        date.point_taq.date_type = self.date_type
        self.assertEqual(date.point_taq.assembled_form,
                         'at or before 2 November 2009')
        self.assertEqual(date.assembled_form, 'at or before 2 November 2009')
        date.point.set_value('3 December 2010')
        date.point.set_normalised_value('2010-12-03')
        date.point.calendar = self.calendar
        date.point.certainty = self.tm.date_no_certainty
        date.point.date_type = self.date_type
        self.assertEqual(date.point.assembled_form, '3 December 2010?')
        self.assertEqual(date.assembled_form, '3 December 2010?')

    def test_property_assertion (self):
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date = assertion.create_date({'date_period': self.date_period})
        self.assertEqual(assertion, date.property_assertion)

    def test_normalised (self):
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date_data = {'point': '1 January 1990', 'point_calendar': self.calendar,
                     'point_type': self.date_type,
                     'point_normalised': '1990-01-01',
                     'point_certainty': self.tm.date_full_certainty,
                     'date_period': self.date_period}
        assertion.create_date(date_data)
        date = assertion.get_dates()[0]
        self.assertEqual(date.point.get_normalised_value(), '1990-01-01')

    def test_remove (self):
        self.assertEqual(len(self.entity.get_existences()), 0)
        assertion = self.entity.create_existence_property_assertion(
            self.authority)
        date_data = {'point': '1 January 1990', 'point_calendar': self.calendar,
                     'point_type': self.date_type,
                     'point_normalised': '1990-01-01',
                     'point_certainty': self.tm.date_full_certainty,
                     'date_period': self.date_period}
        date1 = assertion.create_date(date_data)
        self.assertEqual(len(assertion.get_dates()), 1)
        self.assertEqual(assertion.get_dates()[0], date1)
        date_data = {'start': '9 November 2001',
                     'start_calendar': self.calendar,
                     'start_type': self.date_type,
                     'start_normalised': '2001-11-09',
                     'start_certainty': self.tm.date_full_certainty,
                     'date_period': self.date_period}
        date2 = assertion.create_date(date_data)
        self.assertEqual(len(assertion.get_dates()), 2)
        self.assertTrue(date1 in assertion.get_dates())
        self.assertTrue(date2 in assertion.get_dates())
        date1.remove()
        self.assertEqual(len(assertion.get_dates()), 1)
        self.assertTrue(date2 in assertion.get_dates())
        self.assertEqual(len(self.entity.get_existences()), 1)
