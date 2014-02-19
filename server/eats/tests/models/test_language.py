from tmapi.exceptions import TopicInUseException
from eats.models import Language
from eats.tests.models.model_test_case import ModelTransactionTestCase


class LanguageTestCase (ModelTransactionTestCase):

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

    def test_language_delete (self):
        self.assertEqual(Language.objects.count(), 0)
        authority = self.create_authority('test')
        language = self.create_language('English', 'en')
        name_part_type = self.create_name_part_type('given')
        language.name_part_types = [name_part_type]
        self.assertEqual(Language.objects.count(), 1)
        authority.set_languages([language])
        self.assertRaises(TopicInUseException, language.remove)
        self.assertEqual(Language.objects.count(), 1)
        self.assertEqual(language.name_part_types, [name_part_type])
        authority.set_languages([])
        language.remove()
        self.assertEqual(Language.objects.count(), 0)
        # A language being associated with a name part type should not
        # prevent the language being removed.
        language = self.create_language('English', 'en')
        language.name_part_types = [name_part_type]
        language.remove()
        self.assertEqual(Language.objects.count(), 0)

    def test_language_name_part_types (self):
        language = self.create_language('English', 'en')
        self.assertEqual(language.name_part_types, [])
        name_part_type1 = self.create_name_part_type('given')
        name_part_type2 = self.create_name_part_type('family')
        name_part_type3 = self.create_name_part_type('terms of address')
        language.name_part_types = [name_part_type1, name_part_type2]
        self.assertEqual(language.name_part_types, [name_part_type1,
                                                    name_part_type2])
        language.name_part_types = [name_part_type2, name_part_type3]
        self.assertEqual(language.name_part_types, [name_part_type2,
                                                    name_part_type3])
        self.assertEqual(len(name_part_type1.get_occurrences(
                    self.tm.language_code_type)), 0)
