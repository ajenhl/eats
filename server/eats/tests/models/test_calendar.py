from tmapi.exceptions import TopicInUseException
from eats.models import Calendar
from eats.tests.models.model_test_case import ModelTestCase


class CalendarTestCase (ModelTestCase):

    def test_calendar_admin_name (self):
        calendar = self.create_calendar('Gregorian')
        self.assertEqual(calendar.get_admin_name(), 'Gregorian')
        calendar.set_admin_name('Julian')
        self.assertEqual(calendar.get_admin_name(), 'Julian')
        calendar2 = self.create_calendar('Gregorian')
        self.assertRaises(Exception, calendar2.set_admin_name, 'Julian')

    def test_calendar_delete (self):
        # A name type may not be deleted if it is associated with an
        # authority.
        self.assertEqual(Calendar.objects.count(), 0)
        calendar = self.create_calendar('Gregorian')
        self.assertEqual(Calendar.objects.count(), 1)        
        authority = self.create_authority('test')
        authority.set_calendars([calendar])
        self.assertRaises(TopicInUseException, calendar.remove)
        self.assertEqual(Calendar.objects.count(), 1)
        authority.set_calendars([])
        calendar.remove()
        self.assertEqual(Calendar.objects.count(), 0)
