from eats.tests.base_test_case import BaseTestCase


class EntityTypeTest (BaseTestCase):

    def setUp (self):
        super(EntityTypeTest, self).setUp()
        self.entity = self.tm.create_entity(self.authority)
        self.entity_type = self.create_entity_type('Person')
        self.entity_type2 = self.create_entity_type('Place')
        
    def test_create_entity_type_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_entity_types()))
        assertion = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type)
        self.assertEqual(1, len(self.entity.get_entity_types()))
        self.assertEqual(self.entity_type,
                         self.entity.get_entity_type(assertion))

    def test_delete_entity_type_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_entity_types()))
        assertion1 = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type)
        self.assertEqual(1, len(self.entity.get_entity_types()))
        assertion2 = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type2)
        self.assertEqual(2, len(self.entity.get_entity_types()))
        self.entity.delete_entity_type_property_assertion(assertion2)
        self.assertEqual(1, len(self.entity.get_entity_types()))
        self.entity.delete_entity_type_property_assertion(assertion1)
        self.assertEqual(0, len(self.entity.get_entity_types()))

    def test_update_entity_type_property_assertion (self):
        assertion = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type)
        self.assertEqual(self.authority, self.entity.get_authority(assertion))
        self.assertEqual(self.entity_type,
                         self.entity.get_entity_type(assertion))
        authority2 = self.create_authority('Authority2')
        self.entity.update_entity_type_property_assertion(
            authority2, assertion, self.entity_type2)
        self.assertEqual(authority2, self.entity.get_authority(assertion))
        self.assertEqual(self.entity_type2,
                         self.entity.get_entity_type(assertion))
        
