from django.test import TestCase

from eats.lookups import EntityLookup
from eats.models import Entity
from eats.tests.base_test_case import BaseTestCase


class LookupsTestCase (TestCase, BaseTestCase):

    def setUp (self):
        super(LookupsTestCase, self).setUp()
        self.reset_managers()
        self.tm = self.create_topic_map()
        self.authority = self.create_authority('Test')
        self.name_type = self.create_name_type('regular')
        self.language = self.create_language('English', 'en')
        self.script = self.create_script('Latin', 'Latn', ' ')
        self.authority.set_languages([self.language])
        self.authority.set_name_types([self.name_type])
        self.authority.set_scripts([self.script])

    def test_entity_lookup_get_query (self):
        lookup = EntityLookup()
        self.assertEqual(Entity.objects.count(), 0)
        results = lookup.get_query(None, 'Bac')
        self.assertEqual(len(results), 0)
        entity1 = self.tm.create_entity(self.authority)
        entity1.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'Johann Sebastian Bach')
        self.assertEqual(Entity.objects.count(), 1)
        results = lookup.get_query(None, 'Bac')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], entity1)
        results = lookup.get_query(None, 'J B')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], entity1)
        entity2 = self.tm.create_entity(self.authority)
        entity2.create_name_property_assertion(
            self.authority, self.name_type, self.language, self.script,
            'John Stuart Mill')
        results = lookup.get_query(None, 'Bac')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], entity1)
        results = lookup.get_query(None, 'J B')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0], entity1)
        results = lookup.get_query(None, 'J S')
        self.assertEqual(len(results), 2)
        self.assertTrue(entity1 in results)
        self.assertTrue(entity2 in results)
        results = lookup.get_query(None, 'oh')
        self.assertEqual(len(results), 0)
        results = lookup.get_query(None, 'Mills')
        self.assertEqual(len(results), 0)

    def test_entity_lookup_get_item (self):
        lookup = EntityLookup()
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(lookup.get_item(entity.get_id()), entity)

    def test_entity_lookup_get_item_id (self):
        lookup = EntityLookup()
        entity = self.tm.create_entity(self.authority)
        self.assertEqual(lookup.get_item_id(entity), entity.get_id())
