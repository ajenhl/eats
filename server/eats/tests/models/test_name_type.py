from tmapi.exceptions import TopicInUseException
from eats.models import NameType
from eats.tests.models.model_test_case import ModelTestCase


class NameTypeTestCase (ModelTestCase):

    def test_name_type_admin_name (self):
        name_type = self.create_name_type('regular')
        self.assertEqual(name_type.get_admin_name(), 'regular')
        name_type.set_admin_name('pseudonym')
        self.assertEqual(name_type.get_admin_name(), 'pseudonym')
        name_type2 = self.create_name_type('regular')
        self.assertRaises(Exception, name_type2.set_admin_name, 'pseudonym')

    def test_name_type_delete (self):
        # A name type may not be deleted if it is associated with an
        # authority.
        self.assertEqual(NameType.objects.count(), 0)
        name_type = self.create_name_type('regular')
        self.assertEqual(NameType.objects.count(), 1)        
        authority = self.create_authority('test')
        authority.set_name_types([name_type])
        self.assertRaises(TopicInUseException, name_type.remove)
        self.assertEqual(NameType.objects.count(), 1)
        authority.set_name_types([])
        name_type.remove()
        self.assertEqual(NameType.objects.count(), 0)
