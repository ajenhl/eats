from eats.tests.base_test_case import BaseTestCase


class LanguageTestCase (BaseTestCase):

    def test_language_admin_name (self):
        language = self.create_language('English', 'en')
        self.assertEqual(language.get_admin_name(), 'English')
        language.set_admin_name('French')
        self.assertEqual(language.get_admin_name(), 'French')
    
    def test_language_code (self):
        language = self.create_language('English', 'en')
        self.assertEqual(language.get_code(), 'en')
        language.set_code('eng')
        self.assertEqual(language.get_code(), 'eng')
