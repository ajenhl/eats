from tmapi.indices.type_instance_index import TypeInstanceIndex

from eats.exceptions import EATSValidationException
from eats.models import NameIndex, NamePart
from eats.tests.models.model_test_case import ModelTestCase


class NameTestCase (ModelTestCase):

    def setUp (self):
        super(NameTestCase, self).setUp()
        self.entity = self.tm.create_entity(self.authority)
        self.name_type = self.create_name_type('regular')
        self.name_type2 = self.create_name_type('irregular')
        self.language = self.create_language('English', 'en')
        self.language2 = self.create_language('Arabic', 'ar')
        self.script = self.create_script('Latin', 'Latn')
        self.script2 = self.create_script('Arabic', 'Arab')
        self.authority.set_languages([self.language, self.language2])
        self.authority.set_name_types([self.name_type, self.name_type2])
        self.authority.set_scripts([self.script, self.script2])
        self.type_index = self.tm.get_index(TypeInstanceIndex)
        self.type_index.open()

    def test_illegal_create_name_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_eats_names()))
        language = self.create_language('French', 'fr')
        name_type = self.create_name_type('pseudonym')
        script = self.create_script('Gujarati', 'Gujr')
        self.assertRaises(EATSValidationException,
                          self.entity.create_name_property_assertion,
                          self.authority, name_type, self.language, self.script,
                          'Name')
        self.assertEqual(0, len(self.entity.get_eats_names()))
        self.assertRaises(EATSValidationException,
                          self.entity.create_name_property_assertion,
                          self.authority, self.name_type, language, self.script,
                          'Name')
        self.assertEqual(0, len(self.entity.get_eats_names()))
        self.assertRaises(EATSValidationException,
                          self.entity.create_name_property_assertion,
                          self.authority, self.name_type, self.language, script,
                          'Name')
        self.assertEqual(0, len(self.entity.get_eats_names()))
    
    def test_create_name_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_eats_names()))
        self.assertEqual(0, self.type_index.get_associations(
                self.tm.is_in_language_type).count())
        self.assertEqual(0, self.type_index.get_associations(
                self.tm.is_in_script_type).count())        
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        self.assertEqual(1, len(self.entity.get_eats_names()))
        self.assertEqual(1, self.type_index.get_associations(
                self.tm.is_in_language_type).count())
        self.assertEqual(1, self.type_index.get_associations(
                self.tm.is_in_script_type).count())
        fetched_assertion = self.entity.get_eats_names()[0]
        self.assertEqual(assertion, fetched_assertion)
        name = assertion.name
        self.assertEqual(name.display_form, 'Name')
        self.assertEqual(name.name_type, self.name_type)

    def test_delete_name_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_eats_names()))
        assertion1 = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name1')
        self.assertEqual(1, len(self.entity.get_eats_names()))
        self.assertEqual(0, NamePart.objects.count())
        assertion2 = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name2')
        self.assertEqual(2, len(self.entity.get_eats_names()))
        self.assertEqual(2, self.type_index.get_associations(
                self.tm.is_in_language_type).count())
        self.assertEqual(2, self.type_index.get_associations(
                self.tm.is_in_script_type).count())
        name_part_type = self.create_name_part_type('given')
        assertion2.name.create_name_part(name_part_type, self.language,
                                         self.script, 'Part', 1)
        self.assertEqual(1, NamePart.objects.count())
        assertion2.remove()
        self.assertEqual(1, len(self.entity.get_eats_names()))
        self.assertEqual(1, self.type_index.get_associations(
                self.tm.is_in_language_type).count())
        self.assertEqual(1, self.type_index.get_associations(
                self.tm.is_in_script_type).count())
        self.assertEqual(0, NamePart.objects.count())
        name1 = assertion1.name
        self.assertEqual(name1.display_form, 'Name1')
        assertion1.remove()
        self.assertEqual(0, len(self.entity.get_eats_names()))
        self.assertEqual(0, self.type_index.get_associations(
                self.tm.is_in_language_type).count())
        self.assertEqual(0, self.type_index.get_associations(
                self.tm.is_in_script_type).count())

    def test_illegal_update_name_property_assertion (self):
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        name = assertion.name
        language = self.create_language('French', 'fr')
        name_type = self.create_name_type('pseudonym')
        script = self.create_script('Gujarati', 'Gujr')
        self.assertRaises(EATSValidationException, assertion.update, name_type,
                          self.language, self.script, 'Name')
        self.assertEqual(name.name_type, self.name_type)
        self.assertRaises(EATSValidationException, assertion.update,
                          self.name_type, language, self.script, 'Name')
        self.assertEqual(name.language, self.language)
        self.assertRaises(EATSValidationException, assertion.update,
                          self.name_type, self.language, script, 'Name')
        self.assertEqual(name.script, self.script)

    def test_update_name_property_assertion (self):
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        name = assertion.name
        self.assertEqual(assertion.authority, self.authority)
        self.assertEqual(name.name_type, self.name_type)
        self.assertEqual(name.language, self.language)
        self.assertEqual(name.script, self.script)
        self.assertEqual(name.display_form, 'Name')
        assertion.update(self.name_type2, self.language2,
            self.script2, 'Name2')
        self.assertEqual(name.name_type, self.name_type2)
        self.assertEqual(name.language, self.language2)
        self.assertEqual(name.script, self.script2)
        self.assertEqual(name.display_form, 'Name2')        
        
    def test_language (self):
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        name = assertion.name
        self.assertEqual(self.language, name.language)
        name.language = self.language2
        self.assertEqual(self.language2, name.language)
        
    def test_script (self):
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        name = assertion.name
        self.assertEqual(self.script, name.script)
        name.script = self.script2
        self.assertEqual(self.script2, name.script)

    def test_name_type (self):
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        name = assertion.name
        self.assertEqual(name.name_type, self.name_type)
        name.name_type = self.name_type2
        self.assertEqual(name.name_type, self.name_type2)
        
    def test_display_form (self):
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name1')
        name = assertion.name
        self.assertEqual(name.display_form, 'Name1')
        name.display_form = 'Name2'
        self.assertEqual(name.display_form, 'Name2')

    def test_name_index (self):
        assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            '')
        name = assertion.name
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 0)
        name.display_form = 'Name'
        name.update_name_index()
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 1)
        self.assertEqual(index_items[0].form, 'Name')
        name.display_form = 'Carl Philipp Emanuel Bach'
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 1)
        self.assertEqual(index_items[0].form, 'Name')
        name.update_name_index()
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 4)
        indexed_names = set([item.form for item in index_items])
        self.assertEqual(indexed_names, set(['Carl', 'Philipp', 'Emanuel',
                                             'Bach']))
        assertion2 = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name2')
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 5)
        assertion2.remove()
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 4)
        indexed_names = set([item.form for item in index_items])
        self.assertEqual(indexed_names, set(['Carl', 'Philipp', 'Emanuel',
                                             'Bach']))
