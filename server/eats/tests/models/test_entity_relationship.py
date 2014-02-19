from eats.exceptions import EATSValidationException
from eats.models import Entity, EntityRelationshipCache
from eats.tests.models.model_test_case import ModelTestCase


class EntityRelationshipTestCase (ModelTestCase):

    def setUp (self):
        super(EntityRelationshipTestCase, self).setUp()
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
            self.entity2, self.tm.property_assertion_full_certainty)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(assertion.domain_entity, self.entity)
        self.assertEqual(assertion.range_entity, self.entity2)
        self.assertEqual(assertion.entity_relationship_type,
                         self.entity_relationship_type)
        self.assertEqual(assertion.certainty,
                         self.tm.property_assertion_full_certainty)
        fetched_assertion = self.entity.get_entity_relationships()[0]
        self.assertEqual(assertion, fetched_assertion)

    def test_create_illegal_entity_relationship_property_assertion (self):
        # The entity on which the entity relationship is created must
        # be an entity in that relationship.
        self.assertRaises(
            EATSValidationException,
            self.entity.create_entity_relationship_property_assertion,
            self.authority, self.entity_relationship_type, self.entity2,
            self.entity2, self.tm.property_assertion_no_certainty)
        # The entity relationship type must be associated with the
        # authority making the assertion.
        entity_relationship_type = self.create_entity_relationship_type(
            'is related to', 'is related to')
        self.assertRaises(
            EATSValidationException,
            self.entity.create_entity_relationship_property_assertion,
            self.authority, entity_relationship_type, self.entity, self.entity2,
            self.tm.property_assertion_no_certainty)

    def test_delete_entity_relationship_property_assertion (self):
        # Test that both forward and reverse relationships are picked
        # up by get_entity_relationships().
        self.assertEqual(3, Entity.objects.all().count())
        self.assertEqual(0, len(self.entity.get_entity_relationships()))
        self.assertEqual(0, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        assertion1 = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2, self.tm.property_assertion_no_certainty)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        assertion2 = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type2, self.entity,
            self.entity3, self.tm.property_assertion_full_certainty)
        self.assertEqual(2, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(1, len(self.entity3.get_entity_relationships()))
        assertion2.remove()
        self.assertEqual(3, Entity.objects.all().count())
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        assertion1.remove()
        self.assertEqual(3, Entity.objects.all().count())
        self.assertEqual(0, len(self.entity.get_entity_relationships()))
        self.assertEqual(0, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))

    def test_update_entity_relationship_property_assertion (self):
        assertion = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2, self.tm.property_assertion_full_certainty)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(1, len(self.entity2.get_entity_relationships()))
        self.assertEqual(0, len(self.entity3.get_entity_relationships()))
        self.assertEqual(assertion.domain_entity, self.entity)
        self.assertEqual(assertion.range_entity, self.entity2)
        self.assertEqual(assertion.entity_relationship_type,
                         self.entity_relationship_type)
        self.assertEqual(assertion.certainty,
                         self.tm.property_assertion_full_certainty)
        assertion.update(self.entity_relationship_type2, self.entity3,
                         self.entity, self.tm.property_assertion_no_certainty)
        self.assertEqual(1, len(self.entity.get_entity_relationships()))
        self.assertEqual(0, len(self.entity2.get_entity_relationships()))
        self.assertEqual(1, len(self.entity3.get_entity_relationships()))
        self.assertEqual(assertion.domain_entity, self.entity3)
        self.assertEqual(assertion.range_entity, self.entity)
        self.assertEqual(assertion.entity_relationship_type,
                         self.entity_relationship_type2)
        self.assertEqual(assertion.certainty,
                         self.tm.property_assertion_no_certainty)

    def test_illegal_update_entity_relationship_property_assertion (self):
        assertion = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2, self.tm.property_assertion_full_certainty)
        entity4 = self.tm.create_entity(self.authority)
        self.assertRaises(EATSValidationException, assertion.update,
                          self.entity_relationship_type2, self.entity3,
                          entity4, self.tm.property_assertion_full_certainty)
        # The entity relationship type must be associated with the
        # authority making the assertion.
        entity_relationship_type = self.create_entity_relationship_type(
            'is related to', 'is related to')
        self.assertRaises(EATSValidationException, assertion.update,
                          entity_relationship_type, self.entity, self.entity2,
                          self.tm.property_assertion_full_certainty)

    def test_relationship_cache(self):
        cache = EntityRelationshipCache.objects.filter(
            domain_entity=self.entity)
        self.assertEqual(0, cache.count())

        assertion = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2, self.tm.property_assertion_full_certainty)
        cache = EntityRelationshipCache.objects.filter(
            domain_entity=self.entity)
        self.assertEqual(1, cache.count())
        self.assertEqual(self.entity, cache[0].domain_entity)
        self.assertEqual(self.entity2, cache[0].range_entity)
        self.assertEqual(self.entity_relationship_type,
                         cache[0].relationship_type)

        cache = EntityRelationshipCache.objects.filter(
            range_entity=self.entity2)
        self.assertEqual(1, cache.count())
        self.assertEqual(self.entity, cache[0].domain_entity)
        self.assertEqual(self.entity2, cache[0].range_entity)
        self.assertEqual(self.entity_relationship_type,
                         cache[0].relationship_type)

        assertion.update(self.entity_relationship_type2, self.entity,
                         self.entity3, self.tm.property_assertion_no_certainty)
        cache = EntityRelationshipCache.objects.filter(
            domain_entity=self.entity)
        self.assertEqual(1, cache.count())
        self.assertEqual(self.entity, cache[0].domain_entity)
        self.assertEqual(self.entity3, cache[0].range_entity)
        self.assertEqual(self.entity_relationship_type2,
                         cache[0].relationship_type)

        assertion2 = self.entity.create_entity_relationship_property_assertion(
            self.authority, self.entity_relationship_type, self.entity,
            self.entity2, self.tm.property_assertion_full_certainty)
        cache = EntityRelationshipCache.objects.filter(
            domain_entity=self.entity)
        self.assertEqual(2, cache.count())

        assertion2.remove()
        cache = EntityRelationshipCache.objects.filter(
            domain_entity=self.entity)
        self.assertEqual(1, cache.count())
