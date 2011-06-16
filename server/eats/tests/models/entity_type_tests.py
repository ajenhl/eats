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
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(self.entity_type, assertion.entity_type)

    def test_delete_entity_type_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_entity_types()))
        assertion1 = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type)
        self.assertEqual(1, len(self.entity.get_entity_types()))
        assertion2 = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type2)
        self.assertEqual(2, len(self.entity.get_entity_types()))
        assertion2.remove()
        self.assertEqual(1, len(self.entity.get_entity_types()))
        assertion1.remove()
        self.assertEqual(0, len(self.entity.get_entity_types()))

    def test_update_entity_type_property_assertion (self):
        assertion = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type)
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(self.entity_type, assertion.entity_type)
        authority2 = self.create_authority('Authority2')
        assertion.update(authority2, self.entity_type2)
        self.assertEqual(authority2, assertion.authority)
        self.assertEqual(self.entity_type2, assertion.entity_type)
        
