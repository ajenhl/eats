from django.test import TestCase

from eats.lib.property_assertions import NamePropertyAssertions
from eats.tests.base_test_case import BaseTestCase


class PropertyAssertionsTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(PropertyAssertionsTestCase, self).setUp()
        self.reset_managers()
        self.tm = self.create_topic_map()
        self.authority1 = self.create_authority('Test 1')
        self.authority2 = self.create_authority('Test 2')
        admin_user = self.create_django_user('admin', 'admin@example.org',
                                             'password')
        self.admin = self.create_user(admin_user)

    def test_names_editable (self):
        entity = self.tm.create_entity(self.authority1)
        language = self.tm.create_language('English', 'en')
        name_type = self.tm.create_name_type('regular')
        script = self.tm.create_script('Latin', 'Latn', ' ')
        self.authority1.set_languages([language])
        self.authority1.set_name_types([name_type])
        self.authority1.set_scripts([script])
        self.authority2.set_languages([language])
        self.authority2.set_name_types([name_type])
        self.authority2.set_scripts([script])
        assertion1 = entity.create_name_property_assertion(
            self.authority1, name_type, language, script, 'Name', True)
        names = NamePropertyAssertions(self.tm, entity, self.authority1, None)
        self.assertTrue(assertion1 in names.editable)
        self.assertFalse(assertion1 in names.non_editable)
        names = NamePropertyAssertions(self.tm, entity, self.authority2, None)
        self.assertFalse(assertion1 in names.editable)
        self.assertTrue(assertion1 in names.non_editable)
        assertion2 = entity.create_name_property_assertion(
            self.authority2, name_type, language, script, 'Name', True)
        names = NamePropertyAssertions(self.tm, entity, self.authority1, None)
        self.assertTrue(assertion1 in names.editable)
        self.assertFalse(assertion2 in names.editable)
        self.assertFalse(assertion1 in names.non_editable)
        self.assertTrue(assertion2 in names.non_editable)
        names = NamePropertyAssertions(self.tm, entity, self.authority2, None)
        self.assertFalse(assertion1 in names.editable)
        self.assertTrue(assertion2 in names.editable)
        self.assertTrue(assertion1 in names.non_editable)
        self.assertFalse(assertion2 in names.non_editable)
