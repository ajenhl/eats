from eats.exceptions import EATSValidationException
from eats.tests.models.model_test_case import ModelTestCase


class EntityRelationshipTest (ModelTestCase):

    def setUp (self):
        super(EntityRelationshipTest, self).setUp()
        self.entity = self.tm.create_entity(self.authority)
        self.entity2 = self.tm.create_entity(self.authority)
        self.entity3 = self.tm.create_entity(self.authority)
        self.entity_relationship_type = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        self.entity_relationship_type2 = self.create_entity_relationship_type(
            'is born in', 'is place of birth of')
        self.authority.set_entity_relationship_types(
            [self.entity_relationship_type, self.entity_relationship_type2])
    
    def test_create_entity_relationship_property_assertion (self):
        self.assertEqual(0, len(self.entity.get_entity_relationships()))
        self.assertEqual(0, len(self.entity2.get_entity_relationships()))
        assertion = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(assertion.domain_entity, self.entity)
        self.assertEqual(assertion.range_entity, self.entity2)
        self.assertEqual(assertion.entity_relationship_type,
                         self.entity_relationship_type)
        fetched_assertion = self.entity.get_entity_relationships()[0]
        self.assertEqual(assertion, fetched_assertion)

    def test_create_illegal_entity_relationship_property_assertion (self):
        # The entity on which the entity relationship is created must
        # be an entity in that relationship.
        self.assertRaises(
            EATSValidationException,
            self.entity.create_entity_relationship_property_assertion,
            self.authority, self.entity_relationship_type, self.entity2,
            self.entity2)
        # The entity relationship type must be associated with the
        # authority making the assertion.
        entity_relationship_type = self.create_entity_relationship_type(
            'is related to', 'is related to')
        self.assertRaises(
            EATSValidationException,
            self.entity.create_entity_relationship_property_assertion,
            self.authority, entity_relationship_type, self.entity, self.entity2)

    def test_delete_entity_relationship_property_assertion (self):
        # Test that both forward and reverse relationships are picked
        # up by get_entity_relationships().
        self.assertEqual(0, len(self.entity.get_entity_relationships()))
        self.assertEqual(0, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        assertion1 = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        assertion2 = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type2, self.entity,
            self.entity3)
        self.assertEqual(2, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(1, len(self.entity3.get_entity_relationships()))
        assertion2.remove()
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        assertion1.remove()
        self.assertEqual(0, len(self.entity.get_entity_relationships()))
        self.assertEqual(0, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))

    def test_update_entity_relationship_property_assertion (self):
        assertion = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        self.assertEqual(assertion.domain_entity, self.entity)
        self.assertEqual(assertion.range_entity, self.entity2)
        self.assertEqual(assertion.entity_relationship_type,
                         self.entity_relationship_type)
        assertion.update(self.entity_relationship_type2, self.entity3,
                         self.entity)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(0, len(self.entity2.get_entity_relationships()))
        self.assertEqual(1, len(self.entity3.get_entity_relationships()))
        self.assertEqual(assertion.domain_entity, self.entity3)
        self.assertEqual(assertion.range_entity, self.entity)
        self.assertEqual(assertion.entity_relationship_type,
                         self.entity_relationship_type2)

    def test_illegal_update_entity_relationship_property_assertion (self):
        assertion = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2)
        entity4 = self.tm.create_entity(self.authority)
        self.assertRaises(EATSValidationException, assertion.update,
                          self.entity_relationship_type2, self.entity3,
                          entity4)
        # The entity relationship type must be associated with the
        # authority making the assertion.
        entity_relationship_type = self.create_entity_relationship_type(
            'is related to', 'is related to')
        self.assertRaises(EATSValidationException, assertion.update,
            entity_relationship_type, self.entity, self.entity2)
