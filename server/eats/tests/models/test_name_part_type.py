from tmapi.exceptions import TopicInUseException
from eats.models import NamePartType
from eats.tests.models.model_test_case import ModelTestCase


class NamePartTypeTestCase (ModelTestCase):

    def test_name_part_type_admin_name (self):
        name_part_type = self.create_name_part_type('given')
        self.assertEqual(name_part_type.get_admin_name(), 'given')
        name_part_type.set_admin_name('family')
        self.assertEqual(name_part_type.get_admin_name(), 'family')
        name_part_type2 = self.create_name_part_type('given')
        self.assertRaises(Exception, name_part_type2.set_admin_name, 'family')

    def test_name_part_type_delete (self):
        # A name part type may not be deleted if it is associated with
        # an authority.
        self.assertEqual(NamePartType.objects.count(), 0)
        name_part_type = self.create_name_part_type('given')
        self.assertEqual(NamePartType.objects.count(), 1)        
        authority = self.create_authority('test')
        authority.set_name_part_types([name_part_type])
        self.assertRaises(TopicInUseException, name_part_type.remove)
        self.assertEqual(NamePartType.objects.count(), 1)
        authority.set_name_part_types([])
        name_part_type.remove()
        self.assertEqual(NamePartType.objects.count(), 0)
