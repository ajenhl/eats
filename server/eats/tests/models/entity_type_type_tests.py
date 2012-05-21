from tmapi.exceptions import TopicInUseException
from eats.models import EntityType
from eats.tests.models.model_test_case import ModelTestCase


class EntityTypeTypeTestCase (ModelTestCase):

    def test_entity_type_admin_name (self):
        entity_type = self.create_entity_type('person')
        self.assertEqual(entity_type.get_admin_name(), 'person')
        entity_type.set_admin_name('place')
        self.assertEqual(entity_type.get_admin_name(), 'place')
        entity_type2 = self.create_entity_type('person')
        self.assertRaises(Exception, entity_type2.set_admin_name, 'place')

    def test_entity_type_delete (self):
        # A name type may not be deleted if it is associated with an
        # authority.
        self.assertEqual(EntityType.objects.count(), 0)
        entity_type = self.create_entity_type('person')
        self.assertEqual(EntityType.objects.count(), 1)        
        authority = self.create_authority('test')
        authority.set_entity_types([entity_type])
        self.assertRaises(TopicInUseException, entity_type.remove)
        self.assertEqual(EntityType.objects.count(), 1)
        authority.set_entity_types([])
        entity_type.remove()
        self.assertEqual(EntityType.objects.count(), 0)
