from eats.tests.models.model_test_case import ModelTestCase


class EntityTest (ModelTestCase):

    def setUp (self):
        super(EntityTest, self).setUp()
        self.authority2 = self.create_authority('Test2')
        self.name_type = self.create_name_type('regular')
        self.language1 = self.create_language('English', 'en')
        self.language2 = self.create_language('Arabic', 'ar')
        self.script1 = self.create_script('Latin', 'Latn', ' ')
        self.script2 = self.create_script('Arabic', 'Arab', ' ')
        self.authority.set_languages([self.language1, self.language2])
        self.authority.set_name_types([self.name_type])
        self.authority.set_scripts([self.script1, self.script2])
        self.authority2.set_languages([self.language1, self.language2])
        self.authority2.set_name_types([self.name_type])
        self.authority2.set_scripts([self.script1, self.script2])
    
    def test_get_preferred_name (self):
        entity = self.tm.create_entity(self.authority)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(preferred_name, None)
        name1 = entity.create_name_property_assertion(
            self.authority, self.name_type, self.language1, self.script1,
            'Name1')
        # With a single name, get_preferred_name will return in that
        # one name regardless of the parameters.
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language2, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script2)
        self.assertEqual(name1, preferred_name)
        # Create a second name, differing from the first in language.
        name2 = entity.create_name_property_assertion(
            self.authority, self.name_type, self.language2, self.script1,
            'Name2')
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language2, self.script1)
        self.assertEqual(name2, preferred_name)
        # Create a third name, differing from the first in authority.
        name3 = entity.create_name_property_assertion(
            self.authority2, self.name_type, self.language1, self.script1,
            'Name3')
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script1)
        self.assertEqual(name3, preferred_name)
        # Authority trumps language.
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language2, self.script1)
        self.assertEqual(name3, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority, self.language1, self.script1)
        self.assertEqual(name1, preferred_name)
        # Create a fourth name, differing from the first in script and
        # authority.
        name4 = entity.create_name_property_assertion(
            self.authority2, self.name_type, self.language2, self.script2,
            'Name4')
        # Script trumps authority.
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script1)
        self.assertEqual(name3, preferred_name)
        preferred_name = entity.get_preferred_name(
            self.authority2, self.language1, self.script2)
        self.assertEqual(name4, preferred_name)
        # Script trumps language.
        preferred_name = entity.get_preferred_name(
            self.authority, self.language2, self.script2)
        self.assertEqual(name4, preferred_name)
