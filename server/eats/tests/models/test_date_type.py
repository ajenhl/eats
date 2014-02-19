from tmapi.exceptions import TopicInUseException
from eats.models import DateType
from eats.tests.models.model_test_case import ModelTestCase


class DateTypeTestCase (ModelTestCase):

    def test_date_type_admin_name (self):
        date_type = self.create_date_type('exact')
        self.assertEqual(date_type.get_admin_name(), 'exact')
        date_type.set_admin_name('circa')
        self.assertEqual(date_type.get_admin_name(), 'circa')
        date_type2 = self.create_date_type('exact')
        self.assertRaises(Exception, date_type2.set_admin_name, 'circa')

    def test_date_type_delete (self):
        # A name type may not be deleted if it is associated with an
        # authority.
        self.assertEqual(DateType.objects.count(), 0)
        date_type = self.create_date_type('exact')
        self.assertEqual(DateType.objects.count(), 1)        
        authority = self.create_authority('test')
        authority.set_date_types([date_type])
        self.assertRaises(TopicInUseException, date_type.remove)
        self.assertEqual(DateType.objects.count(), 1)
        authority.set_date_types([])
        date_type.remove()
        self.assertEqual(DateType.objects.count(), 0)
