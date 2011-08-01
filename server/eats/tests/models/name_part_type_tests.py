from eats.tests.models.model_test_case import ModelTestCase


class NamePartTypeTestCase (ModelTestCase):

    def test_name_part_type_admin_name (self):
        name_part_type = self.create_name_part_type('given')
        self.assertEqual(name_part_type.get_admin_name(), 'given')
        name_part_type.set_admin_name('family')
        self.assertEqual(name_part_type.get_admin_name(), 'family')
        name_part_type2 = self.create_name_part_type('given')
        self.assertRaises(Exception, name_part_type2.set_admin_name, 'family')
