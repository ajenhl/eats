from eats.tests.base_test_case import BaseTestCase


class AuthorityTest (BaseTestCase):

    def test_get_calendars (self):
        self.assertEqual(0, len(self.authority.get_calendars()))
        calendar1 = self.create_calendar('Gregorian')
        self.authority.set_calendars([calendar1])
        self.assertEqual(1, len(self.authority.get_calendars()))
        self.assertTrue(calendar1 in self.authority.get_calendars())
        calendar2 = self.create_calendar('Julian')
        self.authority.set_calendars([calendar1, calendar2])
        self.assertEqual(2, len(self.authority.get_calendars()))
        self.assertTrue(calendar1 in self.authority.get_calendars())
        self.assertTrue(calendar2 in self.authority.get_calendars())
        self.authority.set_calendars([calendar2])
        self.assertEqual(1, len(self.authority.get_calendars()))
        self.assertTrue(calendar2 in self.authority.get_calendars())
        self.authority.set_calendars([])
        self.assertEqual(0, len(self.authority.get_calendars()))

    def test_get_date_periods (self):
        self.assertEqual(0, len(self.authority.get_date_periods()))
        period1 = self.create_date_period('lifespan')
        self.authority.set_date_periods([period1])
        self.assertEqual(1, len(self.authority.get_date_periods()))
        self.assertTrue(period1 in self.authority.get_date_periods())
        period2 = self.create_date_period('floruit')
        self.authority.set_date_periods([period1, period2])
        self.assertEqual(2, len(self.authority.get_date_periods()))
        self.assertTrue(period1 in self.authority.get_date_periods())
        self.assertTrue(period2 in self.authority.get_date_periods())
        self.authority.set_date_periods([period2])
        self.assertEqual(1, len(self.authority.get_date_periods()))
        self.assertTrue(period2 in self.authority.get_date_periods())
        self.authority.set_date_periods([])
        self.assertEqual(0, len(self.authority.get_date_periods()))

    def test_get_date_types (self):
        self.assertEqual(0, len(self.authority.get_date_types()))
        date_type1 = self.create_date_type('exact')
        self.authority.set_date_types([date_type1])
        self.assertEqual(1, len(self.authority.get_date_types()))
        self.assertTrue(date_type1 in self.authority.get_date_types())
        date_type2 = self.create_date_type('circa')
        self.authority.set_date_types([date_type1, date_type2])
        self.assertEqual(2, len(self.authority.get_date_types()))
        self.assertTrue(date_type1 in self.authority.get_date_types())
        self.assertTrue(date_type2 in self.authority.get_date_types())
        self.authority.set_date_types([date_type2])
        self.assertEqual(1, len(self.authority.get_date_types()))
        self.assertTrue(date_type2 in self.authority.get_date_types())
        self.authority.set_date_types([])
        self.assertEqual(0, len(self.authority.get_date_types()))

    def test_get_entity_types (self):
        self.assertEqual(0, len(self.authority.get_entity_types()))
        entity_type1 = self.create_entity_type('person')
        self.authority.set_entity_types([entity_type1])
        self.assertEqual(1, len(self.authority.get_entity_types()))
        self.assertTrue(entity_type1 in self.authority.get_entity_types())
        entity_type2 = self.create_entity_type('place')
        self.authority.set_entity_types([entity_type1, entity_type2])
        self.assertEqual(2, len(self.authority.get_entity_types()))
        self.assertTrue(entity_type1 in self.authority.get_entity_types())
        self.assertTrue(entity_type2 in self.authority.get_entity_types())
        self.authority.set_entity_types([entity_type2])
        self.assertEqual(1, len(self.authority.get_entity_types()))
        self.assertTrue(entity_type2 in self.authority.get_entity_types())
        self.authority.set_entity_types([])
        self.assertEqual(0, len(self.authority.get_entity_types()))

    def test_get_entity_relationship_types (self):
        self.assertEqual(0, len(self.authority.get_entity_relationship_types()))
        type1 = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        self.authority.set_entity_relationship_types([type1])
        self.assertEqual(1, len(self.authority.get_entity_relationship_types()))
        self.assertTrue(type1 in self.authority.get_entity_relationship_types())
        type2 = self.create_entity_relationship_type(
            'is born in', 'is place of birth of')
        self.authority.set_entity_relationship_types([type1, type2])
        self.assertEqual(2, len(self.authority.get_entity_relationship_types()))
        self.assertTrue(type1 in self.authority.get_entity_relationship_types())
        self.assertTrue(type2 in self.authority.get_entity_relationship_types())
        self.authority.set_entity_relationship_types([type2])
        self.assertEqual(1, len(self.authority.get_entity_relationship_types()))
        self.assertTrue(type2 in self.authority.get_entity_relationship_types())
        self.authority.set_entity_relationship_types([])
        self.assertEqual(0, len(self.authority.get_entity_relationship_types()))
        
    def test_get_languages (self):
        self.assertEqual(0, len(self.authority.get_languages()))
        language1 = self.create_language('English', 'en')
        self.authority.set_languages([language1])
        self.assertEqual(1, len(self.authority.get_languages()))
        self.assertTrue(language1 in self.authority.get_languages())
        language2 = self.create_language('French', 'fr')
        self.authority.set_languages([language1, language2])
        self.assertEqual(2, len(self.authority.get_languages()))
        self.assertTrue(language1 in self.authority.get_languages())
        self.assertTrue(language2 in self.authority.get_languages())
        self.authority.set_languages([language2])
        self.assertEqual(1, len(self.authority.get_languages()))
        self.assertTrue(language2 in self.authority.get_languages())
        self.authority.set_languages([])
        self.assertEqual(0, len(self.authority.get_languages()))

    def test_get_name_types (self):
        self.assertEqual(0, len(self.authority.get_name_types()))
        name_type1 = self.create_name_type('regular')
        self.authority.set_name_types([name_type1])
        self.assertEqual(1, len(self.authority.get_name_types()))
        self.assertTrue(name_type1 in self.authority.get_name_types())
        name_type2 = self.create_name_type('pseudonym')
        self.authority.set_name_types([name_type1, name_type2])
        self.assertEqual(2, len(self.authority.get_name_types()))
        self.assertTrue(name_type1 in self.authority.get_name_types())
        self.assertTrue(name_type2 in self.authority.get_name_types())
        self.authority.set_name_types([name_type2])
        self.assertEqual(1, len(self.authority.get_name_types()))
        self.assertTrue(name_type2 in self.authority.get_name_types())
        self.authority.set_name_types([])
        self.assertEqual(0, len(self.authority.get_name_types()))

    def test_get_scripts (self):
        self.assertEqual(0, len(self.authority.get_scripts()))
        script1 = self.create_script('Latin', 'Latn')
        self.authority.set_scripts([script1])
        self.assertEqual(1, len(self.authority.get_scripts()))
        self.assertTrue(script1 in self.authority.get_scripts())
        script2 = self.create_script('Arabic', 'Arab')
        self.authority.set_scripts([script1, script2])
        self.assertEqual(2, len(self.authority.get_scripts()))
        self.assertTrue(script1 in self.authority.get_scripts())
        self.assertTrue(script2 in self.authority.get_scripts())
        self.authority.set_scripts([script2])
        self.assertEqual(1, len(self.authority.get_scripts()))
        self.assertTrue(script2 in self.authority.get_scripts())
        self.authority.set_scripts([])
        self.assertEqual(0, len(self.authority.get_scripts()))