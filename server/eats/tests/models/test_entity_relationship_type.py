from tmapi.exceptions import TopicInUseException
from eats.models import EntityRelationshipType
from eats.tests.models.model_test_case import ModelTestCase


class EntityRelationshipTypeTestCase (ModelTestCase):

    def test_entity_relationship_type_admin_name (self):
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        self.assertEqual(er_type.get_admin_name(), 'Forward / Reverse')
        er_type.set_admin_name('Forward2', 'Reverse2')
        self.assertEqual(er_type.get_admin_name(), 'Forward2 / Reverse2')
        er_type.set_admin_name('Forward2', 'Reverse2')
        self.assertEqual(er_type.get_admin_name(), 'Forward2 / Reverse2')

    def test_entity_relationship_type_delete (self):
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        authority = self.create_authority('test')
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        authority.set_entity_relationship_types([er_type])
        self.assertRaises(TopicInUseException, er_type.remove)
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        authority.set_entity_relationship_types([])
        er_type.remove()
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
    
    def test_entity_relationship_type_forward_name (self):
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        self.assertEqual(er_type.get_admin_forward_name(), 'Forward')
        er_type.set_admin_name('Forward2', 'Reverse')
        self.assertEqual(er_type.get_admin_forward_name(), 'Forward2')
        er_type2 = self.create_entity_relationship_type('Test', 'Reverse')
        self.assertRaises(Exception, er_type2.set_admin_name, 'Forward2',
                          'Reverse')

    def test_entity_relationship_type_reverse_name (self):
        er_type = self.create_entity_relationship_type('Forward', 'Reverse')
        self.assertEqual(er_type.get_admin_reverse_name(), 'Reverse')
        er_type.set_admin_name('Forward', 'Reverse2')
        self.assertEqual(er_type.get_admin_reverse_name(), 'Reverse2')
        er_type2 = self.create_entity_relationship_type('Forward', 'Test2')
        self.assertRaises(Exception, er_type2.set_admin_name, 'Forward',
                          'Reverse2')
