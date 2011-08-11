from eats.models import Authority, Calendar, DatePeriod, DateType, EntityRelationshipType, EntityType, Language, NameType, Script
from eats.tests.models.model_test_case import ModelTestCase


class EATSTopicMapTestCase (ModelTestCase):

    def test_create_authority (self):
        self.assertEqual(Authority.objects.count(), 1)
        authority1 = self.tm.create_authority('Test1')
        self.assertEqual(Authority.objects.count(), 2)
        self.assertTrue(authority1 in Authority.objects.all())
        self.assertRaises(Exception, self.tm.create_authority, 'Test1')

    def test_create_calendar (self):
        self.assertEqual(Calendar.objects.count(), 0)
        calendar = self.tm.create_calendar('Test')
        self.assertEqual(Calendar.objects.count(), 1)
        self.assertTrue(calendar in Calendar.objects.all())
        self.assertRaises(Exception, self.tm.create_calendar, 'Test')
        self.assertEqual(Calendar.objects.count(), 1)
        self.assertTrue(calendar in Calendar.objects.all())
        
    def test_create_date_period (self):
        self.assertEqual(DatePeriod.objects.count(), 0)
        date_period = self.tm.create_date_period('Test')
        self.assertEqual(DatePeriod.objects.count(), 1)
        self.assertTrue(date_period in DatePeriod.objects.all())
        self.assertRaises(Exception, self.tm.create_date_period, 'Test')
        self.assertEqual(DatePeriod.objects.count(), 1)
        self.assertTrue(date_period in DatePeriod.objects.all())
        
    def test_create_date_type (self):
        self.assertEqual(DateType.objects.count(), 0)
        date_type = self.tm.create_date_type('Test')
        self.assertEqual(DateType.objects.count(), 1)
        self.assertTrue(date_type in DateType.objects.all())
        self.assertRaises(Exception, self.tm.create_date_type, 'Test')
        self.assertEqual(DateType.objects.count(), 1)
        self.assertTrue(date_type in DateType.objects.all())
        
    def test_create_entity_relationship_type (self):
        self.assertEqual(EntityRelationshipType.objects.count(), 0)
        er_type = self.tm.create_entity_relationship_type('Forward', 'Reverse')
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        self.assertTrue(er_type in EntityRelationshipType.objects.all())
        self.assertRaises(Exception, self.tm.create_entity_relationship_type,
                          'Forward', 'Reverse')
        self.assertEqual(EntityRelationshipType.objects.count(), 1)
        self.assertTrue(er_type in EntityRelationshipType.objects.all())
        er_type2 = self.tm.create_entity_relationship_type(
            'Forward', 'Reverse2')
        self.assertEqual(EntityRelationshipType.objects.count(), 2)
        self.assertTrue(er_type in EntityRelationshipType.objects.all())
        self.assertTrue(er_type2 in EntityRelationshipType.objects.all())
        er_type3 = self.tm.create_entity_relationship_type(
            'Forward2', 'Reverse')
        self.assertEqual(EntityRelationshipType.objects.count(), 3)
        self.assertTrue(er_type in EntityRelationshipType.objects.all())
        self.assertTrue(er_type2 in EntityRelationshipType.objects.all())
        self.assertTrue(er_type3 in EntityRelationshipType.objects.all())

    def test_create_entity_type (self):
        self.assertEqual(EntityType.objects.count(), 0)
        entity_type = self.tm.create_entity_type('Test')
        self.assertEqual(EntityType.objects.count(), 1)
        self.assertTrue(entity_type in EntityType.objects.all())
        self.assertRaises(Exception, self.tm.create_entity_type, 'Test')
        self.assertEqual(EntityType.objects.count(), 1)
        self.assertTrue(entity_type in EntityType.objects.all())
        
    def test_create_language (self):
        self.assertEqual(Language.objects.count(), 0)
        language = self.tm.create_language('English', 'en')
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())
        self.assertRaises(Exception, self.tm.create_language, 'English', 'fr')
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())
        self.assertEqual(language.get_code(), 'en')
        self.assertRaises(Exception, self.tm.create_language, 'French', 'en')
        self.assertEqual(Language.objects.count(), 1)
        self.assertTrue(language in Language.objects.all())
        self.assertEqual(language.get_admin_name(), 'English')

    def test_create_name_type (self):
        self.assertEqual(NameType.objects.count(), 0)
        name_type = self.tm.create_name_type('Test')
        self.assertEqual(NameType.objects.count(), 1)
        self.assertTrue(name_type in NameType.objects.all())
        self.assertRaises(Exception, self.tm.create_name_type, 'Test')
        self.assertEqual(NameType.objects.count(), 1)
        self.assertTrue(name_type in NameType.objects.all())
        
    def test_create_script (self):
        self.assertEqual(Script.objects.count(), 0)
        script = self.tm.create_script('Latin', 'Latn', ' ')
        self.assertEqual(Script.objects.count(), 1)
        self.assertTrue(script in Script.objects.all())
        self.assertRaises(Exception, self.tm.create_script, 'Latin', 'Arab', '')
        self.assertEqual(Script.objects.count(), 1)
        self.assertTrue(script in Script.objects.all())
        self.assertEqual(script.get_code(), 'Latn')
        self.assertRaises(Exception, self.tm.create_script, 'Arabic', 'Latn',
                          ' ')
        self.assertEqual(Script.objects.count(), 1)
        self.assertTrue(script in Script.objects.all())
        self.assertEqual(script.get_admin_name(), 'Latin')
