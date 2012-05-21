from eats.exceptions import EATSValidationException
from eats.tests.models.model_test_case import ModelTestCase


class EntityTypeTestCase (ModelTestCase):

    def setUp (self):
        super(EntityTypeTestCase, self).setUp()
        self.entity = self.tm.create_entity(self.authority)
        self.entity_type = self.create_entity_type('Person')
        self.entity_type2 = self.create_entity_type('Place')
        self.authority.set_entity_types([self.entity_type, self.entity_type2])
        
    def test_create_entity_type_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_entity_types()))
        assertion = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type)
        self.assertEqual(1, len(self.entity.get_entity_types()))
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(self.entity_type, assertion.entity_type)
        fetched_assertion = self.entity.get_entity_types()[0]
        self.assertEqual(assertion, fetched_assertion)

    def test_illegal_create_entity_type_property_assertion (self):
        entity_type = self.create_entity_type('organisation')
        self.assertEqual(0, len(self.entity.get_entity_types()))
        self.assertRaises(EATSValidationException,
                          self.entity.create_entity_type_property_assertion,
                          self.authority, entity_type)
        self.assertEqual(0, len(self.entity.get_entity_types()))

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
        assertion.update(self.entity_type2)
        self.assertEqual(self.entity_type2, assertion.entity_type)
        
    def test_illegal_update_entity_type_property_assertion (self):
        assertion = self.entity.create_entity_type_property_assertion(
            self.authority, self.entity_type)
        self.assertEqual(self.authority, assertion.authority)
        self.assertEqual(self.entity_type, assertion.entity_type)
        entity_type2 = self.create_entity_type('organisation')
        self.assertRaises(EATSValidationException, assertion.update,
                          entity_type2)
