from eats.tests.base_test_case import BaseTestCase


class NamePartTestCase (BaseTestCase):

    def setUp (self):
        super(NamePartTestCase, self).setUp()
        self.language = self.create_language('English', 'en')
        self.name_part_type1 = self.create_name_part_type('given')
        self.name_part_type2 = self.create_name_part_type('family')
        self.name_type = self.create_name_type('regular')
        self.script = self.create_script('Latin', 'Latn')
        self.authority.set_languages([self.language])
        self.authority.set_name_part_types([self.name_part_type1,
                                            self.name_part_type2])
        self.authority.set_name_types([self.name_type])
        self.authority.set_scripts([self.script])
        self.entity = self.tm.create_entity(self.authority)
        self.name = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script, '')
    
    def test_create_name_part (self):
        self.assertEqual(len(self.name.get_name_parts()), 0)
        self.name.create_name_part(self.name_part_type1, self.language,
                                   self.script, 'Johann', 1)
        self.assertEqual(len(self.name.get_name_parts()), 1)
