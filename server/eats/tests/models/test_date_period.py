from tmapi.exceptions import TopicInUseException
from eats.models import DatePeriod
from eats.tests.models.model_test_case import ModelTestCase


class DatePeriodTestCase (ModelTestCase):

    def test_date_period_admin_name (self):
        date_period = self.create_date_period('lifespan')
        self.assertEqual(date_period.get_admin_name(), 'lifespan')
        date_period.set_admin_name('floruit')
        self.assertEqual(date_period.get_admin_name(), 'floruit')
        date_period2 = self.create_date_period('lifespan')
        self.assertRaises(Exception, date_period2.set_admin_name, 'floruit')

    def test_date_period_delete (self):
        # A name type may not be deleted if it is associated with an
        # authority.
        self.assertEqual(DatePeriod.objects.count(), 0)
        date_period = self.create_date_period('lifespan')
        self.assertEqual(DatePeriod.objects.count(), 1)        
        authority = self.create_authority('test')
        authority.set_date_periods([date_period])
        self.assertRaises(TopicInUseException, date_period.remove)
        self.assertEqual(DatePeriod.objects.count(), 1)
        authority.set_date_periods([])
        date_period.remove()
        self.assertEqual(DatePeriod.objects.count(), 0)
