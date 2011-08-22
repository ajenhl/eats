from eats.models import NameIndex
from eats.tests.models.model_test_case import ModelTestCase


class NamePartTestCase (ModelTestCase):

    def setUp (self):
        super(NamePartTestCase, self).setUp()
        self.language = self.create_language('English', 'en')
        self.name_part_type1 = self.create_name_part_type('given')
        self.name_part_type2 = self.create_name_part_type('family')
        self.name_type = self.create_name_type('regular')
        self.script = self.create_script('Latin', 'Latn', ' ')
        self.authority.set_languages([self.language])
        self.authority.set_name_part_types([self.name_part_type1,
                                            self.name_part_type2])
        self.authority.set_name_types([self.name_type])
        self.authority.set_scripts([self.script])
        self.entity = self.tm.create_entity(self.authority)
        self.name_pa = self.entity.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script, '')
        self.name = self.name_pa.name
    
    def test_create_name_part (self):
        self.assertEqual(len(self.name.get_name_parts()), 0)
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        self.assertEqual(len(self.name.get_name_parts().keys()), 1)
        self.assertEqual(self.name.get_name_parts().keys()[0],
                         self.name_part_type1)
        self.assertEqual(len(self.name.get_name_parts().values()), 1)
        self.assertEqual(len(self.name.get_name_parts().values()[0]), 1)
        self.assertEqual(self.name.get_name_parts().values()[0][0], name_part)

    def test_delete_name_part (self):
        self.assertEqual(len(self.name.get_name_parts()), 0)
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        self.assertEqual(len(self.name.get_name_parts()), 1)
        name_part.remove()
        self.assertEqual(len(self.name.get_name_parts()), 0)

    def test_display_form (self):
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        self.assertEqual(name_part.display_form, 'Sam')
        name_part.display_form = 'Jo'
        self.assertEqual(name_part.display_form, 'Jo')
        
    def test_language (self):
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        self.assertEqual(name_part.language, self.language)
        language2 = self.create_language('French', 'fr')
        name_part.language = language2
        self.assertEqual(name_part.language, language2)

    def test_name_part_type (self):
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        self.assertEqual(name_part.name_part_type, self.name_part_type1)
        name_part.name_part_type = self.name_part_type2
        self.assertEqual(name_part.name_part_type, self.name_part_type2)

    def test_order (self):
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        self.assertEqual(name_part.order, 1)
        name_part.order = 2
        self.assertEqual(name_part.order, 2)

    def test_script (self):
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        self.assertEqual(name_part.script, self.script)
        script2 = self.create_script('Arabic', 'Arab', ' ')
        name_part.script = script2
        self.assertEqual(name_part.script, script2)

    def test_name_index (self):
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 0)
        name_part = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Sam', 1)
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 1)
        self.assertEqual(index_items[0].form, 'Sam')
        name_part.display_form = 'Sam Marie'
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 1)
        self.assertEqual(index_items[0].form, 'Sam')
        name_part.update_name_index()
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 2)
        indexed_names = set([item.form for item in index_items])
        self.assertEqual(indexed_names, set(['Sam', 'Marie']))
        name_part2 = self.name.create_name_part(
            self.name_part_type1, self.language, self.script, 'Isabel', 2)
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 3)
        name_part2.remove()
        index_items = NameIndex.objects.filter(entity=self.entity)
        self.assertEqual(index_items.count(), 2)
        index_items = NameIndex.objects.filter(entity=self.entity)
        indexed_names = set([item.form for item in index_items])
        self.assertEqual(indexed_names, set(['Sam', 'Marie']))
        # Updating the name's name index should have no effect on the
        # entries relating to the name parts.
        self.name.update_name_index()
        index_items = NameIndex.objects.filter(entity=self.entity)
        indexed_names = set([item.form for item in index_items])
        self.assertEqual(indexed_names, set(['Sam', 'Marie']))
