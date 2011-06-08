from tmapi.indices.type_instance_index import TypeInstanceIndex

from edit_test_case import EditTestCase


class NameTest (EditTestCase):

    def setUp (self):
        super(NameTest, self).setUp()
        self.entity = self.tm.create_entity(self.authority)
        self.name_type = self.create_name_type('test')
        self.language = self.create_language('English', 'en')
        self.language2 = self.create_language('Arabic', 'ar')
        self.script = self.create_script('Latin', 'Latn')
        self.script2 = self.create_script('Arabic', 'Arab')
        self.type_index = self.tm.get_index(TypeInstanceIndex)
        self.type_index.open()
    
    def test_create_name_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_eats_names()))
        self.assertEqual(0, self.type_index.get_associations(
                self.tm.is_in_language_type).count())
        self.assertEqual(0, self.type_index.get_associations(
                self.tm.is_in_script_type).count())        
        name_assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        self.assertEqual(1, len(self.entity.get_eats_names()))
        self.assertEqual(1, self.type_index.get_associations(
                self.tm.is_in_language_type).count())
        self.assertEqual(1, self.type_index.get_associations(
                self.tm.is_in_script_type).count())
        name = self.entity.get_entity_name(name_assertion).get_eats_name()
        self.assertEqual(name.get_value(), 'Name')
        self.assertEqual(name.get_type(), self.name_type)

    def test_delete_name_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_eats_names()))
        name1_assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name1')
        self.assertEqual(1, len(self.entity.get_eats_names()))
        name2_assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name2')
        self.assertEqual(2, len(self.entity.get_eats_names()))
        self.entity.delete_name_property_assertion(name2_assertion)
        self.assertEqual(1, len(self.entity.get_eats_names()))
        name1 = self.entity.get_entity_name(name1_assertion).get_eats_name()
        self.assertEqual(name1.get_value(), 'Name1')
        self.entity.delete_name_property_assertion(name1_assertion)
        self.assertEqual(0, len(self.entity.get_eats_names()))

    def test_name_language (self):
        name_assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        name_topic = self.entity.get_entity_name(name_assertion)
        self.assertEqual(self.language, name_topic.name_language)
        name_topic.name_language = self.language2
        self.assertEqual(self.language2, name_topic.name_language)
        
    def test_name_script (self):
        name_assertion = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Name')
        name_topic = self.entity.get_entity_name(name_assertion)
        self.assertEqual(self.script, name_topic.name_script)
        name_topic.name_script = self.script2
        self.assertEqual(self.script2, name_topic.name_script)
