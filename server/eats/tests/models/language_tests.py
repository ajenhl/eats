from eats.tests.models.model_test_case import ModelTestCase


class LanguageTestCase (ModelTestCase):

    def test_language_admin_name (self):
        language = self.create_language('English', 'en')
        self.assertEqual(language.get_admin_name(), 'English')
        language.set_admin_name('French')
        self.assertEqual(language.get_admin_name(), 'French')
        language2 = self.create_language('Arabic', 'ar')
        self.assertRaises(Exception, language2.set_admin_name, 'French')
    
    def test_language_code (self):
        language = self.create_language('English', 'en')
        self.assertEqual(language.get_code(), 'en')
        language.set_code('eng')
        self.assertEqual(language.get_code(), 'eng')
        language2 = self.create_language('French', 'fr')
        self.assertRaises(Exception, language2.set_code, 'eng')
