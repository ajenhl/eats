from eats.exceptions import EATSValidationException
from eats.tests.models.model_test_case import ModelTestCase


class AuthorityTestCase (ModelTestCase):

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

    def test_change_calendars (self):
        entity = self.tm.create_entity()
        calendar1 = self.create_calendar('Gregorian')
        calendar2 = self.create_calendar('Julian')
        date_period = self.create_date_period('lifespan')
        date_type = self.create_date_type('exact')
        self.authority.set_calendars([calendar1])
        self.authority.set_date_periods([date_period])
        self.authority.set_date_types([date_type])
        existence = entity.create_existence_property_assertion(self.authority)
        date_data = {'date_period': date_period, 'point': '1 June 2001',
                     'point_calendar': calendar1, 'point_type': date_type,
                     'point_normalised': '2001-06-01',
                     'point_certainty': self.tm.date_full_certainty}
        date = existence.create_date(date_data)
        date_part = date.point
        self.assertRaises(EATSValidationException, self.authority.set_calendars,
                [])
        self.assertTrue(calendar1 in self.authority.get_calendars())
        self.authority.set_calendars([calendar1, calendar2])
        date_part.calendar = calendar2
        self.authority.set_calendars([calendar2])
        self.assertEqual(self.authority.get_calendars().count(), 1)
        self.assertTrue(calendar2 in self.authority.get_calendars())

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

    def test_change_date_periods (self):
        entity = self.tm.create_entity()
        calendar = self.create_calendar('Gregorian')
        date_period1 = self.create_date_period('lifespan')
        date_period2 = self.create_date_period('floruit')
        date_type = self.create_date_type('exact')
        self.authority.set_calendars([calendar])
        self.authority.set_date_periods([date_period1])
        self.authority.set_date_types([date_type])
        existence = entity.create_existence_property_assertion(self.authority)
        date_data = {'date_period': date_period1, 'point': '1 June 2001',
                     'point_calendar': calendar, 'point_type': date_type,
                     'point_normalised': '2001-06-01',
                     'point_certainty': self.tm.date_full_certainty}
        date = existence.create_date(date_data)
        self.assertRaises(EATSValidationException,
                          self.authority.set_date_periods, [])
        self.assertTrue(date_period1 in self.authority.get_date_periods())
        self.authority.set_date_periods([date_period1, date_period2])
        date.period = date_period2
        self.authority.set_date_periods([date_period2])
        self.assertEqual(self.authority.get_date_periods().count(), 1)
        self.assertTrue(date_period2 in self.authority.get_date_periods())

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

    def test_change_date_types (self):
        entity = self.tm.create_entity()
        calendar = self.create_calendar('Gregorian')
        date_period = self.create_date_period('lifespan')
        date_type1 = self.create_date_type('exact')
        date_type2 = self.create_date_type('circa')
        self.authority.set_calendars([calendar])
        self.authority.set_date_periods([date_period])
        self.authority.set_date_types([date_type1])
        existence = entity.create_existence_property_assertion(self.authority)
        date_data = {'date_period': date_period, 'point': '1 June 2001',
                     'point_calendar': calendar, 'point_type': date_type1,
                     'point_normalised': '2001-06-01',
                     'point_certainty': self.tm.date_full_certainty}
        date = existence.create_date(date_data)
        date_part = date.point
        self.assertRaises(EATSValidationException,
                          self.authority.set_date_types, [])
        self.assertTrue(date_type1 in self.authority.get_date_types())
        self.authority.set_date_types([date_type1, date_type2])
        date_part.date_type = date_type2
        self.authority.set_date_types([date_type2])
        self.assertEqual(self.authority.get_date_types().count(), 1)
        self.assertTrue(date_type2 in self.authority.get_date_types())

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

    def test_change_entity_types (self):
        entity = self.tm.create_entity()
        entity_type1 = self.create_entity_type('person')
        entity_type2 = self.create_entity_type('place')
        self.authority.set_entity_types([entity_type1])
        assertion = entity.create_entity_type_property_assertion(
            self.authority, entity_type1)
        self.assertRaises(EATSValidationException,
                          self.authority.set_entity_types, [])
        self.assertTrue(entity_type1 in self.authority.get_entity_types())
        self.authority.set_entity_types([entity_type1, entity_type2])
        self.assertRaises(EATSValidationException,
                          self.authority.set_entity_types, [entity_type2])
        self.assertEqual(self.authority.get_entity_types().count(), 2)
        self.assertTrue(entity_type1 in self.authority.get_entity_types())
        self.assertTrue(entity_type2 in self.authority.get_entity_types())
        assertion.update(entity_type2)
        self.authority.set_entity_types([entity_type2])
        self.assertEqual(self.authority.get_entity_types().count(), 1)
        self.assertTrue(entity_type2 in self.authority.get_entity_types())

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

    def test_change_entity_relationship_types (self):
        entity1 = self.tm.create_entity()
        entity2 = self.tm.create_entity()
        type1 = self.create_entity_relationship_type(
            'is child of', 'is parent of')
        type2 = self.create_entity_relationship_type(
            'is born in', 'is place of birth of')
        self.authority.set_entity_relationship_types([type1])
        assertion = entity1.create_entity_relationship_property_assertion(
            self.authority, type1, entity1, entity2,
            self.tm.property_assertion_full_certainty)
        self.assertRaises(EATSValidationException,
                          self.authority.set_entity_relationship_types, [])
        self.assertTrue(type1 in self.authority.get_entity_relationship_types())
        self.authority.set_entity_relationship_types([type1, type2])
        self.assertRaises(EATSValidationException,
                          self.authority.set_entity_relationship_types, [type2])
        assertion.update(type2, entity1, entity2,
                         self.tm.property_assertion_no_certainty)
        self.authority.set_entity_relationship_types([type2])
        self.assertEqual(self.authority.get_entity_relationship_types().count(),
                         1)
        self.assertTrue(type2 in self.authority.get_entity_relationship_types())

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

    def test_change_languages (self):
        entity = self.tm.create_entity()
        language1 = self.create_language('English', 'en')
        language2 = self.create_language('French', 'fr')
        language3 = self.create_language('German', 'de')
        name_part_type = self.create_name_part_type('given')
        name_type = self.create_name_type('regular')
        script = self.create_script('Latin', 'Latn', ' ')
        self.authority.set_languages([language1])
        self.authority.set_name_part_types([name_part_type])
        self.authority.set_name_types([name_type])
        self.authority.set_scripts([script])
        # Test languages that are associated with a name.
        assertion = entity.create_name_property_assertion(
            self.authority, name_type, language1, script, 'Joan Mills')
        self.assertRaises(EATSValidationException,
                          self.authority.set_languages, [])
        self.assertEqual(self.authority.get_languages().count(), 1)
        self.assertTrue(language1 in self.authority.get_languages())
        self.authority.set_languages([language1, language2])
        self.assertRaises(EATSValidationException,
                          self.authority.set_languages, [language2])
        self.assertEqual(self.authority.get_languages().count(), 2)
        self.assertTrue(language1 in self.authority.get_languages())
        self.assertTrue(language2 in self.authority.get_languages())
        assertion.update(name_type, language2, script, 'Joan Mills', True)
        self.authority.set_languages([language2])
        self.assertEqual(self.authority.get_languages().count(), 1)
        self.assertTrue(language2 in self.authority.get_languages())
        # Test languages that are associated with a name part.
        self.authority.set_languages([language1, language2])
        self.assertEqual(self.authority.get_languages().count(), 2)
        self.assertTrue(language1 in self.authority.get_languages())
        self.assertTrue(language2 in self.authority.get_languages())
        name_part = assertion.name.create_name_part(
            name_part_type, language1, script, 'Joan', 1)
        self.assertRaises(EATSValidationException,
                          self.authority.set_languages, [language2])
        self.assertEqual(self.authority.get_languages().count(), 2)
        self.assertTrue(language1 in self.authority.get_languages())
        self.assertTrue(language2 in self.authority.get_languages())
        self.authority.set_languages([language1, language2, language3])
        name_part.language = language3
        self.authority.set_languages([language2, language3])
        self.assertEqual(self.authority.get_languages().count(), 2)
        self.assertTrue(language2 in self.authority.get_languages())
        self.assertTrue(language3 in self.authority.get_languages())

    def test_get_name_part_types (self):
        self.assertEqual(0, len(self.authority.get_name_part_types()))
        name_part_type1 = self.create_name_part_type('given')
        self.authority.set_name_part_types([name_part_type1])
        self.assertEqual(1, len(self.authority.get_name_part_types()))
        self.assertTrue(name_part_type1 in self.authority.get_name_part_types())
        name_part_type2 = self.create_name_part_type('family')
        self.authority.set_name_part_types([name_part_type1, name_part_type2])
        self.assertEqual(2, len(self.authority.get_name_part_types()))
        self.assertTrue(name_part_type1 in self.authority.get_name_part_types())
        self.assertTrue(name_part_type2 in self.authority.get_name_part_types())
        self.authority.set_name_part_types([name_part_type2])
        self.assertEqual(1, len(self.authority.get_name_part_types()))
        self.assertTrue(name_part_type2 in self.authority.get_name_part_types())
        self.authority.set_name_part_types([])
        self.assertEqual(0, len(self.authority.get_name_part_types()))

    def test_change_name_part_types (self):
        entity = self.tm.create_entity()
        name_type = self.create_name_type('regular')
        language = self.create_language('English', 'en')
        script = self.create_script('Latin', 'Latn', ' ')
        name_part_type1 = self.create_name_part_type('given')
        name_part_type2 = self.create_name_part_type('family')
        self.authority.set_name_part_types([name_part_type1])
        self.authority.set_name_types([name_type])
        self.authority.set_languages([language])
        self.authority.set_scripts([script])
        assertion = entity.create_name_property_assertion(
            self.authority, name_type, language, script, 'Joan Mills')
        name_part = assertion.name.create_name_part(
            name_part_type1, language, script, 'Joan', 1)
        self.assertRaises(EATSValidationException,
                          self.authority.set_name_part_types, [])
        self.assertTrue(name_part_type1 in self.authority.get_name_part_types())
        self.authority.set_name_part_types([name_part_type1, name_part_type2])
        self.assertRaises(EATSValidationException,
                          self.authority.set_name_part_types, [name_part_type2])
        self.assertTrue(name_part_type1 in self.authority.get_name_part_types())
        self.assertTrue(name_part_type2 in self.authority.get_name_part_types())
        name_part.name_part_type = name_part_type2
        self.authority.set_name_part_types([name_part_type2])
        self.assertEqual(self.authority.get_name_part_types().count(), 1)
        self.assertTrue(name_part_type2 in self.authority.get_name_part_types())

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

    def test_change_name_types (self):
        entity = self.tm.create_entity()
        name_type1 = self.create_name_type('regular')
        name_type2 = self.create_name_type('pseudonym')
        language = self.create_language('English', 'en')
        script = self.create_script('Latin', 'Latn', ' ')
        self.authority.set_name_types([name_type1])
        self.authority.set_languages([language])
        self.authority.set_scripts([script])
        assertion = entity.create_name_property_assertion(
            self.authority, name_type1, language, script, 'Joan Mills')
        self.assertRaises(EATSValidationException,
                          self.authority.set_name_types, [])
        self.assertTrue(name_type1 in self.authority.get_name_types())
        self.authority.set_name_types([name_type1, name_type2])
        self.assertRaises(EATSValidationException,
                          self.authority.set_name_types, [])
        self.assertEqual(self.authority.get_name_types().count(), 2)
        self.assertTrue(name_type1 in self.authority.get_name_types())
        self.assertTrue(name_type2 in self.authority.get_name_types())
        assertion.update(name_type2, language, script, 'Joan Mills', True)
        self.authority.set_name_types([name_type2])
        self.assertEqual(self.authority.get_name_types().count(), 1)
        self.assertTrue(name_type2 in self.authority.get_name_types())

    def test_get_scripts (self):
        self.assertEqual(0, len(self.authority.get_scripts()))
        script1 = self.create_script('Latin', 'Latn', ' ')
        self.authority.set_scripts([script1])
        self.assertEqual(1, len(self.authority.get_scripts()))
        self.assertTrue(script1 in self.authority.get_scripts())
        script2 = self.create_script('Arabic', 'Arab', ' ')
        self.authority.set_scripts([script1, script2])
        self.assertEqual(2, len(self.authority.get_scripts()))
        self.assertTrue(script1 in self.authority.get_scripts())
        self.assertTrue(script2 in self.authority.get_scripts())
        self.authority.set_scripts([script2])
        self.assertEqual(1, len(self.authority.get_scripts()))
        self.assertTrue(script2 in self.authority.get_scripts())
        self.authority.set_scripts([])
        self.assertEqual(0, len(self.authority.get_scripts()))

    def test_change_scripts (self):
        entity = self.tm.create_entity()
        language = self.create_language('English', 'en')
        name_part_type = self.create_name_part_type('given')
        name_type = self.create_name_type('regular')
        script1 = self.create_script('Latin', 'Latn', ' ')
        script2 = self.create_script('Arabic', 'Arab', ' ')
        script3 = self.create_script('Gujarati', 'Gujr', ' ')
        self.authority.set_languages([language])
        self.authority.set_name_part_types([name_part_type])
        self.authority.set_name_types([name_type])
        self.authority.set_scripts([script1])
        # Test scripts that are associated with a name.
        assertion = entity.create_name_property_assertion(
            self.authority, name_type, language, script1, 'Joan Mills')
        self.assertRaises(EATSValidationException,
                          self.authority.set_scripts, [])
        self.assertEqual(self.authority.get_scripts().count(), 1)
        self.assertTrue(script1 in self.authority.get_scripts())
        self.authority.set_scripts([script1, script2])
        self.assertRaises(EATSValidationException,
                          self.authority.set_scripts, [])
        self.assertEqual(self.authority.get_scripts().count(), 2)
        self.assertTrue(script1 in self.authority.get_scripts())
        self.assertTrue(script2 in self.authority.get_scripts())
        assertion.update(name_type, language, script2, 'Joan Mills', True)
        self.authority.set_scripts([script2])
        self.assertEqual(self.authority.get_scripts().count(), 1)
        self.assertTrue(script2 in self.authority.get_scripts())
        # Test scripts that are associated with a name part.
        self.authority.set_scripts([script1, script2])
        self.assertEqual(self.authority.get_scripts().count(), 2)
        self.assertTrue(script1 in self.authority.get_scripts())
        self.assertTrue(script2 in self.authority.get_scripts())
        name_part = assertion.name.create_name_part(
            name_part_type, language, script1, 'Joan', 1)
        self.assertRaises(EATSValidationException,
                          self.authority.set_scripts, [script2])
        self.assertEqual(self.authority.get_scripts().count(), 2)
        self.assertTrue(script1 in self.authority.get_scripts())
        self.assertTrue(script2 in self.authority.get_scripts())
        self.authority.set_scripts([script1, script2, script3])
        name_part.script = script3
        self.authority.set_scripts([script2, script3])
        self.assertEqual(self.authority.get_scripts().count(), 2)
        self.assertTrue(script2 in self.authority.get_scripts())
        self.assertTrue(script3 in self.authority.get_scripts())
